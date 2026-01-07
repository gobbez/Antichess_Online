---
trigger: always_on
---

# Description
Antichess variant website with an intuitive, user-friendly and responsive modern design for both the chessboard and whole website.

# Website
Modern website, similar to Lichess, with these functionalities:
-user login (username, password)
-user profile: with details like username, profile pic (that is changeable), Elo graph over time, highest elo and current active game (if any)
-title and header: Antichess Online (and add a short secondary text below it)
-game-cadence: 1'+0" | 2'+1" | 3'+0" | 5'+0"
-in the footer: mention that the game is created by Andrea Gobbetti

# Game
The game is about Antichess variant, not standard chess. 
When the user clicks on a new game (pvp) at a certain game-cadence (1'+0" | 2'+1" | 3'+0" | 5'+0"), a search icon will be displayed and it will search a random user that is also searching for a game of that cadence. 
Then the chessboard is created (from starting position) and both players see it real-time and the time is set (and the user that must play will have its timer start, and pauses when he makes a move). The game will follow Antichess rules for everything (the moving pieces, captures and final result, etc). The move played is visible by both player in real time. 
If a player finishes its time, then the game is lost for him.
When the game finishes, a screen will be displayed showing the Elo of each player adjusted by the gains or loss in their Elo (following Elo rules). 
Every player starts the first game with 1500 Elo.

The game chessboard allows the user to click to a piece and every possible move will be displayed (the possible move-cells will become lighter/brighter). If the user clicks on a possible move-cell (after clicking a piece), then that move will be effective and the chessboard is adjusted with the new move. If the user clicks on a piece and then clicks on a illegal move, then that pieces is not pressed anymore and no move are made (the user will have to click a piece again and click on a valid move).
Every move made in the game are displayed on the right of the screen, similar to Lichess board and it is possible to copy all the moves made so far, in the move_nr. move_notation format (example: 1. Nf3; Nf6). 

Above the chessboard there will be the opponent username with its Elo and a number (positive or negative) with the score of the game (following chess pieces scores, like +10 for queen, etc), that is the sum of captured pieces / lost pieces.

# Tech-Stack
Use Python Django for backend and Vue.js (and css) for frontend

# Images
Get the right images for the chessboard, its up to you where to find them (a possibility could be use the Python chess module for the chessboard/pieces).