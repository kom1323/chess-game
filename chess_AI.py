import random

piece_score ={'K':0, 'Q': 9, 'R':5, 'B':3, 'N':3, 'P':1}

white_knight_score = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 5, 5, 5, 5, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [0, 0, 0, 0, 0, 0, 0, 0]
                ]


black_knight_score = [[0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 2, 2, 2, 2, 2, 2, 1],
                      [1, 2, 3, 3, 3, 3, 2, 1],
                      [1, 2, 3, 4, 4, 3, 2, 1],
                      [1, 2, 5, 5, 5, 5, 2, 1],
                      [1, 2, 3, 3, 3, 3, 2, 1],
                      [1, 2, 2, 2, 2, 2, 2, 1],
                      [1, 1, 1, 1, 1, 1, 1, 1],
]


white_bishop_score = [  [1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 2, 2, 1, 1, 2, 2, 1],
                        [1, 1, 1, 2, 2, 1, 1, 1],
                        [1, 2, 1, 1, 1, 1, 2, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0]
                ]

black_bishop_score = [[0, 0, 0, 0, 0, 0, 0, 0],
                [1, 2, 1, 1, 1, 1, 2, 1],
                [1, 1, 1, 2, 2, 1, 1, 1],
                [1, 2, 2, 1, 1, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                ]
white_rook_score = [[1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 2, 2, 1, 1, 1],
                    [0, 1, 1, 4, 4, 1, 1, 0],
                ]
black_rook_score = [[0, 1, 1, 4, 4, 1, 1, 0],
                    [1, 1, 1, 2, 2, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                ]
white_queen_score = [   [1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 2, 1, 1, 1, 1, 2, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 2, 1, 1, 1, 1, 2, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 2, 2, 1, 1, 1],
                        [0, 0, 0, 1, 0, 0, 0, 0],
                ]
black_queen_score = [   [0, 0, 0, 1, 0, 0, 0, 0],
                        [1, 1, 1, 2, 2, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 2, 1, 1, 1, 1, 2, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 2, 1, 1, 1, 1, 2, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1],
                ]
white_pawn_score = [[10, 10, 10, 10, 10, 10, 10, 10],
                    [5, 5, 5, 5, 5, 5, 5, 5],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 3, 3, 1, 1, 1],
                    [1, 1, 1, 5, 5, 1, 1, 1],
                    [2, 1, 2, 4, 4, 2, 1, 2],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ]

black_pawn_score = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [2, 1, 2, 4, 4, 2, 1, 2],
                    [1, 1, 1, 5, 5, 1, 1, 1],
                    [1, 1, 1, 3, 3, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [5, 5, 5, 5, 5, 5, 5, 5],
                    [10, 10, 10, 10, 10, 10, 10, 10],
                ]

white_king_score = [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 0, -1, -1, -1, -1, 0, 1],
                    [3, 3, 5, 0, 1, 0, 7, 3],
                    ]

black_king_score = [
                    [3, 3, 5, 0, 1, 0, 7, 3],
                    [1, 0, -1, -1, -1, -1, 0, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],



]



piece_position_scores = {'wN': white_knight_score, 'bN': black_knight_score,
                         'wB': white_bishop_score, 'bB': black_bishop_score,
                         'wR': white_rook_score, 'bR': black_rook_score,
                         'wP': white_pawn_score, 'bP': black_pawn_score,
                         'wQ': white_queen_score, 'bQ': black_queen_score,
                         'wK': white_king_score, 'bK': black_king_score}

CHECKMATE = 1000
STALEMATE = 0 
DEPTH = 3

def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]

def find_best_move_iterative_min_max(game_state, valid_moves):
    """
    This is an iterative implementation of MinMax algorithm with depth 2.
    """
    turn_multiplier = 1 if game_state.white_to_move else -1
  
    opponent_min_max_score = CHECKMATE # worst score for black
    best_player_move = None
    random.shuffle(valid_moves)
    for player_move in valid_moves:
        game_state.make_move(player_move)
        opponent_max_score = - CHECKMATE
        all_opponent_moves = game_state.get_valid_moves()

        if game_state.checkmate:
            score = -CHECKMATE 
        elif game_state.stalemate:
            score = STALEMATE
        else:
            for opponent_move in all_opponent_moves: 
                game_state.make_move(opponent_move)
                game_state.get_valid_moves()
                if game_state.checkmate:
                    score = CHECKMATE 
                elif game_state.stalemate:
                    score = STALEMATE
                else: 
                    score = -turn_multiplier * score_board(game_state.board)
                if score > opponent_max_score:
                    opponent_max_score = score    
                game_state.undo_move()
        
        if opponent_min_max_score > opponent_max_score: 
            opponent_min_max_score = opponent_max_score
            best_player_move = player_move
        game_state.undo_move()
    return best_player_move

def find_best_move(game_state, valid_moves, return_queue):
    """
    Helper function for first recursive call.
    """
    global next_move
    next_move = None
    #find_move_min_max(game_state, valid_moves, DEPTH, game_state.white_to_move)
    random.shuffle(valid_moves)
    find_move_nega_max_alpha_beta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if game_state.white_to_move else -1)
    return_queue.put(next_move)

def find_move_min_max(game_state, valid_moves, depth, white_to_move):
    global next_move
    if depth == 0:
        return score_board(game_state.board)
    
    if white_to_move:
        max_score = - CHECKMATE
        for move in valid_moves:
            game_state.make_move(move)
            next_possible_moves = game_state.get_valid_moves()
            score = find_move_min_max(game_state, next_possible_moves, depth - 1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            game_state.undo_move()
        return max_score
    else:
        min_score = CHECKMATE
        for move in valid_moves:
            game_state.make_move(move)
            next_possible_moves = game_state.get_valid_moves()
            score = find_move_min_max(game_state, next_possible_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            game_state.undo_move()
        return min_score    

def find_move_nega_max_alpha_beta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(game_state)
    
    #move ordering -implement later

    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.make_move(move)
        next_possible_moves = game_state.get_valid_moves()
        score = -find_move_nega_max_alpha_beta(game_state, next_possible_moves, depth -1, -beta, -alpha,-turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
                print(move, score)

        game_state.undo_move()
        if max_score > alpha: # pruning
            alpha = max_score
        if alpha >= beta:
            break
    return max_score    

def score_board(game_state):
    """
    A positive score is good for white.
    A negative score is good for black
    """
    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE # black wins
        else:
            return CHECKMATE # white wins
    elif game_state.stalemate:
        return STALEMATE
    
    score = 0
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            square = game_state.board[row][col]
            position_score = 0
            if square != "--":
                position_score = piece_position_scores[square][row][col]
            if square[0] == 'w':
                score += piece_score[square[1]] + position_score * .1
            elif square[0] == 'b':
                score -= piece_score[square[1]] + position_score * .1
                
    return score

