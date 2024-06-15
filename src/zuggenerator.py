import random
import Bitboards

def update_fen(bitboards):
    fen_rows = []
    for row in range(7, -1, -1):
        fen_row = ""
        empty_count = 0
        for col in range(8):
            piece = bitboards.get_piece(row, col)
            if piece:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += piece
            else:
                empty_count += 1
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)
    return "/".join(fen_rows)

def play_game(fen):
    bitboards = Bitboards.parse_fen(Bitboards.reformulate(fen))
    players = ['r', 'b']
    player_index = 0  # Start with player 'r'

    while True:

        bitboards = Bitboards.parse_fen(Bitboards.reformulate(fen))
        player = players[player_index]
        all_possible_moves = Bitboards.calculate_all_possible_moves(bitboards, player)


        if not all_possible_moves:
            print(f"No possible moves for player {player}. Game Over.")
            break

        start_pos, possible_moves = random.choice(list(all_possible_moves.items()))
        end_pos = random.choice(possible_moves)
        print(f"Player {player} moves from {Bitboards.Pos(*start_pos).to_chess_notation()} to {Bitboards.Pos(*end_pos).to_chess_notation()}")


        bitboards = Bitboards.do_move(Bitboards.Pos(*start_pos), Bitboards.Pos(*end_pos), player, bitboards)
        bitboards.print_combined_board()

        # Check if the game is over
        game_end_message = Bitboards.check_game_end(bitboards)
        if game_end_message:
            print(game_end_message)
            break

        fen = bitboards.update_fen()
        # Switch to the other player
        player_index = 1 - player_index

# Example Usage
fen = "b0b04/1b0b05/b01b0rr4/1rb1b01b02/3r0r01rr2/bbr0r02rr2/4r01rr1/r04r0"
play_game(fen)
