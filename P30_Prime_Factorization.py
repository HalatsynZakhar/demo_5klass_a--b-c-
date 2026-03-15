import tkinter as tk
import random
import math

# ── Palette (identical to series) ────────────────────────────────────────────
BG        = "#f0f4f8"
PANEL     = "#ffffff"
BORDER    = "#cbd5e1"
TEXT      = "#0f172a"
MUTED     = "#475569"
WHITE     = "#ffffff"
BTN_NUM   = "#e2e8f0"
HDR_BG    = "#1d4ed8"
NAV_BG    = "#1e3a5f"
NAV_FG    = "#ffffff"
ACCENT    = "#1d4ed8"
ACCENT2   = "#7c3aed"
GREEN     = "#15803d"
GREEN_LT  = "#dcfce7"
RED       = "#b91c1c"
RED_LT    = "#fee2e2"
ORANGE    = "#b45309"
ORANGE_LT = "#fef3c7"
CARD_B    = "#dbeafe"
CARD_V    = "#ede9fe"
CARD_G    = "#dcfce7"
CARD_Y    = "#fef9c3"

# Colour wheel for prime buttons (cycles)
PRIME_COLORS = [
    ("#1d4ed8", "#dbeafe"),   # blue
    ("#15803d", "#dcfce7"),   # green
    ("#b45309", "#fef9c3"),   # amber
    ("#b91c1c", "#fee2e2"),   # red
    ("#7c3aed", "#ede9fe"),   # violet
    ("#0f766e", "#ccfbf1"),   # teal
    ("#9a3412", "#ffedd5"),   # orange-deep
]

# ── Fonts ─────────────────────────────────────────────────────────────────────
F_TITLE  = ("Segoe UI", 34, "bold")
F_HEAD   = ("Segoe UI", 26, "bold")
F_SUB    = ("Segoe UI", 20, "bold")
F_BODY   = ("Segoe UI", 17)
F_BODYB  = ("Segoe UI", 17, "bold")
F_BTN    = ("Segoe UI", 19, "bold")
F_NAV    = ("Segoe UI", 14, "bold")
F_SCORE  = ("Segoe UI", 20, "bold")
F_FEED   = ("Segoe UI", 16)
F_SMALL  = ("Segoe UI", 13)
F_COL    = ("Courier New", 38, "bold")   # column arithmetic
F_COL_SM = ("Courier New", 28, "bold")
F_NUM    = ("Segoe UI", 26, "bold")
F_PRIME  = ("Segoe UI", 22, "bold")
F_BIG    = ("Segoe UI", 72, "bold")

PRIMES_LIST = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


# ── Helpers ───────────────────────────────────────────────────────────────────
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


def theory_card(parent, title, body, bg_c, fg_title=TEXT):
    f = tk.Frame(parent, bg=bg_c, padx=22, pady=14,
                 highlightbackground=BORDER, highlightthickness=1)
    f.pack(fill="x", pady=7)
    tk.Label(f, text=title, font=F_SUB, bg=bg_c, fg=fg_title,
             anchor="w").pack(fill="x")
    tk.Label(f, text=body,  font=F_BODY, bg=bg_c, fg=TEXT,
             justify="left", wraplength=1300, anchor="w").pack(
             fill="x", pady=(6, 0))
    return f


def factorize(n):
    """Return sorted list of prime factors of n."""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def generate_number():
    """Pick a composite number 12–200 with ≥2 prime factors, none >47."""
    candidates = []
    for n in range(12, 201):
        if is_prime(n):
            continue
        fs = factorize(n)
        if len(fs) >= 2 and max(fs) <= 47:
            candidates.append(n)
    return random.choice(candidates)


# ══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("§ 30. Розкладання на прості множники")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()

        self.current_frame = None
        self.mode = None

        # ── Trainer state ─────────────────────────────────────────────────
        self.score    = 0
        self.attempts = 0

        # Column state
        self.start_num    = 0
        self.cur_num      = 0          # number being divided at current step
        self.factors      = []         # factors found so far
        self.col_rows     = []         # list of dicts per row
        self.trainer_mode = "auto"     # "auto" | "manual"
        self.step_state   = "pick"     # "pick" | "enter"
        self.chosen_div   = 0
        self.expected_q   = 0
        self.np_input     = ""

        # UI refs
        self.score_lbl    = None
        self.instr_lbl    = None
        self.column_frame = None
        self.prime_frame  = None
        self.enter_frame  = None
        self.np_disp      = None
        self.result_lbl   = None
        self.prime_btns   = {}

        self._build_chrome()
        self.show_main_menu()

    # ── Chrome ────────────────────────────────────────────────────────────────
    def _build_chrome(self):
        hdr = tk.Frame(self, bg=HDR_BG, height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="§ 30.   Розкладання числа на прості множники",
                 bg=HDR_BG, fg=WHITE,
                 font=("Segoe UI", 21, "bold")).pack(side="left", padx=30)
        mkbtn(hdr, "✕  Вийти", self.destroy, bg="#b91c1c",
              font=("Segoe UI", 13, "bold"), w=9, h=1).pack(
              side="right", padx=18, pady=16)

        nav = tk.Frame(self, bg=NAV_BG, height=52)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        for label, cmd in [
            ("🏠  Меню",       self.show_main_menu),
            ("📖  Теорія",     self.show_theory),
            ("🎯  Тренажер",   self.show_trainer),
        ]:
            b = tk.Button(nav, text=label, command=cmd,
                          bg=NAV_BG, fg=NAV_FG, font=F_NAV,
                          relief="flat", bd=0, cursor="hand2",
                          activebackground=ACCENT, activeforeground=WHITE,
                          padx=20, pady=14)
            b.pack(side="left")
            b.bind("<Enter>", lambda e, x=b: x.config(bg=ACCENT))
            b.bind("<Leave>", lambda e, x=b: x.config(bg=NAV_BG))

        self.main_area = tk.Frame(self, bg=BG)
        self.main_area.pack(fill="both", expand=True)

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

        tk.Label(center, text="Розкладання числа",
                 font=("Segoe UI", 50, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 4))
        tk.Label(center, text="на прості множники",
                 font=("Segoe UI", 28), bg=BG, fg=ACCENT).pack(pady=(0, 32))

        row = tk.Frame(center, bg=BG)
        row.pack()
        for icon, title, bg_c, fg_c, cmd in [
            ("📖", "Теорія",   CARD_B, ACCENT, self.show_theory),
            ("🎯", "Тренажер", CARD_G, GREEN,  self.show_trainer),
        ]:
            c = tk.Frame(row, bg=bg_c, width=230, height=200,
                         highlightbackground=BORDER, highlightthickness=2)
            c.pack(side="left", padx=20)
            c.pack_propagate(False)
            tk.Label(c, text=icon, font=("Segoe UI", 42),
                     bg=bg_c, fg=fg_c).pack(pady=(24, 4))
            tk.Label(c, text=title, font=("Segoe UI", 18, "bold"),
                     bg=bg_c, fg=fg_c).pack()
            orig = bg_c
            for w in [c] + list(c.winfo_children()):
                w.bind("<Button-1>", lambda e, f=cmd: f())
            c.bind("<Enter>", lambda e, x=c, col=orig: x.config(bg=_darken(col, 12)))
            c.bind("<Leave>", lambda e, x=c, col=orig: x.config(bg=col))

        tk.Label(center, text="Натисніть на картку або скористайтесь меню зверху",
                 font=F_SMALL, bg=BG, fg=MUTED).pack(pady=20)

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

        tk.Label(p, text="Розкладання на прості множники",
                 font=F_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        hline(p, ACCENT)

        theory_card(p, "📌  Що таке просте число?",
                    "Просте число — це натуральне число, більше за 1,\n"
                    "яке ділиться рівно на два числа: на 1 і на саме себе.\n\n"
                    "Прості числа:  2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, …\n"
                    "Складені числа (мають інші дільники):  4, 6, 8, 9, 10, 12, …\n"
                    "⚠️  Число 1 — не є ні простим, ні складеним.",
                    CARD_B, ACCENT)

        theory_card(p, "📌  Основна теорема арифметики",
                    "Кожне натуральне число, більше за 1, можна єдиним чином\n"
                    "розкласти у добуток простих чисел (порядок не важливий).\n\n"
                    "Приклади:\n"
                    "   12  =  2 × 2 × 3\n"
                    "   60  =  2 × 2 × 3 × 5\n"
                    "   100 =  2 × 2 × 5 × 5",
                    CARD_V, ACCENT2)

        theory_card(p, "🔑  Алгоритм розкладання у стовпчик",
                    "1. Записуємо число зліва від вертикальної риски.\n"
                    "2. Підбираємо найменший простий дільник (починаємо з 2).\n"
                    "3. Записуємо дільник праворуч від риски.\n"
                    "4. Частку від ділення записуємо під початковим числом.\n"
                    "5. Повторюємо кроки 2–4 з новим числом.\n"
                    "6. Зупиняємось, коли зліва з'явилась 1.\n"
                    "7. Відповідь = добуток усіх дільників праворуч.",
                    CARD_G, GREEN)

        # ── Visual column example ─────────────────────────────────────────
        ex_f = tk.Frame(p, bg=PANEL, padx=28, pady=20,
                        highlightbackground=BORDER, highlightthickness=1)
        ex_f.pack(fill="x", pady=8)
        tk.Label(ex_f, text="📊  Приклад: розкладання числа 60",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(anchor="w")

        cols_f = tk.Frame(ex_f, bg=PANEL)
        cols_f.pack(anchor="w", pady=10, padx=20)

        # Draw the column step by step
        steps = [(60, 2), (30, 2), (15, 3), (5, 5), (1, None)]
        STEP_COLORS = [ACCENT, GREEN, ORANGE, "#b91c1c", MUTED]

        col_left  = tk.Frame(cols_f, bg=PANEL)
        col_sep   = tk.Frame(cols_f, bg=TEXT, width=3)
        col_right = tk.Frame(cols_f, bg=PANEL)
        col_left.pack(side="left")
        col_sep.pack(side="left", fill="y", padx=6)
        col_right.pack(side="left")

        for i, (num, div) in enumerate(steps):
            c = STEP_COLORS[i % len(STEP_COLORS)]
            tk.Label(col_left,  text=f"  {num:<5}", font=F_COL,
                     bg=PANEL, fg=TEXT, anchor="e").pack(anchor="e")
            if div:
                tk.Label(col_right, text=f"  {div}", font=F_COL,
                         bg=PANEL, fg=c, anchor="w").pack(anchor="w")
            else:
                tk.Label(col_right, text="", font=F_COL,
                         bg=PANEL).pack(anchor="w")

        tk.Label(ex_f,
                 text="Відповідь:   60  =  2  ×  2  ×  3  ×  5",
                 font=F_HEAD, bg=PANEL, fg=GREEN).pack(anchor="w", pady=(10, 0))

        # ── Second example ────────────────────────────────────────────────
        ex2_f = tk.Frame(p, bg=CARD_Y, padx=28, pady=20,
                         highlightbackground=BORDER, highlightthickness=1)
        ex2_f.pack(fill="x", pady=8)
        tk.Label(ex2_f, text="📊  Ще один приклад: розкладання числа 84",
                 font=F_BODYB, bg=CARD_Y, fg=TEXT).pack(anchor="w")

        cols2 = tk.Frame(ex2_f, bg=CARD_Y)
        cols2.pack(anchor="w", pady=10, padx=20)
        steps2 = [(84, 2), (42, 2), (21, 3), (7, 7), (1, None)]
        cl2 = tk.Frame(cols2, bg=CARD_Y)
        cs2 = tk.Frame(cols2, bg=TEXT, width=3)
        cr2 = tk.Frame(cols2, bg=CARD_Y)
        cl2.pack(side="left"); cs2.pack(side="left", fill="y", padx=6)
        cr2.pack(side="left")
        for i, (num, div) in enumerate(steps2):
            c = STEP_COLORS[i % len(STEP_COLORS)]
            tk.Label(cl2, text=f"  {num:<5}", font=F_COL,
                     bg=CARD_Y, fg=TEXT, anchor="e").pack(anchor="e")
            if div:
                tk.Label(cr2, text=f"  {div}", font=F_COL,
                         bg=CARD_Y, fg=c, anchor="w").pack(anchor="w")
            else:
                tk.Label(cr2, text="", font=F_COL, bg=CARD_Y).pack(anchor="w")

        tk.Label(ex2_f,
                 text="Відповідь:   84  =  2  ×  2  ×  3  ×  7",
                 font=F_HEAD, bg=CARD_Y, fg=GREEN).pack(anchor="w", pady=(10, 0))

        theory_card(p, "💡  Підказка: з якого числа починати?",
                    "Завжди починай з найменшого простого числа — 2.\n"
                    "Якщо не ділиться на 2 — пробуй 3, потім 5, потім 7 і так далі.\n"
                    "Дільник ніколи не може бути більшим за саме число!",
                    "#fef9c3", ORANGE)

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER
    # ══════════════════════════════════════════════════════════════════════════
    def show_trainer(self):
        self.clear_main()
        self.mode = "trainer"

        cf = self.current_frame

        # ── Score bar ─────────────────────────────────────────────────────
        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.score_lbl = tk.Label(sbar,
            text=f"Правильно: {self.score}  /  Завдань: {self.attempts}",
            font=F_SCORE, bg=PANEL, fg=GREEN)
        self.score_lbl.pack(side="left", padx=30)

        # Mode toggle in score bar
        mode_f = tk.Frame(sbar, bg=PANEL)
        mode_f.pack(side="right", padx=20)
        tk.Label(mode_f, text="Режим:", font=F_SMALL, bg=PANEL, fg=MUTED).pack(side="left", padx=(0, 8))
        self.mode_auto_btn = tk.Button(
            mode_f, text="Авто-ділення", font=("Segoe UI", 13, "bold"),
            bg=ACCENT, fg=WHITE, relief="flat", cursor="hand2", padx=12, pady=4,
            command=lambda: self._set_mode("auto"))
        self.mode_auto_btn.pack(side="left", padx=4)
        self.mode_manual_btn = tk.Button(
            mode_f, text="Ручне ділення", font=("Segoe UI", 13, "bold"),
            bg=BTN_NUM, fg=TEXT, relief="flat", cursor="hand2", padx=12, pady=4,
            command=lambda: self._set_mode("manual"))
        self.mode_manual_btn.pack(side="left", padx=4)

        # ── Two-column workspace ───────────────────────────────────────────
        workspace = tk.Frame(cf, bg=BG)
        workspace.pack(fill="both", expand=True, padx=30, pady=16)

        # LEFT — Column (зошит)
        left_wrap = tk.Frame(workspace, bg=PANEL,
                             highlightbackground=BORDER, highlightthickness=1)
        left_wrap.pack(side="left", fill="both", expand=True, padx=(0, 16))

        tk.Label(left_wrap, text="📒  Зошит",
                 font=F_SUB, bg=PANEL, fg=MUTED).pack(anchor="w", padx=20, pady=(10, 4))
        tk.Frame(left_wrap, bg=BORDER, height=1).pack(fill="x")

        self.column_frame = tk.Frame(left_wrap, bg=PANEL)
        self.column_frame.pack(fill="both", expand=True, padx=20, pady=16)

        # RIGHT — Control panel
        right_wrap = tk.Frame(workspace, bg=PANEL,
                              highlightbackground=BORDER, highlightthickness=1,
                              width=int(self.SW * 0.42))
        right_wrap.pack(side="right", fill="both")
        right_wrap.pack_propagate(False)

        tk.Label(right_wrap, text="🎮  Керування",
                 font=F_SUB, bg=PANEL, fg=MUTED).pack(anchor="w", padx=20, pady=(10, 4))
        tk.Frame(right_wrap, bg=BORDER, height=1).pack(fill="x")

        ctrl = tk.Frame(right_wrap, bg=PANEL)
        ctrl.pack(fill="both", expand=True, padx=16, pady=12)

        # Instruction label
        self.instr_lbl = tk.Label(ctrl, text="",
                                   font=F_SUB, bg=PANEL, fg=TEXT,
                                   wraplength=int(self.SW * 0.4) - 40,
                                   justify="center")
        self.instr_lbl.pack(pady=(4, 12))

        # ── Prime buttons panel ───────────────────────────────────────────
        self.prime_frame = tk.Frame(ctrl, bg=PANEL)
        self.prime_frame.pack()

        self.prime_btns = {}
        grid_f = tk.Frame(self.prime_frame, bg=PANEL)
        grid_f.pack()
        for idx, p in enumerate(PRIMES_LIST):
            fg_c, bg_c = PRIME_COLORS[idx % len(PRIME_COLORS)]
            b = tk.Button(grid_f, text=str(p), font=F_PRIME,
                          width=4, height=1, bg=bg_c, fg=fg_c,
                          relief="flat", cursor="hand2",
                          command=lambda x=p: self._on_prime(x))
            b.grid(row=idx // 5, column=idx % 5, padx=8, pady=8)
            orig_bg = bg_c
            b.bind("<Enter>", lambda e, x=b, o=orig_bg: x.config(bg=_darken(o, 15)))
            b.bind("<Leave>", lambda e, x=b, o=orig_bg: x.config(bg=o))
            self.prime_btns[p] = b

        # ── Enter-quotient panel (hidden until needed) ────────────────────
        self.enter_frame = tk.Frame(ctrl, bg=PANEL)
        # (packed/unpacked dynamically)

        eq_lbl_text = tk.Label(self.enter_frame,
                                text="Введіть результат ділення:",
                                font=F_BODY, bg=PANEL, fg=MUTED)
        eq_lbl_text.pack(pady=(4, 4))

        self.np_disp = tk.Label(self.enter_frame, text="?",
                                 font=("Courier New", 52, "bold"),
                                 bg=BTN_NUM, fg=ACCENT, width=6,
                                 highlightbackground=ACCENT,
                                 highlightthickness=2)
        self.np_disp.pack(pady=6)

        # Numpad
        np_f = tk.Frame(self.enter_frame, bg=PANEL)
        np_f.pack(pady=4)
        layout = [("7","8","9"), ("4","5","6"), ("1","2","3"), ("C","0","OK")]
        for row_chars in layout:
            rf = tk.Frame(np_f, bg=PANEL)
            rf.pack(pady=4)
            for ch in row_chars:
                if ch.isdigit():
                    bc, fc = BTN_NUM, TEXT
                elif ch == "C":
                    bc, fc = RED_LT, RED
                else:   # OK
                    bc, fc = GREEN_LT, GREEN
                b = tk.Button(rf, text=ch, font=F_NUM, width=4, height=1,
                              bg=bc, fg=fc, relief="flat", cursor="hand2",
                              command=lambda c=ch: self._on_numpad(c))
                b.pack(side="left", padx=5)
                orig = bc
                b.bind("<Enter>", lambda e, x=b, o=orig: x.config(bg=_darken(o, 15)))
                b.bind("<Leave>", lambda e, x=b, o=orig: x.config(bg=o))

        # ── Result label + New button ─────────────────────────────────────
        self.result_lbl = tk.Label(ctrl, text="",
                                    font=("Segoe UI", 20, "bold"),
                                    bg=PANEL, fg=GREEN,
                                    wraplength=int(self.SW * 0.4) - 40,
                                    justify="center")
        self.result_lbl.pack(pady=8)

        mkbtn(ctrl, "✨  Нове число", self._new_task,
              bg=ACCENT, w=16, h=2).pack(pady=8)

        self._new_task()

    # ── Mode toggle ────────────────────────────────────────────────────────
    def _set_mode(self, m):
        self.trainer_mode = m
        if m == "auto":
            self.mode_auto_btn.config(bg=ACCENT, fg=WHITE)
            self.mode_manual_btn.config(bg=BTN_NUM, fg=TEXT)
        else:
            self.mode_auto_btn.config(bg=BTN_NUM, fg=TEXT)
            self.mode_manual_btn.config(bg=ACCENT2, fg=WHITE)
        self._new_task()

    # ── Column drawing ─────────────────────────────────────────────────────
    def _draw_column(self):
        """Redraw the entire column from self.col_rows."""
        for w in self.column_frame.winfo_children():
            w.destroy()

        for row in self.col_rows:
            rf = tk.Frame(self.column_frame, bg=PANEL)
            rf.pack(anchor="w", pady=2)

            # Left number
            tk.Label(rf, text=f"{row['num']:>6}",
                     font=F_COL, bg=PANEL, fg=TEXT).pack(side="left")

            # Separator
            tk.Frame(rf, bg=TEXT, width=3, height=48).pack(
                side="left", padx=8, fill="y")

            # Right divisor (or empty)
            div_text = str(row['div']) if row['div'] else ""
            div_fg   = row.get('div_color', ACCENT)
            tk.Label(rf, text=f" {div_text}",
                     font=F_COL, bg=PANEL,
                     fg=div_fg if div_text else PANEL).pack(side="left")

        # Horizontal line at bottom of column
        tk.Frame(self.column_frame, bg=BORDER, height=2).pack(
            fill="x", pady=(4, 0))

    def _add_row(self, num, div=None, div_color=ACCENT):
        self.col_rows.append({"num": num, "div": div, "div_color": div_color})
        self._draw_column()

    def _set_last_div(self, div, color=ACCENT):
        if self.col_rows:
            self.col_rows[-1]["div"] = div
            self.col_rows[-1]["div_color"] = color
            self._draw_column()

    # ── New task ───────────────────────────────────────────────────────────
    def _new_task(self):
        self.start_num = generate_number()
        self.cur_num   = self.start_num
        self.factors   = []
        self.col_rows  = []
        self.np_input  = ""
        self.step_state = "pick"

        if self.column_frame:
            for w in self.column_frame.winfo_children():
                w.destroy()

        self._add_row(self.start_num)
        self._show_pick_panel()
        if self.result_lbl:
            self.result_lbl.config(text="")
        if self.score_lbl:
            self.score_lbl.config(
                text=f"Правильно: {self.score}  /  Завдань: {self.attempts}")

    # ── Panel switching ────────────────────────────────────────────────────
    def _show_pick_panel(self):
        self.step_state = "pick"
        if self.enter_frame: self.enter_frame.pack_forget()
        if self.prime_frame: self.prime_frame.pack()
        # Enable all prime buttons
        for p, b in self.prime_btns.items():
            b.config(state="normal")
            fg_c, bg_c = PRIME_COLORS[PRIMES_LIST.index(p) % len(PRIME_COLORS)]
            b.config(bg=bg_c)
        if self.instr_lbl:
            self.instr_lbl.config(
                text=f"На що ділиться  {self.cur_num}?\nОбери просте число:",
                fg=TEXT)

    def _show_enter_panel(self):
        self.step_state = "enter"
        if self.prime_frame: self.prime_frame.pack_forget()
        if self.enter_frame: self.enter_frame.pack()
        self.np_input = ""
        if self.np_disp: self.np_disp.config(text="?", fg=ACCENT)
        if self.instr_lbl:
            self.instr_lbl.config(
                text=f"{self.cur_num}  ÷  {self.chosen_div}  =  ?",
                fg=ACCENT)

    # ── Prime button clicked ───────────────────────────────────────────────
    def _on_prime(self, p):
        if self.cur_num == 1:
            return

        if self.cur_num % p != 0:
            # Wrong — flash red
            self.instr_lbl.config(
                text=f"❌  {self.cur_num} не ділиться на {p}!\n"
                     f"Спробуй інше число.",
                fg=RED)
            b = self.prime_btns.get(p)
            if b:
                b.config(bg=RED_LT)
                self.after(700, lambda: b.config(
                    bg=PRIME_COLORS[PRIMES_LIST.index(p) % len(PRIME_COLORS)][1]))
            return

        # Correct prime chosen
        self.chosen_div = p
        div_color = PRIME_COLORS[PRIMES_LIST.index(p) % len(PRIME_COLORS)][0]
        self._set_last_div(p, color=div_color)
        self.factors.append(p)
        self.expected_q = self.cur_num // p

        if self.trainer_mode == "auto":
            self._apply_quotient()
        else:
            self._show_enter_panel()

    def _apply_quotient(self):
        self.cur_num = self.expected_q
        if self.cur_num == 1:
            self._add_row(1)
            self._finish()
        else:
            self._add_row(self.cur_num)
            self._show_pick_panel()

    # ── Numpad ────────────────────────────────────────────────────────────
    def _on_numpad(self, ch):
        if ch == "C":
            self.np_input = ""
        elif ch == "OK":
            self._check_quotient()
            return
        elif ch.isdigit():
            if len(self.np_input) < 6:
                self.np_input += ch
        if self.np_disp:
            self.np_disp.config(text=self.np_input if self.np_input else "?")

    def _check_quotient(self):
        if not self.np_input:
            return
        entered = int(self.np_input)
        if entered == self.expected_q:
            # Correct
            self.np_disp.config(fg=GREEN)
            self.after(300, self._apply_quotient)
        else:
            self.instr_lbl.config(
                text=f"❌  Не так!  {self.cur_num} ÷ {self.chosen_div} ≠ {entered}\n"
                     f"Спробуй ще раз.",
                fg=RED)
            self.np_input = ""
            if self.np_disp:
                self.np_disp.config(text="?", fg=RED)
            self.after(700, lambda: self.np_disp.config(fg=ACCENT) if self.np_disp else None)

    # ── Finish ────────────────────────────────────────────────────────────
    def _finish(self):
        self.attempts += 1
        self.score    += 1   # reaching finish = success
        if self.score_lbl:
            self.score_lbl.config(
                text=f"Правильно: {self.score}  /  Завдань: {self.attempts}")

        if self.prime_frame:  self.prime_frame.pack_forget()
        if self.enter_frame:  self.enter_frame.pack_forget()

        factors_str = "  ×  ".join(map(str, self.factors))
        if self.instr_lbl:
            self.instr_lbl.config(text="", fg=TEXT)
        if self.result_lbl:
            self.result_lbl.config(
                text=f"🎉  Чудово!\n\n{self.start_num}  =  {factors_str}",
                fg=GREEN)

        # Re-pack New button already present; re-show prime frame disabled for display
        if self.prime_frame:
            self.prime_frame.pack()
            for b in self.prime_btns.values():
                b.config(state="disabled", bg=BTN_NUM)


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
