from enum import Enum
import main

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
        capture_directions = [(-1, 1), (-1, 1)]

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
            if new_cell.is_empty() or len(new_cell.stack) == 1:
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


1


# Example usage:
#board(row)(col)
#pos(col)(row)

fen = "6/1bb1b02b01/4rb3/2r05/3r01b02/b03r0r02/2rr1r03/6"
fen2 = main.reformulate(fen)
board = main.visualize_board(fen2)  # This would be your function to create and setup the board
print("eyaaaa",board[5][4])
# Now print the legal moves for the stack at (0,0)
print_legal_moves_for_stack(board, Pos(4, 5))