"""
Тренажер «Округлення» — повноекранний, тільки миша, світла тема.
• Кома як роздільник
• Підсвічування розряду в числі
• Більша клавіатура
• Числова пряма
• Підтримка будь-якого монітора (запускається на моніторі де є курсор)
"""

import tkinter as tk
import tkinter.font as tkfont
import math, random
from decimal import Decimal, ROUND_HALF_UP

# ── палітра ───────────────────────────────────────────────────────────────────
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

# ── розряди ──────────────────────────────────────────────────────────────────
ROUND_SPECS = [
    ("тисяч",    3),
    ("сотень",   2),
    ("десятків", 1),
    ("одиниць",  0),
    ("десятих", -1),
    ("сотих",   -2),
    ("тисячних",-3),
]

def _round_to_power(number: Decimal, power: int) -> Decimal:
    if power >= 0:
        factor = Decimal(10 ** power)
        return (number / factor).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * factor
    else:
        fmt = "0." + "0" * (-power)
        return number.quantize(Decimal(fmt), rounding=ROUND_HALF_UP)

def _fmt_comma(d) -> str:
    return str(d).replace(".", ",")

def _gen_task():
    name, power = random.choice(ROUND_SPECS)
    if power >= 2:
        int_val, frac_len = random.randint(100, 9999), random.choice([0,1,2])
    elif power == 1:
        int_val, frac_len = random.randint(10, 999),   random.choice([0,1,2])
    elif power == 0:
        int_val, frac_len = random.randint(1, 999),    random.choice([1,2,3])
    elif power == -1:
        int_val, frac_len = random.randint(1, 99),     random.choice([2,3,4])
    elif power == -2:
        int_val, frac_len = random.randint(1, 99),     random.choice([3,4,5])
    else:
        int_val, frac_len = random.randint(1, 99),     random.choice([4,5,6,7,8])

    if frac_len > 0:
        fd = [str(random.randint(0,9)) for _ in range(frac_len)]
        fd[-1] = str(random.randint(1,9))
        key_pos = -power
        if 0 <= key_pos < frac_len:
            fd[key_pos] = str(random.randint(0,9))
        number_str = f"{int_val}." + "".join(fd)
    else:
        number_str = str(int_val)

    number = Decimal(number_str)
    answer = _round_to_power(number, power)

    # --- підсвічування розряду ---
    # Визначаємо позицію цифри розряду у рядку числа (без коми)
    # int_str — ціла частина; frac_str — дробова
    dot_pos = number_str.find(".")
    if dot_pos == -1:
        int_str  = number_str
        frac_str = ""
    else:
        int_str  = number_str[:dot_pos]
        frac_str = number_str[dot_pos+1:]

    int_len = len(int_str)

    if power >= 0:
        # розряд серед цілої частини
        # int_str[int_len-1-power] — це позиція розряду одиниць, тисяч тощо
        hi_pos_in_int = int_len - 1 - power
        if 0 <= hi_pos_in_int < int_len:
            before = int_str[:hi_pos_in_int]
            hi_ch  = int_str[hi_pos_in_int]
            after  = int_str[hi_pos_in_int+1:]
        else:
            before, hi_ch, after = int_str, "", ""
        # segments: list of (text_with_comma, is_highlight)
        segments = []
        if before:
            segments.append((before, False))
        if hi_ch:
            segments.append((hi_ch, True))
        if after:
            segments.append((after, False))
        if frac_str:
            segments.append(("," + frac_str, False))
    else:
        # розряд у дробовій частині
        frac_idx = (-power) - 1   # 0-based index in frac_str
        if frac_idx < len(frac_str):
            frac_before = frac_str[:frac_idx]
            hi_ch       = frac_str[frac_idx]
            frac_after  = frac_str[frac_idx+1:]
        else:
            frac_before, hi_ch, frac_after = frac_str, "", ""
        segments = [(int_str + ",", False)]
        if frac_before:
            segments.append((frac_before, False))
        if hi_ch:
            segments.append((hi_ch, True))
        if frac_after:
            segments.append((frac_after, False))

    return {
        "number":     number,
        "number_str": _fmt_comma(number),
        "answer":     answer,
        "answer_str": _fmt_comma(answer),
        "round_name": name,
        "power":      power,
        "segments":   segments,   # [(text, is_highlight), ...]
    }


# ── допоміжний клас: число з підсвіченим розрядом ──────────────────────────
class HighlightedNumber(tk.Frame):
    """Відображає число як рядок Label-ів з одним підсвіченим символом."""

    FONT_NORMAL = ("Segoe UI", 44, "bold")
    FONT_HL     = ("Segoe UI", 44, "bold")

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=YELLOW_BG, **kwargs)
        self._labels = []

    def set_segments(self, segments):
        for lbl in self._labels:
            lbl.destroy()
        self._labels = []
        for text, is_hl in segments:
            if is_hl:
                lbl = tk.Label(self, text=text,
                               bg=HL_BG, fg=HL_FG,
                               font=self.FONT_HL,
                               padx=3, pady=2,
                               relief="flat")
            else:
                lbl = tk.Label(self, text=text,
                               bg=YELLOW_BG, fg=TEXT,
                               font=self.FONT_NORMAL,
                               padx=0, pady=2)
            lbl.pack(side="left")
            self._labels.append(lbl)


# ─────────────────────────────────────────────────────────────────────────────
class RoundingTrainer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Тренажер: Округлення")
        self.configure(bg=BG)

        # ── визначаємо монітор де знаходиться курсор миші ──────────────────
        self.update_idletasks()
        mx = self.winfo_pointerx()
        my = self.winfo_pointery()

        # отримуємо список усіх моніторів через tk
        # winfo_screenwidth/height завжди повертають головний монітор,
        # тому використовуємо геометрію через wm_maxsize + позицію курсора
        mon = self._detect_monitor(mx, my)
        self.MON_X  = mon["x"]
        self.MON_Y  = mon["y"]
        self.SW     = mon["w"]
        self.SH     = mon["h"]

        # позиціонуємо та розгортаємо на потрібному моніторі
        self.geometry(f"{self.SW}x{self.SH}+{self.MON_X}+{self.MON_Y}")
        self.update_idletasks()
        self.attributes("-fullscreen", True)

        self.bind("<Escape>", self._exit_fullscreen)

        self.task           = None
        self.user_input     = ""
        self.score          = 0
        self.total          = 0
        self.streak         = 0
        self.phase          = "answer"
        self.line_shown     = False
        self.highlight_shown = False

        self.HDR = 58
        self._build_ui()
        self._new_task()

    # ── визначення монітора ──────────────────────────────────────────────────
    def _detect_monitor(self, px, py):
        """Повертає геометрію монітора де знаходиться курсор."""
        try:
            # спробуємо через xrandr (Linux) або tkinter internal
            monitors = self._get_monitors_tk()
        except Exception:
            monitors = []

        for m in monitors:
            if m["x"] <= px < m["x"] + m["w"] and m["y"] <= py < m["y"] + m["h"]:
                return m

        # fallback: головний монітор
        return {"x": 0, "y": 0,
                "w": self.winfo_screenwidth(),
                "h": self.winfo_screenheight()}

    def _get_monitors_tk(self):
        """Отримує список моніторів через Tk/Tcl."""
        monitors = []
        try:
            # Використовуємо winfo_vrootwidth і winfo_vrootheight
            # для отримання розміру віртуального десктопу
            vw = self.winfo_vrootwidth()
            vh = self.winfo_vrootheight()
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()

            if vw > sw:
                # два монітори горизонтально (припущення)
                n = round(vw / sw)
                for i in range(n):
                    monitors.append({"x": i*sw, "y": 0, "w": sw, "h": sh})
            elif vh > sh:
                # два монітори вертикально
                n = round(vh / sh)
                for i in range(n):
                    monitors.append({"x": 0, "y": i*sh, "w": sw, "h": sh})
            else:
                monitors.append({"x": 0, "y": 0, "w": sw, "h": sh})
        except Exception:
            pass
        return monitors

    def _exit_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)
        # повертаємо нормальне вікно на правильний монітор
        self.geometry(f"1200x800+{self.MON_X}+{self.MON_Y}")

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        SW, SH, HDR = self.SW, self.SH, self.HDR
        CH = SH - HDR

        # шапка
        hdr = tk.Frame(self, bg=ACCENT, height=HDR)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="≈  Тренажер «Округлення»",
                 bg=ACCENT, fg=WHITE, font=("Segoe UI", 17, "bold")
                 ).place(x=22, rely=0.5, anchor="w")
        self.lbl_score = tk.Label(hdr, text="", bg=ACCENT, fg="#bfdbfe",
                                  font=("Segoe UI", 13, "bold"))
        self.lbl_score.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(hdr, text="ESC — вийти", bg=ACCENT, fg="#93c5fd",
                 font=("Segoe UI", 10)).place(relx=1.0, x=-18, rely=0.5, anchor="e")

        # основний контейнер
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True)

        # ── ліва частина  (60% ширини)
        LW = int(SW * 0.60)
        self.LW = LW
        left = tk.Frame(main, bg=BG, width=LW)
        left.pack(side="left", fill="both")
        left.pack_propagate(False)

        # --- задача ---
        task_box = tk.Frame(left, bg=BG)
        task_box.place(relx=0.5, y=int(CH * 0.13), anchor="center")

        self.lbl_instruction = tk.Label(task_box, text="", bg=BG, fg=MUTED,
                                        font=("Segoe UI", 16), justify="center")
        self.lbl_instruction.pack()

        # рамка числа
        num_outer = tk.Frame(task_box, bg=YELLOW_BG,
                             highlightbackground="#fde68a", highlightthickness=2)
        num_outer.pack(pady=(10, 0), ipadx=22, ipady=8)

        self.hl_number = HighlightedNumber(num_outer)
        self.hl_number.pack(padx=10, pady=4)

        # кнопка підсвічування розряду (під числом)
        self.btn_hl = tk.Button(
            task_box,
            text="💡  Показати розряд",
            bg=WHITE, fg=ORANGE, font=("Segoe UI", 11, "bold"),
            relief="flat", bd=0, cursor="hand2", pady=6,
            highlightbackground="#fde68a", highlightthickness=1,
            command=self._toggle_highlight)
        self.btn_hl.pack(pady=(8, 0))

        # --- поле відповіді ---
        inp_box = tk.Frame(left, bg=BG)
        inp_box.place(relx=0.5, y=int(CH * 0.37), anchor="center")

        tk.Label(inp_box, text="Твоя відповідь:", bg=BG, fg=MUTED,
                 font=("Segoe UI", 13)).pack()

        self.display_frame = tk.Frame(inp_box, bg=WHITE,
                                      highlightbackground=ACCENT, highlightthickness=2)
        self.display_frame.pack(pady=8, ipadx=24, ipady=10)
        self.lbl_display = tk.Label(self.display_frame, text="", bg=WHITE, fg=TEXT,
                                    font=("Segoe UI", 36, "bold"), width=12, anchor="e")
        self.lbl_display.pack()

        self.lbl_feedback = tk.Label(inp_box, text="", bg=BG,
                                     font=("Segoe UI", 14, "bold"), justify="center")
        self.lbl_feedback.pack(pady=(4, 0))

        # --- клавіатура (більша) ---
        kbd = tk.Frame(left, bg=BG)
        kbd.place(relx=0.5, y=int(CH * 0.69), anchor="center")

        self.kbd_buttons = []
        BTN_W = max(5, int(SW * 0.032 // 10))   # адаптивна ширина
        BTN_H = 2
        FONT_KBD = ("Segoe UI", 22, "bold")
        PAD_Y = 6

        rows = [["7","8","9"], ["4","5","6"], ["1","2","3"], [",","0","⌫"]]
        for row in rows:
            r = tk.Frame(kbd, bg=BG)
            r.pack(pady=PAD_Y)
            for ch in row:
                is_del = ch == "⌫"
                is_com = ch == ","
                btn = tk.Button(
                    r, text=ch,
                    bg="#fee2e2" if is_del else BTN_NUM,
                    fg=RED if is_del else (ACCENT if is_com else TEXT),
                    font=FONT_KBD,
                    width=BTN_W, height=BTN_H,
                    relief="flat", bd=0, cursor="hand2",
                    highlightbackground=BORDER, highlightthickness=1,
                    command=lambda c=ch: self._key_press(c)
                )
                btn.pack(side="left", padx=6)
                btn.bind("<Enter>", lambda e, b=btn, d=is_del:
                         b.config(bg="#fca5a5" if d else BTN_HOV)
                         if b["state"] == "normal" else None)
                btn.bind("<Leave>", lambda e, b=btn, d=is_del:
                         b.config(bg="#fee2e2" if d else BTN_NUM)
                         if b["state"] == "normal" else None)
                self.kbd_buttons.append(btn)

        # кнопки Перевірити / Наступне
        self.btn_ok = tk.Button(
            left, text="✓  Перевірити",
            bg=ACCENT, fg=WHITE, font=("Segoe UI", 15, "bold"),
            relief="flat", bd=0, cursor="hand2", pady=13,
            command=self._check)
        self.btn_ok.place(relx=0.5, y=int(CH * 0.93), anchor="center", width=300)

        self.btn_next = tk.Button(
            left, text="▶  Наступне",
            bg=GREEN, fg=WHITE, font=("Segoe UI", 15, "bold"),
            relief="flat", bd=0, cursor="hand2", pady=13,
            command=self._new_task)
        self.btn_next.place(relx=0.5, y=int(CH * 0.93), anchor="center", width=300)
        self.btn_next.place_forget()

        # ── права частина
        RW = SW - LW
        self.RW = RW
        right = tk.Frame(main, bg=PANEL, width=RW,
                         highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        rpad = tk.Frame(right, bg=PANEL)
        rpad.place(relx=0.5, rely=0.03, anchor="n", width=RW - 36)

        # правило
        tk.Label(rpad, text="Правило округлення", bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0,6))
        rule_box = tk.Frame(rpad, bg="#eff6ff",
                            highlightbackground="#bfdbfe", highlightthickness=1)
        rule_box.pack(fill="x", ipadx=8, ipady=8)
        tk.Label(rule_box,
                 text="1. Знайди цифру розряду округлення\n"
                      "   (підсвічена у задачі).\n"
                      "2. Подивись на цифру праворуч від неї.\n"
                      "   • < 5 → цифра не змінюється\n"
                      "   • ≥ 5 → цифра збільшується на 1\n"
                      "3. Всі цифри правіше → нулі або відкидаються.",
                 bg="#eff6ff", fg=TEXT, font=("Segoe UI", 11),
                 justify="left", anchor="w").pack(fill="x", padx=6)

        tk.Frame(rpad, bg=BORDER, height=1).pack(fill="x", pady=12)

        # кнопка числової прямої
        self.btn_line = tk.Button(
            rpad, text="📏  Показати на числовій прямій",
            bg=WHITE, fg=ACCENT, font=("Segoe UI", 12, "bold"),
            relief="flat", bd=0, cursor="hand2", pady=10,
            highlightbackground=ACCENT, highlightthickness=1,
            command=self._toggle_line)
        self.btn_line.pack(fill="x")

        tk.Frame(rpad, bg=BORDER, height=1).pack(fill="x", pady=10)

        self.line_canvas = tk.Canvas(rpad, bg=PANEL, highlightthickness=0, height=190)
        # не показуємо до першої відповіді

        # приклади
        tk.Label(rpad, text="Приклади", bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0,6))
        for src, hint, ans in [
            ("3,47",   "до десятих", "3,5"),
            ("1 254",  "до сотень",  "1 300"),
            ("0,0867", "до сотих",   "0,09"),
        ]:
            ex = tk.Frame(rpad, bg=WHITE,
                          highlightbackground=BORDER, highlightthickness=1)
            ex.pack(fill="x", pady=3, ipadx=8, ipady=5)
            tk.Label(ex, text=f"{src}  →  ({hint})", bg=WHITE, fg=MUTED,
                     font=("Segoe UI", 10)).pack(anchor="w", padx=6)
            tk.Label(ex, text=f"= {ans}", bg=WHITE, fg=ACCENT,
                     font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=6)

    # ── нова задача ───────────────────────────────────────────────────────────
    def _new_task(self):
        self.task        = _gen_task()
        self.user_input  = ""
        self.phase       = "answer"
        self.line_shown  = False

        t = self.task
        self.lbl_instruction.config(text=f"Округли до {t['round_name']}:")
        # за замовчуванням — число без підсвічування
        self.highlight_shown = False
        self._apply_highlight()
        self.btn_hl.config(text="💡  Показати розряд",
                           bg=WHITE, fg=ORANGE)

        self.lbl_display.config(text="", bg=WHITE)
        self.display_frame.config(highlightbackground=ACCENT)
        self.lbl_feedback.config(text="")

        self.btn_line.config(text="📏  Показати на числовій прямій",
                             bg=WHITE, fg=ACCENT)
        self.line_canvas.pack_forget()

        self.btn_ok.place(relx=0.5, y=int((self.SH-self.HDR)*0.93),
                          anchor="center", width=300)
        self.btn_next.place_forget()

        for btn in self.kbd_buttons:
            btn.config(state="normal")
        self._update_score()

    # ── підсвічування розряду ─────────────────────────────────────────────────
    def _toggle_highlight(self):
        self.highlight_shown = not self.highlight_shown
        self._apply_highlight()
        if self.highlight_shown:
            self.btn_hl.config(
                text=f"🙈  Сховати  (розряд «{self.task['round_name']}»)",
                bg="#fef3c7", fg=HL_FG)
        else:
            self.btn_hl.config(text="💡  Показати розряд",
                               bg=WHITE, fg=ORANGE)

    def _apply_highlight(self):
        t = self.task
        if self.highlight_shown:
            self.hl_number.set_segments(t["segments"])
        else:
            # показуємо число без підсвічування — один сегмент
            self.hl_number.set_segments([(t["number_str"], False)])

    # ── клавіатура ────────────────────────────────────────────────────────────
    def _key_press(self, ch):
        if self.phase != "answer":
            return
        if ch == "⌫":
            self.user_input = self.user_input[:-1]
        elif ch == ",":
            if "," not in self.user_input:
                self.user_input = ("0," if not self.user_input else self.user_input + ",")
        else:
            if len(self.user_input) < 14:
                self.user_input += ch
        self.lbl_display.config(text=self.user_input)

    # ── перевірка ─────────────────────────────────────────────────────────────
    def _check(self):
        if self.phase != "answer":
            return
        raw = self.user_input.strip()
        if not raw or raw in (",", "0,"):
            self.lbl_feedback.config(text="Введи відповідь!", fg=ORANGE)
            return

        self.phase = "feedback"
        self.total += 1

        try:
            got_d     = Decimal(raw.replace(",", "."))
            correct_d = self.task["answer"]
            ok = (got_d == correct_d)
        except Exception:
            ok = False

        if ok:
            self.score  += 1
            self.streak += 1
            s = f"  🔥×{self.streak}" if self.streak > 1 else ""
            self.lbl_feedback.config(text=f"✅  Правильно!{s}", fg=GREEN)
            self.lbl_display.config(bg=GREEN_BG)
            self.display_frame.config(highlightbackground=GREEN)
        else:
            self.streak = 0
            self.lbl_feedback.config(
                text=f"❌  Ні.  Правильно: {self.task['answer_str']}", fg=RED)
            self.lbl_display.config(bg=RED_BG)
            self.display_frame.config(highlightbackground=RED)

        for btn in self.kbd_buttons:
            btn.config(state="disabled")
        self.btn_ok.place_forget()
        self.btn_next.place(relx=0.5, y=int((self.SH-self.HDR)*0.93),
                            anchor="center", width=300)

        self.line_shown = False
        self._toggle_line()
        self._update_score()

    # ── числова пряма ─────────────────────────────────────────────────────────
    def _toggle_line(self):
        if self.line_shown:
            self.line_canvas.pack_forget()
            self.line_shown = False
            self.btn_line.config(text="📏  Показати на числовій прямій",
                                 bg=WHITE, fg=ACCENT)
        else:
            self.line_shown = True
            self.btn_line.config(text="🙈  Сховати числову пряму",
                                 bg="#dbeafe", fg=ACCENT)
            self._draw_number_line()
            self.line_canvas.pack(fill="x", pady=4)

    def _draw_number_line(self):
        self.update_idletasks()
        c = self.line_canvas
        c.delete("all")
        task   = self.task
        number = float(task["number"])
        answer = float(task["answer"])
        power  = task["power"]
        step   = 10 ** power

        lo = math.floor(number / step) * step
        hi = math.ceil(number  / step) * step
        if lo == hi:
            hi = lo + step
        lo -= step
        hi += step

        W      = self.RW - 40
        c.config(width=W, height=190)
        margin = 30
        usable = W - 2 * margin

        def to_x(val):
            span = hi - lo if hi != lo else 1
            return margin + (val - lo) / span * usable

        ya = 95
        c.create_line(margin-12, ya, W-margin+12, ya,
                      fill=LINE_COL, width=2, arrow="last")

        v = lo
        while v <= hi + step * 0.01:
            x = to_x(v)
            c.create_line(x, ya-10, x, ya+10, fill=LINE_COL, width=2)
            c.create_text(x, ya+24, text=self._fmt_tick(v, power),
                          fill=TEXT, font=("Segoe UI", 9))
            v = round(v + step, 10)

        xn = to_x(number)
        c.create_oval(xn-8, ya-8, xn+8, ya+8, fill=DOT_ORIG, outline="")
        c.create_text(xn, ya-22, text=task["number_str"],
                      fill=DOT_ORIG, font=("Segoe UI", 10, "bold"))

        xa = to_x(answer)
        c.create_oval(xa-9, ya-9, xa+9, ya+9, fill=DOT_ROUND, outline="")
        c.create_text(xa, ya+46, text=f"≈ {task['answer_str']}",
                      fill=DOT_ROUND, font=("Segoe UI", 10, "bold"))

        ay = ya - 38
        c.create_line(xn, ay, xa, ay, fill=ACCENT, width=2,
                      arrow="last", dash=(4,3))

        c.create_oval(margin, 174, margin+10, 184, fill=DOT_ORIG, outline="")
        c.create_text(margin+14, 179, text="вихідне", fill=DOT_ORIG,
                      font=("Segoe UI", 9), anchor="w")
        c.create_oval(margin+90, 174, margin+100, 184, fill=DOT_ROUND, outline="")
        c.create_text(margin+104, 179, text="округлене", fill=DOT_ROUND,
                      font=("Segoe UI", 9), anchor="w")

    def _fmt_tick(self, v, power):
        if power >= 0:
            s = str(int(round(v)))
        else:
            s = f"{v:.{-power}f}"
        return s.replace(".", ",")

    def _update_score(self):
        pct = round(self.score / self.total * 100) if self.total else 0
        self.lbl_score.config(text=f"✓ {self.score} / {self.total}   ({pct}%)")


if __name__ == "__main__":
    app = RoundingTrainer()
    app.mainloop()
