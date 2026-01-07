<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const user = computed(() => userStore.user)
</script>

<template>
  <div class="profile-page" v-if="user">
    <div class="profile-header card">
      <div class="avatar-section">
        <div class="avatar-placeholder" v-if="!user.profile.avatar">{{ user.username[0].toUpperCase() }}</div>
        <img v-else :src="user.profile.avatar" alt="Avatar" class="avatar" />
        <button class="btn-small">Change Picture</button>
      </div>
      
      <div class="info-section">
        <h2>{{ user.username }}</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="label">Current Elo</span>
            <span class="value">{{ user.profile.elo }}</span>
          </div>
          <div class="stat-item">
            <span class="label">Highest Elo</span>
            <span class="value">{{ user.profile.highest_elo }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="stats-details card">
      <h3>Performance</h3>
      <div class="stats-row">
        <div class="stat-box wins">
          <span class="count">{{ user.profile.wins }}</span>
          <span class="type">Wins</span>
        </div>
        <div class="stat-box losses">
          <span class="count">{{ user.profile.losses }}</span>
          <span class="type">Losses</span>
        </div>
        <div class="stat-box draws">
          <span class="count">{{ user.profile.draws }}</span>
          <span class="type">Draws</span>
        </div>
        <div class="stat-box games">
          <span class="count">{{ user.profile.games_played }}</span>
          <span class="type">Total</span>
        </div>
      </div>
      
      <!-- Placeholder for Elo Graph -->
      <div class="elo-graph">
        <h4>Elo History</h4>
        <div class="graph-placeholder">
          Graph coming soon...
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  max-width: 800px;
  margin: 0 auto;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.avatar-placeholder {
  width: 100px;
  height: 100px;
  background-color: var(--color-primary);
  color: #000;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 3rem;
  font-weight: bold;
}

.info-section h2 {
  margin-top: 0;
  font-size: 2rem;
}

.stats-grid {
  display: flex;
  gap: var(--spacing-lg);
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-item .label {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.stat-item .value {
  font-size: 1.5rem;
  font-weight: bold;
}

.stats-details h3 {
  margin-top: 0;
}

.stats-row {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.stat-box {
  flex: 1;
  background-color: var(--color-bg);
  padding: var(--spacing-md);
  border-radius: var(--radius-sm);
  text-align: center;
}

.stat-box .count {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
}

.stat-box .type {
  color: var(--color-text-muted);
  font-size: 0.8rem;
}

.graph-placeholder {
  height: 200px;
  background-color: var(--color-bg);
  display: flex;
  justify-content: center;
  align-items: center;
  color: var(--color-text-muted);
  border-radius: var(--radius-sm);
}

.btn-small {
  margin-top: var(--spacing-sm);
  background: none;
  border: 1px solid var(--color-text-muted);
  color: var(--color-text-muted);
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 0.8rem;
}
</style>
