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

# Call the play_game function to start the game
play_game()
