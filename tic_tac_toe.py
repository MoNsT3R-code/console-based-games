import tkinter as tk

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe Engine")
        self.window.resizable(False, False)

        # Game state tracking
        self.current_player = "X"
        self.board = [""] * 9
        self.game_active = True

        # Grid references for button reconfiguration updates
        self.buttons = []

        self._build_ui()
        self.window.mainloop()

    def _build_ui(self):
        """Constructs the visual scorecards, grid components, and reset buttons."""
        # Status Scorecard Header
        self.status_label = tk.Label(
            self.window, text=f"Player {self.current_player}'s Turn", 
            font=("Helvetica", 16, "bold"), pady=10
        )
        self.status_label.pack()

        # 3x3 Button Grid Frame Assembly
        grid_frame = tk.Frame(self.window, bg="#CCCCCC", bd=2)
        grid_frame.pack(padx=20, pady=5)

        for i in range(9):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                grid_frame, text="", font=("Helvetica", 24, "bold"), 
                width=5, height=2, bg="#FFFFFF", activebackground="#F0F0F0",
                command=lambda index=i: self._process_move(index)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.buttons.append(btn)

        # Action Control Panel Footer
        reset_btn = tk.Button(
            self.window, text="Restart Match", font=("Helvetica", 12, "bold"),
            bg="#2196F3", fg="white", activebackground="#1976D2", 
            activeforeground="white", command=self.reset_game, pady=5
        )
        reset_btn.pack(pady=15)

    def _process_move(self, index: int):
        """Processes player moves and updates game state without try-except overrides."""
        # Defensive check: block action if slot is occupied or game is over
        if self.board[index] != "" or not self.game_active:
            return

        # Update core state tracking array
        self.board[index] = self.current_player
        
        # Style tokens based on player identity
        text_color = "#E53935" if self.current_player == "X" else "#1E88E5"
        self.buttons[index].config(text=self.current_player, fg=text_color)

        # Evaluate match condition
        if self._check_win():
            self.game_active = False
            self.status_label.config(text=f"🏆 Player {self.current_player} Wins!", fg="green")
        elif "" not in self.board:
            self.game_active = False
            self.status_label.config(text="🤝 Match Tied! Clear Board to Retry.", fg="orange")
        else:
            # Shift player turn control smoothly
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.config(text=f"Player {self.current_player}'s Turn", fg="black")

    def _check_win(self) -> bool:
        """Evaluates win row constraints systematically against structural vector indexes."""
        win_vectors = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical Columns
            [0, 4, 8], [2, 4, 6]              # Diagonal Crossings
        ]

        for vector in win_vectors:
            if self.board[vector[0]] == self.board[vector[1]] == self.board[vector[2]] != "":
                # Highlight winning button nodes dynamically
                for cell_index in vector:
                    self.buttons[cell_index].config(bg="#C8E6C9")
                return True
        return False

    def reset_game(self):
        """Flushes structural variable maps and resets UI controls cleanly."""
        self.current_player = "X"
        self.board = [""] * 9
        self.game_active = True
        
        self.status_label.config(text=f"Player {self.current_player}'s Turn", fg="black")
        
        for btn in self.buttons:
            btn.config(text="", bg="#FFFFFF")


if __name__ == "__main__":
    TicTacToe()
