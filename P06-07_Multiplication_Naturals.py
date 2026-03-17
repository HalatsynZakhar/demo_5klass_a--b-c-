"""
Демонстрація: Множення та властивості множення (§ 6-7).
Для 5 класу.
Переставна, сполучна та розподільна властивості множення.
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

# ══════════════════════════════════════════════════════════════════
#  ГОЛОВНИЙ КЛАС
# ══════════════════════════════════════════════════════════════════
class MultiplicationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Множення та властивості множення")
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
        
        tk.Label(hdr, text="Множення натуральних чисел (§ 6-7)", bg=ACCENT, fg=WHITE, font=("Segoe UI", 20, "bold")).pack(side="left", padx=30)
        tk.Button(hdr, text="❌ Вихід", font=("Arial", 14, "bold"), bg=RED, fg=WHITE, bd=0, command=self.destroy).pack(side="right", padx=20)
        
        # ── Navigation Menu (Reduced height 60 -> 50)
        nav = tk.Frame(self, bg=WHITE, height=50)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        
        btn_font = ("Segoe UI", 12, "bold") # Reduced from 16
        tk.Button(nav, text="1. Основні властивості", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_intro).pack(side="left", padx=20)
        tk.Button(nav, text="2. Розподільна властивість", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_distributive).pack(side="left", padx=20)
        tk.Button(nav, text="3. Візуалізація закону", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_distributive_viz).pack(side="left", padx=20)
        tk.Button(nav, text="4. Тренажер: Зручні обчислення", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_rational_trainer).pack(side="left", padx=20)

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
    #  SCENE 1: BASIC PROPERTIES (COMMUTATIVE, ASSOCIATIVE, 10/100/1000)
    # ══════════════════════════════════════════════════════════════════
    def show_intro(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=30) # Reduced from 50
        
        tk.Label(f, text="Закони множення", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20)) # Reduced from 36
        
        props = [
            ("Переставна властивість", "Від перестановки множників добуток не змінюється.", "a ∙ b = b ∙ a", "6 ∙ 5 = 5 ∙ 6 = 30"),
            ("Сполучна властивість", "Щоб добуток двох чисел помножити на третє число, можна перше число помножити на добуток другого і третього.", "(a ∙ b) ∙ c = a ∙ (b ∙ c)", "(5 ∙ 6) ∙ 2 = 5 ∙ (6 ∙ 2) = 60"),
            ("Множення на 10, 100, 1000...", "Щоб помножити число на розрядну одиницю, треба дописати до нього стільки нулів, скільки їх у розрядній одиниці.", "54 ∙ 100 = 5400", "237 ∙ 1000 = 237 000")
        ]

        for title, rule, formula, example in props:
            p_frame = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=15, pady=10) # Reduced padding
            p_frame.pack(fill="x", pady=5) # Reduced pady
            
            tk.Label(p_frame, text=title, font=("Segoe UI", 20, "bold"), bg=WHITE, fg=ACCENT).pack(anchor="w") # Reduced from 22
            tk.Label(p_frame, text=rule, font=("Segoe UI", 16), bg=WHITE, fg=TEXT).pack(anchor="w", pady=2) # Reduced from 16, less padding
            tk.Label(p_frame, text=formula, font=("Consolas", 18, "bold"), bg=YELLOW_BG, fg=HL_FG, padx=10).pack(anchor="w", pady=2) # Reduced from 20
            tk.Label(p_frame, text=f"Приклад: {example}", font=("Segoe UI", 14, "italic"), bg=WHITE, fg=MUTED).pack(anchor="w") # Reduced from 16

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 2: DISTRIBUTIVE PROPERTY
    # ══════════════════════════════════════════════════════════════════
    def show_distributive(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=30) # Reduced from 50
        
        tk.Label(f, text="Розподільна властивість множення", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20)) # Reduced from 36
        
        props = [
            ("Відносно додавання", "Щоб помножити суму на число, можна помножити на це число кожний доданок і отримані добутки додати.", "(a + b) ∙ c = a ∙ c + b ∙ c", "49 ∙ 113 + 51 ∙ 113 = (49 + 51) ∙ 113 = 11 300"),
            ("Відносно віднімання", "Щоб помножити різницю на число, можна помножити на це число зменшуване і від'ємник окремо і від першого добутку відняти другий.", "(a – b) ∙ c = a ∙ c – b ∙ c", "97 ∙ 18 = (100 – 3) ∙ 18 = 1800 – 54 = 1746")
        ]

        for title, rule, formula, example in props:
            p_frame = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=15, pady=15) # Reduced padding
            p_frame.pack(fill="x", pady=8) # Reduced pady
            
            tk.Label(p_frame, text=title, font=("Segoe UI", 20, "bold"), bg=WHITE, fg=ORANGE).pack(anchor="w") # Reduced from 24
            tk.Label(p_frame, text=rule, font=("Segoe UI", 16), bg=WHITE, fg=TEXT).pack(anchor="w", pady=4) # Reduced from 18
            tk.Label(p_frame, text=formula, font=("Consolas", 20, "bold"), bg=YELLOW_BG, fg=HL_FG, padx=10).pack(anchor="w", pady=4) # Reduced from 22
            tk.Label(p_frame, text=f"Приклад: {example}", font=("Segoe UI", 16, "italic"), bg=WHITE, fg=MUTED).pack(anchor="w") # Reduced from 18

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 3: DISTRIBUTIVE VIZ (FROM P11)
    # ══════════════════════════════════════════════════════════════════
    def show_distributive_viz(self):
        self.clear_main()
        
        # Random parameters for visualization
        self.dist_a = random.randint(2, 4) # Rows
        self.dist_b = random.randint(2, 5) # Blue cols
        self.dist_c = random.randint(2, 5) # Red cols
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=20) # Reduced padding
        
        tk.Label(f, text="Візуалізація розподільного закону", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack() # Reduced from 28 (same but consistent)
        tk.Label(f, text=f"{self.dist_a} × ({self.dist_b} + {self.dist_c})", font=("Consolas", 32, "bold"), bg=BG, fg=ACCENT).pack(pady=5) # Reduced from 36
        
        self.canvas = tk.Canvas(f, bg="white", height=300, bd=2, relief="ridge") # Reduced height 400->300
        self.canvas.pack(fill="both", expand=True, padx=20)
        
        self.lbl_expl = tk.Label(f, text=f"{self.dist_a} ряди по {self.dist_b} синіх і {self.dist_c} червоних блоків", font=("Segoe UI", 16), bg=BG, fg=TEXT) # Reduced from 18
        self.lbl_expl.pack(pady=10)
        
        btn_frame = tk.Frame(f, bg=BG)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text=f"Спосіб 1: {self.dist_a} × ({self.dist_b} + {self.dist_c})", font=("Segoe UI", 12, "bold"), bg=ACCENT, fg=WHITE, 
                  command=self.dist_method1, padx=15).pack(side="left", padx=5) # Reduced from 14/20/10
        
        tk.Button(btn_frame, text=f"Спосіб 2: {self.dist_a} × {self.dist_b} + {self.dist_a} × {self.dist_c}", font=("Segoe UI", 12, "bold"), bg=ORANGE, fg=WHITE, 
                  command=self.dist_method2, padx=15).pack(side="left", padx=5)

        tk.Button(btn_frame, text="🎲 Нові числа", font=("Segoe UI", 12, "bold"), bg=GREEN, fg=WHITE, 
                  command=self.show_distributive_viz, padx=15).pack(side="left", padx=5)

        self.reset_blocks()

    def reset_blocks(self):
        self.canvas.delete("all")
        self.blocks_blue = []
        self.blocks_red = []
        
        size = 40 # Reduced from 50
        gap = 6 # Reduced from 8
        total_w = (self.dist_b + self.dist_c) * (size + gap) + 30
        start_x = (self.canvas.winfo_width() - total_w) // 2
        if start_x < 50: start_x = 50
        start_y = 30 # Reduced from 50
        
        for r in range(self.dist_a):
            y = start_y + r * (size + gap)
            for c in range(self.dist_b):
                x = start_x + c * (size + gap)
                rect = self.canvas.create_rectangle(x, y, x+size, y+size, fill=ACCENT, outline=WHITE, width=2)
                self.blocks_blue.append({'id': rect, 'x': x, 'y': y, 'row': r, 'color': ACCENT})
            
            for c in range(self.dist_c):
                x = start_x + (self.dist_b * (size + gap)) + 30 + c * (size + gap)
                rect = self.canvas.create_rectangle(x, y, x+size, y+size, fill=RED, outline=WHITE, width=2)
                self.blocks_red.append({'id': rect, 'x': x, 'y': y, 'row': r, 'color': RED})
        
        # Initial draw needs update if canvas width is 1 (before pack)
        if self.canvas.winfo_width() <= 1:
            self.after(100, self.reset_blocks)

    def dist_method1(self):
        self.reset_blocks()
        sum_bc = self.dist_b + self.dist_c
        res = self.dist_a * sum_bc
        self.lbl_expl.config(text=f"Спосіб 1: Спочатку додаємо в дужках: {self.dist_b} + {self.dist_c} = {sum_bc} в ряду.\nПотім множимо на кількість рядів: {self.dist_a} × {sum_bc} = {res}.")
        
        # Animation: Slide red blocks to the left
        target_dx = -30 # Adjusted
        steps = 20
        step_dx = target_dx / steps
        def anim(step=0):
            if step < steps:
                for b in self.blocks_red:
                    self.canvas.move(b['id'], step_dx, 0)
                self.after(20, lambda: anim(step+1))
        anim()

    def dist_method2(self):
        self.reset_blocks()
        prod1 = self.dist_a * self.dist_b
        prod2 = self.dist_a * self.dist_c
        total = prod1 + prod2
        self.lbl_expl.config(text=f"Спосіб 2: Множимо групи окремо: {self.dist_a} × {self.dist_b} синіх та {self.dist_a} × {self.dist_c} червоних.\n{prod1} + {prod2} = {total}.")
        
        # Animation: Move red blocks further right
        target_dx = 30 # Adjusted
        steps = 20
        step_dx = target_dx / steps
        def anim(step=0):
            if step < steps:
                for b in self.blocks_red:
                    self.canvas.move(b['id'], step_dx, 0)
                self.after(20, lambda: anim(step+1))
        anim()

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 4: RATIONAL MULTIPLICATION TRAINER
    # ══════════════════════════════════════════════════════════════════
    def show_rational_trainer(self):
        self.clear_main()
        
        LW = int(self.SW * 0.60)
        RW = self.SW - LW

        # ── ліва частина (тренажер)
        left = tk.Frame(self.main_area, bg=BG, width=LW)
        left.pack(side="left", fill="both")
        left.pack_propagate(False)

        # Header
        tk.Label(left, text="Тренажер: Раціональне множення", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(20, 0)) # Reduced from 36/40
        tk.Label(left, text="Використовуй властивості множення, щоб рахувати зручно!", font=("Segoe UI", 14), bg=BG, fg=MUTED).pack(pady=2) # Reduced from 18

        # Task Box
        task_box = tk.Frame(left, bg=WHITE, bd=3, relief="solid", padx=20, pady=15) # Reduced padding
        task_box.pack(pady=15) # Reduced from 30
        
        self.task_text = tk.Label(task_box, text="", font=("Segoe UI", 32, "bold"), bg=WHITE, fg=TEXT) # Reduced from 42
        self.task_text.pack()

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
        BTN_W, BTN_H = 6, 1 # Reduced height from 2
        FONT_KBD = ("Segoe UI", 16, "bold") # Reduced from 22
        
        rows = [["7","8","9"], ["4","5","6"], ["1","2","3"], ["C","0","⌫"]]
        for row in rows:
            r = tk.Frame(kbd, bg=BG)
            r.pack(pady=2)
            for ch in row:
                is_del = ch in ("⌫", "C")
                btn = tk.Button(r, text=ch, bg="#fee2e2" if is_del else BTN_NUM, fg=RED if is_del else TEXT,
                                font=FONT_KBD, width=BTN_W, height=BTN_H, relief="flat", bd=0, cursor="hand2",
                                command=lambda c=ch: self._key_press(c))
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

        # ── права частина (правила та рахунок)
        right = tk.Frame(self.main_area, bg=PANEL, width=RW, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        rpad = tk.Frame(right, bg=PANEL)
        rpad.pack(fill="both", expand=True, padx=15, pady=20) # Reduced from 30/40

        tk.Label(rpad, text="Зручні способи", bg=PANEL, fg=MUTED, font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,5)) # Reduced from 18
        hint_box = tk.Frame(rpad, bg="#eff6ff", highlightbackground="#bfdbfe", highlightthickness=1, padx=10, pady=10)
        hint_box.pack(fill="x")
        
        hint_text = (
            "1. Шукай зручні добутки:\n"
            "   • 5 ∙ 2 = 10\n"
            "   • 5 ∙ 20 = 100\n"
            "   • 25 ∙ 4 = 100\n"
            "   • 125 ∙ 8 = 1000\n\n"
            "2. Розподільна властивість:\n"
            "   a ∙ c + b ∙ c = (a + b) ∙ c\n\n"
            "3. Множення на 10, 100...\n"
            "   Дописуй нулі праворуч!"
        )
        tk.Label(hint_box, text=hint_text, bg="#eff6ff", fg=TEXT, font=("Segoe UI", 12), justify="left", anchor="w").pack(fill="x") # Reduced from 14

        # Score
        self.lbl_score = tk.Label(rpad, text="Рахунок: 0 / 0", font=("Segoe UI", 18, "bold"), bg=PANEL, fg=ACCENT) # Reduced from 24
        self.lbl_score.pack(side="bottom", pady=20)

        self.next_task()

    def _key_press(self, ch):
        if self.phase != "answer": return
        if ch == "⌫":
            self.user_input = self.user_input[:-1]
        elif ch == "C":
            self.user_input = ""
        else:
            if len(self.user_input) < 12:
                self.user_input += ch
        self.lbl_display.config(text=self.user_input)

    def next_task(self):
        self.user_input = ""
        self.phase = "answer"
        self.lbl_display.config(text="", bg=WHITE)
        self.display_frame.config(highlightbackground=ACCENT)
        self.lbl_feedback.config(text="")
        self.btn_next.pack_forget()
        self.btn_ok.pack(side="left", padx=20)
        
        # Task types: power of 10, grouping, distributive
        task_type = random.choice(["power10", "grouping", "distributive_add", "distributive_sub"])
        
        if task_type == "power10":
            a = random.randint(11, 999)
            p = random.choice([10, 100, 1000])
            expr = f"{a} ∙ {p}"
            ans = a * p
        elif task_type == "grouping":
            # (a * b) * c where a * c is a round number
            pair = random.choice([(5, 2), (25, 4), (125, 8), (5, 20), (50, 2)])
            a, c = pair
            b = random.randint(11, 49)
            nums = [a, b, c]
            random.shuffle(nums)
            expr = f"{nums[0]} ∙ {nums[1]} ∙ {nums[2]}"
            ans = a * b * c
        elif task_type == "distributive_add":
            # a*c + b*c = (a+b)*c where a+b is round
            c = random.randint(11, 99)
            target = random.choice([10, 50, 100])
            a = random.randint(1, target - 1)
            b = target - a
            expr = f"{a} ∙ {c} + {b} ∙ {c}"
            ans = (a + b) * c
        else: # distributive_sub
            # a*c - b*c = (a-b)*c where a-b is round
            c = random.randint(11, 99)
            target = random.choice([10, 50, 100])
            b = random.randint(1, 40)
            a = target + b
            expr = f"{a} ∙ {c} - {b} ∙ {c}"
            ans = (a - b) * c

        self.task = {"expr": expr, "ans": ans}
        self.task_text.config(text=expr + " = ?")

    def check_answer(self):
        if self.phase != "answer": return
        raw = self.user_input.strip()
        if not raw: return

        self.phase = "feedback"
        self.total += 1
        
        try:
            got = int(raw)
            correct = self.task["ans"]
            ok = (got == correct)
        except:
            ok = False

        if ok:
            self.score += 1
            self.lbl_feedback.config(text="✅ Правильно!", fg=GREEN)
            self.lbl_display.config(bg=GREEN_BG)
            self.display_frame.config(highlightbackground=GREEN)
            self.after(1000, self.next_task)
        else:
            self.lbl_feedback.config(text=f"❌ Помилка! Правильна відповідь: {self.task['ans']}", fg=RED)
            self.lbl_display.config(bg=RED_BG)
            self.display_frame.config(highlightbackground=RED)
            self.btn_ok.pack_forget()
            self.btn_next.pack(side="left", padx=20)

        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")

if __name__ == "__main__":
    app = MultiplicationApp()
    app.mainloop()
