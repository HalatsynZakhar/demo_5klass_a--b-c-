"""
Демонстрація: Ділення натуральних чисел (§ 9).
Для 5 класу.
Ділення на розрядну одиницю, окремі випадки, неможливість ділення на нуль.
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
CYAN      = "#0891b2"

# ══════════════════════════════════════════════════════════════════
#  ГОЛОВНИЙ КЛАС
# ══════════════════════════════════════════════════════════════════
class DivisionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ділення натуральних чисел")
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
        
        tk.Label(hdr, text="Ділення натуральних чисел (§ 9)", bg=ACCENT, fg=WHITE, font=("Segoe UI", 20, "bold")).pack(side="left", padx=30)
        tk.Button(hdr, text="❌ Вихід", font=("Arial", 14, "bold"), bg=RED, fg=WHITE, bd=0, command=self.destroy).pack(side="right", padx=20)
        
        # ── Navigation Menu (Reduced height 60 -> 50)
        nav = tk.Frame(self, bg=WHITE, height=50)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        
        btn_font = ("Segoe UI", 12, "bold") # Reduced from 16
        tk.Button(nav, text="1. Що таке ділення?", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_intro).pack(side="left", padx=20)
        tk.Button(nav, text="2. На нуль ділити не можна!", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_zero_warning).pack(side="left", padx=20)
        tk.Button(nav, text="3. Окремі випадки", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_special_cases).pack(side="left", padx=20)
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
    #  SCENE 1: INTRODUCTION
    # ══════════════════════════════════════════════════════════════════
    def show_intro(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=30) # Reduced from 50
        
        tk.Label(f, text="Ділення як обернена дія до множення", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20)) # Reduced from 36
        
        box = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=20, pady=20) # Reduced padding
        box.pack(pady=15)
        
        tk.Label(box, text="48 : 6 = 8, оскільки 8 ∙ 6 = 48", font=("Consolas", 24, "bold"), bg=WHITE, fg=TEXT).pack(anchor="w") # Reduced from 32
        tk.Label(box, text="Ділене : Дільник = Частка", font=("Segoe UI", 18, "bold"), bg=WHITE, fg=ACCENT).pack(anchor="w", pady=(15, 0)) # Reduced from 24

        desc = (
            "• Частка показує, у скільки разів ділене більше за дільник.\n"
            "• Якщо дільник > 1, то ділення означає зменшення числа в кілька разів.\n"
            "• Правильність ділення завжди можна перевірити множенням."
        )
        tk.Label(f, text=desc, font=("Segoe UI", 18), bg=BG, fg=TEXT, justify="left").pack(pady=20) # Reduced from 24

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 2: ZERO WARNING
    # ══════════════════════════════════════════════════════════════════
    def show_zero_warning(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=30) # Reduced from 50
        
        tk.Label(f, text="❗️ На нуль ділити не можна!", font=("Segoe UI", 32, "bold"), bg=BG, fg=RED).pack(pady=(0, 20)) # Reduced from 48
        
        box = tk.Frame(f, bg=RED_BG, bd=3, relief="solid", padx=30, pady=20) # Reduced padding
        box.pack(pady=15)
        
        logic = (
            "Чому це так?\n\n"
            "Припустимо, що 5 : 0 = b.\n"
            "Тобі за правилом перевірки: b ∙ 0 = 5.\n"
            "Але ми знаємо, що будь-яке число при множенні на 0 дає 0!\n\n"
            "❌ Рівність b ∙ 0 = 5 неможлива.\n"
            "Отже, ділення на нуль не має смислу."
        )
        tk.Label(box, text=logic, font=("Segoe UI", 18), bg=RED_BG, fg=TEXT, justify="left").pack() # Reduced from 24

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 3: SPECIAL CASES
    # ══════════════════════════════════════════════════════════════════
    def show_special_cases(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=20) # Reduced from 50
        
        tk.Label(f, text="Окремі випадки ділення", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20)) # Reduced from 36
        
        cases = [
            ("Число на саме себе", "а : а = 1", "7 : 7 = 1", "Будь-яке число (крім 0), поділене на себе, дає 1."),
            ("Число на одиницю", "а : 1 = а", "125 : 1 = 125", "Будь-яке число при діленні на 1 не змінюється."),
            ("Нуль на число", "0 : а = 0", "0 : 5 = 0", "Якщо нуль поділити на будь-яке натуральне число, отримаємо нуль."),
            ("Ділення на 10, 100...", "270 : 10 = 27", "38000 : 100 = 380", "Просто відкидаємо стільки нулів, скільки їх у дільнику.")
        ]
        
        for title, formula, example, desc in cases:
            p_frame = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=15, pady=10) # Reduced padding
            p_frame.pack(fill="x", pady=4) # Reduced pady
            
            h_f = tk.Frame(p_frame, bg=WHITE)
            h_f.pack(fill="x")
            tk.Label(h_f, text=title, font=("Segoe UI", 14, "bold"), bg=WHITE, fg=CYAN).pack(side="left") # Reduced from 18
            tk.Label(h_f, text=formula, font=("Consolas", 18, "bold"), bg=YELLOW_BG, fg=HL_FG, padx=10).pack(side="right") # Reduced from 22
            
            tk.Label(p_frame, text=f"{desc} Приклад: {example}", font=("Segoe UI", 14), bg=WHITE, fg=TEXT).pack(anchor="w", pady=(2, 0)) # Reduced from 16

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

        # Task Box
        self.task_box = tk.Frame(left, bg=WHITE, bd=3, relief="solid", padx=20, pady=20) # Reduced padding
        self.task_box.pack(pady=20) # Reduced from 50
        
        self.task_text = tk.Label(self.task_box, text="", font=("Segoe UI", 32, "bold"), bg=WHITE, fg=TEXT) # Reduced from 48
        self.task_text.pack()

        # Input display
        self.display_frame = tk.Frame(left, bg=WHITE, highlightbackground=ACCENT, highlightthickness=2)
        self.display_frame.pack(pady=5, ipadx=16, ipady=4) # Reduced padding/margin
        
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
            r.pack(pady=2)
            for ch in row:
                btn = tk.Button(r, text=ch, bg=RED_BG if ch in ("⌫", "C") else BTN_NUM, font=("Segoe UI", 16, "bold"), width=6, height=1, relief="flat", command=lambda c=ch: self._key_press(c)) # Reduced from 22/2
                btn.pack(side="left", padx=4)
                self.kbd_buttons.append(btn)

        # Bottom buttons
        btn_f = tk.Frame(left, bg=BG)
        btn_f.pack(pady=10)

        self.btn_ok = tk.Button(btn_f, text="✓ Перевірити", bg=GREEN, fg=WHITE, font=("Segoe UI", 14, "bold"),
                                relief="flat", bd=0, cursor="hand2", padx=30, pady=10, command=self.check_answer) # Reduced font & padding
        self.btn_ok.pack(side="left", padx=10)

        self.btn_next = tk.Button(btn_f, text="▶ Наступне", bg=ACCENT, fg=WHITE, font=("Segoe UI", 14, "bold"),
                                  relief="flat", bd=0, cursor="hand2", padx=30, pady=10, command=self.next_task)

        # Right side
        right = tk.Frame(self.main_area, bg=PANEL, width=RW, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        rpad = tk.Frame(right, bg=PANEL)
        rpad.pack(fill="both", expand=True, padx=15, pady=20) # Reduced from 30/40

        tk.Label(rpad, text="Підказка", font=("Segoe UI", 14, "bold"), bg=PANEL).pack(anchor="w") # Reduced from 18
        hint_box = tk.Frame(rpad, bg="#eff6ff", highlightbackground="#bfdbfe", highlightthickness=1, padx=10, pady=10)
        hint_box.pack(fill="x", pady=5)
        
        tk.Label(hint_box, text="• 0 : а = 0\n• а : а = 1\n• а : 1 = а\n• 250 : 10 = 25", font=("Segoe UI", 12), bg="#eff6ff", justify="left").pack() # Reduced from 16

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

        # Task types: special cases, power of 10, simple division
        task_type = random.choice(["special", "power10", "simple"])
        
        if task_type == "special":
            case = random.choice(["0_div", "a_div_a", "a_div_1"])
            a = random.randint(2, 999)
            if case == "0_div":
                expr = f"0 : {a}"
                ans = 0
            elif case == "a_div_a":
                expr = f"{a} : {a}"
                ans = 1
            else:
                expr = f"{a} : 1"
                ans = a
        elif task_type == "power10":
            ans = random.randint(11, 999)
            p = random.choice([10, 100, 1000])
            expr = f"{ans * p} : {p}"
        else: # simple division
            ans = random.randint(2, 20)
            b = random.randint(2, 12)
            expr = f"{ans * b} : {b}"

        self.task = {"expr": expr, "ans": ans}
        self.task_text.config(text=expr + " = ?")

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
    app = DivisionApp()
    app.mainloop()
