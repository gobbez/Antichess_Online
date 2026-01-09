import { defineStore } from 'pinia'

export const useGameStore = defineStore('game', {
    state: () => ({
        currentGame: null,
        socket: null,
        isConnected: false,
        error: null
    }),
    actions: {
        connect(gameId) {
            if (this.socket) {
                this.socket.close()
            }

            let wsUrl
            if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
                wsUrl = 'ws://127.0.0.1:8000/ws/game/' + gameId + '/'
            } else {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
                wsUrl = `${protocol}//${window.location.host}/ws/game/${gameId}/`
            }

            this.socket = new WebSocket(wsUrl)

            this.socket.onopen = () => {
                this.isConnected = true
                console.log("Connected to game socket")
                this.socket.send(JSON.stringify({ command: 'join_game' }))
            }

            this.socket.onmessage = (event) => {
                const data = JSON.parse(event.data)
                if (data.type === 'game_state' || data.type === 'game_update') {
                    this.currentGame = data.game
                } else if (data.type === 'error') {
                    console.error("Game error:", data.message)
                    this.error = data.message
                    setTimeout(() => this.error = null, 3000)
                }
            }

            this.socket.onclose = () => {
                this.isConnected = false
                this.currentGame = null
            }
        },
        sendMove(moveUci) {
            if (this.socket && this.isConnected) {
                this.socket.send(JSON.stringify({
                    command: 'make_move',
                    move: moveUci
                }))
            }
        },
        disconnect() {
            if (this.socket) {
                this.socket.close()
            }
        }
    }
})
