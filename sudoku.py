import tkinter as tk

class SudokuGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Professional Sudoku Game")
        self.window.resizable(False, False)

        # 0 represents empty, playable cells
        self.initial_board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

        # The complete correct solution map for validation
        self.solution_board = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 4, 6, 1, 7, 2, 3],
            [4, 2, 6, 8, 7, 3, 9, 5, 1],
            [7, 1, 3, 5, 2, 9, 4, 8, 6],
            [9, 6, 5, 7, 3, 4, 2, 8, 1],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 1, 2, 8, 6, 5, 7, 9]
        ]

        # Container array to keep track of Entry widgets
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        
        self._build_ui()
        self.window.mainloop()

    def _build_ui(self):
        """Constructs the 9x9 visual board layout."""
        grid_frame = tk.Frame(self.window, bg="black", bd=2)
        grid_frame.pack(padx=15, pady=15)

        for row in range(9):
            for col in range(9):
                # Group 3x3 sub-grids visually using internal padding borders
                pad_x = (1 if col % 3 == 0 and col > 0 else 0, 0)
                pad_y = (1 if row % 3 == 0 and row > 0 else 0, 0)
                
                cell_value = self.initial_board[row][col]

                if cell_value != 0:
                    # Given fixed system numbers (Locked labels)
                    cell = tk.Label(
                        grid_frame, text=str(cell_value), width=4, height=2,
                        font=("Helvetica", 16, "bold"), bg="#E0E0E0", fg="#333333"
                    )
                else:
                    # User input fields
                    cell = tk.Entry(
                        grid_frame, width=4, font=("Helvetica", 16),
                        justify="center", bd=1, bg="#FFFFFF", fg="#0000FF"
                    )
                    # Bind string filters directly onto keystrokes
                    cell.bind("<KeyRelease>", lambda e, r=row, c=col: self._sanitize_input(r, c))
                
                cell.grid(row=row, column=col, padx=pad_x, pady=pad_y, sticky="nsew")
                self.cells[row][col] = cell

        # Control Panel Actions Block
        self.status_label = tk.Label(self.window, text="Fill the empty cells!", font=("Helvetica", 12))
        self.status_label.pack(pady=5)

        verify_btn = tk.Button(
            self.window, text="Check Solution", font=("Helvetica", 12, "bold"),
            bg="#4CAF50", fg="white", command=self.verify_board
        )
        verify_btn.pack(pady=10)

    def _sanitize_input(self, row: int, col: int):
        """Ensures input entries remain bounded strictly to a single 1-9 integer value."""
        widget = self.cells[row][col]
        current_text = widget.get().strip()

        if not current_text:
            return

        # Explicit character check to ensure no letters or system-controlled text values pass
        if current_text[-1].isdigit() and current_text[-1] != '0':
            single_digit = current_text[-1]
            widget.delete(0, tk.END)
            widget.insert(0, single_digit)
        else:
            # Completely flush non-compliant text configurations
            widget.delete(0, tk.END)

    def verify_board(self):
        """Scans entries and evaluates placement statuses against the solution dictionary mapping."""
        is_complete_and_correct = True

        for row in range(9):
            for col in range(9):
                widget = self.cells[row][col]
                expected_val = self.solution_board[row][col]

                if isinstance(widget, tk.Entry):
                    user_val = widget.get().strip()
                    
                    if user_val == str(expected_val):
                        widget.config(bg="#C8E6C9") # Light Green highlight for correct values
                    else:
                        widget.config(bg="#FFCDD2") # Light Red highlight for invalid values
                        is_complete_and_correct = False
                else:
                    # Skip configuration for default static label nodes
                    continue

        if is_complete_and_correct:
            self.status_label.config(text=" Brilliant! Puzzle Correctly Solved.", fg="green")
        else:
            self.status_label.config(text=" Discrepancies detected. Review the highlighted squares.", fg="red")


if __name__ == "__main__":
    SudokuGame()
