class Bitboards:
    def __init__(self):
        self.r = [[0 for _ in range(8)] for _ in range(8)]
        self.b = [[0 for _ in range(8)] for _ in range(8)]
        self.rb = [[0 for _ in range(8)] for _ in range(8)]
        self.br = [[0 for _ in range(8)] for _ in range(8)]
        self.bb = [[0 for _ in range(8)] for _ in range(8)]
        self.rr = [[0 for _ in range(8)] for _ in range(8)]

    def set_piece(self, piece_type, row, col):
        if piece_type == 'r':
            self.r[row][col] = 1
        elif piece_type == 'b':
            self.b[row][col] = 1
        elif piece_type == 'rb':
            self.rb[row][col] = 1
        elif piece_type == 'br':
            self.br[row][col] = 1
        elif piece_type == 'bb':
            self.bb[row][col] = 1
        elif piece_type == 'rr':
            self.rr[row][col] = 1

    def get_piece(self, row, col):
        if self.r[row][col] == 1:
            return 'r'
        elif self.b[row][col] == 1:
            return 'b'
        elif self.rb[row][col] == 1:
            return 'rb'
        elif self.br[row][col] == 1:
            return 'br'
        elif self.bb[row][col] == 1:
            return 'bb'
        elif self.rr[row][col] == 1:
            return 'rr'
        return None

    def print_board(self, board, name):
        print(f"{name}:")
        for row in reversed(board):  # Print rows from 7 to 0
            for piece in row:
                if piece == 1:
                    if name == "rr" or name == "r" or name == "br":
                        print("\x1b[31m1\x1b[0m", end=" ")  # Red color
                    elif name == "bb" or name == "b" or name == "rb":
                        print("\x1b[34m1\x1b[0m", end=" ")  # Blue color
                else:
                    print(piece, end=" ")
            print()
    def print_all_boards(self):
        self.print_board(self.r, "r")
        self.print_board(self.b, "b")
        self.print_board(self.rb, "rb")
        self.print_board(self.br, "br")
        self.print_board(self.bb, "bb")
        self.print_board(self.rr, "rr")

    def combine_boards(self):
        # Create a combined board that includes all pieces from all bitboards
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
        # Print the combined board with color-coded pieces
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
              # Print row number at the end of the row
        print("\x1b[95m{}\x1b[0m".format("  A B C D E F G H"))  # Pink color for column headers
   # Pink color for column headers
            #print()


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
        #i = row_num  # Map the FEN row to the board row, starting from the bottom
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



# Modify the print_all_boards method to print colored output
def print_all_boards(self):
    self.print_board(self.r, "\x1b[31mr\x1b[0m")
    self.print_board(self.b, "\x1b[34mb\x1b[0m")
    self.print_board(self.rb, "\x1b[34mrb\x1b[0m")
    self.print_board(self.br, "\x1b[31mbr\x1b[0m")
    self.print_board(self.bb, "\x1b[34mbb\x1b[0m")
    self.print_board(self.rr, "\x1b[31mrr\x1b[0m")

