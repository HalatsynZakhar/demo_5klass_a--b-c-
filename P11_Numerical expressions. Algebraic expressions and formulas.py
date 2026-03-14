"""
Демонстрація: Числові та буквені вирази. Формули (§ 11).
Для 5 класу.
Числові вирази, значення виразу, буквені вирази, формули (S=ab, P=(a+b)*2, s=vt).
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
AMBER     = "#d97706"
BLUE      = "#2563eb"

# ══════════════════════════════════════════════════════════════════
#  ГОЛОВНИЙ КЛАС
# ══════════════════════════════════════════════════════════════════
class ExpressionsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Числові та буквені вирази. Формули")
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
        # ── Header
        hdr = tk.Frame(self, bg=ACCENT, height=80)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        
        tk.Label(hdr, text="Числові та буквені вирази. Формули (§ 11)", bg=ACCENT, fg=WHITE, font=("Segoe UI", 24, "bold")).pack(side="left", padx=30)
        tk.Button(hdr, text="❌ Вихід", font=("Arial", 16, "bold"), bg=RED, fg=WHITE, bd=0, command=self.destroy).pack(side="right", padx=20)
        
        # ── Navigation Menu
        nav = tk.Frame(self, bg=WHITE, height=60)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        
        btn_font = ("Segoe UI", 14, "bold")
        tk.Button(nav, text="1. Теорія виразів", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_intro).pack(side="left", padx=15)
        tk.Button(nav, text="2. Формули", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_formulas).pack(side="left", padx=15)
        tk.Button(nav, text="3. Порядок дій & Дужки", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_brackets_demo).pack(side="left", padx=15)
        tk.Button(nav, text="4. Приклади задач", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_tasks_examples).pack(side="left", padx=15)
        tk.Button(nav, text="5. Тренажер", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_trainer).pack(side="left", padx=15)

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
    #  SCENE 1: THEORY
    # ══════════════════════════════════════════════════════════════════
    def show_intro(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=30)
        
        tk.Label(f, text="Числові та буквені вирази", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20))
        
        # Comparison
        cmp_f = tk.Frame(f, bg=BG)
        cmp_f.pack(fill="x", pady=10)
        
        # Numeric
        n_f = tk.Frame(cmp_f, bg=WHITE, bd=2, relief="solid", padx=20, pady=20)
        n_f.pack(side="left", expand=True, fill="both", padx=10)
        tk.Label(n_f, text="Числові вирази", font=("Segoe UI", 20, "bold"), bg=WHITE, fg=BLUE).pack()
        tk.Label(n_f, text="Складаються тільки з чисел,\nзнаків дій та дужок.\n\nПриклади:\n3547 – 2793\n100 – (145 : 5 + 30)", font=("Segoe UI", 16), bg=WHITE, justify="left").pack(pady=10)
        tk.Label(n_f, text="Результат обчислення —\nзначення виразу.", font=("Segoe UI", 16, "italic"), bg=WHITE, fg=MUTED).pack()

        # Algebraic
        a_f = tk.Frame(cmp_f, bg=WHITE, bd=2, relief="solid", padx=20, pady=20)
        a_f.pack(side="left", expand=True, fill="both", padx=10)
        tk.Label(a_f, text="Буквені вирази", font=("Segoe UI", 20, "bold"), bg=WHITE, fg=AMBER).pack()
        tk.Label(a_f, text="Містять букви (змінні),\nчисла та знаки дій.\n\nПриклади:\np + 400\n3 ∙ (m + n)", font=("Segoe UI", 16), bg=WHITE, justify="left").pack(pady=10)
        tk.Label(a_f, text="Значення залежить від того,\nяке число замість букви.", font=("Segoe UI", 16, "italic"), bg=WHITE, fg=MUTED).pack()

        # Example calculation
        ex_f = tk.Frame(f, bg=YELLOW_BG, bd=1, relief="solid", padx=20, pady=15)
        ex_f.pack(fill="x", pady=20)
        tk.Label(ex_f, text="Приклад: Знайти значення 7 + b, якщо b = 5", font=("Segoe UI", 18, "bold"), bg=YELLOW_BG).pack(anchor="w")
        tk.Label(ex_f, text="Якщо b = 5, то 7 + b = 7 + 5 = 12", font=("Consolas", 20), bg=YELLOW_BG).pack(anchor="w")

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 2: FORMULAS
    # ══════════════════════════════════════════════════════════════════
    def show_formulas(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=30)
        
        tk.Label(f, text="Формули", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20))
        
        forms = [
            ("Площа прямокутника", "S = a ∙ b", "a, b — сторони"),
            ("Периметр прямокутника", "P = (a + b) ∙ 2", "a, b — сторони"),
            ("Формула відстані", "s = v ∙ t", "v — швидкість, t — час")
        ]
        
        for title, formula, vars_desc in forms:
            p_f = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=20, pady=15)
            p_f.pack(fill="x", pady=8)
            tk.Label(p_f, text=title, font=("Segoe UI", 20, "bold"), bg=WHITE, fg=ACCENT).pack(side="left")
            tk.Label(p_f, text=formula, font=("Consolas", 28, "bold"), bg=YELLOW_BG, padx=15).pack(side="left", padx=40)
            tk.Label(p_f, text=vars_desc, font=("Segoe UI", 16, "italic"), bg=WHITE, fg=MUTED).pack(side="right")

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 3: BRACKETS DEMO (INCORPORATED FROM PREVIOUS P11)
    # ══════════════════════════════════════════════════════════════════
    def show_brackets_demo(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=20)
        
        tk.Label(f, text="Порядок дій та вплив дужок", font=("Segoe UI", 28, "bold"), bg=BG).pack()
        
        # Simple comparison demo
        # 20 - 5 + 3  vs 20 - (5 + 3)
        a, b, c = 20, 5, 3
        
        demo_f = tk.Frame(f, bg=BG)
        demo_f.pack(pady=30, fill="x")
        
        # Case 1
        c1 = tk.Frame(demo_f, bg=WHITE, bd=2, relief="groove", padx=20, pady=20)
        c1.pack(side="left", expand=True, fill="both", padx=20)
        tk.Label(c1, text="Без дужок (по порядку)", font=("Segoe UI", 18, "bold"), bg=WHITE, fg=BLUE).pack()
        tk.Label(c1, text=f"{a} - {b} + {c} =", font=("Consolas", 32), bg=WHITE).pack(pady=10)
        tk.Label(c1, text=f"1) {a} - {b} = {a-b}\n2) {a-b} + {c} = {(a-b)+c}", font=("Segoe UI", 16), bg=WHITE, justify="left").pack()
        tk.Label(c1, text=f"Результат: {(a-b)+c}", font=("Segoe UI", 24, "bold"), bg=WHITE, fg=BLUE).pack(pady=10)

        # Case 2
        c2 = tk.Frame(demo_f, bg=WHITE, bd=2, relief="groove", padx=20, pady=20)
        c2.pack(side="left", expand=True, fill="both", padx=20)
        tk.Label(c2, text="З дужками (спочатку в дужках)", font=("Segoe UI", 18, "bold"), bg=WHITE, fg=ORANGE).pack()
        tk.Label(c2, text=f"{a} - ({b} + {c}) =", font=("Consolas", 32), bg=WHITE).pack(pady=10)
        tk.Label(c2, text=f"1) {b} + {c} = {b+c}\n2) {a} - {b+c} = {a-(b+c)}", font=("Segoe UI", 16), bg=WHITE, justify="left").pack()
        tk.Label(c2, text=f"Результат: {a-(b+c)}", font=("Segoe UI", 24, "bold"), bg=WHITE, fg=ORANGE).pack(pady=10)

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 4: TASKS EXAMPLES
    # ══════════════════════════════════════════════════════════════════
    def show_tasks_examples(self):
        self.clear_main()
        # Create a scrollable or just a list of common tasks
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=30)
        
        tk.Label(f, text="Приклади завдань", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20))
        
        tasks = [
            ("443. Було b кг бананів, продали 215 кг.", "Вираз: b - 215"),
            ("444. 30 дітей зробили по x фігурок.", "Вираз: 30 ∙ x"),
            ("447. Знайти (a + b) ∙ c, якщо a=113, b=227, c=13", "Обчислення: (113 + 227) ∙ 13 = 340 ∙ 13 = 4420"),
            ("459. Їхав a год (70 км/год) та b год (80 км/год)", "Формула: s = 70a + 80b")
        ]
        
        for q, ans in tasks:
            t_f = tk.Frame(f, bg=WHITE, bd=1, relief="solid", padx=20, pady=10)
            t_f.pack(fill="x", pady=5)
            tk.Label(t_f, text=q, font=("Segoe UI", 16), bg=WHITE).pack(anchor="w")
            tk.Label(t_f, text=ans, font=("Segoe UI", 16, "bold"), bg=WHITE, fg=GREEN).pack(anchor="w")

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 5: TRAINER
    # ══════════════════════════════════════════════════════════════════
    def show_trainer(self):
        self.clear_main()
        LW = int(self.SW * 0.60)
        RW = self.SW - LW

        left = tk.Frame(self.main_area, bg=BG, width=LW)
        left.pack(side="left", fill="both")
        left.pack_propagate(False)

        # Task Box
        self.task_box = tk.Frame(left, bg=WHITE, bd=3, relief="solid", padx=40, pady=40)
        self.task_box.pack(pady=30)
        self.task_text = tk.Label(self.task_box, text="", font=("Segoe UI", 36, "bold"), bg=WHITE, fg=TEXT)
        self.task_text.pack()

        # Input display
        self.display_frame = tk.Frame(left, bg=WHITE, highlightbackground=ACCENT, highlightthickness=2)
        self.display_frame.pack(pady=10, ipadx=24, ipady=10)
        self.lbl_display = tk.Label(self.display_frame, text="", bg=WHITE, fg=TEXT, font=("Segoe UI", 48, "bold"), width=12, anchor="e")
        self.lbl_display.pack()

        self.lbl_feedback = tk.Label(left, text="", bg=BG, font=("Segoe UI", 20, "bold"), justify="center")
        self.lbl_feedback.pack(pady=10)

        # Numpad
        kbd = tk.Frame(left, bg=BG)
        kbd.pack(pady=10)
        self.kbd_buttons = []
        rows = [["7","8","9"], ["4","5","6"], ["1","2","3"], ["C","0","⌫"]]
        for row in rows:
            r = tk.Frame(kbd, bg=BG)
            r.pack(pady=2)
            for ch in row:
                btn = tk.Button(r, text=ch, bg=RED_BG if ch in ("⌫", "C") else BTN_NUM, font=("Segoe UI", 20, "bold"), width=6, height=1, relief="flat", command=lambda c=ch: self._key_press(c))
                btn.pack(side="left", padx=5)
                self.kbd_buttons.append(btn)

        btn_f = tk.Frame(left, bg=BG)
        btn_f.pack(pady=10)
        self.btn_ok = tk.Button(btn_f, text="✓ Перевірити", bg=GREEN, fg=WHITE, font=("Segoe UI", 18, "bold"), relief="flat", padx=40, pady=10, command=self.check_answer)
        self.btn_ok.pack(side="left", padx=20)
        self.btn_next = tk.Button(btn_f, text="▶ Наступне", bg=ACCENT, fg=WHITE, font=("Segoe UI", 18, "bold"), relief="flat", padx=40, pady=10, command=self.next_task)

        # Right side
        right = tk.Frame(self.main_area, bg=PANEL, width=RW, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        rpad = tk.Frame(right, bg=PANEL)
        rpad.pack(fill="both", expand=True, padx=30, pady=40)
        
        tk.Label(rpad, text="Підказка", font=("Segoe UI", 18, "bold"), bg=PANEL).pack(anchor="w")
        hint_box = tk.Frame(rpad, bg="#eff6ff", highlightbackground="#bfdbfe", highlightthickness=1, padx=15, pady=15)
        hint_box.pack(fill="x", pady=10)
        tk.Label(hint_box, text="Заміни букву числом\nі обчисли результат як\nу звичайному прикладі.", font=("Segoe UI", 16), bg="#eff6ff", justify="left").pack()

        self.lbl_score = tk.Label(rpad, text="Рахунок: 0 / 0", font=("Segoe UI", 24, "bold"), bg=PANEL, fg=ACCENT)
        self.lbl_score.pack(side="bottom", pady=40)

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

        types = ["simple_add", "simple_sub", "formula_y", "formula_s"]
        t = random.choice(types)
        
        if t == "simple_add":
            b = random.randint(10, 100)
            val = random.randint(5, 50)
            self.task = {"ans": b + val, "text": f"Обчисли 7 + b, якщо b = {val}" if b==7 else f"Обчисли {b} + x, якщо x = {val}"}
        elif t == "simple_sub":
            m = random.randint(200, 500)
            val = random.randint(50, 150)
            self.task = {"ans": m - val, "text": f"Обчисли m - {val}, якщо m = {m}"}
        elif t == "formula_y":
            x = random.randint(2, 10)
            # y = 3x - 2
            self.task = {"ans": 3*x - 2, "text": f"За формулою y = 3x - 2\nзнайди y, якщо x = {x}"}
        else: # formula_s
            v = random.randint(60, 90)
            t_val = random.randint(2, 5)
            self.task = {"ans": v * t_val, "text": f"За формулою s = v ∙ t\nзнайди відстань s, якщо\nv = {v} км/год, t = {t_val} год"}

        self.task_text.config(text=self.task["text"])

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
    app = ExpressionsApp()
    app.mainloop()
