<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const userStore = useUserStore()
const router = useRouter()

const handleLogin = async () => {
  error.value = ''
  try {
    await userStore.login(username.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = 'Invalid username or password'
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="card auth-card">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Username</label>
          <input v-model="username" type="text" required />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input v-model="password" type="password" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.auth-card {
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: var(--spacing-md);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-sm);
  color: var(--color-text-muted);
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border-radius: var(--radius-sm);
  border: 1px solid #333;
  background-color: var(--color-bg);
  color: var(--color-text);
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.error {
  color: #cf6679;
  font-size: 0.9rem;
}

h2 {
  margin-top: 0;
  text-align: center;
  color: var(--color-primary);
}

button {
  width: 100%;
  margin-top: var(--spacing-md);
}
</style>
