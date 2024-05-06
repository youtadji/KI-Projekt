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
            else:
                raise ValueError(f"Unexpected character {char} in FEN string")

def set_corners(board):
    # Set the four corners to '0'
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for x, y in corners:
        board[x][y] = '0'
'''
def switch_pieces(board):
    # Switch 'b' and 'r' on the board
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 'b':
                board[row][col] = 'r'
            elif board[row][col] == 'r':
                board[row][col] = 'b'
            elif board[row][col] == 'rr':
                board[row][col] = 'bb'
            elif board[row][col] == 'bb':
                board[row][col] = 'rr'
            elif board[row][col] == 'rb':
                board[row][col] = 'br'
            elif board[row][col] == 'br':
                board[row][col] = 'rb'
'''

def print_board(board):
    # Print the board
    print("Board layout:")
    board.reverse()
    for row in board:
        print(' '.join(row))

# Main execution
board = initialize_board()
fen = "b0b0b02bb/1b01b0bb1b01/2b05/5b02/1r06/8/2r0rrr0rr1r0/r0r01r01r0"
setup_pieces(board, fen)
set_corners(board)  # Set corners after initial setup
#switch_pieces(board)  # Switch 'b' and 'r' after setup
print_board(board)