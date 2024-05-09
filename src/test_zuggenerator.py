import time
import main
import zuggenerator
import board

def benchmark_move_generation(fen, player, board):
    start_time = time.time()
    for _ in range(1000):
        moves = zuggenerator.get_possible_moves(fen, player, board)
    end_time = time.time()
    total_time = end_time - start_time
    average_time_per_call = total_time / 1000
    return average_time_per_call

# Define benchmark cases
benchmark_cases = [
    {"fen": "bb1b0b0b0b0/b01b0b0b01b01/8/3b04/3r04/2r05/1rr2r0r01r0/1r0r0r0r0r0", "player": main.Player.RED, "description": "Start Game"},
    {"fen": "2bbbb1b0/1b06/1b01b04/4b03/4r03/3r02b01/1r0r02rr2/2rr2r0", "player": main.Player.RED, "description": "Middle Game"},
    {"fen": "1b04/2b03b01/b01rr5/r02b01b02/1b06/1r02b03/8/1r01r0r0r0", "player": main.Player.BLUE, "description": "End Game"}
]

# Perform benchmarking for each case
for case in benchmark_cases:
    fen = case["fen"]
    player = case["player"]
    description = case["description"]
    avg_time = benchmark_move_generation(fen, player, board.create_board(fen))
    print(f"Benchmark for {description}: {avg_time:.6f} seconds per call")
    print(f"Benchmark for {description}: {(avg_time)*1000:.4f} seconds for 1000 Wiederholungen")