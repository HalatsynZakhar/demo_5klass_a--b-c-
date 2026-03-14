"""
Демонстрація: Порядок дій і Дужки (§ 11).
Для 5 класу.
"""

import tkinter as tk
from tkinter import font

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

        # Content Area
        self.content = tk.Frame(self.main, bg=WHITE, bd=2, relief="solid")
        self.content.pack(fill="both", expand=True)

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 1: Order of Operations
    # ══════════════════════════════════════════════════════════════════
    def scene_order_of_ops(self):
        self.clear_content()
        
        tk.Label(self.content, text="Порівняймо два вирази:", font=self.f_text, bg=WHITE, fg=MUTED).pack(pady=30)
        
        frame_cmp = tk.Frame(self.content, bg=WHITE)
        frame_cmp.pack(expand=True, fill="both")
        
        # Left: No brackets
        f_left = tk.Frame(frame_cmp, bg="#eff6ff", bd=2, relief="groove") # Blue tint
        f_left.pack(side="left", expand=True, fill="both", padx=20, pady=20)
        
        tk.Label(f_left, text="Без дужок", font=("Segoe UI", 20, "bold"), bg="#eff6ff", fg=BLUE).pack(pady=20)
        lbl_l_expr = tk.Label(f_left, text="10 - 2 + 3", font=self.f_math, bg="#eff6ff", fg=TEXT)
        lbl_l_expr.pack(pady=20)
        
        self.lbl_l_res = tk.Label(f_left, text="", font=("Segoe UI", 28), bg="#eff6ff", fg=BLUE)
        self.lbl_l_res.pack(pady=20)
        
        btn_l = tk.Button(f_left, text="Обчислити", font=self.f_btn, bg=BLUE, fg=WHITE,
                          command=lambda: self.anim_left(lbl_l_expr, self.lbl_l_res))
        btn_l.pack(pady=20)

        # Right: With brackets
        f_right = tk.Frame(frame_cmp, bg="#fefce8", bd=2, relief="groove") # Yellow tint
        f_right.pack(side="right", expand=True, fill="both", padx=20, pady=20)
        
        tk.Label(f_right, text="З дужками", font=("Segoe UI", 20, "bold"), bg="#fefce8", fg=ACCENT).pack(pady=20)
        lbl_r_expr = tk.Label(f_right, text="10 - (2 + 3)", font=self.f_math, bg="#fefce8", fg=TEXT)
        lbl_r_expr.pack(pady=20)
        
        self.lbl_r_res = tk.Label(f_right, text="", font=("Segoe UI", 28), bg="#fefce8", fg=ACCENT)
        self.lbl_r_res.pack(pady=20)
        
        btn_r = tk.Button(f_right, text="Обчислити", font=self.f_btn, bg=ACCENT, fg=WHITE,
                          command=lambda: self.anim_right(lbl_r_expr, self.lbl_r_res))
        btn_r.pack(pady=20)

    def anim_left(self, lbl_expr, lbl_res):
        # 10 - 2 + 3
        # Step 1: 10 - 2 = 8
        lbl_expr.config(text="8 + 3", fg=BLUE)
        lbl_res.config(text="1. Робимо по порядку: 10 - 2 = 8")
        
        def step2():
            lbl_expr.config(text="11", fg=GREEN)
            lbl_res.config(text="2. Потім додаємо: 8 + 3 = 11")
            
        self.after(1500, step2)

    def anim_right(self, lbl_expr, lbl_res):
        # 10 - (2 + 3)
        # Step 1: (2 + 3) = 5
        lbl_expr.config(text="10 - 5", fg=ACCENT)
        lbl_res.config(text="1. ДУЖКИ ГОЛОВНІ! 2 + 3 = 5")
        
        def step2():
            lbl_expr.config(text="5", fg=GREEN)
            lbl_res.config(text="2. Тепер віднімаємо: 10 - 5 = 5")
            
        self.after(1500, step2)

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 2: Distributive Property
    # ══════════════════════════════════════════════════════════════════
    def scene_distributive(self):
        self.clear_content()
        
        tk.Label(self.content, text="Розподільний закон множення", font=self.f_text, bg=WHITE).pack(pady=20)
        tk.Label(self.content, text="2 × (3 + 4)", font=self.f_math, bg=WHITE, fg=TEXT).pack(pady=10)
        
        self.canvas = tk.Canvas(self.content, bg="white", height=400)
        self.canvas.pack(fill="x", padx=40)
        
        # Draw blocks
        # 2 rows. 3 blue blocks, 4 red blocks.
        
        size = 60
        gap = 10
        start_x = 100
        start_y = 50
        
        self.blocks = []
        
        # Draw initial state
        for r in range(2):
            y = start_y + r * (size + gap)
            # 3 Blue
            for c in range(3):
                x = start_x + c * (size + gap)
                rect = self.canvas.create_rectangle(x, y, x+size, y+size, fill=BLUE, outline=WHITE, width=2)
                self.blocks.append(rect)
            
            # 4 Red (separated slightly)
            for c in range(4):
                x = start_x + (3 * (size + gap)) + 40 + c * (size + gap)
                rect = self.canvas.create_rectangle(x, y, x+size, y+size, fill=RED, outline=WHITE, width=2)
                self.blocks.append(rect)
                
        # Label below
        self.lbl_expl = tk.Label(self.content, text="2 ряди по 3 синіх і 4 червоних", font=("Segoe UI", 20), bg=WHITE)
        self.lbl_expl.pack(pady=20)
        
        frame_btns = tk.Frame(self.content, bg=WHITE)
        frame_btns.pack(pady=20)
        
        tk.Button(frame_btns, text="Спосіб 1: Спочатку додати (3+4)", font=self.f_btn, bg="#f0f9ff", 
                  command=self.dist_method1).pack(side="left", padx=20)
        
        tk.Button(frame_btns, text="Спосіб 2: Розкрити дужки (2×3 + 2×4)", font=self.f_btn, bg="#fefce8", 
                  command=self.dist_method2).pack(side="left", padx=20)

    def dist_method1(self):
        self.lbl_expl.config(text="Спочатку додаємо в дужках: 3 + 4 = 7 кубиків у рядку.\nПотім множимо: 2 × 7 = 14.")
        # Visual: Move red blocks closer to blue
        self.canvas.move("all", 0, 0) # Dummy
        # Animation could be complex, simple text explanation is usually enough for quick demo

    def dist_method2(self):
        self.lbl_expl.config(text="Спочатку множимо окремо: (2 × 3) синіх + (2 × 4) червоних.\n6 + 8 = 14.")

MUTED = "#78716c"

if __name__ == "__main__":
    app = BracketsDemoApp()
    app.mainloop()
