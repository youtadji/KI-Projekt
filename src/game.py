import random
import main
import board
import zuggenerator


def parse_move(move_str):
    # Split the move string into start and end positions
    start_str, end_str = move_str.split('-')

    # Extract column and row indices from the start and end position strings
    start_col = ord(start_str[0]) - ord('A')
    start_row = int(start_str[1]) - 1
    end_col = ord(end_str[0]) - ord('A')
    end_row = int(end_str[1]) - 1

    # Create Pos objects for the start and end positions
    start_pos = main.Pos(start_col, start_row)
    end_pos = main.Pos(end_col, end_row)

    return start_pos, end_pos


def play_game():

    # Initialize the game board and other necessary variables
    # Replace the following lines with your actual initialization code
    #fen = "1b04/2b03b01/b01rr5/r02b01b02/1b06/1r02b03/8/1r01r0r0r0"
    fen = "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0"  # Initial FEN string representing the starting position
    #fen = "b01bb1b0b0/1bbb0b0b0b0b01/8/8/8/8/1r0r0r0r0rr2/1rrr01rrr0"
    current_player = main.Player.BLUE  # Assuming Red player starts the game
    reformulated = main.reformulate(fen)
    # Visualize the board
    board_stack = main.visualize_board(reformulated)
    board.create_board(fen)

    while True:
        # Calculate all possible moves for the current player
        possible_moves = zuggenerator.get_possible_moves(fen, current_player, board_stack)
        game_result = zuggenerator.check_game_end(fen)

        if game_result:
            print(game_result)
            break
        else:
            random_move = random.choice(possible_moves)  # Randomly select a move from the list of possible moves
            print("Random move : ", random_move)
            start_pos, end_pos = parse_move(random_move)
            board_stack = zuggenerator.do_move(start_pos, end_pos, current_player, board_stack)

        trimmed_board = main.trim_corners(board_stack)
        fen = main.board_to_fen(trimmed_board)
        print("Updated FEN : ", fen)
        board.create_board(fen)

        current_player = main.Player.RED if current_player == main.Player.BLUE else main.Player.BLUE
        print("the current player is ", current_player)

def score(board, player):
    score = 0
    for move in zuggenerator.get_possible_moves(main.board_to_fen(board), player, board):
        if player ==main.Player.RED:
            enemy = main.Player.BLUE
        else: enemy = main.Player.RED
        pos, end = parse_move(move)
        if player == main.Player.RED:
            score += 10 * (1 - abs(1-pos.row) / 8)
        if player == main.Player.BLUE:
            score += 10 * (1 - abs(8-pos.row) / 8)
        #if figure is threathened by enemy
        for enemy_move in zuggenerator.get_possible_moves(main.board_to_fen(board), enemy, board):
            start, end_enemy = parse_move(enemy_move)
            if end_enemy == pos:
                score -= 5
    return score
def alpha_beta(board2, alpha, beta, player): # time limit / flexible depth limit
    trimmed = main.trim_corners(board2)
    fen2 = main.board_to_fen(trimmed)
    #fen2 = fen2
    #print("fen = ", fen)
    boardy = board.create_board(fen2)
    if zuggenerator.check_game_end(fen):
        if zuggenerator.check_game_end(fen) == "Game Over: Blue wins :D":
            if player == main.Player.BLUE:
                return score(board2, player)
            else: return -score(board2, player)
        if zuggenerator.check_game_end(fen) == "Game Over: Red wins :D":
            if player == main.Player.RED:
                return score(board2, player)
            else: return -score(board2, player)

    if player == main.Player.RED:
        #max_eval = float('-inf')
        #for move in zuggenerator.get_possible_moves(fen2, main.Player.RED, board2):
        moves =  zuggenerator.get_possible_moves(fen2, main.Player.RED, board2)
        for move in moves:
            start_pos, end_pos = parse_move(move)
            print("possible moves = ", zuggenerator.get_possible_moves(fen2, main.Player.RED, board2))
            new_board = zuggenerator.do_move(start_pos, end_pos, player, board2)
            eval = alpha_beta(new_board, alpha, beta, main.Player.BLUE)
            main.undo_move(start_pos, end_pos, player, new_board, board2)
            #max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return alpha
    else:
        #min_eval = float('inf')
        moves = zuggenerator.get_possible_moves(fen2, main.Player.BLUE, board2)
        for move2 in moves:
            start_pos, end_pos = parse_move(move2)
            print("possible moves = ", zuggenerator.get_possible_moves(fen2, main.Player.BLUE, board2))
            print("move = ", move2)
            new_board = zuggenerator.do_move(start_pos, end_pos, player, board2)
            eval = alpha_beta(new_board,  alpha, beta, main.Player.RED)
            main.undo_move(start_pos, end_pos, player, new_board, board2)
            #min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return beta

# Call the play_game function to start the game
#play_game()
fen = "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0"
boardx = main.visualize_board(main.reformulate(fen))
alpha_beta(boardx, float('-inf'), float('inf'), main.Player.RED)
