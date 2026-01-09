<script setup>
import { ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const router = useRouter()
const searching = ref(false)
const selectedCadence = ref('1+0')

let socket = null

const startSearch = () => {
  if (!userStore.isAuthenticated) {
    router.push('/login')
    return
  }
  
  searching.value = true
  
  let wsUrl
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    wsUrl = 'ws://127.0.0.1:8000/ws/matchmaking/'
  } else {
    wsUrl = 'wss://antichess-online.onrender.com/ws/matchmaking/'
  }
  socket = new WebSocket(wsUrl)
  
  socket.onopen = () => {
    socket.send(JSON.stringify({
      command: 'find_game',
      cadence: selectedCadence.value
    }))
  }
  
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.type === 'game_found') {
      router.push(`/game/${data.game_id}`)
    }
  }
}

const cancelSearch = () => {
  if (socket) {
    socket.close()
  }
  searching.value = false
}

onUnmounted(() => {
  if (socket) {
    socket.close()
  }
})

const cadences = ['1+0', '2+1', '3+0', '5+0']
</script>

<template>
  <div class="home-page">
    <div class="hero">
      <h2>Play Antichess</h2>
      <p>Lose all your pieces to win! The ultimate lose-all chess variant.</p>
    </div>
    
    <div class="game-selector card">
      <h3>Quick Pairing</h3>
      
      <div class="cadence-grid">
        <button 
          v-for="cadence in cadences" 
          :key="cadence"
          class="cadence-btn"
          :class="{ active: selectedCadence === cadence }"
          @click="selectedCadence = cadence"
          :disabled="searching"
        >
          {{ cadence }}
        </button>
      </div>
      
      <div class="action-area">
        <button v-if="!searching" class="btn btn-primary btn-large" @click="startSearch">
          Find Game
        </button>
        <button v-else class="btn btn-secondary btn-large" @click="cancelSearch">
          <span class="spinner"></span> Searching...
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
  padding-top: var(--spacing-lg);
}

.hero {
  text-align: center;
}

.hero h2 {
  font-size: 3rem;
  margin-bottom: var(--spacing-sm);
  background: linear-gradient(45deg, var(--color-primary), var(--color-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.game-selector {
  width: 100%;
  max-width: 500px;
  text-align: center;
}

.cadence-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
  margin: var(--spacing-lg) 0;
}

.cadence-btn {
  background-color: var(--color-bg);
  border: 2px solid transparent;
  color: var(--color-text);
  padding: 1.5rem;
  font-size: 1.5rem;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.cadence-btn:hover {
  border-color: var(--color-primary);
  transform: translateY(-2px);
}

.cadence-btn.active {
  border-color: var(--color-primary);
  background-color: rgba(187, 134, 252, 0.1);
}

.btn-large {
  width: 100%;
  font-size: 1.2rem;
  padding: 1rem;
}

.btn-secondary {
  background-color: var(--color-surface-hover);
  color: var(--color-text);
}

.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255,255,255,.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
  margin-right: 10px;
  vertical-align: middle;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
