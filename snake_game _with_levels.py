import tkinter as tk
import random
import math

# --- MODERN DESIGN CONSTANTS ---
INITIAL_WIDTH = 850
INITIAL_HEIGHT = 600
GRID_SIZE = 25          
SNAKE_HEAD_COLOR = "#00F0FF" # Cyan Glow
SNAKE_BODY_COLOR = "#00A8FF" # Matrix Teal
FOOD_COLOR = "#FF007F"       # Neon Pink
BLOCK_COLOR = "#FF9F00"      # Vivid Orange (Obstacles)
ENEMY_COLOR = "#A020F0"      # Purple (Moving Enemies)
GRID_COLOR = "#1A1A2E"       
BG_COLOR = "#0F0F1A"         
SIDEBAR_BG = "#161623"       

FOOD_PER_LEVEL = 5           
MAX_LEVEL = 10


class Snake:
    def __init__(self):
        self.coordinates = []
        self.squares = []
        for i in range(4):
            self.coordinates.append([GRID_SIZE * (5 - i), GRID_SIZE * 8])

    def draw(self, canvas):
        for idx, (x, y) in enumerate(self.coordinates):
            color = SNAKE_HEAD_COLOR if idx == 0 else SNAKE_BODY_COLOR
            r = 2 if idx == 0 else 4
            square = canvas.create_rectangle(
                x + r, y + r, x + GRID_SIZE - r, y + GRID_SIZE - r, 
                fill=color, outline="", width=0, tag="snake"
            )
            self.squares.append(square)


class Food:
    def __init__(self, canvas, snake_coords, block_coords):
        c_width = canvas.winfo_width() if canvas.winfo_width() > 1 else INITIAL_WIDTH - 200
        c_height = canvas.winfo_height() if canvas.winfo_height() > 1 else INITIAL_HEIGHT
        max_x = max(1, int(c_width / GRID_SIZE) - 1)
        max_y = max(1, int(c_height / GRID_SIZE) - 1)
        
        while True:
            x = random.randint(0, max_x) * GRID_SIZE
            y = random.randint(0, max_y) * GRID_SIZE
            if [x, y] not in snake_coords and [x, y] not in block_coords:
                break

        self.coordinates = [x, y]
        self.glow = canvas.create_oval(
            x, y, x + GRID_SIZE, y + GRID_SIZE, fill="#5A005A", outline="", tag="food"
        )
        self.core = canvas.create_oval(
            x + 4, y + 4, x + GRID_SIZE - 4, y + GRID_SIZE - 4, fill=FOOD_COLOR, outline="", tag="food"
        )


class ObstacleBlock:
    def __init__(self, canvas, snake_coords, count):
        self.canvas = canvas
        self.coordinates = []
        self.items = []
        
        if count <= 0: return

        c_width = canvas.winfo_width() if canvas.winfo_width() > 1 else INITIAL_WIDTH - 200
        c_height = canvas.winfo_height() if canvas.winfo_height() > 1 else INITIAL_HEIGHT
        max_x = max(1, int(c_width / GRID_SIZE) - 1)
        max_y = max(1, int(c_height / GRID_SIZE) - 1)

        for _ in range(count):
            while True:
                x = random.randint(0, max_x) * GRID_SIZE
                y = random.randint(0, max_y) * GRID_SIZE
                if [x, y] not in snake_coords and x > GRID_SIZE * 7 and [x, y] not in self.coordinates:
                    break
            
            self.coordinates.append([x, y])
            block = canvas.create_rectangle(
                x + 3, y + 3, x + GRID_SIZE - 3, y + GRID_SIZE - 3,
                fill=BLOCK_COLOR, outline="#FF5500", width=1, tag="block"
            )
            self.items.append(block)


class MovingEnemy:
    def __init__(self, canvas, snake_coords, block_coords):
        self.canvas = canvas
        c_width = canvas.winfo_width() if canvas.winfo_width() > 1 else INITIAL_WIDTH - 200
        c_height = canvas.winfo_height() if canvas.winfo_height() > 1 else INITIAL_HEIGHT
        self.max_x = max(1, int(c_width / GRID_SIZE) - 1) * GRID_SIZE
        self.max_y = max(1, int(c_height / GRID_SIZE) - 1) * GRID_SIZE

        while True:
            x = random.randint(2, int(self.max_x / GRID_SIZE) - 2) * GRID_SIZE
            y = random.randint(2, int(self.max_y / GRID_SIZE) - 2) * GRID_SIZE
            if [x, y] not in snake_coords and [x, y] not in block_coords:
                break

        self.coordinates = [x, y]
        self.direction = random.choice(["up", "down", "left", "right"])
        
        self.item = canvas.create_polygon(
            x + GRID_SIZE/2, y + 2, 
            x + GRID_SIZE - 2, y + GRID_SIZE/2,
            x + GRID_SIZE/2, y + GRID_SIZE - 2, 
            x + 2, y + GRID_SIZE/2,
            fill=ENEMY_COLOR, outline="#FF00FF", width=1, tag="enemy"
        )

    def patrol_step(self):
        x, y = self.coordinates
        if self.direction == "up": y -= GRID_SIZE
        elif self.direction == "down": y += GRID_SIZE
        elif self.direction == "left": x -= GRID_SIZE
        elif self.direction == "right": x += GRID_SIZE

        if x < 0 or x > self.max_x or y < 0 or y > self.max_y:
            bounce = {"up": "down", "down": "up", "left": "right", "right": "left"}
            self.direction = bounce[self.direction]
            return 

        self.canvas.move(self.item, x - self.coordinates[0], y - self.coordinates[1])
        self.coordinates = [x, y]


class ParticleEffect:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.particles = []
        num_particles = 12
        for i in range(num_particles):
            angle = (i / num_particles) * 2 * math.pi
            speed = random.uniform(3, 7)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            p = canvas.create_oval(x+10, y+10, x+14, y+14, fill=FOOD_COLOR, outline="")
            self.particles.append((p, dx, dy, 1.0))

    def update(self) -> bool:
        alive = False
        for idx, (p, dx, dy, life) in enumerate(self.particles):
            if life <= 0: continue
            self.canvas.move(p, dx, dy)
            new_life = life - 0.15
            self.particles[idx] = (p, dx, dy, new_life)
            if new_life <= 0: self.canvas.delete(p)
            else: alive = True
        return alive


class NeonSnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("NEON OVERDRIVE: PROGRESSIVE SECTORS")
        self.window.resizable(True, True)
        self.window.configure(bg=BG_COLOR)

        self.score = 0
        self.high_score = 0
        self.level = 1
        self.level_progress = 0  
        
        self.base_speed = 110
        self.current_speed = self.base_speed
        self.direction = "right"
        self.paused = False
        self.game_is_over = False
        self.death_reason = "UNKNOWN ERROR" # Tracks logs dynamically
        
        self.active_effects = []
        self.enemies = []
        self.blocks_coords_list = []

        # UI Layout Sidebars
        self.main_container = tk.Frame(self.window, bg=BG_COLOR)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.main_container, bg=SIDEBAR_BG, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="⚡ NEON ⚡\nSNAKE", font=("Courier New", 20, "bold"), fg=SNAKE_HEAD_COLOR, bg=SIDEBAR_BG).pack(pady=15)
        self.level_box = tk.Label(self.sidebar, text="SECTOR 01", font=("Courier New", 16, "bold"), fg=SNAKE_HEAD_COLOR, bg=SIDEBAR_BG)
        self.level_box.pack(pady=5)
        self.progress_label = tk.Label(self.sidebar, text=f"NEXT: 0/{FOOD_PER_LEVEL}", font=("Helvetica", 10), fg="#8888AA", bg=SIDEBAR_BG)
        self.progress_label.pack(pady=2)

        self.score_box = tk.Label(self.sidebar, text="SCORE\n000", font=("Consolas", 16, "bold"), fg="#FFFFFF", bg="#222235", bd=4, relief="flat", width=12)
        self.score_box.pack(pady=10)
        self.hi_score_box = tk.Label(self.sidebar, text="HI-SCORE\n000", font=("Consolas", 11), fg="#656585", bg=SIDEBAR_BG)
        self.hi_score_box.pack(pady=2)
        self.status_box = tk.Label(self.sidebar, text="• LIVE ENGINE", font=("Helvetica", 10, "bold"), fg="#00FF66", bg=SIDEBAR_BG)
        self.status_box.pack(pady=15)

        controls_text = "CONTROLS\n\n[Arrows]  Move\n[Space]   Pause\n[Enter]   Resume\n[R Key]   Reset"
        tk.Label(self.sidebar, text=controls_text, font=("Courier New", 8), fg="#555575", bg=SIDEBAR_BG, justify=tk.LEFT).pack(side=tk.BOTTOM, pady=15)

        self.canvas = tk.Canvas(self.main_container, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.window.bind("<Left>", lambda e: self.change_direction("left"))
        self.window.bind("<Right>", lambda e: self.change_direction("right"))
        self.window.bind("<Up>", lambda e: self.change_direction("up"))
        self.window.bind("<Down>", lambda e: self.change_direction("down"))
        self.window.bind("<space>", lambda e: self.toggle_pause(True))
        self.window.bind("<Return>", lambda e: self.toggle_pause(False))
        self.window.bind("<r>", lambda e: self.restart_game())
        self.window.bind("<R>", lambda e: self.restart_game())
        
        self.canvas.bind("<Configure>", lambda e: self.draw_background_matrix())

        self.window.update()
        self.initial_centering(850, INITIAL_HEIGHT)
        
        self.setup_game_entities()
        self.next_turn()
        self.window.mainloop()

    def initial_centering(self, w, h):
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry(f"{w}x{h}+{int((sw-w)/2)}+{int((sh-h)/2)}")

    def draw_background_matrix(self):
        self.canvas.delete("grid_line")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for x in range(0, w, GRID_SIZE):
            self.canvas.create_line(x, 0, x, h, fill=GRID_COLOR, tag="grid_line")
        for y in range(0, h, GRID_SIZE):
            self.canvas.create_line(0, y, w, y, fill=GRID_COLOR, tag="grid_line")
        self.canvas.tag_lower("grid_line")

    def setup_game_entities(self):
        self.canvas.delete("all")
        self.draw_background_matrix()
        
        self.snake = Snake()
        self.enemies = []
        self.blocks_coords_list = []
        
        if 1 <= self.level <= 3:
            self.level_box.config(fg=SNAKE_HEAD_COLOR)
            block_count = 0
            enemy_count = 0
        elif 4 <= self.level <= 7:
            self.level_box.config(fg=ENEMY_COLOR)
            block_count = 0
            enemy_count = 1 + (self.level - 4)
        else:
            self.level_box.config(fg=BLOCK_COLOR)
            block_count = 4 + (self.level - 8) * 3
            enemy_count = 2 + (self.level - 8)

        self.blocks = ObstacleBlock(self.canvas, self.snake.coordinates, count=block_count)
        self.blocks_coords_list = self.blocks.coordinates if hasattr(self.blocks, 'coordinates') else []
        
        for _ in range(enemy_count):
            self.enemies.append(MovingEnemy(self.canvas, self.snake.coordinates, self.blocks_coords_list))
            
        self.food = Food(self.canvas, self.snake.coordinates, self.blocks_coords_list)
        self.snake.draw(self.canvas)
        self.current_speed = max(35, self.base_speed - (self.level * 6))

    def next_turn(self) -> None:
        self.active_effects = [fx for fx in self.active_effects if fx.update()]

        if self.paused or self.game_is_over:
            self.window.after(30, self.next_turn)
            return

        for enemy in self.enemies:
            enemy.patrol_step()

        x, y = self.snake.coordinates[0]

        if self.direction == "up": y -= GRID_SIZE
        elif self.direction == "down": y += GRID_SIZE
        elif self.direction == "left": x -= GRID_SIZE
        elif self.direction == "right": x += GRID_SIZE

        self.snake.coordinates.insert(0, [x, y])
        
        square = self.canvas.create_rectangle(
            x + 2, y + 2, x + GRID_SIZE - 2, y + GRID_SIZE - 2, 
            fill=SNAKE_HEAD_COLOR, outline="", tag="snake"
        )
        self.snake.squares.insert(0, square)

        if len(self.snake.squares) > 1:
            self.canvas.itemconfig(self.snake.squares[1], fill=SNAKE_BODY_COLOR)

        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.level_progress += 1
            self.score_box.config(text=f"SCORE\n{self.score:03d}")
            self.active_effects.append(ParticleEffect(self.canvas, x, y))
            self.canvas.delete("food")
            
            if self.level_progress >= FOOD_PER_LEVEL:
                if self.level >= MAX_LEVEL:
                    self.game_victory()
                    return
                else:
                    self.advance_level()
            else:
                self.progress_label.config(text=f"NEXT: {self.level_progress}/{FOOD_PER_LEVEL}")
                self.food = Food(self.canvas, self.snake.coordinates, self.blocks_coords_list)
        else:
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        if self.check_collisions():
            self.game_over()
        else:
            self.window.after(self.current_speed, self.next_turn)

    def advance_level(self):
        self.level += 1
        self.level_progress = 0
        self.level_box.config(text=f"SECTOR {self.level:02d}")
        self.progress_label.config(text=f"NEXT: 0/{FOOD_PER_LEVEL}")
        
        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill=SNAKE_HEAD_COLOR, tag="flash")
        self.window.update()
        self.window.after(60, lambda: self.canvas.delete("flash"))
        self.setup_game_entities()

    def change_direction(self, new_direction: str) -> None:
        if self.paused or self.game_is_over: return
        opposites = {"left": "right", "right": "left", "up": "down", "down": "up"}
        if new_direction != opposites.get(self.direction):
            self.direction = new_direction

    def toggle_pause(self, request_pause: bool) -> None:
        if self.game_is_over: return

        if request_pause and not self.paused:
            self.paused = True
            self.status_box.config(text="• PAUSED", fg="#FFCC00")
            self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(),
                                         fill="#050510", stipple="gray50", tag="ui_overlay")
            self.canvas.create_text(
                self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2,
                font=("Courier New", 24, "bold"), text="SYSTEM PAUSED\n\n[ Press Enter to Resume ]",
                fill="#FFFFFF", justify="center", tag="ui_text"
            )
        elif not request_pause and self.paused:
            self.paused = False
            self.status_box.config(text="• LIVE ENGINE", fg="#00FF66")
            self.canvas.delete("ui_text")
            self.canvas.delete("ui_overlay")

    def check_collisions(self) -> bool:
        """Determines exactly how and where the snake structural logic fails."""
        x, y = self.snake.coordinates[0]
        
        if x < 0 or x >= self.canvas.winfo_width() or y < 0 or y >= self.canvas.winfo_height():
            self.death_reason = "OUTER WALL GRID COLLISION"
            return True
            
        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                self.death_reason = "SELF-INTERSECTION CRASH"
                return True
                
        if self.level >= 4:
            for enemy in self.enemies:
                if x == enemy.coordinates[0] and y == enemy.coordinates[1]:
                    self.death_reason = "SECURITY DRONE INTERCEPT"
                    return True
                    
        if self.level >= 8 and [x, y] in self.blocks_coords_list:
            self.death_reason = "STATIC HAZARD BLOCK IMPACT"
            return True
            
        return False

    def game_over(self) -> None:
        """Fires off an updated diagnostic screen logging statistics details."""
        self.game_is_over = True
        self.status_box.config(text="• OFFLINE", fg=FOOD_COLOR)
        
        is_new_high = self.score > self.high_score
        if is_new_high:
            self.high_score = self.score
            self.hi_score_box.config(text=f"HI-SCORE\n{self.high_score:03d}")

        # Visual Flash Shockwave
        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill=FOOD_COLOR, tag="flash")
        self.window.update()
        
        self.window.after(80, lambda: self.canvas.delete("flash"))
        self.window.after(100, lambda: self.render_diagnostic_death_screen(is_new_high))

    def render_diagnostic_death_screen(self, new_high):
        """Builds a premium holographic readout display overlay directly on the canvas."""
        cx = self.canvas.winfo_width() / 2
        cy = self.canvas.winfo_height() / 2

        # 1. Holographic Dark Card Base Background
        self.canvas.create_rectangle(cx - 240, cy - 180, cx + 240, cy + 180, 
                                     fill="#0B0B16", outline=FOOD_COLOR, width=2, tag="ui_card")
        
        # 2. Card Header
        self.canvas.create_text(cx, cy - 140, font=("Courier New", 24, "bold"), 
                                text="❌ CRITICAL CRASH ❌", fill=FOOD_COLOR, tag="ui_card")
        
        # 3. Diagnostic Log Text lines
        self.canvas.create_text(cx, cy - 80, font=("Courier New", 11, "bold"),
                                text=f"LOG: {self.death_reason}", fill="#FF7777", tag="ui_card")
        
        # 4. Score statistics tracking rows
        stats_text = (
            f"SECTOR REACHED : {self.level:02d}\n"
            f"FINAL SCORE    : {self.score:03d}\n"
            f"SYSTEM RECORD  : {self.high_score:03d}"
        )
        self.canvas.create_text(cx - 160, cy + 5, font=("Consolas", 14), 
                                text=stats_text, fill="#FFFFFF", anchor="w", tag="ui_card")

        # 5. Conditional High Score Graphic Overlay Badge
        if new_high:
            self.canvas.create_rectangle(cx + 40, cy - 15, cx + 180, cy + 25, fill="#003322", outline=SNAKE_HEAD_COLOR, tag="ui_card")
            self.canvas.create_text(cx + 110, cy + 5, font=("Courier New", 10, "bold"), text="🔥 NEW RECORD 🔥", fill=SNAKE_HEAD_COLOR, tag="ui_card")

        # 6. User Instructions Footer
        self.canvas.create_text(cx, cy + 130, font=("Courier New", 13, "bold"), 
                                text="[ PRESS 'R' TO REBOOT SYSTEM ]", fill="#8888AA", tag="ui_card")

    def game_victory(self) -> None:
        self.game_is_over = True
        self.status_box.config(text="• SECURED", fg=SNAKE_HEAD_COLOR)
        if self.score > self.high_score:
            self.high_score = self.score
            self.hi_score_box.config(text=f"HI-SCORE\n{self.high_score:03d}")
            
        # Draw clean Victory layout
        cx, cy = self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2
        self.canvas.create_rectangle(cx - 240, cy - 150, cx + 240, cy + 150, fill="#0B0B16", outline=SNAKE_HEAD_COLOR, width=2)
        self.canvas.create_text(cx, cy - 80, font=("Courier New", 26, "bold"), text="SYSTEM OVERRIDDEN", fill=SNAKE_HEAD_COLOR)
        self.canvas.create_text(cx, cy - 20, font=("Courier New", 18), text="CORE SECTOR 10 SECURED", fill="#FFFFFF")
        self.canvas.create_text(cx, cy + 30, font=("Consolas", 14), text=f"FINAL SCORE: {self.score:03d}", fill="#FFFFFF")
        self.canvas.create_text(cx, cy + 100, font=("Courier New", 12, "bold"), text="[ PRESS 'R' TO LOOP SIMULATION ]", fill="#8888AA")

    def restart_game(self) -> None:
        self.game_is_over = False
        self.paused = False
        self.score = 0
        self.level = 1
        self.level_progress = 0
        self.direction = "right"
        
        self.level_box.config(text="SECTOR 01")
        self.progress_label.config(text=f"NEXT: 0/{FOOD_PER_LEVEL}")
        self.score_box.config(text="SCORE\n000")
        self.status_box.config(text="• LIVE ENGINE", fg="#00FF66")
        
        self.setup_game_entities()
        self.next_turn()


if __name__ == "__main__":
    NeonSnakeGame()
