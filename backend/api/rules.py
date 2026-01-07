import chess
import chess.variant

def get_initial_fen():
    board = chess.variant.AntichessBoard()
    return board.fen()

def make_move(fen, move_uci):
    """
    Apply a move to the board state in FEN.
    Returns new FEN and standard algebraic notation of the move.
    """
    board = chess.variant.AntichessBoard(fen)
    move = chess.Move.from_uci(move_uci)
    
    if move in board.legal_moves:
        san = board.san(move)
        board.push(move)
        return board.fen(), san, None
    else:
        return fen, None, "Illegal move"

def get_legal_moves(fen):
    board = chess.variant.AntichessBoard(fen)
    return [move.uci() for move in board.legal_moves]

def is_game_over(fen):
    board = chess.variant.AntichessBoard(fen)
    return board.is_game_over()

def get_game_result(fen):
    board = chess.variant.AntichessBoard(fen)
    if board.is_game_over():
        return board.result()
    return None

def calculate_elo(white_elo, black_elo, result):
    """
    Result: 1 (White wins), 0 (Black wins), 0.5 (Draw)
    Returns: (new_white_elo, new_black_elo)
    """
    K = 40 # High K-factor for volatility as requested (or standard for casual site)
    
    # Expected scores
    E_white = 1 / (1 + 10 ** ((black_elo - white_elo) / 400))
    E_black = 1 / (1 + 10 ** ((white_elo - black_elo) / 400))
    
    # New Elos
    new_white_elo = round(white_elo + K * (result - E_white))
    new_black_elo = round(black_elo + K * ((1 - result) - E_black))
    
    return new_white_elo, new_black_elo
