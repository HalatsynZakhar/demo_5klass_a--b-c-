"""
Демонстрація: Ділення з остачею (§ 10).
Для 5 класу.
Поняття остачі, неповна частка, формула ділення з остачею.
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
TEAL      = "#0d9488"

# ══════════════════════════════════════════════════════════════════
#  ГОЛОВНИЙ КЛАС
# ══════════════════════════════════════════════════════════════════
class RemainderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ділення з остачею")
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
        self.user_q = "" # неповна частка
        self.user_r = "" # остача
        self.focus_field = "q" # "q" or "r"
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
        
        tk.Label(hdr, text="Ділення з остачею (§ 10)", bg=ACCENT, fg=WHITE, font=("Segoe UI", 24, "bold")).pack(side="left", padx=30)
        tk.Button(hdr, text="❌ Вихід", font=("Arial", 16, "bold"), bg=RED, fg=WHITE, bd=0, command=self.destroy).pack(side="right", padx=20)
        
        # ── Navigation Menu
        nav = tk.Frame(self, bg=WHITE, height=60)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        
        btn_font = ("Segoe UI", 16, "bold")
        tk.Button(nav, text="1. Що таке остача?", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_intro).pack(side="left", padx=20)
        tk.Button(nav, text="2. Формула ділення", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_formula).pack(side="left", padx=20)
        tk.Button(nav, text="3. Тренажер", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_trainer).pack(side="left", padx=20)

        # ── Main Content Area
        self.main_area = tk.Frame(self, bg=BG)
        self.main_area.pack(fill="both", expand=True)

    def clear_main(self):
        for w in self.main_area.winfo_children():
            w.destroy()

    def _on_key_press(self, event):
        if event.char.isdigit():
            self._key_press(event.char)
        elif event.keysym == "Tab":
            self.focus_field = "r" if self.focus_field == "q" else "q"
            self._update_display()

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 1: INTRODUCTION
    # ══════════════════════════════════════════════════════════════════
    def show_intro(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=50)
        
        tk.Label(f, text="Ділення з остачею", font=("Segoe UI", 36, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 30))
        
        box = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=40, pady=30)
        box.pack(pady=20)
        
        tk.Label(box, text="19 яблук поділити на 5 дітей:", font=("Segoe UI", 24), bg=WHITE, fg=MUTED).pack(anchor="w")
        tk.Label(box, text="19 : 5 = 3 (ост. 4)", font=("Consolas", 48, "bold"), bg=WHITE, fg=TEXT).pack(anchor="w", pady=20)
        
        desc = (
            "• Кожна дитина отримає по 3 яблука (неповна частка).\n"
            "• 4 яблука залишиться (остача).\n\n"
            "❗️ ВАЖЛИВО: Остача завжди має бути МЕНШОЮ за дільник!\n"
            "4 < 5 — правильно."
        )
        tk.Label(f, text=desc, font=("Segoe UI", 24), bg=BG, fg=TEXT, justify="left").pack(pady=30)

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 2: FORMULA
    # ══════════════════════════════════════════════════════════════════
    def show_formula(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=50)
        
        tk.Label(f, text="Формула ділення з остачею", font=("Segoe UI", 36, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 30))
        
        box = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=50, pady=40)
        box.pack(pady=20)
        
        tk.Label(box, text="a = b ∙ q + r", font=("Consolas", 64, "bold"), bg=YELLOW_BG, fg=HL_FG, padx=20).pack()
        
        desc = (
            "a — ділене\n"
            "b — дільник\n"
            "q — неповна частка\n"
            "r — остача (r < b)\n\n"
            "Приклад: 19 = 5 ∙ 3 + 4"
        )
        tk.Label(f, text=desc, font=("Segoe UI", 24), bg=BG, fg=TEXT, justify="left").pack(pady=30)

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 3: TRAINER
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

        # Input display area
        input_area = tk.Frame(left, bg=BG)
        input_area.pack(pady=10)

        # Quotient field
        q_frame_outer = tk.Frame(input_area, bg=BG)
        q_frame_outer.pack(side="left", padx=20)
        tk.Label(q_frame_outer, text="Неповна частка", font=("Segoe UI", 14), bg=BG, fg=MUTED).pack()
        self.q_frame = tk.Frame(q_frame_outer, bg=WHITE, highlightbackground=ACCENT, highlightthickness=2)
        self.q_frame.pack(ipadx=10, ipady=5)
        self.lbl_q = tk.Label(self.q_frame, text="", font=("Segoe UI", 36, "bold"), bg=WHITE, width=5)
        self.lbl_q.pack()
        self.lbl_q.bind("<Button-1>", lambda e: self._set_focus("q"))

        # Remainder field
        r_frame_outer = tk.Frame(input_area, bg=BG)
        r_frame_outer.pack(side="left", padx=20)
        tk.Label(r_frame_outer, text="Остача", font=("Segoe UI", 14), bg=BG, fg=MUTED).pack()
        self.r_frame = tk.Frame(r_frame_outer, bg=WHITE, highlightbackground=BORDER, highlightthickness=2)
        self.r_frame.pack(ipadx=10, ipady=5)
        self.lbl_r = tk.Label(self.r_frame, text="", font=("Segoe UI", 36, "bold"), bg=WHITE, width=5)
        self.lbl_r.pack()
        self.lbl_r.bind("<Button-1>", lambda e: self._set_focus("r"))

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
                btn = tk.Button(r, text=ch, bg=RED_BG if ch in ("⌫", "C") else BTN_NUM, font=("Segoe UI", 20, "bold"), width=5, height=1, relief="flat", command=lambda c=ch: self._key_press(c))
                btn.pack(side="left", padx=4)
                self.kbd_buttons.append(btn)

        # Tab key on screen
        tk.Button(left, text="Переключити поле (Tab)", font=("Segoe UI", 14, "bold"), bg=BTN_NUM, command=lambda: self._set_focus("r" if self.focus_field == "q" else "q")).pack(pady=5)

        # Bottom buttons
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
        
        tk.Label(rpad, text="Правило", font=("Segoe UI", 18, "bold"), bg=PANEL).pack(anchor="w")
        hint_box = tk.Frame(rpad, bg="#f0fdf4", highlightbackground="#bbf7d0", highlightthickness=1, padx=15, pady=15)
        hint_box.pack(fill="x", pady=10)
        tk.Label(hint_box, text="Остача завжди\nменша за дільник!\nr < b", font=("Segoe UI", 16, "bold"), bg="#f0fdf4", fg=GREEN).pack()

        tk.Label(rpad, text="Формула перевірки", font=("Segoe UI", 18, "bold"), bg=PANEL).pack(anchor="w", pady=(20, 0))
        tk.Label(rpad, text="a = b ∙ q + r", font=("Consolas", 20, "bold"), bg=YELLOW_BG).pack(pady=10)

        self.lbl_score = tk.Label(rpad, text="Рахунок: 0 / 0", font=("Segoe UI", 24, "bold"), bg=PANEL, fg=ACCENT)
        self.lbl_score.pack(side="bottom", pady=40)

        self.next_task()

    def _set_focus(self, field):
        if self.phase != "answer": return
        self.focus_field = field
        self._update_display()

    def _update_display(self):
        self.lbl_q.config(text=self.user_q)
        self.lbl_r.config(text=self.user_r)
        self.q_frame.config(highlightbackground=ACCENT if self.focus_field == "q" else BORDER)
        self.r_frame.config(highlightbackground=ACCENT if self.focus_field == "r" else BORDER)

    def _key_press(self, ch):
        if self.phase != "answer": return
        target = "user_q" if self.focus_field == "q" else "user_r"
        current = getattr(self, target)
        
        if ch == "⌫":
            setattr(self, target, current[:-1])
        elif ch == "C":
            setattr(self, target, "")
        else:
            if len(current) < 4:
                setattr(self, target, current + ch)
        
        self._update_display()

    def next_task(self):
        self.user_q = ""
        self.user_r = ""
        self.focus_field = "q"
        self.phase = "answer"
        self.btn_next.pack_forget()
        self.btn_ok.pack(side="left", padx=20)
        
        b = random.randint(3, 15)
        q = random.randint(1, 12)
        r = random.randint(1, b - 1)
        a = b * q + r
        
        self.task = {"a": a, "b": b, "q": q, "r": r}
        self.task_text.config(text=f"{a} : {b} = ?")
        self._update_display()
        self.lbl_feedback.config(text="")
        self.q_frame.config(bg=WHITE)
        self.r_frame.config(bg=WHITE)
        self.lbl_q.config(bg=WHITE)
        self.lbl_r.config(bg=WHITE)

    def check_answer(self):
        if self.phase != "answer" or not self.user_q or not self.user_r: return
        self.phase = "feedback"
        self.total += 1
        
        got_q = int(self.user_q)
        got_r = int(self.user_r)
        
        ok_q = (got_q == self.task["q"])
        ok_r = (got_r == self.task["r"])
        
        if ok_q and ok_r:
            self.score += 1
            self.lbl_feedback.config(text="✅ Правильно!", fg=GREEN)
            self.q_frame.config(highlightbackground=GREEN)
            self.r_frame.config(highlightbackground=GREEN)
            self.after(1000, self.next_task)
        else:
            self.lbl_feedback.config(text=f"❌ Помилка! Правильно: {self.task['q']} (ост. {self.task['r']})", fg=RED)
            if not ok_q: self.q_frame.config(highlightbackground=RED)
            if not ok_r: self.r_frame.config(highlightbackground=RED)
            self.btn_ok.pack_forget()
            self.btn_next.pack(side="left", padx=20)

        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")

if __name__ == "__main__":
    app = RemainderApp()
    app.mainloop()
