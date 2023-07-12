import chess
from stockfish import Stockfish

stockfish = Stockfish(path="stockfish.exe", depth=2)

piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K' : 2000}

def square_to_row_col(square):
    row = 7 - (square // 8)  # Calculate the row
    col = square % 8  # Calculate the column
    return [row, col]

def legal_moves(fen):
    board = chess.Board(fen)
    list = []
    for move in board.legal_moves:
        temp = []
        temp += square_to_row_col(move.from_square)
        temp += square_to_row_col(move.to_square)
        
        if move.promotion == chess.KNIGHT:
            temp.append('n')
        elif move.promotion == chess.BISHOP:
            temp.append('b')
        elif move.promotion == chess.ROOK:
            temp.append('r')
        elif move.promotion == chess.QUEEN:
            temp.append('q')
        else :
            temp.append('#')

        list.append(temp)
    return list

def get_piece_from_fen(fen, start_row, start_col):
    board = chess.Board(fen)
    square = chess.square(start_col, 7 - start_row)  # Convert to internal square representation
    piece = board.piece_at(square)
    if piece is not None:
        return piece.symbol()
    else:
        return None

def evaluate_capture(move, fen):
    capturing_piece = get_piece_from_fen(fen, move[0], move[1])
    captured_piece = get_piece_from_fen(fen, move[2], move[3])

    if captured_piece == None:
        return 0

    capturing_color = capturing_piece.isupper()
    captured_color = captured_piece.isupper()
    
    return piece_values[captured_piece.upper()] - piece_values[capturing_piece.upper()]

def sorted_moves_by_mvv_lva(fen) :    # Most valueable victim - Least valuable Attacker
    lm = legal_moves(fen)
    sorted_moves = sorted(lm, key = lambda x : evaluate_capture(x, fen), reverse=True)
    return sorted_moves

'''Here I can use my own custom evaluation function but for now I am going with Stockfish's evaluation with depth 4'''
def evaluate_position(fen):
    stockfish.set_fen_position(fen)
    evaluation =  stockfish.get_evaluation()
    if evaluation["type"] == "cp" :
        return evaluation["value"]
    else :
        if evaluation["value"] > 0:
            return (5-evaluation["value"])*2000
        elif evaluation["value"] < 0 :
            return (-1)*(5+evaluation["value"])*2000
        else :
            if(fen.split()[1] == "w") :
                return -100000
            else :
                return 100000

# fen = "r1bqk2r/ppp2ppp/2n5/1B1pP3/3P4/5N2/PP1n1PPP/R2QK2R w KQkq - 0 11"
# evaluation = evaluate_position(fen)
# print("Position evaluation:", evaluation)