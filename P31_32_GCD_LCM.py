import tkinter as tk
import random
import math
from collections import Counter

# ── Palette (unified with series) ────────────────────────────────────────────
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
ACCENT    = "#1d4ed8"   # blue  — GCD
ACCENT2   = "#7c3aed"   # violet — LCM
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

# Factor-button colour wheel
FACTOR_COLORS = [
    ("#1d4ed8", "#dbeafe"),
    ("#15803d", "#dcfce7"),
    ("#b45309", "#fef9c3"),
    ("#b91c1c", "#fee2e2"),
    ("#7c3aed", "#ede9fe"),
    ("#0f766e", "#ccfbf1"),
]

# ── Fonts ─────────────────────────────────────────────────────────────────────
F_TITLE  = ("Segoe UI", 34, "bold")
F_HEAD   = ("Segoe UI", 26, "bold")
F_SUB    = ("Segoe UI", 20, "bold")
F_BODY   = ("Segoe UI", 17)
F_BODYB  = ("Segoe UI", 17, "bold")
F_BIG    = ("Segoe UI", 72, "bold")
F_BTN    = ("Segoe UI", 19, "bold")
F_NAV    = ("Segoe UI", 14, "bold")
F_SCORE  = ("Segoe UI", 20, "bold")
F_FEED   = ("Segoe UI", 16)
F_NUM    = ("Segoe UI", 26, "bold")
F_SMALL  = ("Segoe UI", 13)
F_COL    = ("Courier New", 32, "bold")
F_EXPR   = ("Segoe UI", 28, "bold")
F_PRIME  = ("Segoe UI", 22, "bold")


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
    tk.Label(f, text=body, font=F_BODY, bg=bg_c, fg=TEXT,
             justify="left", wraplength=1300, anchor="w").pack(
        fill="x", pady=(6, 0))
    return f


def factorize(n):
    """Return sorted list of prime factors."""
    fs = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            fs.append(d); n //= d
        d += 1
    if n > 1:
        fs.append(n)
    return fs


def fmt(factors):
    return "  ×  ".join(map(str, factors))


def generate_pair():
    """
    Generate two composites A, B that share at least one common factor
    and are not too large for a 5th-grader.
    """
    while True:
        fA = sorted(random.choices([2, 2, 3, 3, 5, 7], k=random.randint(2, 3)))
        fB = sorted(random.choices([2, 3, 3, 5, 5, 7], k=random.randint(2, 3)))
        a, b = math.prod(fA), math.prod(fB)
        cA, cB = Counter(fA), Counter(fB)
        common = list((cA & cB).elements())
        if common and a != b and a <= 200 and b <= 200:
            return fA, fB, a, b


# ══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("§ 31-32.  НСД та НСК натуральних чисел")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()
        self.current_frame = None
        self.mode = None

        # ── Trainer: GCD (numpad answer) ─────────────────────────────────
        self.gcd_a = self.gcd_b = 0
        self.gcd_input = ""
        self.gcd_score = self.gcd_attempts = 0
        self.gcd_done = False
        self.gcd_num_lbl = self.gcd_inp_lbl = None
        self.gcd_feed_lbl = self.gcd_score_lbl = None
        self.gcd_check_btn = None

        # ── Trainer: LCM (numpad answer) ─────────────────────────────────
        self.lcm_a = self.lcm_b = 0
        self.lcm_input = ""
        self.lcm_score = self.lcm_attempts = 0
        self.lcm_done = False
        self.lcm_num_lbl = self.lcm_inp_lbl = None
        self.lcm_feed_lbl = self.lcm_score_lbl = None
        self.lcm_check_btn = None

        # ── Trainer: Constructor (factor-picking) ─────────────────────────
        self.con_fA = self.con_fB = []
        self.con_a = self.con_b = 0
        self.con_gcd_f = self.con_lcm_f = []
        self.con_user_f = []
        self.con_phase = 1          # 1 = GCD, 2 = LCM
        self.con_score = self.con_attempts = 0
        self.con_num_lbl_a = self.con_num_lbl_b = None
        self.con_phase_lbl = None
        self.con_expr_lbl = None
        self.con_fbtn_frame = None
        self.con_feed_lbl = None
        self.con_score_lbl = None
        self.con_check_btn = None

        self._build_chrome()
        self.show_main_menu()

    # ── Chrome ────────────────────────────────────────────────────────────────
    def _build_chrome(self):
        hdr = tk.Frame(self, bg=HDR_BG, height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="§ 31-32.   НСД та НСК натуральних чисел",
                 bg=HDR_BG, fg=WHITE,
                 font=("Segoe UI", 21, "bold")).pack(side="left", padx=30)
        mkbtn(hdr, "✕  Вийти", self.destroy, bg="#b91c1c",
              font=("Segoe UI", 13, "bold"), w=9, h=1).pack(
            side="right", padx=18, pady=16)

        nav = tk.Frame(self, bg=NAV_BG, height=52)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        for label, cmd in [
            ("🏠  Меню",              self.show_main_menu),
            ("📖  Теорія: НСД",       self.show_gcd_theory),
            ("📖  Теорія: НСК",       self.show_lcm_theory),
            ("🎯  Тренажер: НСД",     self.show_gcd_trainer),
            ("🎯  Тренажер: НСК",     self.show_lcm_trainer),
            ("🧩  Конструктор НСД/НСК", self.show_constructor),
        ]:
            b = tk.Button(nav, text=label, command=cmd,
                          bg=NAV_BG, fg=NAV_FG, font=F_NAV,
                          relief="flat", bd=0, cursor="hand2",
                          activebackground=ACCENT, activeforeground=WHITE,
                          padx=14, pady=14)
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

        tk.Label(center, text="НСД та НСК",
                 font=("Segoe UI", 50, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 4))
        tk.Label(center, text="натуральних чисел",
                 font=("Segoe UI", 28), bg=BG, fg=ACCENT).pack(pady=(0, 30))

        cards = [
            ("📖", "Теорія\nНСД",       CARD_B, ACCENT,  self.show_gcd_theory),
            ("📖", "Теорія\nНСК",       CARD_V, ACCENT2, self.show_lcm_theory),
            ("🎯", "Тренажер\nНСД",     CARD_G, GREEN,   self.show_gcd_trainer),
            ("🎯", "Тренажер\nНСК",     CARD_Y, ORANGE,  self.show_lcm_trainer),
            ("🧩", "Конструктор\nНСД/НСК", CARD_B, ACCENT, self.show_constructor),
        ]
        row = tk.Frame(center, bg=BG)
        row.pack()
        for icon, title, bg_c, fg_c, cmd in cards:
            c = tk.Frame(row, bg=bg_c, width=210, height=200,
                         highlightbackground=BORDER, highlightthickness=2)
            c.pack(side="left", padx=12)
            c.pack_propagate(False)
            tk.Label(c, text=icon, font=("Segoe UI", 36),
                     bg=bg_c, fg=fg_c).pack(pady=(20, 4))
            tk.Label(c, text=title, font=("Segoe UI", 14, "bold"),
                     bg=bg_c, fg=fg_c, justify="center").pack()
            orig = bg_c
            for w in [c] + list(c.winfo_children()):
                w.bind("<Button-1>", lambda e, f=cmd: f())
            c.bind("<Enter>", lambda e, x=c, col=orig: x.config(bg=_darken(col, 12)))
            c.bind("<Leave>", lambda e, x=c, col=orig: x.config(bg=col))

        tk.Label(center, text="Натисніть на картку або скористайтесь меню зверху",
                 font=F_SMALL, bg=BG, fg=MUTED).pack(pady=18)

    # ══════════════════════════════════════════════════════════════════════════
    # SCROLLABLE THEORY WRAPPER
    # ══════════════════════════════════════════════════════════════════════════
    def _make_scroll_page(self):
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
        return p

    # ══════════════════════════════════════════════════════════════════════════
    # THEORY — GCD
    # ══════════════════════════════════════════════════════════════════════════
    def show_gcd_theory(self):
        self.clear_main()
        self.mode = "theory_gcd"
        p = self._make_scroll_page()

        tk.Label(p, text="Найбільший спільний дільник (НСД)",
                 font=F_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        hline(p, ACCENT)

        theory_card(p, "📌  Означення",
                    "НСД двох натуральних чисел — це найбільше натуральне число,\n"
                    "на яке ділиться кожне з цих чисел без остачі.\n\n"
                    "Позначення:  НСД(A, B)  або  гcd(A, B)",
                    CARD_B, ACCENT)

        theory_card(p, "🔑  Як знайти НСД через розкладання на множники",
                    "1. Розкласти обидва числа на прості множники.\n"
                    "2. Виписати ТІЛЬКИ СПІЛЬНІ прості множники (ті, що є в обох розкладах).\n"
                    "3. Якщо спільний множник зустрічається кілька разів — беремо його\n"
                    "   стільки разів, скільки він є в ОБОХ числах одночасно (мінімум).\n"
                    "4. НСД = добуток цих спільних множників.",
                    CARD_G, GREEN)

        # ── Visual example 12 and 18 ──────────────────────────────────────
        ex = tk.Frame(p, bg=PANEL, padx=24, pady=16,
                      highlightbackground=BORDER, highlightthickness=1)
        ex.pack(fill="x", pady=8)
        tk.Label(ex, text="📊  Приклад:  НСД(12, 18)",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(anchor="w")

        cols = tk.Frame(ex, bg=PANEL)
        cols.pack(anchor="w", padx=20, pady=10)

        def factor_row(parent, label, factors, highlight, bg_c):
            rf = tk.Frame(parent, bg=bg_c, padx=14, pady=8,
                          highlightbackground=BORDER, highlightthickness=1)
            rf.pack(fill="x", pady=4)
            tk.Label(rf, text=label, font=F_BODYB, bg=bg_c,
                     fg=TEXT, width=14, anchor="w").pack(side="left")
            for i, f in enumerate(factors):
                is_common = f in highlight and highlight[f] > 0
                if is_common:
                    highlight[f] -= 1
                bc = GREEN_LT if is_common else BTN_NUM
                fc = GREEN    if is_common else MUTED
                tk.Label(rf, text=str(f), font=F_PRIME,
                         bg=bc, fg=fc, width=3, relief="flat",
                         padx=6, pady=4).pack(side="left", padx=3)

        from collections import Counter as Ctr
        fA12 = [2, 2, 3];  fB18 = [2, 3, 3]
        hl12 = dict(Ctr(fA12) & Ctr(fB18))
        hl18 = dict(Ctr(fA12) & Ctr(fB18))
        factor_row(cols, "12  =", fA12, hl12, CARD_B)
        factor_row(cols, "18  =", fB18, hl18, CARD_V)
        tk.Label(ex,
                 text="Спільні (зелені):  2  і  3   →   НСД(12, 18)  =  2 × 3  =  6",
                 font=F_HEAD, bg=PANEL, fg=GREEN).pack(anchor="w", padx=20, pady=(6, 2))

        theory_card(p, "⚡  Особливі випадки",
                    "• Якщо числа не мають спільних простих множників — НСД = 1.\n"
                    "  Такі числа називають взаємно простими.\n"
                    "  Приклад:  НСД(4, 9) = 1  (4 = 2×2,  9 = 3×3 — спільних немає)\n\n"
                    "• НСД(a, a) = a  (НСД числа з самим собою = саме число)",
                    CARD_Y, ORANGE)

        theory_card(p, "💡  Практична підказка",
                    "НСД(12, 18) = 6  означає, що найбільший шматочок, на які можна\n"
                    "рівно розрізати і 12 і 18 — це шматочок розміром 6.",
                    "#f1f5f9", MUTED)

    # ══════════════════════════════════════════════════════════════════════════
    # THEORY — LCM
    # ══════════════════════════════════════════════════════════════════════════
    def show_lcm_theory(self):
        self.clear_main()
        self.mode = "theory_lcm"
        p = self._make_scroll_page()

        tk.Label(p, text="Найменше спільне кратне (НСК)",
                 font=F_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        hline(p, ACCENT2)

        theory_card(p, "📌  Означення",
                    "НСК двох натуральних чисел — це найменше натуральне число,\n"
                    "яке ділиться на кожне з цих чисел без остачі.\n\n"
                    "Позначення:  НСК(A, B)  або  lcm(A, B)",
                    CARD_V, ACCENT2)

        theory_card(p, "🔑  Як знайти НСК через розкладання на множники",
                    "1. Розкласти обидва числа на прості множники.\n"
                    "2. Виписати ВСІ прості множники, що зустрічаються хоча б в одному числі.\n"
                    "3. Якщо множник зустрічається в обох — беремо його стільки разів,\n"
                    "   скільки він є в ТОМУ числі, де його БІЛЬШЕ (максимум).\n"
                    "4. НСК = добуток усіх відібраних множників.",
                    CARD_G, GREEN)

        # ── Visual example 12 and 18 ──────────────────────────────────────
        ex = tk.Frame(p, bg=PANEL, padx=24, pady=16,
                      highlightbackground=BORDER, highlightthickness=1)
        ex.pack(fill="x", pady=8)
        tk.Label(ex, text="📊  Приклад:  НСК(12, 18)",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(anchor="w")

        inner = tk.Frame(ex, bg=PANEL, padx=12)
        inner.pack(anchor="w", pady=10)

        rows_data = [
            ("12  =", [2, 2, 3], CARD_B),
            ("18  =", [2, 3, 3], CARD_V),
            ("НСК =", [2, 2, 3, 3], CARD_G),   # union: max(2,1)×2 + max(1,2)×3
        ]
        lcm_colors = {2: ACCENT, 3: ACCENT2}
        for label, factors, bg_c in rows_data:
            rf = tk.Frame(inner, bg=bg_c, padx=14, pady=8,
                          highlightbackground=BORDER, highlightthickness=1)
            rf.pack(fill="x", pady=4)
            tk.Label(rf, text=label, font=F_BODYB, bg=bg_c,
                     fg=TEXT, width=10, anchor="w").pack(side="left")
            for f in factors:
                fc = lcm_colors.get(f, MUTED)
                tk.Label(rf, text=str(f), font=F_PRIME,
                         bg=BTN_NUM, fg=fc, width=3,
                         padx=6, pady=4).pack(side="left", padx=3)

        tk.Label(ex,
                 text="НСК(12, 18)  =  2 × 2 × 3 × 3  =  36",
                 font=F_HEAD, bg=PANEL, fg=GREEN).pack(anchor="w", padx=20, pady=(6, 2))
        tk.Label(ex,
                 text="Перевірка:  36 ÷ 12 = 3 ✅     36 ÷ 18 = 2 ✅",
                 font=F_BODY, bg=PANEL, fg=MUTED).pack(anchor="w", padx=20)

        theory_card(p, "⚡  Зв'язок НСД і НСК",
                    "Для будь-яких двох чисел A і B:\n\n"
                    "   НСД(A, B)  ×  НСК(A, B)  =  A  ×  B\n\n"
                    "Приклад:  НСД(12, 18) = 6,   НСК(12, 18) = 36\n"
                    "   6 × 36 = 216   і   12 × 18 = 216  ✅",
                    CARD_Y, ORANGE)

        theory_card(p, "💡  Практична підказка",
                    "НСК(12, 18) = 36  означає: якщо купувати товар,\n"
                    "що продається по 12 або по 18 штук у пачці,\n"
                    "найменша кількість, що ділиться на обидва — 36.",
                    "#f1f5f9", MUTED)

    # ══════════════════════════════════════════════════════════════════════════
    # NUMPAD INPUT HELPER  (shared between GCD / LCM trainers)
    # ══════════════════════════════════════════════════════════════════════════
    def _build_numpad(self, parent, key_fn):
        np = tk.Frame(parent, bg=BG)
        for row_chars in [("7","8","9"),("4","5","6"),("1","2","3"),("C","0","⌫")]:
            rf = tk.Frame(np, bg=BG)
            rf.pack(pady=4)
            for ch in row_chars:
                if ch.isdigit():   bc, fc = BTN_NUM, TEXT
                elif ch == "C":    bc, fc = RED_LT,  RED
                else:              bc, fc = CARD_V,  ACCENT2
                b = tk.Button(rf, text=ch, font=F_NUM, width=4, height=1,
                              bg=bc, fg=fc, relief="flat", cursor="hand2",
                              command=lambda c=ch: key_fn(c))
                b.pack(side="left", padx=5)
                orig = bc
                b.bind("<Enter>", lambda e, x=b, o=orig: x.config(bg=_darken(o, 18)))
                b.bind("<Leave>", lambda e, x=b, o=orig: x.config(bg=o))
        return np

    # ── shared score bar ──────────────────────────────────────────────────────
    def _score_bar(self, parent, text_lbl, score_var_fn):
        sbar = tk.Frame(parent, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        lbl = tk.Label(sbar, text=score_var_fn(),
                       font=F_SCORE, bg=PANEL, fg=GREEN)
        lbl.pack(side="left", padx=30)
        tk.Label(sbar, text=text_lbl,
                 font=("Segoe UI", 15, "bold"), bg=PANEL, fg=MUTED).pack(
            side="left", padx=10)
        return lbl

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER — GCD
    # ══════════════════════════════════════════════════════════════════════════
    def show_gcd_trainer(self):
        self.clear_main()
        self.mode = "gcd_trainer"
        self.gcd_done = False

        cf = self.current_frame
        self.gcd_score_lbl = self._score_bar(
            cf, "Знайди НСД двох чисел",
            lambda: f"Правильно: {self.gcd_score}  /  Завдань: {self.gcd_attempts}")

        center = tk.Frame(cf, bg=BG)
        center.pack(expand=True)

        # Task display
        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=28, pady=12)
        task_f.pack(pady=(14, 6))
        tk.Label(task_f, text="Знайди  НСД ( A, B )",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack()

        nums_row = tk.Frame(task_f, bg=PANEL)
        nums_row.pack(pady=6)
        self.gcd_num_lbl = tk.Label(nums_row, text="",
                                     font=F_BIG, bg=PANEL, fg=ACCENT)
        self.gcd_num_lbl.pack()

        # Hint: factorizations shown after first wrong attempt
        self.gcd_hint_lbl = tk.Label(center, text="",
                                      font=F_BODY, bg=BG, fg=MUTED,
                                      justify="center")
        self.gcd_hint_lbl.pack(pady=2)

        # Input display
        inp_f = tk.Frame(center, bg=BTN_NUM,
                         highlightbackground=ACCENT, highlightthickness=2,
                         padx=14, pady=6)
        inp_f.pack(pady=6)
        tk.Label(inp_f, text="НСД =", font=F_BODYB,
                 bg=BTN_NUM, fg=MUTED).pack(side="left")
        self.gcd_inp_lbl = tk.Label(inp_f, text="",
                                     font=("Segoe UI", 44, "bold"),
                                     bg=BTN_NUM, fg=ACCENT, width=5)
        self.gcd_inp_lbl.pack(side="left", padx=10)

        # Feedback
        self.gcd_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                      bg=BG, fg=ORANGE,
                                      wraplength=680, justify="center")
        self.gcd_feed_lbl.pack(pady=4)

        # Numpad
        self._build_numpad(center, self._gcd_key).pack(pady=6)

        act = tk.Frame(center, bg=BG)
        act.pack(pady=8)
        self.gcd_check_btn = mkbtn(act, "✔  Перевірити", self._gcd_check,
                                    bg=GREEN, w=14, h=2)
        self.gcd_check_btn.pack(side="left", padx=10)
        mkbtn(act, "▶  Наступне", self._gcd_new,
              bg=ACCENT, w=12, h=2).pack(side="left", padx=10)

        self._gcd_new()

    def _gcd_new(self):
        fA, fB, a, b = generate_pair()
        self.gcd_a, self.gcd_b = a, b
        self._gcd_fA, self._gcd_fB = fA, fB
        self.gcd_input = ""
        self.gcd_done = False
        self.gcd_attempts += 1
        if self.gcd_num_lbl:
            self.gcd_num_lbl.config(text=f"A = {a}        B = {b}", fg=ACCENT)
        if self.gcd_inp_lbl:   self.gcd_inp_lbl.config(text="", fg=ACCENT)
        if self.gcd_feed_lbl:  self.gcd_feed_lbl.config(text="")
        if self.gcd_hint_lbl:  self.gcd_hint_lbl.config(text="")
        if self.gcd_check_btn: self.gcd_check_btn.config(state="normal", bg=GREEN)
        if self.gcd_score_lbl:
            self.gcd_score_lbl.config(
                text=f"Правильно: {self.gcd_score}  /  Завдань: {self.gcd_attempts}")

    def _gcd_key(self, ch):
        if self.gcd_done: return
        if ch.isdigit():
            if len(self.gcd_input) < 5: self.gcd_input += ch
        elif ch == "⌫": self.gcd_input = self.gcd_input[:-1]
        elif ch == "C":  self.gcd_input = ""
        if self.gcd_inp_lbl: self.gcd_inp_lbl.config(text=self.gcd_input)

    def _gcd_check(self):
        if not self.gcd_input.strip():
            if self.gcd_feed_lbl:
                self.gcd_feed_lbl.config(text="⚠️  Введіть відповідь!", fg=ORANGE)
            return
        val = int(self.gcd_input)
        correct = math.gcd(self.gcd_a, self.gcd_b)
        self.gcd_input = ""
        if self.gcd_inp_lbl: self.gcd_inp_lbl.config(text="")

        if val == correct:
            self.gcd_score += 1
            self.gcd_done = True
            cA, cB = Counter(self._gcd_fA), Counter(self._gcd_fB)
            common = list((cA & cB).elements())
            if self.gcd_feed_lbl:
                self.gcd_feed_lbl.config(
                    text=f"🎉  Правильно!\n"
                         f"{self.gcd_a} = {fmt(self._gcd_fA)}\n"
                         f"{self.gcd_b} = {fmt(self._gcd_fB)}\n"
                         f"Спільні: {fmt(common)}  →  НСД = {correct}",
                    fg=GREEN)
            if self.gcd_inp_lbl: self.gcd_inp_lbl.config(fg=GREEN)
            if self.gcd_check_btn: self.gcd_check_btn.config(state="disabled", bg=BTN_NUM)
        else:
            # Show factorization hint
            if self.gcd_hint_lbl:
                self.gcd_hint_lbl.config(
                    text=f"Підказка:  {self.gcd_a} = {fmt(self._gcd_fA)}     "
                         f"{self.gcd_b} = {fmt(self._gcd_fB)}",
                    fg=MUTED)
            if self.gcd_feed_lbl:
                self.gcd_feed_lbl.config(
                    text=f"❌  {val} — не правильно. Спробуй ще!",
                    fg=RED)

        if self.gcd_score_lbl:
            self.gcd_score_lbl.config(
                text=f"Правильно: {self.gcd_score}  /  Завдань: {self.gcd_attempts}")

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER — LCM
    # ══════════════════════════════════════════════════════════════════════════
    def show_lcm_trainer(self):
        self.clear_main()
        self.mode = "lcm_trainer"
        self.lcm_done = False

        cf = self.current_frame
        self.lcm_score_lbl = self._score_bar(
            cf, "Знайди НСК двох чисел",
            lambda: f"Правильно: {self.lcm_score}  /  Завдань: {self.lcm_attempts}")

        center = tk.Frame(cf, bg=BG)
        center.pack(expand=True)

        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=28, pady=12)
        task_f.pack(pady=(14, 6))
        tk.Label(task_f, text="Знайди  НСК ( A, B )",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack()
        self.lcm_num_lbl = tk.Label(task_f, text="",
                                     font=F_BIG, bg=PANEL, fg=ACCENT2)
        self.lcm_num_lbl.pack(pady=6)

        self.lcm_hint_lbl = tk.Label(center, text="",
                                      font=F_BODY, bg=BG, fg=MUTED,
                                      justify="center")
        self.lcm_hint_lbl.pack(pady=2)

        inp_f = tk.Frame(center, bg=BTN_NUM,
                         highlightbackground=ACCENT2, highlightthickness=2,
                         padx=14, pady=6)
        inp_f.pack(pady=6)
        tk.Label(inp_f, text="НСК =", font=F_BODYB,
                 bg=BTN_NUM, fg=MUTED).pack(side="left")
        self.lcm_inp_lbl = tk.Label(inp_f, text="",
                                     font=("Segoe UI", 44, "bold"),
                                     bg=BTN_NUM, fg=ACCENT2, width=5)
        self.lcm_inp_lbl.pack(side="left", padx=10)

        self.lcm_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                      bg=BG, fg=ORANGE,
                                      wraplength=680, justify="center")
        self.lcm_feed_lbl.pack(pady=4)

        self._build_numpad(center, self._lcm_key).pack(pady=6)

        act = tk.Frame(center, bg=BG)
        act.pack(pady=8)
        self.lcm_check_btn = mkbtn(act, "✔  Перевірити", self._lcm_check,
                                    bg=GREEN, w=14, h=2)
        self.lcm_check_btn.pack(side="left", padx=10)
        mkbtn(act, "▶  Наступне", self._lcm_new,
              bg=ACCENT2, w=12, h=2).pack(side="left", padx=10)

        self._lcm_new()

    def _lcm_new(self):
        fA, fB, a, b = generate_pair()
        self.lcm_a, self.lcm_b = a, b
        self._lcm_fA, self._lcm_fB = fA, fB
        self.lcm_input = ""
        self.lcm_done = False
        self.lcm_attempts += 1
        if self.lcm_num_lbl:
            self.lcm_num_lbl.config(text=f"A = {a}        B = {b}", fg=ACCENT2)
        if self.lcm_inp_lbl:   self.lcm_inp_lbl.config(text="", fg=ACCENT2)
        if self.lcm_feed_lbl:  self.lcm_feed_lbl.config(text="")
        if self.lcm_hint_lbl:  self.lcm_hint_lbl.config(text="")
        if self.lcm_check_btn: self.lcm_check_btn.config(state="normal", bg=GREEN)
        if self.lcm_score_lbl:
            self.lcm_score_lbl.config(
                text=f"Правильно: {self.lcm_score}  /  Завдань: {self.lcm_attempts}")

    def _lcm_key(self, ch):
        if self.lcm_done: return
        if ch.isdigit():
            if len(self.lcm_input) < 6: self.lcm_input += ch
        elif ch == "⌫": self.lcm_input = self.lcm_input[:-1]
        elif ch == "C":  self.lcm_input = ""
        if self.lcm_inp_lbl: self.lcm_inp_lbl.config(text=self.lcm_input)

    def _lcm_check(self):
        if not self.lcm_input.strip():
            if self.lcm_feed_lbl:
                self.lcm_feed_lbl.config(text="⚠️  Введіть відповідь!", fg=ORANGE)
            return
        val = int(self.lcm_input)
        correct = self.lcm_a * self.lcm_b // math.gcd(self.lcm_a, self.lcm_b)
        self.lcm_input = ""
        if self.lcm_inp_lbl: self.lcm_inp_lbl.config(text="")

        if val == correct:
            self.lcm_score += 1
            self.lcm_done = True
            cA, cB = Counter(self._lcm_fA), Counter(self._lcm_fB)
            union = list((cA | cB).elements())
            if self.lcm_feed_lbl:
                self.lcm_feed_lbl.config(
                    text=f"🎉  Правильно!\n"
                         f"{self.lcm_a} = {fmt(self._lcm_fA)}\n"
                         f"{self.lcm_b} = {fmt(self._lcm_fB)}\n"
                         f"Усі (максимум):  {fmt(sorted(union))}  →  НСК = {correct}",
                    fg=GREEN)
            if self.lcm_inp_lbl: self.lcm_inp_lbl.config(fg=GREEN)
            if self.lcm_check_btn: self.lcm_check_btn.config(state="disabled", bg=BTN_NUM)
        else:
            if self.lcm_hint_lbl:
                self.lcm_hint_lbl.config(
                    text=f"Підказка:  {self.lcm_a} = {fmt(self._lcm_fA)}     "
                         f"{self.lcm_b} = {fmt(self._lcm_fB)}",
                    fg=MUTED)
            if self.lcm_feed_lbl:
                self.lcm_feed_lbl.config(
                    text=f"❌  {val} — не правильно. Спробуй ще!",
                    fg=RED)

        if self.lcm_score_lbl:
            self.lcm_score_lbl.config(
                text=f"Правильно: {self.lcm_score}  /  Завдань: {self.lcm_attempts}")

    # ══════════════════════════════════════════════════════════════════════════
    # CONSTRUCTOR  (factor-picking, two phases: GCD then LCM)
    # ══════════════════════════════════════════════════════════════════════════
    def show_constructor(self):
        self.clear_main()
        self.mode = "constructor"

        cf = self.current_frame

        # Score bar
        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.con_score_lbl = tk.Label(sbar,
            text=f"Правильно: {self.con_score}  /  Завдань: {self.con_attempts}",
            font=F_SCORE, bg=PANEL, fg=GREEN)
        self.con_score_lbl.pack(side="left", padx=30)
        tk.Label(sbar, text="Конструктор НСД та НСК — вибирай множники!",
                 font=("Segoe UI", 15, "bold"), bg=PANEL, fg=MUTED).pack(
            side="left", padx=10)

        # Two-column layout
        ws = tk.Frame(cf, bg=BG)
        ws.pack(fill="both", expand=True, padx=24, pady=14)

        # LEFT — given numbers
        left = tk.Frame(ws, bg=PANEL,
                        highlightbackground=BORDER, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        tk.Label(left, text="📋  Розкладені числа",
                 font=F_SUB, bg=PANEL, fg=MUTED).pack(anchor="w", padx=20, pady=(10, 4))
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x")

        # Number display rows with visual factor chips
        self.con_chips_frame = tk.Frame(left, bg=PANEL)
        self.con_chips_frame.pack(fill="both", expand=True, padx=20, pady=12)

        # RIGHT — constructor panel
        right = tk.Frame(ws, bg=PANEL,
                         highlightbackground=BORDER, highlightthickness=1,
                         width=int(self.SW * 0.44))
        right.pack(side="right", fill="both")
        right.pack_propagate(False)

        tk.Label(right, text="🧩  Збирай відповідь",
                 font=F_SUB, bg=PANEL, fg=MUTED).pack(anchor="w", padx=20, pady=(10, 4))
        tk.Frame(right, bg=BORDER, height=1).pack(fill="x")

        ctrl = tk.Frame(right, bg=PANEL)
        ctrl.pack(fill="both", expand=True, padx=16, pady=10)

        # Phase label
        self.con_phase_lbl = tk.Label(ctrl, text="",
                                       font=F_SUB, bg=PANEL, fg=ACCENT,
                                       wraplength=int(self.SW * 0.42) - 40,
                                       justify="center")
        self.con_phase_lbl.pack(pady=(4, 8))

        # User expression display
        expr_wrap = tk.Frame(ctrl, bg=BTN_NUM, padx=12, pady=8,
                             highlightbackground=ACCENT, highlightthickness=2)
        expr_wrap.pack(fill="x", pady=4)
        self.con_expr_lbl = tk.Label(expr_wrap, text="?",
                                      font=F_EXPR, bg=BTN_NUM, fg=ACCENT,
                                      anchor="center")
        self.con_expr_lbl.pack(fill="x")

        # Factor pick buttons
        self.con_fbtn_frame = tk.Frame(ctrl, bg=PANEL)
        self.con_fbtn_frame.pack(pady=8)

        # Feedback
        self.con_feed_lbl = tk.Label(ctrl, text="", font=F_FEED,
                                      bg=PANEL, fg=ORANGE,
                                      wraplength=int(self.SW * 0.42) - 40,
                                      justify="center")
        self.con_feed_lbl.pack(pady=4)

        # Action buttons
        act = tk.Frame(ctrl, bg=PANEL)
        act.pack(pady=8)
        mkbtn(act, "⌫  Стерти", self._con_undo, bg=ACCENT2, w=10, h=2).pack(
            side="left", padx=6)
        self.con_check_btn = mkbtn(act, "✔  Перевірити", self._con_check,
                                    bg=GREEN, w=12, h=2)
        self.con_check_btn.pack(side="left", padx=6)
        mkbtn(act, "▶  Далі", self._con_next, bg=ACCENT, w=10, h=2).pack(
            side="left", padx=6)

        self._con_new_task()

    # ── Constructor helpers ────────────────────────────────────────────────────
    def _con_draw_chips(self):
        """Redraw the left panel with factor chips."""
        for w in self.con_chips_frame.winfo_children():
            w.destroy()

        cA = Counter(self.con_fA)
        cB = Counter(self.con_fB)
        common = cA & cB

        for label, val, factors, bg_row in [
            (f"A  =  {self.con_a}", self.con_a, self.con_fA, CARD_B),
            (f"B  =  {self.con_b}", self.con_b, self.con_fB, CARD_V),
        ]:
            rf = tk.Frame(self.con_chips_frame, bg=bg_row, padx=14, pady=10,
                          highlightbackground=BORDER, highlightthickness=1)
            rf.pack(fill="x", pady=6)
            tk.Label(rf, text=label, font=F_BODYB, bg=bg_row,
                     fg=TEXT, anchor="w").pack(anchor="w", pady=(0, 6))
            chips = tk.Frame(rf, bg=bg_row)
            chips.pack(anchor="w")
            # Track how many common factors shown to highlight correctly
            common_remaining = dict(common)
            for f in factors:
                is_c = common_remaining.get(f, 0) > 0
                if is_c:
                    common_remaining[f] -= 1
                bc = GREEN_LT if is_c else BTN_NUM
                fc = GREEN    if is_c else MUTED
                chip = tk.Frame(chips, bg=bc, padx=8, pady=4,
                                highlightbackground=BORDER, highlightthickness=1)
                chip.pack(side="left", padx=3)
                tk.Label(chip, text=str(f), font=F_PRIME, bg=bc, fg=fc).pack()

        # Equation hint
        cA2, cB2 = Counter(self.con_fA), Counter(self.con_fB)
        gcd_f = sorted(list((cA2 & cB2).elements()))
        lcm_f = sorted(list((cA2 | cB2).elements()))

        hint_f = tk.Frame(self.con_chips_frame, bg=PANEL, padx=14, pady=8,
                          highlightbackground=BORDER, highlightthickness=1)
        hint_f.pack(fill="x", pady=6)
        tk.Label(hint_f, text="🔵  Спільні (зелені) → НСД",
                 font=F_SMALL, bg=PANEL, fg=ACCENT).pack(anchor="w")
        tk.Label(hint_f, text="🔴  Усі разом (максимум з кожного) → НСК",
                 font=F_SMALL, bg=PANEL, fg=ACCENT2).pack(anchor="w")

    def _con_rebuild_fbtns(self):
        """Rebuild factor pick buttons from unique available primes."""
        for w in self.con_fbtn_frame.winfo_children():
            w.destroy()
        available = sorted(set(self.con_fA + self.con_fB))
        for idx, p in enumerate(available):
            fg_c, bg_c = FACTOR_COLORS[idx % len(FACTOR_COLORS)]
            b = tk.Button(self.con_fbtn_frame, text=str(p),
                          font=F_PRIME, width=5, height=2,
                          bg=bg_c, fg=fg_c, relief="flat", cursor="hand2",
                          command=lambda x=p: self._con_add(x))
            b.pack(side="left", padx=8)
            orig = bg_c
            b.bind("<Enter>", lambda e, x=b, o=orig: x.config(bg=_darken(o, 15)))
            b.bind("<Leave>", lambda e, x=b, o=orig: x.config(bg=o))

    def _con_update_expr(self):
        if not self.con_user_f:
            if self.con_expr_lbl: self.con_expr_lbl.config(text="?", fg=ACCENT)
            return
        val = math.prod(self.con_user_f)
        s = "  ×  ".join(map(str, self.con_user_f))
        color = ACCENT if self.con_phase == 1 else ACCENT2
        if self.con_expr_lbl:
            self.con_expr_lbl.config(text=f"{s}  =  {val}", fg=color)

    def _con_new_task(self):
        fA, fB, a, b = generate_pair()
        self.con_fA, self.con_fB = fA, fB
        self.con_a,  self.con_b  = a,  b
        cA, cB = Counter(fA), Counter(fB)
        self.con_gcd_f = sorted(list((cA & cB).elements()))
        self.con_lcm_f = sorted(list((cA | cB).elements()))
        self.con_user_f = []
        self.con_phase  = 1
        self.con_attempts += 1
        self._con_draw_chips()
        self._con_rebuild_fbtns()
        self._con_set_phase_label()
        self._con_update_expr()
        if self.con_feed_lbl:  self.con_feed_lbl.config(text="")
        if self.con_check_btn: self.con_check_btn.config(state="normal", bg=GREEN)
        if self.con_score_lbl:
            self.con_score_lbl.config(
                text=f"Правильно: {self.con_score}  /  Завдань: {self.con_attempts}")

    def _con_set_phase_label(self):
        if self.con_phase == 1:
            gcd_val = math.prod(self.con_gcd_f) if self.con_gcd_f else 1
            if self.con_phase_lbl:
                self.con_phase_lbl.config(
                    text=f"Етап 1 з 2  —  НСД\n"
                         f"Вибери СПІЛЬНІ прості множники (зелені)",
                    fg=ACCENT)
        else:
            if self.con_phase_lbl:
                self.con_phase_lbl.config(
                    text=f"Етап 2 з 2  —  НСК\n"
                         f"Вибери ВСІ множники (максимум з кожного числа)",
                    fg=ACCENT2)

    def _con_add(self, p):
        if self.con_check_btn and str(self.con_check_btn["state"]) == "disabled":
            return
        self.con_user_f.append(p)
        self._con_update_expr()

    def _con_undo(self):
        if self.con_user_f:
            self.con_user_f.pop()
            self._con_update_expr()

    def _con_check(self):
        target = self.con_gcd_f if self.con_phase == 1 else self.con_lcm_f
        name   = "НСД" if self.con_phase == 1 else "НСК"
        t_val  = math.prod(target) if target else 1
        u_val  = math.prod(self.con_user_f) if self.con_user_f else 0

        if sorted(self.con_user_f) == target:
            self.con_score += 1
            if self.con_feed_lbl:
                self.con_feed_lbl.config(
                    text=f"🎉  Правильно!  {name}({self.con_a}, {self.con_b}) = "
                         f"{fmt(target)} = {t_val}",
                    fg=GREEN)
            if self.con_check_btn: self.con_check_btn.config(state="disabled", bg=BTN_NUM)
        else:
            if self.con_feed_lbl:
                self.con_feed_lbl.config(
                    text=f"❌  Не так!  Правильна відповідь: "
                         f"{fmt(target)} = {t_val}\n"
                         f"Ти вибрав: {fmt(self.con_user_f) if self.con_user_f else '(нічого)'} = {u_val}",
                    fg=RED)

        if self.con_score_lbl:
            self.con_score_lbl.config(
                text=f"Правильно: {self.con_score}  /  Завдань: {self.con_attempts}")

    def _con_next(self):
        if self.con_phase == 1:
            # Move to LCM phase
            self.con_phase = 2
            self.con_user_f = []
            self._con_set_phase_label()
            self._con_update_expr()
            if self.con_feed_lbl:  self.con_feed_lbl.config(text="")
            if self.con_check_btn: self.con_check_btn.config(state="normal", bg=GREEN)
        else:
            self._con_new_task()


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()