import  Bitboards
# Example FEN string
fen = "2rr2br/2rr2br1b0/b07/b03rr2r0/b05rb1/8/8/r0r0r0r0r0r0"
# Parse the FEN string
bitboards = Bitboards.parse_fen(Bitboards.reformulate(fen))

# Visualize the parsed bit boards
bitboards.print_all_boards()
#the combined one
bitboards.print_combined_board()