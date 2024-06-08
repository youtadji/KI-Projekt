import random
import main
import board
import zuggenerator
import time


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
    # fen = "1b04/2b03b01/b01rr5/r02b01b02/1b06/1r02b03/8/1r01r0r0r0"
    fen = "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0"  # Initial FEN string representing the starting position
    # fen = "b01bb1b0b0/1bbb0b0b0b0b01/8/8/8/8/1r0r0r0r0rr2/1rrr01rrr0"
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
        if player == main.Player.RED:
            enemy = main.Player.BLUE
        else:
            enemy = main.Player.RED
        pos, end = parse_move(move)
        if player == main.Player.RED:
            score += 10 * (1 - abs(1 - pos.row) / 8)
        if player == main.Player.BLUE:
            score += 10 * (1 - abs(8 - pos.row) / 8)
        # if figure is threathened by enemy
        for enemy_move in zuggenerator.get_possible_moves(main.board_to_fen(board), enemy, board):
            start, end_enemy = parse_move(enemy_move)
            if end_enemy == pos:
                score -= 5
    return score


"""def alpha_beta(board2, alpha, beta, player, depth, max_depth):

    trimmed = main.trim_corners(board2)
    fen2 = main.board_to_fen(trimmed)
    boardy = board.create_board(fen2)

    #board_state_hash = hash(fen2)
   # if board_state_hash in visited_states:
        #print(f"Detected repeated state at depth {depth}")
        #return 0  # Return a neutral score for repeated states

    #visited_states.add(board_state_hash)

    # Base case: Check for game end or depth limit
    game_result = zuggenerator.check_game_end(fen2)
    if game_result:
        print(f"Game end detected at depth {depth}: {game_result}")
        if game_result == "Game Over: Blue wins :D":
            if player == main.Player.BLUE:
                return score(board2, player)
            else:
                return -score(board2, player)
        if game_result == "Game Over: Red wins :D":
            if player == main.Player.RED:
                return score(board2, player)
            else:
                return -score(board2, player)
    if depth == max_depth:
        print(f"Depth limit reached at depth {depth}, returning score")
        return score(board2, player)

    if player == main.Player.RED:
        max_eval = float('-inf')
        for move in zuggenerator.get_possible_moves(fen2, main.Player.RED, board2):
            start_pos, end_pos = parse_move(move)
            new_board = zuggenerator.do_move(start_pos, end_pos, player, board2)
            eval = alpha_beta(new_board, alpha, beta, main.Player.BLUE, depth+1, max_depth)
            undo_board = main.undo_move(start_pos, end_pos, player, new_board, board2)
            depth -= 1
            # max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
           # x = alpha_beta(undo_board, alpha, beta, -player, depth-1)
        return alpha
    else:
        min_eval = float('inf')
        for move2 in zuggenerator.get_possible_moves(fen2, main.Player.BLUE, board2):
            start_pos, end_pos = parse_move(move2)
            new_board = zuggenerator.do_move(start_pos, end_pos, player, board2)


            eval = alpha_beta(new_board, alpha, beta, main.Player.RED, depth + 1, max_depth)
            undo_board = main.undo_move(start_pos, end_pos, player, new_board, board2)
            depth -= 1
            #min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                print(f"Pruning at depth {depth} with alpha {alpha} and beta {beta}")
                break
            #eval2 = alpha_beta(undo_board, alpha, beta, )
        return beta"""


def alpha_beta(board2, alpha, beta, player, start_time, time_limit):
    # Check if the time limit has been reached
    if time.time() - start_time > time_limit:
        return score(board2, player)  # Return a heuristic score when the time limit is reached

    trimmed = main.trim_corners(board2)
    fen2 = main.board_to_fen(trimmed)
    boardy = board.create_board(fen2)

    # Check for game end conditions
    if zuggenerator.check_game_end(fen2):
        if zuggenerator.check_game_end(fen2) == "Game Over: Blue wins :D":
            if player == main.Player.BLUE:
                return score(board2, player)
            else:
                return -score(board2, player)
        if zuggenerator.check_game_end(fen2) == "Game Over: Red wins :D":
            if player == main.Player.RED:
                return score(board2, player)
            else:
                return -score(board2, player)

    if player == main.Player.RED:
        moves = zuggenerator.get_possible_moves(fen2, main.Player.RED, board2)
        for move in moves:
            start_pos, end_pos = parse_move(move)
            new_board = zuggenerator.do_move(start_pos, end_pos, player, board2)
            eval = alpha_beta(new_board, alpha, beta, main.Player.BLUE, start_time, time_limit)
            # undone_board = main.undo_move(start_pos, end_pos, player, new_board, board2)

            # print("UNDONEEE ALPHAAA")

            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return alpha
    else:
        moves = zuggenerator.get_possible_moves(fen2, main.Player.BLUE, board2)
        for move2 in moves:
            start_pos, end_pos = parse_move(move2)
            new_board = zuggenerator.do_move(start_pos, end_pos, player, board2)
            eval = alpha_beta(new_board, alpha, beta, main.Player.RED, start_time, time_limit)
            # main.undo_move(start_pos, end_pos, player, new_board, board2)
            # print("UNDONEEE BETAAA")
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return beta


## Example of how to call the alpha_beta function with a time limit
start_time = time.time()
time_limit = 0.5  # 2 seconds
# fen = "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0"
fen = "6/7b0/8/8/1r06/4b03/2rr1rrr02/5r0"
boardx = main.visualize_board(main.reformulate(fen))
best_move_value = alpha_beta(boardx, float('-inf'), float('inf'), main.Player.BLUE, start_time, time_limit)
print(best_move_value)