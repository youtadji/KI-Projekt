import time
from src.main import *
from src.zuggenerator import *

# Function to benchmark the calculate_possible_moves function with a specific position
def benchmark_zuggenerator_with_test_case(zuggenerator_func, board, pos, player):
    print(f"Testing position at row {pos.row}, column {pos.col}...")
    start_time = time.time()
    for _ in range(1000):  # Repeat each position 1000 times for accurate benchmarking
        # Call the zuggenerator function with player, board, and position
        zuggenerator_func(board, pos, player)
    end_time = time.time()

    total_time = end_time - start_time
    print(f"Total time taken: {total_time:.4f} seconds")
    print(f"Avg. time per position: {total_time / 1000:.6f} seconds\n")

# Call the benchmark function with your Zuggenerator function and all positions on the board
for row in range(8):
    for col in range(8):
        # Setup the board for each position
        board = main.visualize_board(main.reformulate("6/1bb1b02b01/8/2r05/3r01b02/5r0r02/2rr1r03/6 b"))  # Example FEN string
        player = "b"  # Example player color
        pos = Pos(col, row)  # Create Pos object for the position

        # Replace Zuggenerator() with the actual way you instantiate your Zuggenerator class
        benchmark_zuggenerator_with_test_case(calculate_possible_moves, board, pos, player)
