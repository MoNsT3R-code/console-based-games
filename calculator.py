import tkinter as tk

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Standard Calculator")
        self.window.geometry("350x500")
        self.window.resizable(False, False)

        # Main string tracking state for calculations
        self.expression = ""

        self._build_ui()
        self.window.mainloop()

    def _build_ui(self):
        """Constructs the visual digital readouts and button matrix grids."""
        # --- DISPLAY SCREEN PANEL ---
        display_frame = tk.Frame(self.window, bg="#F5F5F5", height=100)
        display_frame.pack(expand=True, fill="both")

        # Inferred display tracking label
        self.display_label = tk.Label(
            display_frame, text="0", anchor="e", font=("Helvetica", 36),
            bg="#F5F5F5", fg="#212121", padx=20
        )
        self.display_label.pack(expand=True, fill="both")

        # --- BUTTON GRID CONFIGURATION ---
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(expand=True, fill="both")

        # Map out grid structures logically (Rows & Columns)
        button_layout = [
            ["C", "(", ")", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["C", "0", ".", "="]  # Left duplicate acts as helper button padding mapping
        ]

        # Configure scaling matrices inside rows/columns
        for r in range(5):
            buttons_frame.rowconfigure(r, weight=1)
        for c in range(4):
            buttons_frame.columnconfigure(c, weight=1)

        # Instantiate buttons across layouts dynamically
        for row_idx, row in enumerate(button_layout):
            for col_idx, symbol in enumerate(row):
                # Edge Case: Handle unique button placements manually
                if row_idx == 4 and col_idx == 0:
                    continue # Skip duplicate mapping position to make space for clean alignment

                # Distinguish operation buttons using distinct highlight colors
                bg_color = "#E0E0E0"  # Default numeric button color
                fg_color = "#000000"
                if symbol in ["/", "*", "-", "+", "="]:
                    bg_color = "#FF9800"  # Action orange accent highlight
                    fg_color = "#FFFFFF"
                elif symbol in ["C", "(", ")"]:
                    bg_color = "#BDBDBD"  # Auxiliary control button highlight

                # Bind special logic directly to custom actions or numeric string routing
                if symbol == "=":
                    action = self._evaluate_expression
                elif symbol == "C":
                    action = self._clear_display
                else:
                    action = lambda val=symbol: self._append_character(val)

                btn = tk.Button(
                    buttons_frame, text=symbol, font=("Helvetica", 18),
                    bg=bg_color, fg=fg_color, activebackground="#9E9E9E", 
                    bd=1, relief="flat", command=action
                )
                
                # Expand specific button blocks to anchor perfectly over remaining matrices
                if symbol == "0":
                    btn.grid(row=row_idx, column=0, columnspan=2, sticky="nsew", padx=1, pady=1)
                elif symbol == "." and row_idx == 4:
                    btn.grid(row=row_idx, column=2, sticky="nsew", padx=1, pady=1)
                elif symbol == "=" and row_idx == 4:
                    btn.grid(row=row_idx, column=3, sticky="nsew", padx=1, pady=1)
                else:
                    btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)

    def _append_character(self, character: str):
        """Appends validation variables onto the evaluation string safely."""
        self.expression += str(character)
        self.display_label.config(text=self.expression)

    def _clear_display(self):
        """Flushes storage strings and re-initializes screen monitors to default state."""
        self.expression = ""
        self.display_label.config(text="0")

    def _evaluate_expression(self):
        """Safely parses mathematical syntax constraints using defensive checks instead of exception loops."""
        if not self.expression:
            return

        # Defensive check: Block standard math limits to prevent ZeroDivision runtime crashes
        if "/0" in self.expression:
            self.display_label.config(text="Error: Div by 0")
            self.expression = ""
            return

        # Clean string layout inputs before using built-in evaluating interpreters
        sanitized_query = self.expression.strip()
        
        # Inferred eval block execution tracking
        # eval syntax processes raw operations matching standard precedence profiles automatically
        result = str(eval(sanitized_query))
        
        # Format floating points nicely if they get too long
        if "." in result and len(result) > 10:
            result = result[:10]

        self.display_label.config(text=result)
        self.expression = result  # Retain calculation result index history for step linking


if __name__ == "__main__":
    Calculator()
