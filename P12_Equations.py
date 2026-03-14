"""
Демонстрація: Рівняння (§ 12).
Для 5 класу.
Поняття рівняння, корінь рівняння, правила знаходження невідомих компонентів.
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
class EquationsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Рівняння")
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
        
        tk.Label(hdr, text="Рівняння (§ 12)", bg=ACCENT, fg=WHITE, font=("Segoe UI", 24, "bold")).pack(side="left", padx=30)
        tk.Button(hdr, text="❌ Вихід", font=("Arial", 16, "bold"), bg=RED, fg=WHITE, bd=0, command=self.destroy).pack(side="right", padx=20)
        
        # ── Navigation Menu
        nav = tk.Frame(self, bg=WHITE, height=60)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        
        btn_font = ("Segoe UI", 13, "bold")
        tk.Button(nav, text="1. Основні поняття", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_intro).pack(side="left", padx=10)
        tk.Button(nav, text="2. Правила (Додавання/Віднімання)", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_rules_add_sub).pack(side="left", padx=10)
        tk.Button(nav, text="3. Правила (Множення/Ділення)", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_rules_mul_div).pack(side="left", padx=10)
        tk.Button(nav, text="4. Складні рівняння", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_complex_examples).pack(side="left", padx=10)
        tk.Button(nav, text="5. Тренажер", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_trainer).pack(side="left", padx=10)

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
    #  SCENE 1: INTRODUCTION
    # ══════════════════════════════════════════════════════════════════
    def show_intro(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=30)
        
        tk.Label(f, text="Що таке рівняння?", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20))
        
        box = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=40, pady=30)
        box.pack(pady=10)
        
        tk.Label(box, text="Рівняння — це рівність, що містить невідоме число,\nпозначене буквою.", font=("Segoe UI", 20), bg=WHITE, justify="left").pack(anchor="w")
        tk.Label(box, text="x + 14 = 58", font=("Consolas", 36, "bold"), bg=WHITE, fg=ACCENT).pack(pady=20)
        
        desc = (
            "• Корінь (або розв'язок) рівняння — це число, яке при підстановці\n"
            "  замість букви перетворює рівняння на правильну числову рівність.\n"
            "• Розв'язати рівняння — означає знайти всі його корені\n"
            "  або переконатися, що їх немає.\n\n"
            "Перевірка: 44 + 14 = 58; 58 = 58. (Отже, 44 — корінь)"
        )
        tk.Label(f, text=desc, font=("Segoe UI", 20), bg=BG, fg=TEXT, justify="left").pack(pady=20)

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 2: RULES ADD/SUB
    # ══════════════════════════════════════════════════════════════════
    def show_rules_add_sub(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=20)
        
        tk.Label(f, text="Додавання та віднімання", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 15))
        
        rules = [
            ("Невідомий доданок", "x + 14 = 58", "Щоб знайти невідомий доданок,\nтреба від суми відняти відомий доданок.", "x = 58 - 14"),
            ("Невідоме зменшуване", "x - 12 = 37", "Щоб знайти невідоме зменшуване,\nтреба до різниці додати від'ємник.", "x = 37 + 12"),
            ("Невідомий від'ємник", "42 - x = 18", "Щоб знайти невідомий від'ємник,\nтреба від зменшуваного відняти різницю.", "x = 42 - 18")
        ]
        
        for title, formula, rule, step in rules:
            r_f = tk.Frame(f, bg=WHITE, bd=1, relief="solid", padx=20, pady=10)
            r_f.pack(fill="x", pady=5)
            tk.Label(r_f, text=title, font=("Segoe UI", 18, "bold"), bg=WHITE, fg=PURPLE).pack(anchor="w")
            tk.Label(r_f, text=rule, font=("Segoe UI", 15), bg=WHITE, justify="left").pack(anchor="w")
            tk.Label(r_f, text=f"{formula}  →  {step}", font=("Consolas", 20, "bold"), bg=YELLOW_BG).pack(anchor="w", pady=5)

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 3: RULES MUL/DIV
    # ══════════════════════════════════════════════════════════════════
    def show_rules_mul_div(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=20)
        
        tk.Label(f, text="Множення та ділення", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 15))
        
        rules = [
            ("Невідомий множник", "7 ∙ x = 56", "Щоб знайти невідомий множник,\nтреба добуток поділити на відомий множник.", "x = 56 : 7"),
            ("Невідоме ділене", "x : 5 = 9", "Щоб знайти невідоме ділене,\nтреба частку помножити на дільник.", "x = 9 ∙ 5"),
            ("Невідомий дільник", "36 : x = 9", "Щоб знайти невідомий дільник,\nтреба ділене поділити на частку.", "x = 36 : 9")
        ]
        
        for title, formula, rule, step in rules:
            r_f = tk.Frame(f, bg=WHITE, bd=1, relief="solid", padx=20, pady=10)
            r_f.pack(fill="x", pady=5)
            tk.Label(r_f, text=title, font=("Segoe UI", 18, "bold"), bg=WHITE, fg=ORANGE).pack(anchor="w")
            tk.Label(r_f, text=rule, font=("Segoe UI", 15), bg=WHITE, justify="left").pack(anchor="w")
            tk.Label(r_f, text=f"{formula}  →  {step}", font=("Consolas", 20, "bold"), bg=YELLOW_BG).pack(anchor="w", pady=5)

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 4: COMPLEX EXAMPLES
    # ══════════════════════════════════════════════════════════════════
    def show_complex_examples(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=20)
        
        tk.Label(f, text="Розв'язування складних рівнянь", font=("Segoe UI", 28, "bold"), bg=BG).pack(pady=(0, 15))
        
        exs = [
            ("Приклад 1: (x + 27) - 35 = 62", "1) x + 27 = 62 + 35 (шукаємо зменшуване)\n2) x + 27 = 97\n3) x = 97 - 27 (шукаємо доданок)\n4) x = 70"),
            ("Приклад 2: 36 : (x - 18) = 3", "1) x - 18 = 36 : 3 (шукаємо дільник)\n2) x - 18 = 12\n3) x = 12 + 18 (шукаємо зменшуване)\n4) x = 30"),
            ("Приклад 3: 4x + 8x = 36", "1) (4 + 8)x = 36 (спрощуємо вираз)\n2) 12x = 36\n3) x = 36 : 12\n4) x = 3")
        ]
        
        for title, steps in exs:
            e_f = tk.Frame(f, bg=WHITE, bd=1, relief="solid", padx=20, pady=10)
            e_f.pack(fill="x", pady=5)
            tk.Label(e_f, text=title, font=("Segoe UI", 18, "bold"), bg=WHITE, fg=ACCENT).pack(anchor="w")
            tk.Label(e_f, text=steps, font=("Segoe UI", 14), bg=WHITE, justify="left").pack(anchor="w")

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
        self.task_text = tk.Label(self.task_box, text="", font=("Segoe UI", 48, "bold"), bg=WHITE, fg=TEXT)
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
        tk.Label(hint_box, text="Знайди невідомий\nкомпонент за правилом.\nНе забудь зробити\nперевірку!", font=("Segoe UI", 16), bg="#eff6ff", justify="left").pack()

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

        types = ["add", "sub_x", "sub_const", "mul", "div_x", "div_const", "complex"]
        t = random.choice(types)
        
        if t == "add":
            x = random.randint(10, 100)
            const = random.randint(10, 100)
            self.task = {"ans": x, "text": f"x + {const} = {x + const}"}
        elif t == "sub_x":
            x = random.randint(50, 150)
            const = random.randint(10, 40)
            self.task = {"ans": x, "text": f"x - {const} = {x - const}"}
        elif t == "sub_const":
            x = random.randint(10, 50)
            const = random.randint(60, 100)
            self.task = {"ans": x, "text": f"{const} - x = {const - x}"}
        elif t == "mul":
            x = random.randint(2, 12)
            const = random.randint(2, 20)
            self.task = {"ans": x, "text": f"{const} ∙ x = {const * x}"}
        elif t == "div_x":
            x = random.randint(50, 200)
            const = random.randint(2, 10)
            self.task = {"ans": x, "text": f"x : {const} = {x // const}"}
        elif t == "div_const":
            x = random.randint(2, 12)
            const = random.randint(24, 144)
            # ensure divisibility
            ans = const // x
            self.task = {"ans": x, "text": f"{const} : x = {ans}"}
        else: # complex like 4x + 8x = 36 or (x+2)-5=10
            x = random.randint(2, 10)
            a = random.randint(2, 10)
            b = random.randint(2, 10)
            self.task = {"ans": x, "text": f"{a}x + {b}x = {(a+b)*x}"}

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
            self.lbl_feedback.config(text=f"❌ Помилка! Корінь: {self.task['ans']}", fg=RED)
            self.lbl_display.config(bg=RED_BG)
            self.btn_ok.pack_forget()
            self.btn_next.pack(side="left", padx=20)

        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")

if __name__ == "__main__":
    app = EquationsApp()
    app.mainloop()
