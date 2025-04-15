
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
                    if piece == 'P':
                        self.get_pawn_moves(row, col, moves)
                    if piece == 'R':
                        self.get_rook_moves(row, col, moves)



    def get_pawn_moves(self, row, col, moves):
        pass        

    def get_rook_moves(self, row, col, moves):
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

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]