ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, 
                   "e": 4, "f": 5, "g": 6, "h": 7}
rowsToRanks = {v: k for k, v in ranksToRows.items()}
colsToFiles = {v: k for k, v in filesToCols.items()}  

def rowcol_to_boardposition(row, col):
    ans = ""
    ans += colsToFiles[col]
    ans += rowsToRanks[row]
    return ans

class Move():
    def __init__(self, startrow, startcol, endrow, endcol):
        self.startrow = startrow
        self.startcol = startcol
        self.endrow = endrow
        self.endcol = endcol

previous_fen = "rnbqkbnr/pppp2pp/4p3/4Pp2/8/8/PPPP1PPP/RNBQKBNR w KQkq f6 0 3"
move = Move(3, 4, 2, 5);

def generate_new_fen(previous_fen, movex):
    move = Move(movex[0], movex[1], movex[2], movex[3])

    '''Setting previous state of the board'''

    ispromotion = movex[4]    # This can be implemented in future to check which piece has the pawn been promoted to
    board = [
                ['-','-','-','-','-','-','-','-'], 
                ['-','-','-','-','-','-','-','-'], 
                ['-','-','-','-','-','-','-','-'], 
                ['-','-','-','-','-','-','-','-'], 
                ['-','-','-','-','-','-','-','-'], 
                ['-','-','-','-','-','-','-','-'], 
                ['-','-','-','-','-','-','-','-'], 
                ['-','-','-','-','-','-','-','-']
            ]
    wkcastle = False
    wqcastle = False
    bkcastle = False
    bqcastle = False

    enpassant = previous_fen.split()[3]

    whitetomove = 'w'

    half_move_clock = int(previous_fen.split()[4])
    full_move_number = int(previous_fen.split()[5])
    
    board_position = previous_fen.split()[0].split('/')
    i = 0
    for row in range(len(board_position)):
        j = 0
        for col in range(len(board_position[row])):
            temp = board_position[row][col]
            if(temp.isdigit()):
                temp = int(temp)
                while temp != 0:
                    j = j+1
                    temp = temp-1
            else:
                board[i][j] = board_position[row][col]
                j = j+1
        i = i+1
    
    castlingRights = previous_fen.split()[2];
    if 'K' in castlingRights : 
        wkcastle = True
    if 'Q' in castlingRights :
        wqcastle = True
    if 'k' in castlingRights :
        bkcastle = True
    if 'q' in castlingRights :
        bqcastle = True
    if previous_fen.split()[1] == 'w':
        whitetomove = 'b'

    '''Now making changes to get the new state'''

    piecemoved = board[move.startrow][move.startcol]
    piececaptured = board[move.endrow][move.endcol]

    if piececaptured == 'R' :
        if wkcastle == True and move.endcol == 7:
            wkcastle = False
        if wqcastle == True and move.endcol == 0:
            wqcastle = False
    if piececaptured == 'r':
        if bkcastle == True and move.endcol == 7:
            bkcastle = False;
        if bqcastle == True and move.endcol == 0:
            bqcastle = False

    if piecemoved.lower() == 'p' :
        half_move_clock = 0
    else:
        if board[move.endrow][move.endcol] != '-' :
            half_move_clock = 0
        else :
            half_move_clock = half_move_clock + 1

    if piecemoved != 'K' and piecemoved != 'k':

        board[move.startrow][move.startcol] = '-'
        board[move.endrow][move.endcol] = piecemoved

        if piecemoved == 'p' or piecemoved == 'P':
            
            if abs(move.startrow - move.endrow) == 2:   # Telling enpassant is possible at next move and at what position
                temp = (move.startrow + move.endrow)/2
                enpassant = rowcol_to_boardposition(temp, move.startcol)
            else:
                enpassant = '-'

            if move.startcol != move.endcol and ispromotion == '#' and enpassant != '-':   # Current move is an enpassant move
                if(rowsToRanks[move.endrow] == enpassant[1] and colsToFiles[move.endcol] == enpassant[0]):
                    board[move.startrow][move.endcol] = '-'
            
            if move.endrow == 0 :   # White pawn promotion 
                board[move.endrow][move.endcol] = ispromotion.upper()  
            if move.endrow == 7 :   # Black pawn promotion 
                board[move.endrow][move.endcol] = ispromotion.lower()

        if piecemoved == 'R' and move.endcol == 7:
            wkcastle = False
        if piecemoved == 'R' and move.endcol == 1:
            wqcastle = False
        if piecemoved == 'r' and move.endcol == 7:
            bkcastle = False
        if piecemoved == 'r' and move.endcol == 0:
            bqcastle = False

    else :
        board[move.startrow][move.startcol] = '-'
        board[move.endrow][move.endcol] = piecemoved
        if piecemoved == 'k' :
            bkcastle = False
            bqcastle = False
        else :
            wkcastle = False
            wqcastle = False

        if abs(move.startcol - move.endcol) == 2:
            if(move.startrow == 0 and move.endcol == 6):
                board[0][5] = 'r'
                board[0][7] = '-'
            if(move.startrow == 0 and move.endcol == 2):
                board[0][3] = 'r'
                board[0][0] = '-'
            if(move.startrow == 7 and move.endcol == 6):
                board[7][5] = 'R'
                board[7][7] = '-'
            if(move.startrow == 7 and move.endcol == 2):
                board[7][3] = 'R'
                board[7][0] = '-'

    if piecemoved.islower() :
        full_move_number = full_move_number + 1

    new_fen = ""
    i = 0
    while i < 8 :
        j = 0
        while j < 8 :
            if board[i][j] == '-' :
                count = 1
                j = j + 1
                while j < 8 and board[i][j] == '-':
                    count = count + 1
                    j = j + 1
                new_fen += str(count)
            else :
                new_fen += board[i][j]
                j = j + 1
        new_fen += '/'
        i = i + 1
    new_fen = new_fen[:-1]

    new_fen += ' '
    new_fen += whitetomove
    new_fen += ' '

    if wkcastle == False and wqcastle == False and bkcastle == False and bqcastle == False:
        new_fen += '-'
    else :
        if(wkcastle == True) :
            new_fen += 'K'
        if(wqcastle == True) :
            new_fen += 'Q'
        if(bkcastle == True) :
            new_fen += 'k'
        if(bqcastle == True) :
            new_fen += 'q'
    new_fen += ' '

    new_fen += enpassant
    new_fen += ' '

    new_fen += str(half_move_clock)
    new_fen += ' '

    new_fen += str(full_move_number)
    # print("Previous FEN : ", previous_fen)
    # print("Move : ", move.startrow, move.startcol, move.endrow, move.endcol)
    # print("New FEN : ", new_fen)
    return new_fen

# new_fen = generate_new_fen(previous_fen, move)
# print(new_fen)