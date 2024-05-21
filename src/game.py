import random
import main
import board
import zuggenerator
import main



def board_to_fen(board):
    fen_parts = []
    for row in board:
        row_part = ""
        empty_count = 0
        for cell in row:
            if cell is None or cell.is_empty():
                empty_count += 1
            else:
                if empty_count > 0:
                    row_part += str(empty_count)
                    empty_count = 0
                # Handle the cell based on its stack content
                if len(cell.stack) == 1:
                    row_part += cell.stack[0].value[0] + "0"
                else:
                    stack_representation = ''.join(player.value[0] for player in cell.stack)
                    row_part += stack_representation

        # If the row ends with empty cells, append the count
        if empty_count > 0:
            row_part += str(empty_count)

        fen_parts.append(row_part)

    return "/".join(fen_parts)

# Example usage:
# board = setup_your_board_somehow()
# fen_string = board_to_fen(board)
# print(fen_string)


# You can then use this function in your main game loop or wherever you need to convert a board state back into an FEN string.


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


def reverse_reformulate(fen):
    rows = fen.split("/")

    # Process the first row: Remove '1' from the beginning and the end if added
    if len(rows[0]) > 1:  # Ensure there is something to remove
        if rows[0][0] == '1':
            first_row = rows[0][1:]  # Remove the first '1'
            if first_row[0] == '0':
                first_row = first_row[1:]  # Remove leading '0' if present
        if first_row[-1] == '1':
            first_row = first_row[:-1]  # Remove the last '1'
            if first_row[-1] == '0':
                first_row = first_row[:-1]  # Remove trailing '0' if present
        rows[0] = first_row

    # Process the last row: Remove '1' from the beginning and the end if added
    if len(rows[-1]) > 1:  # Ensure there is something to remove
        if rows[-1][0] == '1':
            last_row = rows[-1][1:]  # Remove the first '1'
            if last_row[0] == '0':
                last_row = last_row[1:]  # Remove leading '0' if present
        if last_row[-1] == '1':
            last_row = last_row[:-1]  # Remove the last '1'
            if last_row[-1] == '0':
                last_row = last_row[:-1]  # Remove trailing '0' if present
        rows[-1] = last_row

    # Join the rows back together with "/"
    new_fen = "/".join(rows)
    return new_fen


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
    current_player = main.Player.BLUE  # Assuming Red player starts the game

    board.create_board(fen)
    print("starting fen : ", fen)
    print("the current player is ", current_player)

    while True:
        reformulated = main.reformulate(fen)
        # Visualize the board
        board_stack = main.visualize_board(reformulated)
        # Calculate all possible moves for the current player
        possible_moves = zuggenerator.get_possible_moves(fen, current_player, board_stack)
        game_result = zuggenerator.check_game_end(fen)

        if game_result:
            print(game_result)
            break
        else:
            random_move = random.choice(possible_moves)  # Randomly select a move from the list of possible moves
            start_pos, end_pos = parse_move(random_move)
            board_stack = zuggenerator.do_move(start_pos, end_pos, current_player, board_stack)
            # print("board after update")
            '''for row in board_stack:
                print(" | ".join(str(cell) for cell in row))'''

        trimmed_board = main.trim_corners(board_stack)
        fen = main.board_to_fen(trimmed_board)
        print("Random move : ", random_move)
        print("Updated FEN : ", fen)
        board.create_board(fen)

        current_player = main.Player.RED if current_player == main.Player.BLUE else main.Player.BLUE
        print("the current player is ", current_player)
# Call the play_game function to start the game
play_game()