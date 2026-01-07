from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Game, Profile
from .rules import calculate_elo, make_move, is_game_over

User = get_user_model()

class AntichessTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='player1', password='password')
        Profile.objects.create(user=self.user1)
        self.user2 = User.objects.create_user(username='player2', password='password')
        Profile.objects.create(user=self.user2)

    def test_user_profile_creation(self):
        self.assertEqual(self.user1.profile.elo, 1500)

    def test_calculate_elo(self):
        # White wins, equal elo
        w, b = calculate_elo(1500, 1500, 1)
        self.assertTrue(w > 1500)
        self.assertTrue(b < 1500)
        self.assertEqual(w, 1520) # K=40, result=1, E=0.5 -> 1500 + 40*0.5 = 1520
        self.assertEqual(b, 1480)

    def test_game_creation_and_move(self):
        game = Game.objects.create(white_player=self.user1, black_player=self.user2, cadence='1+0')
        self.assertEqual(game.fen, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        
        # Test standard move e3 (antichess common opening)
        new_fen, san, error = make_move(game.fen, 'e2e3')
        self.assertIsNone(error)
        self.assertNotEqual(new_fen, game.fen)
        self.assertEqual(san, 'e3')
        
    def test_antichess_capture_logic(self):
        # Setup board where capture is forced (or verify library handles it)
        # Antichess starting position: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        # 1. e3 b5 2. Bxb5 (forced?)
        # Let's interact with python-chess via rules
        
        fen1, _, _ = make_move('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'e2e3')
        fen2, _, _ = make_move(fen1, 'b7b5')
        
        # Now white bishop on f1 can take b5. Is it forced?
        # In antichess, if you can capture, you must.
        # Valid moves for white?
        import chess.variant
        board = chess.variant.AntichessBoard(fen2)
        legal_moves = [m.uci() for m in board.legal_moves]
        
        self.assertIn('f1b5', legal_moves)
        # Check if non-captures are excluded if capture is available
        # Need to know if this specific position has forced capture.
        # Yes, Bxb5 is available. Is there any other capture? 
        # No other pieces can capture. So ONLY captures are allowed.
        # Are there other captures? No.
        # So 'f1b5' should be the ONLY legal move?
        # Let's verify.
        
        # Actually e3 can also move but can it capture? No.
        # So only f1b5 should be legal.
        self.assertEqual(len(legal_moves), 1)
        self.assertEqual(legal_moves[0], 'f1b5')

