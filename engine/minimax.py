from move_generator import evaluate_position
from move_generator import legal_moves
from move_generator import sorted_moves_by_mvv_lva
from fen import generate_new_fen
import time
import chess

def is_checkmate(fen):
    board = chess.Board(fen)
    return board.is_checkmate(), board.is_stalemate()

def convert_move_to_notation(fen, move):
    board = chess.Board(fen)
    chess_move = chess.Move(from_square=chess.square(move[1], 7-move[0]),
                            to_square=chess.square(move[3], 7-move[2]))
    return board.san(chess_move)

def minimax(fen, depth, alpha, beta, maximizing_player):
    global count
    is_cm, is_sm = is_checkmate(fen)

    if depth == 0 or is_cm == True or is_sm == True:
        '''This is done in order to reach the mate fastest'''
        if is_cm == True :
            if(fen.split()[1] == 'b'):
                return evaluate_position(fen)+depth, None
            else :
                return evaluate_position(fen)-depth, None 
            
        if is_sm == True :
            return 0, None
        
        return evaluate_position(fen), None

    best_move = None

    if maximizing_player:
        max_eval = -1000000
        moves = sorted_moves_by_mvv_lva(fen)
        for move in moves:
            new_fen = generate_new_fen(fen, move)
            score, _ = minimax(new_fen, depth-1, alpha, beta, False)
            if score > max_eval:
                max_eval = score
                best_move = move
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                break
        return max_eval, best_move
    else:
        min_eval = 1000000
        moves = sorted_moves_by_mvv_lva(fen)
        for move in moves:
            new_fen = generate_new_fen(fen, move)
            score, _ = minimax(new_fen, depth-1, alpha, beta, True)
            if score < min_eval:
                min_eval = score
                best_move = move
            beta = min(beta, min_eval)
            if alpha >= beta:
                break
        return min_eval, best_move

# fen = "8/3K4/P6p/1Q6/2B3P1/k5bP/8/8 w - - 5 88"

# start_time = time.time();
# evaluation, best_move = minimax(fen, 4, -1000000, 1000000, True)
# elapsed_time = time.time() - start_time

# print("Evaluation : ", evaluation)
# print("Best Move : ", best_move)
# print(convert_move_to_notation(fen, best_move))
# print("Time : ", elapsed_time)