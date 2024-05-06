import unittest

def fen_to_board(fen):
    board = []
    for row in fen.split('/'):
        board_row = []
        for char in row:
            if char.isdigit():
                board_row.extend(['.'] * int(char))  # Leere Felder
            else:
                board_row.append(char)  # Steine
        board.append(board_row)
    return board

def print_board(board):
    for row in board:
        print(' '.join(row))

def is_move_legal(board, start, end):
    # Einfache Überprüfung: Ziel muss leer sein und Start muss einen Stein haben
    start_row, start_col = start
    end_row, end_col = end
    if board[start_row][start_col] in 'br' and board[end_row][end_col] == '.':
        return True
    return False

def make_move(board, start, end):
    if is_move_legal(board, start, end):
        start_row, start_col = start
        end_row, end_col = end
        board[end_row][end_col] = board[start_row][start_col]
        board[start_row][start_col] = '.'
    else:
        raise ValueError("Illegal move")

def pos_to_index(pos):
    column, row = pos[0], int(pos[1])
    return 8 - row, ord(column) - ord('A')

class TestGameMoves(unittest.TestCase):
    def setUp(self):
        fen = "6/1b06/1r03bb2/2r02b02/8/5r0r0/2r0r04/6"
        self.board = fen_to_board(fen)
        self.moves = [
            ("B3", "A3"), ("B3", "C3"), ("C4", "B4"), ("C4", "D4"),
            ("C4", "C3"), ("F6", "E6"), ("F6", "G6"), ("F6", "F5"),
            ("G6", "F6"), ("G6", "H6"), ("G6", "G5"), ("C7", "B7"),
            ("C7", "D7"), ("C7", "C6"), ("D7", "C7"), ("D7", "E7"),
            ("D7", "D6")
        ]

    def test_moves(self):
        for move in self.moves:
            start, end = pos_to_index(move[0]), pos_to_index(move[1])
            with self.subTest(move=move):
                self.assertTrue(is_move_legal(self.board, start, end))
                make_move(self.board, start, end)

if __name__ == "__main__":
    unittest.main()
