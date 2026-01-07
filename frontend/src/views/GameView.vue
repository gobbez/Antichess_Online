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
         :legal-moves="game.legal_moves"
         @move="handleMove"
       />
       
       <div class="player-info">
           <div class="user-strip">
               <span class="username">{{ userStore.user.username }}</span>
               <span class="elo">({{ userStore.user.profile?.elo }})</span>
           </div>
       </div>

       <div v-if="game.status === 'finished'" class="game-over-overlay">
           <h2>Game Over</h2>
           <p v-if="game.winner">Winner: {{ game.winner === userStore.user.id ? 'You' : 'Opponent' }}</p>
           <p v-else>Draw</p>
           <button class="btn btn-primary" @click="$router.push('/')">Back to Home</button>
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
  
  <div v-if="gameStore.error" class="error-toast">
      {{ gameStore.error }}
  </div>
</template>

<style scoped>
.error-toast {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background-color: #ff4444;
    color: white;
    padding: 1rem 2rem;
    border-radius: 4px;
    z-index: 100;
    font-weight: bold;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    animation: fadeIn 0.3s, fadeOut 0.3s 2.7s forwards;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translate(-50%, -20px); }
    to { opacity: 1; transform: translate(-50%, 0); }
}

@keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
}


.game-view {
    display: flex;
    gap: var(--spacing-lg);
    justify-content: center;
    align-items: flex-start;
}

.game-container {
    flex: 2;
    max-width: 600px;
    position: relative;
}

.game-over-overlay {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: rgba(0,0,0,0.85);
    padding: 2rem;
    border-radius: var(--radius-md);
    text-align: center;
    border: 1px solid var(--color-primary);
    z-index: 10;
}
.game-over-overlay h2 {
    color: var(--color-primary);
    margin-top: 0;
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
