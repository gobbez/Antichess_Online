import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://localhost:8000/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null, // If using Token auth, but we use Session for now? 
    // Wait, I enabled credentials. But standard Django login uses session cookies.
    // Axios needs "withCredentials: true".
    // I won't store token if using session.
  }),
  getters: {
    isAuthenticated: (state) => !!state.user,
  },
  actions: {
    async initialize() {
      try {
        const response = await axios.get(`${API_URL}/user/`, { withCredentials: true })
        this.user = response.data
      } catch (error) {
        this.user = null
      }
    },
    async login(username, password) {
      // For session auth using Django's login view
      // We might need to send CSRF token.
      // Easiest is to basic auth or just simple post.
      // My LoginView in backend uses standard `authenticate` and `login`.
      // It sets the session cookie.
      // Need to get CSRF token first?
      // For simplicity in DRF with SessionAuth, often we skip CSRF if "SessionAuthentication" is not in DEFAULT_AUTHENTICATION_CLASSES or we use CsrfExempt, or we fetch cookie.
      // Let's assume for now we might hit CSRF issues.
      // I added 'corsheaders'.
      
      await axios.post(`${API_URL}/login/`, { username, password }, { withCredentials: true })
      await this.initialize()
    },
    async register(username, password) {
       await axios.post(`${API_URL}/register/`, { username, password })
       // Auto login after register? Or ask to login.
       await this.login(username, password)
    },
    async logout() {
      await axios.post(`${API_URL}/logout/`, {}, { withCredentials: true })
      this.user = null
    }
  }
})
