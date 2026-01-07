<script setup>
import { RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
</script>

<template>
  <div class="app-layout">
    <header class="main-header">
      <div class="container header-content">
        <div class="logo">
          <h1>
            <router-link to="/">Antichess Online</router-link>
          </h1>
          <span class="subtitle">The suicide chess variant</span>
        </div>
        
        <nav>
          <router-link to="/">Play</router-link>
          <template v-if="userStore.isAuthenticated">
            <router-link to="/profile">Profile</router-link>
            <a href="#" @click.prevent="userStore.logout">Logout</a>
          </template>
          <template v-else>
            <router-link to="/login">Login</router-link>
            <router-link to="/register">Register</router-link>
          </template>
        </nav>
      </div>
    </header>

    <main class="main-content container">
      <RouterView />
    </main>

    <footer class="main-footer">
      <div class="container">
        <p>Created by Andrea Gobbetti</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-header {
  background-color: var(--color-surface);
  padding: var(--spacing-md) 0;
  box-shadow: var(--shadow-md);
  margin-bottom: var(--spacing-lg);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo h1 {
  margin: 0;
  font-size: 1.5rem;
}

.logo a {
  color: var(--color-text);
}

.subtitle {
  font-size: 0.8rem;
  color: var(--color-text-muted);
  display: block;
}

nav {
  display: flex;
  gap: var(--spacing-md);
}

nav a {
  font-weight: 500;
  color: var(--color-text);
}

nav a.router-link-active {
  color: var(--color-primary);
}

.main-content {
  flex: 1;
}

.main-footer {
  margin-top: var(--spacing-lg);
  padding: var(--spacing-md) 0;
  text-align: center;
  color: var(--color-text-muted);
  font-size: 0.9rem;
}
</style>
