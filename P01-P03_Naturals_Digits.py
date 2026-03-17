"""
Демонстрація: Натуральні числа, порівняння та округлення (§ 1-3).
Для 5 класу.
"""

import tkinter as tk
import tkinter.font as tkfont
import math, random
from decimal import Decimal, ROUND_HALF_UP

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
HL_BG     = "#fde68a"   # підсвічений розряд — фон
HL_FG     = "#92400e"   # підсвічений розряд — текст
GREEN_BG  = "#dcfce7"
RED_BG    = "#fee2e2"
WHITE     = "#ffffff"
BTN_NUM   = "#e2e8f0"
BTN_HOV   = "#cbd5e1"
LINE_COL  = "#1e40af"
DOT_ORIG  = "#f59e0b"
DOT_ROUND = "#16a34a"

# ══════════════════════════════════════════════════════════════════
#  ЛОГІКА ОКРУГЛЕННЯ (Тільки натуральні числа)
# ══════════════════════════════════════════════════════════════════
ROUND_SPECS = [
    ("тисяч",    3),
    ("сотень",   2),
    ("десятків", 1),
]

def _round_to_power(number: int, power: int) -> int:
    factor = 10 ** power
    # Standard half-up rounding for integers
    return int((Decimal(number) / Decimal(factor)).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * factor)

def _gen_task():
    name, power = random.choice(ROUND_SPECS)
    if power == 3: # тисяч
        number = random.randint(1000, 99999)
    elif power == 2: # сотень
        number = random.randint(100, 9999)
    else: # десятків
        number = random.randint(10, 999)

    answer = _round_to_power(number, power)
    number_str = str(number)
    
    # --- підсвічування розряду ---
    int_len = len(number_str)
    hi_pos_in_int = int_len - 1 - power
    
    if 0 <= hi_pos_in_int < int_len:
        before = number_str[:hi_pos_in_int]
        hi_ch  = number_str[hi_pos_in_int]
        after  = number_str[hi_pos_in_int+1:]
    else:
        before, hi_ch, after = number_str, "", ""
        
    segments = []
    if before: segments.append((before, False))
    if hi_ch:  segments.append((hi_ch, True))
    if after:  segments.append((after, False))

    return {
        "number":     number,
        "number_str": number_str,
        "answer":     answer,
        "answer_str": str(answer),
        "round_name": name,
        "power":      power,
        "segments":   segments,
    }

# ══════════════════════════════════════════════════════════════════
#  ВІДЖЕТИ
# ══════════════════════════════════════════════════════════════════
class HighlightedNumber(tk.Frame):
    """Відображає число як рядок Label-ів з одним підсвіченим символом."""
    FONT_NORMAL = ("Segoe UI", 32, "bold") # Reduced from 44
    FONT_HL     = ("Segoe UI", 32, "bold") # Reduced from 44

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=YELLOW_BG, **kwargs)
        self._labels = []

    def set_segments(self, segments):
        for lbl in self._labels:
            lbl.destroy()
        self._labels = []
        for text, is_hl in segments:
            if is_hl:
                lbl = tk.Label(self, text=text, bg=HL_BG, fg=HL_FG, font=self.FONT_HL, padx=3, pady=2, relief="flat")
            else:
                lbl = tk.Label(self, text=text, bg=YELLOW_BG, fg=TEXT, font=self.FONT_NORMAL, padx=0, pady=2)
            lbl.pack(side="left")
            self._labels.append(lbl)

# ══════════════════════════════════════════════════════════════════
#  ГОЛОВНИЙ КЛАС
# ══════════════════════════════════════════════════════════════════
class NaturalsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Натуральні числа: Вступ, Порівняння, Округлення")
        self.configure(bg=BG)
        
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        
        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()

        # State
        self.task = None
        self.user_input = ""
        self.phase = "answer"
        self.line_shown = False
        self.highlight_shown = False
        self.score = 0
        self.total = 0
        self.streak = 0

        self._build_ui()
        self.show_intro()

    def _build_ui(self):
        # ── Header (Reduced height 80 -> 60)
        hdr = tk.Frame(self, bg=ACCENT, height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        
        tk.Label(hdr, text="Натуральні числа (§ 1-3)", bg=ACCENT, fg=WHITE, font=("Segoe UI", 20, "bold")).pack(side="left", padx=30)
        tk.Button(hdr, text="❌ Вихід", font=("Arial", 14, "bold"), bg=RED, fg=WHITE, bd=0, command=self.destroy).pack(side="right", padx=20)
        
        # ── Navigation Menu (Reduced height 60 -> 50)
        nav = tk.Frame(self, bg=WHITE, height=50)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        
        btn_font = ("Segoe UI", 12, "bold") # Reduced from 16
        tk.Button(nav, text="1. Що таке натуральні числа?", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_intro).pack(side="left", padx=20)
        tk.Button(nav, text="2. Порівняння", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_comparison).pack(side="left", padx=20)
        tk.Button(nav, text="3. Округлення (Тренажер)", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_rounding).pack(side="left", padx=20)

        # ── Main Content Area
        self.main_area = tk.Frame(self, bg=BG)
        self.main_area.pack(fill="both", expand=True)

    def clear_main(self):
        for w in self.main_area.winfo_children():
            w.destroy()

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 1: INTRO
    # ══════════════════════════════════════════════════════════════════
    def show_intro(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Reduced fonts
        tk.Label(f, text="Що таке натуральні числа?", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20))
        
        desc = (
            "Натуральні числа — це числа, які виникають природним чином при лічбі предметів.\n\n"
            "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ...\n\n"
            "❗️ Важливо пам'ятати:\n"
            "• Найменше натуральне число — 1.\n"
            "• Найбільшого натурального числа не існує.\n"
            "• Нуль (0) НЕ є натуральним числом, бо ми не рахуємо 'нуль яблук'."
        )
        
        tk.Label(f, text=desc, font=("Segoe UI", 18), bg=BG, fg=TEXT, justify="left", wraplength=self.SW-100).pack(anchor="w")

    # ══════════════════════════════════════════════════════════════════
    #  SCENE 2: COMPARISON
    # ══════════════════════════════════════════════════════════════════
    def show_comparison(self):
        self.clear_main()
        
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=30)
        
        tk.Label(f, text="Порівняння натуральних чисел", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20))
        
        rules = tk.Frame(f, bg=WHITE, bd=2, relief="solid")
        rules.pack(fill="x", pady=10, ipadx=15, ipady=15)
        
        tk.Label(rules, text="Правила порівняння:", font=("Segoe UI", 20, "bold"), bg=WHITE, fg=ACCENT).pack(anchor="w")
        tk.Label(rules, text="1. З двох натуральних чисел більше те, у записі якого більше цифр.\n   (Наприклад: 1024 > 999)\n\n2. Якщо кількість цифр однакова, порівнюємо розряди зліва направо.\n   (Наприклад: 5432 > 5399, бо 4 сотні > 3 сотні)", 
                 font=("Segoe UI", 16), bg=WHITE, fg=TEXT, justify="left").pack(anchor="w", pady=5)

        # Interactive quick check
        self.cmp_frame = tk.Frame(f, bg=BG)
        self.cmp_frame.pack(pady=20)
        
        self.gen_cmp_task()

    def gen_cmp_task(self):
        for w in self.cmp_frame.winfo_children(): w.destroy()
        
        # 50% chance for same length
        if random.random() < 0.5:
            a = random.randint(1000, 9999)
            b = random.randint(1000, 9999)
        else:
            a = random.randint(100, 999)
            b = random.randint(1000, 9999)
            if random.random() < 0.5: a, b = b, a
            
        while a == b: b = a + 1
            
        tk.Label(self.cmp_frame, text=f"{a}", font=("Courier New", 40, "bold"), bg=BG).pack(side="left", padx=10)
        
        btn_f = tk.Frame(self.cmp_frame, bg=BG)
        btn_f.pack(side="left", padx=10)
        
        ans = ">" if a > b else "<"
        
        def check(sym):
            if sym == ans:
                res.config(text="✅ Правильно!", fg=GREEN)
                self.after(1000, self.gen_cmp_task)
            else:
                res.config(text="❌ Помилка", fg=RED)
                
        tk.Button(btn_f, text="<", font=("Arial", 28, "bold"), command=lambda: check("<")).pack(side="left", padx=5)
        tk.Button(btn_f, text=">", font=("Arial", 28, "bold"), command=lambda: check(">")).pack(side="left", padx=5)
        
        tk.Label(self.cmp_frame, text=f"{b}", font=("Courier New", 40, "bold"), bg=BG).pack(side="left", padx=10)
        
        res = tk.Label(self.cmp_frame, text="", font=("Segoe UI", 20, "bold"), bg=BG, width=15)
        res.pack(side="left", padx=10)


    # ══════════════════════════════════════════════════════════════════
    #  SCENE 3: ROUNDING (Adapted from P42)
    # ══════════════════════════════════════════════════════════════════
    def show_rounding(self):
        self.clear_main()
        
        LW = int(self.SW * 0.60)
        RW = self.SW - LW

        # ── ліва частина (тренажер)
        left = tk.Frame(self.main_area, bg=BG, width=LW)
        left.pack(side="left", fill="both")
        left.pack_propagate(False)

        # Task Box
        task_box = tk.Frame(left, bg=BG)
        task_box.pack(pady=10) # Reduced from 40

        self.lbl_instruction = tk.Label(task_box, text="", bg=BG, fg=MUTED, font=("Segoe UI", 16), justify="center") # Font 20->16
        self.lbl_instruction.pack()

        num_outer = tk.Frame(task_box, bg=YELLOW_BG, highlightbackground="#fde68a", highlightthickness=2)
        num_outer.pack(pady=(5, 0), ipadx=10, ipady=4)

        self.hl_number = HighlightedNumber(num_outer)
        self.hl_number.pack(padx=5, pady=2)

        self.btn_hl = tk.Button(task_box, text="💡 Показати розряд", bg=WHITE, fg=ORANGE, font=("Segoe UI", 12, "bold"),
                                relief="flat", bd=0, cursor="hand2", pady=2, highlightbackground="#fde68a", highlightthickness=1,
                                command=self._toggle_highlight)
        self.btn_hl.pack(pady=(5, 0))

        # Input Box
        inp_box = tk.Frame(left, bg=BG)
        inp_box.pack(pady=5) # Reduced from 20

        tk.Label(inp_box, text="Твоя відповідь:", bg=BG, fg=MUTED, font=("Segoe UI", 14)).pack()

        self.display_frame = tk.Frame(inp_box, bg=WHITE, highlightbackground=ACCENT, highlightthickness=2)
        self.display_frame.pack(pady=4, ipadx=16, ipady=4)
        
        self.lbl_display = tk.Label(self.display_frame, text="", bg=WHITE, fg=TEXT, font=("Segoe UI", 32, "bold"), width=10, anchor="e") # Font 48->32
        self.lbl_display.pack()

        self.lbl_feedback = tk.Label(inp_box, text="", bg=BG, font=("Segoe UI", 14, "bold"), justify="center") # Font 18->14
        self.lbl_feedback.pack(pady=(2, 0))

        # Numpad
        kbd = tk.Frame(left, bg=BG)
        kbd.pack(pady=5) # Reduced from 20

        self.kbd_buttons = []
        BTN_W = 5
        BTN_H = 1 # Reduced from 2
        FONT_KBD = ("Segoe UI", 16, "bold") # Reduced from 24
        
        # No comma for natural numbers
        rows = [["7","8","9"], ["4","5","6"], ["1","2","3"], ["C","0","⌫"]]
        for row in rows:
            r = tk.Frame(kbd, bg=BG)
            r.pack(pady=2) # Reduced
            for ch in row:
                is_del = ch in ("⌫", "C")
                btn = tk.Button(r, text=ch, bg="#fee2e2" if is_del else BTN_NUM, fg=RED if is_del else TEXT,
                                font=FONT_KBD, width=BTN_W, height=BTN_H, relief="flat", bd=0, cursor="hand2",
                                highlightbackground=BORDER, highlightthickness=1,
                                command=lambda c=ch: self._key_press(c))
                btn.pack(side="left", padx=4)
                self.kbd_buttons.append(btn)

        self.btn_ok = tk.Button(left, text="✓ Перевірити", bg=ACCENT, fg=WHITE, font=("Segoe UI", 14, "bold"),
                                relief="flat", bd=0, cursor="hand2", pady=10, command=self._check) # Reduced font & pad
        self.btn_ok.pack(pady=10, ipadx=40)

        self.btn_next = tk.Button(left, text="▶ Наступне", bg=GREEN, fg=WHITE, font=("Segoe UI", 14, "bold"),
                                  relief="flat", bd=0, cursor="hand2", pady=10, command=self._new_task)
        # Packed later when needed

        # ── права частина (правила та візуал)
        right = tk.Frame(self.main_area, bg=PANEL, width=RW, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        rpad = tk.Frame(right, bg=PANEL)
        rpad.pack(fill="both", expand=True, padx=10, pady=10) # Reduced pad

        # Правило
        tk.Label(rpad, text="Правило округлення", bg=PANEL, fg=MUTED, font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,5))
        rule_box = tk.Frame(rpad, bg="#eff6ff", highlightbackground="#bfdbfe", highlightthickness=1)
        rule_box.pack(fill="x", ipadx=5, ipady=5)
        
        rule_text = (
            "1. Знайди цифру розряду округлення.\n"
            "2. Подивись на цифру ПРАВОРУЧ від неї.\n"
            "   • 0, 1, 2, 3, 4 → цифра не змінюється\n"
            "   • 5, 6, 7, 8, 9 → цифра збільшується на 1\n"
            "3. Всі цифри правіше перетворюються на НУЛІ."
        )
        tk.Label(rule_box, text=rule_text, bg="#eff6ff", fg=TEXT, font=("Segoe UI", 12), justify="left", anchor="w").pack(fill="x", padx=5)

        tk.Frame(rpad, bg=BORDER, height=2).pack(fill="x", pady=10)

        # Числова пряма
        self.btn_line = tk.Button(rpad, text="📏 Показати на числовій прямій", bg=WHITE, fg=ACCENT, font=("Segoe UI", 12, "bold"),
                                  relief="flat", bd=0, cursor="hand2", pady=5, highlightbackground=ACCENT, highlightthickness=1,
                                  command=self._toggle_line)
        self.btn_line.pack(fill="x")

        self.line_canvas = tk.Canvas(rpad, bg=PANEL, highlightthickness=0, height=180) # Reduced height

        # Score
        self.lbl_score_round = tk.Label(rpad, text="Рахунок: 0 / 0", font=("Segoe UI", 14, "bold"), bg=PANEL, fg=MUTED)
        self.lbl_score_round.pack(side="bottom", pady=10)

        self._new_task()

    def _new_task(self):
        self.task = _gen_task()
        self.user_input = ""
        self.phase = "answer"
        self.line_shown = False

        t = self.task
        self.lbl_instruction.config(text=f"Округли до {t['round_name']}:")
        self.highlight_shown = False
        self._apply_highlight()
        self.btn_hl.config(text="💡 Показати розряд", bg=WHITE, fg=ORANGE)

        self.lbl_display.config(text="", bg=WHITE)
        self.display_frame.config(highlightbackground=ACCENT)
        self.lbl_feedback.config(text="")

        self.btn_line.config(text="📏 Показати на числовій прямій", bg=WHITE, fg=ACCENT)
        self.line_canvas.pack_forget()

        self.btn_next.pack_forget()
        self.btn_ok.pack(pady=10, ipadx=40)

        for btn in self.kbd_buttons: btn.config(state="normal")
        self._update_score()

    def _toggle_highlight(self):
        self.highlight_shown = not self.highlight_shown
        self._apply_highlight()
        if self.highlight_shown:
            self.btn_hl.config(text=f"🙈 Сховати (розряд «{self.task['round_name']}»)", bg="#fef3c7", fg=HL_FG)
        else:
            self.btn_hl.config(text="💡 Показати розряд", bg=WHITE, fg=ORANGE)

    def _apply_highlight(self):
        if self.highlight_shown:
            self.hl_number.set_segments(self.task["segments"])
        else:
            self.hl_number.set_segments([(self.task["number_str"], False)])

    def _key_press(self, ch):
        if self.phase != "answer": return
        if ch == "⌫":
            self.user_input = self.user_input[:-1]
        elif ch == "C":
            self.user_input = ""
        else:
            if len(self.user_input) < 10:
                self.user_input += ch
        self.lbl_display.config(text=self.user_input)

    def _check(self):
        if self.phase != "answer": return
        raw = self.user_input.strip()
        if not raw:
            self.lbl_feedback.config(text="Введи відповідь!", fg=ORANGE)
            return

        self.phase = "feedback"
        self.total += 1

        try:
            got = int(raw)
            correct = self.task["answer"]
            ok = (got == correct)
        except:
            ok = False

        if ok:
            self.score += 1
            self.streak += 1
            s = f" 🔥×{self.streak}" if self.streak > 1 else ""
            self.lbl_feedback.config(text=f"✅ Правильно!{s}", fg=GREEN)
            self.lbl_display.config(bg=GREEN_BG)
            self.display_frame.config(highlightbackground=GREEN)
        else:
            self.streak = 0
            self.lbl_feedback.config(text=f"❌ Ні. Правильно: {self.task['answer_str']}", fg=RED)
            self.lbl_display.config(bg=RED_BG)
            self.display_frame.config(highlightbackground=RED)

        for btn in self.kbd_buttons: btn.config(state="disabled")
        
        self.btn_ok.pack_forget()
        self.btn_next.pack(pady=10, ipadx=40)

        self.line_shown = False
        self._toggle_line()
        self._update_score()

    def _toggle_line(self):
        if self.line_shown:
            self.line_canvas.pack_forget()
            self.line_shown = False
            self.btn_line.config(text="📏 Показати на числовій прямій", bg=WHITE, fg=ACCENT)
        else:
            self.line_shown = True
            self.btn_line.config(text="🙈 Сховати числову пряму", bg="#dbeafe", fg=ACCENT)
            self._draw_number_line()
            self.line_canvas.pack(fill="x", pady=10)

    def _draw_number_line(self):
        self.update_idletasks()
        c = self.line_canvas
        c.delete("all")
        
        task = self.task
        number = task["number"]
        answer = task["answer"]
        power = task["power"]
        step = 10 ** power

        # Find bounds
        lo = (number // step) * step
        hi = lo + step

        # Extend bounds slightly for visual context
        draw_lo = lo - step
        draw_hi = hi + step

        W = c.winfo_width()
        c.config(height=180) # Reduced height
        margin = 40
        usable = W - 2 * margin

        def to_x(val):
            span = draw_hi - draw_lo
            if span == 0: span = 1
            return margin + (val - draw_lo) / span * usable

        ya = 80 # Adjusted Y
        c.create_line(margin-20, ya, W-margin+20, ya, fill=LINE_COL, width=3, arrow="last")

        # Draw main ticks
        v = draw_lo
        while v <= draw_hi:
            x = to_x(v)
            c.create_line(x, ya-15, x, ya+15, fill=LINE_COL, width=2)
            c.create_text(x, ya+30, text=str(v), fill=TEXT, font=("Segoe UI", 10, "bold"))
            v += step

        # Draw half tick
        half = lo + step // 2
        x_half = to_x(half)
        c.create_line(x_half, ya-8, x_half, ya+8, fill=MUTED, width=1)
        c.create_text(x_half, ya+20, text=str(half), fill=MUTED, font=("Segoe UI", 8))

        # Original number
        xn = to_x(number)
        c.create_oval(xn-8, ya-8, xn+8, ya+8, fill=DOT_ORIG, outline="")
        c.create_text(xn, ya-30, text=task["number_str"], fill=DOT_ORIG, font=("Segoe UI", 12, "bold"))

        # Answer
        xa = to_x(answer)
        c.create_oval(xa-10, ya-10, xa+10, ya+10, fill=DOT_ROUND, outline=WHITE, width=2)
        
        # Arc to show rounding direction
        if xn != xa:
            c.create_line(xn, ya-15, xa, ya-15, fill=ACCENT, width=3, arrow="last", dash=(4,4))

        # Legend
        c.create_oval(margin, 150, margin+12, 162, fill=DOT_ORIG, outline="")
        c.create_text(margin+20, 156, text="вихідне число", fill=DOT_ORIG, font=("Segoe UI", 10), anchor="w")
        
        c.create_oval(margin+150, 150, margin+162, 162, fill=DOT_ROUND, outline="")
        c.create_text(margin+170, 156, text="округлене", fill=DOT_ROUND, font=("Segoe UI", 10), anchor="w")

    def _update_score(self):
        pct = round(self.score / self.total * 100) if self.total else 0
        self.lbl_score_round.config(text=f"Рахунок: {self.score} / {self.total} ({pct}%)")

if __name__ == "__main__":
    app = NaturalsApp()
    app.mainloop()
