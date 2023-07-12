import chess
from minimax import minimax
from fen import generate_new_fen

def is_checkmate(fen):
    board = chess.Board(fen)
    return board.is_checkmate()

def is_stalemate(fen):
    board = chess.Board(fen)
    return board.is_stalemate()

def convert_move_to_notation(fen, move):
    board = chess.Board(fen)
    chess_move = chess.Move(from_square=chess.square(move[1], 7-move[0]),
                            to_square=chess.square(move[3], 7-move[2]))
    
    string = board.san(chess_move)

    piece_type = board.piece_type_at(square=chess.square(move[1], 7-move[0]))
    if piece_type == chess.PAWN:
        if move[2] == 0 or move[2] == 7:
            string += "="
            string += move[4].upper()

    return string

fen = "r3k2r/4qb2/p1ppnp2/Pp2p1p1/4P2p/3PBP1P/1PP1N1P1/R3QR1K w kq - 0 23"
white_to_move = True
depth = 2
counter = 0

while is_checkmate(fen) == False and counter < 200 and is_stalemate(fen) == False:
    evaluation, move = minimax(fen, depth, -1000000, 1000000, white_to_move)
    print(convert_move_to_notation(fen, move), end=' ')
    fen = generate_new_fen(fen, move)
    # print(fen)
    white_to_move = not white_to_move
    counter = counter + 1