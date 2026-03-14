"""
Демонстрація: Порядок дій і Дужки (§ 11).
Для 5 класу.
"""

import tkinter as tk
from tkinter import font
import random
import time

# ══════════════════════════════════════════════════════════════════
#  COLORS & STYLES
# ══════════════════════════════════════════════════════════════════
BG        = "#fdfbf7"
WHITE     = "#ffffff"
TEXT      = "#1c1917"
ACCENT    = "#d97706" # Amber
BLUE      = "#2563eb"
RED       = "#dc2626"
GREEN     = "#16a34a"

class BracketsDemoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Дужки та порядок дій (§ 11)")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        # Fonts
        self.f_header = font.Font(family="Segoe UI", size=32, weight="bold")
        self.f_math   = font.Font(family="Courier New", size=48, weight="bold")
        self.f_text   = font.Font(family="Segoe UI", size=24)
        self.f_btn    = font.Font(family="Segoe UI", size=20, weight="bold")

        self.a, self.b, self.c = 10, 2, 3
        self.dist_a, self.dist_b, self.dist_c = 2, 3, 4

        self._build_ui()
        self.scene_order_of_ops()

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=WHITE, height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🔢 Порядок дій і Дужки", font=self.f_header, bg=WHITE, fg=TEXT).pack(side="left", padx=40)
        tk.Button(header, text="❌ Вихід", font=("Arial", 20), bg=RED, fg=WHITE, bd=0, command=self.destroy).pack(side="right", padx=20)

        # Main Area
        self.main = tk.Frame(self, bg=BG)
        self.main.pack(fill="both", expand=True, padx=40, pady=40)

        # Nav Bar
        nav = tk.Frame(self.main, bg=BG)
        nav.pack(fill="x", pady=(0, 40))
        
        tk.Button(nav, text="1. Порядок дій", font=self.f_btn, bg=BLUE, fg=WHITE, 
                  command=self.scene_order_of_ops).pack(side="left", padx=10)
        tk.Button(nav, text="2. Розподільний закон", font=self.f_btn, bg=ACCENT, fg=WHITE, 
                  command=self.scene_distributive).pack(side="left", padx=10)
        
        tk.Button(nav, text="🎲 Нові числа", font=self.f_btn, bg=GREEN, fg=WHITE, 
                  command=self.generate_random_numbers).pack(side="right", padx=10)

        # Content Area
        self.content = tk.Frame(self.main, bg=WHITE, bd=2, relief="solid")
        self.content.pack(fill="both", expand=True)

    def generate_random_numbers(self):
        # Order of ops: a - b + c vs a - (b + c)
        # Ensure a > b + c for subtraction to be valid in naturals
        self.b = random.randint(2, 9)
        self.c = random.randint(2, 9)
        self.a = random.randint(self.b + self.c + 2, 30)
        
        # Distributive: a * (b + c)
        # Keep small for visualization
        self.dist_a = random.randint(2, 4) # Rows
        self.dist_b = random.randint(2, 5) # Blue cols
        self.dist_c = random.randint(2, 5) # Red cols
        
        # Refresh current scene
        if hasattr(self, 'current_scene'):
            self.current_scene()

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 1: Order of Operations
    # ══════════════════════════════════════════════════════════════════
    def scene_order_of_ops(self):
        self.current_scene = self.scene_order_of_ops
        self.clear_content()
        
        tk.Label(self.content, text="Порівняймо два вирази:", font=self.f_text, bg=WHITE, fg=MUTED).pack(pady=30)
        
        frame_cmp = tk.Frame(self.content, bg=WHITE)
        frame_cmp.pack(expand=True, fill="both")
        
        # Left: No brackets
        f_left = tk.Frame(frame_cmp, bg="#eff6ff", bd=2, relief="groove") # Blue tint
        f_left.pack(side="left", expand=True, fill="both", padx=20, pady=20)
        
        tk.Label(f_left, text="Без дужок", font=("Segoe UI", 24, "bold"), bg="#eff6ff", fg=BLUE).pack(pady=20)
        
        # Container for dynamic expression parts
        self.f_expr_l = tk.Frame(f_left, bg="#eff6ff")
        self.f_expr_l.pack(pady=20)
        
        # Parts of expression: [a] [-] [b] [+] [c]
        self.lbl_l_parts = []
        parts_l = [str(self.a), " - ", str(self.b), " + ", str(self.c)]
        for p in parts_l:
            l = tk.Label(self.f_expr_l, text=p, font=self.f_math, bg="#eff6ff", fg=TEXT)
            l.pack(side="left")
            self.lbl_l_parts.append(l)
            
        self.lbl_l_res = tk.Label(f_left, text="", font=("Segoe UI", 28), bg="#eff6ff", fg=BLUE, wraplength=500)
        self.lbl_l_res.pack(pady=20)
        
        btn_l = tk.Button(f_left, text="▶ Обчислити", font=self.f_btn, bg=BLUE, fg=WHITE,
                          command=lambda: self.anim_left())
        btn_l.pack(pady=20)

        # Right: With brackets
        f_right = tk.Frame(frame_cmp, bg="#fefce8", bd=2, relief="groove") # Yellow tint
        f_right.pack(side="right", expand=True, fill="both", padx=20, pady=20)
        
        tk.Label(f_right, text="З дужками", font=("Segoe UI", 24, "bold"), bg="#fefce8", fg=ACCENT).pack(pady=20)
        
        self.f_expr_r = tk.Frame(f_right, bg="#fefce8")
        self.f_expr_r.pack(pady=20)
        
        # Parts: [a] [-] [(] [b] [+] [c] [)]
        self.lbl_r_parts = []
        parts_r = [str(self.a), " - ", "(", str(self.b), " + ", str(self.c), ")"]
        for p in parts_r:
            l = tk.Label(self.f_expr_r, text=p, font=self.f_math, bg="#fefce8", fg=TEXT)
            l.pack(side="left")
            self.lbl_r_parts.append(l)
        
        self.lbl_r_res = tk.Label(f_right, text="", font=("Segoe UI", 28), bg="#fefce8", fg=ACCENT, wraplength=500)
        self.lbl_r_res.pack(pady=20)
        
        btn_r = tk.Button(f_right, text="▶ Обчислити", font=self.f_btn, bg=ACCENT, fg=WHITE,
                          command=lambda: self.anim_right())
        btn_r.pack(pady=20)

    def anim_left(self):
        # a - b + c
        # 1. Highlight "a - b"
        # Indices: 0(a), 1(-), 2(b), 3(+), 4(c)
        
        # Reset colors
        for l in self.lbl_l_parts: l.config(fg=TEXT, bg="#eff6ff")
        
        # Highlight Step 1: a - b
        for i in range(3):
            self.lbl_l_parts[i].config(bg="#bfdbfe", fg=BLUE) # Highlight blue
            
        res1 = self.a - self.b
        self.lbl_l_res.config(text=f"1. По порядку: {self.a} - {self.b} = {res1}")
        
        def step2():
            # Replace "a - b" with result visually? 
            # Better: Keep equation but update highlighting
            
            # Reset first part
            for i in range(3): self.lbl_l_parts[i].config(fg="#94a3b8", bg="#eff6ff") # Fade out
            
            # Highlight Step 2: result + c
            # We can't easily highlight result + c in original string.
            # Let's change the text of the first part to the result
            
            self.lbl_l_parts[0].config(text=str(res1), fg=GREEN, bg="#dcfce7")
            self.lbl_l_parts[1].config(text=" + ", fg=GREEN, bg="#dcfce7")
            self.lbl_l_parts[2].config(text=str(self.c), fg=GREEN, bg="#dcfce7")
            
            # Hide remaining parts
            self.lbl_l_parts[3].pack_forget()
            self.lbl_l_parts[4].pack_forget()
            
            res2 = res1 + self.c
            self.lbl_l_res.config(text=f"2. Потім додаємо: {res1} + {self.c} = {res2}", fg=GREEN)
            
        self.after(1500, step2)

    def anim_right(self):
        # a - (b + c)
        # Indices: 0(a), 1(-), 2((), 3(b), 4(+), 5(c), 6())
        
        # Reset colors
        for l in self.lbl_r_parts: l.config(fg=TEXT, bg="#fefce8")
        
        # Highlight Step 1: (b + c)
        for i in range(2, 7):
            self.lbl_r_parts[i].config(bg="#fde68a", fg=ACCENT) # Highlight yellow/orange
            
        res1 = self.b + self.c
        self.lbl_r_res.config(text=f"1. ДУЖКИ ГОЛОВНІ! {self.b} + {self.c} = {res1}")
        
        def step2():
            # Fade out brackets part
            # Replace bracket part with result
            
            self.lbl_r_parts[0].config(bg="#dcfce7", fg=GREEN) # a
            self.lbl_r_parts[1].config(bg="#dcfce7", fg=GREEN) # -
            
            # Hide bracket parts
            for i in range(2, 7): self.lbl_r_parts[i].pack_forget()
            
            # Create new label for result if not exists, or reuse one
            # Let's reuse index 2
            self.lbl_r_parts[2].config(text=str(res1), bg="#dcfce7", fg=GREEN)
            self.lbl_r_parts[2].pack(side="left")
            
            res2 = self.a - res1
            self.lbl_r_res.config(text=f"2. Тепер віднімаємо: {self.a} - {res1} = {res2}", fg=GREEN)
            
        self.after(1500, step2)

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 2: Distributive Property
    # ══════════════════════════════════════════════════════════════════
    def scene_distributive(self):
        self.current_scene = self.scene_distributive
        self.clear_content()
        
        tk.Label(self.content, text="Розподільний закон множення", font=self.f_text, bg=WHITE).pack(pady=20)
        tk.Label(self.content, text=f"{self.dist_a} × ({self.dist_b} + {self.dist_c})", font=self.f_math, bg=WHITE, fg=TEXT).pack(pady=10)
        
        self.canvas = tk.Canvas(self.content, bg="white", height=500)
        self.canvas.pack(fill="both", expand=True, padx=40)
        
        # Draw blocks
        size = 60
        gap = 10
        
        # Calculate centering
        total_w = (self.dist_b + self.dist_c) * (size + gap) + 40 # 40 extra gap
        start_x = (self.winfo_screenwidth() - total_w) // 2
        start_y = 100
        
        self.blocks_blue = []
        self.blocks_red = []
        
        # Draw initial state
        for r in range(self.dist_a):
            y = start_y + r * (size + gap)
            # Blue blocks
            for c in range(self.dist_b):
                x = start_x + c * (size + gap)
                rect = self.canvas.create_rectangle(x, y, x+size, y+size, fill=BLUE, outline=WHITE, width=2)
                self.blocks_blue.append({'id': rect, 'x': x, 'y': y})
            
            # Red blocks (separated)
            for c in range(self.dist_c):
                x = start_x + (self.dist_b * (size + gap)) + 40 + c * (size + gap)
                rect = self.canvas.create_rectangle(x, y, x+size, y+size, fill=RED, outline=WHITE, width=2)
                self.blocks_red.append({'id': rect, 'x': x, 'y': y})
                
        # Label below
        self.lbl_expl = tk.Label(self.content, text=f"{self.dist_a} ряди по {self.dist_b} синіх і {self.dist_c} червоних", font=("Segoe UI", 20), bg=WHITE)
        self.lbl_expl.pack(pady=20)
        
        frame_btns = tk.Frame(self.content, bg=WHITE)
        frame_btns.pack(pady=20)
        
        tk.Button(frame_btns, text=f"Спосіб 1: Спочатку додати ({self.dist_b}+{self.dist_c})", font=self.f_btn, bg="#f0f9ff", 
                  command=self.dist_method1).pack(side="left", padx=20)
        
        tk.Button(frame_btns, text=f"Спосіб 2: Розкрити дужки ({self.dist_a}×{self.dist_b} + {self.dist_a}×{self.dist_c})", font=self.f_btn, bg="#fefce8", 
                  command=self.dist_method2).pack(side="left", padx=20)

    def dist_method1(self):
        sum_bc = self.dist_b + self.dist_c
        res = self.dist_a * sum_bc
        self.lbl_expl.config(text=f"Спочатку додаємо в дужках: {self.dist_b} + {self.dist_c} = {sum_bc} кубиків у рядку.\nПотім множимо на кількість рядків: {self.dist_a} × {sum_bc} = {res}.")
        
        # Reset position first (in case method 2 was run)
        self.reset_blocks()
        
        # Animation: Slide red blocks to the left to join blue blocks
        target_dx = -40
        steps = 30
        step_dx = target_dx / steps
        
        def anim(step=0):
            if step < steps:
                for b in self.blocks_red:
                    self.canvas.move(b['id'], step_dx, 0)
                self.after(16, lambda: anim(step+1))
            else:
                # Highlight row by row sequentially
                self.highlight_rows_sequence(0)

        anim()

    def highlight_rows_sequence(self, row_idx):
        if row_idx >= self.dist_a:
            # Clear highlight after done
            self.after(1000, self.reset_styles)
            return

        # Highlight current row (both blue and red blocks in this row)
        # We need to find blocks belonging to this row
        # blocks_blue structure: {'id': rect, 'x': x, 'y': y, 'row': r, 'col': c}
        
        # Reset previous row styles if not first
        if row_idx > 0:
             self.reset_row_style(row_idx - 1)

        # Highlight current row
        for b in self.blocks_blue + self.blocks_red:
            if b['row'] == row_idx:
                self.canvas.itemconfig(b['id'], outline="#facc15", width=4, stipple="gray50") # Yellow outline + stipple
        
        self.after(800, lambda: self.highlight_rows_sequence(row_idx + 1))

    def reset_row_style(self, row_idx):
        for b in self.blocks_blue + self.blocks_red:
            if b['row'] == row_idx:
                self.canvas.itemconfig(b['id'], outline=WHITE, width=2, stipple="")

    def reset_styles(self):
        for b in self.blocks_blue + self.blocks_red:
            self.canvas.itemconfig(b['id'], outline=WHITE, width=2, stipple="", fill=b['color'])

    def dist_method2(self):
        prod1 = self.dist_a * self.dist_b
        prod2 = self.dist_a * self.dist_c
        total = prod1 + prod2
        self.lbl_expl.config(text=f"Спочатку множимо окремо: ({self.dist_a} × {self.dist_b}) синіх + ({self.dist_a} × {self.dist_c}) червоних.\n{prod1} + {prod2} = {total}.")
        
        # Reset position first
        self.reset_blocks()
        
        # Animation: Move red blocks further RIGHT to emphasize separation
        target_dx = 60
        steps = 30
        step_dx = target_dx / steps
        
        def anim(step=0):
            if step < steps:
                for b in self.blocks_red:
                    self.canvas.move(b['id'], step_dx, 0)
                self.after(16, lambda: anim(step+1))
            else:
                # Pulse effects after separation
                self.flash_groups()
                
        anim()

    def flash_groups(self):
        # 1. Highlight Blue Group (stipple)
        for b in self.blocks_blue:
            self.canvas.itemconfig(b['id'], stipple="gray25", outline="#60a5fa", width=3)
            
        def step2():
            # Reset Blue
            for b in self.blocks_blue:
                self.canvas.itemconfig(b['id'], stipple="", outline=WHITE, width=2)
            # Highlight Red Group
            for b in self.blocks_red:
                self.canvas.itemconfig(b['id'], stipple="gray25", outline="#f87171", width=3)
            self.after(1000, step3)
            
        def step3():
            # Reset Red
            for b in self.blocks_red:
                self.canvas.itemconfig(b['id'], stipple="", outline=WHITE, width=2)
            
        self.after(1000, step2)

    def reset_blocks(self):
        # Redraw blocks at initial positions
        self.canvas.delete("all")
        self.blocks_blue = []
        self.blocks_red = []
        
        size = 60
        gap = 10
        total_w = (self.dist_b + self.dist_c) * (size + gap) + 40
        start_x = (self.winfo_screenwidth() - total_w) // 2
        start_y = 100
        
        for r in range(self.dist_a):
            y = start_y + r * (size + gap)
            for c in range(self.dist_b):
                x = start_x + c * (size + gap)
                rect = self.canvas.create_rectangle(x, y, x+size, y+size, fill=BLUE, outline=WHITE, width=2)
                self.blocks_blue.append({'id': rect, 'x': x, 'y': y, 'row': r, 'color': BLUE})
            
            for c in range(self.dist_c):
                x = start_x + (self.dist_b * (size + gap)) + 40 + c * (size + gap)
                rect = self.canvas.create_rectangle(x, y, x+size, y+size, fill=RED, outline=WHITE, width=2)
                self.blocks_red.append({'id': rect, 'x': x, 'y': y, 'row': r, 'color': RED})

MUTED = "#78716c"

if __name__ == "__main__":
    app = BracketsDemoApp()
    app.mainloop()
