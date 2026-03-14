"""
Демонстрація: Текстові задачі на рух (§ 13).
Для 5 класу.
Формула відстані, рух по річці, швидкість зближення та віддалення.
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
SKY       = "#0ea5e9"
INDIGO    = "#4f46e5"

# ══════════════════════════════════════════════════════════════════
#  ГОЛОВНИЙ КЛАС
# ══════════════════════════════════════════════════════════════════
class MotionProblemsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Текстові задачі на рух")
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
        
        tk.Label(hdr, text="Задачі на рух (§ 13)", bg=ACCENT, fg=WHITE, font=("Segoe UI", 24, "bold")).pack(side="left", padx=30)
        tk.Button(hdr, text="❌ Вихід", font=("Arial", 16, "bold"), bg=RED, fg=WHITE, bd=0, command=self.destroy).pack(side="right", padx=20)
        
        # ── Navigation Menu
        nav = tk.Frame(self, bg=WHITE, height=60)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        
        btn_font = ("Segoe UI", 12, "bold")
        tk.Button(nav, text="1. Формула відстані", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_intro).pack(side="left", padx=10)
        tk.Button(nav, text="2. Рух по річці", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_river).pack(side="left", padx=10)
        tk.Button(nav, text="3. Рух двох об'єктів", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_two_objects).pack(side="left", padx=10)
        tk.Button(nav, text="4. Тренажер задач", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_trainer).pack(side="left", padx=10)

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
    #  SCENE 1: BASIC FORMULA
    # ══════════════════════════════════════════════════════════════════
    def show_intro(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=30)
        
        tk.Label(f, text="Формула відстані", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20))
        
        box = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=40, pady=30)
        box.pack(pady=10)
        
        tk.Label(box, text="s — відстань (шлях)\nV — швидкість руху\nt — час руху", font=("Segoe UI", 20), bg=WHITE, justify="left").pack(side="left", padx=40)
        
        f_box = tk.Frame(box, bg=YELLOW_BG, padx=30, pady=20)
        f_box.pack(side="left", padx=40)
        tk.Label(f_box, text="s = V ∙ t", font=("Consolas", 48, "bold"), bg=YELLOW_BG, fg=ACCENT).pack()
        tk.Label(f_box, text="V = s : t\nt = s : V", font=("Consolas", 24), bg=YELLOW_BG, fg=TEXT).pack()

        desc = (
            "1. Швидкість вважаємо сталою (незмінною).\n"
            "2. Одиниці вимірювання швидкості залежать від умови:\n"
            "   • км/год (кілометри за годину)\n"
            "   • м/хв (метри за хвилину)\n"
            "   • м/с (метри за секунду)\n\n"
            "Приклад: Жук за 5 хв проповз 10 м.\n"
            "V = 10 : 5 = 2 (м/хв)."
        )
        tk.Label(f, text=desc, font=("Segoe UI", 20), bg=BG, fg=TEXT, justify="left").pack(pady=30)

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 2: RIVER MOTION
    # ══════════════════════════════════════════════════════════════════
    def show_river(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=30)
        
        tk.Label(f, text="Рух по річці", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20))
        
        cards = tk.Frame(f, bg=BG)
        cards.pack(pady=10)
        
        # Downstream
        c1 = tk.Frame(cards, bg="#eff6ff", bd=2, relief="solid", padx=30, pady=20)
        c1.pack(side="left", padx=20, fill="both", expand=True)
        tk.Label(c1, text="За течією", font=("Segoe UI", 24, "bold"), bg="#eff6ff", fg=SKY).pack()
        tk.Label(c1, text="Швидкість збільшується\nна швидкість течії", font=("Segoe UI", 16), bg="#eff6ff").pack(pady=10)
        tk.Label(c1, text="V за теч. = V влас. + V теч.", font=("Consolas", 18, "bold"), bg=WHITE, padx=10).pack(pady=10)
        tk.Label(c1, text="Приклад: 15 + 2 = 17 км/год", font=("Segoe UI", 14, "italic"), bg="#eff6ff", fg=MUTED).pack()

        # Upstream
        c2 = tk.Frame(cards, bg="#fef2f2", bd=2, relief="solid", padx=30, pady=20)
        c2.pack(side="left", padx=20, fill="both", expand=True)
        tk.Label(c2, text="Проти течії", font=("Segoe UI", 24, "bold"), bg="#fef2f2", fg=RED).pack()
        tk.Label(c2, text="Швидкість зменшується\nна швидкість течії", font=("Segoe UI", 16), bg="#fef2f2").pack(pady=10)
        tk.Label(c2, text="V пр. теч. = V влас. - V теч.", font=("Consolas", 18, "bold"), bg=WHITE, padx=10).pack(pady=10)
        tk.Label(c2, text="Приклад: 15 - 2 = 13 км/год", font=("Segoe UI", 14, "italic"), bg="#fef2f2", fg=MUTED).pack()

        # Canvas for small animation/diagram
        cv = tk.Canvas(f, bg=WHITE, height=200, bd=1, relief="ridge")
        cv.pack(fill="x", pady=20, padx=50)
        
        # 1. Downstream diagram
        cv.create_text(150, 30, text="ЗА ТЕЧІЄЮ (додаємо)", font=("Segoe UI", 12, "bold"), fill=SKY)
        cv.create_rectangle(50, 50, self.SW-100, 80, fill="#e0f2fe", outline="")
        cv.create_line(100, 65, 200, 65, arrow="last", width=3, fill=SKY) # River arrow
        # Boat
        cv.create_polygon(300, 55, 360, 55, 350, 75, 310, 75, fill=ORANGE)
        cv.create_line(365, 65, 420, 65, arrow="last", width=4, fill=ORANGE) # Boat arrow
        
        # 2. Upstream diagram
        cv.create_text(150, 120, text="ПРОТИ ТЕЧІЇ (віднімаємо)", font=("Segoe UI", 12, "bold"), fill=RED)
        cv.create_rectangle(50, 140, self.SW-100, 170, fill="#e0f2fe", outline="")
        cv.create_line(100, 155, 200, 155, arrow="last", width=3, fill=SKY) # River arrow
        # Boat (pointing left)
        cv.create_polygon(400, 145, 340, 145, 350, 165, 390, 165, fill=ORANGE)
        cv.create_line(335, 155, 280, 155, arrow="last", width=4, fill=ORANGE) # Boat arrow (against current)

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 3: TWO OBJECTS
    # ══════════════════════════════════════════════════════════════════
    def show_two_objects(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=10)
        
        tk.Label(f, text="Рух двох об'єктів", font=("Segoe UI", 28, "bold"), bg=BG).pack()
        
        # We'll use a scrollable frame or a grid with diagrams
        container = tk.Frame(f, bg=BG)
        container.pack(fill="both", expand=True, pady=10)
        
        # 1. Towards each other
        self._create_motion_card(container, 0, 0, "1. Назустріч", 
                                 "V збл. = V₁ + V₂", 
                                 "Об'єкти зближуються.\nЩоб знайти швидкість зближення, швидкості додаємо.", 
                                 "s = (V₁ + V₂) ∙ t", 
                                 "towards")

        # 2. Opposite directions
        self._create_motion_card(container, 0, 1, "2. У протилежні сторони", 
                                 "V від. = V₁ + V₂", 
                                 "Об'єкти віддаляються.\nЩоб знайти швидкість віддалення, швидкості додаємо.", 
                                 "s = (V₁ + V₂) ∙ t", 
                                 "opposite")

        # 3. Chase (Catch up)
        self._create_motion_card(container, 1, 0, "3. Навздогін (V₁ > V₂)", 
                                 "V збл. = V₁ - V₂", 
                                 "Той, хто позаду, наздоганяє.\nШвидкість зближення — це різниця швидкостей.", 
                                 "s = (V₁ - V₂) ∙ t", 
                                 "chase")

        # 4. Same direction (Away)
        self._create_motion_card(container, 1, 1, "4. В одному напрямку (V₁ > V₂)", 
                                 "V від. = V₁ - V₂", 
                                 "Той, хто попереду, тікає швидше.\nШвидкість віддалення — це різниця швидкостей.", 
                                 "s = (V₁ - V₂) ∙ t", 
                                 "away")

    def _create_motion_card(self, parent, r, c, title, formula, desc, s_formula, m_type):
        card = tk.Frame(parent, bg=WHITE, bd=2, relief="solid", padx=10, pady=10)
        card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        parent.grid_columnconfigure(c, weight=1)
        parent.grid_rowconfigure(r, weight=1)

        tk.Label(card, text=title, font=("Segoe UI", 16, "bold"), bg=WHITE, fg=INDIGO).pack()
        
        # Canvas for diagram
        cv = tk.Canvas(card, bg=WHITE, height=80, highlightthickness=0)
        cv.pack(fill="x", pady=5)
        
        # Draw base line
        w = 300
        cv.create_line(20, 50, w-20, 50, fill=MUTED, dash=(4, 4))
        
        if m_type == "towards":
            # Two objects moving towards each other
            cv.create_oval(50, 40, 70, 60, fill=ACCENT) # Obj 1
            cv.create_line(75, 50, 120, 50, arrow="last", width=3, fill=ACCENT)
            cv.create_oval(w-70, 40, w-50, 60, fill=ORANGE) # Obj 2
            cv.create_line(w-75, 50, w-120, 50, arrow="last", width=3, fill=ORANGE)
        elif m_type == "opposite":
            # Two objects moving apart
            cv.create_oval(w//2-10, 40, w//2+10, 60, fill=MUTED) # Start point
            cv.create_line(w//2-15, 50, w//2-70, 50, arrow="last", width=3, fill=ACCENT)
            cv.create_line(w//2+15, 50, w//2+70, 50, arrow="last", width=3, fill=ORANGE)
        elif m_type == "chase":
            # One chasing another
            cv.create_oval(40, 40, 60, 60, fill=ACCENT) # Chaser
            cv.create_line(65, 50, 140, 50, arrow="last", width=4, fill=ACCENT) # Fast
            cv.create_oval(160, 40, 180, 60, fill=ORANGE) # Chased
            cv.create_line(185, 50, 230, 50, arrow="last", width=2, fill=ORANGE) # Slow
        elif m_type == "away":
            # One moving away faster
            cv.create_oval(40, 40, 60, 60, fill=ORANGE) # Slow
            cv.create_line(65, 50, 110, 50, arrow="last", width=2, fill=ORANGE) # Slow
            cv.create_oval(130, 40, 150, 60, fill=ACCENT) # Fast
            cv.create_line(155, 50, 230, 50, arrow="last", width=4, fill=ACCENT) # Fast

        tk.Label(card, text=formula, font=("Consolas", 16, "bold"), bg=YELLOW_BG).pack(pady=5)
        tk.Label(card, text=desc, font=("Segoe UI", 11), bg=WHITE, justify="center").pack()
        tk.Label(card, text=s_formula, font=("Consolas", 12, "bold"), bg=WHITE, fg=TEXT).pack(pady=5)

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
        self.task_box = tk.Frame(left, bg=WHITE, bd=3, relief="solid", padx=40, pady=40)
        self.task_box.pack(pady=30)
        self.task_text = tk.Label(self.task_box, text="", font=("Segoe UI", 20), bg=WHITE, fg=TEXT, justify="left", wraplength=LW-100)
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
        
        tk.Label(rpad, text="Підказки", font=("Segoe UI", 18, "bold"), bg=PANEL).pack(anchor="w")
        hint_box = tk.Frame(rpad, bg="#eff6ff", highlightbackground="#bfdbfe", highlightthickness=1, padx=15, pady=15)
        hint_box.pack(fill="x", pady=10)
        
        hints = (
            "• s = V ∙ t\n\n"
            "• За течією: Vвлас. + Vтеч.\n"
            "• Проти течії: Vвлас. - Vтеч.\n\n"
            "• Назустріч: V₁ + V₂ (збл.)\n"
            "• У протилежні: V₁ + V₂ (від.)\n"
            "• Навздогін: V₁ - V₂ (збл.)\n"
            "• В одному напр.: V₁ - V₂ (від.)"
        )
        tk.Label(hint_box, text=hints, font=("Segoe UI", 12), bg="#eff6ff", justify="left").pack()

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

        types = ["simple", "river", "meeting", "opposite", "chase"]
        t = random.choice(types)
        
        if t == "simple":
            v = random.randint(60, 95)
            time_val = random.randint(2, 6)
            ans = v * time_val
            text = f"Автомобіль рухався {time_val} год зі швидкістю {v} км/год. Яку відстань він подолав?"
        elif t == "river":
            v_own = random.randint(15, 25)
            v_river = random.randint(2, 4)
            time_val = random.randint(2, 4)
            if random.choice([True, False]): # Downstream
                ans = (v_own + v_river) * time_val
                text = f"Власна швидкість катера {v_own} км/год, а швидкість течії {v_river} км/год. Яку відстань пропливе катер за {time_val} год за течією?"
            else: # Upstream
                ans = (v_own - v_river) * time_val
                text = f"Власна швидкість човна {v_own} км/год, а швидкість течії {v_river} км/год. Яку відстань пропливе човен за {time_val} год проти течії?"
        elif t == "meeting":
            v1 = random.randint(10, 15)
            v2 = random.randint(10, 15)
            time_val = random.randint(2, 4)
            ans = (v1 + v2) * time_val
            text = f"Два велосипедисти виїхали назустріч один одному. Швидкість одного {v1} км/год, іншого — {v2} км/год. Яка відстань була між ними спочатку, якщо вони зустрілися через {time_val} год?"
        elif t == "opposite":
            v1 = random.randint(60, 80)
            v2 = random.randint(60, 80)
            time_val = random.randint(2, 3)
            ans = (v1 + v2) * time_val
            text = f"Два автомобілі виїхали з однієї точки у протилежних напрямках. Швидкість одного {v1} км/год, іншого — {v2} км/год. Яка відстань буде між ними через {time_val} год?"
        else: # chase
            v_slow = random.randint(5, 8)
            v_fast = v_slow + random.randint(2, 5)
            time_val = random.randint(2, 4)
            ans = (v_fast - v_slow) * time_val
            text = f"Хлопчик зі швидкістю {v_fast} км/год наздоганяє дівчинку, яка йде попереду зі швидкістю {v_slow} км/год. На скільки кілометрів скоротиться відстань між ними через {time_val} год?"

        self.task = {"ans": ans, "text": text}
        self.task_text.config(text=text)

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
    app = MotionProblemsApp()
    app.mainloop()
