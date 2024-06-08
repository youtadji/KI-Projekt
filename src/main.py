from enum import Enum

import mem
import copy
import board

# Player can have any of two values (Red or Blue)
from enum import Enum

# Player can have any of two values (Red or Blue)
class Player(Enum):
    RED = 'red'
    BLUE = 'blue'

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.value == other.value
        return False

    def __str__(self):
        return self.value[0]

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
        # Convert col (numeric) to letters (A=1, B=2, etc.)
        #col_letter = chr(64 + self.col)  # 'A' is ASCII 65
        return f"{chr(65 + self.col)}{self.row + 1}"


# Class representing a move with start and end positions
class Move:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.start == other.start and self.end == other.end
        return False

    def __str__(self):
        # Represent the move in the format "B1-B2"
        return f"{self.start}-{self.end}"


def parseRow(row_str, row_index):
    row = []
    col = 0
    if row_index == 0 or row_index == 7:  # For the first and last row
        max_columns = 6  # Exclude columns 'a' and 'h'
    else:
        max_columns = 8  # Include all columns

    # Check if row_str is not empty
    if row_str:
        while col < len(row_str):
            char = row_str[col]
            if char.isdigit():
                # If a digit is encountered, it represents the number of consecutive empty cells
                num_empty_cells = int(char)
                row.extend([Cell() for _ in range(num_empty_cells)])  # Create new instances
                #row.extend([Cell()] * num_empty_cells) #use the str
                col += 1  # Move to the next character
            else:
                # Determine the player color
                player = Player.RED if char.lower() == 'r' else Player.BLUE

                # Check if the character is followed by a '0'
                if col + 1 < len(row_str) and row_str[col + 1] == '0':
                    # Add a stack with only red or blue without anything on top
                    row.append(Cell([player]))
                    col += 2  # Skip the '0'
                else:
                    # Check if the current character should be appended to the previous stack
                    if (row and row[-1] and isinstance(row[-1], Cell) and hasattr(row[-1], 'stack') and
                            row[-1].stack and not isinstance(row[-1].stack[-1], int) and len(row[-1].stack) < 2) and (row_str[col - 1] != '0'):
                        row[-1].stack.append(player)
                    else:
                        # Otherwise, start a new stack
                        row.append(Cell([player]))
                    col += 1

        # Add remaining empty cells if necessary
        if len(row) < max_columns:
            row.extend([Cell()] * (max_columns - len(row)))

    return row

def visualize_board(fen):
    board = []
    #order_board = []
    rows = fen.split("/")
    for i, row_str in enumerate(rows):
        row = parseRow(row_str, i)
        board.append(row) #iterate over the cells in the row and add the string of the cell to the board

    return board
#r0r0rr4b0
def reformulate(fen):
    # Split the FEN string into rows
    rows = fen.split("/")

    # Add "1" to the beginning and end of row 0
    rows[0] = "1" + rows[0] + "1"

    # Add "2" to the beginning and end of row 7
    rows[7] = "1" + rows[7] + "1"

    # Join the rows back together with "/"
    new_fen = "/".join(rows)

    return new_fen

# Function to convert a board into an FEN (Forsyth-Edwards Notation) string
def board_to_fen(board):
    fen_rows = []  # List to hold FEN strings for each row

    # Loop through each row in the board
    for row in board:
        fen_row = ""  # String to build the FEN representation of the row
        empty_count = 0  # Counter for consecutive empty cells

        # Loop through each cell in the row
        for cell in row:
            if not cell.stack:
                # If the cell is empty, increment the empty count
                empty_count += 1
            else:
                # If there are empty cells, add the count to the FEN row
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0  # Reset the empty count

                # Get the FEN representation for the stack in the cell
                stack_fen = "".join(
                    ['r' if player == Player.RED else 'b' for player in cell.stack]
                )

                # If the stack has only one piece, append '0' to indicate a single item
                if len(cell.stack) == 1:
                    stack_fen += "0"

                # Add the stack representation to the FEN row
                fen_row += stack_fen

        # If there are trailing empty cells, add their count to the FEN row
        if empty_count > 0:
            fen_row += str(empty_count)

        # Add the FEN row to the list
        fen_rows.append(fen_row)

    # Join all rows with '/' to get the full FEN representation
    return "/".join(fen_rows)


# Function to remove the first and last cells from the first and last rows
def trim_corners(board):
    #make a deep copy to avoid trimming the original board
    copied_board = copy.deepcopy(board)

    # Remove the first and last cell from the first row
    copied_board[0] = copied_board[0][1:-1]

    # Remove the first and last cell from the last row
    copied_board[-1] = copied_board[-1][1:-1]

    return copied_board  # Return the modified board
def undo_move(start_pos, end_pos, player, updated_board, board):
    # Create a deep copy of the board to work with
    board_copy = copy.deepcopy(updated_board)

    # Retrieve the start and end cells from the copied board
    start_cell = board_copy[start_pos.row][start_pos.col]
    end_cell_not_updated = board[end_pos.row][end_pos.col]
    end_cell = board_copy[end_pos.row][end_pos.col]

    if (not end_cell_not_updated.is_empty() and end_cell_not_updated.stack[-1] != player):
        # Move the player back to the start position
        start_cell.stack.append(player)
        end_cell.stack.pop()
        end_cell.stack.append(Player.RED if player == Player.BLUE else Player.BLUE)

    else:
        start_cell.stack.append(player)
        # Remove the player from the end position
        if end_cell.stack[-1] == player:
            end_cell.stack.pop()


    # If the end cell stack had an opponent piece originally, restore it
    # if len(end_cell.stack) == 0:
    # This indicates the end cell was initially empty and got captured
    # end_cell.stack.append(main.Player.RED if player == main.Player.BLUE else main.Player.BLUE)

    return board_copy
def main():
    # Example FEN string
    #fen = "2rr2br/2rr2br1b0/b07/b03rrr2r0/b05rbb1/8/8/r0r0r0r0r0r0"
    #print("fen",fen)
    #reformulated= reformulate(fen)
    #print("reformulated",reformulated)
    # Visualize the board
    '''visualize_board(reformulated)
    board.create_board(fen)'''


if __name__ == "__main__":
    main()
