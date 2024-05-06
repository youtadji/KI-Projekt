from enum import Enum


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


# Initialize an 8x8 board with None in the corner cells
def create_board():
    # Start with a list comprehension to generate an 8x8 grid
    board = [[Cell() for _ in range(8)] for _ in range(8)]

    # Set corner cells to None to indicate their absence
    board[0][0] = None  # Top-left corner
    board[0][7] = None  # Top-right corner
    board[7][0] = None  # Bottom-left corner
    board[7][7] = None  # Bottom-right corner

    return board


# Class representing a move with start and end positions
class Move:
    def _init_(self, start, end):
        self.start = start
        self.end = end

    def _eq_(self, other):
        if isinstance(other, Move):
            return self.start == other.start and self.end == other.end
        return False

    def _str_(self):
        return f"Move from {self.start} to {self.end}"


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
                row.extend([Cell()] * num_empty_cells) #use the str
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
                    # Check if the current character should be appended to the previous stack and that the one before i not 0
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
    rows = fen.split("/")
    for i, row_str in enumerate(rows):
        row = parseRow(row_str, i)
        board.append(row) #iterate over the cells in the row and add the string of the cell to the board

    for row in board:
        print(" | ".join(str(cell) for cell in row))



    return board

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

def main():
    # Example FEN string
    fen = "6/8/6b01/4bb3/r0r0rr4b0/3b02r01/1rr3r2/6"
    print("fen : " +fen)
    reformulated = reformulate(fen)
    print("reformulated : " +reformulated)
    # Visualize the board
    visualize_board(reformulated)


if __name__ == "__main__":
    main()