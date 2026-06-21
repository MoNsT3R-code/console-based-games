import tkinter as tk
import random
import math

# --- PREMIUM DESIGN CONSTANTS ---
INITIAL_WIDTH = 920
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

# --- TRANSLATION TRANSLITERATION DATABASE ---
LOCALIZATION = {
    "en": {
        "title": "⚡ NEON OVERDRIVE ⚡",
        "sector": "SECTOR",
        "lives": "LIVES",
        "next_link": "NEXT LINK",
        "diagnostic": "DIAGNOSTIC STRENGTH",
        "tier_easy": "EASY TIER (NO HAZARDS)",
        "tier_med": "MEDIUM TIER ({} DRONES)",
        "tier_hard": "HARD TIER (MAX THREAT)",
        "engine_rate": "ENGINE RATE: {}%",
        "score_label": "SCORE",
        "hiscore_label": "HI-SCORE: {:03d}",
        "history_title": "CLEARED STAGES LOG",
        "history_none": "None (Current: S{:02d})",
        "history_cleared": "Cleared: {}\nActive: S{:02d}",
        "legend_title": " ‖ SYSTEM CONTROL MATRIX ‖ ",
        "legend_body": " [Arrows] ── Move Matrix\n [Space]  ── Pause Game\n [ [ / ] ] ── Speed Up/Down\n [R Key]  ── Reboot Engine\n [L Key]  ── Swap Language\n [H Key]  ── Help Manual\n [P Key]  ── Privacy Policy",
        "boot_title": "INITIALIZE CORE PROGRAM?",
        "boot_sub": "Press [ENTER] or click button to run simulation",
        "boot_btn": "START SIMULATION",
        "pause_title": "SYSTEM PAUSED\n\n[ Press Space to Resume ]",
        "int_title": "SECTOR {:02d} SECURED",
        "int_sub": "Initialize next database sector link?",
        "int_btn": "CONTINUE SIMULATION",
        "dismiss": "DISMISS INTERFACE",
        "feedback_ask": "DID YOU ENJOY THE NEON OVERDRIVE LOGIC?",
        "feedback_yes": "YES",
        "feedback_no": "NO",
        "feedback_thanks_yes": "SYSTEM ENCRYPTED: THANK YOU FOR THE FEEDBACK!",
        "feedback_thanks_no": "LOGGED. ENGINES WILL ADAPT FOR NEXT SYSTEM BOOT.",
        "crash_title": "❌ CRITICAL CRASH ❌",
        "crash_log": "LOG: {}",
        "stat_reached": "SECTOR REACHED : {:02d}",
        "stat_cleared": "STAGES CLEARED : {}",
        "stat_score":   "FINAL SCORE    : {:03d}",
        "new_record": "🔥 NEW RECORD 🔥",
        "reboot_prompt": "[ PRESS 'R' TO REBOOT ENGINE ]",
        "victory_title": "ALL SECTORS SECURED",
        "victory_score": "FINAL OVERDRIVE SCORE: {:03d}",
        "victory_prompt": "[ PRESS 'R' TO RESET SIMULATION ]",
        "death_wall": "OUTER WALL GRID COLLISION",
        "death_self": "PLASMA CORE SELF-INTERSECTION",
        "death_drone": "SECURITY DRONE INTERCEPT",
        "death_block": "STATIC HAZARD BLOCK IMPACT",
        "help_title": "‖ CORE ENGINE USER MANUAL ‖",
        "help_p1": "1. OBJECTIVE CONFIGURATION\nNavigate through grid sectors collecting data units (pink circles).\nSecuring 5 links opens up an uplink matrix path into next difficulty node.",
        "help_p2": "2. DEFENSIVE EVASION TACTICS\nAvoid physical contact with outermost parameters or your own tail core.\nStatic orange grid blocks and tracking drones remove stars from system life.",
        "help_p3": "3. TELEMETRY SPEED OVERRIDES\nUse the '[' bracket key to increment game loop delays (Slower Response).\nUse the ']' bracket key to compress loop ticks directly (Faster Response).",
        "priv_title": "‖ SYSTEM PRIVACY ARCHIVE ‖",
        "priv_p1": "1. DATA COLLECTION ISOLATION MATRIX\nNeon Overdrive operates locally inside your personal environment storage.\nZero external API network transfers are called; telemetry stays local.",
        "priv_p2": "2. STATE STORAGE PERSISTENCE\nHigh-scores and configuration levels populate via runtime memories only.\nNo underlying device tracking IDs, session parameters, or files are parsed.",
        "priv_p3": "3. ARCHITECTURE INTEGRITY STACK\nThis compilation leverages pure structural Python/Tkinter environments.\nNo background scripts cookies tracking files or telemetry is active."
    },
    "ur": {
        "title": "⚡ نیون اوور ڈرائیو ⚡",
        "sector": "سیکٹر",
        "lives": "زندگیاں",
        "next_link": "اگلا لنک",
        "diagnostic": "تشخیصی طاقت",
        "tier_easy": "آسان لیول (کوئی خطرہ نہیں)",
        "tier_med": "درمیانہ لیول ({} ڈرونز)",
        "tier_hard": "مشکل لیول (زیادہ سے زیادہ خطرہ)",
        "engine_rate": "انجن کی رفتار: {}%",
        "score_label": "اسکور",
        "hiscore_label": "اعلیٰ اسکور: {:03d}",
        "history_title": "صاف شدہ مراحل کا لاگ",
        "history_none": "کوئی نہیں (موجودہ: S{:02d})",
        "history_cleared": "صاف شدہ: {}\nفعال: S{:02d}",
        "legend_title": " ‖ سسٹم کنٹرول میٹرکس ‖ ",
        "legend_body": " [تیر کے نشان] ── حرکت کریں\n [Space]       ── گیم روکیں\n [ [ / ] ]     ── رفتار کم/تیز کریں\n [R کلید]      ── ریبوٹ انجن\n [L کلید]      ── زبان تبدیل کریں\n [H کلید]      ── مدد انڈیکس\n [P کلید]      ── رازداری پالیسی",
        "boot_title": "کور پروگرام شروع کریں؟",
        "boot_sub": "سیولیشن چلانے کے لیے [ENTER] دبائیں یا بٹن پر کلک کریں",
        "boot_btn": "گیم شروع کریں",
        "pause_title": "سسٹم روک دیا گیا ہے\n\n[ دوبارہ شروع کرنے کے لیے Space دبائیں ]",
        "int_title": "سیکٹر {:02d} محفوظ ہو گیا",
        "int_sub": "اگلا ڈیٹا بیس سیکٹر لنک شروع کریں؟",
        "int_btn": "گیم جاری رکھیں",
        "dismiss": "انٹرفیس بند کریں",
        "feedback_ask": "کیا آپ نیون اوور ڈرائیو لاجک سے لطف اندوز ہوئے؟",
        "feedback_yes": "ہاں",
        "feedback_no": "نہیں",
        "feedback_thanks_yes": "سسٹم انکرپٹڈ: آراء کا شکریہ!",
        "feedback_thanks_no": "محفوظ کر لیا گیا۔ انجن اگلے سسٹم بوٹ کے لیے خود کو ڈھال لے گا۔",
        "crash_title": "❌ اہم حادثہ / کریش ❌",
        "crash_log": "لاگ رپورٹ: {}",
        "stat_reached": "پہنچا ہوا سیکٹر  : {:02d}",
        "stat_cleared": "صاف کردہ مراحل : {}",
        "stat_score":   "حتمی اسکور      : {:03d}",
        "new_record": "🔥 نیا ریکارڈ 🔥",
        "reboot_prompt": "[ انجن کو دوبارہ شروع کرنے کے لیے 'R' دبائیں ]",
        "victory_title": "تمام سیکٹرز محفوظ ہو گئے",
        "victory_score": "حتمی اوور ڈرائیو اسکور: {:03d}",
        "victory_prompt": "[ تخروپن کو دوبارہ ترتیب دینے کے لیے 'R' دبائیں ]",
        "death_wall": "بیرونی دیوار گرڈ سے ٹکراؤ",
        "death_self": "پلازما کور کا اپنے آپ سے ٹکراؤ",
        "death_drone": "سیکیورٹی ڈرون کا حملہ",
        "death_block": "ساکت رکاوٹ بلاک اثر",
        "help_title": "‖ CORE ENGINE USER MANUAL ‖",
        "help_p1": "1. ہدف کی ترتیب\nگلابی دائروں (ڈیٹا یونٹس) کو جمع کرتے ہوئے گرڈ سیکٹرز میں نیویگیٹ کریں۔\n5 لنکس حاصل کرنے سے اگلے مشکل نوڈ کا راستہ کھل جاتا ہے۔",
        "help_p2": "2. دفاعی حکمت عملی\nبیرونی دیواروں یا اپنی ہی دم سے جسمانی رابطے سے گریز کریں۔\nنارنجی بلاکس اور ٹریکنگ ڈرونز سسٹم کی زندگی کو کم کرتے ہیں۔",
        "help_p3": "3. ٹیلی میٹری اسپیڈ اوور رائیڈز\nگیم لوپ تاخیر کو بڑھانے کے لیے '[' کلید استعمال کریں (آہستہ ردعمل)۔\nلوپ ٹک کو براہ راست کم کرنے کے لیے ']' کلید استعمال کریں (تیز ردعمل)۔",
        "priv_title": "‖ SYSTEM PRIVACY ARCHIVE ‖",
        "priv_p1": "1. ڈیٹا اکٹھا کرنے کی تنہائی کا میٹرکس\nنیون اوور ڈرائیو مقامی طور پر آپ کے ذاتی ماحول کے اسٹوریج میں کام کرتی ہے۔\nکوئی بیرونی API نیٹ ورک ٹرانسفر نہیں ہوتا؛ ٹیلی میٹری مقامی رہتی ہے۔",
        "priv_p2": "2. اسٹیٹ اسٹوریج کا تسلسل\nاعلی اسکور اور ترتیب کی سطحیں صرف رن ٹائم میموری کے ذریعے آباد ہوتی ہیں۔\nکسی ڈیوائس ٹریکنگ آئی ڈی یا سیشن پیرامیٹرز کو پارس نہیں کیا جاتا۔",
        "priv_p3": "3. آرکیٹیکچر کی سالمیت کا اسٹیک\nیہ تالیف خالص ساختی پائتھن/ٹکنٹر ماحول کا فائدہ استحصال کرتی ہے۔\nکوئی پس منظر کے اسکرپٹ کوکیز ٹریکنگ فائلیں یا ٹیلی میٹری فعال نہیں ہے۔"
    }
}


class Snake:
    def __init__(self):
        self.coordinates = []
        self.squares = []
        self.reset_position()

    def reset_position(self):
        self.coordinates = []
        for i in range(4):
            self.coordinates.append([GRID_SIZE * (5 - i), GRID_SIZE * 8])

    def draw(self, canvas, direction="right"):
        """Draws a premium, tapered plasma-thread snake body with structural details."""
        for idx, (x, y) in enumerate(self.coordinates):
            taper = max(1, min(6, idx))
            
            if idx == 0:
                color = SNAKE_HEAD_COLOR
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
        c_width = canvas.winfo_width() if canvas.winfo_width() > 10 else INITIAL_WIDTH - 250
        c_height = canvas.winfo_height() if canvas.winfo_height() > 10 else INITIAL_HEIGHT
        max_x = max(1, int(c_width / GRID_SIZE) - 1)
        max_y = max(1, int(c_height / GRID_SIZE) - 1)
        
        attempts = 0
        while attempts < 1000:
            x = random.randint(0, max_x) * GRID_SIZE
            y = random.randint(0, max_y) * GRID_SIZE
            if [x, y] not in snake_coords and [x, y] not in block_coords:
                break
            attempts += 1

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

        c_width = canvas.winfo_width() if canvas.winfo_width() > 10 else INITIAL_WIDTH - 250
        c_height = canvas.winfo_height() if canvas.winfo_height() > 10 else INITIAL_HEIGHT
        max_x = max(1, int(c_width / GRID_SIZE) - 1)
        max_y = max(1, int(c_height / GRID_SIZE) - 1)

        for _ in range(count):
            attempts = 0
            while attempts < 100:
                x = random.randint(0, max_x) * GRID_SIZE
                y = random.randint(0, max_y) * GRID_SIZE
                if [x, y] not in snake_coords and x > GRID_SIZE * 7 and [x, y] not in self.coordinates:
                    self.coordinates.append([x, y])
                    block = canvas.create_rectangle(
                        x + 3, y + 3, x + GRID_SIZE - 3, y + GRID_SIZE - 3,
                        fill=BLOCK_COLOR, outline="#FF5500", width=1, tag="block"
                    )
                    self.items.append(block)
                    break
                attempts += 1


class MovingEnemy:
    def __init__(self, canvas, snake_coords, block_coords):
        self.canvas = canvas
        c_width = canvas.winfo_width() if canvas.winfo_width() > 10 else INITIAL_WIDTH - 250
        c_height = canvas.winfo_height() if canvas.winfo_height() > 10 else INITIAL_HEIGHT
        self.max_x = max(1, int(c_width / GRID_SIZE) - 1) * GRID_SIZE
        self.max_y = max(1, int(c_height / GRID_SIZE) - 1) * GRID_SIZE

        attempts = 0
        while attempts < 1000:
            x = random.randint(2, int(self.max_x / GRID_SIZE) - 2) * GRID_SIZE
            y = random.randint(2, int(self.max_y / GRID_SIZE) - 2) * GRID_SIZE
            if [x, y] not in snake_coords and [x, y] not in block_coords:
                break
            attempts += 1

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

        # Base engine stats
        self.lang = "en"  
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.lives = 3
        self.level_progress = 0  
        self.completed_history = []
        
        self.base_speed = 110
        self.manual_speed_offset = 0  
        self.current_speed = self.base_speed
        
        self.direction = "right"
        self.direction_lock = False  
        self.paused = False
        self.game_is_over = False
        self.intermission_active = False
        self.engine_booted = False    
        self.info_overlay_active = False
        self.death_reason_key = "death_wall" 
        self._loop_id = None 
        
        self.enemies = []
        self.blocks_coords_list = []
        self.feedback_buttons = []

        # --- UI LAYOUT ASSEMBLY ---
        self.main_container = tk.Frame(self.window, bg=BG_COLOR)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.main_container, bg=SIDEBAR_BG, width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.title_label = tk.Label(self.sidebar, text="", font=("Courier New", 12, "bold"), fg=SNAKE_HEAD_COLOR, bg=SIDEBAR_BG)
        self.title_label.pack(pady=10)
        
        self.lang_btn = tk.Button(
            self.sidebar, text="اردو (Urdu)", font=("Helvetica", 9, "bold"),
            bg="#1A1A2E", fg=SNAKE_HEAD_COLOR, activebackground=SNAKE_HEAD_COLOR, activeforeground="#0A0A12",
            bd=1, relief="groove", padx=10, pady=3, cursor="hand2", command=self.toggle_language
        )
        self.lang_btn.pack(pady=(0, 10))

        self.level_box = tk.Label(self.sidebar, text="", font=("Courier New", 16, "bold"), fg=SNAKE_HEAD_COLOR, bg=SIDEBAR_BG)
        self.level_box.pack(pady=2)
        
        self.lives_label = tk.Label(self.sidebar, text="", font=("Courier New", 11, "bold"), fg="#FF007F", bg=SIDEBAR_BG)
        self.lives_label.pack(pady=2)

        self.progress_label = tk.Label(self.sidebar, text="", font=("Helvetica", 9), fg="#8888AA", bg=SIDEBAR_BG)
        self.progress_label.pack(pady=2)

        self.tier_title = tk.Label(self.sidebar, text="", font=("Courier New", 8, "bold"), fg="#555575", bg=SIDEBAR_BG)
        self.tier_title.pack(pady=(10, 0))
        self.tier_status = tk.Label(self.sidebar, text="", font=("Courier New", 9, "bold"), fg="#00FF66", bg=SIDEBAR_BG)
        self.tier_status.pack(pady=2)

        self.speed_metrics_box = tk.Label(self.sidebar, text="", font=("Courier New", 9, "bold"), fg=SNAKE_HEAD_COLOR, bg=SIDEBAR_BG)
        self.speed_metrics_box.pack(pady=5)

        self.score_box = tk.Label(self.sidebar, text="", font=("Consolas", 14, "bold"), fg="#FFFFFF", bg="#1A1A2E", bd=4, relief="flat", width=16)
        self.score_box.pack(pady=10)
        self.hi_score_box = tk.Label(self.sidebar, text="", font=("Consolas", 11), fg="#656585", bg=SIDEBAR_BG)
        self.hi_score_box.pack(pady=2)

        self.history_title_label = tk.Label(self.sidebar, text="", font=("Courier New", 8, "bold"), fg="#555575", bg=SIDEBAR_BG)
        self.history_title_label.pack(pady=(10, 0))
        self.history_box = tk.Label(self.sidebar, text="", font=("Courier New", 9), fg="#757595", bg=SIDEBAR_BG, justify=tk.LEFT)
        self.history_box.pack(pady=2)

        # --- NEW HIGH-PROMINENCE LEGEND PANEL ---
        self.legend_frame = tk.LabelFrame(
            self.sidebar, text="", font=("Courier New", 8, "bold"), 
            bg="#1A1A2E", fg=SNAKE_HEAD_COLOR, bd=1, relief="solid", padx=8, pady=8
        )
        self.legend_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=15)

        self.legend_title_lbl = tk.Label(self.legend_frame, text="", font=("Courier New", 8, "bold"), fg=SNAKE_HEAD_COLOR, bg="#1A1A2E")
        self.legend_title_lbl.pack(anchor="w", pady=(0, 5))

        self.legend_body_lbl = tk.Label(self.legend_frame, text="", font=("Courier New", 8), fg="#A9A9C9", bg="#1A1A2E", justify=tk.LEFT)
        self.legend_body_lbl.pack(anchor="w")

        self.canvas = tk.Canvas(self.main_container, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # KEY BINDINGS MATRIX
        self.window.bind("<Left>", lambda e: self.change_direction("left"))
        self.window.bind("<Right>", lambda e: self.change_direction("right"))
        self.window.bind("<Up>", lambda e: self.change_direction("up"))
        self.window.bind("<Down>", lambda e: self.change_direction("down"))
        self.window.bind("<space>", lambda e: self.toggle_pause())
        self.window.bind("<r>", lambda e: self.restart_game())
        self.window.bind("<R>", lambda e: self.restart_game())
        self.window.bind("<l>", lambda e: self.toggle_language())
        self.window.bind("<L>", lambda e: self.toggle_language())
        
        self.window.bind("<bracketleft>", lambda e: self.adjust_speed(15))   
        self.window.bind("<bracketright>", lambda e: self.adjust_speed(-15)) 
        self.window.bind("<Return>", lambda e: self.trigger_boot_sequence())
        
        self.window.bind("<h>", lambda e: self.show_help_overlay())
        self.window.bind("<H>", lambda e: self.show_help_overlay())
        self.window.bind("<p>", lambda e: self.show_privacy_overlay())
        self.window.bind("<P>", lambda e: self.show_privacy_overlay())

        self.canvas.bind("<Configure>", lambda e: self.draw_background_matrix())

        self.window.update()
        self.initial_centering(920, INITIAL_HEIGHT)
        
        self.setup_game_entities()
        self.refresh_ui_text()
        self.ask_user_to_start()  
        self.window.mainloop()

    def initial_centering(self, w, h):
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry(f"{w}x{h}+{int((sw-w)/2)}+{int((sh-h)/2)}")

    def toggle_language(self):
        self.lang = "ur" if self.lang == "en" else "en"
        self.lang_btn.config(text="English" if self.lang == "ur" else "اردو (Urdu)")
        self.refresh_ui_text()
        
        if not self.engine_booted:
            self.canvas.delete("boot_screen")
            self.ask_user_to_start()
        elif self.intermission_active:
            if hasattr(self, 'continue_btn') and self.continue_btn.winfo_exists():
                self.continue_btn.destroy()
            self.canvas.delete("int_menu")
            self.trigger_level_intermission_prompt()
        elif self.game_is_over:
            self.canvas.delete("all")
            self.draw_background_matrix()
            is_new_high = self.score >= self.high_score
            self.render_diagnostic_death_screen(is_new_high)

    def refresh_ui_text(self):
        ctx = LOCALIZATION[self.lang]
        
        self.title_label.config(text=ctx["title"])
        self.level_box.config(text=f"{ctx['sector']} {self.level:02d}")
        self.lives_label.config(text=f"{ctx['lives']}: {'⭐' * self.lives}")
        self.progress_label.config(text=f"{ctx['next_link']}: {self.level_progress}/{FOOD_PER_LEVEL}")
        self.tier_title.config(text=ctx["diagnostic"])
        
        if 1 <= self.level <= 3:
            self.level_box.config(fg=SNAKE_HEAD_COLOR)
            self.tier_status.config(text=ctx["tier_easy"], fg="#00FF66")
        elif 4 <= self.level <= 7:
            self.level_box.config(fg=ENEMY_COLOR)
            self.tier_status.config(text=ctx["tier_med"].format(len(self.enemies)), fg="#CCAA00")
        else:
            self.level_box.config(fg=BLOCK_COLOR)
            self.tier_status.config(text=ctx["tier_hard"], fg="#FF3333")

        percentage = int((self.base_speed / max(1, self.current_speed)) * 100)
        self.speed_metrics_box.config(text=ctx["engine_rate"].format(percentage))
        
        self.score_box.config(text=f"{ctx['score_label']}\n{self.score:03d}")
        self.hi_score_box.config(text=ctx["hiscore_label"].format(self.high_score))
        self.history_title_label.config(text=ctx["history_title"])

        if self.completed_history:
            history_text = ", ".join([f"S{lvl:02d}" for lvl in self.completed_history])
            if len(self.completed_history) > 3:
                history_text = "..." + ", ".join([f"S{lvl:02d}" for lvl in self.completed_history[-3:]])
            self.history_box.config(text=ctx["history_cleared"].format(history_text, self.level))
        else:
            self.history_box.config(text=ctx["history_none"].format(self.level))

        # Core Grid Control updates
        self.legend_title_lbl.config(text=ctx["legend_title"])
        self.legend_body_lbl.config(text=ctx["legend_body"])

    def draw_background_matrix(self):
        self.canvas.delete("grid_line")
        w = self.canvas.winfo_width() if self.canvas.winfo_width() > 10 else INITIAL_WIDTH - 250
        h = self.canvas.winfo_height() if self.canvas.winfo_height() > 10 else INITIAL_HEIGHT
        for x in range(0, w, GRID_SIZE):
            self.canvas.create_line(x, 0, x, h, fill=GRID_COLOR, tag="grid_line")
        for y in range(0, h, GRID_SIZE):
            self.canvas.create_line(0, y, w, y, fill=GRID_COLOR, tag="grid_line")
        self.canvas.tag_lower("grid_line")

    def ask_user_to_start(self):
        self.engine_booted = False
        ctx = LOCALIZATION[self.lang]
        c_width = self.canvas.winfo_width() if self.canvas.winfo_width() > 10 else INITIAL_WIDTH - 250
        c_height = self.canvas.winfo_height() if self.canvas.winfo_height() > 10 else INITIAL_HEIGHT
        cx, cy = c_width / 2, c_height / 2

        self.canvas.create_rectangle(cx - 260, cy - 110, cx + 260, cy + 110, 
                                     fill="#0B0B18", outline=SNAKE_HEAD_COLOR, width=2, tag="boot_screen")
        
        self.canvas.create_text(cx, cy - 50, font=("Courier New", 16, "bold"), 
                                text=ctx["boot_title"], fill="#FFFFFF", tag="boot_screen")
        
        self.canvas.create_text(cx, cy - 10, font=("Helvetica", 10), 
                                text=ctx["boot_sub"], fill="#8888AA", tag="boot_screen")

        self.boot_btn = tk.Button(
            self.window, text=ctx["boot_btn"], font=("Helvetica", 11, "bold"),
            bg="#00FF66", fg="#0A0A12", activebackground=SNAKE_HEAD_COLOR, activeforeground="#0A0A12",
            bd=0, padx=25, pady=8, cursor="hand2", command=self.trigger_boot_sequence
        )
        self.canvas.create_window(cx, cy + 45, window=self.boot_btn, tag="boot_screen")

    def trigger_boot_sequence(self):
        if self.engine_booted or self.info_overlay_active: return
        if hasattr(self, 'boot_btn') and self.boot_btn.winfo_exists():
            self.boot_btn.destroy()
        self.canvas.delete("boot_screen")
        self.engine_booted = True
        self.start_loop()

    def adjust_speed(self, change: int):
        self.manual_speed_offset += change
        self.recalculate_current_speed()
        self.refresh_ui_text()

    def recalculate_current_speed(self):
        calc = (self.base_speed - (self.level * 6)) + self.manual_speed_offset
        self.current_speed = max(25, min(300, calc))

    def setup_game_entities(self):
        self.canvas.delete("all")
        self.draw_background_matrix()
        
        self.snake = Snake()
        self.enemies = []
        self.blocks_coords_list = []
        
        if self.level == 5:
            enemy_count = 2; block_count = 3
        elif self.level == 6:
            enemy_count = 4; block_count = 5
        elif 1 <= self.level <= 3:
            enemy_count = 0; block_count = 0
        elif self.level == 4:
            enemy_count = 1; block_count = 1
        elif self.level == 7:
            enemy_count = 5; block_count = 6
        else: 
            enemy_count = 5 + (self.level - 8)
            block_count = min(25, 10 + (self.level - 8) * 3) 

        self.blocks = ObstacleBlock(self.canvas, self.snake.coordinates, count=block_count)
        self.blocks_coords_list = self.blocks.coordinates if hasattr(self.blocks, 'coordinates') else []
        
        for _ in range(enemy_count):
            self.enemies.append(MovingEnemy(self.canvas, self.snake.coordinates, self.blocks_coords_list))
            
        self.food = Food(self.canvas, self.snake.coordinates, self.blocks_coords_list)
        self.snake.draw(self.canvas, self.direction)
        
        self.recalculate_current_speed()

    def start_loop(self):
        if not self.engine_booted: return
        if self._loop_id:
            self.window.after_cancel(self._loop_id)
        self._loop_id = self.window.after(self.current_speed, self.next_turn)

    def next_turn(self) -> None:
        if self.paused or self.game_is_over or self.intermission_active or not self.engine_booted or self.info_overlay_active:
            self._loop_id = self.window.after(30, self.next_turn)
            return

        self.direction_lock = False  
        for enemy in self.enemies:
            enemy.patrol_step()

        x, y = self.snake.coordinates[0]
        if self.direction == "up": y -= GRID_SIZE
        elif self.direction == "down": y += GRID_SIZE
        elif self.direction == "left": x -= GRID_SIZE
        elif self.direction == "right": x += GRID_SIZE

        self.snake.coordinates.insert(0, [x, y])
        self.canvas.delete("snake")
        self.snake.squares = []
        self.snake.draw(self.canvas, self.direction)

        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.level_progress += 1
            self.refresh_ui_text()
            self.canvas.delete("food")
            
            if self.level_progress >= FOOD_PER_LEVEL:
                if self.level >= MAX_LEVEL:
                    self.game_victory()
                    return
                else:
                    self.trigger_level_intermission_prompt()
            else:
                self.food = Food(self.canvas, self.snake.coordinates, self.blocks_coords_list)
        else:
            del self.snake.coordinates[-1]
            if self.snake.squares:
                self.canvas.delete(self.snake.squares[-1])
                del self.snake.squares[-1]

        collision_state = self.check_collisions()
        if collision_state:
            self.handle_life_loss()
        else:
            self._loop_id = self.window.after(self.current_speed, self.next_turn)

    def handle_life_loss(self):
        self.lives -= 1
        self.refresh_ui_text()
        
        flash_color = "#FF5500" if self.death_reason_key in ["death_block", "death_drone"] else "#FF0033"
        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width() if self.canvas.winfo_width() > 10 else INITIAL_WIDTH-250, 
                                     self.canvas.winfo_height() if self.canvas.winfo_height() > 10 else INITIAL_HEIGHT, 
                                     fill=flash_color, tag="flash")
        self.window.update()
        self.window.after(70, lambda: self.canvas.delete("flash"))

        if self.lives <= 0:
            self.game_over()
        else:
            self.snake.reset_position()
            self.direction = "right"
            self.canvas.delete("snake")
            self.snake.squares = []
            self.snake.draw(self.canvas, self.direction)
            self._loop_id = self.window.after(self.current_speed, self.next_turn)

    def trigger_level_intermission_prompt(self):
        self.intermission_active = True
        ctx = LOCALIZATION[self.lang]
        cx = (self.canvas.winfo_width() / 2) if self.canvas.winfo_width() > 10 else (INITIAL_WIDTH - 250) / 2
        cy = (self.canvas.winfo_height() / 2) if self.canvas.winfo_height() > 10 else INITIAL_HEIGHT / 2

        self.canvas.create_rectangle(cx - 240, cy - 120, cx + 240, cy + 120, 
                                     fill="#0B0B18", outline=SNAKE_HEAD_COLOR, width=2, tag="int_menu")
        
        self.canvas.create_text(cx, cy - 60, font=("Helvetica", 18, "bold"), 
                                text=ctx["int_title"].format(self.level), fill="#00FF66", tag="int_menu")
        
        self.canvas.create_text(cx, cy - 15, font=("Helvetica", 11), 
                                text=ctx["int_sub"], fill="#FFFFFF", tag="int_menu")

        self.continue_btn = tk.Button(
            self.window, text=ctx["int_btn"], font=("Helvetica", 10, "bold"),
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
        
        self.setup_game_entities()
        self.refresh_ui_text()
        self.intermission_active = False

    def change_direction(self, new_direction: str) -> None:
        if self.paused or self.game_is_over or self.intermission_active or self.direction_lock or not self.engine_booted or self.info_overlay_active: 
            return
        
        opposites = {"left": "right", "right": "left", "up": "down", "down": "up"}
        if new_direction != opposites.get(self.direction):
            self.direction = new_direction
            self.direction_lock = True  

    def toggle_pause(self) -> None:
        if self.game_is_over or self.intermission_active or not self.engine_booted or self.info_overlay_active: return
        ctx = LOCALIZATION[self.lang]
        cx = (self.canvas.winfo_width() / 2) if self.canvas.winfo_width() > 10 else (INITIAL_WIDTH - 250) / 2
        cy = (self.canvas.winfo_height() / 2) if self.canvas.winfo_height() > 10 else INITIAL_HEIGHT / 2

        if not self.paused:
            self.paused = True
            self.canvas.create_rectangle(0, 0, self.canvas.winfo_width() if self.canvas.winfo_width() > 10 else INITIAL_WIDTH - 250, 
                                         self.canvas.winfo_height() if self.canvas.winfo_height() > 10 else INITIAL_HEIGHT,
                                         fill="#050510", stipple="gray50", tag="ui_overlay")
            self.canvas.create_text(
                cx, cy, font=("Helvetica", 18, "bold"), text=ctx["pause_title"],
                fill="#FFFFFF", justify="center", tag="ui_text"
            )
        else:
            self.paused = False
            self.canvas.delete("ui_text")
            self.canvas.delete("ui_overlay")

    def create_info_panel(self, title, paragraphs):
        if self.game_is_over: return
        self.close_info_panel()
        self.info_overlay_active = True
        ctx = LOCALIZATION[self.lang]
        
        cx = (self.canvas.winfo_width() / 2) if self.canvas.winfo_width() > 10 else (INITIAL_WIDTH - 250) / 2
        cy = (self.canvas.winfo_height() / 2) if self.canvas.winfo_height() > 10 else INITIAL_HEIGHT / 2
        
        self.canvas.create_rectangle(cx - 280, cy - 210, cx + 280, cy + 210, fill="#07070F", outline=SNAKE_HEAD_COLOR, width=2, tag="info_panel")
        self.canvas.create_text(cx, cy - 175, font=("Helvetica", 14, "bold"), text=title, fill=SNAKE_HEAD_COLOR, tag="info_panel")
        
        text_y_cursor = cy - 120
        for para in paragraphs:
            self.canvas.create_text(cx, text_y_cursor, font=("Helvetica", 9), text=para, fill="#BBBCDC", justify=tk.CENTER, tag="info_panel")
            text_y_cursor += 65
            
        self.info_close_btn = tk.Button(
            self.window, text=ctx["dismiss"], font=("Helvetica", 9, "bold"),
            bg="#FF007F", fg="#FFFFFF", activebackground="#A020F0", activeforeground="#FFFFFF",
            bd=0, padx=20, pady=6, cursor="hand2", command=self.close_info_panel
        )
        self.canvas.create_window(cx, cy + 175, window=self.info_close_btn, tag="info_panel")

    def close_info_panel(self):
        if hasattr(self, 'info_close_btn') and self.info_close_btn.winfo_exists():
            self.info_close_btn.destroy()
        self.canvas.delete("info_panel")
        self.info_overlay_active = False

    def show_help_overlay(self):
        ctx = LOCALIZATION[self.lang]
        self.create_info_panel(ctx["help_title"], [ctx["help_p1"], ctx["help_p2"], ctx["help_p3"]])

    def show_privacy_overlay(self):
        ctx = LOCALIZATION[self.lang]
        self.create_info_panel(ctx["priv_title"], [ctx["priv_p1"], ctx["priv_p2"], ctx["priv_p3"]])

    def check_collisions(self):
        x, y = self.snake.coordinates[0]
        c_width = self.canvas.winfo_width() if self.canvas.winfo_width() > 10 else INITIAL_WIDTH - 250
        c_height = self.canvas.winfo_height() if self.canvas.winfo_height() > 10 else INITIAL_HEIGHT
        
        if x < 0 or x >= c_width or y < 0 or y >= c_height:
            self.death_reason_key = "death_wall"
            return "hit"
        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                self.death_reason_key = "death_self"
                return "hit"
        for enemy in self.enemies:
            if x == enemy.coordinates[0] and y == enemy.coordinates[1]:
                self.death_reason_key = "death_drone"
                return "hit"
        if [x, y] in self.blocks_coords_list:
            self.death_reason_key = "death_block"
            return "hit"
        return None

    def display_feedback_prompt(self, cx, cy):
        ctx = LOCALIZATION[self.lang]
        self.canvas.create_text(cx, cy + 55, font=("Helvetica", 10, "bold"), text=ctx["feedback_ask"], fill="#FFFF00", tag="feedback_ui")
        
        def log_feedback(liked):
            self.canvas.delete("feedback_ui")
            for btn in self.feedback_buttons:
                if btn.winfo_exists(): btn.destroy()
            self.feedback_buttons.clear()
            
            thanks = ctx["feedback_thanks_yes"] if liked else ctx["feedback_thanks_no"]
            self.canvas.create_text(cx, cy + 75, font=("Helvetica", 9, "italic"), text=thanks, fill=SNAKE_HEAD_COLOR, tag="feedback_ui")

        yes_btn = tk.Button(self.window, text=ctx["feedback_yes"], font=("Helvetica", 9, "bold"), bg="#00FF66", fg="#000", bd=0, padx=15, command=lambda: log_feedback(True))
        no_btn = tk.Button(self.window, text=ctx["feedback_no"], font=("Helvetica", 9, "bold"), bg="#FF007F", fg="#FFF", bd=0, padx=15, command=lambda: log_feedback(False))
        
        self.feedback_buttons.append(yes_btn)
        self.feedback_buttons.append(no_btn)
        
        self.canvas.create_window(cx - 50, cy + 95, window=yes_btn, tag="feedback_ui")
        self.canvas.create_window(cx + 50, cy + 95, window=no_btn, tag="feedback_ui")

    def game_over(self) -> None:
        self.game_is_over = True
        is_new_high = self.score > self.high_score
        if is_new_high:
            self.high_score = self.score
        
        self.refresh_ui_text()
        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width() if self.canvas.winfo_width() > 10 else INITIAL_WIDTH - 250, 
                                     self.canvas.winfo_height() if self.canvas.winfo_height() > 10 else INITIAL_HEIGHT, 
                                     fill=FOOD_COLOR, tag="flash")
        self.window.update()
        self.window.after(80, lambda: self.canvas.delete("flash"))
        self.window.after(100, lambda: self.render_diagnostic_death_screen(is_new_high))

    def render_diagnostic_death_screen(self, new_high):
        self.close_info_panel()
        ctx = LOCALIZATION[self.lang]
        cx = (self.canvas.winfo_width() / 2) if self.canvas.winfo_width() > 10 else (INITIAL_WIDTH - 250) / 2
        cy = (self.canvas.winfo_height() / 2) if self.canvas.winfo_height() > 10 else INITIAL_HEIGHT / 2
        
        self.canvas.create_rectangle(cx - 240, cy - 180, cx + 240, cy + 180, fill="#0B0B16", outline=FOOD_COLOR, width=2)
        self.canvas.create_text(cx, cy - 140, font=("Helvetica", 18, "bold"), text=ctx["crash_title"], fill=FOOD_COLOR)
        
        translated_reason = ctx[self.death_reason_key]
        self.canvas.create_text(cx, cy - 100, font=("Helvetica", 11, "bold"), text=ctx["crash_log"].format(translated_reason), fill="#FF7777")
        
        stats_text = (
            f"{ctx['stat_reached'].format(self.level)}\n"
            f"{ctx['stat_cleared'].format(len(self.completed_history))}\n"
            f"{ctx['stat_score'].format(self.score)}"
        )
        self.canvas.create_text(cx - 140, cy - 20, font=("Courier New", 12, "bold"), text=stats_text, fill="#FFFFFF", anchor="w")

        if new_high:
            self.canvas.create_text(cx + 100, cy - 20, font=("Helvetica", 11, "bold"), text=ctx["new_record"], fill=SNAKE_HEAD_COLOR)

        self.display_feedback_prompt(cx, cy)
        self.canvas.create_text(cx, cy + 145, font=("Helvetica", 10, "bold"), text=ctx["reboot_prompt"], fill="#8888AA")

    def game_victory(self) -> None:
        self.game_is_over = True
        self.close_info_panel()
        ctx = LOCALIZATION[self.lang]
        cx = (self.canvas.winfo_width() / 2) if self.canvas.winfo_width() > 10 else (INITIAL_WIDTH - 250) / 2
        cy = (self.canvas.winfo_height() / 2) if self.canvas.winfo_height() > 10 else INITIAL_HEIGHT / 2
        
        self.canvas.create_rectangle(cx - 240, cy - 150, cx + 240, cy + 150, fill="#0B0B16", outline=SNAKE_HEAD_COLOR, width=2)
        self.canvas.create_text(cx, cy - 90, font=("Helvetica", 20, "bold"), text=ctx["victory_title"], fill=SNAKE_HEAD_COLOR)
        self.canvas.create_text(cx, cy - 40, font=("Helvetica", 12), text=ctx["victory_score"].format(self.score), fill="#FFFFFF")
        
        self.display_feedback_prompt(cx, cy - 5)
        self.canvas.create_text(cx, cy + 110, font=("Helvetica", 10, "bold"), text=ctx["victory_prompt"], fill="#8888AA")

    def restart_game(self) -> None:
        if self._loop_id:
            self.window.after_cancel(self._loop_id)
            self._loop_id = None

        if hasattr(self, 'continue_btn') and self.continue_btn.winfo_exists():
            self.continue_btn.destroy()
        if hasattr(self, 'boot_btn') and self.boot_btn.winfo_exists():
            self.boot_btn.destroy()
        for btn in self.feedback_buttons:
            if btn.winfo_exists(): btn.destroy()
        self.feedback_buttons.clear()
        
        self.close_info_panel()

        self.game_is_over = False
        self.paused = False
        self.intermission_active = False
        self.score = 0
        self.level = 1
        self.lives = 3
        self.level_progress = 0
        self.manual_speed_offset = 0
        self.completed_history = []
        self.direction = "right"
        self.direction_lock = False
        
        self.setup_game_entities()
        self.refresh_ui_text()
        self.ask_user_to_start()  


if __name__ == "__main__":
    NeonSnakeGame()
