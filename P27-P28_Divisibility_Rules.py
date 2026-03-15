import tkinter as tk
import random

# ── Palette ───────────────────────────────────────────────────────────────────
BG        = "#f0f4f8"
PANEL     = "#ffffff"
BORDER    = "#cbd5e1"
TEXT      = "#0f172a"
MUTED     = "#475569"
WHITE     = "#ffffff"
BTN_NUM   = "#e2e8f0"
BTN_HOV   = "#cbd5e1"
HDR_BG    = "#1d4ed8"
NAV_BG    = "#1e3a5f"
NAV_FG    = "#ffffff"

# Per-divisor accent colours  (fg_active, card_bg)
DIV_STYLE = {
    2:  ("#b91c1c", "#fee2e2"),   # red
    3:  ("#15803d", "#dcfce7"),   # green
    5:  ("#b45309", "#fef9c3"),   # amber
    9:  ("#7c3aed", "#ede9fe"),   # violet
    10: ("#1d4ed8", "#dbeafe"),   # blue
}
# Named references
ACCENT  = "#1d4ed8"
GREEN   = "#15803d"
RED     = "#b91c1c"
ORANGE  = "#b45309"
VIOLET  = "#7c3aed"

GREEN_LT  = "#bbf7d0"
RED_LT    = "#fee2e2"
ORANGE_LT = "#fef3c7"

# ── Fonts ─────────────────────────────────────────────────────────────────────
F_TITLE = ("Segoe UI", 34, "bold")
F_HEAD  = ("Segoe UI", 26, "bold")
F_SUB   = ("Segoe UI", 20, "bold")
F_BODY  = ("Segoe UI", 17)
F_BODYB = ("Segoe UI", 17, "bold")
F_BIG   = ("Segoe UI", 76, "bold")
F_BTN   = ("Segoe UI", 19, "bold")
F_NAV   = ("Segoe UI", 14, "bold")
F_SCORE = ("Segoe UI", 20, "bold")
F_FEED  = ("Segoe UI", 15)
F_NUM   = ("Segoe UI", 26, "bold")
F_SMALL = ("Segoe UI", 13)

# Trainer modes: which divisors to test
MODES = {
    "last_digit": [2, 5, 10],
    "digit_sum":  [3, 9],
    "all":        [2, 3, 5, 9, 10],
}
MODE_LABELS = {
    "last_digit": "Остання цифра\n÷ 2,  ÷ 5,  ÷ 10",
    "digit_sum":  "Сума цифр\n÷ 3,  ÷ 9",
    "all":        "Загальний аналіз\n÷ 2, ÷ 3, ÷ 5, ÷ 9, ÷ 10",
}
MODE_COLORS = {
    "last_digit": ("#dbeafe", ACCENT),
    "digit_sum":  ("#ede9fe", VIOLET),
    "all":        ("#dcfce7", GREEN),
}


# ── Widget helpers ────────────────────────────────────────────────────────────
def _darken(h, a=30):
    r = max(0, int(h[1:3], 16) - a)
    g = max(0, int(h[3:5], 16) - a)
    b = max(0, int(h[5:7], 16) - a)
    return f"#{r:02x}{g:02x}{b:02x}"


def mkbtn(parent, text, cmd, bg=ACCENT, fg=WHITE, font=F_BTN,
          w=12, h=2, px=6, py=6):
    b = tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg,
                  font=font, width=w, height=h,
                  relief="flat", bd=0, cursor="hand2",
                  activebackground=bg, activeforeground=fg,
                  padx=px, pady=py)
    orig = bg
    b.bind("<Enter>", lambda e: b.config(bg=_darken(orig, 25)))
    b.bind("<Leave>", lambda e: b.config(bg=orig))
    return b


def hline(parent, color=BORDER):
    tk.Frame(parent, bg=color, height=2).pack(fill="x", pady=(4, 12))


def rule_card(parent, title, body, bg_c, fg_c=TEXT):
    f = tk.Frame(parent, bg=bg_c, padx=22, pady=14,
                 highlightbackground=BORDER, highlightthickness=1)
    f.pack(fill="x", pady=7)
    tk.Label(f, text=title, font=F_SUB, bg=bg_c, fg=fg_c, anchor="w").pack(fill="x")
    tk.Label(f, text=body,  font=F_BODY, bg=bg_c, fg=TEXT,
             justify="left", wraplength=1300, anchor="w").pack(fill="x", pady=(6, 0))


def numpad_widget(parent, get_var, set_var, bg=BG):
    """Reusable on-screen numpad that edits a StringVar."""
    frame = tk.Frame(parent, bg=bg)
    layout = [("7","8","9"), ("4","5","6"), ("1","2","3"), ("C","0","⌫")]
    for row_chars in layout:
        rf = tk.Frame(frame, bg=bg)
        rf.pack(pady=3)
        for ch in row_chars:
            if ch.isdigit():
                bc, fc = BTN_NUM, TEXT
            elif ch == "C":
                bc, fc = RED_LT, RED
            else:
                bc, fc = "#ede9fe", VIOLET

            def make_cmd(c=ch):
                def cmd():
                    cur = get_var()
                    if c.isdigit():
                        if len(cur) < 6:
                            set_var(cur + c)
                    elif c == "⌫":
                        set_var(cur[:-1])
                    elif c == "C":
                        set_var("")
                return cmd

            b = tk.Button(rf, text=ch, font=F_NUM, width=4, height=1,
                          bg=bc, fg=fc, relief="flat", cursor="hand2",
                          command=make_cmd())
            b.pack(side="left", padx=4)
            orig = bc
            b.bind("<Enter>", lambda e, x=b, o=orig: x.config(bg=_darken(o, 20)))
            b.bind("<Leave>", lambda e, x=b, o=orig: x.config(bg=o))
    return frame


# ══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ознаки подільності на 2, 3, 5, 9, 10")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()

        self.current_frame = None
        self.mode = None          # current screen key

        # ── Per-mode trainer state ────────────────────────────────────────
        # scores stored separately per mode key
        self.scores    = {"last_digit": 0, "digit_sum": 0, "all": 0}
        self.attempts  = {"last_digit": 0, "digit_sum": 0, "all": 0}
        self.active_mode   = None   # "last_digit" / "digit_sum" / "all"
        self.active_divs   = []     # list of divisors in current trainer
        self.current_number = 0
        self.selected      = {}     # div -> bool
        self.toggle_btns   = {}     # div -> tk.Button
        self.feed_labels   = {}     # div -> tk.Label
        self.score_lbl     = None
        self.number_lbl    = None
        self.result_lbl    = None
        self.check_btn     = None
        self.next_btn      = None

        self._build_chrome()
        self.show_main_menu()

    # ── Chrome ────────────────────────────────────────────────────────────────
    def _build_chrome(self):
        hdr = tk.Frame(self, bg=HDR_BG, height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="§   Ознаки подільності на 2, 3, 5, 9 і 10",
                 bg=HDR_BG, fg=WHITE, font=("Segoe UI", 21, "bold")).pack(
                 side="left", padx=30)
        mkbtn(hdr, "✕  Вийти", self.destroy, bg="#b91c1c",
              font=("Segoe UI", 13, "bold"), w=9, h=1).pack(
              side="right", padx=18, pady=16)

        nav = tk.Frame(self, bg=NAV_BG, height=52)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        for label, cmd in [
            ("🏠  Меню",    self.show_main_menu),
            ("📖  Теорія",  self.show_theory),
            ("🎯  Практика: остання цифра",
             lambda: self.show_trainer("last_digit")),
            ("🎯  Практика: сума цифр",
             lambda: self.show_trainer("digit_sum")),
            ("🎯  Практика: загальний аналіз",
             lambda: self.show_trainer("all")),
        ]:
            b = tk.Button(nav, text=label, command=cmd,
                          bg=NAV_BG, fg=NAV_FG, font=F_NAV,
                          relief="flat", bd=0, cursor="hand2",
                          activebackground=ACCENT, activeforeground=WHITE,
                          padx=16, pady=14)
            b.pack(side="left")
            b.bind("<Enter>", lambda e, x=b: x.config(bg=ACCENT))
            b.bind("<Leave>", lambda e, x=b: x.config(bg=NAV_BG))

        self.main_area = tk.Frame(self, bg=BG)
        self.main_area.pack(fill="both", expand=True)

    # ── Utils ─────────────────────────────────────────────────────────────────
    def clear_main(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.main_area, bg=BG)
        self.current_frame.pack(expand=True, fill="both")

    # ══════════════════════════════════════════════════════════════════════════
    # MAIN MENU
    # ══════════════════════════════════════════════════════════════════════════
    def show_main_menu(self):
        self.clear_main()
        self.mode = "menu"

        center = tk.Frame(self.current_frame, bg=BG)
        center.place(relx=.5, rely=.5, anchor="center")

        tk.Label(center, text="Ознаки подільності",
                 font=("Segoe UI", 50, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 4))
        tk.Label(center, text="на  2,  3,  5,  9  і  10",
                 font=("Segoe UI", 28), bg=BG, fg=ACCENT).pack(pady=(0, 32))

        cards_data = [
            ("📖", "Теорія",
             "#dbeafe", ACCENT, self.show_theory),
            ("🎯", "Практика\nОстання цифра\n÷ 2, ÷ 5, ÷ 10",
             "#dbeafe", ACCENT, lambda: self.show_trainer("last_digit")),
            ("🎯", "Практика\nСума цифр\n÷ 3, ÷ 9",
             "#ede9fe", VIOLET, lambda: self.show_trainer("digit_sum")),
            ("🎯", "Практика\nЗагальний аналіз\n÷ 2, ÷ 3, ÷ 5, ÷ 9, ÷ 10",
             "#dcfce7", GREEN, lambda: self.show_trainer("all")),
        ]

        row = tk.Frame(center, bg=BG)
        row.pack()
        for icon, title, bg_c, fg_c, cmd in cards_data:
            c = tk.Frame(row, bg=bg_c, width=220, height=200,
                         highlightbackground=BORDER, highlightthickness=2)
            c.pack(side="left", padx=14)
            c.pack_propagate(False)
            tk.Label(c, text=icon, font=("Segoe UI", 36),
                     bg=bg_c, fg=fg_c).pack(pady=(18, 4))
            tk.Label(c, text=title, font=("Segoe UI", 13, "bold"),
                     bg=bg_c, fg=fg_c, justify="center").pack()
            orig = bg_c
            for w in [c] + list(c.winfo_children()):
                w.bind("<Button-1>", lambda e, f=cmd: f())
            c.bind("<Enter>", lambda e, x=c, col=orig: x.config(bg=_darken(col, 12)))
            c.bind("<Leave>", lambda e, x=c, col=orig: x.config(bg=col))

        tk.Label(center,
                 text="Оберіть розділ або скористайтесь меню зверху",
                 font=F_SMALL, bg=BG, fg=MUTED).pack(pady=18)

    # ══════════════════════════════════════════════════════════════════════════
    # THEORY
    # ══════════════════════════════════════════════════════════════════════════
    def show_theory(self):
        self.clear_main()
        self.mode = "theory"

        sc = tk.Canvas(self.current_frame, bg=BG, highlightthickness=0)
        vsb = tk.Scrollbar(self.current_frame, orient="vertical", command=sc.yview)
        sc.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        sc.pack(side="left", fill="both", expand=True)

        outer = tk.Frame(sc, bg=BG)
        win = sc.create_window((0, 0), window=outer, anchor="nw")
        outer.bind("<Configure>",
                   lambda e: sc.configure(scrollregion=sc.bbox("all")))
        sc.bind("<Configure>",
                lambda e: sc.itemconfig(win, width=e.width))

        p = tk.Frame(outer, bg=BG)
        p.pack(fill="both", expand=True, padx=60, pady=28)

        tk.Label(p, text="Ознаки подільності",
                 font=F_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        hline(p, ACCENT)

        # ── Rule cards ────────────────────────────────────────────────────
        rules = [
            (DIV_STYLE[2][1],  RED,    "÷ 2  —  дивимось на ОСТАННЮ цифру",
             "Число ділиться на 2, якщо його остання цифра парна: 0, 2, 4, 6 або 8.\n\n"
             "Приклади:\n"
             "   134  →  остання цифра  4  (парна)  →  ділиться на 2\n"
             "   57    →  остання цифра  7  (непарна)  →  НЕ ділиться на 2"),
            (DIV_STYLE[3][1],  GREEN,  "÷ 3  —  рахуємо СУМУ ЦИФР",
             "Число ділиться на 3, якщо сума всіх його цифр ділиться на 3.\n\n"
             "Приклади:\n"
             "   123  →  1+2+3 = 6,  6÷3 = 2 (без остачі)  →  ділиться на 3\n"
             "   154  →  1+5+4 = 10, 10÷3 → остача 1  →  НЕ ділиться на 3"),
            (DIV_STYLE[5][1],  ORANGE, "÷ 5  —  дивимось на ОСТАННЮ цифру",
             "Число ділиться на 5, якщо його остання цифра  0  або  5.\n\n"
             "Приклади:\n"
             "   345  →  остання цифра  5  →  ділиться на 5\n"
             "   732  →  остання цифра  2  →  НЕ ділиться на 5"),
            (DIV_STYLE[9][1],  VIOLET, "÷ 9  —  рахуємо СУМУ ЦИФР",
             "Число ділиться на 9, якщо сума всіх його цифр ділиться на 9.\n\n"
             "Приклади:\n"
             "   531  →  5+3+1 = 9,   9÷9 = 1 (без остачі)  →  ділиться на 9\n"
             "   123  →  1+2+3 = 6,   6÷9 → остача 6  →  НЕ ділиться на 9\n\n"
             "💡  Зверни увагу: якщо число ділиться на 9 — воно також ділиться на 3!"),
            (DIV_STYLE[10][1], ACCENT, "÷ 10  —  дивимось на ОСТАННЮ цифру",
             "Число ділиться на 10, якщо його остання цифра  0.\n\n"
             "Приклади:\n"
             "   1230  →  остання цифра  0  →  ділиться на 10\n"
             "   455   →  остання цифра  5  →  НЕ ділиться на 10\n\n"
             "💡  Якщо ділиться на 10 — також ділиться на 2 і на 5!"),
        ]
        for bg_c, fg_c, title, body in rules:
            rule_card(p, title, body, bg_c, fg_c)

        # ── Connections card ──────────────────────────────────────────────
        rule_card(p, "🔗  Зв'язки між ознаками",
                  "÷ 10  →  також ÷ 2  і  ÷ 5\n"
                  "÷ 9   →  також ÷ 3\n"
                  "÷ 2  і  ÷ 3  одночасно  →  також ÷ 6",
                  "#f1f5f9", MUTED)

        # ── Demo with on-screen numpad ────────────────────────────────────
        demo_f = tk.Frame(p, bg=PANEL, padx=22, pady=16,
                          highlightbackground=BORDER, highlightthickness=1)
        demo_f.pack(fill="x", pady=12)

        tk.Label(demo_f, text="🔢  Спробуйте самі — введіть число (з екрану або клавіатури):",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(anchor="w", pady=(0, 8))

        demo_main = tk.Frame(demo_f, bg=PANEL)
        demo_main.pack(anchor="w", fill="x")

        # left: numpad + display
        left_f = tk.Frame(demo_main, bg=PANEL)
        left_f.pack(side="left", padx=(0, 30))

        # Display box
        disp_var = tk.StringVar(value="")
        disp = tk.Label(left_f, textvariable=disp_var,
                        font=("Segoe UI", 40, "bold"),
                        bg=BTN_NUM, fg=ACCENT,
                        width=8, anchor="e",
                        padx=12, pady=6,
                        highlightbackground=ACCENT, highlightthickness=2)
        disp.pack(pady=(0, 8))

        np = numpad_widget(left_f,
                           lambda: disp_var.get(),
                           lambda v: disp_var.set(v),
                           bg=PANEL)
        np.pack()

        # right: result + calc button
        right_f = tk.Frame(demo_main, bg=PANEL)
        right_f.pack(side="left", fill="both", expand=True)

        res_lbl = tk.Label(right_f, text="", font=F_BODYB, bg=PANEL, fg=ACCENT,
                           wraplength=self.SW - 500, justify="left", anchor="nw")
        res_lbl.pack(anchor="nw", pady=(4, 12))

        def calc(*_):
            raw = disp_var.get().strip()
            try:
                n = int(raw)
                if n < 1:
                    raise ValueError
            except ValueError:
                res_lbl.config(text="Введіть натуральне число", fg=RED)
                return
            s = str(n)
            last = int(s[-1])
            dsum = sum(int(d) for d in s)

            lines = [f"Число:  {n}",
                     f"Остання цифра:  {last}",
                     f"Сума цифр:  {' + '.join(list(s))} = {dsum}",
                     ""]
            for d in [2, 3, 5, 9, 10]:
                ok = (n % d == 0)
                mark = "✅" if ok else "❌"
                lines.append(f"  {mark}  ÷{d}:  {'ділиться' if ok else 'НЕ ділиться'}")
            res_lbl.config(text="\n".join(lines), fg=TEXT)

        mkbtn(right_f, "Перевірити →", calc, bg=ACCENT, w=14, h=2).pack(anchor="nw")

        # Also allow physical keyboard Enter
        self.bind("<Return>", calc)

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER
    # ══════════════════════════════════════════════════════════════════════════
    def show_trainer(self, mode_key):
        self.clear_main()
        self.mode = "trainer"
        self.active_mode = mode_key
        self.active_divs = MODES[mode_key]

        cf = self.current_frame

        # ── Score bar ─────────────────────────────────────────────────────
        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)

        # Mode label in score bar
        _, fg_c = MODE_COLORS[mode_key]
        tk.Label(sbar, text=MODE_LABELS[mode_key].replace("\n", "  "),
                 font=("Segoe UI", 13, "bold"), bg=PANEL, fg=fg_c).pack(
                 side="left", padx=20)
        self.score_lbl = tk.Label(sbar, text=self._score_text(),
                                   font=F_SCORE, bg=PANEL, fg=GREEN)
        self.score_lbl.pack(side="right", padx=30)

        # ── Centred column ─────────────────────────────────────────────────
        center = tk.Frame(cf, bg=BG)
        center.pack(expand=True)

        # Task header
        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=28, pady=12)
        task_f.pack(pady=(14, 4))
        tk.Label(task_f, text="На які числа ділиться?",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack()
        tk.Label(task_f, text="(Натискай кнопки — можна кілька відповідей)",
                 font=F_SMALL, bg=PANEL, fg=MUTED).pack()

        # Big number
        num_f = tk.Frame(center, bg=PANEL,
                         highlightbackground=BORDER, highlightthickness=2,
                         padx=28, pady=4)
        num_f.pack(pady=4)
        self.number_lbl = tk.Label(num_f, text="", font=F_BIG, bg=PANEL, fg=ACCENT)
        self.number_lbl.pack()

        # Toggle buttons — one per active divisor
        tog_f = tk.Frame(center, bg=BG)
        tog_f.pack(pady=12)
        self.toggle_btns = {}
        self.selected    = {d: False for d in self.active_divs}
        for d in self.active_divs:
            fg_on = DIV_STYLE[d][0]
            b = tk.Button(tog_f, text=f"÷ {d}",
                          font=("Segoe UI", 26, "bold"),
                          width=6, height=2,
                          bg=BTN_NUM, fg=TEXT,
                          relief="flat", cursor="hand2",
                          command=lambda x=d: self._toggle(x))
            b.pack(side="left", padx=10)
            self.toggle_btns[d] = b

        # Feedback rows
        feed_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=18, pady=10)
        feed_f.pack(fill="x", pady=8, padx=60)
        self.feed_labels = {}
        for d in self.active_divs:
            lbl = tk.Label(feed_f, text="", font=F_FEED,
                           bg=PANEL, fg=TEXT, justify="left", anchor="w",
                           wraplength=self.SW - 140)
            lbl.pack(fill="x", pady=2)
            self.feed_labels[d] = lbl

        # Overall result
        self.result_lbl = tk.Label(center, text="",
                                    font=("Segoe UI", 21, "bold"),
                                    bg=BG, fg=GREEN)
        self.result_lbl.pack(pady=4)

        # Action buttons
        act = tk.Frame(center, bg=BG)
        act.pack(pady=8)
        self.check_btn = mkbtn(act, "✔  Перевірити", self._check,
                                bg=GREEN, w=14, h=2)
        self.check_btn.pack(side="left", padx=10)
        self.next_btn = mkbtn(act, "▶  Наступне число", self._new_task,
                               bg=ACCENT, w=16, h=2)
        self.next_btn.pack(side="left", padx=10)

        self._new_task()

    # ── Score helper ──────────────────────────────────────────────────────────
    def _score_text(self):
        if self.active_mode:
            s = self.scores[self.active_mode]
            a = self.attempts[self.active_mode]
        else:
            s = a = 0
        return f"Правильно: {s}  /  Завдань: {a}"

    # ── Toggle ────────────────────────────────────────────────────────────────
    def _toggle(self, d):
        if self.check_btn and str(self.check_btn["state"]) == "disabled":
            return
        self.selected[d] = not self.selected[d]
        b = self.toggle_btns[d]
        if self.selected[d]:
            b.config(bg=DIV_STYLE[d][0], fg=WHITE)
        else:
            b.config(bg=BTN_NUM, fg=TEXT)

    # ── Generate task ─────────────────────────────────────────────────────────
    def _new_task(self):
        divs = self.active_divs
        # Guarantee at least one divisor from the active set is satisfied
        base = random.randint(10, 999)
        pick = random.choice(divs)
        n = base * pick
        # Cap at 5 digits
        if n > 99999:
            n = random.randint(1000, 9999)
        # Occasionally fully random for variety
        if random.random() > 0.8:
            n = random.randint(23, 9999)
        self.current_number = n

        self.selected = {d: False for d in divs}
        for d, b in self.toggle_btns.items():
            b.config(bg=BTN_NUM, fg=TEXT, state="normal")
        for lbl in self.feed_labels.values():
            lbl.config(text="")
        if self.number_lbl: self.number_lbl.config(text=str(n), fg=ACCENT)
        if self.result_lbl:  self.result_lbl.config(text="")
        if self.check_btn:   self.check_btn.config(state="normal", bg=GREEN)
        if self.next_btn:    self.next_btn.config(state="normal", bg=ACCENT)
        if self.score_lbl:   self.score_lbl.config(text=self._score_text())

    # ── Check ─────────────────────────────────────────────────────────────────
    def _check(self):
        n   = self.current_number
        s   = str(n)
        last = int(s[-1])
        dsum = sum(int(d) for d in s)

        truth = {d: (n % d == 0) for d in self.active_divs}
        all_ok = all(self.selected[d] == truth[d] for d in self.active_divs)

        self.attempts[self.active_mode] += 1
        if all_ok:
            self.scores[self.active_mode] += 1
            self.result_lbl.config(
                text="🎉  ВІДМІННО!  Усі ознаки визначено правильно!", fg=GREEN)
        else:
            self.result_lbl.config(
                text="Є помилки — дивись пояснення нижче 👇", fg=RED)
        if self.score_lbl:
            self.score_lbl.config(text=self._score_text())

        # ── Build explanation per divisor ─────────────────────────────────
        def explain(d):
            if d in (2, 5, 10):
                base = f"Остання цифра:  {last}"
            else:
                base = f"Сума цифр:  {' + '.join(list(s))} = {dsum}"

            if d == 2:
                detail = (f"→ {last} парна → ДІЛИТЬСЯ на 2"
                          if truth[2] else f"→ {last} непарна → НЕ ділиться на 2")
            elif d == 3:
                detail = (f"→ {dsum}÷3={dsum//3} без остачі → ДІЛИТЬСЯ на 3"
                          if truth[3] else f"→ {dsum}÷3 остача {dsum%3} → НЕ ділиться на 3")
            elif d == 5:
                detail = (f"→ {last} це 0 або 5 → ДІЛИТЬСЯ на 5"
                          if truth[5] else f"→ {last} не 0 і не 5 → НЕ ділиться на 5")
            elif d == 9:
                detail = (f"→ {dsum}÷9={dsum//9} без остачі → ДІЛИТЬСЯ на 9"
                          if truth[9] else f"→ {dsum}÷9 остача {dsum%9} → НЕ ділиться на 9")
            elif d == 10:
                detail = (f"→ {last} це 0 → ДІЛИТЬСЯ на 10"
                          if truth[10] else f"→ {last} не 0 → НЕ ділиться на 10")
            return f"{base}   {detail}"

        for d in self.active_divs:
            user  = self.selected[d]
            corr  = truth[d]
            lbl   = self.feed_labels[d]
            btn_w = self.toggle_btns[d]

            if user == corr:
                prefix = f"✅  ÷{d}:  "
                color  = GREEN if corr else MUTED
            elif corr and not user:
                prefix = f"❌  ÷{d}:  Не позначив, а треба! "
                color  = RED
            else:
                prefix = f"❌  ÷{d}:  Позначив зайве! "
                color  = RED

            lbl.config(text=prefix + explain(d), fg=color)

            # Colour the toggle button
            if corr and user:    btn_w.config(bg=GREEN,      fg=WHITE)
            elif corr:           btn_w.config(bg=ORANGE_LT,  fg=ORANGE)
            elif user:           btn_w.config(bg=RED_LT,     fg=RED)
            else:                btn_w.config(bg=BTN_NUM,    fg=MUTED)
            btn_w.config(state="disabled")

        self.check_btn.config(state="disabled", bg=BTN_NUM)


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
