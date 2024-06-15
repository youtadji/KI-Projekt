import copy
import random

class Pos:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def to_chess_notation(self):
        # Convert row index to chess notation (A-H)
        chess_col = chr(ord('A') + self.col)
        # Convert column index to chess notation (1-8)
        chess_row = str(self.row + 1)
        # Combine row and column notation
        return chess_col + chess_row


class Bitboards:
    def __init__(self):
        self.r = 0
        self.b = 0
        self.rb = 0
        self.br = 0
        self.bb = 0
        self.rr = 0
        self.all_pieces = 0

    def set_piece(self, piece_type, row, col):
        # Calculate the bit position based on row and column
        bit_position = row * 8 + col
        if piece_type == 'r':
            self.r |= 1 << bit_position  # Set the bit in the 'r' bitboard - it adds 1 in the r board where the position is
        elif piece_type == 'b':
            self.b |= 1 << bit_position  # Set the bit in the 'b' bitboard
        elif piece_type == 'rb':
            self.rb |= 1 << bit_position  # Set the bit in the 'rb' bitboard
        elif piece_type == 'br':
            self.br |= 1 << bit_position  # Set the bit in the 'br' bitboard
        elif piece_type == 'bb':
            self.bb |= 1 << bit_position  # Set the bit in the 'bb' bitboard
        elif piece_type == 'rr':
            self.rr |= 1 << bit_position  # Set the bit in the 'rr' bitboard
        # Update the all_pieces bitboard
        self.all_pieces |= 1 << bit_position

    def get_piece(self, row, col):
        # Calculate the bit position based on row and column
        bit_position = row * 8 + col
        # Check each bitboard to see which piece is at the given position
        if self.r & (1 << bit_position):  #and operation between r bitboard and 1 at the given position
            return 'r'
        elif self.b & (1 << bit_position):
            return 'b'
        elif self.rb & (1 << bit_position):
            return 'rb'
        elif self.br & (1 << bit_position):
            return 'br'
        elif self.bb & (1 << bit_position):
            return 'bb'
        elif self.rr & (1 << bit_position):
            return 'rr'
        return None  # No piece at this position

    def remove_piece(self, row, col):
        bit_position = row * 8 + col
        self.r &= ~(1 << bit_position)
        self.b &= ~(1 << bit_position)
        self.rb &= ~(1 << bit_position)
        self.br &= ~(1 << bit_position)
        self.bb &= ~(1 << bit_position)
        self.rr &= ~(1 << bit_position)
        self.all_pieces &= ~(1 << bit_position)

    def print_board(self, board, name):
        print(f"{name}:")
        for row in reversed(range(8)):  # Print rows from 7 to 0
            for col in range(8):
                bit_position = row * 8 + col
                if board & (1 << bit_position):
                    if name in ["rr", "r", "br"]:
                        print("\x1b[31m1\x1b[0m", end=" ")  # Red color
                    elif name in ["bb", "b", "rb"]:
                        print("\x1b[34m1\x1b[0m", end=" ")  # Blue color
                else:
                    print(".", end=" ")
            print()

    def print_all_boards(self):
        self.print_board(self.r, "r")
        self.print_board(self.b, "b")
        self.print_board(self.rb, "rb")
        self.print_board(self.br, "br")
        self.print_board(self.bb, "bb")
        self.print_board(self.rr, "rr")
        self.print_board(self.all_pieces, "All Pieces")

    def combine_boards(self):
        combined = [["." for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece:
                    combined[row][col] = piece
        # Set corners to '0'
        combined[0][0] = '0'
        combined[0][7] = '0'
        combined[7][0] = '0'
        combined[7][7] = '0'
        return combined

    def print_combined_board(self):
        combined_board = self.combine_boards()
        print("Combined Board:")
        for row_idx, row in enumerate(reversed(combined_board)):  # Print rows from 7 to 0
            print("\x1b[95m{}\x1b[0m".format(8 - row_idx), end=" ")  # Pink color for row numbers
            for piece in row:
                if piece == 'r':
                    print("\x1b[31mr\x1b[0m", end=" ")  # Red 'r'
                elif piece == 'b':
                    print("\x1b[34mb\x1b[0m", end=" ")  # Blue 'b'
                elif piece == 'rb':
                    print("\x1b[34mrb\x1b[0m", end=" ")  # Blue 'rb'
                elif piece == 'br':
                    print("\x1b[31mbr\x1b[0m", end=" ")  # Red 'br'
                elif piece == 'bb':
                    print("\x1b[34mbb\x1b[0m", end=" ")  # Blue 'bb'
                elif piece == 'rr':
                    print("\x1b[31mrr\x1b[0m", end=" ")  # Red 'rr'
                else:
                    print(piece, end=" ")
            print()
        print("\x1b[95m{}\x1b[0m".format("  A B C D E F G H"))  # Pink color for column headers


def reformulate(fen):
    rows = fen.split("/")
    rows[0] = "1" + rows[0] + "1"
    rows[7] = "1" + rows[7] + "1"
    new_fen = "/".join(rows)
    return new_fen


def parse_fen(fen):
    bitboards = Bitboards()
    rows = fen.split('/')

    for row_num, row in enumerate(rows):
        col = 0
        i = 7 - row_num  # Map the FEN row to the board row, starting from the top

        j = 0
        while j < len(row):
            char = row[j]
            if col >= 8:
                break  # Prevent going out of column bounds

            if char == 'r':
                if j < len(row) - 1 and row[j + 1] == '0':
                    bitboards.set_piece('r', i, col)
                    j += 1  # Skip the next character
                elif j < len(row) - 1 and row[j + 1] == 'b':
                    bitboards.set_piece('rb', i, col)
                    j += 1  # Skip the next character
                elif j < len(row) - 1 and row[j + 1] == 'r':
                    bitboards.set_piece('rr', i, col)
                    j += 1  # Skip the next character
                else:
                    bitboards.set_piece('r', i, col)
            elif char == 'b':
                if j < len(row) - 1 and row[j + 1] == '0':
                    bitboards.set_piece('b', i, col)
                    j += 1  # Skip the next character
                elif j < len(row) - 1 and row[j + 1] == 'r':
                    bitboards.set_piece('br', i, col)
                    j += 1  # Skip the next character
                elif j < len(row) - 1 and row[j + 1] == 'b':
                    bitboards.set_piece('bb', i, col)
                    j += 1  # Skip the next character
                else:
                    bitboards.set_piece('b', i, col)
            elif char.isdigit():
                col += int(char)  # Skip the corresponding number of columns
                j += 1
                continue  # Skip the increment of col below

            col += 1
            j += 1

    return bitboards


def check_game_end(bitboards):
    # Masks to isolate the top row (row 0) and bottom row (row 7)
    top_row_mask = 0xFF00000000000000
    bottom_row_mask = 0x00000000000000FF

    # Check if any red pieces are in the top row (row 0)
    if (bitboards.r & top_row_mask) or (bitboards.rr & top_row_mask) or (bitboards.br & top_row_mask):
        return "Game Over: Red wins :D"

    # Check if any blue pieces are in the bottom row (row 7)
    if (bitboards.b & bottom_row_mask) or (bitboards.bb & bottom_row_mask) or (bitboards.rb & bottom_row_mask):
        return "Game Over: Blue wins :D"

    return None  # Game is not over yet


def calculate_possible_moves_for_stack(bitboards, row, col, player):
    possible_moves = []

    # Directions for stack piece movements
    if player == 'r':
        move_directions = [(2, 1), (2, -1), (1, -2), (1, 2)]
    else:
        move_directions = [(-1, -2), (-1, 2), (-2, -1), (-2, 1)]

    # Iterate over possible move directions
    for dr, dc in move_directions:
        r, c = row, col

        # Calculate the new position
        r_new = r + dr
        c_new = c + dc

        # Check if the move is within board boundaries
        if 0 <= r_new < 8 and 0 <= c_new < 8:
            bit_position = r_new * 8 + c_new

            # Check if the position is empty or contains exactly one piece
            if (not (bitboards.all_pieces & (1 << bit_position))) or \
                    ((bitboards.r & (1 << bit_position)) ^ (bitboards.b & (1 << bit_position))):
                possible_moves.append((r_new, c_new))


    return possible_moves


# Function to calculate possible moves
def calculate_possible_moves(bitboard, row, col, player):
    forbidden_positions = [(0, 0), (7, 7), (0, 7), (7, 0)]
    possible_moves = []
    piece = bitboards.get_piece(row, col)
    #piece = 1 << (row * 8 + col)
    #print("top piece: ", piece[-1], "player: ", player)

    if piece == 'r':
        move_directions = [(0, 1), (0, -1), (1, 0)]
        capture_directions = [(1, -1), (1, 1)]
    elif piece == 'b':
        move_directions = [(-1, 0), (0, 1), (0, -1)]
        capture_directions = [(-1, 1), (-1, -1)]
    elif piece in ['rr', 'br', 'bb', 'rb']:
        move_directions = calculate_possible_moves_for_stack(bitboard, row, col, player)
        return move_directions

    # Iterate over possible move directions
    for dr, dc in move_directions:
        r, c = row + dr, col + dc
        bit_position = r * 8 + c
        # Check if the move is within bounds and the square is empty
        if 0 <= r < 8 and 0 <= c < 8 and (r, c) not in forbidden_positions:
            if not (bitboards.all_pieces & (1 << bit_position)):
                possible_moves.append((r, c))  # if there is no piece then move
            elif piece == 'r' and (bitboards.r & (1 << bit_position)):  # occupied by a single red
                possible_moves.append((r, c))
            elif piece == 'b' and (bitboards.b & (1 << bit_position)):
                possible_moves.append((r, c))

        # Iterate over possible capture directions
    for dr, dc in capture_directions:
        r, c = row + dr, col + dc
        bit_position = r * 8 + c
        # Check if the move is within bounds and there's an opponent's piece
        if (0 <= r < 8 and 0 <= c < 8 and
                bitboards.all_pieces & (1 << (r * 8 + c)) and
                (r, c) not in forbidden_positions):
            if player == 'r' and (
                    (bitboards.b & (1 << bit_position)) != 0 or
                    (bitboards.rb & (1 << bit_position)) != 0 or
                    (bitboards.bb & (1 << bit_position)) != 0):
                possible_moves.append((r, c))
            elif player == 'b' and (
                    (bitboards.r & (1 << bit_position)) != 0 or
                    (bitboards.br & (1 << bit_position)) != 0 or
                    (bitboards.rr & (1 << bit_position)) != 0):
                possible_moves.append((r, c))
            #possible_moves.append((r, c))
    return possible_moves

def get_all_pieces(bitboards, player):
    pieces = []
    for row in range(8):
        for col in range(8):
            piece = bitboards.get_piece(row, col)

            if piece and piece[-1] == player:
                    pieces.append((row, col))
    return pieces


# Function to calculate possible moves for all pieces of a player
def calculate_all_possible_moves(bitboards, player):
    all_possible_moves = {}
    pieces = get_all_pieces(bitboards, player)
    for row, col in pieces:
        possible_moves = calculate_possible_moves(bitboards, row, col, player)
        all_possible_moves[(row, col)] = possible_moves
    return all_possible_moves


def print_all_possible_moves(all_possible_moves):
    def to_chess_notation(row, col):
        chess_col = chr(ord('A') + col)
        chess_row = str(row + 1)
        return chess_col + chess_row

    for start_pos, moves in all_possible_moves.items():
        start_row, start_col = start_pos
        start_pos_chess = to_chess_notation(start_row, start_col)
        for move in moves:
            end_row, end_col = move
            end_pos_chess = to_chess_notation(end_row, end_col)
            print(f"{start_pos_chess}-{end_pos_chess}")


def do_move(start_pos, end_pos, player, bitboards):
    # Create a deep copy of the bitboards
    updated_bitboards = copy.deepcopy(bitboards)
    #print("start row", start_pos.row)
    # Get the piece type at the start position
    start_piece_type = updated_bitboards.get_piece(start_pos.row, start_pos.col)
    if not start_piece_type:
        print(f"No piece at start position ({start_pos.row}, {start_pos.col})")
    else:
        # Remove the piece from the start position
        updated_bitboards.remove_piece(start_pos.row, start_pos.col)
        #end_piece_type = updated_bitboards.get_piece(end_pos.row, end_pos.col)

        if start_piece_type == 'rr' and player == 'r':
            updated_bitboards.set_piece('r', start_pos.row, start_pos.col)
        elif start_piece_type == 'br' and player == 'r':
            updated_bitboards.set_piece('b', start_pos.row, start_pos.col)
        elif start_piece_type == 'rb' and player == 'b':
            updated_bitboards.set_piece('r', start_pos.row, start_pos.col)
        elif start_piece_type == 'bb' and player == 'b':
            updated_bitboards.set_piece('b', start_pos.row, start_pos.col)


    end_piece_type = updated_bitboards.get_piece(end_pos.row, end_pos.col)

    if end_piece_type:


        if end_piece_type == 'r' and player == 'b'  :

                updated_bitboards.remove_piece(end_pos.row, end_pos.col)
                updated_bitboards.set_piece('b', end_pos.row, end_pos.col)
        elif end_piece_type == 'r' and player == 'r':
                updated_bitboards.remove_piece(end_pos.row, end_pos.col)
                updated_bitboards.set_piece('rr', end_pos.row, end_pos.col)
                #in all cases if thestart one is rr, or br or r we always have the end pos becoming rr
        elif end_piece_type == 'b' and player == 'r':
                updated_bitboards.remove_piece(end_pos.row, end_pos.col)
                updated_bitboards.set_piece('r', end_pos.row, end_pos.col)
                #i all cases ae are eating the blue and will get just red ine nd pos
        elif end_piece_type == 'b' and player == 'b':
            updated_bitboards.remove_piece(end_pos.row, end_pos.col)
            updated_bitboards.set_piece('bb', end_pos.row, end_pos.col)
               # same all cases bb
        elif end_piece_type == 'rb' and player == 'r':
            updated_bitboards.remove_piece(end_pos.row, end_pos.col)
            updated_bitboards.set_piece('rr', end_pos.row, end_pos.col)
        elif end_piece_type == 'bb' and player == 'r':
            updated_bitboards.remove_piece(end_pos.row, end_pos.col)
            updated_bitboards.set_piece('br', end_pos.row, end_pos.col)
        elif end_piece_type == 'rr' and player == 'b':
            updated_bitboards.remove_piece(end_pos.row, end_pos.col)
            updated_bitboards.set_piece('rb', end_pos.row, end_pos.col)
        elif end_piece_type == 'br' and player == 'b':
            updated_bitboards.remove_piece(end_pos.row, end_pos.col)
            updated_bitboards.set_piece('bb', end_pos.row, end_pos.col)

    else:
         if player == 'r':
                updated_bitboards.set_piece('r', end_pos.row, end_pos.col)
         else:
                updated_bitboards.set_piece('b', end_pos.row, end_pos.col)
    return updated_bitboards

def update_fen(bitboards):
    fen_rows = []
    for row in range(7, -1, -1):
        fen_row = ""
        empty_count = 0
        for col in range(8):
            piece = bitboards.get_piece(row, col)
            if piece:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += piece
            else:
                empty_count += 1
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)
    return "/".join(fen_rows)


# Function to simulate the game with random moves until it ends
def simulate_game(bitboards):
    current_player = 'r'
    while True:
        all_possible_moves = calculate_all_possible_moves(bitboards, current_player)
        if not all_possible_moves:
            print("No possible moves left for", current_player)
            break


        start_pos, possible_moves = random.choice(list(all_possible_moves.items()))
        print("all possible moves ", all_possible_moves)
        print("for this starts position ", start_pos,"we will pick one if these :",possible_moves)
        end_pos = random.choice(possible_moves)
        print("we picked this one",end_pos)


        print(
            f"{current_player} moves from {Pos(*start_pos).to_chess_notation()} to {Pos(*end_pos).to_chess_notation()}")
        bitboards = do_move(Pos(*start_pos), Pos(*end_pos), current_player, bitboards)
        bitboards.print_combined_board()
        game_end = check_game_end(bitboards)
        if game_end:
            print(game_end)
            break
        current_player = 'b' if current_player == 'r' else 'r'

# Example Usage
'''fen = "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0"
bitboards = parse_fen(reformulate(fen))
bitboards.print_combined_board()

simulate_game(bitboards)'''

fen = "b0br4/1b0b05/b01b0rr4/1rb1b01b02/3r0r01rr2/bbr0r02rr2/4r01rr1/r04r0"
bitboards = parse_fen(reformulate(fen))
bitboards.print_combined_board()
#row, col = 4, 1
player = 'r'
all_possible_moves = calculate_all_possible_moves(bitboards, player)
print("these are all possible moves for player ", player , ": ", all_possible_moves)
start_pos, possible_moves = random.choice(list(all_possible_moves.items()))
print(" for this random start pos", start_pos,  "this is its list of end position", possible_moves)
end_pos = random.choice(possible_moves)
print(" and thus is the one picked: " , end_pos)
updated_bitboards = do_move(Pos(*start_pos), Pos(*end_pos), player, bitboards)
updated_bitboards.print_combined_board()
#print_all_possible_moves(all_possible_moves)
#piece = bitboards.get_piece(row, col)
#print(f"Piece at ({row}, {col}): {piece}")'''
