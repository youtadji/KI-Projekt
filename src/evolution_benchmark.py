import time
import Bitboards


def benchmark_evolution(bitboards, player):
    total_time = 0
    total_moves = 0
    pop_size = 5
    num_generations = 3
    mutation_rate = 0.1

    start_time = time.time()
    for _ in range(1000):
        start_time = time.time()
        move_time = min(total_time - (time.time() - start_time), 1.0)

        Bitboards.evolutionary_algorithm_with_alpha_beta(bitboards, player,  pop_size, num_generations, mutation_rate, move_time)
        end_time = time.time()
        # Calculate elapsed time
        total_time += (end_time - start_time)

        # Calculate average time per call
        average_time_per_call = total_time / 1000
        return average_time_per_call


# Define benchmark cases
benchmark_cases = [
    {"fen": "bb1b0b0b0b0/b01b0b0b01b01/8/3b04/3r04/2r05/1rr2r0r01r0/1r0r0r0r0r0", "player": 'r', "description": "Start Game"},
    {"fen": "2bbbb1b0/1b06/1b01b04/4b03/4r03/3r02b01/1r0r02rr2/2rr2r0", "player": 'r', "description": "Middle Game"},
    {"fen": "1b04/2b03b01/b01rr5/r02b01b02/1b06/1r02b03/8/1r01r0r0r0", "player": 'b', "description": "End Game"}
]

# Perform benchmarking for each case
for case in benchmark_cases:
    fen = case["fen"]
    player = case["player"]
    description = case["description"]
    bitboards = Bitboards.parse_fen(Bitboards.reformulate(fen))
    visualized_board = bitboards.print_combined_board()
    avg_time = benchmark_evolution(bitboards, player)
    print(f"Benchmarking evolution for {description}: {avg_time:.6f} seconds per call")
    print(f"Benchmark for {description}: {(avg_time) * 1000:.4f} seconds for 1000 Wiederholungen")