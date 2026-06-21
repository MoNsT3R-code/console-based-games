import tkinter as tk
import random
import string
import json
import os
from tkinter import messagebox

# --- PALETTE MATRIX CONFIGURATIONS ---
THEMES = {
    "CYBER_PINK": {"bg": "#0A0A12", "sidebar": "#12121F", "panel": "#1A1A2E", "glow": "#00F0FF", "highlight": "#A020F0", "found": "#FF007F", "text": "#FFFFFF"},
    "EMERALD": {"bg": "#050F0A", "sidebar": "#0B1A12", "panel": "#12261B", "glow": "#00FF66", "highlight": "#1E5A38", "found": "#A3FF00", "text": "#E0FFE0"},
    "RETRO_AMBER": {"bg": "#100B00", "sidebar": "#1A1200", "panel": "#2B1E00", "glow": "#FFB000", "highlight": "#664600", "found": "#FF5500", "text": "#FFE0B2"},
    "DEEP_COBALT": {"bg": "#020813", "sidebar": "#061324", "panel": "#0C233F", "glow": "#38B6FF", "highlight": "#1D4ED8", "found": "#00F0FF", "text": "#E2F1FF"}
}
THEME_KEYS = list(THEMES.keys())
TEXT_MUTED = "#757595"
SAVE_FILE = "save_state.json"

DICTIONARY_POOL = [
    "SNAKE", "DRONE", "GRID", "NEON", "MATRIX", "ENGINE", 
    "URDU", "LIVES", "VECTOR", "PLASMA", "TACTICAL", "CANVAS",
    "UPLINK", "BUFFER", "CYBER", "OVERDRIVE", "KERNEL", "PROXY"
]

class UltimateWordSearchEngine:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("⚡ NEON OVERDRIVE: ULTIMATE DECRYPTER ⚡")
        self.window.geometry("1150x720")
        self.window.resizable(False, False)
        
        # Core State Machine Registers
        self.theme_index = 0
        self.current_theme = THEMES[THEME_KEYS[self.theme_index]]
        self.window.configure(bg=self.current_theme["bg"])
        
        self.level = 1
        self.score = 0
        self.total_score = 0
        self.time_left = 120
        self.paused = False
        self.game_active = False
        self.is_maximized = False
        
        self.word_bank = []
        self.found_words = set()
        self.selected_coords = []
        self.word_positions = {}
        self.grid_buttons = []

        # System Architecture Builders
        self.setup_layout_panels()
        self.intercept_window_shutdown()
        
        # Verification Pipeline: Automatically reload persistent sector data if it exists
        self.evaluate_save_handshake_on_boot()
        
        self.execute_clock_tick()
        self.window.mainloop()

    def setup_layout_panels(self):
        th = self.current_theme
        
        # Dual-Panel Core Grid Architecture
        self.sidebar = tk.Frame(self.window, bg=th["sidebar"], width=330)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        self.viewport = tk.Frame(self.window, bg=th["bg"])
        self.viewport.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Optimization Control Grid Banner
        self.window_ctrl_bar = tk.Frame(self.sidebar, bg=th["panel"], height=35)
        self.window_ctrl_bar.pack(fill=tk.X, side=tk.TOP)
        self.window_ctrl_bar.pack_propagate(False)

        tk.Button(self.window_ctrl_bar, text="✕", font=("Arial", 11, "bold"), bg="#D90429", fg="#FFFFFF", bd=0, cursor="hand2", width=4, command=self.safely_terminate_application).pack(side=tk.RIGHT)
        tk.Button(self.window_ctrl_bar, text="🗖", font=("Arial", 10), bg="#22223B", fg=th["glow"], bd=0, cursor="hand2", command=self.toggle_maximize_state).pack(side=tk.RIGHT, padx=2)
        tk.Button(self.window_ctrl_bar, text="🗕", font=("Arial", 10), bg="#22223B", fg=th["glow"], bd=0, cursor="hand2", command=self.window.iconify).pack(side=tk.RIGHT, padx=2)

        # Telemetry Metrics Viewports
        self.title_lbl = tk.Label(self.sidebar, text="⚡ METRICS SYSTEM ⚡", font=("Courier New", 14, "bold"), fg=th["glow"], bg=th["sidebar"])
        self.title_lbl.pack(pady=10)

        self.stats_box = tk.Frame(self.sidebar, bg=th["panel"], bd=1, relief="solid", padx=10, pady=8)
        self.stats_box.pack(fill=tk.X, padx=15, pady=5)

        self.lvl_lbl = tk.Label(self.stats_box, text="SECTOR NODE: 01/10", font=("Consolas", 11, "bold"), fg=th["text"], bg=th["panel"])
        self.lvl_lbl.pack(anchor="w")

        self.timer_lbl = tk.Label(self.stats_box, text="TIME MATRIX: 120s", font=("Consolas", 11, "bold"), fg="#FF3333", bg=th["panel"])
        self.timer_lbl.pack(anchor="w")

        self.score_lbl = tk.Label(self.stats_box, text="TOTAL SCORE: 0000", font=("Consolas", 11, "bold"), fg=th["glow"], bg=th["panel"])
        self.score_lbl.pack(anchor="w")

        # System Control Panel Buttons
        self.action_panel = tk.Frame(self.sidebar, bg=th["sidebar"])
        self.action_panel.pack(fill=tk.X, padx=15, pady=8)

        self.start_btn = tk.Button(self.action_panel, text="START RUN", font=("Helvetica", 9, "bold"), bg="#00FF66", fg="#000000", bd=0, cursor="hand2", pady=5, command=self.trigger_simulation_start)
        self.start_btn.pack(fill=tk.X, pady=2)

        self.pause_btn = tk.Button(self.action_panel, text="PAUSE DECRYPT", font=("Helvetica", 9, "bold"), bg="#FF9F00", fg="#000000", bd=0, cursor="hand2", pady=5, state=tk.DISABLED, command=self.toggle_pause_state)
        self.pause_btn.pack(fill=tk.X, pady=2)

        self.reboot_btn = tk.Button(self.action_panel, text="REBOOT ENGINE", font=("Helvetica", 9, "bold"), bg=th["found"], fg="#FFFFFF", bd=0, cursor="hand2", pady=5, command=self.reboot_simulation_runtime)
        self.reboot_btn.pack(fill=tk.X, pady=2)

        self.theme_btn = tk.Button(self.action_panel, text="CYCLE SYSTEM THEME", font=("Helvetica", 9, "bold"), bg="#00A8FF", fg="#FFFFFF", bd=0, cursor="hand2", pady=5, command=self.cycle_color_themes)
        self.theme_btn.pack(fill=tk.X, pady=2)

        # Dynamic Checklist Box
        self.checklist_lbl = tk.Label(self.sidebar, text="‖ REGISTRY TARGETS ‖", font=("Courier New", 9, "bold"), fg=TEXT_MUTED, bg=th["sidebar"])
        self.checklist_lbl.pack(pady=(10, 2))
        self.checklist_scroll = tk.Frame(self.sidebar, bg=th["sidebar"])
        self.checklist_scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        # Dynamic Grid Wrapper Viewport Panel
        self.matrix_wrapper = tk.Frame(self.viewport, bg=th["bg"])
        self.matrix_wrapper.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

    # --- ADVANCED PROCEDURAL COLOR MATRIX HOT-SWAPPING ENGINE ---
    def cycle_color_themes(self):
        """Redraws the entire application view layout utilizing alternative palette registers."""
        self.theme_index = (self.theme_index + 1) % len(THEME_KEYS)
        self.current_theme = THEMES[THEME_KEYS[self.theme_index]]
        th = self.current_theme
        
        # Apply Base Configuration Transforms
        self.window.configure(bg=th["bg"])
        self.sidebar.configure(bg=th["sidebar"])
        self.viewport.configure(bg=th["bg"])
        self.window_ctrl_bar.configure(bg=th["panel"])
        self.stats_box.configure(bg=th["panel"])
        self.matrix_wrapper.configure(bg=th["bg"])
        self.checklist_scroll.configure(bg=th["sidebar"])
        
        # Update Text Colors
        self.title_lbl.config(fg=th["glow"], bg=th["sidebar"])
        self.lvl_lbl.config(fg=th["text"], bg=th["panel"])
        self.score_lbl.config(fg=th["glow"], bg=th["panel"])
        self.timer_lbl.config(bg=th["panel"])
        self.checklist_lbl.config(bg=th["sidebar"])
        self.reboot_btn.config(bg=th["found"])
        
        # Redraw existing UI artifacts safely
        self.synchronize_telemetry_dashboards()
        if self.game_active and not self.paused:
            self.render_interactive_matrix_viewport()
            # Remap locked items
            for word in self.found_words:
                for r, c in self.word_positions[word]:
                    self.grid_buttons[r][c].config(bg=th["found"])
                    self.grid_buttons[r][c].verified = True
        elif self.paused:
            self.mask_viewport_display("DECRYPTION PAUSED\n\n[ Select Resume Option to Continue ]")
        else:
            self.render_disabled_placeholder_viewport()

    # --- PROCEDURAL WORD GENERATION & VIEWPORT ENGINE ---
    def initialize_campaign_level(self, loaded_grid=None):
        self.paused = False
        self.found_words.clear()
        self.selected_coords = []
        self.word_positions.clear()
        
        self.grid_dim = 9 + self.level  
        word_count = 4 + (self.level // 2)
        
        if loaded_grid is None:
            self.time_left = max(45, 135 - (self.level * 15))
            available_pool = list(DICTIONARY_POOL)
            random.shuffle(available_pool)
            self.word_bank = available_pool[:min(len(available_pool), word_count)]
            self.grid_matrix = [["" for _ in range(self.grid_dim)] for _ in range(self.grid_dim)]
            self.execute_matrix_generation_pass()
        
        self.render_dynamic_checklist_labels()
        
        if self.game_active:
            self.render_interactive_matrix_viewport()
        else:
            self.render_disabled_placeholder_viewport()
            
        self.synchronize_telemetry_dashboards()

    def execute_matrix_generation_pass(self):
        directions = [(0, 1), (1, 0), (1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1), (-1, 1)]
        for word in self.word_bank:
            placed = False
            attempts = 0
            while not placed and attempts < 300:
                d_r, d_c = random.choice(directions)
                r = random.randint(0, self.grid_dim - 1)
                c = random.randint(0, self.grid_dim - 1)
                if 0 <= r + d_r * (len(word) - 1) < self.grid_dim and 0 <= c + d_c * (len(word) - 1) < self.grid_dim:
                    match = True
                    coords = []
                    for i in range(len(word)):
                        if self.grid_matrix[r + d_r * i][c + d_c * i] not in ("", word[i]):
                            match = False
                            break
                        coords.append((r + d_r * i, c + d_c * i))
                    if match:
                        for idx, (curr_r, curr_c) in enumerate(coords):
                            self.grid_matrix[curr_r][curr_c] = word[idx]
                        self.word_positions[word] = coords
                        placed = True
                attempts += 1

        for r in range(self.grid_dim):
            for c in range(self.grid_dim):
                if self.grid_matrix[r][c] == "":
                    self.grid_matrix[r][c] = random.choice(string.ascii_uppercase)

    def render_interactive_matrix_viewport(self):
        th = self.current_theme
        for widget in self.matrix_wrapper.winfo_children(): widget.destroy()
        self.grid_buttons = [[None for _ in range(self.grid_dim)] for _ in range(self.grid_dim)]
        
        for r in range(self.grid_dim):
            self.matrix_wrapper.rowconfigure(r, weight=1)
            for c in range(self.grid_dim):
                self.matrix_wrapper.columnconfigure(c, weight=1)
                
                btn = tk.Button(
                    self.matrix_wrapper, text=self.grid_matrix[r][c], font=("Consolas", 11, "bold"),
                    bg=th["panel"], fg=th["text"], activebackground=th["panel"], activeforeground=th["text"],
                    bd=1, relief="solid", highlightthickness=0
                )
                btn.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
                
                btn.bind("<ButtonPress-1>", lambda e, row=r, col=c: self.handle_selection_start(row, col))
                btn.bind("<B1-Motion>", lambda e: self.handle_mouse_drag_pass(e))
                btn.bind("<ButtonRelease-1>", lambda e: self.handle_selection_end_pass())
                
                self.grid_buttons[r][c] = btn

    def handle_selection_start(self, r, c):
        if self.paused or not self.game_active: return
        self.clear_visual_transient_highlights()
        self.selected_coords = [(r, c)]
        self.apply_cell_color_shift(r, c, self.current_theme["highlight"])

    def handle_mouse_drag_pass(self, event):
        if self.paused or not self.game_active: return
        widget = event.widget.winfo_containing(event.x_root, event.y_root)
        if widget:
            for r in range(self.grid_dim):
                for c in range(self.grid_dim):
                    if self.grid_buttons[r][c] == widget:
                        current_cell = (r, c)
                        
                        if len(self.selected_coords) > 1 and current_cell == self.selected_coords[-2]:
                            removed_cell = self.selected_coords.pop()
                            self.apply_cell_color_shift(removed_cell[0], removed_cell[1], self.current_theme["panel"])
                            return
                        
                        if current_cell not in self.selected_coords:
                            if self.validate_vector_line_progression(current_cell):
                                self.selected_coords.append(current_cell)
                                self.apply_cell_color_shift(r, c, self.current_theme["highlight"])
                        return

    # --- VECTOR VALIDATION & UTILITIES ---
    def validate_vector_line_progression(self, next_cell):
        if len(self.selected_coords) < 1: return True
        if len(self.selected_coords) == 1:
            r1, c1 = self.selected_coords[0]
            r2, c2 = next_cell
            return abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1
        r0, c0 = self.selected_coords[0]
        r1, c1 = self.selected_coords[1]
        dr, dc = r1 - r0, c1 - c0
        dr, dc = (dr > 0) - (dr < 0), (dc > 0) - (dc < 0)
        last_r, last_c = self.selected_coords[-1]
        return (next_cell[0] - last_r == dr) and (next_cell[1] - last_c == dc)

    def handle_selection_end_pass(self):
        if self.paused or not self.game_active: return
        extracted_string = "".join([self.grid_matrix[r][c] for r, c in self.selected_coords])
        inverted_string = extracted_string[::-1]
        matched_word = None
        for word in self.word_bank:
            if word not in self.found_words and word in (extracted_string, inverted_string):
                matched_word = word
                break
        if matched_word:
            self.found_words.add(matched_word)
            self.score += 100
            for r, c in self.word_positions[matched_word]:
                self.apply_cell_color_shift(r, c, self.current_theme["found"], lock_state=True)
            self.checklist_labels[matched_word].config(text=f"[✓] {matched_word}", fg=self.current_theme["found"])
            self.synchronize_telemetry_dashboards()
            self.evaluate_victory_metrics()
        else:
            self.clear_visual_transient_highlights()
        self.selected_coords = []

    def apply_cell_color_shift(self, r, c, color, lock_state=False):
        btn = self.grid_buttons[r][c]
        if not hasattr(btn, 'verified') or not btn.verified or lock_state:
            btn.config(bg=color)
            if lock_state: btn.verified = True

    def clear_visual_transient_highlights(self):
        for r in range(self.grid_dim):
            for c in range(self.grid_dim):
                btn = self.grid_buttons[r][c]
                if not hasattr(btn, 'verified') or not btn.verified:
                    btn.config(bg=self.current_theme["panel"])

    # --- PERSISTENT DATA SAVE MECHANICS ---
    def intercept_window_shutdown(self):
        self.window.protocol("WM_DELETE_WINDOW", self.safely_terminate_application)

    def safely_terminate_application(self):
        """Asks user to export configuration snapshots to state cache archives prior to close logs."""
        self.paused = True
        ans = messagebox.askyesnocancel("⚡ CORE SUSPEND PROTOCOL ⚡", "Save active decryption run parameters to persistent system local database before closing?")
        if ans is True:
            self.export_save_state_archive()
            self.window.destroy()
        elif ans is False:
            if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
            self.window.destroy()
        else:
            self.paused = False # Cancel close operation

    def export_save_state_archive(self):
        """Serializes environment variables into static JSON format parameters."""
        data_pack = {
            "level": self.level, "score": self.score, "total_score": self.total_score,
            "time_left": self.time_left, "word_bank": self.word_bank, "found_words": list(self.found_words),
            "grid_matrix": self.grid_matrix, "word_positions": self.word_positions, "theme_index": self.theme_index
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data_pack, f)

    def evaluate_save_handshake_on_boot(self):
        """Checks for existing state cache profiles to reconstruct runtime states seamlessly."""
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f: data = json.load(f)
                self.level = data["level"]
                self.score = data["score"]
                self.total_score = data["total_score"]
                self.time_left = data["time_left"]
                self.word_bank = data["word_bank"]
                self.found_words = set(data["found_words"])
                self.grid_matrix = data["grid_matrix"]
                self.word_positions = {k: [tuple(x) for x in v] for k, v in data["word_positions"].items()}
                self.theme_index = data.get("theme_index", 0)
                self.current_theme = THEMES[THEME_KEYS[self.theme_index]]
                
                self.game_active = True
                self.start_btn.config(state=tk.DISABLED, text="RESUMED...", bg=self.current_theme["panel"], fg=TEXT_MUTED)
                self.pause_btn.config(state=tk.NORMAL)
                
                self.initialize_campaign_level(loaded_grid=True)
                
                # Relock pre-solved state elements
                for word in self.found_words:
                    self.checklist_labels[word].config(text=f"[✓] {word}", fg=self.current_theme["found"])
                    for r, c in self.word_positions[word]:
                        self.grid_buttons[r][c].config(bg=self.current_theme["found"])
                        self.grid_buttons[r][c].verified = True
                messagebox.showinfo("⚡ CORE RELOADED ⚡", f"Persistent state profile decrypted successfully.\nResuming runtime at Sector {self.level:02d}.")
            except Exception:
                if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)

    # --- CLOCK WORKERS & CORE ENGINE WRAPPERS ---
    def execute_clock_tick(self):
        if self.game_active and not self.paused:
            self.time_left -= 1
            self.synchronize_telemetry_dashboards()
            if self.time_left <= 0:
                self.handle_critical_timeout()
                return
        self.window.after(1000, self.execute_clock_tick)

    def trigger_simulation_start(self):
        self.game_active = True
        self.start_btn.config(state=tk.DISABLED, text="RUNNING...", bg=self.current_theme["panel"], fg=TEXT_MUTED)
        self.pause_btn.config(state=tk.NORMAL)
        self.initialize_campaign_level()

    def toggle_pause_state(self):
        if not self.game_active: return
        th = self.current_theme
        if not self.paused:
            self.paused = True
            self.pause_btn.config(text="RESUME RUN", bg="#00FF66")
            self.mask_viewport_display("DECRYPTION PAUSED\n\n[ Select Resume Option to Continue ]")
        else:
            self.paused = False
            self.pause_btn.config(text="PAUSE DECRYPT", bg="#FF9F00")
            self.render_interactive_matrix_viewport()
            for word in self.found_words:
                for r, c in self.word_positions[word]:
                    self.grid_buttons[r][c].config(bg=th["found"])
                    self.grid_buttons[r][c].verified = True

    def mask_viewport_display(self, message):
        for widget in self.matrix_wrapper.winfo_children(): widget.destroy()
        tk.Label(self.matrix_wrapper, text=message, font=("Courier New", 12, "bold"), fg="#FFFFFF", bg=self.current_theme["bg"]).pack(expand=True)

    def render_disabled_placeholder_viewport(self):
        for widget in self.matrix_wrapper.winfo_children(): widget.destroy()
        lbl = tk.Label(self.matrix_wrapper, text="⚡ ENGINE HALTED ⚡\n\n[ Initialize Simulation Core to Begin ]", font=("Courier New", 13, "bold"), fg=TEXT_MUTED, bg=self.current_theme["bg"])
        lbl.pack(expand=True)

    def render_dynamic_checklist_labels(self):
        for widget in self.checklist_scroll.winfo_children(): widget.destroy()
        self.checklist_labels = {}
        for word in self.word_bank:
            lbl = tk.Label(self.checklist_scroll, text=f"[ ] {word}", font=("Courier New", 10, "bold"), fg=self.current_theme["text"], bg=self.current_theme["sidebar"], anchor="w")
            lbl.pack(fill=tk.X, pady=2)
            self.checklist_labels[word] = lbl

    def synchronize_telemetry_dashboards(self):
        self.lvl_lbl.config(text=f"SECTOR NODE: {self.level:02d}/10")
        self.timer_lbl.config(text=f"TIME MATRIX: {self.time_left:03d}s")
        self.score_lbl.config(text=f"TOTAL SCORE: {self.total_score + self.score:04d}")

    def reboot_simulation_runtime(self):
        self.score = 0
        if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
        self.initialize_campaign_level()

    def evaluate_victory_metrics(self):
        if len(self.found_words) == len(self.word_bank):
            self.total_score += self.score + (self.time_left * 2)
            if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE) # Flush old level save parameters cleanly
            if self.level < 10:
                messagebox.showinfo("⚡ NODE SECURED ⚡", f"Sector {self.level:02d} decryption clean!\nAdvancing data pipelines onto next difficulty tier.")
                self.level += 1
                self.score = 0
                self.initialize_campaign_level()
            else:
                messagebox.showinfo("🏆 CAMPAIGN SECURED 🏆", f"All 10 information layers decrypted successfully!\nTotal Score: {self.total_score}")
                self.reset_entire_engine_state()

    def handle_critical_timeout(self):
        messagebox.showerror("❌ SYSTEM CORRUPT ❌", "Decryption pipeline runtime failure! Resetting firmware to baseline.")
        if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
        self.reset_entire_engine_state()

    def reset_entire_engine_state(self):
        self.game_active = False
        self.level = 1
        self.total_score = 0
        self.score = 0
        self.start_btn.config(state=tk.NORMAL, text="START RUN", bg="#00FF66", fg="#000000")
        self.pause_btn.config(state=tk.DISABLED, text="PAUSE DECRYPT")
        self.initialize_campaign_level()

    def toggle_maximize_state(self):
        if not self.is_maximized:
            self.window.attributes("-fullscreen", True)
            self.is_maximized = True
        else:
            self.window.attributes("-fullscreen", False)
            self.is_maximized = False

if __name__ == "__main__":
    UltimateWordSearchEngine()
