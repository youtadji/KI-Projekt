import Bitboards
import unittest
import time

class TestCalculatePossibleMoves(unittest.TestCase):

    def to_chess_notation(pos):
        col_letters = 'ABCDEFGH'
        row_numbers = '12345678'

        col = col_letters[pos[1]]
        row = row_numbers[7 - pos[0]]  # Adjust for row numbering (1-8 from bottom to top)

        return f"{col}{row}"

    def move_to_chess_notation(self, move):
        start_pos, end_pos = move
        return f"{TestCalculatePossibleMoves.to_chess_notation(start_pos)}-{TestCalculatePossibleMoves.to_chess_notation(end_pos)}"

    def check_missing_and_extra_moves(self, fen, player, expected_best_moves, actual_moves):

        if isinstance(actual_moves, tuple):
            actual_moves = [actual_moves]
        actual_moves = [self.move_to_chess_notation(move) for move in actual_moves]

        expected_best_moves.sort()
        actual_moves.sort()

        # Check for discrepancies
        if expected_best_moves != actual_moves:
            missing_moves = set(expected_best_moves) - set(actual_moves)
            extra_moves = set(actual_moves) - set(expected_best_moves)
            print("Fen: ", fen, player)

            print("Missing moves:", missing_moves)
            print("Extra moves:", extra_moves)

        # Assert that expected and actual moves are the same
        self.assertListEqual(actual_moves, expected_best_moves, "Our best moves do not match best expected moves.")

    def test_possible_moves_Gruppe_T_Mid(self):
        case = {
            "fen": "1b0b0b02/8/3b04/3b04/r0r06/2b05/5r0r01/6",
            "description": "Gruppe T: Blau gewinnt in 2 Zügen",
            "player": 'b',
            "expected_best_moves": ["C6-C7"]
        }
        self.run_test_case(case)

    def test_possible_moves_Gruppe_T_Late(self):
        case = {
            "fen": "6/4bb3/8/8/4b0r0b01/8/8/6",
            "description": "Blau gewinnt in einem Zug durch Blocken",
            "player": 'b',
            "expected_best_moves": ["E2-F4"]
        }
        self.run_test_case(case)

    def test_possible_moves_Gruppe_AG(self):
        case = {
            "fen": "6/8/8/8/b0b02b0b0/2b05/2r0r0r0r02/6",
            "description": "Blau gewinnt in zwei Zügen",
            "player": 'b',
            "expected_best_moves": ["C6-D7"]
        }
        self.run_test_case(case)

    def test_possible_moves_Gruppe_AG_2(self):
        case = {
            "fen": "3b01b0/3bb1b02/8/8/8/2r0b0r02/8/0r04r0",
            "description": "Blau gewinnt in zwei Zügen",
            "player": 'b',
            "expected_best_moves": ["D6-D7"]
        }
        self.run_test_case(case)

    def test_possible_moves_Gruppe_J(self):
        case = {
            "fen": "6/1bb1b0bbb0b01/r02b04/2b01b0b02/2r02r02/1r02rrr02/6rr1/2r01r01",
            "description": "Rot gewinnt in zwei Zügen",
            "player": 'r',
            "expected_best_moves": ["A3-B2"]
        }
        self.run_test_case(case)

    def test_possible_moves_Gruppe_K(self):
        case = {
            "fen": "1bbb01b0b0/4b03/4r01b01/2b01r0b02/5r02/1r06/3r02r01/1rrr01r01",
            "description": "Rot gewinnt in zwei Zügen",
            "player": 'r',
            "expected_best_moves": ["E4-E3"]
        }
        self.run_test_case(case)

    def test_possible_moves_Gruppe_G(self):
        case = {
            "fen": "b02b01b0/4r03/1b02r03/1bb6/8/4r0b02/1r03r02/r01r02r0",
            "description": "Rot gewinnt in zwei Zügen",
            "player": 'r',
            "expected_best_moves": ["E3-E2"]
        }
        self.run_test_case(case)

    def test_possible_moves_Gruppe_X(self):
        case = {
            "fen": "4b0b0/2b0br4/3b04/2b0b01b02/8/4r03/1r03r02/r0r0r01r0r0",
            "description": "Rot gewinnt in 1 Zug",
            "player": 'r',
            "expected_best_moves": ["D2-B1", "D2-F1"]
        }
        self.run_test_case(case)

    def run_test_case(self, case):
        fen = case["fen"]
        player = case["player"]
        expected_best_moves = case["expected_best_moves"]

        bitboards = Bitboards.parse_fen(Bitboards.reformulate(fen))
        bitboards.print_combined_board()

        total_time = 0
        total_moves = 0
        pop_size = 5
        num_generations = 3
        mutation_rate = 0.1
        start_time = time.time()
        move_time = min(total_time - (time.time() - start_time), 1.0)
        
        best_moves, _ = Bitboards.evolutionary_algorithm_with_alpha_beta(bitboards, player,  pop_size, num_generations, mutation_rate, move_time, total_moves)

        self.check_missing_and_extra_moves(fen, player, expected_best_moves, best_moves)
