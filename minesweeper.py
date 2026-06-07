import tkinter as tk
import random

# --- CONFIGURATION CONSTANTS ---
GRID_SIZE = 10         # 10x10 grid matrix
NUM_MINES = 12         # Total hidden landmines


class Minesweeper:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Minesweeper Core Engine")
        self.window.resizable(False, False)

        # Game state tracking properties
        self.board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.flagged = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        
        # Grid reference matrix for button widget tracking
        self.buttons = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.game_active = True

        self._initialize_game()
        self.window.mainloop()

    def _initialize_game(self):
        """Orchestrates system setup, handles asset mapping, and builds the UI matrix."""
        # Scorecard Panel Header
        self.status_label = tk.Label(
            self.window, text=f"🚩 Right-Click to Flag | Mines: {NUM_MINES}", 
            font=("Helvetica", 12, "bold"), pady=5
        )
        self.status_label.pack()

        # Build Interactive Grid Frame
        grid_frame = tk.Frame(self.window, bg="#777777", bd=2)
        grid_frame.pack(padx=10, pady=5)

        # 1. Instantiate Button Layouts safely across rows and columns
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                btn = tk.Button(
                    grid_frame, text="", font=("Helvetica", 11, "bold"), 
                    width=3, height=1, bg="#D9D9D9", relief="raised"
                )
                # Bind Left-Click for revealing and Right-Click for flagging tracking matrices
                btn.bind("<Button-1>", lambda event, row=r, col=c: self._left_click(row, col))
                btn.bind("<Button-3>", lambda event, row=r, col=c: self._toggle_flag(row, col))
                
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[r][c] = btn

        # 2. Deploy Mines randomly across coordinates
        mines_placed = 0
        while mines_placed < NUM_MINES:
            rand_row = random.randint(0, GRID_SIZE - 1)
            rand_col = random.randint(0, GRID_SIZE - 1)
            
            if self.board[rand_row][rand_col] != -1:
                self.board[rand_row][rand_col] = -1  # -1 represents a mine node
                mines_placed += 1

        # 3. Calculate adjacent threat numbers for all safe coordinate vectors
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board[r][c] == -1:
                    continue
                self.board[r][c] = self._count_adjacent_mines(r, c)

    def _count_adjacent_mines(self, row: int, col: int) -> int:
        """Counts hidden mines surrounding a target coordinate cell block index."""
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                    if self.board[nr][nc] == -1:
                        count += 1
        return count

    def _left_click(self, row: int, col: int):
        """Processes selection events and triggers cascading reveal maps."""
        if not self.game_active or self.revealed[row][col] or self.flagged[row][col]:
            return

        # Condition A: Stepped on a hidden mine -> Trigger Game Over sequence
        if self.board[row][col] == -1:
            self._trigger_defeat()
            return

        # Condition B: Process safe spot revelation cascade
        self._reveal_cell(row, col)

        # Condition C: Evaluate if all safe blocks are completely unmasked
        if self._check_victory_condition():
            self.game_active = False
            self.status_label.config(text="🏆 Outstanding! Minefield Cleared Successfully.", fg="green")

    def _reveal_cell(self, row: int, col: int):
        """Unmasks target index layers and applies auto-expansion cascading recursively."""
        if self.revealed[row][col] or self.flagged[row][col]:
            return

        self.revealed[row][col] = True
        value = self.board[row][col]
        
        # Explicit aesthetic coloring configurations mapped to proximity threat numbers
        color_map = {1: "blue", 2: "green", 3: "red", 4: "purple", 5: "maroon"}
        text_color = color_map.get(value, "black")

        if value > 0:
            self.buttons[row][col].config(text=str(value), bg="#E6E6E6", fg=text_color, relief="sunken")
        else:
            # If the block has 0 surrounding mines, cleanly clear it out and trigger auto-expansion cascades
            self.buttons[row][col].config(text="", bg="#E6E6E6", relief="sunken")
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                        self._reveal_cell(nr, nc)

    def _toggle_flag(self, row: int, col: int):
        """Locks or unlocks cells safely via right-click interaction loops."""
        if not self.game_active or self.revealed[row][col]:
            return

        if not self.flagged[row][col]:
            self.flagged[row][col] = True
            self.buttons[row][col].config(text="🚩", fg="red")
        else:
            self.flagged[row][col] = False
            self.buttons[row][col].config(text="")

    def _check_victory_condition(self) -> bool:
        """Verifies if every non-mine cell context has been cleanly unmasked."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board[r][c] != -1 and not self.revealed[r][c]:
                    return False
        return True

    def _trigger_defeat(self):
        """Terminates session controls and reveals all underlying mine nodes."""
        self.game_active = False
        self.status_label.config(text="💥 BOOM! Game Over. Explosion Detected.", fg="red")
        
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board[r][c] == -1:
                    self.buttons[r][c].config(text="💣", bg="#FFCDD2", relief="sunken")


if __name__ == "__main__":
    Minesweeper()
