import tkinter as tk
import random
import math

# --- PREMIUM DESIGN CONSTANTS ---
INITIAL_WIDTH = 880
INITIAL_HEIGHT = 620
GRID_SIZE = 25          
SNAKE_HEAD_COLOR = "#00F0FF" # Electric Cyan Glow
SNAKE_BODY_CORE = "#00A8FF"  # High-Res Plasma Teal
SNAKE_BODY_TAIL = "#00558F"  # Deep Gradient Blue
FOOD_COLOR = "#FF007F"       # Cyber Neon Pink
BLOCK_COLOR = "#FF9F00"      # Vivid Alert Orange 
ENEMY_COLOR = "#A020F0"      # Aggressive Drone Purple
GRID_COLOR = "#141424"       # Deep Matrix Grid Link
BG_COLOR = "#0A0A12"         
SIDEBAR_BG = "#12121F"       

FOOD_PER_LEVEL = 5           
MAX_LEVEL = 10


class Snake:
    def __init__(self):
        self.coordinates = []
        self.squares = []
        # Spawn near middle left heading right
        for i in range(4):
            self.coordinates.append([GRID_SIZE * (5 - i), GRID_SIZE * 8])

    def draw(self, canvas, direction="right"):
        """Draws a premium, tapered plasma-thread snake body with structural details."""
        for idx, (x, y) in enumerate(self.coordinates):
            taper = max(1, min(6, idx))
            
            if idx == 0:
                color = SNAKE_HEAD_COLOR
                # Draw main head base
                square = canvas.create_rectangle(
                    x + taper, y + taper, x + GRID_SIZE - taper, y + GRID_SIZE - taper, 
                    fill=color, outline="#FFFFFF", width=1, tag="snake"
                )
                self.squares.append(square)
                
                eye_offset = 5
                if direction in ["right", "left"]:
                    ex = x + (GRID_SIZE - 6 if direction == "right" else 4)
                    canvas.create_line(ex, y + eye_offset, ex, y + eye_offset + 3, fill=BG_COLOR, width=2, tag="snake")
                    canvas.create_line(ex, y + GRID_SIZE - eye_offset - 3, ex, y + GRID_SIZE - eye_offset, fill=BG_COLOR, width=2, tag="snake")
                elif direction in ["up", "down"]:
                    ey = y + (4 if direction == "up" else GRID_SIZE - 6)
                    canvas.create_line(x + eye_offset, ey, x + eye_offset + 3, ey, fill=BG_COLOR, width=2, tag="snake")
                    canvas.create_line(x + GRID_SIZE - eye_offset - 3, ey, x + GRID_SIZE - eye_offset, ey, fill=BG_COLOR, width=2, tag="snake")
            else:
                color = SNAKE_BODY_CORE if idx < 5 else SNAKE_BODY_TAIL
                square = canvas.create_rectangle(
                    x + taper, y + taper, x + GRID_SIZE - taper, y + GRID_SIZE - taper, 
                    fill=color, outline=SNAKE_BODY_TAIL, width=0, tag="snake"
                )
                self.squares.append(square)


class Food:
    def __init__(self, canvas, snake_coords, block_coords):
        c_width = canvas.winfo_width() if canvas.winfo_width() > 1 else INITIAL_WIDTH - 230
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
            x - 2, y - 2, x + GRID_SIZE + 2, y + GRID_SIZE + 2, fill="#4A0033", outline="", tag="food"
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

        c_width = canvas.winfo_width() if canvas.winfo_width() > 1 else INITIAL_WIDTH - 230
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
        c_width = canvas.winfo_width() if canvas.winfo_width() > 1 else INITIAL_WIDTH - 230
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


class NeonSnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("NEON OVERDRIVE: ADVANCED METRICS ENGINE")
        self.window.resizable(True, True)
        self.window.configure(bg=BG_COLOR)

        # Game Structural Logic Variables
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.level_progress = 0  
        self.completed_history = []
        
        self.base_speed = 110
        self.current_speed = self.base_speed
        self.direction = "right"
        self.direction_lock = False  # Prevents quick-tap self-collisions
        self.paused = False
        self.game_is_over = False
        self.intermission_active = False
        self.death_reason = "UNKNOWN ERROR" 
        self._loop_id = None # Tracks active loops to eliminate speed bugs
        
        self.enemies = []
        self.blocks_coords_list = []

        # UI Framework Side Panel Configuration
        self.main_container = tk.Frame(self.window, bg=BG_COLOR)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.main_container, bg=SIDEBAR_BG, width=230)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="⚡ NEON OVERDRIVE ⚡", font=("Courier New", 13, "bold"), fg=SNAKE_HEAD_COLOR, bg=SIDEBAR_BG).pack(pady=15)
        
        # Sector Tracking Panel Display
        self.level_box = tk.Label(self.sidebar, text="SECTOR 01", font=("Courier New", 18, "bold"), fg=SNAKE_HEAD_COLOR, bg=SIDEBAR_BG)
        self.level_box.pack(pady=2)
        self.progress_label = tk.Label(self.sidebar, text=f"NEXT LINK: 0/{FOOD_PER_LEVEL}", font=("Helvetica", 9), fg="#8888AA", bg=SIDEBAR_BG)
        self.progress_label.pack(pady=2)

        # Dynamic Threat Diagnostics Display Box
        self.tier_title = tk.Label(self.sidebar, text="DIAGNOSTIC STRENGTH", font=("Courier New", 8, "bold"), fg="#555575", bg=SIDEBAR_BG)
        self.tier_title.pack(pady=(10, 0))
        self.tier_status = tk.Label(self.sidebar, text="EASY MODE (CLEAN GRID)", font=("Courier New", 9, "bold"), fg="#00FF66", bg=SIDEBAR_BG)
        self.tier_status.pack(pady=2)

        self.score_box = tk.Label(self.sidebar, text="SCORE\n000", font=("Consolas", 16, "bold"), fg="#FFFFFF", bg="#1A1A2E", bd=4, relief="flat", width=14)
        self.score_box.pack(pady=15)
        self.hi_score_box = tk.Label(self.sidebar, text="HI-SCORE: 000", font=("Consolas", 11), fg="#656585", bg=SIDEBAR_BG)
        self.hi_score_box.pack(pady=2)

        # Levels History Log
        tk.Label(self.sidebar, text="CLEARED STAGES LOG", font=("Courier New", 8, "bold"), fg="#555575", bg=SIDEBAR_BG).pack(pady=(15, 0))
        self.history_box = tk.Label(self.sidebar, text="None (Current: S01)", font=("Courier New", 9), fg="#757595", bg=SIDEBAR_BG, justify=tk.LEFT)
        self.history_box.pack(pady=2)

        controls_text = "KEY LEGEND MAP\n[Arrows] Move\n[Space]  Pause\n[R Key]  Reboot Game"
        tk.Label(self.sidebar, text=controls_text, font=("Courier New", 8), fg="#444460", bg=SIDEBAR_BG, justify=tk.LEFT).pack(side=tk.BOTTOM, pady=15)

        # Gameplay Arena Canvas
        self.canvas = tk.Canvas(self.main_container, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Input Window Handlers
        self.window.bind("<Left>", lambda e: self.change_direction("left"))
        self.window.bind("<Right>", lambda e: self.change_direction("right"))
        self.window.bind("<Up>", lambda e: self.change_direction("up"))
        self.window.bind("<Down>", lambda e: self.change_direction("down"))
        self.window.bind("<space>", lambda e: self.toggle_pause())
        self.window.bind("<r>", lambda e: self.restart_game())
        self.window.bind("<R>", lambda e: self.restart_game())
        
        self.canvas.bind("<Configure>", lambda e: self.draw_background_matrix())

        self.window.update()
        self.initial_centering(880, INITIAL_HEIGHT)
        
        self.setup_game_entities()
        self.start_loop()
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

    def update_sidebar_diagnostics(self):
        """Updates difficulty strength logs dynamically based on milestones."""
        if 1 <= self.level <= 3:
            self.level_box.config(fg=SNAKE_HEAD_COLOR)
            self.tier_status.config(text="EASY TIER (NO HAZARDS)", fg="#00FF66")
        elif 4 <= self.level <= 7:
            self.level_box.config(fg=ENEMY_COLOR)
            self.tier_status.config(text="MEDIUM TIER (DRONES)", fg="#CCAA00")
        else:
            self.level_box.config(fg=BLOCK_COLOR)
            self.tier_status.config(text="HARD TIER (MAX THREAT)", fg="#FF3333")

        if self.completed_history:
            history_text = ", ".join([f"S{lvl:02d}" for lvl in self.completed_history])
            if len(self.completed_history) > 3:
                history_text = "..." + ", ".join([f"S{lvl:02d}" for lvl in self.completed_history[-3:]])
            self.history_box.config(text=f"Cleared: {history_text}\nActive: S{self.level:02d}")
        else:
            self.history_box.config(text=f"None (Current: S{self.level:02d})")

    def setup_game_entities(self):
        self.canvas.delete("all")
        self.draw_background_matrix()
        self.update_sidebar_diagnostics()
        
        self.snake = Snake()
        self.enemies = []
        self.blocks_coords_list = []
        
        if 1 <= self.level <= 3:
            block_count = 0
            enemy_count = 0
        elif 4 <= self.level <= 7:
            block_count = 0
            enemy_count = 1 + (self.level - 4)
        else:
            block_count = 4 + (self.level - 8) * 3
            enemy_count = 2 + (self.level - 8)

        self.blocks = ObstacleBlock(self.canvas, self.snake.coordinates, count=block_count)
        self.blocks_coords_list = self.blocks.coordinates if hasattr(self.blocks, 'coordinates') else []
        
        for _ in range(enemy_count):
            self.enemies.append(MovingEnemy(self.canvas, self.snake.coordinates, self.blocks_coords_list))
            
        self.food = Food(self.canvas, self.snake.coordinates, self.blocks_coords_list)
        self.snake.draw(self.canvas, self.direction)
        self.current_speed = max(35, self.base_speed - (self.level * 6))

    def start_loop(self):
        """Safely initiates or overwrites the turn loop execution stack."""
        if self._loop_id:
            self.window.after_cancel(self._loop_id)
        self._loop_id = self.window.after(self.current_speed, self.next_turn)

    def next_turn(self) -> None:
        if self.paused or self.game_is_over or self.intermission_active:
            self._loop_id = self.window.after(30, self.next_turn)
            return

        self.direction_lock = False  # Reset lock at the frame execution step

        for enemy in self.enemies:
            enemy.patrol_step()

        x, y = self.snake.coordinates[0]
        if self.direction == "up": y -= GRID_SIZE
        elif self.direction == "down": y += GRID_SIZE
        elif self.direction == "left": x -= GRID_SIZE
        elif self.direction == "right": x += GRID_SIZE

        self.snake.coordinates.insert(0, [x, y])
        
        # Redraw enhanced snake configuration components
        self.canvas.delete("snake")
        self.snake.squares = []
        self.snake.draw(self.canvas, self.direction)

        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.level_progress += 1
            self.score_box.config(text=f"SCORE\n{self.score:03d}")
            self.canvas.delete("food")
            
            if self.level_progress >= FOOD_PER_LEVEL:
                if self.level >= MAX_LEVEL:
                    self.game_victory()
                    return
                else:
                    self.trigger_level_intermission_prompt()
            else:
                self.progress_label.config(text=f"NEXT LINK: {self.level_progress}/{FOOD_PER_LEVEL}")
                self.food = Food(self.canvas, self.snake.coordinates, self.blocks_coords_list)
        else:
            del self.snake.coordinates[-1]
            if self.snake.squares:
                self.canvas.delete(self.snake.squares[-1])
                del self.snake.squares[-1]

        if self.check_collisions():
            self.game_over()
        else:
            self._loop_id = self.window.after(self.current_speed, self.next_turn)

    def trigger_level_intermission_prompt(self):
        self.intermission_active = True
        cx = self.canvas.winfo_width() / 2
        cy = self.canvas.winfo_height() / 2

        self.canvas.create_rectangle(cx - 240, cy - 120, cx + 240, cy + 120, 
                                     fill="#0B0B18", outline=SNAKE_HEAD_COLOR, width=2, tag="int_menu")
        
        self.canvas.create_text(cx, cy - 60, font=("Courier New", 20, "bold"), 
                                text=f"SECTOR {self.level:02d} SECURED", fill="#00FF66", tag="int_menu")
        
        self.canvas.create_text(cx, cy - 15, font=("Courier New", 12), 
                                text="Initialize next database sector link?", fill="#FFFFFF", tag="int_menu")

        self.continue_btn = tk.Button(
            self.window, text="CONTINUE SIMULATION", font=("Courier New", 11, "bold"),
            bg="#00A8FF", fg="#FFFFFF", activebackground="#00558F", activeforeground="#FFFFFF",
            bd=0, padx=20, pady=8, cursor="hand2", command=self.confirm_next_level
        )
        self.canvas.create_window(cx, cy + 50, window=self.continue_btn, tag="int_menu")

    def confirm_next_level(self):
        if hasattr(self, 'continue_btn') and self.continue_btn.winfo_exists():
            self.continue_btn.destroy()
        self.canvas.delete("int_menu")
        
        self.completed_history.append(self.level)
        self.level += 1
        self.level_progress = 0
        
        self.level_box.config(text=f"SECTOR {self.level:02d}")
        self.progress_label.config(text=f"NEXT LINK: 0/{FOOD_PER_LEVEL}")
        
        self.setup_game_entities()
        self.intermission_active = False

    def change_direction(self, new_direction: str) -> None:
        if self.paused or self.game_is_over or self.intermission_active or self.direction_lock: 
            return
        
        opposites = {"left": "right", "right": "left", "up": "down", "down": "up"}
        if new_direction != opposites.get(self.direction):
            self.direction = new_direction
            self.direction_lock = True  # Locks updates until the current tick processes

    def toggle_pause(self) -> None:
        if self.game_is_over or self.intermission_active: return

        if not self.paused:
            self.paused = True
            self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(),
                                         fill="#050510", stipple="gray50", tag="ui_overlay")
            self.canvas.create_text(
                self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2,
                font=("Courier New", 22, "bold"), text="SYSTEM PAUSED\n\n[ Press Space to Resume ]",
                fill="#FFFFFF", justify="center", tag="ui_text"
            )
        else:
            self.paused = False
            self.canvas.delete("ui_text")
            self.canvas.delete("ui_overlay")

    def check_collisions(self) -> bool:
        x, y = self.snake.coordinates[0]
        if x < 0 or x >= self.canvas.winfo_width() or y < 0 or y >= self.canvas.winfo_height():
            self.death_reason = "OUTER WALL GRID COLLISION"
            return True
        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                self.death_reason = "PLASMA CORE SELF-INTERSECTION"
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
        self.game_is_over = True
        is_new_high = self.score > self.high_score
        if is_new_high:
            self.high_score = self.score
            self.hi_score_box.config(text=f"HI-SCORE: {self.high_score:03d}")

        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill=FOOD_COLOR, tag="flash")
        self.window.update()
        self.window.after(80, lambda: self.canvas.delete("flash"))
        self.window.after(100, lambda: self.render_diagnostic_death_screen(is_new_high))

    def render_diagnostic_death_screen(self, new_high):
        cx, cy = self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2
        self.canvas.create_rectangle(cx - 240, cy - 180, cx + 240, cy + 180, fill="#0B0B16", outline=FOOD_COLOR, width=2)
        self.canvas.create_text(cx, cy - 140, font=("Courier New", 22, "bold"), text="❌ CRITICAL CRASH ❌", fill=FOOD_COLOR)
        self.canvas.create_text(cx, cy - 80, font=("Courier New", 11, "bold"), text=f"LOG: {self.death_reason}", fill="#FF7777")
        
        stats_text = (
            f"SECTOR REACHED : {self.level:02d}\n"
            f"STAGES CLEARED : {len(self.completed_history)}\n"
            f"FINAL SCORE    : {self.score:03d}"
        )
        self.canvas.create_text(cx - 160, cy + 10, font=("Consolas", 13), text=stats_text, fill="#FFFFFF", anchor="w")

        if new_high:
            self.canvas.create_text(cx + 100, cy + 10, font=("Courier New", 11, "bold"), text="🔥 NEW RECORD 🔥", fill=SNAKE_HEAD_COLOR)

        self.canvas.create_text(cx, cy + 130, font=("Courier New", 12, "bold"), text="[ PRESS 'R' TO REBOOT ENGINE ]", fill="#8888AA")

    def game_victory(self) -> None:
        self.game_is_over = True
        cx, cy = self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2
        self.canvas.create_rectangle(cx - 240, cy - 120, cx + 240, cy + 120, fill="#0B0B16", outline=SNAKE_HEAD_COLOR, width=2)
        self.canvas.create_text(cx, cy - 40, font=("Courier New", 24, "bold"), text="ALL SECTORS SECURED", fill=SNAKE_HEAD_COLOR)
        self.canvas.create_text(cx, cy + 10, font=("Courier New", 14), text=f"FINAL OVERDRIVE SCORE: {self.score:03d}", fill="#FFFFFF")
        self.canvas.create_text(cx, cy + 70, font=("Courier New", 11, "bold"), text="[ PRESS 'R' TO RESET SIMULATION ]", fill="#8888AA")

    def restart_game(self) -> None:
        if hasattr(self, 'continue_btn') and self.continue_btn.winfo_exists():
            self.continue_btn.destroy()

        self.game_is_over = False
        self.paused = False
        self.intermission_active = False
        self.score = 0
        self.level = 1
        self.level_progress = 0
        self.completed_history = []
        self.direction = "right"
        self.direction_lock = False
        
        self.level_box.config(text="SECTOR 01")
        self.progress_label.config(text=f"NEXT LINK: 0/{FOOD_PER_LEVEL}")
        self.score_box.config(text="SCORE\n000")
        
        self.setup_game_entities()
        self.start_loop()


if __name__ == "__main__":
    NeonSnakeGame()
