import random

piece_score ={'K':0, 'Q': 9, 'R':5, 'B':3, 'N':3, 'P':1}
CHECKMATE = 1000
STALEMATE = 0 
DEPTH = 2

def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]


def find_best_move(game_state, valid_moves):
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
                    score = -turn_multiplier * score_material(game_state.board)
                if score > opponent_max_score:
                    opponent_max_score = score    
                game_state.undo_move()
        
        if opponent_min_max_score > opponent_max_score: 
            opponent_min_max_score = opponent_max_score
            best_player_move = player_move
        game_state.undo_move()
    return best_player_move



def find_best_move_min_max(game_state, valid_moves):
    """
    Helper function for first recursive call.
    """
    global next_move
    next_move = None
    find_move_min_max(game_state, valid_moves, DEPTH, game_state.white_to_move)
    return next_move

def find_move_min_max(game_state, valid_moves, depth, white_to_move):
    global next_move
    if depth == 0:
        return score_material(game_state.board)
    
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
    for row in game_state.board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]
                
    return score

def score_material(board):
    """
    Score the board based on material.
    """
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]
                
    return score