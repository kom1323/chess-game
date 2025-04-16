
class GameState():
    """
    This class is responsible for storing all the information about the current state of a chess game.
    It will also be responsible for determining the valid moves at the current state.
    It will also keep a move log.
    """
    def __init__(self):
        #Board is an 8x8 2d list, each element of the list has 2 characters.
        #The first character represent the color of the piece, 'b' or 'w'.
        #The second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N' or 'P'.
        #"--" - represents an empty space with no piece.
        #Maybe switch to numpy for engine
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        
        self.move_functions = {'P': self.get_pawn_moves, 'R': self.get_rook_moves, 'N':self.get_knight_moves,
                               'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.white_to_move = True
        self.move_log = []

    def make_move(self, move):
        """
        Takes a Move as a parameter and executes it (will not work for castling and en passant)
        """
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move) # log the move
        self.white_to_move = not self.white_to_move #swap players

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move


    def get_valid_moves(self):
        """
        All moves considering checks.
        """
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        """
        All moves without considering checks.
        """
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.white_to_move) or (turn =='b' and not self.white_to_move):
                    piece = self.board[row][col][1]
                    self.move_functions[piece](row, col, moves)

        return moves

    def get_pawn_moves(self, row, col, moves):
        if self.white_to_move:
            #Handle move white
            if self.board[row - 1][col] == "--": # square in front is empty
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == "--":
                    moves.append(Move((row, col),(row - 2, col),self.board))
            
            #Handle diag captures
            if col + 1 <= 7: 
                if self.board[row - 1][col + 1][0] == 'b': 
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
            if col - 1 >= 0: 
                if self.board[row - 1][col - 1][0] == 'b': 
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
        
        else:
            #Handle move black
            if self.board[row + 1][col] == "--": # square in front is empty
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == "--":
                    moves.append(Move((row, col),(row + 2, col),self.board))

            #Handle diag captures
            if col + 1 <= 7: 
                if self.board[row + 1][col + 1][0] == 'w': 
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
            if col - 1 >= 0: 
                if self.board[row + 1][col - 1][0] == 'w': 
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))

    
    
    
    def get_rook_moves(self, row, col, moves):
        if self.white_to_move:
            for row_iter in range(row + 1, 8):
                if self.board[row_iter][col][0] != 'w':
                    moves.append(Move((row, col), (row_iter, col), self.board))
                if self.board[row_iter][col] != '--':
                    break
            for row_iter in range(row - 1, -1, -1):
                if self.board[row_iter][col][0] != 'w':
                    moves.append(Move((row, col), (row_iter, col), self.board))
                if self.board[row_iter][col] != '--':
                    break
            for col_iter in range(col + 1, 8):
                if self.board[row][col_iter][0] != 'w':
                    moves.append(Move((row, col), (row, col_iter), self.board))
                if self.board[row][col_iter] != '--':
                    break
            for col_iter in range(col -1, -1, -1):
                if self.board[row_iter][col][0] != 'w':
                    moves.append(Move((row, col), (col_iter, col), self.board))
                if self.board[row_iter][col] != '--':
                    break
        else:
            for row_iter in range(row + 1, 8):
                if self.board[row_iter][col][0] != 'b':
                    moves.append(Move((row, col), (row_iter, col), self.board))
                if self.board[row_iter][col] != '--':
                    break
            for row_iter in range(row - 1, -1, -1):
                if self.board[row_iter][col][0] != 'b':
                    moves.append(Move((row, col), (row_iter, col), self.board))
                if self.board[row_iter][col] != '--':
                    break
            for col_iter in range(col + 1, 8):
                if self.board[row][col_iter][0] != 'b':
                    moves.append(Move((row, col), (row, col_iter), self.board))
                if self.board[row][col_iter] != '--':
                    break
            for col_iter in range(col -1, -1, -1):
                if self.board[row_iter][col][0] != 'b':
                    moves.append(Move((row, col), (col_iter, col), self.board))
                if self.board[row_iter][col] != '--':
                    break


    def get_knight_moves(self, row, col, moves):
        
        possible_moves = [(row - 2, col + 1), (row - 1, col + 2),
                            (row + 1, col + 2), (row + 2, col + 1),
                            (row + 2, col - 1), (row + 1, col - 2),
                            (row - 1, col - 2), (row - 2, col - 1)
                            ]
        
        if self.white_to_move:
            for move in possible_moves:
                if move[0] <= 7 and move[1] <= 7 and self.board[move[0]][move[1]][0] != 'w':
                    moves.append(Move((row, col), move, self.board))
        else:
            for move in possible_moves:
                if move[0] <= 7 and move[1] <= 7 and self.board[move[0]][move[1]][0] != 'b':
                    moves.append(Move((row, col), move, self.board))




    def get_bishop_moves(self, row, col, moves):
        if self.white_to_move:
            for row_iter in range(row + 1, 8):
                # fix col - (row_iter - row) range, currently out of bounds
                if self.board[row_iter][col + (row_iter - row)][0] != 'w':
                    moves.append(Move((row, col), (row_iter, col + (row_iter - row)), self.board))
                if self.board[row_iter][col + (row_iter - row)] != '--':
                    break
                if self.board[row_iter][col - (row_iter - row)][0] != 'w':
                    moves.append(Move((row, col), (row_iter, col - (row_iter - row)), self.board))
                if self.board[row_iter][col - (row_iter - row)] != '--':
                    break
            
            for row_iter in range(row - 1, -1, -1):
                if self.board[row_iter][col + (row_iter - row)][0] != 'w':
                    moves.append(Move((row, col), (row_iter, col + (row_iter - row)), self.board))
                if self.board[row_iter][col + (row_iter - row)] != '--':
                    break
                if self.board[row_iter][col - (row_iter - row)][0] != 'w':
                    moves.append(Move((row, col), (row_iter, col - (row_iter - row)), self.board))
                if self.board[row_iter][col - (row_iter - row)] != '--':
                    break
        else:
            for row_iter in range(row + 1, 8):
                if self.board[row_iter][col + (row_iter - row)][0] != 'b':
                    moves.append(Move((row, col), (row_iter, col + (row_iter - row)), self.board))
                if self.board[row_iter][col + (row_iter - row)] != '--':
                    break
                if self.board[row_iter][col - (row_iter - row)][0] != 'b':
                    moves.append(Move((row, col), (row_iter, col - (row_iter - row)), self.board))
                if self.board[row_iter][col - (row_iter - row)] != '--':
                    break
            
            for row_iter in range(row - 1, -1, -1):
                if self.board[row_iter][col + (row_iter - row)][0] != 'b':
                    moves.append(Move((row, col), (row_iter, col + (row_iter - row)), self.board))
                if self.board[row_iter][col + (row_iter - row)] != '--':
                    break
                if self.board[row_iter][col - (row_iter - row)][0] != 'b':
                    moves.append(Move((row, col), (row_iter, col - (row_iter - row)), self.board))
                if self.board[row_iter][col - (row_iter - row)] != '--':
                    break



    def get_queen_moves(self, row, col, moves):
        pass
    def get_king_moves(self, row, col, moves):
        pass
    
class Move():

    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k,v in ranks_to_rows.items()}
    files_to_cols = {"a":0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k,v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, value):
        """
        Overriding the equals method to compare moves
        """
        if isinstance(value, Move):
            return self.move_id == value.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]