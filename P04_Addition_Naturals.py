"""
Демонстрація: Додавання натуральних чисел (§ 4).
Для 5 класу.
Основні властивості додавання: переставна, сполучна, додавання нуля.
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
class AdditionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Додавання натуральних чисел")
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
        
        tk.Label(hdr, text="Додавання натуральних чисел (§ 4)", bg=ACCENT, fg=WHITE, font=("Segoe UI", 24, "bold")).pack(side="left", padx=30)
        tk.Button(hdr, text="❌ Вихід", font=("Arial", 16, "bold"), bg=RED, fg=WHITE, bd=0, command=self.destroy).pack(side="right", padx=20)
        
        # ── Navigation Menu
        nav = tk.Frame(self, bg=WHITE, height=60)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        
        btn_font = ("Segoe UI", 16, "bold")
        tk.Button(nav, text="1. Властивості додавання", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_intro).pack(side="left", padx=20)
        tk.Button(nav, text="2. Переставна та Сполучна", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_properties).pack(side="left", padx=20)
        tk.Button(nav, text="3. Раціональне додавання (Тренажер)", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_rational_trainer).pack(side="left", padx=20)

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
    #  SCENE 1: INTRO & ZERO PROPERTY
    # ══════════════════════════════════════════════════════════════════
    def show_intro(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=50)
        
        tk.Label(f, text="Додавання та властивість нуля", font=("Segoe UI", 36, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 30))
        
        desc = (
            "Додавання — це математична дія, за допомогою якої ми знаходимо суму чисел.\n\n"
            "❗️ Властивість нуля:\n"
            "Якщо до будь-якого числа додати нуль, число НЕ зміниться.\n\n"
            "a + 0 = a\n"
            "0 + a = a\n\n"
            "Наприклад:\n"
            "125 + 0 = 125\n"
            "0 + 98 = 98\n\n"
            "Тому додавання 0 не має практичного сенсу, адже результат відомий заздалегідь."
        )
        
        tk.Label(f, text=desc, font=("Segoe UI", 24), bg=BG, fg=TEXT, justify="left", wraplength=self.SW-200).pack(anchor="w")

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 2: PROPERTIES (COMMUTATIVE & ASSOCIATIVE)
    # ══════════════════════════════════════════════════════════════════
    def show_properties(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=50)
        
        tk.Label(f, text="Основні закони додавання", font=("Segoe UI", 36, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 30))
        
        props = [
            ("Переставний закон", "Від перестановки доданків сума не змінюється.", "a + b = b + a", "14 + 23 = 23 + 14 = 37"),
            ("Сполучний закон", "Щоб до суми двох чисел додати третє число, можна до першого числа додати суму другого і третього.", "(a + b) + c = a + (b + c)", "(14 + 86) + 234 = 14 + (86 + 234)")
        ]

        for title, rule, formula, example in props:
            p_frame = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=20, pady=20)
            p_frame.pack(fill="x", pady=10)
            
            tk.Label(p_frame, text=title, font=("Segoe UI", 24, "bold"), bg=WHITE, fg=ACCENT).pack(anchor="w")
            tk.Label(p_frame, text=rule, font=("Segoe UI", 18), bg=WHITE, fg=TEXT).pack(anchor="w", pady=5)
            tk.Label(p_frame, text=formula, font=("Consolas", 22, "bold"), bg=YELLOW_BG, fg=HL_FG, padx=10).pack(anchor="w", pady=5)
            tk.Label(p_frame, text=f"Приклад: {example}", font=("Segoe UI", 18, "italic"), bg=WHITE, fg=MUTED).pack(anchor="w")

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 3: RATIONAL ADDITION TRAINER
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
        tk.Label(left, text="Тренажер: Раціональне додавання", font=("Segoe UI", 36, "bold"), bg=BG, fg=TEXT).pack(pady=(40, 0))
        tk.Label(left, text="Шукай пари чисел, які в сумі дають кругле число!", font=("Segoe UI", 18), bg=BG, fg=MUTED).pack(pady=5)

        # Task Box
        task_box = tk.Frame(left, bg=WHITE, bd=3, relief="solid", padx=40, pady=30)
        task_box.pack(pady=30)
        
        self.task_text = tk.Label(task_box, text="", font=("Segoe UI", 48, "bold"), bg=WHITE, fg=TEXT)
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
        # Packed later when needed

        # ── права частина (правила та рахунок)
        right = tk.Frame(self.main_area, bg=PANEL, width=RW, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        rpad = tk.Frame(right, bg=PANEL)
        rpad.pack(fill="both", expand=True, padx=30, pady=40)

        tk.Label(rpad, text="Порада", bg=PANEL, fg=MUTED, font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0,10))
        hint_box = tk.Frame(rpad, bg="#eff6ff", highlightbackground="#bfdbfe", highlightthickness=1, padx=15, pady=15)
        hint_box.pack(fill="x")
        
        hint_text = (
            "Шукай числа, які закінчуються на:\n"
            "• 1 та 9 (1+9=10)\n"
            "• 2 та 8 (2+8=10)\n"
            "• 3 та 7 (3+7=10)\n"
            "• 4 та 6 (4+6=10)\n"
            "• 5 та 5 (5+5=10)\n\n"
            "Додавай їх спочатку, а потім решту!"
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
        
        # Difficulty scaling
        level = min(5, (self.total // 5) + 1) # Increase difficulty every 5 tasks
        
        # Task types
        task_type = random.choice(["zero", "rational_3", "rational_4", "rational_mixed"])
        
        if task_type == "zero":
            a = random.randint(100, 9999)
            if random.random() < 0.5:
                nums = [a, 0]
            else:
                nums = [0, a]
        elif task_type == "rational_3":
            # Three numbers, two sum to 100 or 1000
            target = random.choice([100, 200, 500, 1000])
            a = random.randint(1, target - 1)
            c = target - a
            b = random.randint(10, 500)
            nums = [a, b, c]
        elif task_type == "rational_4":
            # Four numbers, two pairs sum to round numbers
            t1 = random.choice([50, 100, 200])
            a1 = random.randint(1, t1 - 1)
            a2 = t1 - a1
            
            t2 = random.choice([50, 100, 200])
            b1 = random.randint(1, t2 - 1)
            b2 = t2 - b1
            nums = [a1, b1, a2, b2]
        else: # rational_mixed
            # 4-5 numbers with some zeroes and round pairs
            t = 100
            a = random.randint(1, 99)
            b = 100 - a
            nums = [a, b, 0, random.randint(10, 100), random.randint(10, 100)]
            if level > 3:
                nums.append(random.randint(100, 500))

        random.shuffle(nums)
        self.task = {
            "nums": nums,
            "ans": sum(nums),
            "expr": " + ".join(str(n) for n in nums)
        }
        self.task_text.config(text=self.task["expr"] + " = ?")

    def check_answer(self):
        if self.phase != "answer": return
        raw = self.user_input.strip()
        if not raw:
            return

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
            # Auto-next after 1 second
            self.after(1000, self.next_task)
        else:
            self.lbl_feedback.config(text=f"❌ Помилка! Правильна відповідь: {self.task['ans']}", fg=RED)
            self.lbl_display.config(bg=RED_BG)
            self.display_frame.config(highlightbackground=RED)
            self.btn_ok.pack_forget()
            self.btn_next.pack(side="left", padx=20)

        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")

if __name__ == "__main__":
    app = AdditionApp()
    app.mainloop()
