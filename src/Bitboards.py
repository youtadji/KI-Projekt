import copy
import random
import time
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

transposition_table = {}

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
        bit_position = row * 8 + col

        if self.rr & (1 << bit_position):
            return 'rr'
        elif self.br & (1 << bit_position):
            return 'br'
        elif self.bb & (1 << bit_position):
            return 'bb'
        elif self.rb & (1 << bit_position):
            return 'rb'
        elif self.r & (1 << bit_position):
            return 'r'
        elif self.b & (1 << bit_position):
            return 'b'

        return None  # No piece found at this position

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

    def get_all_pieces(self, player):
        # Select the correct bitboard for the current player ('r' for red, 'b' for blue)
        bitboard = self.r if player == 'r' else self.b

        # Initialize an empty list to hold the positions of the pieces
        positions = []

        # Iterate over each bit position in the bitboard (0 to 63 for an 8x8 board)
        for i in range(64):
            # Check if the bit at position i is set (indicating a piece is present)
            if bitboard & (1 << i):
                # Calculate the row and column from the bit index and add to the positions list
                positions.append((i // 8, i % 8))

        # Return the list of positions where pieces are present for the given player
        return positions


def reformulate(fen):
    rows = fen.split("/")
    rows[0] = "1" + rows[0] + "1"
    rows[7] = "1" + rows[7] + "1"
    new_fen = "/".join(rows)
    return new_fen

def reverse_fen(fen):
    # Split the FEN string into parts
    parts = fen.split(' ')
    position = parts[0]
    color = parts[1] if len(parts) > 1 else None

    # Split the position into rows and reverse the order
    rows = position.split('/')
    reversed_rows = rows[::-1]

    # Join the reversed rows back into a position string
    reversed_position = '/'.join(reversed_rows)

    # Reconstruct the FEN string
    reversed_fen = reversed_position
    if color:
        reversed_fen += f' {color}'

    return reversed_fen

def parse_fen(fen):
    bitboards = Bitboards()
    rows = fen.split('/')
    rows.reverse()  # Reverse the rows to parse from bottom to top

    for row_num, row in enumerate(rows):
        col = 0
        i = 7 - row_num  # Map the FEN row to the board row, starting from the top (7th rank) 0

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
    if (bitboards.b & top_row_mask) or (bitboards.rb & top_row_mask) or (bitboards.bb & top_row_mask):
        return "Game Over: Blue wins :D"

    # Check if any blue pieces are in the bottom row (row 7)
    if (bitboards.r & bottom_row_mask) or (bitboards.br & bottom_row_mask) or (bitboards.rr & bottom_row_mask):
        return "Game Over: Red wins :D"

    return None  # Game is not over yet


def calculate_possible_moves_for_stack(bitboards, row, col, player):
    forbidden_positions = [(0, 0), (7, 7), (0, 7), (7, 0)]

    possible_moves = []

    # Directions for stack piece movements
    if player == 'b':
        move_directions = [(2, 1), (2, -1), (1, -2), (1, 2)]
    else:
        move_directions = [(-2, -1), (-1, -2), (-1, 2),  (-2, 1)]

    # Iterate over possible move directions
    for dr, dc in move_directions:
        r, c = row, col

        # Calculate the new position
        r_new = r + dr
        c_new = c + dc

        # Check if the move is within board boundaries
        if 0 <= r_new < 8 and 0 <= c_new < 8 and (r_new, c_new) not in forbidden_positions:
            bit_position = r_new * 8 + c_new

            # Check if the position is empty or contains exactly one piece
            if ((bitboards.r & (1 << bit_position)) ^ (bitboards.b & (1 << bit_position))) or \
                    ((bitboards.br & (1 << bit_position)) and player == 'b') or \
                    ((bitboards.rb & (1 << bit_position)) and player == 'r') or \
                    ((bitboards.bb & (1 << bit_position)) and player == 'r') or \
                    ((bitboards.rr & (1 << bit_position)) and player == 'b') or \
                    (not (bitboards.all_pieces & (1 << bit_position))) :
                possible_moves.append((r_new, c_new))

    return possible_moves


# Function to calculate possible moves
def calculate_possible_moves(bitboard, row, col, player):
    forbidden_positions = [(0, 0), (7, 7), (0, 7), (7, 0)]
    possible_moves = []
    piece = bitboard.get_piece(row, col)
    #print(f"Calculating moves for piece at ({row}, {col}): {piece}")
    if piece in ['rr', 'br', 'bb', 'rb']:
        #print("Piece is a stack piece.")
        return calculate_possible_moves_for_stack(bitboard, row, col, player)
        #print("Stack piece moves:", moves)

    if piece == 'b':
        move_directions = [(0, 1), (0, -1), (1, 0)]
        capture_directions = [(1, -1), (1, 1)]
    elif piece == 'r':
        move_directions = [(-1, 0), (0, 1), (0, -1)]
        capture_directions = [(-1, 1), (-1, -1)]
    else:
        print("Unknown piece type.")
        #####when SIMUALTING GAME after few secoonds you will get none for some pieces even tho they are there CHECK WHYYYYYYYYY BIITE I AM GONNA KILL MYSELF
        ####i fugured theNONE is coming from either set or get piece so there s some issue in do move or there with updating the board
        return []

    # Iterate over possible move directions
    for dr, dc in move_directions:
        r, c = row + dr, col + dc
        bit_position = r * 8 + c
        # Check if the move is within bounds and the square is empty
        if 0 <= r < 8 and 0 <= c < 8 and (r, c) not in forbidden_positions:
            if not (bitboard.all_pieces & (1 << bit_position)):
                #bitboards.print_all_boards(bitboards)
                possible_moves.append((r, c))  # if there is no piece then move
            elif piece == 'r' and (bitboard.r & (1 << bit_position)):  # occupied by a single red
                possible_moves.append((r, c))
            elif piece == 'b' and (bitboard.b & (1 << bit_position)):
                possible_moves.append((r, c))

    # Iterate over possible capture directions
    for dr, dc in capture_directions:
        r, c = row + dr, col + dc
        bit_position = r * 8 + c
        # Check if the move is within bounds and there's an opponent's piece
        if (0 <= r < 8 and 0 <= c < 8 and
                bitboard.all_pieces & (1 << (r * 8 + c)) and
                (r, c) not in forbidden_positions):
            if player == 'r' and (
                    (bitboard.b & (1 << bit_position)) != 0 or
                    (bitboard.rb & (1 << bit_position)) != 0 or
                    (bitboard.bb & (1 << bit_position)) != 0):
                possible_moves.append((r, c))
            elif player == 'b' and (
                    (bitboard.r & (1 << bit_position)) != 0 or
                    (bitboard.br & (1 << bit_position)) != 0 or
                    (bitboard.rr & (1 << bit_position)) != 0):
                possible_moves.append((r, c))
            #possible_moves.append((r, c))
    #print(f"Possible moves calculated: {possible_moves}")
    return possible_moves


def calculate_all_possible_moves(bitboards, player):
    all_possible_moves = {}

    for row in range(8):
        for col in range(8):
            piece = bitboards.get_piece(row, col)
            if piece and piece[-1] == player:
                possible_moves = calculate_possible_moves(bitboards, row, col, player)
                all_possible_moves[(row, col)] = possible_moves

    return all_possible_moves


def print_return_all_possible_moves(all_possible_moves):
    all_moves = []
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
            move = f"{start_pos_chess}-{end_pos_chess}"
            all_moves.append(move)
            #print(f"{start_pos_chess}-{end_pos_chess}")
    return all_moves


def do_move(start_pos, end_pos, player, bitboards):
    # Create a deep copy of the bitboards
    updated_bitboards = copy.deepcopy(bitboards)  #max recursion reach

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

        if end_piece_type == 'r' and player == 'b':

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


def calculate_score(bitboards, player, move=None):
    score = 0
    piece_values = {'r': 1, 'b': 1, 'rr': 2, 'bb': 2, 'br': 2, 'rb': 2}  # Base values for pieces
    capture_bonus = 5  # Bonus score for capturing an opponent's piece

    if player == 'r':
        opponent = 'b'
        diagonal_directions = [(-1, -1), (-1, 1)]
        horse_directions = [(-2, 1), (-2, -1), (-1, -2), (-1, 2)]  # y, x
    else:
        opponent = 'r'
        diagonal_directions = [(1, 1), (1, -1)]
        horse_directions = [(1, -2), (1, 2), (2, -1), (2, 1)]

    if move:
        start_pos, end_pos = move
        end_piece = bitboards.get_piece(end_pos[0], end_pos[1])
        if end_piece and end_piece[0] == opponent:
            score += capture_bonus

    pieces = bitboards.get_all_pieces(player)
    for row, col in pieces:
        piece = bitboards.get_piece(row, col)

        # Check if the piece has reached the finish line
        """if (player == 'r' and row == 7) or (player == 'b' and row == 0):
            print("NEW IF")
            return 200  # Set score to 200 if the current player reached the finish line"""

        # Determine the score based on proximity to the finish line
        if player == 'b':  # Red player aims for the top row
            proximity_score = (row - 0)  # Score increases as red moves upwards
        elif player == 'r':  # Blue player aims for the bottom row
            proximity_score = (7 - row)  # Score increases as blue moves downwards

        # Calculate the base score using piece values and proximity
        base_score = piece_values.get(piece[0], 0) * proximity_score
        score += base_score

        # Check for threats from diagonals
        for dr, dc in diagonal_directions:
            threat_row, threat_col = row + dr, col + dc
            if 0 <= threat_row < 8 and 0 <= threat_col < 8:
                threat_piece = bitboards.get_piece(threat_row, threat_col)
                if threat_piece and threat_piece[0] == opponent:
                    score -= piece_values.get(piece[0], 0)  # Subtract score if threatened by opponent
                    break
                elif threat_piece and threat_piece[0] == player:
                    score += 1  # Add score if the player's piece is in a diagonal position

        # Check for threats from horse directions
        horse_threats = 0
        for dr, dc in horse_directions:
            threat_row, threat_col = row + dr, col + dc
            if 0 <= threat_row < 8 and 0 <= threat_col < 8:
                threat_piece = bitboards.get_piece(threat_row, threat_col)
                if threat_piece and threat_piece[0] == opponent:

                    score -= piece_values.get(piece[0], 0)  # Subtract score if threatened by two opponents
                    break  # Only need to subtract once per piece
                elif threat_piece and threat_piece[0] == player:
                    score += 2  # Add score if the player's piece is in a horse position
    """if player == 'b':
        score *= -1"""
    return score


def alpha_beta(bitboards, alpha, beta, depth, player, start_time, time_limit, move=None):
    if time.time() - start_time > time_limit:
        if player == 'r':
            return calculate_score(bitboards, 'b', move), None
        else:
            return calculate_score(bitboards, 'r', move), None


    game_end_status = check_game_end(bitboards)
    if game_end_status:
        if game_end_status == "Game Over: Blue wins :D":
            if player == 'b':
                # print("Blue won, player b")
                return float('inf'), None
            else:
                # print("game end stat")
                return float('-inf'), None
        if game_end_status == "Game Over: Red wins :D":
            if player == 'r':
                return float('inf'), None
            else:
                return float('-inf'), None

    if depth == 0:
        #return calculate_score(bitboards, player), None
        if player == 'r':

            return calculate_score(bitboards, 'b', move), None
        else:
            return calculate_score(bitboards, 'r', move), None

    best_move = None
    all_possible_moves = calculate_all_possible_moves(bitboards, player)
    if player == 'r':
        max_eval = float('-inf')  #Do we need max_eval and alpha, or can we use the same variable?
        for start_pos, moves in all_possible_moves.items():
            for end_pos in moves:
                updated_bitboards = do_move(Pos(*start_pos), Pos(*end_pos), player, bitboards)
                move = (start_pos, end_pos)
                eval, _ = alpha_beta(updated_bitboards, alpha, beta, depth - 1, 'b', start_time, time_limit, move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (start_pos, end_pos)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval, best_move  ###it evaluates the score from the blue's pov, and as it didnt move, it is getting the same score for both red movements, and is just getting the first end position bec eval !> maxeval --> i changed the calc score fkt to take -p
    else:
        min_eval = float('inf')
        for start_pos, moves in all_possible_moves.items():
            for end_pos in moves:
                updated_bitboards = do_move(Pos(*start_pos), Pos(*end_pos), player, bitboards)
                eval, _ = alpha_beta(updated_bitboards, alpha, beta, depth - 1, 'r', start_time, time_limit)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (start_pos, end_pos)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
    return min_eval, best_move

def game_stage(bitboards):
    # Count pieces on the board
    num_red_pieces = bin(bitboards.r).count('1') + bin(bitboards.rr).count('1')
    num_blue_pieces = bin(bitboards.b).count('1') + bin(bitboards.bb).count('1')

    total_pieces = num_red_pieces + num_blue_pieces

    # Thresholds for determining the stage based on the number of pieces
    if total_pieces > 24:
        return 'early'
    elif 12 < total_pieces <= 24:
        return 'mid'
    else:
        return 'late'
'''def dynamic_time_allocation(stage, base_time):
    if stage == 'early':
        return base_time * 0.5
    elif stage == 'mid':
        return base_time * 1.5
    else:
        return base_time * 0.75'''
def dynamic_time_allocation(stage, base_time):
    if stage == 'early':
        return base_time * 0.5
    elif stage == 'mid':
        return base_time * 1.5
    else:
        return base_time * 0.75

def iterative_deepening(bitboards, player, total_time):
    start_time = time.time()
    depth = 1
    best_move = None
    best_score = float('-inf') if player == 'r' else float('inf')

    stage = game_stage(bitboards)
    print("stage: ", stage)
    time_per_move = dynamic_time_allocation(stage, total_time)

    while time.time() - start_time < time_per_move:
        time_left = time_per_move - (time.time() - start_time)
        if time_left <= 0:
            break
        score, move = alpha_beta(bitboards, float('-inf'), float('inf'), depth, player, start_time, time_left)
        if time.time() - start_time < total_time and move:
            start_pos, end_pos = move
            print("Depth = ", depth)
            print(f"move: {Pos(*start_pos).to_chess_notation()} to {Pos(*end_pos).to_chess_notation()}", "score: ", score)

            if (player == 'r' and score > best_score) or (player == 'b' and score < best_score):
                best_score = score
                best_move = move

        depth += 1

    return best_score, best_move

'''def iterative_deepening(bitboards, player, total_time, total_moves):
    start_time = time.time()
    depth = 1
    best_move = None
    best_score = float('-inf')
    #best_score = 0

    stage = game_stage(total_moves)
    print("stage: ", stage)
    time_per_move = dynamic_time_allocation(stage, total_time)

    while time.time() - start_time < time_per_move:
        time_left = time_per_move - (time.time() - start_time)
        #print("time left: ", time_left, "time per move: ", time_per_move)
        if time_left <= 0:
            break  # if it breaks before calling alphabeta - -inf
        score, move = alpha_beta(bitboards, float('-inf'), float('inf'), depth, player, start_time, time_left)
        if time.time() - start_time < total_time and move:
            start_pos, end_pos = move
            print("Depth = ", depth)
            print(f"move: {Pos(*start_pos).to_chess_notation()} to {Pos(*end_pos).to_chess_notation()}", "score: ",
                  score)

            #if player == 'r':
            if score > best_score:
                best_score = score
                best_move = move

        depth += 1

    return best_score, best_move'''


def simulate_game(fen_player, total_time=120):
    player = fen_player[-1]
    fen = fen_player[:-2]
    bitboards = parse_fen(reformulate(fen))
    start_time = time.time()

    while time.time() - start_time < total_time:
        if check_game_end(bitboards):
            break

        move_time = min(total_time - (time.time() - start_time), 1.0)  # Allocate 1 second for each move
        best_score, best_move = iterative_deepening(bitboards, player, move_time)

        if not best_move:
            print("No valid move found", player, "Lost")
            break

        start_pos, end_pos = best_move
        bitboards = do_move(Pos(*start_pos), Pos(*end_pos), player, bitboards)
        print(f"{player.upper()} moved from {Pos(*start_pos).to_chess_notation()} to {Pos(*end_pos).to_chess_notation()}")
        bitboards.print_combined_board()

        player = 'b' if player == 'r' else 'r'

    print("Game Over")
    game_end_status = check_game_end(bitboards)
    if game_end_status:
        print(game_end_status)
    else:
        print("Time limit reached")
'''def simulate_game(fen_player, total_time=120):
    player = fen_player[-1]
    fen = fen_player[:-2]
    bitboards = parse_fen(reformulate(fen))
    total_moves = 0
    start_time = time.time()

    while time.time() - start_time < total_time:
        if check_game_end(bitboards):
            break

        move_time = min(total_time - (time.time() - start_time), 1.0)  # Allocate 1 second for each move
        best_move = iterative_deepening(bitboards, player, move_time, total_moves)

        if not best_move:

            print("No valid move found", player, "Lost")
            break

        start_pos, end_pos = best_move
        bitboards = do_move(Pos(*start_pos), Pos(*end_pos), player, bitboards)
        print(
            f"{player.upper()} moved from {Pos(*start_pos).to_chess_notation()} to {Pos(*end_pos).to_chess_notation()}")
        bitboards.print_combined_board()



        player = 'b' if player == 'r' else 'r'
        total_moves += 1

    print("Game Over")
    game_end_status = check_game_end(bitboards)
    if game_end_status:
        print(game_end_status)
    else:
        print("Time limit reached")'''

'''def fitness_function_alpha_beta(bitboards, player, move, move_time, total_moves):
    start_pos, end_pos = move
    simulated_bitboards = do_move(Pos(*start_pos), Pos(*end_pos), player, bitboards)
    board_hash = hash(simulated_bitboards)

    if board_hash in transposition_table:
        return transposition_table[board_hash]

    opponent = 'b' if player == 'r' else 'r'
    score, _ = iterative_deepening(simulated_bitboards, opponent,  move_time, total_moves)
    #score, _ = alpha_beta(simulated_bitboards, float('-inf'), float('inf'), alpha_beta_depth, opponent, time.time(), 0.5)

    transposition_table[board_hash] = score
    return score
'''
def fitness_function_alpha_beta(bitboards, player, move, move_time):
    start_pos, end_pos = move
    simulated_bitboards = do_move(Pos(*start_pos), Pos(*end_pos), player, bitboards)
    board_hash = hash(simulated_bitboards)

    if board_hash in transposition_table:
        return transposition_table[board_hash]

    opponent = 'b' if player == 'r' else 'r'
    score, _ = iterative_deepening(simulated_bitboards, opponent, move_time)

    transposition_table[board_hash] = score
    return score

def evaluate_population(bitboards, player, population, move_time, total_moves):
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        futures = [executor.submit(fitness_function_alpha_beta, bitboards, player, move, move_time, total_moves) for move in population]
        fitnesses = [future.result() for future in futures]
    return fitnesses


# Initialpopulation erzeugen
def generate_initial_population(bitboards, player, pop_size):
    population = []
    all_possible_moves = calculate_all_possible_moves(bitboards, player)
    move_list = [(start_pos, end_pos) for start_pos in all_possible_moves for end_pos in all_possible_moves[start_pos]]
    for _ in range(pop_size):
        population.append(random.choice(move_list)) #we choose random 3 moves
    return population

# Selektion der besten Individuen
def select_parents(population, fitnesses, num_parents):
    parents = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
    return [parent[0] for parent in parents[:num_parents]]

def crossover(parents, num_offspring):
    offspring = []
    for _ in range(num_offspring):
        parent1, parent2 = random.sample(parents, 2)
        start_pos = parent1[0]
        end_pos = parent1[1]
        offspring.append((start_pos, end_pos))
    return offspring

def mutate(bitboards, offspring, mutation_rate, player):
    all_possible_moves = calculate_all_possible_moves(bitboards, player)
    move_list = [(start_pos, end_pos) for start_pos in all_possible_moves for end_pos in all_possible_moves[start_pos]]
    for i in range(len(offspring)):
        if random.random() < mutation_rate:
            offspring[i] = random.choice(move_list)
    return offspring

def evolutionary_algorithm_with_alpha_beta(bitboards, player, pop_size, num_generations, mutation_rate, move_time):
    population = generate_initial_population(bitboards, player, pop_size)

    for generation in range(num_generations):
        fitnesses = [fitness_function_alpha_beta(bitboards, player, move, move_time) for move in population]
        parents = select_parents(population, fitnesses, pop_size // 2)
        offspring = crossover(parents, pop_size - len(parents))
        population = parents + mutate(bitboards, offspring, mutation_rate, player)

        best_fitness = max(fitnesses) if player == 'r' else min(fitnesses)
        best_move = population[fitnesses.index(best_fitness)]
        print(f'Generation {generation + 1}: Best Fitness = {best_fitness}, Best Move = {best_move}')

    best_fitness = max(fitnesses) if player == 'r' else min(fitnesses)
    best_move = population[fitnesses.index(best_fitness)]
    return best_move, best_fitness
# Evolutionären Prozess durchführen
'''def evolutionary_algorithm_with_alpha_beta(bitboards, player, pop_size, num_generations, mutation_rate,
                                           move_time, total_moves):
    population = generate_initial_population(bitboards, player, pop_size)

    for generation in range(num_generations):
        fitnesses = [fitness_function_alpha_beta(bitboards, player, move, move_time, total_moves) for move in population]
        parents = select_parents(population, fitnesses, pop_size // 2)
        offspring = crossover(parents, pop_size - len(parents))
        population = parents + mutate(bitboards, offspring, mutation_rate, player)

        best_fitness = max(fitnesses)
        best_move = population[fitnesses.index(best_fitness)]
        print(f'Generation {generation + 1}: Best Fitness = {best_fitness}, Best Move = {best_move}')

    best_fitness = max(fitnesses)
    best_move = population[fitnesses.index(best_fitness)]
    return best_move, best_fitness'''

def simulate_game_with_evolution_and_alpha_beta(fen, total_time=120, pop_size=5, num_generations=3, mutation_rate=0.1):
    bitboards = parse_fen(reformulate(fen))
    player = 'b'
    start_time = time.time()

    while time.time() - start_time < total_time:
        if check_game_end(bitboards):
            break

        move_time = min(total_time - (time.time() - start_time), 1.0)
        best_move, _ = evolutionary_algorithm_with_alpha_beta(bitboards, player, pop_size, num_generations, mutation_rate, move_time)

        if not best_move:
            print("No valid move found", player, "Lost")
            break

        start_pos, end_pos = best_move

        bitboards = do_move(Pos(*start_pos), Pos(*end_pos), player, bitboards)
        print(f"{player.upper()} moved from {Pos(*start_pos).to_chess_notation()} to {Pos(*end_pos).to_chess_notation()}")
        bitboards.print_combined_board()

        player = 'b' if player == 'r' else 'r'

    print("Game Over")
    game_end_status = check_game_end(bitboards)
    if game_end_status:
        print(game_end_status)
    else:
        print("Time limit reached")
# Simulationsfunktion
'''def simulate_game_with_evolution_and_alpha_beta(fen, total_time=120, pop_size=5, num_generations=3, mutation_rate=0.1):
    bitboards = parse_fen(reformulate(fen))
    player = 'b'
    total_moves = 0
    start_time = time.time()

    while time.time() - start_time < total_time:
        if check_game_end(bitboards):
            break

        move_time = min(total_time - (time.time() - start_time), 1.0)
        best_move, _ = evolutionary_algorithm_with_alpha_beta(bitboards, player, pop_size, num_generations, mutation_rate, move_time, total_moves)

        if not best_move:
            print("No valid move found", player, "Lost")
            break

        start_pos, end_pos = best_move


        bitboards = do_move(Pos(*start_pos), Pos(*end_pos), player, bitboards)
        print(f"{player.upper()} moved from {Pos(*start_pos).to_chess_notation()} to {Pos(*end_pos).to_chess_notation()}")
        bitboards.print_combined_board()

        player = 'b' if player == 'r' else 'r'
        total_moves += 1

    print("Game Over")
    game_end_status = check_game_end(bitboards)
    if game_end_status:
        print(game_end_status)
    else:
        print("Time limit reached")
'''
# Beispiel der Nutzung der Simulationsfunktion
fen = "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0"
simulate_game_with_evolution_and_alpha_beta(fen)
