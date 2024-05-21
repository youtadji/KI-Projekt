from enum import Enum
import main
import board
import copy


   # Cell that can either be a Stack (containing a list of Player objects) or Empty
class Cell:
    def __init__(self, stack=None):
        if stack is None:
            self.stack = []
        else:
            self.stack = stack

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.stack == other.stack  # Compares the content of the stack
        return False

    def is_empty(self):
        return len(self.stack) == 0

    def __str__(self):
        if self.is_empty():
            return "Empty"
        else:
            return "Stack: " + ", ".join([player.value[0] for player in self.stack])


# Pos with col and row attributes
class Pos:
    def __init__(self, col, row):
        self.col = col
        self.row = row

    def __eq__(self, other):
        if isinstance(other, Pos):
            return self.col == other.col and self.row == other.row
        return False

    def __str__(self):
        return f"Pos({self.col}, {self.row})"



# several possible values representing directions
class Dir(Enum):
    NORTH = 'North'
    NORTHEAST = 'NorthEast'
    EAST = 'East'
    WEST = 'West'
    NORTHWEST = 'NorthWest'

    def __eq__(self, other):
        if isinstance(other, Dir):
            return self.value == other.value  # Compares the direction
        return False
def calculate_possible_moves_for_single_piece(board, pos, player):
    forbidden_positions = [(0, 0), (7, 7), (0, 7), (7, 0)]
    possible_moves = []

    # Movement directions for single pieces
    if player == main.Player.RED:
        movement_directions = [(1, 0), (-1, 0), (0, -1)]
        capture_directions = [(1, -1), (-1, -1)]
    else:
        movement_directions = [(-1, 0), (1, 0), (0, 1)]
        capture_directions = [(1, 1), (-1, 1)]

    # Initial positions for capture and movement
    initial_pos_capture = pos
    initial_pos_movement = pos

    # Check capture directions for single pieces
    for capture_dir in capture_directions:
        new_row = initial_pos_capture.row + capture_dir[1]
        new_col = initial_pos_capture.col + capture_dir[0]

        # Check if the new position is within the board boundaries and not forbidden
        if 0 <= new_row < 8 and 0 <= new_col < 8 and (new_col, new_row) not in forbidden_positions:
            new_cell = board[new_row][new_col]

            # Check if the new cell contains opponent's pieces
            if not new_cell.is_empty() and player != new_cell.stack[-1]:
                possible_moves.append(Pos(new_col, new_row))  # Add capture move
                  # Update initial position for capture

    # No capture moves, check regular movement moves
    for move_dir in movement_directions:
        new_row = initial_pos_movement.row + move_dir[1]
        new_col = initial_pos_movement.col + move_dir[0]

        # Check if the new position is within the board boundaries and not forbidden
        if 0 <= new_row < 8 and 0 <= new_col < 8 and (new_col, new_row) not in forbidden_positions:
            new_cell = board[new_row][new_col]

            # Check if the new cell is empty
            if new_cell.is_empty() or len(new_cell.stack) == 1 and not (player != new_cell.stack[-1]):
                possible_moves.append(Pos(new_col, new_row))  # Add movement move


    return possible_moves


def calculate_possible_moves(board, pos, player):
    forbidden_positions = [(0, 0), (7, 7), (0, 7), (7, 0)]
    possible_moves = []
    is_stack = len(board[pos.row][pos.col].stack) > 1

    if is_stack:
        if player == main.Player.RED:
            move_directions = [(-1, -2),(1, -2), (-2, -1), (2, -1)]
        else:
            move_directions = [(2, 1), (1, 2), (-2, 1), (-1, 2)]
        # Stack movements: knight-like moves in chess

    else:
        possible_moves = calculate_possible_moves_for_single_piece(board, pos, player)

    if not is_stack:
        return possible_moves


    initial_pos_movement = pos

    for move_dir in move_directions:
        new_row = initial_pos_movement.row + move_dir[1]
        new_col = initial_pos_movement.col + move_dir[0]

        # Check if the new position is within the board boundaries and not forbidden
        if 0 <= new_row < 8 and 0 <= new_col < 8 and (new_col, new_row) not in forbidden_positions:
            new_cell = board[new_row][new_col]

            # Check if the new cell is empty or has only one piece or has two pieces but the top one is oppenents one so it can eats it
            if new_cell.is_empty() or (len(new_cell.stack) == 1) or (len(new_cell.stack) == 2 and new_cell.stack[-1] != player):
                possible_moves.append(Pos(new_col, new_row))

    return possible_moves
def index_to_notation(col, row):
    # Converts zero-based index to board notation (A-H for columns, 1-8 for rows bottom to top)
    return f"{chr(65 + col)}{row + 1}"


def print_legal_moves_for_stack(board, position):
    def index_to_notation(col, row):
        # Converts zero-based index to board notation (A-H for columns, 1-8 for rows bottom to top)
        return f"{chr(65 + col)}{row + 1}"

    print("Position:", index_to_notation(position.col, position.row))
    print("Stack at position:", board[position.row][position.col].stack)

    player = board[position.row][position.col].stack[-1]  # Assuming the top of the stack defines the player's color


    # Retrieve legal moves from the existing function
    legal_moves = calculate_possible_moves(board, position, player)

    # Print the results
    print("Legal Moves from position", index_to_notation(position.col, position.row), ":")
    for move in legal_moves:
        print("Move to", index_to_notation(move.col, move.row))
    return legal_moves

#NEW YARA
def do_move(start_pos, end_pos, player, board):
    # Create a deep copy of the board
    updated_board = copy.deepcopy(board)

    # Retrieve the start and end cells from the copied board
    start_cell = updated_board[start_pos.row][start_pos.col]
    end_cell = updated_board[end_pos.row][end_pos.col]

    # Check if the end position is empty
    if end_cell.is_empty():
        end_cell.stack.append(player)

    else:
        # If end position has a stack with a top player other than the given player
        if end_cell.stack[-1] != player:
            # Remove the top player from the end stack
            end_cell.stack.pop()
            # Add the current player to the end stack
            end_cell.stack.append(player)
        # If the end stack has the same player on top
        elif end_cell.stack[-1] == player and len(end_cell.stack) == 1:
            # Add the current player to the top of the end stack
            end_cell.stack.append(player)
    # Remove the top player from the start cell
    start_cell.stack.pop()

    return updated_board



# NEW TRA MY
def check_game_end(fen):
    rows = fen.split('/')
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            if cell.isdigit():
                continue  # Skip empty spaces which are represented by digits
            elif 'b' in cell:  # Assuming 'b' represents the blue player
                if i == 7:  # Blue piece on the last row indicates game end
                    return "Game Over: Blue wins :D"
            elif 'r' in cell:  # Assuming 'r' represents the red player
                if i == 0:  # Red piece on the first row indicates game end
                    return "Game Over: Red wins :D"
    return None  # Game is not over yet

def get_possible_moves(fen, player, board):
    game_result = check_game_end(fen)

    if game_result:
        print(game_result)
        board2 = board
    else:
        board2 = board
    # print(board2)
    # If the game hasn't ended, continue with regular board setup and move calculation
    fen2 = main.reformulate(fen)
    board = main.visualize_board(fen2)  # This would be your function to create and setup the board

    '''board[4][0] = Cell([main.Player.RED])  # Now set a stack at position (0,0)
    print_legal_moves_for_stack(board, Pos(0, 4))'''

    # NEW YARAA
    player_positions = []
    updated_boards = []
    # NEW YARA
    # game_ends = []
    possible_moves = []

    player = player
    for row_index, row in enumerate(board):
        for col_index, cell in enumerate(row):
            if cell and not cell.is_empty() and cell.stack[-1] == player:
                # Add the position to the list
                player_positions.append(Pos(col_index, row_index))
    for start_position in player_positions:
        end_positions = calculate_possible_moves(board, start_position, player)
        for end_pos in end_positions:
            start = index_to_notation(start_position.col, start_position.row)
            end = index_to_notation(end_pos.col, end_pos.row)
            # print(start, end)
            move = main.Move(start, end)

            possible_moves.append(str(move))

    # Return the list of possible moves
    return possible_moves
fen = "bb1b0b0b0b0/b01b0b0b01b01/8/3b04/3r04/2r05/1rr2r0r01r0/1r0r0r0r0r0"
p = get_possible_moves(fen, main.Player.BLUE, board.create_board(fen))
print(p)

