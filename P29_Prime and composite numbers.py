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
CARD_R    = "#fee2e2"
TEAL      = "#0f766e"
TEAL_LT   = "#ccfbf1"

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
F_GRID   = ("Segoe UI", 15, "bold")


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


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def get_divisors(n):
    d = set()
    for i in range(1, int(math.isqrt(n)) + 1):
        if n % i == 0:
            d.add(i)
            d.add(n // i)
    return sorted(d)


def smallest_factor(n):
    """Return smallest prime factor of n (>1)."""
    if n % 2 == 0:
        return 2
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return i
    return n   # n is prime


# ══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("§ 29. Прості і складені числа")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()
        self.current_frame = None
        self.mode = None

        # ── Trainer 1: Prime or Composite? ───────────────────────────────
        self.t1_score    = 0
        self.t1_attempts = 0
        self.t1_number   = 0
        self.t1_num_lbl  = None
        self.t1_feed_lbl = None
        self.t1_score_lbl = None
        self.t1_answered = False

        # ── Trainer 2: Find all divisors ─────────────────────────────────
        self.t2_score     = 0
        self.t2_attempts  = 0
        self.t2_number    = 0
        self.t2_correct   = []
        self.t2_found     = []
        self.t2_remaining = []
        self.t2_input     = ""
        self.t2_done      = False
        self.t2_num_lbl   = None
        self.t2_found_lbl = None
        self.t2_rem_lbl   = None
        self.t2_inp_lbl   = None
        self.t2_feed_lbl  = None
        self.t2_score_lbl = None
        self.t2_check_btn = None
        self.t2_next_btn  = None

        # ── Trainer 3: Sieve of Eratosthenes ─────────────────────────────
        self.t3_score    = 0
        self.t3_attempts = 0
        self.t3_btns     = {}     # n -> Button
        self.t3_marked   = set()  # numbers user crossed out
        self.t3_primes_in_range = set()
        self.t3_score_lbl = None
        self.t3_count_lbl = None
        self.t3_feed_lbl  = None
        self.t3_check_btn = None

        self._build_chrome()
        self.show_main_menu()

    # ── Chrome ────────────────────────────────────────────────────────────────
    def _build_chrome(self):
        hdr = tk.Frame(self, bg=HDR_BG, height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="§ 29.   Прості і складені числа",
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
            ("📖  Теорія",                 self.show_theory),
            ("🎯  Просте чи складене?",    self.show_trainer_1),
            ("🔢  Знайди дільники",        self.show_trainer_2),
            ("🏺  Решето Ератосфена",      self.show_trainer_3),
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

        tk.Label(center, text="Прості і складені числа",
                 font=("Segoe UI", 48, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 4))
        tk.Label(center, text="§ 29",
                 font=("Segoe UI", 26), bg=BG, fg=ACCENT).pack(pady=(0, 30))

        cards = [
            ("📖", "Теорія",              CARD_B, ACCENT,  self.show_theory),
            ("🎯", "Просте чи\nскладене?", CARD_G, GREEN,   self.show_trainer_1),
            ("🔢", "Знайди\nдільники",     CARD_V, ACCENT2, self.show_trainer_2),
            ("🏺", "Решето\nЕратосфена",   CARD_Y, ORANGE,  self.show_trainer_3),
        ]
        row = tk.Frame(center, bg=BG)
        row.pack()
        for icon, title, bg_c, fg_c, cmd in cards:
            c = tk.Frame(row, bg=bg_c, width=210, height=200,
                         highlightbackground=BORDER, highlightthickness=2)
            c.pack(side="left", padx=14)
            c.pack_propagate(False)
            tk.Label(c, text=icon, font=("Segoe UI", 38),
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

        tk.Label(p, text="Прості і складені числа",
                 font=F_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        hline(p, ACCENT)

        theory_card(p, "📌  Просте число",
                    "Натуральне число називають простим, якщо воно має рівно ДВА дільники:\n"
                    "число 1  і  саме це число.\n\n"
                    "Приклади простих чисел:  2,  3,  5,  7,  11,  13,  17,  19,  23,  29,  31 …\n\n"
                    "Дільники числа 11:  1  і  11  (тільки два)  →  11 є простим.",
                    CARD_B, ACCENT)

        theory_card(p, "📌  Складене число",
                    "Натуральне число називають складеним, якщо воно має БІЛЬШЕ ніж два дільники.\n\n"
                    "Приклади:\n"
                    "   Дільники числа 8:   1, 2, 4, 8  (чотири дільники)  →  8 складене\n"
                    "   Дільники числа 18:  1, 2, 3, 6, 9, 18  (шість дільників)  →  18 складене\n\n"
                    "Якщо число має хоча б ОДИН дільник, відмінний від 1 і від себе — воно складене.",
                    CARD_R, RED)

        theory_card(p, "⚠️  Особливий випадок: число 1",
                    "Число 1 має лише ОДИН дільник — саме себе.\n"
                    "Тому 1 — НЕ є простим і НЕ є складеним числом.\n"
                    "Це особливе число, яке стоїть окремо.",
                    CARD_Y, ORANGE)

        theory_card(p, "⚡  Важливі факти про прості числа",
                    "• Найменше просте число — 2.\n"
                    "• Число 2 — єдине ПАРНЕ просте число. Усі інші прості числа — непарні.\n"
                    "• Простих чисел безліч: скільки б великого простого числа ми не взяли,\n"
                    "  завжди знайдеться ще більше.\n"
                    "• Будь-яке складене число можна розкласти на два множники, кожний > 1.\n"
                    "  Наприклад:  10 345  =  5  ×  2069",
                    CARD_G, GREEN)

        # ── Visual: numbers 1–30 coloured by type ────────────────────────
        vis_f = tk.Frame(p, bg=PANEL, padx=22, pady=16,
                         highlightbackground=BORDER, highlightthickness=1)
        vis_f.pack(fill="x", pady=8)
        tk.Label(vis_f, text="🔢  Числа від 1 до 50: класифікація",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(anchor="w", pady=(0, 10))

        legend = tk.Frame(vis_f, bg=PANEL)
        legend.pack(anchor="w", pady=(0, 8))
        for color, label in [
            (CARD_B,  "Просте число"),
            (CARD_R,  "Складене число"),
            (CARD_Y,  "Число 1 (особливе)"),
        ]:
            box = tk.Frame(legend, bg=color, width=22, height=22,
                           highlightbackground=BORDER, highlightthickness=1)
            box.pack(side="left", padx=(0, 4))
            tk.Label(legend, text=label, font=F_SMALL, bg=PANEL, fg=MUTED).pack(
                side="left", padx=(0, 18))

        grid_f = tk.Frame(vis_f, bg=PANEL)
        grid_f.pack(anchor="w")
        for i, n in enumerate(range(1, 51)):
            if n == 1:
                bg_c, fg_c = CARD_Y, ORANGE
            elif is_prime(n):
                bg_c, fg_c = CARD_B, ACCENT
            else:
                bg_c, fg_c = CARD_R, RED
            cell = tk.Frame(grid_f, bg=bg_c, width=70, height=56,
                            highlightbackground=BORDER, highlightthickness=1)
            cell.grid(row=i // 10, column=i % 10, padx=3, pady=3)
            cell.pack_propagate(False)
            tk.Label(cell, text=str(n), font=F_GRID,
                     bg=bg_c, fg=fg_c).pack(expand=True)

        # ── Task example ──────────────────────────────────────────────────
        theory_card(p, "✏️  Задача.  Просте чи складене число 10 345?",
                    "Розв'язання. За ознакою подільності на 5:\n"
                    "   остання цифра числа 10 345 — це 5.\n"
                    "   Отже, воно ділиться на 5.\n\n"
                    "5 ≠ 1  і  5 ≠ 10 345  →  є дільник, відмінний від 1 і від числа.\n\n"
                    "Відповідь:  10 345 — складене число  (10 345 = 5 × 2069).",
                    "#fef9c3", ORANGE)

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER 1 — Prime or Composite?
    # ══════════════════════════════════════════════════════════════════════════
    def show_trainer_1(self):
        self.clear_main()
        self.mode = "trainer1"
        self.t1_answered = False

        cf = self.current_frame

        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.t1_score_lbl = tk.Label(sbar,
            text=self._t1_score_text(), font=F_SCORE, bg=PANEL, fg=GREEN)
        self.t1_score_lbl.pack(side="left", padx=30)
        tk.Label(sbar, text="Просте чи складене число?",
                 font=("Segoe UI", 15, "bold"), bg=PANEL, fg=MUTED).pack(
            side="left", padx=10)

        center = tk.Frame(cf, bg=BG)
        center.pack(expand=True)

        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=30, pady=12)
        task_f.pack(pady=(16, 6))
        tk.Label(task_f, text="Визнач тип числа:",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack()
        tk.Label(task_f, text="(Натисни правильну кнопку)",
                 font=F_SMALL, bg=PANEL, fg=MUTED).pack()

        # Big number display
        num_f = tk.Frame(center, bg=PANEL,
                         highlightbackground=BORDER, highlightthickness=2,
                         padx=30, pady=4)
        num_f.pack(pady=6)
        self.t1_num_lbl = tk.Label(num_f, text="", font=F_BIG,
                                    bg=PANEL, fg=ACCENT)
        self.t1_num_lbl.pack()

        # Two big answer buttons
        btns_f = tk.Frame(center, bg=BG)
        btns_f.pack(pady=16)

        self.t1_prime_btn = tk.Button(
            btns_f, text="🔵  ПРОСТЕ",
            font=("Segoe UI", 28, "bold"),
            width=12, height=2,
            bg=CARD_B, fg=ACCENT,
            relief="flat", cursor="hand2",
            command=lambda: self._t1_answer("prime"))
        self.t1_prime_btn.pack(side="left", padx=20)

        self.t1_comp_btn = tk.Button(
            btns_f, text="🔴  СКЛАДЕНЕ",
            font=("Segoe UI", 28, "bold"),
            width=12, height=2,
            bg=CARD_R, fg=RED,
            relief="flat", cursor="hand2",
            command=lambda: self._t1_answer("composite"))
        self.t1_comp_btn.pack(side="left", padx=20)

        # Feedback
        self.t1_feed_lbl = tk.Label(center, text="",
                                     font=F_FEED, bg=BG, fg=ORANGE,
                                     wraplength=700, justify="center")
        self.t1_feed_lbl.pack(pady=8)

        mkbtn(center, "▶  Наступне число", self._t1_new,
              bg=ACCENT, w=18, h=2).pack(pady=6)

        self._t1_new()

    def _t1_score_text(self):
        return f"Правильно: {self.t1_score}  /  Завдань: {self.t1_attempts}"

    def _t1_new(self):
        self.t1_answered = False
        # Mix: 40% prime, 40% composite, 20% tricky (1, large prime, large composite)
        pool = []
        pool += [n for n in range(2, 100) if is_prime(n)]        # primes
        pool += [n for n in range(4, 100) if not is_prime(n)]    # composites
        pool += [1, 101, 103, 107, 109, 121, 143, 169]           # tricky
        self.t1_number = random.choice(pool)
        if self.t1_num_lbl:
            self.t1_num_lbl.config(text=str(self.t1_number), fg=ACCENT)
        if self.t1_feed_lbl:
            self.t1_feed_lbl.config(text="")
        for b in [self.t1_prime_btn, self.t1_comp_btn]:
            b.config(state="normal")
        self.t1_prime_btn.config(bg=CARD_B, fg=ACCENT)
        self.t1_comp_btn.config(bg=CARD_R, fg=RED)
        if self.t1_score_lbl:
            self.t1_score_lbl.config(text=self._t1_score_text())

    def _t1_answer(self, ans):
        if self.t1_answered:
            return
        self.t1_answered = True
        self.t1_attempts += 1
        n = self.t1_number

        if n == 1:
            correct_ans = "special"
        elif is_prime(n):
            correct_ans = "prime"
        else:
            correct_ans = "composite"

        divs = get_divisors(n)

        if ans == correct_ans or (correct_ans == "special"):
            # Special case: 1 is neither — both buttons wrong, explain
            if correct_ans == "special":
                self.t1_feed_lbl.config(
                    text="⚠️  Число 1 — особливе! Воно НЕ є ні простим, ні складеним.\n"
                         "У нього лише один дільник — само себе.",
                    fg=ORANGE)
                self.t1_prime_btn.config(bg=ORANGE_LT, fg=ORANGE)
                self.t1_comp_btn.config(bg=ORANGE_LT, fg=ORANGE)
                self.t1_attempts -= 1  # don't count as attempt
            elif ans == "prime":
                self.t1_score += 1
                divs_str = ", ".join(map(str, divs))
                self.t1_feed_lbl.config(
                    text=f"🎉  Правильно!  {n} — ПРОСТЕ.\n"
                         f"Дільники: {divs_str}  (лише 2 дільники)",
                    fg=GREEN)
                self.t1_prime_btn.config(bg=GREEN_LT, fg=GREEN)
            else:
                self.t1_score += 1
                sf = smallest_factor(n)
                divs_str = ", ".join(map(str, divs))
                self.t1_feed_lbl.config(
                    text=f"🎉  Правильно!  {n} — СКЛАДЕНЕ.\n"
                         f"Наприклад, {n} ÷ {sf} = {n//sf}  →  є дільник {sf}.\n"
                         f"Усі дільники: {divs_str}",
                    fg=GREEN)
                self.t1_comp_btn.config(bg=GREEN_LT, fg=GREEN)
        else:
            # Wrong
            if ans == "prime":
                # said prime, actually composite
                sf = smallest_factor(n)
                divs_str = ", ".join(map(str, divs))
                self.t1_feed_lbl.config(
                    text=f"❌  Ні!  {n} — СКЛАДЕНЕ.\n"
                         f"{n} ÷ {sf} = {n//sf}  →  є дільник {sf} ≠ 1 і ≠ {n}.\n"
                         f"Усі дільники: {divs_str}",
                    fg=RED)
                self.t1_prime_btn.config(bg=RED_LT, fg=RED)
                self.t1_comp_btn.config(bg=GREEN_LT, fg=GREEN)
            else:
                # said composite, actually prime
                self.t1_feed_lbl.config(
                    text=f"❌  Ні!  {n} — ПРОСТЕ.\n"
                         f"Перевіряємо: ділиться тільки на 1 і на {n}.\n"
                         f"Інших дільників немає.",
                    fg=RED)
                self.t1_comp_btn.config(bg=RED_LT, fg=RED)
                self.t1_prime_btn.config(bg=GREEN_LT, fg=GREEN)

        for b in [self.t1_prime_btn, self.t1_comp_btn]:
            b.config(state="disabled")
        if self.t1_score_lbl:
            self.t1_score_lbl.config(text=self._t1_score_text())

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER 2 — Find all divisors (one by one)
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
            text=self._t2_score_text(), font=F_SCORE, bg=PANEL, fg=GREEN)
        self.t2_score_lbl.pack(side="left", padx=30)
        tk.Label(sbar, text="Знайди всі дільники — визнач тип числа",
                 font=("Segoe UI", 15, "bold"), bg=PANEL, fg=MUTED).pack(
            side="left", padx=10)

        center = tk.Frame(cf, bg=BG)
        center.pack(expand=True)

        # Task
        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=28, pady=10)
        task_f.pack(pady=(14, 4))
        tk.Label(task_f, text="Знайди ВСІ дільники числа — вводь по ОДНОМУ:",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack()
        self.t2_num_lbl = tk.Label(task_f, text="",
                                    font=("Segoe UI", 64, "bold"),
                                    bg=PANEL, fg=ACCENT)
        self.t2_num_lbl.pack()

        # Progress
        prog_f = tk.Frame(center, bg=BG)
        prog_f.pack(pady=4)
        tk.Label(prog_f, text="Знайдені:", font=F_BODYB, bg=BG, fg=GREEN).pack(side="left")
        self.t2_found_lbl = tk.Label(prog_f, text="—",
                                      font=F_BODYB, bg=BG, fg=GREEN)
        self.t2_found_lbl.pack(side="left", padx=(6, 24))
        self.t2_rem_lbl = tk.Label(prog_f, text="",
                                    font=F_SMALL, bg=BG, fg=MUTED)
        self.t2_rem_lbl.pack(side="left")

        # Input display
        inp_f = tk.Frame(center, bg=BTN_NUM,
                         highlightbackground=ACCENT, highlightthickness=2,
                         padx=14, pady=6)
        inp_f.pack(pady=6)
        tk.Label(inp_f, text="Ваше число:", font=F_BODY,
                 bg=BTN_NUM, fg=MUTED).pack(side="left")
        self.t2_inp_lbl = tk.Label(inp_f, text="",
                                    font=("Segoe UI", 44, "bold"),
                                    bg=BTN_NUM, fg=ACCENT, width=5)
        self.t2_inp_lbl.pack(side="left", padx=10)

        # Feedback
        self.t2_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                     bg=BG, fg=ORANGE,
                                     wraplength=680, justify="center")
        self.t2_feed_lbl.pack(pady=4)

        # Numpad centred
        np_outer = tk.Frame(center, bg=BG)
        np_outer.pack(pady=8)
        for row_chars in [("7","8","9"),("4","5","6"),("1","2","3"),("C","0","⌫")]:
            rf = tk.Frame(np_outer, bg=BG)
            rf.pack(pady=4)
            for ch in row_chars:
                if ch.isdigit():
                    bc, fc = BTN_NUM, TEXT
                elif ch == "C":
                    bc, fc = RED_LT, RED
                else:
                    bc, fc = CARD_V, ACCENT2
                b = tk.Button(rf, text=ch, font=F_NUM, width=4, height=1,
                              bg=bc, fg=fc, relief="flat", cursor="hand2",
                              command=lambda c=ch: self._t2_key(c))
                b.pack(side="left", padx=5)
                orig = bc
                b.bind("<Enter>", lambda e, x=b, o=orig: x.config(bg=_darken(o, 18)))
                b.bind("<Leave>", lambda e, x=b, o=orig: x.config(bg=o))

        act = tk.Frame(center, bg=BG)
        act.pack(pady=10)
        self.t2_check_btn = mkbtn(act, "✔  Перевірити", self._t2_check,
                                   bg=GREEN, w=14, h=2)
        self.t2_check_btn.pack(side="left", padx=10)
        self.t2_next_btn = mkbtn(act, "▶  Наступне", self._t2_new,
                                  bg=ACCENT, w=12, h=2)
        self.t2_next_btn.pack(side="left", padx=10)

        self._t2_new()

    def _t2_score_text(self):
        return f"Правильно: {self.t2_score}  /  Завдань: {self.t2_attempts}"

    def _t2_new(self):
        # Numbers 2–60, mix of prime and composite
        pool = list(range(2, 61))
        self.t2_number    = random.choice(pool)
        self.t2_correct   = get_divisors(self.t2_number)
        self.t2_remaining = list(self.t2_correct)
        self.t2_found     = []
        self.t2_input     = ""
        self.t2_done      = False
        self.t2_attempts += 1

        if self.t2_num_lbl:   self.t2_num_lbl.config(text=str(self.t2_number), fg=ACCENT)
        if self.t2_inp_lbl:   self.t2_inp_lbl.config(text="", fg=ACCENT)
        if self.t2_feed_lbl:  self.t2_feed_lbl.config(text="")
        if self.t2_check_btn: self.t2_check_btn.config(state="normal", bg=GREEN)
        self._t2_update_progress()
        if self.t2_score_lbl: self.t2_score_lbl.config(text=self._t2_score_text())

    def _t2_update_progress(self):
        found_str = ",  ".join(map(str, sorted(self.t2_found))) if self.t2_found else "—"
        rem = len(self.t2_remaining)
        if self.t2_found_lbl:
            self.t2_found_lbl.config(text=found_str)
        if self.t2_rem_lbl:
            if rem > 0 and not self.t2_done:
                self.t2_rem_lbl.config(
                    text=f"(ще {rem} {'дільник' if rem==1 else 'дільники'})",
                    fg=MUTED)
            else:
                self.t2_rem_lbl.config(text="")

    def _t2_key(self, ch):
        if self.t2_done:
            return
        if ch.isdigit():
            if len(self.t2_input) < 5:
                self.t2_input += ch
        elif ch == "⌫":
            self.t2_input = self.t2_input[:-1]
        elif ch == "C":
            self.t2_input = ""
        if self.t2_inp_lbl:
            self.t2_inp_lbl.config(text=self.t2_input)

    def _t2_check(self):
        raw = self.t2_input.strip()
        if not raw:
            if self.t2_feed_lbl:
                self.t2_feed_lbl.config(text="⚠️  Введіть число!", fg=ORANGE)
            return
        try:
            val = int(raw)
        except ValueError:
            if self.t2_feed_lbl:
                self.t2_feed_lbl.config(text="❌  Введіть ціле число.", fg=RED)
            return
        finally:
            self.t2_input = ""
            if self.t2_inp_lbl:
                self.t2_inp_lbl.config(text="")

        n = self.t2_number
        if val in self.t2_found:
            if self.t2_feed_lbl:
                self.t2_feed_lbl.config(
                    text=f"🔁  {val} вже знайдено! Введіть інше число.", fg=ORANGE)
        elif val in self.t2_remaining:
            self.t2_remaining.remove(val)
            self.t2_found.append(val)
            self._t2_update_progress()
            if not self.t2_remaining:
                # All found!
                self.t2_score += 1
                self.t2_done = True
                divs = self.t2_correct
                if n == 1:
                    verdict = "⚠️  Число 1 — особливе (не просте і не складене)"
                elif len(divs) == 2:
                    verdict = f"🔵  {n} — ПРОСТЕ число (рівно 2 дільники)"
                else:
                    verdict = f"🔴  {n} — СКЛАДЕНЕ число ({len(divs)} дільники)"
                if self.t2_feed_lbl:
                    self.t2_feed_lbl.config(
                        text=f"🎉  Усі дільники знайдені!\n{verdict}",
                        fg=GREEN)
                if self.t2_inp_lbl:
                    self.t2_inp_lbl.config(fg=GREEN)
                if self.t2_check_btn:
                    self.t2_check_btn.config(state="disabled", bg=BTN_NUM)
                if self.t2_score_lbl:
                    self.t2_score_lbl.config(text=self._t2_score_text())
            else:
                if self.t2_feed_lbl:
                    self.t2_feed_lbl.config(
                        text=f"✅  {val} — дільник!  "
                             f"Ще {len(self.t2_remaining)} …",
                        fg=GREEN)
        else:
            if n % val == 0 and val > n:
                msg = f"❌  {val} більше за {n} — не може бути дільником."
            else:
                msg = (f"❌  {val} не ділить {n} без остачі.  "
                       f"{n} ÷ {val} = {n//val if val else '?'} "
                       f"(остача {n%val if val else '?'})")
            if self.t2_feed_lbl:
                self.t2_feed_lbl.config(text=msg, fg=RED)

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER 3 — Sieve of Eratosthenes: select all primes 1–100
    # All cells start neutral (same colour). Task: click every prime number.
    # ══════════════════════════════════════════════════════════════════════════
    def show_trainer_3(self):
        self.clear_main()
        self.mode = "trainer3"

        cf = self.current_frame

        # ── Score bar ─────────────────────────────────────────────────────
        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.t3_score_lbl = tk.Label(
            sbar,
            text=f"Спроб: {self.t3_attempts}  |  Правильно: {self.t3_score}",
            font=F_SCORE, bg=PANEL, fg=GREEN)
        self.t3_score_lbl.pack(side="left", padx=30)

        # Selected-count label (live counter)
        self.t3_count_lbl = tk.Label(
            sbar, text="Вибрано: 0",
            font=("Segoe UI", 15, "bold"), bg=PANEL, fg=ACCENT)
        self.t3_count_lbl.pack(side="right", padx=30)

        # ── Instruction panel ─────────────────────────────────────────────
        center = tk.Frame(cf, bg=BG)
        center.pack(expand=True, fill="both")

        instr_f = tk.Frame(center, bg=PANEL,
                           highlightbackground=BORDER, highlightthickness=1,
                           padx=24, pady=10)
        instr_f.pack(pady=(10, 6), fill="x", padx=30)
        tk.Label(instr_f,
                 text="🏺  Решето Ератосфена  —  вибери ВСІ прості числа від 1 до 100",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack(anchor="w")
        tk.Label(instr_f,
                 text="Натисни на число, щоб позначити його як просте (синє).  "
                      "Натисни ще раз — зніми позначку.",
                 font=F_SMALL, bg=PANEL, fg=MUTED).pack(anchor="w")

        # ── Number grid 1–100, 10 columns ────────────────────────────────
        self.t3_marked = set()          # numbers user selected as prime
        self.t3_primes_in_range = {n for n in range(1, 101) if is_prime(n)}
        self.t3_btns = {}

        grid_wrap = tk.Frame(center, bg=BG)
        grid_wrap.pack(pady=6, padx=30, anchor="w")

        for i, n in enumerate(range(1, 101)):
            b = tk.Button(grid_wrap, text=str(n),
                          font=F_GRID,
                          width=4, height=2,
                          bg=BTN_NUM, fg=TEXT,          # all neutral at start
                          relief="flat", cursor="hand2",
                          command=lambda x=n: self._t3_toggle(x))
            b.grid(row=i // 10, column=i % 10, padx=3, pady=3)
            self.t3_btns[n] = b

        # ── Legend ────────────────────────────────────────────────────────
        leg = tk.Frame(center, bg=BG)
        leg.pack(pady=4, padx=30, anchor="w")
        for bg_c, fg_c, txt in [
            (BTN_NUM,   TEXT,   "Не вибрано"),
            (CARD_B,    ACCENT, "Вибрано як просте"),
            (GREEN_LT,  GREEN,  "✅ Правильно"),
            (RED_LT,    RED,    "❌ Помилка"),
            (ORANGE_LT, ORANGE, "🟡 Пропущено"),
        ]:
            f = tk.Frame(leg, bg=bg_c, padx=8, pady=3,
                         highlightbackground=BORDER, highlightthickness=1)
            f.pack(side="left", padx=5)
            tk.Label(f, text=txt, font=F_SMALL, bg=bg_c, fg=fg_c).pack()

        # ── Feedback ──────────────────────────────────────────────────────
        self.t3_feed_lbl = tk.Label(
            center, text="", font=F_FEED,
            bg=BG, fg=ORANGE,
            wraplength=self.SW - 80, justify="center")
        self.t3_feed_lbl.pack(pady=4)

        # ── Action buttons ────────────────────────────────────────────────
        act = tk.Frame(center, bg=BG)
        act.pack(pady=6)
        self.t3_check_btn = mkbtn(
            act, "✔  Перевірити", self._t3_check,
            bg=GREEN, w=14, h=2)
        self.t3_check_btn.pack(side="left", padx=10)
        mkbtn(act, "🔄  Скинути", self._t3_reset,
              bg=ORANGE, w=10, h=2).pack(side="left", padx=10)

    # ── Toggle a cell ──────────────────────────────────────────────────────
    def _t3_toggle(self, n):
        if n in self.t3_marked:
            self.t3_marked.discard(n)
            self.t3_btns[n].config(bg=BTN_NUM, fg=TEXT)
        else:
            self.t3_marked.add(n)
            self.t3_btns[n].config(bg=CARD_B, fg=ACCENT)
        # update live counter
        if self.t3_count_lbl:
            self.t3_count_lbl.config(text=f"Вибрано: {len(self.t3_marked)}")

    # ── Reset ──────────────────────────────────────────────────────────────
    def _t3_reset(self):
        self.t3_marked.clear()
        for b in self.t3_btns.values():
            b.config(bg=BTN_NUM, fg=TEXT, state="normal")
        if self.t3_feed_lbl:
            self.t3_feed_lbl.config(text="")
        if self.t3_check_btn:
            self.t3_check_btn.config(state="normal", bg=GREEN)
        if self.t3_count_lbl:
            self.t3_count_lbl.config(text="Вибрано: 0")

    # ── Check ──────────────────────────────────────────────────────────────
    def _t3_check(self):
        self.t3_attempts += 1

        correct  = self.t3_primes_in_range          # all true primes 1–100
        selected = self.t3_marked                   # what user clicked

        true_pos  = correct & selected              # correctly selected primes
        false_pos = selected - correct              # selected but not prime (1 or composite)
        missed    = correct - selected              # primes not selected

        perfect = (not false_pos and not missed)
        if perfect:
            self.t3_score += 1

        # Colour every cell with result
        for n, b in self.t3_btns.items():
            b.config(state="disabled")
            if n in true_pos:
                b.config(bg=GREEN_LT, fg=GREEN)      # ✅ correct prime selected
            elif n in false_pos:
                b.config(bg=RED_LT,   fg=RED)        # ❌ selected but not prime
            elif n in missed:
                b.config(bg=ORANGE_LT, fg=ORANGE)    # 🟡 prime not selected
            else:
                b.config(bg=BTN_NUM,  fg=MUTED)      # correctly ignored composite/1

        if self.t3_score_lbl:
            self.t3_score_lbl.config(
                text=f"Спроб: {self.t3_attempts}  |  Правильно: {self.t3_score}")

        if perfect:
            primes_str = "  ".join(str(n) for n in sorted(correct))
            if self.t3_feed_lbl:
                self.t3_feed_lbl.config(
                    text=f"🎉  Чудово!  Всі {len(correct)} простих числа знайдені правильно!\n"
                         f"{primes_str}",
                    fg=GREEN)
        else:
            parts = []
            if false_pos:
                parts.append("❌  Вибрано зайве (не прості!):  "
                             + ", ".join(map(str, sorted(false_pos))))
            if missed:
                parts.append("🟡  Пропущено прості:  "
                             + ", ".join(map(str, sorted(missed))))
            if self.t3_feed_lbl:
                self.t3_feed_lbl.config(text="\n".join(parts), fg=RED)

        if self.t3_check_btn:
            self.t3_check_btn.config(state="disabled", bg=BTN_NUM)


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
