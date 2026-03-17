import tkinter as tk
import random
import math

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
TEAL      = "#0f766e"
TEAL_LT   = "#ccfbf1"

# ── Fonts ─────────────────────────────────────────────────────────────────────
F_TITLE  = ("Segoe UI", 30, "bold")
F_HEAD   = ("Segoe UI", 22, "bold")
F_SUB    = ("Segoe UI", 18, "bold")
F_BODY   = ("Segoe UI", 17)
F_BODYB  = ("Segoe UI", 17, "bold")
F_BIG    = ("Segoe UI", 72, "bold")
F_BTN    = ("Segoe UI", 19, "bold")
F_NAV    = ("Segoe UI", 14, "bold")
F_SCORE  = ("Segoe UI", 18, "bold")
F_FEED   = ("Segoe UI", 16)
F_NUM    = ("Segoe UI", 22, "bold")
F_SMALL  = ("Segoe UI", 13)
F_FRAC   = ("Segoe UI", 32, "bold")
F_FRAC_S = ("Segoe UI", 20, "bold")
F_STEP   = ("Segoe UI", 16, "bold")
F_STEP_V = ("Segoe UI", 16)


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


def fraction_widget(parent, numer, denom, bg=PANEL, size="big"):
    """Draw a visual fraction: numerator / line / denominator."""
    f = tk.Frame(parent, bg=bg)
    fn = F_FRAC if size == "big" else F_FRAC_S
    tk.Label(f, text=str(numer), font=fn, bg=bg, fg=ACCENT).pack()
    tk.Frame(f, bg=ACCENT, height=3, width=60 if size == "big" else 40).pack(pady=2)
    tk.Label(f, text=str(denom), font=fn, bg=bg, fg=ACCENT).pack()
    return f


def generate_task_frac_of_num():
    """
    Generate: find (a/b) of N
    Ensure N is divisible by b for clean answer.
    """
    while True:
        b = random.choice([2, 3, 4, 5, 6, 8, 10])
        a = random.randint(1, b - 1)
        # Pick N divisible by b, reasonable size
        k = random.randint(2, 20)
        N = b * k
        result = N // b * a
        if result > 0 and N <= 200 and math.gcd(a, b) == 1:
            return a, b, N, result


def generate_task_num_from_frac():
    """
    Generate: if (a/b) of M = P, find M.
    So M = P : a * b.
    """
    while True:
        b = random.choice([2, 3, 4, 5, 6, 8, 10])
        a = random.randint(1, b - 1)
        # Pick M divisible by b to get clean P
        k = random.randint(2, 15)
        M = b * k
        P = M // b * a   # P = (a/b) of M
        if P > 0 and M <= 200 and math.gcd(a, b) == 1:
            return a, b, M, P  # answer is M, given P


# ══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Звичайні дроби. Знаходження дробу і числа")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()
        self.current_frame = None
        self.mode = None

        # ── Trainer 1: Fraction of number ────────────────────────────────
        # Step 1: divide N by b  →  Step 2: multiply by a  →  answer
        self.t1_a = self.t1_b = self.t1_N = self.t1_ans = 0
        self.t1_step = 1          # 1 or 2
        self.t1_step1_val = 0     # result of step 1
        self.t1_input = ""
        self.t1_score = self.t1_attempts = 0
        self.t1_inp_lbl = None
        self.t1_feed_lbl = None
        self.t1_score_lbl = None
        self.t1_check_btn = None
        self.t1_step_lbl = None
        self.t1_step1_result_lbl = None

        # ── Trainer 2: Number from fraction ──────────────────────────────
        # Step 1: divide P by a  →  Step 2: multiply by b  →  answer M
        self.t2_a = self.t2_b = self.t2_M = self.t2_P = 0
        self.t2_step = 1
        self.t2_step1_val = 0
        self.t2_input = ""
        self.t2_score = self.t2_attempts = 0
        self.t2_inp_lbl = None
        self.t2_feed_lbl = None
        self.t2_score_lbl = None
        self.t2_check_btn = None
        self.t2_step_lbl = None
        self.t2_step1_result_lbl = None

        # ── Trainer 3: Free practice (random type, direct answer) ────────
        self.t3_type  = "frac"   # "frac" or "num"
        self.t3_a = self.t3_b = self.t3_N = self.t3_ans = 0
        self.t3_input = ""
        self.t3_score = self.t3_attempts = 0
        self.t3_inp_lbl   = None
        self.t3_feed_lbl  = None
        self.t3_score_lbl = None
        self.t3_check_btn = None
        self.t3_frac_frame = None
        self.t3_task_lbl   = None

        self._build_chrome()
        self.show_main_menu()

    # ── Chrome ────────────────────────────────────────────────────────────────
    def _build_chrome(self):
        hdr = tk.Frame(self, bg=HDR_BG, height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="Звичайні дроби.  Знаходження дробу і числа",
                 bg=HDR_BG, fg=WHITE,
                 font=("Segoe UI", 21, "bold")).pack(side="left", padx=30)
        mkbtn(hdr, "✕  Вийти", self.destroy, bg="#b91c1c",
              font=("Segoe UI", 13, "bold"), w=9, h=1).pack(
            side="right", padx=18, pady=16)

        nav = tk.Frame(self, bg=NAV_BG, height=52)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        for label, cmd in [
            ("🏠  Меню",                   self.show_main_menu),
            ("📖  Що таке дріб",           self.show_theory_intro),
            ("📖  Дріб від числа",         self.show_theory_frac_of_num),
            ("📖  Число за дробом",        self.show_theory_num_from_frac),
            ("🎯  Практика: дріб від числа",   self.show_trainer_1),
            ("🎯  Практика: число за дробом",  self.show_trainer_2),
            ("🏆  Вільна практика",            self.show_trainer_3),
        ]:
            b = tk.Button(nav, text=label, command=cmd,
                          bg=NAV_BG, fg=NAV_FG, font=F_NAV,
                          relief="flat", bd=0, cursor="hand2",
                          activebackground=ACCENT, activeforeground=WHITE,
                          padx=13, pady=14)
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

    def _scroll_page(self, px=60, py=28):
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
        p.pack(fill="both", expand=True, padx=px, pady=py)
        return p

    # ══════════════════════════════════════════════════════════════════════════
    # MAIN MENU
    # ══════════════════════════════════════════════════════════════════════════
    def show_main_menu(self):
        self.clear_main()
        self.mode = "menu"
        center = tk.Frame(self.current_frame, bg=BG)
        center.place(relx=.5, rely=.5, anchor="center")

        tk.Label(center, text="Звичайні дроби",
                 font=("Segoe UI", 50, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 4))
        tk.Label(center, text="знаходження дробу від числа  і  числа за дробом",
                 font=("Segoe UI", 22), bg=BG, fg=ACCENT).pack(pady=(0, 28))

        cards = [
            ("📖", "Що таке\nдріб",         CARD_B, ACCENT,  self.show_theory_intro),
            ("📖", "Дріб\nвід числа",       CARD_G, GREEN,   self.show_theory_frac_of_num),
            ("📖", "Число\nза дробом",      CARD_V, ACCENT2, self.show_theory_num_from_frac),
            ("🎯", "Практика\nдріб від числа\n(2 кроки)",  CARD_Y, ORANGE, self.show_trainer_1),
            ("🎯", "Практика\nчисло за дробом\n(2 кроки)", TEAL_LT, TEAL, self.show_trainer_2),
            ("🏆", "Вільна\nпрактика",      "#fce7f3", "#9d174d", self.show_trainer_3),
        ]
        row = tk.Frame(center, bg=BG)
        row.pack()
        for icon, title, bg_c, fg_c, cmd in cards:
            c = tk.Frame(row, bg=bg_c, width=210, height=200,
                         highlightbackground=BORDER, highlightthickness=2)
            c.pack(side="left", padx=11)
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
    # THEORY 1 — What is a fraction
    # ══════════════════════════════════════════════════════════════════════════
    def show_theory_intro(self):
        self.clear_main()
        self.mode = "theory_intro"
        p = self._scroll_page()

        tk.Label(p, text="Що таке звичайний дріб",
                 font=F_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        hline(p, ACCENT)

        # Означення — no text fractions, use inline widgets
        def_f = tk.Frame(p, bg=CARD_B, padx=22, pady=14,
                         highlightbackground=BORDER, highlightthickness=1)
        def_f.pack(fill="x", pady=7)
        tk.Label(def_f, text="📌  Означення",
                 font=F_SUB, bg=CARD_B, fg=ACCENT, anchor="w").pack(fill="x")
        tk.Label(def_f,
                 text="Якщо ціле ділять на b рівних частин і беруть a таких частин —\n"
                      "отримують дріб:",
                 font=F_BODY, bg=CARD_B, fg=TEXT, justify="left").pack(anchor="w", pady=(6, 4))
        frow0 = tk.Frame(def_f, bg=CARD_B)
        frow0.pack(anchor="w", pady=4)
        fraction_widget(frow0, "a", "b", CARD_B, "big").pack(side="left", padx=(0, 20))
        tk.Frame(frow0, bg=BORDER, width=2, height=80).pack(side="left", padx=16, fill="y")
        ann = tk.Frame(frow0, bg=CARD_B)
        ann.pack(side="left")
        tk.Label(ann, text="a  —  ЧИСЕЛЬНИК  (скільки частин взяли)",
                 font=F_BODY, bg=CARD_B, fg=TEXT, anchor="w").pack(anchor="w")
        tk.Label(ann, text="b  —  ЗНАМЕННИК  (на скільки частин поділили ціле)",
                 font=F_BODY, bg=CARD_B, fg=TEXT, anchor="w").pack(anchor="w", pady=(6, 0))
        tk.Label(ann, text="Читають: «a b-их»",
                 font=F_BODY, bg=CARD_B, fg=MUTED, anchor="w").pack(anchor="w", pady=(6, 0))

        # Visual: pizza slices
        vis_f = tk.Frame(p, bg=PANEL, padx=24, pady=20,
                         highlightbackground=BORDER, highlightthickness=1)
        vis_f.pack(fill="x", pady=8)
        tk.Label(vis_f, text="🍕  Наочний приклад: торт поділено на 8 частин, взяли 3",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(anchor="w", pady=(0, 12))
        pizza_row = tk.Frame(vis_f, bg=PANEL)
        pizza_row.pack(anchor="w")
        for i in range(8):
            color = ACCENT if i < 3 else BTN_NUM
            fc    = WHITE  if i < 3 else MUTED
            cell = tk.Frame(pizza_row, bg=color, width=70, height=70,
                            highlightbackground=BORDER, highlightthickness=1)
            cell.pack(side="left", padx=4)
            cell.pack_propagate(False)
            tk.Label(cell, text="🍕" if i < 3 else "○",
                     font=("Segoe UI", 22), bg=color, fg=fc).pack(expand=True)
        mid = tk.Frame(vis_f, bg=PANEL)
        mid.pack(anchor="w", pady=10)
        tk.Label(mid, text="Взяли  ", font=F_BODY, bg=PANEL, fg=TEXT).pack(side="left")
        fraction_widget(mid, 3, 8, PANEL, "big").pack(side="left", padx=10)
        tk.Label(mid, text="  торта  (три восьмих)", font=F_BODY, bg=PANEL, fg=TEXT).pack(side="left")

        # Правильний / неправильний — visual fraction rows, no text a/b
        pn_f = tk.Frame(p, bg=CARD_V, padx=22, pady=14,
                        highlightbackground=BORDER, highlightthickness=1)
        pn_f.pack(fill="x", pady=7)
        tk.Label(pn_f, text="📏  Правильний і неправильний дріб",
                 font=F_SUB, bg=CARD_V, fg=ACCENT2).pack(anchor="w")

        cols = tk.Frame(pn_f, bg=CARD_V)
        cols.pack(anchor="w", pady=10)

        # Правильні
        left_col = tk.Frame(cols, bg=CARD_B, padx=16, pady=12,
                            highlightbackground=BORDER, highlightthickness=1)
        left_col.pack(side="left", padx=(0, 16))
        tk.Label(left_col, text="Правильний дріб\n(чисельник < знаменника)",
                 font=F_BODYB, bg=CARD_B, fg=ACCENT, justify="center").pack(pady=(0, 8))
        fr_row = tk.Frame(left_col, bg=CARD_B)
        fr_row.pack()
        for n, d in [(3, 8), (1, 2), (5, 6)]:
            fraction_widget(fr_row, n, d, CARD_B, "small").pack(side="left", padx=10)
        tk.Label(left_col, text="дріб < 1", font=F_SMALL, bg=CARD_B, fg=MUTED).pack(pady=(6, 0))

        # Неправильні
        right_col = tk.Frame(cols, bg=CARD_R if hasattr(self, '_') else "#fee2e2",
                             padx=16, pady=12,
                             highlightbackground=BORDER, highlightthickness=1)
        right_col.config(bg="#fee2e2")
        right_col.pack(side="left")
        tk.Label(right_col, text="Неправильний дріб\n(чисельник ≥ знаменника)",
                 font=F_BODYB, bg="#fee2e2", fg=RED, justify="center").pack(pady=(0, 8))
        fr_row2 = tk.Frame(right_col, bg="#fee2e2")
        fr_row2.pack()
        for n, d in [(8, 8), (9, 4), (7, 3)]:
            fraction_widget(fr_row2, n, d, "#fee2e2", "small").pack(side="left", padx=10)
        tk.Label(right_col, text="дріб ≥ 1", font=F_SMALL, bg="#fee2e2", fg=RED).pack(pady=(6, 0))

        # Часто вживані дроби — visual table
        names_f = tk.Frame(p, bg=CARD_Y, padx=22, pady=14,
                           highlightbackground=BORDER, highlightthickness=1)
        names_f.pack(fill="x", pady=7)
        tk.Label(names_f, text="📐  Часто вживані дроби та їх назви",
                 font=F_SUB, bg=CARD_Y, fg=ORANGE).pack(anchor="w", pady=(0, 8))
        names_row = tk.Frame(names_f, bg=CARD_Y)
        names_row.pack(anchor="w")
        for n, d, name in [
            (1, 2, "одна друга\n(половина)"),
            (1, 3, "одна третя\n(третина)"),
            (1, 4, "одна четверта\n(чверть)"),
            (3, 4, "три четвертих"),
            (1, 5, "одна п'ята"),
            (2, 5, "дві п'ятих"),
            (1, 10, "одна десята"),
        ]:
            box = tk.Frame(names_row, bg=PANEL, padx=10, pady=8,
                           highlightbackground=BORDER, highlightthickness=1)
            box.pack(side="left", padx=5)
            fraction_widget(box, n, d, PANEL, "small").pack()
            tk.Label(box, text=name, font=F_SMALL, bg=PANEL, fg=MUTED,
                     justify="center").pack(pady=(4, 0))

    # ══════════════════════════════════════════════════════════════════════════
    # THEORY 2 — Fraction of number
    # ══════════════════════════════════════════════════════════════════════════
    def show_theory_frac_of_num(self):
        self.clear_main()
        self.mode = "theory_frac"
        p = self._scroll_page()

        tk.Label(p, text="Знаходження дробу від числа",
                 font=F_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        hline(p, GREEN)

        # Formula card
        formula_f = tk.Frame(p, bg=CARD_G, padx=24, pady=20,
                             highlightbackground=GREEN, highlightthickness=2)
        formula_f.pack(fill="x", pady=8)
        tk.Label(formula_f, text="🔑  Формула",
                 font=F_SUB, bg=CARD_G, fg=GREEN).pack(anchor="w")

        frow = tk.Frame(formula_f, bg=CARD_G)
        frow.pack(anchor="w", pady=10)
        tk.Label(frow, text="Щоб знайти  ", font=F_BODYB, bg=CARD_G, fg=TEXT).pack(side="left")
        fraction_widget(frow, "a", "b", CARD_G, "big").pack(side="left", padx=8)
        tk.Label(frow, text="  від числа  N  :", font=F_BODYB, bg=CARD_G, fg=TEXT).pack(side="left")

        steps_f = tk.Frame(formula_f, bg=CARD_G)
        steps_f.pack(anchor="w", pady=6)
        for step, color, txt in [
            ("Крок 1", ACCENT, "Поділи  N  на знаменник  b"),
            ("Крок 2", GREEN,  "Помнож результат на чисельник  a"),
        ]:
            row = tk.Frame(steps_f, bg=CARD_G)
            row.pack(anchor="w", pady=4)
            tk.Label(row, text=f"  {step}:  ", font=F_STEP, bg=CARD_G, fg=color, width=10, anchor="w").pack(side="left")
            tk.Label(row, text=txt, font=F_STEP_V, bg=CARD_G, fg=TEXT).pack(side="left")

        tk.Label(formula_f,
                 text="Результат:   N  :  b  ×  a",
                 font=F_HEAD, bg=CARD_G, fg=GREEN).pack(anchor="w", pady=(8, 0))

        # Example 1
        ex1 = tk.Frame(p, bg=PANEL, padx=24, pady=18,
                       highlightbackground=BORDER, highlightthickness=1)
        ex1.pack(fill="x", pady=8)

        # Task header with visual fraction
        t1row = tk.Frame(ex1, bg=PANEL)
        t1row.pack(anchor="w")
        tk.Label(t1row, text="✏️  Задача 1.  Скільки кілограмів становить  ",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(side="left")
        fraction_widget(t1row, 3, 5, PANEL, "small").pack(side="left", padx=6)
        tk.Label(t1row, text="  мішка (180 кг)?",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(side="left")

        sol1 = tk.Frame(ex1, bg=PANEL)
        sol1.pack(anchor="w", padx=20, pady=10)
        for label, color, calc, explain in [
            ("Крок 1", ACCENT, "180  :  5  =  36", "Знаходимо одну п'яту від 180"),
            ("Крок 2", GREEN,  "36   ×  3  =  108", "Беремо 3 такі частини"),
        ]:
            row = tk.Frame(sol1, bg=CARD_G, padx=16, pady=8,
                           highlightbackground=BORDER, highlightthickness=1)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=label, font=F_STEP, bg=CARD_G, fg=color,
                     width=8, anchor="w").pack(side="left")
            tk.Label(row, text=calc, font=("Segoe UI", 22, "bold"),
                     bg=CARD_G, fg=color).pack(side="left", padx=16)
            tk.Label(row, text=f"({explain})", font=F_SMALL,
                     bg=CARD_G, fg=MUTED).pack(side="left")

        tk.Label(ex1, text="Відповідь:  108 кг",
                 font=F_HEAD, bg=PANEL, fg=GREEN).pack(anchor="w", padx=20, pady=(6, 0))

        # Visual bar
        bar_f = tk.Frame(ex1, bg=PANEL)
        bar_f.pack(anchor="w", padx=20, pady=8)
        tk.Label(bar_f, text="Наочно (180 кг = 5 частин по 36 кг):",
                 font=F_SMALL, bg=PANEL, fg=MUTED).pack(anchor="w")
        bar_row = tk.Frame(bar_f, bg=PANEL)
        bar_row.pack(anchor="w", pady=4)
        for i in range(5):
            color = GREEN if i < 3 else BTN_NUM
            fc    = WHITE if i < 3 else MUTED
            cell = tk.Frame(bar_row, bg=color, width=100, height=54,
                            highlightbackground=BORDER, highlightthickness=1)
            cell.pack(side="left", padx=3)
            cell.pack_propagate(False)
            tk.Label(cell, text="36 кг", font=("Segoe UI", 13, "bold"),
                     bg=color, fg=fc).pack(expand=True)

        bar_ann = tk.Frame(bar_f, bg=PANEL)
        bar_ann.pack(anchor="w", pady=2)
        fraction_widget(bar_ann, 3, 5, PANEL, "small").pack(side="left")
        tk.Label(bar_ann, text="  від 180 кг  =  108 кг",
                 font=F_SMALL, bg=PANEL, fg=GREEN).pack(side="left", padx=6)

        # Example 2
        ex2 = tk.Frame(p, bg=CARD_Y, padx=24, pady=16,
                       highlightbackground=BORDER, highlightthickness=1)
        ex2.pack(fill="x", pady=8)

        t2row = tk.Frame(ex2, bg=CARD_Y)
        t2row.pack(anchor="w")
        tk.Label(t2row, text="✏️  Задача 2.  Знайди  ",
                 font=F_BODYB, bg=CARD_Y, fg=TEXT).pack(side="left")
        fraction_widget(t2row, 2, 3, CARD_Y, "small").pack(side="left", padx=6)
        tk.Label(t2row, text="  від числа 60.",
                 font=F_BODYB, bg=CARD_Y, fg=TEXT).pack(side="left")

        tk.Label(ex2,
                 text="60 : 3 = 20    (одна третя від 60)\n"
                      "20 × 2 = 40    (дві третіх від 60)\n\n"
                      "Відповідь:  40",
                 font=F_BODY, bg=CARD_Y, fg=TEXT,
                 justify="left").pack(anchor="w", padx=20, pady=6)

    # ══════════════════════════════════════════════════════════════════════════
    # THEORY 3 — Number from fraction
    # ══════════════════════════════════════════════════════════════════════════
    def show_theory_num_from_frac(self):
        self.clear_main()
        self.mode = "theory_num"
        p = self._scroll_page()

        tk.Label(p, text="Знаходження числа за значенням його дробу",
                 font=F_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        hline(p, ACCENT2)

        # Formula card
        formula_f = tk.Frame(p, bg=CARD_V, padx=24, pady=20,
                             highlightbackground=ACCENT2, highlightthickness=2)
        formula_f.pack(fill="x", pady=8)
        tk.Label(formula_f, text="🔑  Формула",
                 font=F_SUB, bg=CARD_V, fg=ACCENT2).pack(anchor="w")

        frow = tk.Frame(formula_f, bg=CARD_V)
        frow.pack(anchor="w", pady=10)
        fraction_widget(frow, "a", "b", CARD_V, "big").pack(side="left", padx=(0, 8))
        tk.Label(frow, text="  числа  СТАНОВИТЬ  P  :",
                 font=F_BODYB, bg=CARD_V, fg=TEXT).pack(side="left")

        steps_f = tk.Frame(formula_f, bg=CARD_V)
        steps_f.pack(anchor="w", pady=6)
        for step, color, txt in [
            ("Крок 1", ACCENT,  "Поділи  P  на чисельник  a  →  знайдеш одну b-ту частину числа"),
            ("Крок 2", ACCENT2, "Помнож результат на знаменник  b  →  знайдеш все число"),
        ]:
            row = tk.Frame(steps_f, bg=CARD_V)
            row.pack(anchor="w", pady=4)
            tk.Label(row, text=f"  {step}:  ", font=F_STEP, bg=CARD_V, fg=color,
                     width=10, anchor="w").pack(side="left")
            tk.Label(row, text=txt, font=F_STEP_V, bg=CARD_V, fg=TEXT).pack(side="left")

        tk.Label(formula_f,
                 text="Результат:   число  =  P  :  a  ×  b",
                 font=F_HEAD, bg=CARD_V, fg=ACCENT2).pack(anchor="w", pady=(8, 0))

        # Example
        ex = tk.Frame(p, bg=PANEL, padx=24, pady=18,
                      highlightbackground=BORDER, highlightthickness=1)
        ex.pack(fill="x", pady=8)

        # Task header — no M, use "СТАНОВИТЬ"
        t_row1 = tk.Frame(ex, bg=PANEL)
        t_row1.pack(anchor="w")
        tk.Label(t_row1, text="✏️  Задача.  Відстань між A і B — 120 км.  Це становить  ",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(side="left")
        fraction_widget(t_row1, 3, 4, PANEL, "small").pack(side="left", padx=6)
        tk.Label(t_row1, text="  відстані між A і C.  Яка відстань між A і C?",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(side="left")

        sol = tk.Frame(ex, bg=PANEL)
        sol.pack(anchor="w", padx=20, pady=10)
        for label, color, calc, explain in [
            ("Крок 1", ACCENT,  "120  :  3  =  40",  "Знаходимо одну четверту відстані A–C"),
            ("Крок 2", ACCENT2, "40   ×  4  =  160", "Знаходимо чотири четвертих = усю відстань"),
        ]:
            row = tk.Frame(sol, bg=CARD_V, padx=16, pady=8,
                           highlightbackground=BORDER, highlightthickness=1)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=label, font=F_STEP, bg=CARD_V, fg=color,
                     width=8, anchor="w").pack(side="left")
            tk.Label(row, text=calc, font=("Segoe UI", 22, "bold"),
                     bg=CARD_V, fg=color).pack(side="left", padx=16)
            tk.Label(row, text=f"({explain})", font=F_SMALL,
                     bg=CARD_V, fg=MUTED).pack(side="left")

        tk.Label(ex, text="Відповідь:  160 км",
                 font=F_HEAD, bg=PANEL, fg=ACCENT2).pack(anchor="w", padx=20, pady=(6, 0))

        # Visual road
        road_f = tk.Frame(ex, bg=PANEL)
        road_f.pack(anchor="w", padx=20, pady=8)
        tk.Label(road_f, text="Наочно:", font=F_SMALL, bg=PANEL, fg=MUTED).pack(anchor="w")
        road = tk.Frame(road_f, bg=PANEL)
        road.pack(anchor="w", pady=4)
        for i, (lbl, color) in enumerate([("40", ACCENT), ("40", ACCENT),
                                           ("40", ACCENT), ("40", ACCENT2)]):
            cell = tk.Frame(road, bg=color, width=100, height=50,
                            highlightbackground=BORDER, highlightthickness=1)
            cell.pack(side="left", padx=3)
            cell.pack_propagate(False)
            tk.Label(cell, text=f"{lbl} км", font=("Segoe UI", 13, "bold"),
                     bg=color, fg=WHITE).pack(expand=True)

        road_ann = tk.Frame(road_f, bg=PANEL)
        road_ann.pack(anchor="w", pady=2)
        tk.Label(road_ann, text="← A–B = 120 км  (становить  ",
                 font=F_SMALL, bg=PANEL, fg=MUTED).pack(side="left")
        fraction_widget(road_ann, 3, 4, PANEL, "small").pack(side="left")
        tk.Label(road_ann, text="  відстані A–C)        1 четверта = 40 км →",
                 font=F_SMALL, bg=PANEL, fg=MUTED).pack(side="left")

        # Comparison card — no text fractions
        cmp_f = tk.Frame(p, bg=CARD_Y, padx=22, pady=14,
                         highlightbackground=BORDER, highlightthickness=1)
        cmp_f.pack(fill="x", pady=7)
        tk.Label(cmp_f, text="⚡  Порівняй обидві формули",
                 font=F_SUB, bg=CARD_Y, fg=ORANGE).pack(anchor="w")

        for bg_c, fg_c, lbl_text, formula in [
            (CARD_G, GREEN,   "Дріб ВІД числа:",      "N  :  b  ×  a\n(ділимо на знаменник, множимо на чисельник)"),
            (CARD_V, ACCENT2, "Число якщо СТАНОВИТЬ:", "P  :  a  ×  b\n(ділимо на чисельник, множимо на знаменник)"),
        ]:
            r = tk.Frame(cmp_f, bg=bg_c, padx=16, pady=8,
                         highlightbackground=BORDER, highlightthickness=1)
            r.pack(fill="x", pady=5)
            tk.Label(r, text=lbl_text, font=F_BODYB, bg=bg_c, fg=fg_c,
                     width=24, anchor="w").pack(side="left")
            tk.Label(r, text=formula, font=F_BODY, bg=bg_c, fg=TEXT,
                     justify="left").pack(side="left", padx=10)
        tk.Label(cmp_f,
                 text="Підказка: крок 1 завжди ДІЛЕННЯ,  крок 2 завжди МНОЖЕННЯ.",
                 font=F_BODYB, bg=CARD_Y, fg=ORANGE).pack(anchor="w", pady=(8, 0))

    # ══════════════════════════════════════════════════════════════════════════
    # SHARED: numpad builder + score bar
    # ══════════════════════════════════════════════════════════════════════════
    def _build_numpad(self, parent, key_fn):
        np = tk.Frame(parent, bg=BG)
        for row_chars in [("7","8","9"),("4","5","6"),("1","2","3"),("C","0","⌫")]:
            rf = tk.Frame(np, bg=BG)
            rf.pack(pady=2)
            for ch in row_chars:
                if ch.isdigit():  bc, fc = BTN_NUM, TEXT
                elif ch == "C":   bc, fc = RED_LT,  RED
                else:             bc, fc = CARD_V,  ACCENT2
                b = tk.Button(rf, text=ch, font=F_NUM, width=4, height=1,
                              bg=bc, fg=fc, relief="flat", cursor="hand2",
                              command=lambda c=ch: key_fn(c))
                b.pack(side="left", padx=5)
                orig = bc
                b.bind("<Enter>", lambda e, x=b, o=orig: x.config(bg=_darken(o, 18)))
                b.bind("<Leave>", lambda e, x=b, o=orig: x.config(bg=o))
        return np

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER 1 — Fraction of number (2 steps)
    # ══════════════════════════════════════════════════════════════════════════
    def show_trainer_1(self):
        self.clear_main()
        self.mode = "trainer1"

        cf = self.current_frame

        # Score bar
        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.t1_score_lbl = tk.Label(sbar,
            text=f"Правильно: {self.t1_score}  /  Завдань: {self.t1_attempts}",
            font=F_SCORE, bg=PANEL, fg=GREEN)
        self.t1_score_lbl.pack(side="left", padx=30)

        # Formula reminder in score bar
        frm = tk.Frame(sbar, bg=PANEL)
        frm.pack(side="right", padx=20)
        tk.Label(frm, text="Формула:  N : b × a",
                 font=("Segoe UI", 14, "bold"), bg=PANEL, fg=GREEN).pack()

        p = self._scroll_page(py=10)
        center = tk.Frame(p, bg=BG)
        center.pack(expand=True, fill="both")

        # ── 2-step banner ─────────────────────────────────────────────────
        banner = tk.Frame(center, bg=CARD_G, padx=20, pady=8,
                          highlightbackground=GREEN, highlightthickness=2)
        banner.pack(fill="x", padx=40, pady=(4, 2))
        tk.Label(banner,
                 text="📋  Відповідай У ДВА КРОКИ:   "
                      "Крок 1 → введи  N : b  і натисни «Перевірити»   "
                      "Крок 2 → введи  результат × a  і натисни «Перевірити»",
                 font=("Segoe UI", 14, "bold"), bg=CARD_G, fg=GREEN,
                 justify="center").pack()

        # ── Task header ───────────────────────────────────────────────────
        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=28, pady=10)
        task_f.pack(pady=(8, 4))

        task_row = tk.Frame(task_f, bg=PANEL)
        task_row.pack()
        tk.Label(task_row, text="Знайди  ",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack(side="left")
        self.t1_frac_frame = tk.Frame(task_row, bg=PANEL)
        self.t1_frac_frame.pack(side="left", padx=6)
        tk.Label(task_row, text="  від числа  ",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack(side="left")
        self.t1_num_lbl = tk.Label(task_row, text="",
                                    font=("Segoe UI", 36, "bold"),
                                    bg=PANEL, fg=ACCENT)
        self.t1_num_lbl.pack(side="left")

        # ── Step indicator ────────────────────────────────────────────────
        steps_row = tk.Frame(center, bg=BG)
        steps_row.pack(pady=4)

        self.t1_step_boxes = []
        for i, (label, desc) in enumerate([
            ("Крок 1", "N  :  b  = ?"),
            ("Крок 2", "результат  ×  a  = ?"),
        ]):
            box = tk.Frame(steps_row, bg=BTN_NUM, padx=18, pady=8,
                           highlightbackground=BORDER, highlightthickness=1,
                           width=280)
            box.pack(side="left", padx=10)
            box.pack_propagate(False)
            tk.Label(box, text=label, font=F_STEP,
                     bg=BTN_NUM, fg=MUTED).pack()
            lbl = tk.Label(box, text=desc, font=F_STEP_V,
                           bg=BTN_NUM, fg=MUTED)
            lbl.pack()
            self.t1_step_boxes.append((box, lbl))

        # Step 1 result display (shown after step 1 done)
        self.t1_step1_result_lbl = tk.Label(center, text="",
                                             font=("Segoe UI", 16, "bold"),
                                             bg=BG, fg=ACCENT)
        self.t1_step1_result_lbl.pack(pady=2)

        # ── Input ─────────────────────────────────────────────────────────
        self.t1_step_lbl = tk.Label(center, text="", font=F_SUB,
                                     bg=BG, fg=ACCENT)
        self.t1_step_lbl.pack(pady=2)

        inp_f = tk.Frame(center, bg=BTN_NUM,
                         highlightbackground=ACCENT, highlightthickness=2,
                         padx=14, pady=4)
        inp_f.pack(pady=2)
        tk.Label(inp_f, text="Відповідь:", font=F_BODYB,
                 bg=BTN_NUM, fg=MUTED).pack(side="left")
        self.t1_inp_lbl = tk.Label(inp_f, text="",
                                    font=("Segoe UI", 36, "bold"),
                                    bg=BTN_NUM, fg=ACCENT, width=5)
        self.t1_inp_lbl.pack(side="left", padx=10)

        self.t1_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                     bg=BG, fg=ORANGE,
                                     wraplength=700, justify="center")
        self.t1_feed_lbl.pack(pady=2)

        # Numpad
        self._build_numpad(center, self._t1_key).pack(pady=4)

        act = tk.Frame(center, bg=BG)
        act.pack(pady=4)
        self.t1_check_btn = mkbtn(act, "✔  Перевірити", self._t1_check,
                                   bg=GREEN, w=14, h=1)
        self.t1_check_btn.pack(side="left", padx=10)
        mkbtn(act, "▶  Наступне", self._t1_new,
              bg=ACCENT, w=12, h=1).pack(side="left", padx=10)

        self._t1_new()

    def _t1_highlight_step(self, step):
        """Highlight active step box, dim the other."""
        for i, (box, lbl) in enumerate(self.t1_step_boxes):
            if i + 1 == step:
                box.config(bg=CARD_G, highlightbackground=GREEN,
                           highlightthickness=2)
                lbl.config(bg=CARD_G, fg=GREEN)
                box.winfo_children()[0].config(bg=CARD_G, fg=GREEN)
            else:
                box.config(bg=BTN_NUM, highlightbackground=BORDER,
                           highlightthickness=1)
                lbl.config(bg=BTN_NUM, fg=MUTED)
                box.winfo_children()[0].config(bg=BTN_NUM, fg=MUTED)

    def _t1_new(self):
        self.t1_a, self.t1_b, self.t1_N, self.t1_ans = generate_task_frac_of_num()
        self.t1_step = 1
        self.t1_input = ""
        self.t1_attempts += 1

        # Rebuild fraction widget
        for w in self.t1_frac_frame.winfo_children():
            w.destroy()
        fraction_widget(self.t1_frac_frame, self.t1_a, self.t1_b,
                        PANEL, "big").pack()

        if self.t1_num_lbl:    self.t1_num_lbl.config(text=str(self.t1_N), fg=ACCENT)
        if self.t1_inp_lbl:    self.t1_inp_lbl.config(text="", fg=ACCENT)
        if self.t1_feed_lbl:   self.t1_feed_lbl.config(text="")
        if self.t1_step1_result_lbl: self.t1_step1_result_lbl.config(text="")
        if self.t1_check_btn:  self.t1_check_btn.config(state="normal", bg=GREEN)
        if self.t1_score_lbl:
            self.t1_score_lbl.config(
                text=f"Правильно: {self.t1_score}  /  Завдань: {self.t1_attempts}")
        self._t1_set_step_label()
        self._t1_highlight_step(1)

    def _t1_set_step_label(self):
        if self.t1_step == 1:
            if self.t1_step_lbl:
                self.t1_step_lbl.config(
                    text=f"Крок 1:   {self.t1_N}  :  {self.t1_b}  =  ?",
                    fg=ACCENT)
        else:
            partial = self.t1_step1_val
            if self.t1_step_lbl:
                self.t1_step_lbl.config(
                    text=f"Крок 2:   {partial}  ×  {self.t1_a}  =  ?",
                    fg=GREEN)

    def _t1_key(self, ch):
        if ch.isdigit():
            if len(self.t1_input) < 6: self.t1_input += ch
        elif ch == "⌫": self.t1_input = self.t1_input[:-1]
        elif ch == "C":  self.t1_input = ""
        if self.t1_inp_lbl: self.t1_inp_lbl.config(text=self.t1_input)

    def _t1_check(self):
        if not self.t1_input.strip():
            if self.t1_feed_lbl:
                self.t1_feed_lbl.config(text="⚠️  Введіть відповідь!", fg=ORANGE)
            return
        val = int(self.t1_input)
        self.t1_input = ""
        if self.t1_inp_lbl: self.t1_inp_lbl.config(text="")

        if self.t1_step == 1:
            expected = self.t1_N // self.t1_b
            if val == expected:
                self.t1_step1_val = val
                self.t1_step = 2
                if self.t1_step1_result_lbl:
                    self.t1_step1_result_lbl.config(
                        text=f"✅  Крок 1:   {self.t1_N} : {self.t1_b} = {val}   (одна {self.t1_b}-а частина)",
                        fg=GREEN)
                if self.t1_feed_lbl:
                    self.t1_feed_lbl.config(
                        text=f"Правильно!  Тепер крок 2 — помнож {val} на {self.t1_a}",
                        fg=GREEN)
                self._t1_set_step_label()
                self._t1_highlight_step(2)
            else:
                if self.t1_feed_lbl:
                    self.t1_feed_lbl.config(
                        text=f"❌  {self.t1_N} : {self.t1_b} ≠ {val}.   Спробуй ще!",
                        fg=RED)
        else:
            # Step 2
            expected = self.t1_step1_val * self.t1_a
            if val == expected:
                self.t1_score += 1
                if self.t1_feed_lbl:
                    self.t1_feed_lbl.config(
                        text=f"🎉  Чудово!   {self.t1_a}/{self.t1_b}  від  {self.t1_N}  =  "
                             f"{self.t1_N} : {self.t1_b} × {self.t1_a} = "
                             f"{self.t1_step1_val} × {self.t1_a} = {expected}",
                        fg=GREEN)
                if self.t1_inp_lbl: self.t1_inp_lbl.config(fg=GREEN)
                if self.t1_check_btn: self.t1_check_btn.config(state="disabled", bg=BTN_NUM)
                self._t1_highlight_step(2)
            else:
                if self.t1_feed_lbl:
                    self.t1_feed_lbl.config(
                        text=f"❌  {self.t1_step1_val} × {self.t1_a} ≠ {val}.   Спробуй ще!",
                        fg=RED)

        if self.t1_score_lbl:
            self.t1_score_lbl.config(
                text=f"Правильно: {self.t1_score}  /  Завдань: {self.t1_attempts}")

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER 2 — Number from fraction (2 steps)
    # ══════════════════════════════════════════════════════════════════════════
    def show_trainer_2(self):
        self.clear_main()
        self.mode = "trainer2"

        cf = self.current_frame

        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.t2_score_lbl = tk.Label(sbar,
            text=f"Правильно: {self.t2_score}  /  Завдань: {self.t2_attempts}",
            font=F_SCORE, bg=PANEL, fg=GREEN)
        self.t2_score_lbl.pack(side="left", padx=30)
        frm = tk.Frame(sbar, bg=PANEL)
        frm.pack(side="right", padx=20)
        tk.Label(frm, text="Формула:  P : a × b",
                 font=("Segoe UI", 14, "bold"), bg=PANEL, fg=ACCENT2).pack()

        p = self._scroll_page(py=10)
        center = tk.Frame(p, bg=BG)
        center.pack(expand=True, fill="both")

        # ── 2-step banner ─────────────────────────────────────────────────
        banner2 = tk.Frame(center, bg=CARD_V, padx=20, pady=8,
                           highlightbackground=ACCENT2, highlightthickness=2)
        banner2.pack(fill="x", padx=40, pady=(4, 2))
        tk.Label(banner2,
                 text="📋  Відповідай У ДВА КРОКИ:   "
                      "Крок 1 → введи  P : a  і натисни «Перевірити»   "
                      "Крок 2 → введи  результат × b  і натисни «Перевірити»",
                 font=("Segoe UI", 14, "bold"), bg=CARD_V, fg=ACCENT2,
                 justify="center").pack()

        # Task header
        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=28, pady=10)
        task_f.pack(pady=(8, 4))

        self.t2_task_lbl = tk.Label(task_f, text="",
                                     font=F_SUB, bg=PANEL, fg=TEXT,
                                     justify="center")
        self.t2_task_lbl.pack()
        tk.Label(task_f, text="(Натисни «Перевірити» після кожного кроку)",
                 font=F_SMALL, bg=PANEL, fg=MUTED).pack()

        self.t2_frac_row = tk.Frame(task_f, bg=PANEL)
        self.t2_frac_row.pack(pady=4)

        # Step boxes
        steps_row = tk.Frame(center, bg=BG)
        steps_row.pack(pady=4)
        self.t2_step_boxes = []
        for label, desc in [
            ("Крок 1", "P  :  a  = ?"),
            ("Крок 2", "результат  ×  b  = ?"),
        ]:
            box = tk.Frame(steps_row, bg=BTN_NUM, padx=18, pady=8,
                           highlightbackground=BORDER, highlightthickness=1,
                           width=300)
            box.pack(side="left", padx=10)
            box.pack_propagate(False)
            tk.Label(box, text=label, font=F_STEP, bg=BTN_NUM, fg=MUTED).pack()
            lbl = tk.Label(box, text=desc, font=F_STEP_V, bg=BTN_NUM, fg=MUTED)
            lbl.pack()
            self.t2_step_boxes.append((box, lbl))

        self.t2_step1_result_lbl = tk.Label(center, text="",
                                             font=("Segoe UI", 16, "bold"),
                                             bg=BG, fg=ACCENT2)
        self.t2_step1_result_lbl.pack(pady=2)

        self.t2_step_lbl = tk.Label(center, text="", font=F_SUB,
                                     bg=BG, fg=ACCENT2)
        self.t2_step_lbl.pack(pady=2)

        inp_f = tk.Frame(center, bg=BTN_NUM,
                         highlightbackground=ACCENT2, highlightthickness=2,
                         padx=14, pady=4)
        inp_f.pack(pady=2)
        tk.Label(inp_f, text="Число  =", font=F_BODYB,
                 bg=BTN_NUM, fg=MUTED).pack(side="left")
        self.t2_inp_lbl = tk.Label(inp_f, text="",
                                    font=("Segoe UI", 36, "bold"),
                                    bg=BTN_NUM, fg=ACCENT2, width=5)
        self.t2_inp_lbl.pack(side="left", padx=10)

        self.t2_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                     bg=BG, fg=ORANGE,
                                     wraplength=700, justify="center")
        self.t2_feed_lbl.pack(pady=2)

        self._build_numpad(center, self._t2_key).pack(pady=4)

        act = tk.Frame(center, bg=BG)
        act.pack(pady=4)
        self.t2_check_btn = mkbtn(act, "✔  Перевірити", self._t2_check,
                                   bg=GREEN, w=14, h=1)
        self.t2_check_btn.pack(side="left", padx=10)
        mkbtn(act, "▶  Наступне", self._t2_new,
              bg=ACCENT2, w=12, h=1).pack(side="left", padx=10)

        self._t2_new()

    def _t2_highlight_step(self, step):
        for i, (box, lbl) in enumerate(self.t2_step_boxes):
            if i + 1 == step:
                box.config(bg=CARD_V, highlightbackground=ACCENT2,
                           highlightthickness=2)
                lbl.config(bg=CARD_V, fg=ACCENT2)
                box.winfo_children()[0].config(bg=CARD_V, fg=ACCENT2)
            else:
                box.config(bg=BTN_NUM, highlightbackground=BORDER,
                           highlightthickness=1)
                lbl.config(bg=BTN_NUM, fg=MUTED)
                box.winfo_children()[0].config(bg=BTN_NUM, fg=MUTED)

    def _t2_new(self):
        self.t2_a, self.t2_b, self.t2_M, self.t2_P = generate_task_num_from_frac()
        self.t2_step = 1
        self.t2_input = ""
        self.t2_attempts += 1

        # Rebuild task display: "[frac] від числа СТАНОВИТЬ [P]"
        if hasattr(self, 't2_frac_row') and self.t2_frac_row:
            for w in self.t2_frac_row.winfo_children():
                w.destroy()
            fraction_widget(self.t2_frac_row, self.t2_a, self.t2_b,
                            PANEL, "big").pack(side="left", padx=(0, 10))
            tk.Label(self.t2_frac_row, text="від числа  СТАНОВИТЬ",
                     font=F_SUB, bg=PANEL, fg=MUTED).pack(side="left", padx=(0, 10))
            tk.Label(self.t2_frac_row, text=str(self.t2_P),
                     font=("Segoe UI", 48, "bold"), bg=PANEL, fg=ACCENT2).pack(side="left")

        if hasattr(self, 't2_task_lbl') and self.t2_task_lbl:
            self.t2_task_lbl.config(text="Знайди число, якщо відомо, що:")

        if self.t2_inp_lbl:   self.t2_inp_lbl.config(text="", fg=ACCENT2)
        if self.t2_feed_lbl:  self.t2_feed_lbl.config(text="")
        if self.t2_step1_result_lbl: self.t2_step1_result_lbl.config(text="")
        if self.t2_check_btn: self.t2_check_btn.config(state="normal", bg=GREEN)
        if self.t2_score_lbl:
            self.t2_score_lbl.config(
                text=f"Правильно: {self.t2_score}  /  Завдань: {self.t2_attempts}")
        self._t2_set_step_label()
        self._t2_highlight_step(1)

    def _t2_set_step_label(self):
        if self.t2_step == 1:
            if self.t2_step_lbl:
                self.t2_step_lbl.config(
                    text=f"Крок 1:   {self.t2_P}  :  {self.t2_a}  =  ?",
                    fg=ACCENT2)
        else:
            partial = self.t2_step1_val
            if self.t2_step_lbl:
                self.t2_step_lbl.config(
                    text=f"Крок 2:   {partial}  ×  {self.t2_b}  =  ?",
                    fg=ACCENT)

    def _t2_key(self, ch):
        if ch.isdigit():
            if len(self.t2_input) < 6: self.t2_input += ch
        elif ch == "⌫": self.t2_input = self.t2_input[:-1]
        elif ch == "C":  self.t2_input = ""
        if self.t2_inp_lbl: self.t2_inp_lbl.config(text=self.t2_input)

    def _t2_check(self):
        if not self.t2_input.strip():
            if self.t2_feed_lbl:
                self.t2_feed_lbl.config(text="⚠️  Введіть відповідь!", fg=ORANGE)
            return
        val = int(self.t2_input)
        self.t2_input = ""
        if self.t2_inp_lbl: self.t2_inp_lbl.config(text="")

        if self.t2_step == 1:
            expected = self.t2_P // self.t2_a
            if val == expected:
                self.t2_step1_val = val
                self.t2_step = 2
                if self.t2_step1_result_lbl:
                    self.t2_step1_result_lbl.config(
                        text=f"✅  Крок 1:   {self.t2_P} : {self.t2_a} = {val}   (знайшли 1/{self.t2_b} від M)",
                        fg=GREEN)
                if self.t2_feed_lbl:
                    self.t2_feed_lbl.config(
                        text=f"Правильно!  Тепер крок 2 — помнож {val} на {self.t2_b}",
                        fg=GREEN)
                self._t2_set_step_label()
                self._t2_highlight_step(2)
            else:
                if self.t2_feed_lbl:
                    self.t2_feed_lbl.config(
                        text=f"❌  {self.t2_P} : {self.t2_a} ≠ {val}.   Спробуй ще!",
                        fg=RED)
        else:
            expected = self.t2_step1_val * self.t2_b
            if val == expected:
                self.t2_score += 1
                if self.t2_feed_lbl:
                    self.t2_feed_lbl.config(
                        text=f"🎉  Чудово!   M = {self.t2_P} : {self.t2_a} × {self.t2_b} = "
                             f"{self.t2_step1_val} × {self.t2_b} = {expected}",
                        fg=GREEN)
                if self.t2_inp_lbl: self.t2_inp_lbl.config(fg=GREEN)
                if self.t2_check_btn: self.t2_check_btn.config(state="disabled", bg=BTN_NUM)
                self._t2_highlight_step(2)
            else:
                if self.t2_feed_lbl:
                    self.t2_feed_lbl.config(
                        text=f"❌  {self.t2_step1_val} × {self.t2_b} ≠ {val}.   Спробуй ще!",
                        fg=RED)

        if self.t2_score_lbl:
            self.t2_score_lbl.config(
                text=f"Правильно: {self.t2_score}  /  Завдань: {self.t2_attempts}")

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER 3 — Free practice: random type, direct single answer, no hints
    # ══════════════════════════════════════════════════════════════════════════
    def show_trainer_3(self):
        self.clear_main()
        self.mode = "trainer3"
        PINK    = "#9d174d"
        PINK_LT = "#fce7f3"

        cf = self.current_frame

        # Score bar
        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.t3_score_lbl = tk.Label(sbar,
            text=f"Правильно: {self.t3_score}  /  Завдань: {self.t3_attempts}",
            font=F_SCORE, bg=PANEL, fg=GREEN)
        self.t3_score_lbl.pack(side="left", padx=30)
        tk.Label(sbar,
                 text="🏆  Вільна практика — завдання змішані, вводь відповідь одразу",
                 font=("Segoe UI", 14, "bold"), bg=PANEL, fg=PINK).pack(
            side="left", padx=10)

        p = self._scroll_page(py=10)
        center = tk.Frame(p, bg=BG)
        center.pack(expand=True, fill="both")

        # Task card
        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=32, pady=12)
        task_f.pack(pady=(10, 4))

        self.t3_task_lbl = tk.Label(task_f, text="",
                                     font=F_SUB, bg=PANEL, fg=TEXT,
                                     justify="center")
        self.t3_task_lbl.pack()

        self.t3_frac_row = tk.Frame(task_f, bg=PANEL)
        self.t3_frac_row.pack(pady=4)

        # Badge: shown after correct answer revealing task type
        self.t3_type_badge = tk.Label(center, text="", font=F_SMALL,
                                       bg=BG, fg=MUTED)
        self.t3_type_badge.pack(pady=2)

        # Input display
        inp_f = tk.Frame(center, bg=BTN_NUM,
                         highlightbackground=PINK, highlightthickness=2,
                         padx=14, pady=4)
        inp_f.pack(pady=4)
        tk.Label(inp_f, text="Відповідь:", font=F_BODYB,
                 bg=BTN_NUM, fg=MUTED).pack(side="left")
        self.t3_inp_lbl = tk.Label(inp_f, text="",
                                    font=("Segoe UI", 36, "bold"),
                                    bg=BTN_NUM, fg=PINK, width=5)
        self.t3_inp_lbl.pack(side="left", padx=10)

        self.t3_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                     bg=BG, fg=ORANGE,
                                     wraplength=700, justify="center")
        self.t3_feed_lbl.pack(pady=2)

        # Numpad with pink accent
        np = tk.Frame(center, bg=BG)
        for row_chars in [("7","8","9"),("4","5","6"),("1","2","3"),("C","0","⌫")]:
            rf = tk.Frame(np, bg=BG)
            rf.pack(pady=2)
            for ch in row_chars:
                if ch.isdigit():  bc, fc = BTN_NUM, TEXT
                elif ch == "C":   bc, fc = RED_LT,  RED
                else:             bc, fc = PINK_LT, PINK
                b = tk.Button(rf, text=ch, font=F_NUM, width=4, height=1,
                              bg=bc, fg=fc, relief="flat", cursor="hand2",
                              command=lambda c=ch: self._t3_key(c))
                b.pack(side="left", padx=5)
                orig = bc
                b.bind("<Enter>", lambda e, x=b, o=orig: x.config(bg=_darken(o, 18)))
                b.bind("<Leave>", lambda e, x=b, o=orig: x.config(bg=o))
        np.pack(pady=4)

        act = tk.Frame(center, bg=BG)
        act.pack(pady=4)
        self.t3_check_btn = mkbtn(act, "✔  Перевірити", self._t3_check,
                                   bg=GREEN, w=14, h=1)
        self.t3_check_btn.pack(side="left", padx=10)
        mkbtn(act, "▶  Наступне", self._t3_new,
              bg=PINK, w=12, h=1).pack(side="left", padx=10)

        self._t3_new()

    def _t3_new(self):
        self.t3_type  = random.choice(["frac", "num"])
        self.t3_input = ""

        if self.t3_type == "frac":
            a, b, N, ans = generate_task_frac_of_num()
            self.t3_a, self.t3_b, self.t3_N, self.t3_ans = a, b, N, ans
        else:
            a, b, M, P = generate_task_num_from_frac()
            self.t3_a, self.t3_b = a, b
            self.t3_N   = P   # given value
            self.t3_ans = M   # find M

        self.t3_attempts += 1

        # Rebuild task label (no type hint shown)
        if self.t3_task_lbl:
            if self.t3_type == "frac":
                self.t3_task_lbl.config(text="Знайди:")
            else:
                self.t3_task_lbl.config(text="Знайди число, якщо відомо, що:")

        # Rebuild fraction display row
        for w in self.t3_frac_row.winfo_children():
            w.destroy()
        if self.t3_type == "frac":
            fraction_widget(self.t3_frac_row, self.t3_a, self.t3_b,
                            PANEL, "big").pack(side="left", padx=10)
            tk.Label(self.t3_frac_row, text=f"  від  {self.t3_N}",
                     font=("Segoe UI", 48, "bold"),
                     bg=PANEL, fg=ACCENT).pack(side="left")
        else:
            fraction_widget(self.t3_frac_row, self.t3_a, self.t3_b,
                            PANEL, "big").pack(side="left", padx=10)
            tk.Label(self.t3_frac_row,
                     text="від числа  СТАНОВИТЬ",
                     font=F_SUB, bg=PANEL, fg=MUTED).pack(side="left", padx=(0, 10))
            tk.Label(self.t3_frac_row,
                     text=str(self.t3_N),
                     font=("Segoe UI", 48, "bold"),
                     bg=PANEL, fg=ACCENT2).pack(side="left")

        if self.t3_type_badge:  self.t3_type_badge.config(text="")
        if self.t3_inp_lbl:     self.t3_inp_lbl.config(text="", fg="#9d174d")
        if self.t3_feed_lbl:    self.t3_feed_lbl.config(text="")
        if self.t3_check_btn:   self.t3_check_btn.config(state="normal", bg=GREEN)
        if self.t3_score_lbl:
            self.t3_score_lbl.config(
                text=f"Правильно: {self.t3_score}  /  Завдань: {self.t3_attempts}")

    def _t3_key(self, ch):
        if ch.isdigit():
            if len(self.t3_input) < 6: self.t3_input += ch
        elif ch == "⌫": self.t3_input = self.t3_input[:-1]
        elif ch == "C":  self.t3_input = ""
        if self.t3_inp_lbl: self.t3_inp_lbl.config(text=self.t3_input)

    def _t3_check(self):
        if not self.t3_input.strip():
            if self.t3_feed_lbl:
                self.t3_feed_lbl.config(text="⚠️  Введіть відповідь!", fg=ORANGE)
            return
        val = int(self.t3_input)
        self.t3_input = ""
        if self.t3_inp_lbl: self.t3_inp_lbl.config(text="")

        a, b, N, ans = self.t3_a, self.t3_b, self.t3_N, self.t3_ans

        if val == ans:
            self.t3_score += 1
            # Now reveal type + solution
            if self.t3_type == "frac":
                solution = f"{N} : {b} × {a} = {N//b} × {a} = {ans}"
                badge = "📘 Це було: знаходження дробу від числа  (N : b × a)"
            else:
                solution = f"{N} : {a} × {b} = {N//a} × {b} = {ans}"
                badge = "📗 Це було: знаходження числа за дробом  (P : a × b)"
            if self.t3_feed_lbl:
                self.t3_feed_lbl.config(
                    text=f"🎉  Правильно!   Розв'язок:  {solution}", fg=GREEN)
            if self.t3_type_badge:
                self.t3_type_badge.config(text=badge, fg=MUTED)
            if self.t3_inp_lbl:   self.t3_inp_lbl.config(fg=GREEN)
            if self.t3_check_btn: self.t3_check_btn.config(state="disabled", bg=BTN_NUM)
        else:
            # On wrong: reveal the two-step path as hint
            if self.t3_type == "frac":
                hint = f"Підказка:  {N} : {b} = {N//b},   потім × {a} = {ans}"
            else:
                hint = f"Підказка:  {N} : {a} = {N//a},   потім × {b} = {ans}"
            if self.t3_feed_lbl:
                self.t3_feed_lbl.config(
                    text=f"❌  {val} — не правильно.   {hint}", fg=RED)

        if self.t3_score_lbl:
            self.t3_score_lbl.config(
                text=f"Правильно: {self.t3_score}  /  Завдань: {self.t3_attempts}")


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
