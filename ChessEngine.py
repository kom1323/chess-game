
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
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        #self.stalemate = False
        self.pins = []
        self.checks = []

    def make_move(self, move):
        """
        Takes a Move as a parameter and executes it (will not work for castling and en passant)
        """
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move) # log the move
        self.white_to_move = not self.white_to_move #swap players
        # Update king's position
        if move.piece_moved == 'wK':
            self.white_king_location =(move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location =(move.end_row, move.end_col)

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
        # Update king's position
        if move.piece_moved == 'wK':
            self.white_king_location =(move.start_row, move.start_col)
        elif move.piece_moved == 'bK':
            self.black_king_location =(move.start_row, move.start_col)


    def get_valid_moves(self):
        """
        All moves considering checks.
        """
        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if self.in_check:
            if len(self.checks) == 1: # Only 1 check, block check or move king
                moves = self.get_all_possible_moves()
                # to block a check you must move a piece into one of the squares between the enemy piece and king
                check = self.checks[0] # first get the check information and parse it
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = [] # squares that pieces can move
                # if knight, must capture knight or move king, other pieces can be blocked
                if piece_checking[1] == 'K':
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i) # check[2] and check[3] are the check direction
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col: #last valid move is on the checking piece
                            break
                
                # get rid of any moves that don't block check or move king after get_all_posible_moves is called
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != 'K': # move doesn't move king so it must block or capture
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else: # double check, king has to move
                self.get_king_moves(king_row, king_col, moves)
        else: # not in check so all moves are fine
            moves = self.get_all_possible_moves()

        return moves
    

    def check_for_pins_and_checks(self):
        pins = []
        checks = []
        in_check = False
        if self.white_to_move:
            enemy_color = 'b'
            ally_color = 'w'
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = 'w'
            ally_color = 'b'
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        
        # Check outwards from king for pins and checks, keep track of pins
        possible_directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for dir_iter in range(len(possible_directions)):
            direction = possible_directions[dir_iter]
            possible_pin = () # reset possible pins
            for i in range(1, 8):
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != 'K':
                        if possible_pin == (): # 1st allied piece could be pinned
                            possible_pin = (end_row, end_col, direction[0], direction[1])
                        else: # 2st allied piece , so no pin or check possible in this direction
                            break
                    elif end_piece[0] == enemy_color:
                        piece_type = end_piece[1]
                        # 5 possibilities here
                        # 1) orthogonally away from king and piece is a rook
                        # 2) diagonally away from king and piece is a bishop
                        # 3) 1 square away diagonally from king and piece is a pawn
                        # 4) any direction and piece is a queen
                        # 5) any direction and 1 square away and piece is a king (this is necessary to prevent a king move to a square controlled by another king)
                        if (0 <= dir_iter <=3 and piece_type == 'R') or \
                                (4 <= dir_iter <= 7 and piece_type == 'B') or \
                                (i == 1 and piece_type == 'P' and ((enemy_color == 'w' and 6 <= dir_iter <=7) or (enemy_color == 'b' and 4 <= dir_iter <= 5))) or \
                                (piece_type == 'Q') or (i == 1 and piece_type == 'K'):
                            if possible_pin == (): # no piece is blocking, so check
                                in_check = True
                                checks.append((end_row, end_col, direction[0], direction[1]))
                                break
                            else: # piece blocking so pin
                                pins.append(possible_pin)
                                break
                        else: # enemy piece not applying check
                            break
                else: # off board
                    break
        #check for knight checks
        knight_moves = ((-2,-1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'N': # enemy knight attacking king
                    in_check = True
                    checks.append((end_row, end_col, move[0], move[1]))
        return in_check, pins, checks

    def in_check(self):
        """
        DONT FORGET TO MAYBE DELETE
        """
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])


    def square_under_attack(self, row, col):
        """
        DONT FORGET TO MAYBE DELETE
        """
        self.white_to_move = not self.white_to_move
        opponent_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opponent_moves:
            if move.end_row == row and move.end_col == col:
                return True
        return False 
    

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
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break


        if self.white_to_move:
            #Handle move white
            if self.board[row - 1][col] == "--": # square in front is empty
                if not piece_pinned or pin_direction == (-1, 0):
                    moves.append(Move((row, col), (row - 1, col), self.board))
                    if row == 6 and self.board[row - 2][col] == "--":
                        moves.append(Move((row, col),(row - 2, col),self.board))
            
            #Handle diag captures
            if col + 1 <= 7: 
                if self.board[row - 1][col + 1][0] == 'b': 
                    if not piece_pinned or pin_direction == (-1, 1):
                        moves.append(Move((row, col), (row - 1, col + 1), self.board))
            if col - 1 >= 0: 
                if self.board[row - 1][col - 1][0] == 'b': 
                    if not piece_pinned or pin_direction == (-1, -1):
                        moves.append(Move((row, col), (row - 1, col - 1), self.board))
        
        else:
            #Handle move black
            if self.board[row + 1][col] == "--": # square in front is empty
                    if not piece_pinned or pin_direction == (1, 0):
                        moves.append(Move((row, col), (row + 1, col), self.board))
                        if row == 1 and self.board[row + 2][col] == "--":
                            moves.append(Move((row, col),(row + 2, col),self.board))

            #Handle diag captures
            if col + 1 <= 7: 
                if self.board[row + 1][col + 1][0] == 'w': 
                        if not piece_pinned or pin_direction == (1, 1):
                            moves.append(Move((row, col), (row + 1, col + 1), self.board))
            if col - 1 >= 0: 
                if self.board[row + 1][col - 1][0] == 'w': 
                    if not piece_pinned or pin_direction == (1, -1):
                        moves.append(Move((row, col), (row + 1, col - 1), self.board))

    
    
    
    def get_rook_moves(self, row, col, moves):
        
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) -1, -1 ,-1):
            if self.pins[i][0] == row and self.pins[i][0] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][0] != 'Q': #can't remove queen from pin on rook moves, only remove on bishop moves because I call it after
                    self.pins.remove(self.pins[i])
                break
        
        current_turn_color = 'w' if self.white_to_move else 'b'
        # up
        for it in range(1, 8):
            row_iter = row - it
            if row_iter < 0:
                break
            if self.board[row_iter][col][0] != current_turn_color:  
                if not piece_pinned or pin_direction == (-1, 0):
                    moves.append(Move((row, col), (row_iter, col), self.board))
            if self.board[row_iter][col] != '--':
                break

        # down
        for it in range(1, 8):
            row_iter = row + it
            if row_iter > 7:
                break
            if self.board[row_iter][col][0] != current_turn_color:  
                if not piece_pinned or pin_direction == (1, 0):
                    moves.append(Move((row, col), (row_iter, col), self.board))
            if self.board[row_iter][col] != '--':
                break

        # right
        for it in range(1, 8):
            col_iter = col + it
            if col_iter > 7:
                break
            if self.board[row][col_iter][0] != current_turn_color:  
                if not piece_pinned or pin_direction == (0, 1):
                    moves.append(Move((row, col), (row, col_iter), self.board))
            if self.board[row][col_iter] != '--':
                break
        # left
        for it in range(1, 8):
            col_iter = col - it
            if col_iter < 0:
                break
            if self.board[row][col_iter][0] != current_turn_color:  
                if not piece_pinned or pin_direction == (0, -1):
                    moves.append(Move((row, col), (row, col_iter), self.board))
            if self.board[row][col_iter] != '--':
                break
        

    def get_knight_moves(self, row, col, moves):

        piece_pinned = False
        for i in range(len(self.pins) -1, -1 ,-1):
            if self.pins[i][0] == row and self.pins[i][0] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break


        current_turn_color = 'w' if self.white_to_move else 'b'
        possible_moves = [(row - 2, col + 1), (row - 1, col + 2),
                            (row + 1, col + 2), (row + 2, col + 1),
                            (row + 2, col - 1), (row + 1, col - 2),
                            (row - 1, col - 2), (row - 2, col - 1)
                            ]
        
        for move in possible_moves:
            if (move[0] <= 7 and move[1] <= 7 and move[0] >= 0 and move[1] >= 0 and 
                    self.board[move[0]][move[1]][0] != current_turn_color):
                if not piece_pinned:
                    moves.append(Move((row, col), move, self.board))
  




    def get_bishop_moves(self, row, col, moves):

        piece_pinned = False
        pin_direction = ()
        print("Pins size ",len(self.pins)) 
        for i in range(len(self.pins) -1, -1 ,-1):
            if self.pins[i][0] == row and self.pins[i][0] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break


        current_turn_color = 'w' if self.white_to_move else 'b'
        
        # down-right
        for it in range(1, 8):
            row_iter = row + it
            col_iter = col + it
            if col_iter > 7 or row_iter > 7:
                break
            if self.board[row_iter][col_iter][0] != current_turn_color:
                if not piece_pinned or pin_direction == (1, 1):
                    moves.append(Move((row, col), (row_iter, col_iter), self.board))
            if self.board[row_iter][col_iter] != '--':
                break  
        
        #down-left
        for it in range(1, 8):
            row_iter = row + it
            col_iter = col - it
            if col_iter < 0 or row_iter > 7:
                break
            if self.board[row_iter][col_iter][0] != current_turn_color:
                if not piece_pinned or pin_direction == (1, -1):
                    moves.append(Move((row, col), (row_iter, col_iter), self.board))
            if self.board[row_iter][col_iter] != '--':
                break

        #up-right
        for it in range(1, 8):
            row_iter = row - it
            col_iter = col + it
            if col_iter > 7 or row_iter < 0:
                break
            if self.board[row_iter][col_iter][0] != current_turn_color:
                if not piece_pinned or pin_direction == (-1, 1):
                    moves.append(Move((row, col), (row_iter, col_iter), self.board))
            if self.board[row_iter][col_iter] != '--':
                break

        #up-left
        for it in range(1, 8):
            row_iter = row - it
            col_iter = col - it
            if col_iter < 0 or row_iter < 0:
                break
            if self.board[row_iter][col_iter][0] != current_turn_color:
                if not piece_pinned or pin_direction == (-1, -1):
                    moves.append(Move((row, col), (row_iter, col_iter), self.board))
            if self.board[row_iter][col_iter] != '--':
                break

    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)


    def get_king_moves(self, row, col, moves):
        current_turn_color = 'w' if self.white_to_move else 'b'
        possible_moves = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                          (row, col - 1), (row, col), (row, col + 1),
                          (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]
        
        for move in possible_moves:
            if (move[0] <= 7 and move[1] <= 7 and move[0] >= 0 and move[1] >= 0 and 
                    self.board[move[0]][move[1]][0] != current_turn_color):
                if current_turn_color == 'w':
                    self.white_king_location = move
                else:
                    self.black_king_location = move
                in_check, pins, checks = self.check_for_pins_and_checks()
                if not in_check:
                    moves.append(Move((row, col), move, self.board))
                if current_turn_color == 'w':
                    self.white_king_location = (row,col)
                else:
                    self.black_king_location = (row,col)
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