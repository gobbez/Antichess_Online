<script setup>
import { onMounted, onUnmounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useGameStore } from '@/stores/game'
import { useUserStore } from '@/stores/user'
import ChessBoard from '@/components/ChessBoard.vue'

const route = useRoute()
const gameStore = useGameStore()
const userStore = useUserStore()

const gameId = route.params.id

onMounted(() => {
  gameStore.connect(gameId)
})

onUnmounted(() => {
  gameStore.disconnect()
})

const game = computed(() => gameStore.currentGame)
const playerColor = computed(() => {
    if (!game.value || !userStore.user) return 'white'
    if (game.value.black_player && game.value.black_player.id === userStore.user.id) return 'black'
    return 'white'
})

const gameStatus = computed(() => {
    if (!game.value) return 'Loading...'
    if (game.value.status === 'waiting') return 'Waiting for opponent...'
    if (game.value.status === 'finished') return 'Game Over'
    const turn = game.value.fen.split(' ')[1] === 'w' ? 'White' : 'Black'
    return `${turn} to move`
})

const handleMove = (moveUci) => {
    gameStore.sendMove(moveUci)
}

// Timer mock (visual only, synced loosely with server times later if needed)
// Realtime implementation would require server timestmaps
</script>

<template>
  <div class="game-view" v-if="game">
    <div class="game-container">
       <div class="opponent-info" v-if="playerColor === 'white' && game.black_player">
           <div class="user-strip">
               <span class="username">{{ game.black_player.username }}</span>
               <span class="elo">({{ game.black_player.profile?.elo || 1500 }})</span>
           </div>
       </div>
       <div class="opponent-info" v-else-if="playerColor === 'black' && game.white_player">
           <div class="user-strip">
               <span class="username">{{ game.white_player.username }}</span>
               <span class="elo">({{ game.white_player.profile?.elo || 1500 }})</span>
           </div>
       </div>
       <div class="opponent-info" v-else>
           Waiting...
       </div>


       <ChessBoard 
         :fen="game.fen" 
         :orientation="playerColor"
         :legalMoves="game.legal_moves"
         @move="handleMove"
       />
       
       <div class="player-info">
           <div class="user-strip">
               <span class="username">{{ userStore.user.username }}</span>
               <span class="elo">({{ userStore.user.profile?.elo }})</span>
           </div>
       </div>
    </div>
    
    <div class="sidebar">
        <div class="card game-status">
            <h3>{{ gameStatus }}</h3>
        </div>
        
        <div class="card move-list">
            <h4>Moves</h4>
            <div class="pgn-display">{{ game.pgn || 'No moves yet' }}</div>
        </div>
    </div>
  </div>
</template>

<style scoped>
.game-view {
    display: flex;
    gap: var(--spacing-lg);
    justify-content: center;
    align-items: flex-start;
}

.game-container {
    flex: 2;
    max-width: 600px;
}

.sidebar {
    flex: 1;
    max-width: 300px;
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
}

.user-strip {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 0;
    font-size: 1.2rem;
}

.username {
    font-weight: bold;
}

.elo {
    color: var(--color-text-muted);
}

.pgn-display {
    font-family: monospace;
    white-space: pre-wrap;
    max-height: 300px;
    overflow-y: auto;
    background-color: #222;
    padding: 10px;
    border-radius: 4px;
}

@media (max-width: 800px) {
    .game-view {
        flex-direction: column;
        align-items: center;
    }
    .game-container, .sidebar {
        width: 100%;
        max-width: 100%;
    }
}
</style>
