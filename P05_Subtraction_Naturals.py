"""
Демонстрація: Віднімання натуральних чисел (§ 5).
Для 5 класу.
Основные властивості віднімання: віднімання суми від числа, числа від суми, окремі випадки.
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
class SubtractionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Віднімання натуральних чисел")
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
        
        tk.Label(hdr, text="Віднімання натуральних чисел (§ 5)", bg=ACCENT, fg=WHITE, font=("Segoe UI", 20, "bold")).pack(side="left", padx=30)
        tk.Button(hdr, text="❌ Вихід", font=("Arial", 14, "bold"), bg=RED, fg=WHITE, bd=0, command=self.destroy).pack(side="right", padx=20)
        
        # ── Navigation Menu (Reduced height 60 -> 50)
        nav = tk.Frame(self, bg=WHITE, height=50)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        
        btn_font = ("Segoe UI", 12, "bold") # Reduced from 16
        tk.Button(nav, text="1. Поняття віднімання", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_intro).pack(side="left", padx=20)
        tk.Button(nav, text="2. Властивості віднімання", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_properties).pack(side="left", padx=20)
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
    #  SCENE 1: INTRO & DEFINITION
    # ══════════════════════════════════════════════════════════════════
    def show_intro(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=30) # Reduced from 50
        
        tk.Label(f, text="Що таке віднімання?", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20)) # Reduced from 36
        
        desc = (
            "Віднімання — це дія, за допомогою якої за відомою сумою і одним із доданків знаходять другий доданок.\n\n"
            "a - b = c\n"
            "a — зменшуване, b — від'ємник, c — різниця.\n\n"
            "❗️ Різниця показує, на скільки перше число більше за друге.\n\n"
            "Окремі випадки:\n"
            "• a - 0 = a (віднімання нуля не змінює число)\n"
            "• a - a = 0 (віднімання числа від самого себе дає нуль)\n\n"
            "Віднімати можна усно або письмово («стовпчиком»)."
        )
        
        tk.Label(f, text=desc, font=("Segoe UI", 18), bg=BG, fg=TEXT, justify="left", wraplength=self.SW-100).pack(anchor="w") # Reduced from 24

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 2: PROPERTIES
    # ══════════════════════════════════════════════════════════════════
    def show_properties(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=30) # Reduced from 50
        
        tk.Label(f, text="Властивості віднімання", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20)) # Reduced from 36
        
        props = [
            ("Віднімання суми від числа", "Щоб відняти суму від числа, можна відняти від нього один доданок, а потім від результату — інший.", "a – (b + c) = (a – b) – c", "225 – (125 + 37) = (225 – 125) – 37 = 100 – 37 = 63"),
            ("Віднімання числа від суми", "Щоб відняти число від суми, можна відняти його від одного з доданків і до результату додати інший доданок.", "(a + b) – c = (a – c) + b", "(432 + 729) – 232 = (432 – 232) + 729 = 200 + 729 = 929")
        ]

        for title, rule, formula, example in props:
            p_frame = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=15, pady=15) # Reduced padding
            p_frame.pack(fill="x", pady=5) # Reduced pady
            
            tk.Label(p_frame, text=title, font=("Segoe UI", 20, "bold"), bg=WHITE, fg=ACCENT).pack(anchor="w") # Reduced from 24
            tk.Label(p_frame, text=rule, font=("Segoe UI", 16), bg=WHITE, fg=TEXT).pack(anchor="w", pady=2) # Reduced from 18
            tk.Label(p_frame, text=formula, font=("Consolas", 20, "bold"), bg=YELLOW_BG, fg=HL_FG, padx=10).pack(anchor="w", pady=2) # Reduced from 22
            tk.Label(p_frame, text=f"Приклад: {example}", font=("Segoe UI", 16, "italic"), bg=WHITE, fg=MUTED).pack(anchor="w") # Reduced from 18

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 3: RATIONAL SUBTRACTION TRAINER
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
        tk.Label(left, text="Тренажер: Раціональне віднімання", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(20, 0)) # Reduced from 36
        tk.Label(left, text="Використовуй властивості віднімання для зручних обчислень!", font=("Segoe UI", 14), bg=BG, fg=MUTED).pack(pady=2) # Reduced from 18

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
        BTN_W, BTN_H = 6, 1 # Reduced from 2
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
            "1. Віднімання суми:\n"
            "a – (b + c) = (a – b) – c\n"
            "Знайди доданок, який зручно відняти від зменшуваного!\n\n"
            "2. Віднімання від суми:\n"
            "(a + b) – c = (a – c) + b\n"
            "Знайди число в дужках, від якого зручно відняти від'ємник!"
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
        
        task_type = random.choice(["sub_sum", "sub_from_sum", "simple", "zero"])
        
        if task_type == "zero":
            a = random.randint(100, 9999)
            if random.random() < 0.5:
                expr = f"{a} - 0"
                ans = a
            else:
                expr = f"{a} - {a}"
                ans = 0
        elif task_type == "sub_sum":
            # a - (b + c) where a - b is a round number
            round_val = random.choice([100, 200, 500, 1000])
            b = random.randint(50, 400)
            a = round_val + b
            c = random.randint(10, 90)
            if random.random() < 0.5:
                expr = f"{a} - ({b} + {c})"
            else:
                expr = f"{a} - ({c} + {b})"
            ans = a - (b + c)
        elif task_type == "sub_from_sum":
            # (a + b) - c where a - c is a round number
            round_val = random.choice([100, 200, 500, 1000])
            c = random.randint(50, 400)
            a = round_val + c
            b = random.randint(10, 90)
            if random.random() < 0.5:
                expr = f"({a} + {b}) - {c}"
            else:
                expr = f"({b} + {a}) - {c}"
            ans = (a + b) - c
        else: # simple
            a = random.randint(100, 999)
            b = random.randint(10, a)
            expr = f"{a} - {b}"
            ans = a - b

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
    app = SubtractionApp()
    app.mainloop()
