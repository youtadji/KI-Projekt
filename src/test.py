import unittest
import main
import board
import zuggenerator


class TestCalculatePossibleMoves(unittest.TestCase):

    def check_missing_and_extra_moves(self, expected_moves, actual_moves):
        # Sort the moves for comparison
        expected_moves.sort()
        actual_moves.sort()

        # Check for discrepancies
        if expected_moves != actual_moves:
            missing_moves = set(expected_moves) - set(actual_moves)
            extra_moves = set(actual_moves) - set(expected_moves)

            print("Missing moves:", missing_moves)
            print("Extra moves:", extra_moves)

        # Assert that expected and actual moves are the same
        self.assertListEqual(actual_moves, expected_moves, "Possible moves do not match expected moves.")

    def test_possible_moves_Gruppe_MTY_Mid_Game(self):
        case = {
            "fen": "b02b01b0/3b01b02/b02b02b01/b01b05/5r02/1r02r02r0/2rrr02r01/r03r01",
            "description": "Gruppe MTY (Gruppe AF): Mid-Game mit einem Turm",
            "player": main.Player.BLUE,
            "expected_moves": [
                "B1-B2", "B1-C1", "E1-E2", "E1-D1", "E1-F1", "G1-G2", "G1-F1",
                "D2-D3", "D2-C2", "D2-E2", "F2-F3", "F2-E2", "F2-G2", "A3-A4",
                "A3-B3", "D3-D4", "D3-C3", "D3-E3", "G3-G4", "G3-F3", "G3-H3",
                "A4-A5", "A4-B4", "C4-C5", "C4-B4", "C4-D4"
            ]
        }
        self.run_test_case(case)

    # Add more test methods for each test case...

    def test_possible_moves_case_one_prof(self):
        case = {
            "fen": "6/1b06/2bb1b0b02/6bb1/1r0br5/3r0rr3/8/4r0r0",
            "description": "Stellungsbeschreibung: Endspiel",
            "player": main.Player.BLUE,
            "expected_moves": [
                "B2-A2", "B2-C2", "B2-B3", "C3-A4", "C3-E4", "C3-B5", "C3-D5",
                "E3-D3", "E3-F3", "E3-E4", "F3-E3", "F3-G3", "F3-F4", "G4-E5",
                "G4-F6", "G4-H6"
            ]
        }
        self.run_test_case(case)

    def test_possible_moves_case_two_prof(self):
        case = {
            "fen": "6/8/6b01/4bb3/r0r0rr4b0/3b02r01/1rr3r2/6",
            "description": "Stellungsbeschreibung: Endspiel",
            "player": main.Player.RED,
            "expected_moves": [
                "A5-B5", "A5-A4", "B5-A5", "B5-B4", "C5-E4", "C5-A4", "C5-D3",
                "C5-B3", "G6-F6", "G6-H6", "G6-H5", "G6-G5", "B7-D6", "B7-A5",
                "F7-E7", "F7-G7", "F7-F6"
            ]
        }
        self.run_test_case(case)

    def test_possible_moves_Mögliches_early_Game_jumpstreet(self):
        case = {
            "fen": "bb1b0b0b0b0/b01b0b0b01b01/8/3b04/3r04/2r05/1rr2r0r01r0/1r0r0r0r0r0",
            "description": "Mögliches early Game jumpstreet",
            "player": main.Player.RED,
            "expected_moves": ["D5-E5", "D5-C5", "D5-D4", "C6-D6", "C6-B6", "C6-C5", "B7-A5", "B7-C5", "B7-D6", "E7-F7",
                               "E7-D7", "E7-E6", "F7-G7", "F7-E7", "F7-F6", "H7-G7", "H7-H6", "C8-D8", "C8-B8",
                               "C8-C7", "D8-E8", "D8-C8", "D8-D7", "E8-F8", "E8-D8", "E8-E7", "F8-G8", "F8-E8",
                               "F8-F7", "G8-F8", "G8-G7"]
        }
        self.run_test_case(case)

    def test_possible_moves_Midgame_random_group(self):
        case = {
            "fen": "2bbbb1b0/1b06/1b01b04/4b03/4r03/3r02b01/1r0r02rr2/2rr2r0",
            "description": "Midgame random group",
            "player": main.Player.RED,
            "expected_moves": ["E5-F5", "E5-D5", "E5-E4", "D6-E6", "D6-C6", "D6-D5", "B7-C7", "B7-A7", "B7-B6",
                               "C7-D7", "C7-B7", "C7-C6", "F7-E5", "F7-G5", "F7-D6", "F7-H6", "D8-C6", "D8-E6",
                               "D8-B7", "G8-F8", "G8-G7"]
        }
        self.run_test_case(case)

    def test_possible_moves_End_Game_jumpstreet(self):
        case = {
            "fen": "1b04/2b03b01/b01rr5/r02b01b02/1b06/1r02b03/8/1r01r0r0r0",
            "description": "End Game jumpstreet",
            "player": main.Player.BLUE,
            "expected_moves": ["C1-B1", "C1-D1", "C1-C2", "C2-B2", "C2-D2", "G2-F2", "G2-H2", "G2-G3", "A3-B3",
                               "A3-A4", "D4-C4", "D4-E4", "D4-D5", "F4-E4", "F4-G4", "F4-F5", "B5-A5", "B5-C5",
                               "B5-B6", "E6-D6", "E6-F6", "E6-E7"]
        }
        self.run_test_case(case)

    def run_test_case(self, case):
        fen = case["fen"]
        player = case["player"]
        expected_moves = case["expected_moves"]

        # Create the board from FEN
        game_board = board.create_board(fen)

        # Get the possible moves
        actual_moves = zuggenerator.get_possible_moves(fen, player, game_board)

        # Check for discrepancies and validate
        self.check_missing_and_extra_moves(expected_moves, actual_moves)


if __name__ == '__main__':
    unittest.main()
