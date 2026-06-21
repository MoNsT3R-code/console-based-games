import tkinter as tk
import random

# --- CONFIGURATION CONSTANTS ---
INITIAL_WIDTH = 600
INITIAL_HEIGHT = 600
SPEED = 90              # Game loop speed in milliseconds (slightly faster for better gameplay)
SPACE_SIZE = 30         # Grid spacing size in pixels
BODY_PARTS = 3          # Starting snake length
SNAKE_COLOR = "#00FF66" # Vibrant Neon Green
FOOD_COLOR = "#FF3366"  # Vibrant Crimson Red
BG_COLOR = "#121212"    # Modern Deep Charcoal Dark-Mode


class Snake:
    def __init__(self):
        self.coordinates = []
        self.squares = []

        # Initialize starting coordinates cascading vertically down from top-left
        for i in range(BODY_PARTS):
            self.coordinates.append([SPACE_SIZE * 2, 0])

    def draw(self, canvas):
        """Draws the initial snake blocks."""
        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, 
                fill=SNAKE_COLOR, outline="#1c1c1c", tag="snake"
            )
            self.squares.append(square)


class Food:
    def __init__(self, canvas):
        # Calculate dynamic bounds based on active window size
        canvas_width = canvas.winfo_width() if canvas.winfo_width() > 1 else INITIAL_WIDTH
        canvas_height = canvas.winfo_height() if canvas.winfo_height() > 1 else INITIAL_HEIGHT
        
        max_x = max(1, int(canvas_width / SPACE_SIZE) - 1)
        max_y = max(1, int(canvas_height / SPACE_SIZE) - 1)
        
        x = random.randint(0, max_x) * SPACE_SIZE
        y = random.randint(0, max_y) * SPACE_SIZE

        self.coordinates = [x, y]
        self.canvas_item = canvas.create_oval(
            x + 2, y + 2, x + SPACE_SIZE - 2, y + SPACE_SIZE - 2, 
            fill=FOOD_COLOR, outline="", tag="food"
        )


class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Classic Snake (Modernized)")
        
        # Enable complete Maximize and Minimize features
        self.window.resizable(True, True)
        self.window.configure(bg=BG_COLOR)

        self.score = 0
        self.direction = "right"
        self.paused = False
        self.game_is_over = False

        # Custom Frameless UI Container for Scoreboard
        self.ui_frame = tk.Frame(self.window, bg=BG_COLOR)
        self.ui_frame.pack(fill=tk.X, padx=10, pady=5)

        self.label = tk.Label(
            self.ui_frame, text=f"SCORE: {self.score}", 
            font=("Helvetica", 18, "bold"), fg="#FFFFFF", bg=BG_COLOR
        )
        self.label.pack(side=tk.LEFT, padx=10)
        
        self.info_label = tk.Label(
            self.ui_frame, text="Space: Pause | R: Restart", 
            font=("Helvetica", 10), fg="#888888", bg=BG_COLOR
        )
        self.info_label.pack(side=tk.RIGHT, padx=10)

        # Initialize Adaptable Game Canvas
        self.canvas = tk.Canvas(
            self.window, bg=BG_COLOR, height=INITIAL_HEIGHT, width=INITIAL_WIDTH,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Center Window on Display Initially
        self.window.update()
        ww, wh = self.window.winfo_width(), self.window.winfo_height()
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry(f"{ww}x{wh}+{int((sw-ww)/2)}+{int((sh-wh)/2)}")

        # Input Bindings
        self.window.bind("<Left>", lambda e: self.change_direction("left"))
        self.window.bind("<Right>", lambda e: self.change_direction("right"))
        self.window.bind("<Up>", lambda e: self.change_direction("up"))
        self.window.bind("<Down>", lambda e: self.change_direction("down"))
        
        # Utility Bindings (Space, Enter, Escape, R)
        self.window.bind("<space>", lambda e: self.toggle_pause(True))
        self.window.bind("<Return>", lambda e: self.toggle_pause(False))
        self.window.bind("<r>", lambda e: self.restart_game())
        self.window.bind("<R>", lambda e: self.restart_game())

        # Build Game Components
        self.snake = Snake()
        self.window.update() 
        self.food = Food(self.canvas)
        self.snake.draw(self.canvas)

        # Start Engine
        self.next_turn()
        self.window.mainloop()

    def next_turn(self) -> None:
        """Core physics loop calculation."""
        if self.paused or self.game_is_over:
            return

        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE

        # Unshift head mechanics
        self.snake.coordinates.insert(0, [x, y])
        square = self.canvas.create_rectangle(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, 
            fill=SNAKE_COLOR, outline="#121212", tag="snake"
        )
        self.snake.squares.insert(0, square)

        # Collision Check against Active Vector Food Point
        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.label.config(text=f"SCORE: {self.score}")
            self.canvas.delete("food")
            self.food = Food(self.canvas)
        else:
            # Shift Tail if structural dimensions remain static
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        # Safety checking relative system state dimensions
        if self.check_collisions():
            self.game_over()
        else:
            self.window.after(SPEED, self.next_turn)

    def change_direction(self, new_direction: str) -> None:
        """Changes heading vectors strictly avoiding reversing into oneself."""
        if self.paused or self.game_is_over:
            return

        opposites = {"left": "right", "right": "left", "up": "down", "down": "up"}
        if new_direction != opposites.get(self.direction):
            self.direction = new_direction

    def toggle_pause(self, request_pause: bool) -> None:
        """Pauses and resumes the active game engine thread execution safely."""
        if self.game_is_over:
            return

        if request_pause and not self.paused:
            self.paused = True
            self.canvas.create_rectangle(
                0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(),
                fill="#000000", stipple="gray50", tag="pause_overlay"
            )
            self.canvas.create_text(
                self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2,
                font=("Helvetica", 28, "bold"), text="GAME PAUSED\n[ Press Enter to Resume ]",
                fill="#FFFFFF", justify="center", tag="pause_text"
            )
        elif not request_pause and self.paused:
            self.paused = False
            self.canvas.delete("pause_text")
            self.canvas.delete("pause_overlay")
            self.next_turn()

    def check_collisions(self) -> bool:
        """Translates current context configurations against board vectors."""
        x, y = self.snake.coordinates[0]

        # Validates responsive width dynamic updates
        if x < 0 or x >= self.canvas.winfo_width() or y < 0 or y >= self.canvas.winfo_height():
            return True

        # Process standard inner matrix arrays self colliding loops
        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False

    def game_over(self) -> None:
        """Halts framework and provides a modern Game Over interface screen."""
        self.game_is_over = True
        self.canvas.delete("all")
        
        # Transparent background styling
        self.canvas.create_text(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2,
            font=("Helvetica", 36, "bold"), text="GAME OVER\n\nPress 'R' to Play Again",
            fill=FOOD_COLOR, justify="center", tag="gameover"
        )

    def restart_game(self) -> None:
        """Completely restores the base variables without reconstructing application loops."""
        self.game_is_over = False
        self.paused = False
        self.score = 0
        self.direction = "right"
        
        self.label.config(text=f"SCORE: {self.score}")
        self.canvas.delete("all")
        
        self.snake = Snake()
        self.food = Food(self.canvas)
        self.snake.draw(self.canvas)
        
        self.next_turn()


if __name__ == "__main__":
    SnakeGame()
