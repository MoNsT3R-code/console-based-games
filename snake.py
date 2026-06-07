import tkinter as tk
import random

# --- CONFIGURATION CONSTANTS ---
GAME_WIDTH = 600
GAME_HEIGHT = 600
SPEED = 100            # Refresh rate in milliseconds (lower is faster)
SPACE_SIZE = 30        # Size of grid items in pixels
BODY_PARTS = 3         # Starting size of the snake
SNAKE_COLOR = "#00FF00" # Green
FOOD_COLOR = "#FF0000"  # Red
BACKGROUND_COLOR = "#000000" # Black


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Initialize starting coordinates at top-left grid
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

    def draw(self, canvas):
        """Draws the initial snake blocks onto the canvas."""
        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


class Food:
    def __init__(self, canvas):
        # Calculate random grid coordinates
        x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE)) - 1) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE)) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        self.canvas_item = canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )


class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Classic Snake Game")
        self.window.resizable(False, False)

        self.score = 0
        self.direction = "down"

        # Initialize Scoreboard Label
        self.label = tk.Label(
            self.window, text=f"Score: {self.score}", font=("Consolas", 24)
        )
        self.label.pack()

        # Initialize Game Canvas
        self.canvas = tk.Canvas(
            self.window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH
        )
        self.canvas.pack()

        # Center Window on Display
        self.window.update()
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Bind Control Inputs
        self.window.bind("<Left>", lambda event: self.change_direction("left"))
        self.window.bind("<Right>", lambda event: self.change_direction("right"))
        self.window.bind("<Up>", lambda event: self.change_direction("up"))
        self.window.bind("<Down>", lambda event: self.change_direction("down"))

        # Setup Entities
        self.snake = Snake()
        self.food = Food(self.canvas)
        self.snake.draw(self.canvas)

        # Start Engine Loop
        self.next_turn()
        self.window.mainloop()

    def next_turn(self) -> None:
        """Main game loop handler tracking coordinates, collisions, and updates."""
        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE

        # Insert new head coordinates
        self.snake.coordinates.insert(0, [x, y])
        square = self.canvas.create_rectangle(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
        )
        self.snake.squares.insert(0, square)

        # Collision Check: Did the head touch the food?
        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.label.config(text=f"Score: {self.score}")
            self.canvas.delete("food")
            self.food = Food(self.canvas)
        else:
            # Pop tail if no food eaten to simulate movement
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        # Defensively verify collision bounds
        if self.check_collisions():
            self.game_over()
        else:
            self.window.after(SPEED, self.next_turn)

    def change_direction(self, new_direction: str) -> None:
        """Updates heading direction while preventing immediate 180-degree self-collisions."""
        if new_direction == "left" and self.direction != "right":
            self.direction = new_direction
        elif new_direction == "right" and self.direction != "left":
            self.direction = new_direction
        elif new_direction == "up" and self.direction != "down":
            self.direction = new_direction
        elif new_direction == "down" and self.direction != "up":
            self.direction = new_direction

    def check_collisions(self) -> bool:
        """Checks if the snake hit the walls or its own body."""
        x, y = self.snake.coordinates[0]

        # Wall collisions
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True

        # Body self-collisions
        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False

    def game_over(self) -> None:
        """Clears canvas and displays game-over sequence."""
        self.canvas.delete("all")
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            font=("Consolas", 50),
            text="GAME OVER",
            fill="red",
            tag="gameover"
        )


if __name__ == "__main__":
    SnakeGame()
