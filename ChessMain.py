"""
This is our main driver file. 
It will be responsible for handling user input and displaying the current GameState object.
"""
import pygame as p
import ChessEngine, chessAI


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images(): 
    """
    Initialize a global dictionary of images.
    """
    pieces  = [ 'wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE,SQ_SIZE))


def main():
    """
    Handles user input and updates graphics.
    """
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False # flag variable whether a move is made
    animate = False # flag variable  whether to animate a move
    load_images()
    running = True
    square_selected = () # Keep track of the last click of the user (row, col)
    player_clicks = [] # two tuples
    game_over = False
    player_one = False # if human is playing white then True, if Ai then False
    player_two = False # same as above but for black
    while running:
        is_human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over and is_human_turn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if square_selected == (row, col): # The user clicked the same square twice
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row ,col)
                        player_clicks.append(square_selected)
                    if len(player_clicks) == 2:
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.make_move(valid_moves[i])
                                move_made = True
                                animate = True
                                square_selected = () # Reset user clicks
                                player_clicks = []
                                break
                        if not move_made:
                            player_clicks = [square_selected]
            #Key handler
            elif e.type == p.KEYDOWN:
                    if e.key == p.K_z: # undo move when z is pressed
                        game_state.undo_move()
                        move_made = True
                        animate = False
                    if e.key == p.K_r: # reset when r is pressed
                        game_state = ChessEngine.GameState()
                        valid_moves = game_state.get_valid_moves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
                        break

        # AI move logic
        if not game_over and not is_human_turn:
            ai_move = chessAI.find_best_move(game_state, valid_moves)
            if ai_move is None:
                ai_move = chessAI.find_random_move(valid_moves)
            game_state.make_move(ai_move)
            move_made = True
            animate = True



        if move_made:
            if animate:
                animate_move(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.get_valid_moves()
            move_made = False
            animate = False

        draw_game_state(screen, game_state, valid_moves, square_selected)

        if game_state.checkmate:
            game_over = True
            if game_state.white_to_move:
                draw_text(screen, "Black wins by checkmate")
            else:
                draw_text(screen, "White wins by checkmate")
        elif game_state.stalemate:
            game_over = True
            draw_text(screen, "Stalemate")        
        clock.tick(MAX_FPS)
        p.display.flip()



def highlight_squares(screen, game_state, valid_moves, square_selected):
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == ('w' if game_state.white_to_move else  'b'): # if squareselected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE)) 


def draw_game_state(screen, game_state, valid_moves, square_selected):
    """
    Responsible for all the graphics within current game state.
    """
    draw_board(screen)
    highlight_squares(screen, game_state, valid_moves, square_selected)
    draw_pieces(screen, game_state.board)


def draw_board(screen):
    """
    Draw squares on the board.
    """
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row+col)%2)]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    """
    Draw pieces on the board using current GameState.board.
    """
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def animate_move(move, screen, board, clock):
    global colors
    coords = [] # list of coords that the animation will move through
    delta_row = move.end_row - move.start_row
    delta_col = move.end_col - move.start_col
    frames_per_square = 4
    frame_count = (abs(delta_row) + abs(delta_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = ((move.start_row + delta_row * frame / frame_count,move.start_col + delta_col * frame / frame_count))
        draw_board(screen)
        draw_pieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--' and not move.is_enpassant_move:
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen. blit(IMAGES[move.piece_moved], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def draw_text(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text, 0, p.Color('Gray'))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2, HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, p.Color('Black'))
    screen.blit(text_object, text_location.move(2, 2))
if __name__ == "__main__":
    main()
