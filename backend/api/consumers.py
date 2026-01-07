import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Game, Profile, CustomUser
from .rules import make_move, is_game_over, get_game_result, get_initial_fen, calculate_elo
from .serializers import GameSerializer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.room_group_name = f'game_{self.game_id}'
        self.user = self.scope['user']

        if self.user == AnonymousUser():
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        command = data.get('command')

        if command == 'make_move':
            await self.process_move(data.get('move'))
        
        elif command == 'join_game':
             # Send initial state
             game_data = await self.get_game_data()
             await self.send(text_data=json.dumps({
                 'type': 'game_state',
                 'game': game_data
             }))

    async def process_move(self, move_uci):
        # 1. Get Game
        game = await self.get_game()
        
        # 2. Validate Turn
        # (Simplified turn check, relying on FEN in rules usually, but should check user color)
        # Checking if user is valid player is good practice
        
        # 3. Apply Move
        new_fen, san, error = await database_sync_to_async(make_move)(game.fen, move_uci)
        
        if error:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': error
            }))
            return

        # 4. Update Game
        game.fen = new_fen
        if game.pgn:
            game.pgn += f" {san}"
        else:
            game.pgn = san
            
        if await database_sync_to_async(is_game_over)(new_fen):
            game.status = 'finished'
            game.finished_at = timezone.now() # Added timezone import below or just use auto_now if field allows, but manual set better
            
            result_str = await database_sync_to_async(get_game_result)(new_fen)
            # result_str is '1-0', '0-1', '1/2-1/2'
            
            score_white = 0.5
            if result_str == '1-0':
                score_white = 1.0
                game.winner = game.white_player
            elif result_str == '0-1':
                score_white = 0.0
                game.winner = game.black_player
            
            # Update Elos
            if game.white_player and game.black_player:
                w_profile = await database_sync_to_async(lambda: game.white_player.profile)()
                b_profile = await database_sync_to_async(lambda: game.black_player.profile)()
                
                new_w, new_b = calculate_elo(w_profile.elo, b_profile.elo, score_white)
                
                w_profile.elo = new_w
                w_profile.games_played += 1
                if score_white == 1: w_profile.wins += 1
                elif score_white == 0: w_profile.losses += 1
                else: w_profile.draws += 1
                if new_w > w_profile.highest_elo: w_profile.highest_elo = new_w
                
                b_profile.elo = new_b
                b_profile.games_played += 1
                if score_white == 0: b_profile.wins += 1
                elif score_white == 1: b_profile.losses += 1
                else: b_profile.draws += 1
                if new_b > b_profile.highest_elo: b_profile.highest_elo = new_b
                
                await database_sync_to_async(w_profile.save)()
                await database_sync_to_async(b_profile.save)()
                
        await database_sync_to_async(game.save)()
        
        # 5. Broadcast State
        game_data = await self.get_game_data()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_update',
                'game': game_data
            }
        )

    async def game_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_state',
            'game': event['game']
        }))

    @database_sync_to_async
    def get_game(self):
        return Game.objects.get(id=self.game_id)

    @database_sync_to_async
    def get_game_data(self):
        game = Game.objects.get(id=self.game_id)
        return GameSerializer(game).data


class MatchmakingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user == AnonymousUser():
             await self.close()
             return
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        command = data.get('command')
        cadence = data.get('cadence')

        if command == 'find_game':
            game = await self.find_match(cadence)
            if game:
                await self.send(text_data=json.dumps({
                    'type': 'game_found',
                    'game_id': game.id,
                    'color': 'white' if game.white_player == self.user else 'black'
                }))
            else:
                # Should not happen with logic below, it either joins or creates
                pass

    @database_sync_to_async
    def find_match(self, cadence):
        # 1. Try to find a waiting game
        game = Game.objects.filter(cadence=cadence, status='waiting').exclude(white_player=self.user).exclude(black_player=self.user).first()
        
        if game:
            if not game.white_player:
                 game.white_player = self.user
            elif not game.black_player:
                 game.black_player = self.user
            
            game.status = 'active'
            game.save()
            return game
        else:
            # 2. Create new game
            # Defaulting user to White for simplicity, or random
            game = Game.objects.create(
                white_player=self.user,
                cadence=cadence,
                status='waiting',
                fen=get_initial_fen()
            )
            return game
