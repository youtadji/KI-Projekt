def initialize_board():
    # Create an 8x8 board with empty fields
    board = [['.' for _ in range(8)] for _ in range(8)]
    return board

def setup_pieces(board, fen):
    # Break down the FEN string into rows
    rows = fen.split('/')
    for row_index, row in enumerate(rows):
        col_index = 0
        i = 0
        # Initialize row shifting for the first and last rows
        if row_index == 0 or row_index == len(rows) - 1:
            board[row_index][col_index] = '.'
            col_index += 1  # Start from the second column
        while i < len(row):
            char = row[i]
            if char.isdigit():
                # Add the appropriate number of empty fields
                for _ in range(int(char)):
                    if col_index < 8:  # Ensure we don't go out of bounds
                        board[row_index][col_index] = '.'
                        col_index += 1
                i += 1
            elif char in 'br':
                #stack
                if i + 1 < len(row) and row[i + 1] in 'br':
                    combined_char = char + row[i + 1]
                    # Set the combined value on the board
                    if col_index < 8:
                        board[row_index][col_index] = combined_char
                        col_index += 1
                    # Skip the next character as it's used in combination
                    i += 1
                # Set the piece on the board
                elif col_index < 8:  # Ensure we don't go out of bounds
                    board[row_index][col_index] = char
                    col_index += 1
                i += 1
            elif char == '1':
                # Skip '1' if it's treated as a delimiter
                i += 1
            '''else:
                raise ValueError(f"Unexpected character {char} in FEN string")
'''
def set_corners(board):
    # Set the four corners to '0'
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for x, y in corners:
        board[x][y] = '0'

'''def print_board(board):

    # Print the board
    print("Board layout:")
    board.reverse()
    for row in board:
        print(' '.join(row))

'''

def print_board(board):
    # Define ANSI escape codes for colors
    RED = "\033[31m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"  # Magenta is often used as pink in terminal color schemes
    RESET = "\033[0m"

    print("Board layout:")
    # Print column labels in pink (magenta)
    column_labels = ' '.join(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
    #print(MAGENTA + "  " + column_labels + RESET)

    # Print the board with row numbers, using colors for 'r', 'b', 'rr', and 'bb'
    for index, row in enumerate(board[::-1]):  # Reverse board for correct display
        row_display = []
        for piece in row:
            if 'r' in piece:
                row_display.append(RED + piece + RESET)
            elif 'b' in piece:
                row_display.append(BLUE + piece + RESET)
            else:
                row_display.append(piece)
        # Row label in pink (magenta)
        print(MAGENTA + str(8 - index) + RESET, ' '.join(row_display))

    # Print the column labels again at the bottom in pink (magenta)
    print(MAGENTA + "  " + column_labels + RESET)
    # Printing the "table flip" emoticon
    print("(ﾉಠдಠ)ﾉ︵┻━┻")


def create_board(fen):
    board = initialize_board()
    setup_pieces(board, fen)
    set_corners(board)  # Set corners after initial setup
    print_board(board)
    return board

'''# Main execution
board = initialize_board()
fen = "b0b0b02bb/1b01b0bb1b01/2b05/5b02/1r06/8/2r0rrr0rr1r0/r0r01r01r0"
setup_pieces(board, fen)
set_corners(board)  # Set corners after initial setup
#switch_pieces(board)  # Switch 'b' and 'r' after setup
print_board(board)'''
'''
fen = "b0b0b02bb/1b01b0bb1b01/2b05/5b02/1r06/8/2r0rrr0rr1r0/r0r01r01r0"
board = create_board(fen)
#print_board(board)'''
# Example of using ANSI escape codes in Python to color terminal output

# Define some ANSI escape codes for colors
'''RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# Use them in print statements
print(f"{RED}This text is red!{RESET}")
print(f"{GREEN}This text is green!{RESET}")
print(f"{YELLOW}This text is yellow!{RESET}")'''