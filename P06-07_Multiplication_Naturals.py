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
        # ── Header
        hdr = tk.Frame(self, bg=ACCENT, height=80)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        
        tk.Label(hdr, text="Множення натуральних чисел (§ 6-7)", bg=ACCENT, fg=WHITE, font=("Segoe UI", 24, "bold")).pack(side="left", padx=30)
        tk.Button(hdr, text="❌ Вихід", font=("Arial", 16, "bold"), bg=RED, fg=WHITE, bd=0, command=self.destroy).pack(side="right", padx=20)
        
        # ── Navigation Menu
        nav = tk.Frame(self, bg=WHITE, height=60)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        
        btn_font = ("Segoe UI", 16, "bold")
        tk.Button(nav, text="1. Основні властивості", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_intro).pack(side="left", padx=20)
        tk.Button(nav, text="2. Розподільна властивість", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_distributive).pack(side="left", padx=20)
        tk.Button(nav, text="3. Тренажер: Зручні обчислення", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_rational_trainer).pack(side="left", padx=20)

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
        f.pack(expand=True, fill="both", padx=50, pady=50)
        
        tk.Label(f, text="Закони множення", font=("Segoe UI", 36, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20))
        
        props = [
            ("Переставна властивість", "Від перестановки множників добуток не змінюється.", "a ∙ b = b ∙ a", "6 ∙ 5 = 5 ∙ 6 = 30"),
            ("Сполучна властивість", "Щоб добуток двох чисел помножити на третє число, можна перше число помножити на добуток другого і третього.", "(a ∙ b) ∙ c = a ∙ (b ∙ c)", "(5 ∙ 6) ∙ 2 = 5 ∙ (6 ∙ 2) = 60"),
            ("Множення на 10, 100, 1000...", "Щоб помножити число на розрядну одиницю, треба дописати до нього стільки нулів, скільки їх у розрядній одиниці.", "54 ∙ 100 = 5400", "237 ∙ 1000 = 237 000")
        ]

        for title, rule, formula, example in props:
            p_frame = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=20, pady=15)
            p_frame.pack(fill="x", pady=8)
            
            tk.Label(p_frame, text=title, font=("Segoe UI", 22, "bold"), bg=WHITE, fg=ACCENT).pack(anchor="w")
            tk.Label(p_frame, text=rule, font=("Segoe UI", 16), bg=WHITE, fg=TEXT).pack(anchor="w", pady=2)
            tk.Label(p_frame, text=formula, font=("Consolas", 20, "bold"), bg=YELLOW_BG, fg=HL_FG, padx=10).pack(anchor="w", pady=2)
            tk.Label(p_frame, text=f"Приклад: {example}", font=("Segoe UI", 16, "italic"), bg=WHITE, fg=MUTED).pack(anchor="w")

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 2: DISTRIBUTIVE PROPERTY
    # ══════════════════════════════════════════════════════════════════
    def show_distributive(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=50)
        
        tk.Label(f, text="Розподільна властивість множення", font=("Segoe UI", 36, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20))
        
        props = [
            ("Відносно додавання", "Щоб помножити суму на число, можна помножити на це число кожний доданок і отримані добутки додати.", "(a + b) ∙ c = a ∙ c + b ∙ c", "49 ∙ 113 + 51 ∙ 113 = (49 + 51) ∙ 113 = 11 300"),
            ("Відносно віднімання", "Щоб помножити різницю на число, можна помножити на це число зменшуване і від'ємник окремо і від першого добутку відняти другий.", "(a – b) ∙ c = a ∙ c – b ∙ c", "97 ∙ 18 = (100 – 3) ∙ 18 = 1800 – 54 = 1746")
        ]

        for title, rule, formula, example in props:
            p_frame = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=20, pady=20)
            p_frame.pack(fill="x", pady=10)
            
            tk.Label(p_frame, text=title, font=("Segoe UI", 24, "bold"), bg=WHITE, fg=ORANGE).pack(anchor="w")
            tk.Label(p_frame, text=rule, font=("Segoe UI", 18), bg=WHITE, fg=TEXT).pack(anchor="w", pady=5)
            tk.Label(p_frame, text=formula, font=("Consolas", 22, "bold"), bg=YELLOW_BG, fg=HL_FG, padx=10).pack(anchor="w", pady=5)
            tk.Label(p_frame, text=f"Приклад: {example}", font=("Segoe UI", 18, "italic"), bg=WHITE, fg=MUTED).pack(anchor="w")

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 3: RATIONAL MULTIPLICATION TRAINER
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
        tk.Label(left, text="Тренажер: Раціональне множення", font=("Segoe UI", 36, "bold"), bg=BG, fg=TEXT).pack(pady=(40, 0))
        tk.Label(left, text="Використовуй властивості множення, щоб рахувати зручно!", font=("Segoe UI", 18), bg=BG, fg=MUTED).pack(pady=5)

        # Task Box
        task_box = tk.Frame(left, bg=WHITE, bd=3, relief="solid", padx=40, pady=30)
        task_box.pack(pady=30)
        
        self.task_text = tk.Label(task_box, text="", font=("Segoe UI", 42, "bold"), bg=WHITE, fg=TEXT)
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
        kbd.pack(pady=20)

        self.kbd_buttons = []
        BTN_W, BTN_H = 6, 2
        FONT_KBD = ("Segoe UI", 22, "bold")
        
        rows = [["7","8","9"], ["4","5","6"], ["1","2","3"], ["C","0","⌫"]]
        for row in rows:
            r = tk.Frame(kbd, bg=BG)
            r.pack(pady=5)
            for ch in row:
                is_del = ch in ("⌫", "C")
                btn = tk.Button(r, text=ch, bg="#fee2e2" if is_del else BTN_NUM, fg=RED if is_del else TEXT,
                                font=FONT_KBD, width=BTN_W, height=BTN_H, relief="flat", bd=0, cursor="hand2",
                                command=lambda c=ch: self._key_press(c))
                btn.pack(side="left", padx=6)
                self.kbd_buttons.append(btn)

        # Bottom buttons
        btn_f = tk.Frame(left, bg=BG)
        btn_f.pack(pady=20)

        self.btn_ok = tk.Button(btn_f, text="✓ Перевірити", bg=GREEN, fg=WHITE, font=("Segoe UI", 18, "bold"),
                                relief="flat", bd=0, cursor="hand2", padx=40, pady=15, command=self.check_answer)
        self.btn_ok.pack(side="left", padx=20)

        self.btn_next = tk.Button(btn_f, text="▶ Наступне", bg=ACCENT, fg=WHITE, font=("Segoe UI", 18, "bold"),
                                  relief="flat", bd=0, cursor="hand2", padx=40, pady=15, command=self.next_task)

        # ── права частина (правила та рахунок)
        right = tk.Frame(self.main_area, bg=PANEL, width=RW, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        rpad = tk.Frame(right, bg=PANEL)
        rpad.pack(fill="both", expand=True, padx=30, pady=40)

        tk.Label(rpad, text="Зручні способи", bg=PANEL, fg=MUTED, font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0,10))
        hint_box = tk.Frame(rpad, bg="#eff6ff", highlightbackground="#bfdbfe", highlightthickness=1, padx=15, pady=15)
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
        tk.Label(hint_box, text=hint_text, bg="#eff6ff", fg=TEXT, font=("Segoe UI", 14), justify="left", anchor="w").pack(fill="x")

        # Score
        self.lbl_score = tk.Label(rpad, text="Рахунок: 0 / 0", font=("Segoe UI", 24, "bold"), bg=PANEL, fg=ACCENT)
        self.lbl_score.pack(side="bottom", pady=40)

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
