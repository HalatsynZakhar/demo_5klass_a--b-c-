"""
Демонстрація: Степінь натурального числа (§ 8).
Для 5 класу.
Поняття степеня, квадрат, куб, пріоритет операцій.
"""

import tkinter as tk
import tkinter.font as tkfont
import math, random

# ══════════════════════════════════════════════════════════════════
#  ПАЛІТРА
# ══════════════════════════════════════════════════════════════════
BG        = "#f5f7fa"
PANEL     = "#ffffff"
ACCENT    = "#2563eb"
BORDER    = "#dbeafe"
TEXT      = "#1e293b"
MUTED     = "#64748b"
GREEN     = "#16a34a"
RED       = "#dc2626"
ORANGE    = "#d97706"
YELLOW_BG = "#fef9c3"
HL_BG     = "#fde68a"
HL_FG     = "#92400e"
GREEN_BG  = "#dcfce7"
RED_BG    = "#fee2e2"
WHITE     = "#ffffff"
BTN_NUM   = "#e2e8f0"
BTN_HOV   = "#cbd5e1"
PURPLE    = "#7c3aed"

# ══════════════════════════════════════════════════════════════════
#  ГОЛОВНИЙ КЛАС
# ══════════════════════════════════════════════════════════════════
class PowersApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Степінь натурального числа")
        self.configure(bg=BG)
        
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        
        # Keyboard support
        self.bind("<Key>", self._on_key_press)
        self.bind("<Return>", lambda e: self.check_answer())
        self.bind("<BackSpace>", lambda e: self._key_press("⌫"))
        self.bind("<Delete>", lambda e: self._key_press("C"))

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()

        # State
        self.task = None
        self.user_input = ""
        self.score = 0
        self.total = 0
        self.phase = "answer" # "answer" or "feedback"

        self._build_ui()
        self.show_intro()

    def _build_ui(self):
        # ── Header (Reduced height 80 -> 60)
        hdr = tk.Frame(self, bg=ACCENT, height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        
        tk.Label(hdr, text="Степінь натурального числа (§ 8)", bg=ACCENT, fg=WHITE, font=("Segoe UI", 20, "bold")).pack(side="left", padx=30)
        tk.Button(hdr, text="❌ Вихід", font=("Arial", 14, "bold"), bg=RED, fg=WHITE, bd=0, command=self.destroy).pack(side="right", padx=20)
        
        # ── Navigation Menu (Reduced height 60 -> 50)
        nav = tk.Frame(self, bg=WHITE, height=50)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        
        btn_font = ("Segoe UI", 12, "bold") # Reduced from 16
        tk.Button(nav, text="1. Що таке степінь?", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_intro).pack(side="left", padx=20)
        tk.Button(nav, text="2. Квадрат та куб", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_square_cube).pack(side="left", padx=20)
        tk.Button(nav, text="3. Пріоритет дій", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_priority).pack(side="left", padx=20)
        tk.Button(nav, text="4. Тренажер", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_trainer).pack(side="left", padx=20)

        # ── Main Content Area
        self.main_area = tk.Frame(self, bg=BG)
        self.main_area.pack(fill="both", expand=True)

    def clear_main(self):
        for w in self.main_area.winfo_children():
            w.destroy()

    def _on_key_press(self, event):
        if event.char.isdigit():
            self._key_press(event.char)

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 1: CONCEPT OF POWER
    # ══════════════════════════════════════════════════════════════════
    def show_intro(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=30) # Reduced from 50
        
        tk.Label(f, text="Степінь як короткий запис добутку", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20)) # Reduced from 36
        
        # Visual comparison
        box = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=20, pady=20) # Reduced padding
        box.pack(pady=15)
        
        tk.Label(box, text="Додавання однакових доданків:", font=("Segoe UI", 16), bg=WHITE, fg=MUTED).pack(anchor="w") # Reduced from 18
        tk.Label(box, text="3 + 3 + 3 + 3 + 3 = 3 ∙ 5", font=("Consolas", 24, "bold"), bg=WHITE, fg=TEXT).pack(anchor="w", pady=(0, 15)) # Reduced from 32
        
        tk.Label(box, text="Множення однакових множників:", font=("Segoe UI", 16), bg=WHITE, fg=MUTED).pack(anchor="w") # Reduced from 18
        
        # Render power using labels for superscript
        p_frame = tk.Frame(box, bg=WHITE)
        p_frame.pack(anchor="w")
        tk.Label(p_frame, text="3 ∙ 3 ∙ 3 ∙ 3 ∙ 3 = 3", font=("Consolas", 24, "bold"), bg=WHITE, fg=TEXT).pack(side="left") # Reduced from 32
        tk.Label(p_frame, text="5", font=("Consolas", 14, "bold"), bg=WHITE, fg=ACCENT).pack(side="left", pady=(0, 15)) # Reduced from 20

        desc = (
            "Вираз 3⁵ називають степенем:\n"
            "• 3 — основа степеня (число, яке множимо)\n"
            "• 5 — показник степеня (скільки разів множимо)\n\n"
            "❗️ Важлива домовленість: a¹ = a (будь-яке число в першому степені дорівнює самому собі)."
        )
        tk.Label(f, text=desc, font=("Segoe UI", 18), bg=BG, fg=TEXT, justify="left").pack(pady=20) # Reduced from 24

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 2: SQUARE AND CUBE
    # ══════════════════════════════════════════════════════════════════
    def show_square_cube(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=30) # Reduced from 50
        
        tk.Label(f, text="Квадрат і куб числа", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20)) # Reduced from 36
        
        cards = tk.Frame(f, bg=BG)
        cards.pack(pady=15)
        
        # Square Card
        sq = tk.Frame(cards, bg=WHITE, bd=2, relief="solid", padx=20, pady=20) # Reduced padding
        sq.pack(side="left", padx=15, fill="y")
        
        tk.Label(sq, text="Квадрат числа", font=("Segoe UI", 20, "bold"), bg=WHITE, fg=PURPLE).pack() # Reduced from 24
        
        p_sq = tk.Frame(sq, bg=WHITE)
        p_sq.pack(pady=8)
        tk.Label(p_sq, text="a", font=("Consolas", 36, "bold"), bg=WHITE).pack(side="left") # Reduced from 48
        tk.Label(p_sq, text="2", font=("Consolas", 18, "bold"), bg=WHITE, fg=PURPLE).pack(side="left", pady=(0, 25)) # Reduced from 24
        
        tk.Label(sq, text="a² = a ∙ a", font=("Segoe UI", 16), bg=WHITE).pack(pady=8) # Reduced from 20
        tk.Label(sq, text="17² = 17 ∙ 17 = 289", font=("Segoe UI", 14, "italic"), bg=WHITE, fg=MUTED).pack() # Reduced from 18

        # Cube Card
        cb = tk.Frame(cards, bg=WHITE, bd=2, relief="solid", padx=20, pady=20) # Reduced padding
        cb.pack(side="left", padx=15, fill="y")
        
        tk.Label(cb, text="Куб числа", font=("Segoe UI", 20, "bold"), bg=WHITE, fg=ORANGE).pack() # Reduced from 24
        
        p_cb = tk.Frame(cb, bg=WHITE)
        p_cb.pack(pady=8)
        tk.Label(p_cb, text="a", font=("Consolas", 36, "bold"), bg=WHITE).pack(side="left") # Reduced from 48
        tk.Label(p_cb, text="3", font=("Consolas", 18, "bold"), bg=WHITE, fg=ORANGE).pack(side="left", pady=(0, 25)) # Reduced from 24
        
        tk.Label(cb, text="a³ = a ∙ a ∙ a", font=("Segoe UI", 16), bg=WHITE).pack(pady=8) # Reduced from 20
        tk.Label(cb, text="5³ = 5 ∙ 5 ∙ 5 = 125", font=("Segoe UI", 14, "italic"), bg=WHITE, fg=MUTED).pack() # Reduced from 18

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 3: PRIORITY OF OPERATIONS
    # ══════════════════════════════════════════════════════════════════
    def show_priority(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=30) # Reduced from 50
        
        tk.Label(f, text="Пріоритет операцій", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20)) # Reduced from 36
        
        order = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=20, pady=20) # Reduced padding
        order.pack(fill="x", pady=15)
        
        steps = [
            ("1. Піднесення до степеня", "Виконується ПЕРШИМ (якщо немає дужок)"),
            ("2. Множення та ділення", "Виконуються після степеня зліва направо"),
            ("3. Додавання та віднімання", "Виконуються в останню чергу")
        ]
        
        for i, (title, desc) in enumerate(steps):
            tk.Label(order, text=title, font=("Segoe UI", 18, "bold"), bg=WHITE, fg=ACCENT if i==0 else TEXT).pack(anchor="w") # Reduced from 22
            tk.Label(order, text=desc, font=("Segoe UI", 14), bg=WHITE, fg=MUTED).pack(anchor="w", pady=(0, 10)) # Reduced from 18

        ex = tk.Frame(f, bg=YELLOW_BG, padx=15, pady=15)
        ex.pack(pady=15)
        tk.Label(ex, text="Приклад: 6 ∙ 3² + 5 = 6 ∙ 9 + 5 = 54 + 5 = 59", font=("Consolas", 18, "bold"), bg=YELLOW_BG).pack() # Reduced from 24

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 4: TRAINER
    # ══════════════════════════════════════════════════════════════════
    def show_trainer(self):
        self.clear_main()
        
        LW = int(self.SW * 0.60)
        RW = self.SW - LW

        left = tk.Frame(self.main_area, bg=BG, width=LW)
        left.pack(side="left", fill="both")
        left.pack_propagate(False)

        # Task display with power rendering
        self.task_box = tk.Frame(left, bg=WHITE, bd=3, relief="solid", padx=20, pady=15) # Reduced padding
        self.task_box.pack(pady=20) # Reduced from 50
        
        self.task_container = tk.Frame(self.task_box, bg=WHITE)
        self.task_container.pack()

        # Input display
        self.display_frame = tk.Frame(left, bg=WHITE, highlightbackground=ACCENT, highlightthickness=2)
        self.display_frame.pack(pady=5, ipadx=16, ipady=4) # Reduced from 10/24/10
        
        self.lbl_display = tk.Label(self.display_frame, text="", bg=WHITE, fg=TEXT, font=("Segoe UI", 32, "bold"), width=12, anchor="e") # Reduced from 48
        self.lbl_display.pack()

        self.lbl_feedback = tk.Label(left, text="", bg=BG, font=("Segoe UI", 14, "bold"), justify="center") # Reduced from 20
        self.lbl_feedback.pack(pady=5)

        # Numpad
        kbd = tk.Frame(left, bg=BG)
        kbd.pack(pady=5) # Reduced from 20
        self.kbd_buttons = []
        rows = [["7","8","9"], ["4","5","6"], ["1","2","3"], ["C","0","⌫"]]
        for row in rows:
            r = tk.Frame(kbd, bg=BG)
            r.pack(pady=2) # Reduced from 5
            for ch in row:
                btn = tk.Button(r, text=ch, bg=RED_BG if ch in ("⌫", "C") else BTN_NUM, font=("Segoe UI", 16, "bold"), width=6, height=1, relief="flat", command=lambda c=ch: self._key_press(c)) # Reduced from 22/2
                btn.pack(side="left", padx=4)
                self.kbd_buttons.append(btn)

        # Bottom buttons
        btn_f = tk.Frame(left, bg=BG)
        btn_f.pack(pady=10)

        self.btn_ok = tk.Button(btn_f, text="✓ Перевірити", bg=GREEN, fg=WHITE, font=("Segoe UI", 14, "bold"),
                                relief="flat", bd=0, cursor="hand2", padx=30, pady=10, command=self.check_answer) # Reduced from 18/40/15
        self.btn_ok.pack(side="left", padx=10)

        self.btn_next = tk.Button(btn_f, text="▶ Наступне", bg=ACCENT, fg=WHITE, font=("Segoe UI", 14, "bold"),
                                  relief="flat", bd=0, cursor="hand2", padx=30, pady=10, command=self.next_task)
        # Packed later when needed

        # Right side
        right = tk.Frame(self.main_area, bg=PANEL, width=RW, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        rpad = tk.Frame(right, bg=PANEL)
        rpad.pack(fill="both", expand=True, padx=15, pady=20) # Reduced from 30/40
        
        tk.Label(rpad, text="Таблиця квадратів", font=("Segoe UI", 14, "bold"), bg=PANEL).pack(anchor="w") # Reduced from 18
        grid = tk.Frame(rpad, bg=PANEL)
        grid.pack(pady=5)
        for i in range(1, 11):
            tk.Label(grid, text=f"{i}² = {i*i}", font=("Consolas", 12), bg=PANEL).grid(row=(i-1)%5, column=(i-1)//5, padx=5, pady=2, sticky="w") # Reduced from 14

        tk.Label(rpad, text="Таблиця кубів", font=("Segoe UI", 14, "bold"), bg=PANEL).pack(anchor="w", pady=(10, 0)) # Reduced from 18/20
        grid2 = tk.Frame(rpad, bg=PANEL)
        grid2.pack(pady=5)
        for i in range(1, 6):
            tk.Label(grid2, text=f"{i}³ = {i**3}", font=("Consolas", 12), bg=PANEL).pack(anchor="w") # Reduced from 14

        self.lbl_score = tk.Label(rpad, text="Рахунок: 0 / 0", font=("Segoe UI", 18, "bold"), bg=PANEL, fg=ACCENT) # Reduced from 24
        self.lbl_score.pack(side="bottom", pady=20)

        self.next_task()

    def _key_press(self, ch):
        if self.phase != "answer": return
        if ch == "⌫": self.user_input = self.user_input[:-1]
        elif ch == "C": self.user_input = ""
        else:
            if len(self.user_input) < 10: self.user_input += ch
        self.lbl_display.config(text=self.user_input)

    def next_task(self):
        self.user_input = ""
        self.phase = "answer"
        self.lbl_display.config(text="", bg=WHITE)
        self.display_frame.config(highlightbackground=ACCENT)
        self.lbl_feedback.config(text="")
        self.btn_next.pack_forget()
        self.btn_ok.pack(side="left", padx=20)
        
        for w in self.task_container.winfo_children(): w.destroy()

        # Task types: square, cube, expression
        task_type = random.choice(["square", "cube", "expr"])
        
        if task_type == "square":
            a = random.randint(2, 20)
            self._render_power(a, 2)
            self.task = {"ans": a*a}
        elif task_type == "cube":
            a = random.randint(2, 10)
            self._render_power(a, 3)
            self.task = {"ans": a**3}
        else: # expression: a * b^2 + c
            a = random.randint(2, 10)
            b = random.randint(2, 5)
            c = random.randint(1, 20)
            # a * b^2 + c
            tk.Label(self.task_container, text=f"{a} ∙ ", font=("Segoe UI", 32, "bold"), bg=WHITE).pack(side="left") # Reduced from 42
            self._render_power(b, 2, container=self.task_container, inline=True)
            tk.Label(self.task_container, text=f" + {c} = ?", font=("Segoe UI", 32, "bold"), bg=WHITE).pack(side="left") # Reduced from 42
            self.task = {"ans": a * (b**2) + c}

    def _render_power(self, base, exp, container=None, inline=False):
        if container is None: container = self.task_container
        f = tk.Frame(container, bg=WHITE)
        f.pack(side="left" if inline else "top")
        tk.Label(f, text=str(base), font=("Segoe UI", 32, "bold"), bg=WHITE).pack(side="left") # Reduced from 42
        tk.Label(f, text=str(exp), font=("Segoe UI", 16, "bold"), bg=WHITE, fg=ACCENT).pack(side="left", pady=(0, 25)) # Reduced from 22/30
        if not inline: tk.Label(f, text=" = ?", font=("Segoe UI", 32, "bold"), bg=WHITE).pack(side="left") # Reduced from 42

    def check_answer(self):
        if self.phase != "answer" or not self.user_input: return
        self.phase = "feedback"
        self.total += 1
        got = int(self.user_input)
        ok = (got == self.task["ans"])
        
        if ok:
            self.score += 1
            self.lbl_feedback.config(text="✅ Правильно!", fg=GREEN)
            self.lbl_display.config(bg=GREEN_BG)
            self.after(1000, self.next_task)
        else:
            self.lbl_feedback.config(text=f"❌ Помилка! Відповідь: {self.task['ans']}", fg=RED)
            self.lbl_display.config(bg=RED_BG)
            self.btn_ok.pack_forget()
            self.btn_next.pack(side="left", padx=20)

        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")

if __name__ == "__main__":
    app = PowersApp()
    app.mainloop()
