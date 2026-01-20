import tkinter as tk
from tkinter import messagebox
import Bitboards  # Ensure this is the file with your Bitboards class


class JumpSturdyGUI:
    def __init__(self, root, bitboards):
        self.root = root
        self.root.title("Jump Sturdy - Projektgruppe U")
        self.bitboards = bitboards
        self.selected_pos = None
        self.valid_moves = []
        self.current_player = 'b'  # Standard starting player

        # UI Elements
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.setup_ui()

    def setup_ui(self):
        # Create Frame for Board
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(side=tk.TOP, padx=10, pady=10)

        # Create 8x8 Grid
        for r in range(8):
            # Row Labels (8-1)
            tk.Label(self.board_frame, text=str(8 - r)).grid(row=r, column=0)

            for c in range(8):
                # Column Labels (A-H) only on bottom row
                if r == 7:
                    tk.Label(self.board_frame, text=chr(ord('A') + c)).grid(row=8, column=c + 1)

                # Set square color
                bg_color = "#DDBB99" if (r + c) % 2 == 0 else "#AA8866"

                # Forbidden corner squares
                logic_row = 7 - r
                if (logic_row, c) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                    bg_color = "gray"
                    btn = tk.Button(self.board_frame, width=8, height=4, bg=bg_color, state=tk.DISABLED)
                else:
                    btn = tk.Button(self.board_frame, width=8, height=4, bg=bg_color,
                                    command=lambda lr=logic_row, lc=c: self.on_square_click(lr, lc))

                btn.grid(row=r, column=c + 1)
                self.buttons[logic_row][c] = btn

        # Control Panel
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.info_label = tk.Label(self.control_frame, text="Current Player: Blue", font=('Arial', 10, 'bold'))
        self.info_label.pack()

        self.ai_btn = tk.Button(self.control_frame, text="Execute AI Move", bg="lightgray",
                                command=self.play_ai_move)
        self.ai_btn.pack(pady=5)

        self.refresh_board()

    def refresh_board(self):
        """Syncs the UI buttons with the current Bitboard state."""
        for r in range(8):
            for c in range(8):
                if self.buttons[r][c]:
                    piece = self.bitboards.get_piece(r, c)
                    # Reset color to standard
                    std_bg = "#DDBB99" if (r + c) % 2 == 0 else "#AA8866"
                    self.buttons[r][c].config(bg=std_bg)

                    if piece:
                        # Styling pieces based on player
                        color = "red" if 'r' in piece else "blue"
                        # Use bold text for stacks
                        display_text = piece.upper() if len(piece) > 1 else piece
                        self.buttons[r][c].config(text=display_text, fg=color, font=('Arial', 12, 'bold'))
                    else:
                        self.buttons[r][c].config(text="")

    def on_square_click(self, r, c):
        if self.selected_pos is None:
            piece = self.bitboards.get_piece(r, c)
            if piece and piece[-1] == self.current_player:
                self.selected_pos = (r, c)
                all_moves = Bitboards.calculate_possible_moves(self.bitboards, r, c, self.current_player)
                self.valid_moves = all_moves

                # Highlight selection and moves
                self.buttons[r][c].config(bg="yellow")
                for mr, mc in self.valid_moves:
                    self.buttons[mr][mc].config(bg="#90EE90")  # Light Green
        else:
            # Check if click is a move
            if (r, c) in self.valid_moves:
                start = Bitboards.Pos(self.selected_pos[0], self.selected_pos[1])
                end = Bitboards.Pos(r, c)
                self.bitboards = Bitboards.do_move(start, end, self.current_player, self.bitboards)
                self.switch_player()

            self.selected_pos = None
            self.valid_moves = []
            self.refresh_board()
            self.check_game_over()

    def switch_player(self):
        self.current_player = 'r' if self.current_player == 'b' else 'b'
        name = "Red" if self.current_player == 'r' else "Blue"
        self.info_label.config(text=f"Current Player: {name}")

    def play_ai_move(self):
        """Triggers your AI to move for the current player."""
        self.info_label.config(text="AI is thinking...")
        self.root.update()  # Force UI update

        # Using your Iterative Deepening
        score, move = Bitboards.iterative_deepening(self.bitboards, self.current_player, total_time=2)

        if move:
            start_pos, end_pos = move
            s = Bitboards.Pos(start_pos[0], start_pos[1])
            e = Bitboards.Pos(end_pos[0], end_pos[1])
            self.bitboards = Bitboards.do_move(s, e, self.current_player, self.bitboards)
            self.switch_player()
            self.refresh_board()
            self.check_game_over()
        else:
            messagebox.showinfo("Game Over", f"AI found no moves. {self.current_player} loses.")

    def check_game_over(self):
        status = Bitboards.check_game_end(self.bitboards)
        if status:
            messagebox.showinfo("Game Result", status)

if __name__ == "__main__":
    # This part runs ONLY when you start this specific file
    start_fen = "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0"
    init_boards = Bitboards.parse_fen(Bitboards.reformulate(start_fen))

    root = tk.Tk()
    app = JumpSturdyGUI(root, init_boards)
    root.mainloop()