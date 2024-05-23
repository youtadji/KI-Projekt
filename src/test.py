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
            "expected_moves": ["D5-E5", "D5-C5", "C6-D6", "C6-B6", "C6-C5", "B7-A5", "B7-C5", "B7-D6", "E7-F7",
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
            "expected_moves": ["E5-F5", "E5-D5", "D6-E6", "D6-C6", "D6-D5", "B7-C7", "B7-A7", "B7-B6",
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
                                "D4-C4", "D4-E4", "D4-D5", "F4-E4", "F4-G4", "F4-F5", "B5-A5", "B5-C5",
                                "E6-D6", "E6-F6", "E6-E7"]
        }

        self.run_test_case(case)

    # --------------------------------------------------------------------------------------------
    # Tests aus Isis
    def test_gruppe_a_late_game(self):
        case = {
            "fen": "6/1b06/1r03bb2/2r02b02/8/5r0r0/2r0r04/6",
            "description": "Late Game",
            "player": main.Player.RED,
            "expected_moves": [ "B3-A3", "B3-C3", "C4-B4", "C4-D4", "C4-C3", "F6-E6", "F6-G6", "F6-F5", "G6-F6", "G6-H6",
                              "G6-G5", "C7-B7", "C7-D7", "C7-C6", "D7-C7", "D7-E7", "D7-D6"]
        }

        self.run_test_case(case)

    def test_gruppe_a_mid_game(self):
        case = {
            "fen": "6/1b0b0b0b0b0b01/1b0b0b0b0b0b01/8/8/1r0r0r0r0r0r01/1r0r0r0r0r0r01/6",
            "description": "Mid Game",
            "player": main.Player.BLUE,
            "expected_moves": ["B2-C2", "B2-A2", "B2-B3", "C2-D2", "C2-B2", "C2-C3", "D2-E2", "D2-C2", "D2-D3", "E2-F2",
                               "E2-D2", "E2-E3", "F2-G2", "F2-E2", "F2-F3", "G2-H2", "G2-F2", "G2-G3", "B3-C3", "B3-A3",
                               "B3-B4", "C3-D3", "C3-B3", "C3-C4", "D3-E3", "D3-C3", "D3-D4", "E3-F3", "E3-D3", "E3-E4",
                               "F3-G3", "F3-E3", "F3-F4", "G3-H3", "G3-F3", "G3-G4"]
        }

        self.run_test_case(case)

    def test_gruppe_o_early_game(self):
        case = {
            "fen": "b0b01b0b0b0/1b0b02b0b01/3b0b03/2b05/3r04/2r05/1r01rr1r0r01/r0r02r0r0",
            "description": "Early Game",
            "player": main.Player.BLUE,
            "expected_moves": ["B1-B2", "B1-C1", "C1-B1", "C1-C2", "C1-D1", "E1-D1", "E1-E2", "E1-F1", "F1-E1", "F1-F2",
                              "F1-G1", "G1-F1", "G1-G2", "B2-A2", "B2-B3", "B2-C2", "C2-B2", "C2-C3", "C2-D2", "D3-C3",
                              "D3-D4", "D3-E3", "E3-D3", "E3-E4", "E3-F3", "F2-E2", "F2-F3", "F2-G2", "G2-F2", "G2-G3",
                              "G2-H2", "C4-B4", "C4-C5", "C4-D5", "C4-D4"]
        }

        self.run_test_case(case)

    def test_gruppe_o_end_game(self):
        case = {
            "fen": "6/2bb1b03/4b0b02/3b01r02/2b05/8/1rr1r02r01/6",
            "description": "End Game",
            "player": main.Player.RED,
            "expected_moves": ['B7-A5', 'B7-C5', 'B7-D6', 'D7-C7', 'D7-D6', 'D7-E7', 'F4-E3', 'F4-E4', 'F4-G4', 'G7-F7',
                              'G7-G6', 'G7-H7']
        }

        self.run_test_case(case)

    def test_gruppe_i_early_game(self):
        case = {
            "fen": "b0b01b01b0/2b0bbb0bb1b0/8/1b06/5r02/2r05/1r01r0rr1r01/r0r0r02rr",
            "description": "Early Game",
            "player": main.Player.BLUE,
            "expected_moves": ["B1-B2", "B1-C1", "C1-B1", "C1-C2", "C1-D1", "E1-D1", "E1-E2", "E1-F1", "G1-F1", "G1-G2",
                              "C2-B2", "C2-C3", "D2-B3", "D2-C4", "D2-E4", "D2-F3", "E2-E3", "F2-D3", "F2-E4", "F2-G4",
                              "F2-H3", "H2-G2", "H2-H3", "B4-A4", "B4-B5", "B4-C4"]
        }

        self.run_test_case(case)

    def test_gruppe_i_end_game(self):
        case = {
            "fen": "1b01b02/2b01b01b0b0/2r02b02/4r03/2b02b02/b07/3r02r01/rr4rr",
            "description": "End Game",
            "player": main.Player.BLUE,
            "expected_moves": ["C1-B1", "C1-C2", "C1-D1", "E1-D1", "E1-E2", "E1-F1", "C2-B2", "C2-D2", "E2-D2", "E2-E3",
                               "E2-F2", "G2-F2", "G2-G3", "G2-H2", "H2-G2", "H2-H3", "F3-E3", "F3-E4", "F3-F4", "F3-G3",
                               "C5-B5", "C5-C6", "C5-D5", "F5-E5", "F5-F6", "F5-G5", "A6-A7", "A6-B6"]
        }

        self.run_test_case(case)

    def test_gruppe_al_opening_strategy(self):
        case = {
            "fen": "6/1bbbbbbbbbbbb1/8/8/8/1r0r0r0r0r0r01/8/r0r0r0r0r0r0",
            "description": "Start Game",
            "player": main.Player.BLUE,
            "expected_moves": ["B2-A4", "B2-C4", "B2-D3", "C2-B4", "C2-D4", "C2-A3", "C2-E3", "D2-C4", "D2-E4",
                               "D2-B3", "D2-F3", "E2-D4", "E2-F4", "E2-C3", "E2-G3", "F2-E4", "F2-G4", "F2-D3",
                               "F2-H3", "G2-F4", "G2-H4", "G2-E3"]
        }

        self.run_test_case(case)

    def test_gruppe_al_end_game(self):
        case = {
            "fen": "8/2b02b02/2r02r02/8/8/2b02b02/2r02r02/8",
            "description": "End Game",
            "player": main.Player.BLUE,
            "expected_moves": ["C6-B6", "C6-D6", "F6-E6", "F6-G6", "C2-B2", "C2-D2", "F2-E2", "F2-G2"]
        }

        self.run_test_case(case)

    def test_gruppe_x_end_position(self):
        case = {
            "fen": "1b03b0/3b01b02/8/4b0r02/4b03/4r0b02/3r01r02/1r01r01r0",
            "description": "End Game",
            "player": main.Player.BLUE,
            "expected_moves": ["C1-B1", "C1-D1", "C1-C2", "G1-F1", "G1-G2", "F2-G2", "D2-D3", "D2-E2", "F2-E2", "F2-F3",
                               "E4-D4", "F6-G6", "E4-E5", "E5-F5", "D2-C2", "E5-D5"]
        }

        self.run_test_case(case)


    def test_gruppe_x_early_game(self):
        case = {
                "fen": "b0b0b0b0b0b0/2b01b0b02/1b01b04/4r03/2b01r03/6r01/1r0r0r01r02/r0r0r0r01r0",
                "description": "Early Game",
                "player": main.Player.RED,
                "expected_moves": ["E4-E3", "E5-E4", "G6-G5", "F7-F6", "D7-D6", "C7-C6", "B7-B6", "G8-G7", "E8-E7", "D8-D7",
                              "C8-C7", "B8-B7", "E4-F4", "E5-F5", "G6-H6", "F7-G7", "D7-E7", "C7-D7", "B7-C7", "E8-F8",
                              "D8-E8", "C8-D8", "B8-C8", "E4-D4", "E5-D5", "G6-F6", "F7-E7", "D7-C7", "C7-B7", "B7-A7",
                              "G8-F8", "E8-D8", "D8-C8", "C8-B8", "E4-D3"]
            }

        self.run_test_case(case)

    def test_gruppe_e_early_game(self):
        case = {
                "fen": "1b0b0b0b01/1b0b0b0b0b0b01/8/4r0b02/2b05/3r04/1r0rr1r0r0r01/r01r0r01r0",
                "description": "Early Game",
                "player": main.Player.BLUE,
                "expected_moves": ["C1-B1", "C1-C2", "C1-D1", "D1-C1", "D1-D2", "D1-E1", "E1-D1", "E1-E2", "E1-F1", "F1-E1",
                              "F1-F2", "F1-G1", "B2-A2", "B2-B3", "B2-C2", "C2-B2", "C2-C3", "C2-D2", "D2-C2", "D2-D3",
                              "D2-E2", "E2-D2", "E2-E3", "E2-F2", "F2-E2", "F2-F3", "F2-G2", "G2-F2", "G2-G3", "G2-H2",
                              "F4-F5", "F4-G4", "C5-B5", "C5-C6", "C5-D6", "C5-D5"]
            }

        self.run_test_case(case)

    def test_gruppe_e_end_game(self):
        case = {
                "fen": "3b02/1b0b03r01/5b02/8/1b0bb3r01/1r06/2r05/3r02",
                "description": "Early Game",
                "player": main.Player.RED,
                "expected_moves": ["B6-A6", "B6-C6", "C7-B7", "C7-C6", "C7-D7", "E8-D8", "E8-E7", "E8-F8", "G2-F2", "G2-G1",
                               "G2-H2", "G5-F5", "G5-G4", "G5-H5", "B6-C5"]
            }

        self.run_test_case(case)

    def test_gruppe_m_endgame_with_edge_cases(self):
        case = {
                "fen": "6/1b06/8/2b01bbb0rb1/1rbr0rr1r0r01/8/b07/6",
                "description": "End Game",
                "player": main.Player.BLUE,
                "expected_moves": ["B2-A2", "B2-B3", "B2-C2", "C4-B4", "C4-D4", "C4-D5", "E4-C5", "E4-D6", "E4-F6", "E4-G5",
                               "F4-G5", "G4-E5", "G4-F6", "G4-H6", "B5-A7", "B5-C7", "B5-D6", "A7-B7"]
            }

        self.run_test_case(case)

    def test_gruppe_l_example_position(self):
        case = {
                "fen": "3b02/2bb2b02/5b0bb1/2r0b04/2rb3b01/1rr1rr2r0r0/5r02/2rr3",
                "description": "ExampleGame",
                "player": main.Player.BLUE,
                "expected_moves": ["C2-A3", "C2-B4", "C2-D4", "C2-E3", "C5-A6", "C5-B7", "C5-D7", "C5-E6", "D4-D5", "D4-E4",
                              "E1-D1", "E1-E2", "E1-F1", "F2-E2", "F2-F3", "F2-G2", "F3-E3", "F3-F4", "G3-E4", "G3-F5",
                              "G3-H5", "G5-F5", "G5-H5", "G5-H6"]
            }

        self.run_test_case(case)

    def test_gruppe_l_early_to_mid_game(self):
        case = {
                "fen": "1b01b0b01/b01bb0b01bb0b01/1b06/8/7b0/1r02r01rr1/2rr2rr2/r0r01r0r01",
                "description": "Mid Game",
                "player": main.Player.BLUE,
                "expected_moves": ["A2-A3", "A2-B2", "B3-A3", "B3-B4", "B3-C3", "C1-B1", "C1-D1", "C2-A3", "C2-B4", "C2-D4",
                               "C2-E3", "D2-D3", "D2-E2", "E1-D1", "E1-E2", "E1-F1", "F1-E1", "F1-G1", "F2-D3", "F2-E4",
                               "F2-G4", "F2-H3", "G2-G3", "G2-H2", "H5-G5", "H5-G6", "H5-H6"]
            }

        self.run_test_case(case)

    def test_gruppe_mty_mid_game(self):
        case = {
                "fen": "b02b01b0/3b01b02/b02b02b01/b01b05/5r02/1r02r02r0/2rrr02r01/r03r01",
                "description": "Mid Game",
                "player": main.Player.BLUE,
                "expected_moves": ["B1-B2", "B1-C1", "E1-E2", "E1-D1", "E1-F1", "G1-G2", "G1-F1", "D2-D3", "D2-C2", "D2-E2",
                               "F2-F3", "F2-E2", "F2-G2", "A3-A4", "A3-B3", "D3-D4", "D3-C3", "D3-E3", "G3-G4", "G3-F3",
                               "G3-H3", "A4-A5", "A4-B4", "C4-C5", "C4-B4", "C4-D4"]
            }

        self.run_test_case(case)

    def test_gruppe_mty_end_game(self):
        case = {
            "fen": "6/1b03b02/3b01r0b01/bb2b04/1b01r02r0r0/1r0r02rbr01/1r06/6",
            "description": "End Game",
            "player": main.Player.RED,
            "expected_moves": ["F3-E3", "D5-C5", "D5-E5", "G5-G4", "G5-F5", "G5-H5", "H5-H4", "H5-G5", "B6-A6", "B6-C6",
                              "C6-C5", "C6-B6", "C6-B5", "C6-D6", "G6-G5", "G6-H6", "B7-B6", "B7-A7", "B7-C7"]
        }

        self.run_test_case(case)

    def test_gruppe_rusty_ai_end_game(self):
        case = {
            "fen": "2b03/8/8/3b0b03/2b03b01/2r03r01/2r05/6",
            "description": "End Game",
            "player": main.Player.RED,
            "expected_moves": ["C6-B6", "C6-D6", "C7-B7", "C7-C6", "C7-D7", "G6-F6", "G6-H6"]
        }

        self.run_test_case(case)

    def test_gruppe_rusty_ai_mid_game(self):
        case = {
            "fen": "2bbbb1b0/1b06/1b01b04/4b03/4r03/3r02b01/1r0r02rr2/2rr2r0",
            "description": "Mid Game",
            "player": main.Player.BLUE,
            "expected_moves": ["B2-A2", "B2-B3", "B2-C2", "B3-A3", "B3-B4", "B3-C3", "D1-B2", "D1-C3", "D1-E3", "D1-F2",
                               "D3-C3", "D3-D4", "D3-E3", "E1-C2", "E1-D3", "E1-F3", "E1-G2", "E4-D4", "E4-F4", "G1-F1",
                               "G1-G2", "G6-F6", "G6-F7", "G6-G7", "G6-H6"]
        }

        self.run_test_case(case)

    def test_gruppe_aj_early_game(self):
        case = {
            "fen": "b0b01b02/3bbb0bb2/2b03bb1/8/2b01r03/5r02/1rr1r0rr1rr1/1rr4",
            "description": "Early Game",
            "player": main.Player.BLUE,
            "expected_moves": ["B1-B2", "B1-C1", "C1-B1", "C1-C2", "C1-D1", "E1-D1", "E1-E2", "E1-F1", "D2-B3", "D2-C4",
                               "D2-E4", "D2-F3", "E2-E3", "F2-D3", "F2-E4", "F2-G4", "F2-H3", "C3-B3", "C3-C4", "C3-D3",
                               "G3-E4", "G3-F5", "G3-H5", "C5-B5", "C5-C6", "C5-D5"]
        }

        self.run_test_case(case)

    def test_gruppe_aj_end_game(self):
        case = {
            "fen": "6/1b02br3/6bb1/2b0b04/2r04r0/8/1rr1r0rr1r01/6",
            "description": "End Game",
            "player": main.Player.BLUE,
            "expected_moves": ["B2-A2", "B2-B3", "B2-C2", "G3-E4", "G3-F5", "G3-H5", "C4-B4", "C4-D4", "D4-C4", "D4-C5",
                               "D4-D5", "D4-E4"]
        }

        self.run_test_case(case)

    def test_gruppe_ac_5th_move(self):
        case = {
            "fen": "2bbb0b0b0/1bbb0b0b0b0b01/8/8/8/1r01r04/2r01r0r0r01/r0r0r0r0r0r0",
            "description": "5th move",
            "player": main.Player.BLUE,
            "expected_moves": ["C2-C3", "D2-D3", "E2-E3", "F2-F3", "G2-G3", "G2-H2", "F1-E1", "G1-F1", "D2-C2", "E2-D2",
                               "F2-E2", "G2-F2", "E1-E2", "F1-F2", "G1-G2", "E1-F1", "F1-G1", "C2-D2", "D2-E2", "E2-F2",
                               "F2-G2", "D1-C3", "B2-A4", "D1-E3", "B2-C4", "B2-D3", "D1-F2"]
        }

        self.run_test_case(case)

    def test_gruppe_ac_mid_game(self):
        case = {
            "fen": "bb5/1bb6/bb6b0/b0r0rb5/7rb/5rr2/8/6",
            "description": "Mid Game",
            "player": main.Player.BLUE,
            "expected_moves": ["H3-G3", "H3-H4", "A4-A5", "C4-A5", "C4-B6", "H5-G7", "B1-C3", "A3-B5", "C4-D6", "B1-D2",
                              "B2-D3", "C4-E5", "H5-F6", "B2-A4"]
        }

        self.run_test_case(case)

    def test_gruppe_ab_endgame(self):
        case = {
            "fen": "1b0b0b0b0b0/1b01bb2b01/8/3bb1b02/5rr2/2r01r03/2rr5/r0r0r0r0r0r0",
            "description": "End Game",
            "player": main.Player.BLUE,
            "expected_moves": ["C1-B1", "C1-C2", "C1-D1", "D1-C1", "D1-E1", "E1-D1", "E1-E2", "E1-F1", "F1-E1", "F1-F2",
                               "F1-G1", "G1-F1", "G1-G2", "B2-A2", "B2-B3", "B2-C2", "D2-B3", "D2-C4", "D2-E4", "D2-F3",
                               "G2-F2", "G2-G3", "G2-H2", "D4-B5", "D4-C6", "D4-E6", "D4-F5", "F4-E4", "F4-G4"]
        }

        self.run_test_case(case)

    def test_gruppe_ab_before_last_move(self):
        case = {
            "fen": "b0b0b01b01/2b03b01/8/3b01b02/1b01r01r02/2br1r03/b01r02r02/2r0r0r01",
            "description": "End Game",
            "player": main.Player.RED,
            "expected_moves": ["F8-G8", "F8-F7", "F8-E8", "E8-F8", "E8-E7", "E8-D8", "D8-E8", "D8-D7", "D8-C8", "F7-G7",
                              "F7-F6", "F7-E7", "C7-D7", "C7-B7", "E6-F6", "E6-E5", "E6-D6", "C6-E5", "C6-D4", "C6-B4",
                              "C6-A5", "F5-G5", "F5-E5", "D5-E5", "D5-C5"]
        }

        self.run_test_case(case)

    def test_gruppe_g_earlygame(self):
        case = {
            "fen": "b01b0b0b0b0/1b0b01b01b01/3b01b02/2b05/8/2r0r01rr2/1r04r01/r0r0r0r0r0r0",
            "description": "Early Game",
            "player": main.Player.RED,
            "expected_moves": ["B8-B7", "B8-C8", "C8-B8", "C8-C7", "C8-D8", "D8-C8", "D8-D7", "D8-E8", "E8-D8", "E8-E7",
                               "E8-F8", "F8-E8", "F8-F7", "F8-G8", "G8-F8", "G8-G7", "B7-A7", "B7-B6", "B7-C7", "C6-B6",
                               "C6-C5", "C6-D6", "D6-C6", "D6-D5", "D6-E6", "G7-F7", "G7-G6", "G7-H7", "F6-D5",
                               "F6-E4", "F6-G4", "F6-H5"]
        }

        self.run_test_case(case)

    def test_gruppe_g_late_game(self):
        case = {
            "fen": "b01b01b01/8/2b03b01/1b06/1r01b01b02/3r04/2r03r01/4r01",
            "description": "Late Game",
            "player": main.Player.RED,
            "expected_moves": ["F8-E8", "F8-F7", "F8-G8", "C7-B7", "C7-C6", "C7-D7", "G7-F7", "G7-G6", "G7-H7", "D6-C6",
                              "D6-E6", "B5-A5", "B5-C5"]
        }

        self.run_test_case(case)

    def test_gruppe_ad_middlegame(self):
        case = {
            "fen": "b0b0b01bb1/2b0b0bbb02/5r02/3b04/4r0b02/8/2rrr01r02/r0r0r0r01r0",
            "description": "Middle Game",
            "player": main.Player.RED,
            "expected_moves": ["B8-B7", "B8-C8", "C8-B8", "C8-D8", "D8-C8", "D8-E8", "D8-D7", "E8-D8", "E8-F8", "E8-E7",
                              "G8-F8", "G8-G7", "C7-A6", "C7-B5", "C7-D5", "C7-E6", "D7-D6", "D7-E7", "F7-E7", "F7-G7",
                              "F7-F6", "E5-D5", "E5-D4", "E5-E4", "F3-E3", "F3-E2", "F3-G3"]
        }

        self.run_test_case(case)

    def test_gruppe_ad_endgame(self):
        case = {
            "fen": "3b02/5r02/3r04/8/8/2b02b02/2r05/6",
            "description": "End Game",
            "player": main.Player.BLUE,
            "expected_moves": ["C6-B6", "C6-D6", "F6-E6", "F6-G6", "F6-F7", "E1-D1", "E1-F1", "E1-E2", "E1-F2"]
        }

        self.run_test_case(case)

    def test_gruppe_z_endgame(self):
        case = {
            "fen": "3b01b0/1bb1r0b03/4bb3/2b03b01/2r03r01/3rb1r02/2r0r04/r02r01r0",
            "description": "End Game",
            "player": main.Player.BLUE,
            "expected_moves": ["D6-B7", "D6-C8", "D6-E8", "D6-F7", "C4-B4", "C4-D4", "G4-F4", "G4-H4", "E3-C4", "E3-D5",
                              "E3-F5", "E3-G4", "B2-A4", "B2-C4", "B2-D3", "E2-F2", "E1-D1", "E1-D2", "E1-E2", "E1-F1",
                              "G1-F1", "G1-G2"]
        }

        self.run_test_case(case)

    def test_gruppe_z_midgame(self):
        case = {
            "fen": "2b01b0b0/2b0bb4/8/1r06/3b0rbr0b01/3r02r01/2rr5/2r01r01",
            "description": "Mid Game",
            "player": main.Player.BLUE,
            "expected_moves": ["D5-C5", "E5-C6", "E5-D7", "E5-F7", "E5-G6", "G5-H5", "C2-B2", "C2-C3", "D2-B3", "D2-C4",
                               "D2-E4", "D2-F3", "D1-C1", "D1-E1", "F1-E1", "F1-F2", "F1-G1", "G1-G2", "G1-F1"]
        }

        self.run_test_case(case)

    def test_gruppe_b_endgame(self):
        case = {
            "fen": "2b02bb/1bb2b03/5bb2/8/1r03r02/6r01/8/r01r01rrr0",
            "description": "End Game",
            "player": main.Player.BLUE,
            "expected_moves": ["D1-C1", "D1-D2", "D1-E1", "G1-E2", "G1-H3", "B2-A4", "B2-C4", "B2-D3", "E2-D2", "E2-E3",
                               "E2-F2", "F3-D4", "F3-E5", "F3-G5", "F3-H4"]
        }

        self.run_test_case(case)

    def test_gruppe_k_early_game(self):
        case = {
            "fen": "b0b0b0b0b0b0/1bb3b0b01/3b04/4b03/5r02/1r02r03/2r0r02r01/r0r0r0r0r0r0",
            "description": "Early Game",
            "player": main.Player.BLUE,
            "expected_moves": ["B1-C1", "C1-B1", "C1-C2", "C1-D1", "D1-C1", "D1-D2", "D1-E1", "E1-D1", "E1-E2", "E1-F1",
                               "F1-E1", "F1-F2", "F1-G1", "G1-F1", "G1-G2", "B2-A4", "B2-C4", "B2-D3", "F2-E2", "F2-F3",
                               "F2-G2", "G2-F2", "G2-G3", "G2-H2", "D3-C3", "D3-D4", "D3-E3", "E4-D4", "E4-E5", "E4-F5",
                               "E4-F4"]
        }

        self.run_test_case(case)

    def test_gruppe_k_end_game(self):
        case = {
            "fen": "1bbb01b0b0/4b03/4rr1b01/2b02b02/5r02/1r06/3r02r01/1rrr01r01",
            "description": "End Game",
            "player": main.Player.RED,
            "expected_moves": ["C8-A7", "C8-B6", "C8-D6", "C8-E7", "D8-D7", "D8-E8", "F8-E8", "F8-F7", "F8-G8", "D7-C7",
                              "D7-D6", "D7-E7", "G7-F7", "G7-G6", "G7-H7", "B6-A6", "B6-B5", "B6-C6", "F5-E5", "F5-G5",
                              "E3-C2", "E3-D1", "E3-F1", "E3-G2"]
        }

        self.run_test_case(case)

    def test_gruppe_n_mid_end_game(self):
        case = {
            "fen": "b0b01b0b0b0/8/4b0b02/3br4/6b01/2rr3rb1/4rr3/r0r02r0r0",
            "description": "Mid Game",
            "player": main.Player.RED,
            "expected_moves": ["C6-E5", "C8-B8", "C6-B4", "C8-C7", "C8-D8", "C6-A5", "E7-D5", "E7-G6", "E7-F5", "G8-F8",
                               "G8-G7", "B8-B7", "B8-C8", "D4-B3", "F8-F7", "F8-G8", "D4-C2", "F8-E8", "D4-F3", "D4-E2"]
        }

        self.run_test_case(case)

    def test_gruppe_n_end_game_blue_win_in_1(self):
        case = {
            "fen": "b0b0b0b0b0b0/8/5b01b0/5r0b01/3b04/4r0rr1rb/3r04/r0r0r0r01r0",
            "description": "End Game",
            "player": main.Player.BLUE,
            "expected_moves": ["H3-H4", "C1-B1", "C1-D1", "E1-E2", "G4-G5", "G1-G2", "B1-C1", "D5-D6", "D1-D2", "F3-E3",
                               "F1-G1", "F3-G3", "F1-E1", "H6-G8", "H3-G3", "C1-C2", "G4-H4", "E1-D1", "E1-F1", "G1-F1",
                               "B1-B2", "D1-E1", "D5-C5", "D5-E6", "D1-C1", "D5-E5", "F1-F2", "H6-F7"]
        }

        self.run_test_case(case)

    def test_gruppe_t_endgame1(self):
        case = {
            "fen": "6/1b06/2bb1b0b02/6bb1/1r0br5/3r0rr3/8/4r0r0",
            "description": "End Game",
            "player": main.Player.BLUE,
            "expected_moves": ["B2-A2", "B2-C2", "B2-B3", "C3-A4", "C3-E4", "C3-B5", "C3-D5", "E3-D3", "E3-F3", "E3-E4",
                               "F3-E3", "F3-G3", "F3-F4", "G4-E5", "G4-F6", "G4-H6"]
        }

        self.run_test_case(case)

    def test_gruppe_t_endgame2(self):
        case = {
            "fen": "6/8/6b01/4bb3/r0r0rr4b0/3b02r01/1rr3r2/6",
            "description": "End Game",
            "player": main.Player.RED,
            "expected_moves": ["A5-B5", "A5-A4", "B5-A5", "B5-B4", "C5-E4", "C5-A4", "C5-D3", "C5-B3", "G6-F6", "G6-H6",
                              "G6-H5", "G6-G5", "B7-D6", "B7-A5", "F7-E7", "F7-G7", "F7-F6"]
        }

        self.run_test_case(case)

    def test_gruppe_j_endgame(self):
        case = {
            "fen": "6/1b06/1r0b02bb2/2r02b02/8/5rr2/2r03r01/6",
            "description": "End Game",
            "player": main.Player.BLUE,
            "expected_moves": ["B2-A2", "B2-C2", "C3-D3", "F4-E4", "F4-G4", "F4-F5", "F3-D4", "F3-E5", "F3-G5", "F3-H4"]
        }

        self.run_test_case(case)

    def test_gruppe_j_midgame(self):
        case = {
            "fen": "b0b04/b02bb2b01/2b05/4rb3/6b01/2r04r0/1r01r0r01r01/r0r04",
            "description": "Mid Game",
            "player": main.Player.RED,
            "expected_moves": ["B8-B7", "B8-C8", "C8-B8", "C8-C7", "C8-D8", "B7-A7", "B7-B6", "B7-C7", "D7-C7", "D7-D6",
                              "D7-E7", "E7-D7", "E7-E6", "E7-F7", "G7-F7", "G7-G6", "G7-H7", "C6-B6", "C6-C5", "C6-D6",
                              "H6-G6", "H6-H5", "H6-G5"]
        }

        self.run_test_case(case)

    def test_gruppe_f_advanced_game(self):
        case = {
            "fen": "b0b04/r0r0b02b0b0b0/2r02r0r0r0/8/8/b0b0b02b02/r0r0r02r0b0b0/4r0r0",
            "description": "Advanced Game",
            "player": main.Player.BLUE,
            "expected_moves": ["B1-A2", "B1-C1", "C1-B1", "C1-B2", "C1-D1", "C1-C2", "C2-D2", "F2-E2", "F2-G2", "F2-G3",
                               "G2-F2", "G2-F3", "G2-H2", "G2-H3", "H2-G2", "H2-G3", "A6-B6", "A6-B7", "B6-A6", "B6-A7",
                               "B6-C6", "B6-C7", "C6-B6", "C6-B7", "C6-D6", "F6-E6", "F6-G6", "G7-F8", "G7-H7", "H7-G7",
                               "H7-G8"]
        }

        self.run_test_case(case)

    def test_gruppe_f_endgame(self):
        case = {
            "fen": "6/3bb4/1br6/r01b0b02bb1/1rr2r0r01b0/6rb1/4rr3/6",
            "description": "End Game",
            "player": main.Player.BLUE,
            "expected_moves": ["D2-C4", "D2-B3", "D2-E4", "D2-F3", "C4-B4", "C4-B5", "C4-D4", "C4-C5", "D4-C4", "D4-E4",
                              "D4-E5", "D4-D5", "G4-F6", "G4-E5", "G4-H6", "H5-G5", "H5-H6", "G6-F8", "G6-E7"]
        }

        self.run_test_case(case)

    def test_gruppe_r_midgame(self):
        case = {
            "fen": "1b0b01b0b0/3bb4/8/1r03b02/3b0rrr0b01/6r01/1r0r0r04/2r01r0",
            "description": "Mid Game",
            "player": main.Player.RED,
            "expected_moves": ["D8-C8", "D8-E8", "D8-D7", "F8-E8", "F8-G8", "F8-F7", "B7-A7", "B7-C7", "B7-B6", "C7-B7",
                               "C7-D7", "C7-C6", "D7-C7", "D7-E7", "D7-D6", "G6-F6", "G6-H6", "E5-C4", "E5-G4", "E5-D3",
                               "E5-F3", "B4-A4", "B4-C4", "B4-B3"]
        }

        self.run_test_case(case)

    def test_gruppe_r_endgame(self):
        case = {
            "fen": "6/7rr/4bb1r01/8/8/b02bb3b0/8/6",
            "description": "End Game",
            "player": main.Player.RED,
            "expected_moves": ["G3-F3", "G3-H3", "G3-G2", "H2-F1"]
        }

        self.run_test_case(case)

    def test_gruppe_ag_midgame(self):
        case = {
            "fen": "b03b01/3bb2bb1/2bb1br3/1b06/5r02/2rr5/1r02rr3/r0r02rr1",
            "description": "Mid Game",
            "player": main.Player.BLUE,
            "expected_moves": ["B1-C1", "B1-B2", "F1-E1", "F1-G1", "F1-F2", "D2-B3", "D2-F3", "D2-C4", "D2-E4", "G2-E3",
                               "G2-F4", "G2-H4", "C3-A4", "C3-E4", "C3-B5", "C3-D5", "B4-A4", "B4-C4", "B4-B5"]
        }

        self.run_test_case(case)

    def test_gruppe_ag_endgame(self):
        case = {
            "fen": "b03b01/3b02b01/r01b05/8/8/4rb3/1r06/r03r01",
            "description": "End Game",
            "player": main.Player.BLUE,
            "expected_moves": ["B1-C1", "B1-B2", "F1-E1", "F1-G1", "F1-F2", "D2-C2", "D2-E2", "D2-D3", "G2-F2", "G2-H2",
                               "G2-G3", "C3-B3", "C3-D3", "C3-C4", "E6-C7", "E6-G7", "E6-D8", "E6-F8"]
        }

        self.run_test_case(case)

    def test_gruppe_s_early_game(self):
        case = {
            "fen": "b0b0b0b0b0b0/2bbb02bb1/4b03/8/3r04/8/1r0r01r0r0r01/r0r0r0r0r0r0",
            "description": "Early Game",
            "player": main.Player.RED,
            "expected_moves": ["B8-C8", "B8-B7", "C8-B8", "C8-C7", "C8-D8", "D8-C8", "D8-D7", "D8-E8", "E8-D8", "E8-E7",
                               "E8-F8", "F8-E8", "F8-F7", "F8-G8", "G8-F8", "G8-G7", "B7-A7", "B7-B6", "B7-C7", "C7-B7",
                               "C7-C6", "C7-D7", "E7-D7", "E7-E6", "E7-F7", "F7-E7", "F7-F6", "F7-G7", "G7-F7", "G7-G6",
                               "G7-H7", "D5-C5", "D5-D4", "D5-E5"]
        }

        self.run_test_case(case)

    def test_gruppe_s_end_game(self):
        case = {
            "fen": "2b03/1b0b05/6b01/3bb2r01/3r02r01/2b05/2r03r01/3r02",
            "description": "End Game",
            "player": main.Player.BLUE,
            "expected_moves": ["D1-C1", "D1-D2", "D1-E1", "B2-A2", "B2-B3", "B2-C2", "C2-B2", "C2-C3", "C2-D2", "G3-F3",
                               "G3-H3", "D4-B5", "D4-C6", "D4-E6", "D4-F5", "C6-B6", "C6-D6"]
        }

        self.run_test_case(case)

    def test_gruppe_aa(self):
        case = {
            "fen": "b0b02b01/3b04/4r03/1rrb03bb1/5r02/4b03/3rr4/1r03r0",
            "description": "End Game",
            "player": main.Player.BLUE,
            "expected_moves": ["E6-D6", "E6-E7", "E6-F6", "C4-C5", "C4-D4", "G4-H6", "G4-F6", "G4-E5", "D2-D3", "D2-C2",
                               "D2-E2", "B1-B2", "B1-C1", "C1-B1", "C1-C2", "C1-D1", "F1-E1", "F1-F2", "F1-G1", "D2-E3",
                               "E6-D7"]
        }

        self.run_test_case(case)

    def test_gruppe_aa_2(self):
        case = {
            "fen": "b0b0b01b0b0/4b01b01/2bb2b02/8/1r01br4/4r01r01/2r02rr2/r01r01r0r0",
            "description": "End Game",
            "player": main.Player.RED,
            "expected_moves": ["B8-C8", "B8-B7", "D8-C8", "D8-E8", "D8-D7", "F8-E8", "F8-G8", "G8-F8", "G8-G7", "C7-B7",
                               "C7-D7", "C7-C6", "F7-D6", "F7-E5", "F7-G5", "F7-H6", "E6-D6", "E6-E5", "E6-F6", "G6-F6",
                               "G6-G5", "G6-H6", "B5-A5", "B5-B4", "B5-C5", "D5-B4", "D5-C3", "D5-E3", "D5-F4"]
        }

        self.run_test_case(case)

    def test_gruppe_q_scenario_1(self):
        case = {
            "fen": "6/8/4b03/1r01b0r03/2r02r0b01/1b02b01r01/1r06/6",
            "description": "End Game",
            "player": main.Player.BLUE,
            "expected_moves": ["D4-C4", "B6-A6", "B6-C6", "D4-D5", "D4-C5", "E3-D3", "E3-F3", "E6-D6", "E6-F6", "E6-E7",
                               "G5-H5"]
        }

        self.run_test_case(case)

    def test_gruppe_q_scenario_2(self):
        case = {
            "fen": "b0b0b0b0b0b0/8/8/4b03/1r01b01r02/8/3r02r01/6",
            "description": "End Game",
            "player": main.Player.RED,
            "expected_moves": ["B5-A5", "B5-C5", "B5-B4", "D7-C7", "D7-E7", "D7-D6", "F5-E4", "F5-E5", "F5-G5", "F5-F4",
                               "G7-G6", "G7-H7", "G7-F7"]
        }

        self.run_test_case(case)

    def test_gruppe_c_end_game(self):
        case = {
            "fen": "5b0/1bbb0b0brb0b01/8/3b0r03/8/4b03/1rr1b0r0rrrr1/1r04",
            "description": "End Game",
            "player": main.Player.RED,
            "expected_moves": ["C8-B8", "C8-C7", "C8-D7", "C8-D8", "B7-A5", "B7-C5", "B7-D6", "E4-E3", "E4-F4", "F7-H6",
                              "F7-G5", "F7-E5", "F7-D6", "G7-H5", "G7-F5", "G7-E6", "E2-G1", "E2-C1"]
        }

        self.run_test_case(case)

    def test_gruppe_c_early_game(self):
        case = {
            "fen": "6/1bbbbbbbbbbbb1/8/8/8/8/1rrrrrrrrrrrr1/6",
            "description": "Early Game",
            "player": main.Player.BLUE,
            "expected_moves": ["B2-A4", "B2-C4", "B2-D3", "C2-A3", "C2-B4", "C2-D4", "C2-E3", "D2-B3", "D2-C4", "D2-E4",
                               "D2-F3", "E2-C3", "E2-D4", "E2-F4", "E2-G3", "F2-D3", "F2-E4", "F2-G4", "F2-H3", "G2-E3",
                               "G2-F4", "G2-H4"]
        }

        self.run_test_case(case)

    def test_gruppe_v_midgame(self):
        case = {
            "fen": "b0b0b0b01b0/3b04/2b01b0b0b01/2b05/3b04/1r01r01rr2/2rr1r03/r0r0r0r01r0",
            "description": "Mid Game",
            "player": main.Player.BLUE,
            "expected_moves": ["B1-B2", "B1-C1", "C1-B1", "C1-C2", "C1-D1", "D1-C1", "D1-D2", "D1-E1", "E1-D1", "E1-E2",
                               "E1-F1", "G1-F1", "G1-G2", "D2-C2", "D2-D3", "D2-E2", "C3-B3", "C3-C4", "C3-D3", "E3-D3",
                               "E3-E4", "E3-F3", "F3-E3", "F3-F4", "F3-G3", "G3-F3", "G3-G4", "G3-H3", "C4-B4", "C4-C5",
                               "C4-D4", "D5-C5", "D5-E5"]
        }

        self.run_test_case(case)

    def test_gruppe_v_endgame(self):
        case = {
            "fen": "2bb3/5b02/8/2bb5/5rr2/8/3b03r0/7",
            "description": "End Game",
            "player": main.Player.RED,
            "expected_moves": ["F5-D4", "F5-E3", "F5-G3", "F5-H4", "H7-G7", "H7-H6"]
        }

        self.run_test_case(case)

    def test_gruppe_p_midgame(self):
        case = {
            "fen": "1b0b01b0b0/3b0b03/1b03b02/2b01b03/4r0r0b01/4r01r01/1rr1rr4/1r0r01r01",
            "description": "Mid Game",
            "player": main.Player.BLUE,
            "expected_moves": ["C1-B1", "C1-D1", "C1-C2", "D1-C1", "D1-E1", "D1-D2", "F1-G1", "F1-E1", "F1-F2", "G1-F1",
                               "G1-G2", "D2-E2", "D2-C2", "D2-D3", "E2-D2", "E2-E3", "E2-F2", "B3-A3", "B3-B4", "B3-C3",
                               "F3-E3", "F3-F4", "F3-G3", "C4-B4", "C4-C5", "C4-D4", "E4-D4", "E4-F4", "E4-F5", "G5-H5"]
        }

        self.run_test_case(case)

    def test_gruppe_p_end_game(self):
        case = {
            "fen": "1b03b0/r02bb1b02/3b04/1r06/4r0r0b01/2b03r01/2r05/2r01r01",
            "description": "End Game",
            "player": main.Player.RED,
            "expected_moves": ["A2-B2", "B4-A4", "B4-C4", "B4-B3", "E5-F5", "E5-D5", "E5-E4", "F5-E5", "F5-F4", "G6-F6",
                              "G6-H6", "C7-B7", "C7-D7", "D8-D7", "D8-E8", "D8-C8", "F8-E8", "F8-G8", "F8-F7"]
        }

        self.run_test_case(case)

    def test_midgame_possible_moves(self):
        case = {
            "fen": "1b04/5b02/8/8/3b04/2r05/8/r03r01",
            "description": "Game",
            "player": main.Player.RED,
            "expected_moves": [ "B8-B7", "B8-C8", "F8-E8", "F8-F7", "F8-G8",
                                "C6-B6", "C6-C5", "C6-D6", "C6-D5"]
        }

        self.run_test_case(case)

    def test_endgame_possible_moves(self):
        case = {
            "fen": "r05/8/8/3rr4/5b02/8/1b06/6",
            "description": "Game",
            "player": main.Player.BLUE,
            "expected_moves": ["F5-E5", "F5-F6", "F5-G5", "B7-A7", "B7-B8", "B7-C7"]
        }

        self.run_test_case(case)

    def test_gruppe_h_left_edge_blue_moves(self):
        case = {
            "fen": "b0b0b0b0b0b0/b06r0/b06r0/b06r0/b06r0/b06r0/b06r0/r0r0r0r0r0r0",
            "description": "Game",
            "player": main.Player.BLUE,
            "expected_moves": ["A2-A3", "A2-B2", "A3-A4", "A3-B3", "A4-A5", "A4-B4", "A5-A6", "A5-B5",
            "A6-A7", "A6-B6", "A7-B7", "A7-B8", "B1-B2", "B1-C1", "C1-B1", "C1-C2",
            "C1-D1", "D1-C1", "D1-D2", "D1-E1", "E1-D1", "E1-E2", "E1-F1", "F1-E1",
            "F1-F2", "F1-G1", "G1-F1", "G1-G2", "G1-H2"]
        }

        self.run_test_case(case)

    def test_gruppe_h_right_edge_red_moves(self):
        case = {
            "fen": "b0b0b0b0b0b0/b06r0/b06r0/b06r0/b06r0/b06r0/b06r0/r0r0r0r0r0r0",
            "description": "Game",
            "player": main.Player.RED,
            "expected_moves": [ "B8-A7", "B8-B7", "B8-C8", "C8-B8", "C8-C7", "C8-D8", "D8-C8", "D8-D7", "D8-E8",
            "E8-D8", "E8-E7", "E8-F8", "F8-E8", "F8-F7", "F8-G8", "G8-F8", "G8-G7", "H2-G1",
            "H2-G2", "H3-G3", "H3-H2", "H4-G4", "H4-H3", "H5-G5", "H5-H4", "H6-G6", "H6-H5",
            "H7-G7", "H7-H6"]
        }

        self.run_test_case(case)

    def test_gruppe_h_midgame_blue_moves(self):
        case = {
            "fen": "4b01/2b01bb3/1bb1b02b01/1r01r0rrbb2/2bb3r01/2rrr01rr2/1r06/3r02",
            "description": "Game",
            "player": main.Player.BLUE,
            "expected_moves": [ "B3-A5", "B3-D4", "C2-B2", "C2-C3", "C2-D2", "C5-A6", "C5-B7", "C5-D7", "C5-E6",
            "D3-C3", "D3-E3", "D3-E4", "E2-C3", "E2-D4", "E2-G3", "F1-E1", "F1-F2", "F1-G1",
            "F4-D5", "F4-E6", "F4-G6", "F4-H5", "G3-F3", "G3-G4", "G3-H3"]
        }

        self.run_test_case(case)

    def test_gruppe_h_midgame_red_moves(self):
        case = {
            "fen": "4b01/2b01bb3/1bb1b02b1/1r01r0rrbb2/2bb3r01/2rrr01rr2/1r06/3r02",
            "description": "Game",
            "player": main.Player.RED,
            "expected_moves": [ "B4-A4", "B4-C4", "B7-A7", "B7-B6", "B7-C7", "C6-A5", "C6-B4", "C6-D4", "C6-E5",
            "D4-C4", "D6-C5", "D6-D5", "D6-E6", "E4-C3", "E4-D2", "E4-F2", "E4-G3", "E8-D8",
            "E8-E7", "E8-F8", "F6-D5", "F6-G4", "F6-H5", "G5-F4", "G5-F5", "G5-G4", "G5-H5"]
        }

        self.run_test_case(case)

    def test_gruppe_h_midgame_blue_moves2(self):
        case = {
            "fen": "1b02b01/3bbbb3/1b03b02/2b01bb1b01/1r05r0/1rr1rrr0rr2/3r01r02/1r04",
            "description": "Game",
            "player": main.Player.BLUE,
            "expected_moves": ["B3-A3", "B3-B4", "B3-C3", "C1-B1", "C1-C2", "C1-D1", "C4-B4", "C4-B5", "C4-C5",
            "C4-D4", "D2-B3", "D2-C4", "D2-F3", "E2-C3", "E2-D4", "E2-F4", "E2-G3", "E4-C5",
            "E4-D6", "E4-F6", "E4-G5", "F1-E1", "F1-F2", "F1-G1", "F3-E3", "F3-F4", "F3-G3",
            "G4-F4", "G4-G5", "G4-H4", "G4-H5"]
        }

        self.run_test_case(case)

    def test_gruppe_h_midgame_red_moves2(self):
        case = {
            "fen": "1b02b01/3bbbb3/1b03b02/2b01bb1b01/1r05r0/1rr1rrr0rr2/3r01r02/1r04",
            "description": "Game",
            "player": main.Player.RED,
            "expected_moves": ["B5-A5", "B5-B4", "B5-C4", "B5-C5", "B6-A4", "B6-C4", "B6-D5", "C8-B8", "C8-C7",
            "C8-D8", "D6-B5", "D6-C4", "D6-E4", "D6-F5", "D7-C7", "D7-E7", "E6-E5", "F6-D5",
            "F6-E4", "F6-G4", "F6-H5", "F7-E7", "F7-G7", "H5-G4", "H5-G5", "H5-H4"]
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






if __name__ == "__main__":
    main()
