<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  fen: {
    type: String,
    required: true
  },
  orientation: {
    type: String,
    default: 'white'
  },
  legalMoves: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['move'])

// Helpers
const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
const ranks = ['8', '7', '6', '5', '4', '3', '2', '1']

const selectedSquare = ref(null)

const parseFen = (fen) => {
    const board = []
    const [placement] = fen.split(' ')
    const rows = placement.split('/')
    
    for (let r = 0; r < 8; r++) {
        const rowData = []
        const fenRow = rows[r]
        let col = 0
        for (let char of fenRow) {
            if (isNaN(char)) {
                // Piece
                const color = char === char.toUpperCase() ? 'w' : 'b'
                const type = char.toLowerCase()
                rowData.push({ type, color })
                col++
            } else {
                // Empty squares
                const emptyCount = parseInt(char)
                for (let k = 0; k < emptyCount; k++) {
                    rowData.push(null)
                    col++
                }
            }
        }
        board.push(rowData)
    }
    return board
}

const displayedBoard = computed(() => {
    const board = parseFen(props.fen)
    if (props.orientation === 'black') {
        return [...board].reverse().map(row => [...row].reverse())
    }
    return board
})

const getSquareName = (rowIndex, colIndex) => {
    let r = rowIndex
    let c = colIndex
    if (props.orientation === 'black') {
        r = 7 - rowIndex
        c = 7 - colIndex
    }
    return `${files[c]}${ranks[r]}`
}

const getPieceImage = (piece) => {
    if (!piece) return null
    const color = piece.color
    const type = piece.type.toUpperCase()
    // Using standard piece images
    const name = `${color}${type}`
    return `https://raw.githubusercontent.com/ornicar/lila/master/public/piece/cburnett/${name}.svg`
}

const getPossibleDestinations = (square) => {
    // Return list of target squares for the selected piece
    return props.legalMoves
        .filter(m => m.startsWith(square))
        .map(m => m.substring(2, 4)) // Extract target square (e2e4 -> e4) - Handling promotions? e7e8q
}

const isDestination = (square) => {
    if (!selectedSquare.value) return false
    const dests = getPossibleDestinations(selectedSquare.value)
    return dests.includes(square)
}

const handleSquareClick = (rowIndex, colIndex) => {
    const square = getSquareName(rowIndex, colIndex)
    const piece = displayedBoard.value[rowIndex][colIndex]
    
    // Check if clicking a valid move destination (executing move)
    if (selectedSquare.value && isDestination(square)) {
        // Find full move string
        const move = props.legalMoves.find(m => m.startsWith(selectedSquare.value) && m.includes(square))
        
        if (move) {
            emit('move', move)
            selectedSquare.value = null
        }
        return
    }
    
    // Selecting a piece
    if (piece) {
        const playerColorCode = props.orientation === 'white' ? 'w' : 'b'
        if (piece.color !== playerColorCode) {
            // Cannot select opponent's pieces
            selectedSquare.value = null
            return
        }
    }

    // Check if this square has any legal moves?
    const movesFromHere = props.legalMoves.filter(m => m.startsWith(square))
    if (movesFromHere.length > 0) {
        selectedSquare.value = square
    } else {
        selectedSquare.value = null
    }
}
</script>

<template>
  <div class="chessboard">
    <div 
        v-for="(row, rIndex) in displayedBoard" 
        :key="rIndex" 
        class="board-row"
    >
      <div 
        v-for="(square, cIndex) in row" 
        :key="cIndex"
        class="square"
        :class="[
            (rIndex + cIndex) % 2 === 0 ? 'light' : 'dark',
            { 'selected': selectedSquare === getSquareName(rIndex, cIndex) },
            { 'dest': isDestination(getSquareName(rIndex, cIndex)) }
        ]"
        @click="handleSquareClick(rIndex, cIndex)"
      >
        <img v-if="square" :src="getPieceImage(square)" class="piece" />
        <div v-if="isDestination(getSquareName(rIndex, cIndex))" class="move-hint"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chessboard {
    display: flex;
    flex-direction: column;
    border: 5px solid #484848;
    user-select: none;
    width: 100%;
    max-width: 600px;
    height: auto;
    aspect-ratio: 1 / 1;
}

.board-row {
    display: flex;
    flex: 1;
    width: 100%;
}

.square {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    cursor: pointer;
    aspect-ratio: 1 / 1; /* Enforce squareness per cell too */
}

.light {
    background-color: #f0d9b5;
}

.dark {
    background-color: #b58863;
}

.selected {
    background-color: rgba(123, 97, 255, 0.5) !important;
}

.dest {
    /* Potential destination */
}

.move-hint {
    position: absolute;
    width: 30%;
    height: 30%;
    background-color: rgba(0, 0, 0, 0.3);
    border-radius: 50%;
    pointer-events: none; /* Let clicks pass through to square */
}

.square:hover .move-hint {
    background-color: rgba(0, 0, 0, 0.5);
}

.piece {
    width: 100%;
    height: 100%;
    z-index: 2;
}
</style>
