import tkinter as tk
import random
import math

# ── Light-theme Palette ───────────────────────────────────────────────────────
BG        = "#f0f4f8"   # very light blue-grey
PANEL     = "#ffffff"   # white
CARD_DIV  = "#dbeafe"   # light blue card
CARD_MUL  = "#ede9fe"   # light violet card
CARD_GRN  = "#dcfce7"   # light green card
ACCENT    = "#1d4ed8"   # strong blue
ACCENT2   = "#7c3aed"   # strong violet
GREEN     = "#15803d"   # dark green
GREEN_LT  = "#bbf7d0"   # light green bg
RED       = "#b91c1c"   # dark red
RED_LT    = "#fee2e2"   # light red bg
ORANGE    = "#b45309"   # dark amber
ORANGE_LT = "#fef3c7"   # light amber bg
TEXT      = "#0f172a"   # near-black
MUTED     = "#475569"
WHITE     = "#ffffff"
BTN_NUM   = "#e2e8f0"   # numpad key bg
BTN_HOV   = "#cbd5e1"   # numpad hover
BORDER    = "#cbd5e1"
YELLOW_HL = "#fbbf24"   # highlight accent
NAV_BG    = "#1e3a5f"   # dark nav bar
NAV_FG    = "#ffffff"
HDR_BG    = "#1d4ed8"

# ── Fonts ─────────────────────────────────────────────────────────────────────
F_TITLE  = ("Segoe UI", 34, "bold")
F_HEAD   = ("Segoe UI", 26, "bold")
F_SUB    = ("Segoe UI", 20, "bold")
F_BODY   = ("Segoe UI", 17)
F_BODYB  = ("Segoe UI", 17, "bold")
F_BIG    = ("Segoe UI", 60, "bold")
F_HUGE   = ("Segoe UI", 80, "bold")
F_BTN    = ("Segoe UI", 19, "bold")
F_NAV    = ("Segoe UI", 14, "bold")
F_SCORE  = ("Segoe UI", 20, "bold")
F_FEED   = ("Segoe UI", 18)
F_NUM    = ("Segoe UI", 26, "bold")
F_SMALL  = ("Segoe UI", 13)


def btn(parent, text, cmd, bg=ACCENT, fg=WHITE, font=F_BTN,
        w=12, h=2, px=6, py=6):
    b = tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg,
                  font=font, width=w, height=h,
                  relief="flat", bd=0, cursor="hand2",
                  activebackground=bg, activeforeground=fg,
                  padx=px, pady=py)
    b.bind("<Enter>", lambda e: b.config(bg=_darken(bg, 30)))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


def _darken(hex_color, amt=30):
    r = max(0, int(hex_color[1:3], 16) - amt)
    g = max(0, int(hex_color[3:5], 16) - amt)
    b = max(0, int(hex_color[5:7], 16) - amt)
    return f"#{r:02x}{g:02x}{b:02x}"


def _lighten(hex_color, amt=30):
    r = min(255, int(hex_color[1:3], 16) + amt)
    g = min(255, int(hex_color[3:5], 16) + amt)
    b = min(255, int(hex_color[5:7], 16) + amt)
    return f"#{r:02x}{g:02x}{b:02x}"


def hline(parent, color=BORDER):
    tk.Frame(parent, bg=color, height=2).pack(fill="x", pady=(4, 12))


def card(parent, title, body_text, bg_color, fg_text=TEXT, w=None):
    f = tk.Frame(parent, bg=bg_color, padx=22, pady=14,
                 highlightbackground=BORDER, highlightthickness=1)
    kw = {"fill": "x", "pady": 6}
    if w: kw = {"pady": 6}
    f.pack(**kw)
    tk.Label(f, text=title, font=F_BODYB, bg=bg_color, fg=fg_text,
             anchor="w").pack(fill="x")
    tk.Label(f, text=body_text, font=F_BODY, bg=bg_color, fg=fg_text,
             justify="left", wraplength=1300, anchor="w").pack(fill="x",
                                                                pady=(4, 0))
    return f


# ══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("§ 26. Дільники і кратні натурального числа")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        self.bind("<Return>",    lambda e: self._on_enter())
        self.bind("<BackSpace>", lambda e: self._on_bs())

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()

        self.current_frame = None
        self.mode = None

        # ── Divisors trainer state ─────────────────────────────────────────
        self.div_number    = 0
        self.div_correct   = []        # sorted list of all divisors
        self.div_remaining = []        # divisors still to be found
        self.div_found     = []        # confirmed correct answers so far
        self.div_input     = ""
        self.div_score     = 0
        self.div_attempts  = 0        # tasks attempted
        self.div_task_done = False

        # ── Multiples trainer state ────────────────────────────────────────
        self.mul_number    = 0
        self.mul_options   = []
        self.mul_correct   = set()
        self.mul_selected  = []
        self.mul_btns      = []
        self.mul_score     = 0
        self.mul_attempts  = 0

        # ── UI refs ────────────────────────────────────────────────────────
        self.div_num_lbl    = None
        self.div_input_lbl  = None
        self.div_found_lbl  = None
        self.div_remain_lbl = None
        self.div_feed_lbl   = None
        self.div_score_lbl  = None
        self.div_check_btn  = None
        self.div_next_btn   = None

        self.mul_num_lbl   = None
        self.mul_feed_lbl  = None
        self.mul_score_lbl = None
        self.mul_check_btn = None
        self.mul_next_btn  = None

        self._build_chrome()
        self.show_main_menu()

    # ── Chrome ────────────────────────────────────────────────────────────────
    def _build_chrome(self):
        hdr = tk.Frame(self, bg=HDR_BG, height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="§ 26.   Дільники і кратні натурального числа",
                 bg=HDR_BG, fg=WHITE, font=("Segoe UI", 21, "bold")).pack(
                 side="left", padx=30)
        btn(hdr, "✕  Вийти", self.destroy, bg="#b91c1c",
            font=("Segoe UI", 13, "bold"), w=9, h=1).pack(
            side="right", padx=18, pady=16)

        nav = tk.Frame(self, bg=NAV_BG, height=52)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        nav_items = [
            ("📖  Теорія: Дільники",   self.show_divisors_theory),
            ("📖  Теорія: Кратні",     self.show_multiples_theory),
            ("🎯  Тренажер: Дільники", self.show_divisors_trainer),
            ("🎯  Тренажер: Кратні",   self.show_multiples_trainer),
        ]
        for label, cmd in nav_items:
            b = tk.Button(nav, text=label, command=cmd,
                          bg=NAV_BG, fg=NAV_FG, font=F_NAV,
                          relief="flat", bd=0, cursor="hand2",
                          activebackground=ACCENT, activeforeground=WHITE,
                          padx=18, pady=14)
            b.pack(side="left")
            b.bind("<Enter>", lambda e, x=b: x.config(bg=ACCENT))
            b.bind("<Leave>", lambda e, x=b: x.config(bg=NAV_BG))

        self.main_area = tk.Frame(self, bg=BG)
        self.main_area.pack(fill="both", expand=True)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def clear_main(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.main_area, bg=BG)
        self.current_frame.pack(expand=True, fill="both")

    def _get_divisors(self, n):
        d = set()
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                d.add(i); d.add(n // i)
        return sorted(d)

    def _on_enter(self):
        if self.mode == "div_trainer":
            if not self.div_task_done:
                self._div_check()
            else:
                self._div_new()

    def _on_bs(self):
        if self.mode == "div_trainer":
            self._div_key("⌫")

    # ══════════════════════════════════════════════════════════════════════════
    # MAIN MENU
    # ══════════════════════════════════════════════════════════════════════════
    def show_main_menu(self):
        self.clear_main()
        self.mode = "menu"
        center = tk.Frame(self.current_frame, bg=BG)
        center.place(relx=.5, rely=.5, anchor="center")

        tk.Label(center, text="Дільники і кратні", font=("Segoe UI", 54, "bold"),
                 bg=BG, fg=TEXT).pack(pady=(0, 4))
        tk.Label(center, text="натурального числа", font=("Segoe UI", 30),
                 bg=BG, fg=ACCENT).pack(pady=(0, 36))

        cards_data = [
            ("📖", "Теорія\nДільники",   CARD_DIV, ACCENT,  self.show_divisors_theory),
            ("📖", "Теорія\nКратні",     CARD_MUL, ACCENT2, self.show_multiples_theory),
            ("🎯", "Тренажер\nДільники", CARD_GRN, GREEN,   self.show_divisors_trainer),
            ("🎯", "Тренажер\nКратні",   "#fef9c3", ORANGE, self.show_multiples_trainer),
        ]
        row = tk.Frame(center, bg=BG)
        row.pack()
        for icon, title, bg_c, fg_c, cmd in cards_data:
            c = tk.Frame(row, bg=bg_c, width=210, height=190,
                         highlightbackground=BORDER, highlightthickness=2)
            c.pack(side="left", padx=14)
            c.pack_propagate(False)
            tk.Label(c, text=icon, font=("Segoe UI", 38),
                     bg=bg_c, fg=fg_c).pack(pady=(22, 4))
            tk.Label(c, text=title, font=("Segoe UI", 15, "bold"),
                     bg=bg_c, fg=fg_c, justify="center").pack()
            for w in [c] + c.winfo_children():
                w.bind("<Button-1>", lambda e, f=cmd: f())
                w.bind("<Enter>",    lambda e, x=c, col=bg_c: x.config(bg=_darken(col, 15)))
                w.bind("<Leave>",    lambda e, x=c, col=bg_c: x.config(bg=col))

        tk.Label(center, text="Натисніть на картку або скористайтесь меню зверху",
                 font=F_SMALL, bg=BG, fg=MUTED).pack(pady=20)

    # ══════════════════════════════════════════════════════════════════════════
    # THEORY — DIVISORS  (5th grade: no square roots)
    # ══════════════════════════════════════════════════════════════════════════
    def show_divisors_theory(self):
        self.clear_main()
        self.mode = "theory_div"

        scroll_canvas = tk.Canvas(self.current_frame, bg=BG, highlightthickness=0)
        vsb = tk.Scrollbar(self.current_frame, orient="vertical",
                           command=scroll_canvas.yview)
        scroll_canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        scroll_canvas.pack(side="left", fill="both", expand=True)

        outer = tk.Frame(scroll_canvas, bg=BG)
        win_id = scroll_canvas.create_window((0, 0), window=outer, anchor="nw")
        outer.bind("<Configure>",
                   lambda e: scroll_canvas.configure(
                       scrollregion=scroll_canvas.bbox("all")))
        scroll_canvas.bind("<Configure>",
                           lambda e: scroll_canvas.itemconfig(
                               win_id, width=e.width))

        p = tk.Frame(outer, bg=BG)
        p.pack(fill="both", expand=True, padx=60, pady=28)

        tk.Label(p, text="Дільники натурального числа",
                 font=F_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        hline(p, ACCENT)

        card(p, "📌  Означення",
             "Дільником натурального числа називають натуральне число,\n"
             "на яке дане число ділиться без остачі.",
             CARD_DIV)

        card(p, "⚡  Важливо",
             "Будь-яке натуральне число a завжди ділиться на 1 і на саме себе.\n"
             "Тому 1 і a — завжди дільники числа a.\n"
             "1 — найменший дільник,    a — найбільший дільник числа a.",
             CARD_GRN)

        card(p, "✏️  Приклад — знайти всі дільники числа 18",
             "Перевіряємо: ділиться 18 на 1? Так → 1 і 18 — дільники.\n"
             "Ділиться на 2? Так → 2 і 9 — дільники.\n"
             "Ділиться на 3? Так → 3 і 6 — дільники.\n"
             "Ділиться на 4? Ні.    Ділиться на 5? Ні.\n\n"
             "Відповідь:  дільники числа 18 — це  1, 2, 3, 6, 9, 18",
             CARD_MUL)

        card(p, "🔑  Як знайти всі дільники: алгоритм",
             "1. Починаємо перевірку з числа 1.\n"
             "2. Якщо число ділиться — записуємо його як дільник.\n"
             "3. Перевіряємо 2, 3, 4, 5 … до половини числа (можна трохи менше).\n"
             "4. Не забуваємо записати саме число a — воно теж є дільником!",
             "#fef9c3")

        # ── Live demo ──────────────────────────────────────────────────────
        demo_f = tk.Frame(p, bg=PANEL, padx=22, pady=16,
                          highlightbackground=BORDER, highlightthickness=1)
        demo_f.pack(fill="x", pady=10)
        tk.Label(demo_f, text="🔢  Спробуйте самі — введіть число:",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(anchor="w")
        row = tk.Frame(demo_f, bg=PANEL)
        row.pack(anchor="w", pady=8)
        entry = tk.Entry(row, font=F_HEAD, width=7, bg=BTN_NUM, fg=TEXT,
                         relief="flat", insertbackground=ACCENT)
        entry.pack(side="left", ipady=6, padx=(0, 10))
        res_lbl = tk.Label(row, text="", font=F_BODYB, bg=PANEL, fg=ACCENT,
                           wraplength=self.SW - 300, justify="left")
        res_lbl.pack(side="left")

        def calc(*_):
            try:
                n = int(entry.get())
                if 1 <= n <= 9999:
                    divs = self._get_divisors(n)
                    res_lbl.config(
                        text=f"Дільники числа {n}:   "
                             + ",   ".join(map(str, divs))
                             + f"   ({len(divs)} шт.)",
                        fg=ACCENT)
                else:
                    res_lbl.config(text="Введіть число від 1 до 9999", fg=RED)
            except ValueError:
                res_lbl.config(text="Введіть ціле число", fg=RED)

        btn(row, "Знайти →", calc, bg=ACCENT, w=9, h=1).pack(side="left")
        entry.bind("<Return>", calc)

    # ══════════════════════════════════════════════════════════════════════════
    # THEORY — MULTIPLES
    # ══════════════════════════════════════════════════════════════════════════
    def show_multiples_theory(self):
        self.clear_main()
        self.mode = "theory_mul"

        scroll_canvas = tk.Canvas(self.current_frame, bg=BG, highlightthickness=0)
        vsb = tk.Scrollbar(self.current_frame, orient="vertical",
                           command=scroll_canvas.yview)
        scroll_canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        scroll_canvas.pack(side="left", fill="both", expand=True)

        outer = tk.Frame(scroll_canvas, bg=BG)
        win_id = scroll_canvas.create_window((0, 0), window=outer, anchor="nw")
        outer.bind("<Configure>",
                   lambda e: scroll_canvas.configure(
                       scrollregion=scroll_canvas.bbox("all")))
        scroll_canvas.bind("<Configure>",
                           lambda e: scroll_canvas.itemconfig(
                               win_id, width=e.width))

        p = tk.Frame(outer, bg=BG)
        p.pack(fill="both", expand=True, padx=60, pady=28)

        tk.Label(p, text="Кратні натурального числа",
                 font=F_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        hline(p, ACCENT2)

        card(p, "📌  Означення",
             "Кратним натурального числа a називають натуральне число,\n"
             "яке ділиться на a без остачі.",
             CARD_MUL)

        card(p, "⚡  Важливо",
             "Кратних числа a — нескінченно багато:\n"
             "a,   2·a,   3·a,   4·a,   5·a,  …\n\n"
             "Найменше кратне числа a — це саме число a.",
             CARD_GRN)

        card(p, "✏️  Приклад — кратні числа 7",
             "7×1 = 7     7×2 = 14     7×3 = 21     7×4 = 28     7×5 = 35\n"
             "7×6 = 42    7×7 = 49     7×8 = 56  …  і так далі без кінця.\n\n"
             "Кратні числа 7:  7, 14, 21, 28, 35, 42, 49, 56, …",
             CARD_DIV)

        card(p, "🔑  Зв'язок: дільник ↔ кратне",
             "Якщо b ділиться на a без остачі — значить:\n"
             "  •  a  є дільником числа  b\n"
             "  •  b  є кратним числа  a\n\n"
             "Приклад:  28 ÷ 7 = 4  (без остачі)  →  7 — дільник 28,  28 — кратне 7.",
             "#fef9c3")

        # ── Multiples strip demo ────────────────────────────────────────────
        demo_f = tk.Frame(p, bg=PANEL, padx=22, pady=16,
                          highlightbackground=BORDER, highlightthickness=1)
        demo_f.pack(fill="x", pady=10)
        tk.Label(demo_f, text="🔢  Оберіть число — побачте кратні:",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(anchor="w")

        btns_row = tk.Frame(demo_f, bg=PANEL)
        btns_row.pack(anchor="w", pady=(6, 8))

        strip = tk.Frame(demo_f, bg=PANEL)
        strip.pack(fill="x")

        COLORS = [ACCENT, ACCENT2, GREEN, ORANGE, "#0891b2", "#be185d",
                  "#65a30d", "#b45309", "#0f766e", "#7c2d12", "#1d4ed8", "#4f46e5"]

        def show_mul(n):
            for w in strip.winfo_children():
                w.destroy()
            for k in range(1, 13):
                c = COLORS[(k - 1) % len(COLORS)]
                box = tk.Frame(strip, bg=c, width=86, height=74)
                box.pack(side="left", padx=3)
                box.pack_propagate(False)
                tk.Label(box, text=f"{n}×{k}", font=("Segoe UI", 11),
                         bg=c, fg=WHITE).pack(pady=(6, 0))
                tk.Label(box, text=str(n * k), font=("Segoe UI", 19, "bold"),
                         bg=c, fg=WHITE).pack()

        for n in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15]:
            b = btn(btns_row, str(n), lambda x=n: show_mul(x),
                    bg=BTN_NUM, fg=TEXT, font=("Segoe UI", 15, "bold"),
                    w=4, h=1, px=4, py=4)
            b.pack(side="left", padx=3)
            # Fix hover for light buttons
            orig = BTN_NUM
            b.bind("<Enter>", lambda e, x=b: x.config(bg=BTN_HOV))
            b.bind("<Leave>", lambda e, x=b: x.config(bg=BTN_NUM))

        show_mul(3)

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER — DIVISORS  (one-by-one entry with numpad centred)
    # ══════════════════════════════════════════════════════════════════════════
    def show_divisors_trainer(self):
        self.clear_main()
        self.mode = "div_trainer"
        self.div_task_done = False

        cf = self.current_frame

        # ── Score bar ─────────────────────────────────────────────────────
        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.div_score_lbl = tk.Label(sbar,
            text=f"Правильно: {self.div_score}  /  Завдань: {self.div_attempts}",
            font=F_SCORE, bg=PANEL, fg=GREEN)
        self.div_score_lbl.pack(side="left", padx=30)

        # ── Main centred column ────────────────────────────────────────────
        center = tk.Frame(cf, bg=BG)
        center.pack(expand=True)

        # Task question
        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=30, pady=14)
        task_f.pack(pady=(20, 8))
        tk.Label(task_f,
                 text="Знайдіть ВСІ дільники числа — вводьте по ОДНОМУ:",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack(side="left", padx=(0, 20))
        self.div_num_lbl = tk.Label(task_f, text="", font=F_BIG,
                                     bg=PANEL, fg=ACCENT)
        self.div_num_lbl.pack(side="left")

        # Progress: found / remaining
        prog_f = tk.Frame(center, bg=BG)
        prog_f.pack(pady=4)
        tk.Label(prog_f, text="Знайдені:", font=F_BODYB, bg=BG, fg=GREEN).pack(side="left")
        self.div_found_lbl = tk.Label(prog_f, text="", font=F_BODYB,
                                       bg=BG, fg=GREEN)
        self.div_found_lbl.pack(side="left", padx=(4, 30))
        self.div_remain_lbl = tk.Label(prog_f, text="", font=F_SMALL,
                                        bg=BG, fg=MUTED)
        self.div_remain_lbl.pack(side="left")

        # Input display
        inp_f = tk.Frame(center, bg=BTN_NUM,
                         highlightbackground=ACCENT, highlightthickness=2,
                         padx=16, pady=8)
        inp_f.pack(pady=8)
        tk.Label(inp_f, text="Ваше число:", font=F_BODY, bg=BTN_NUM, fg=MUTED).pack(side="left")
        self.div_input_lbl = tk.Label(inp_f, text="", font=("Segoe UI", 44, "bold"),
                                       bg=BTN_NUM, fg=ACCENT, width=5)
        self.div_input_lbl.pack(side="left", padx=10)

        # Feedback
        self.div_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                      bg=BG, fg=ORANGE,
                                      wraplength=680, justify="center")
        self.div_feed_lbl.pack(pady=4)

        # ── Numpad (centred) ───────────────────────────────────────────────
        np_outer = tk.Frame(center, bg=BG)
        np_outer.pack(pady=10)

        layout = [
            ("7", "8", "9"),
            ("4", "5", "6"),
            ("1", "2", "3"),
            ("C", "0", "⌫"),
        ]
        NP_BG   = BTN_NUM
        NP_TEXT = TEXT
        for row_chars in layout:
            row_f = tk.Frame(np_outer, bg=BG)
            row_f.pack(pady=4)
            for ch in row_chars:
                if ch.isdigit():
                    bg_c, fg_c = NP_BG, NP_TEXT
                elif ch == "C":
                    bg_c, fg_c = RED_LT, RED
                else:  # ⌫
                    bg_c, fg_c = CARD_MUL, ACCENT2
                b = tk.Button(row_f, text=ch, font=F_NUM,
                              width=4, height=2,
                              bg=bg_c, fg=fg_c, relief="flat",
                              cursor="hand2",
                              command=lambda c=ch: self._div_key(c))
                b.pack(side="left", padx=5)
                b.bind("<Enter>", lambda e, x=b, col=bg_c: x.config(
                    bg=_darken(col, 20)))
                b.bind("<Leave>", lambda e, x=b, col=bg_c: x.config(bg=col))

        # Check / Next buttons
        act = tk.Frame(center, bg=BG)
        act.pack(pady=14)
        self.div_check_btn = btn(act, "✔  Перевірити", self._div_check,
                                  bg=GREEN, w=14, h=2)
        self.div_check_btn.pack(side="left", padx=10)
        self.div_next_btn = btn(act, "▶  Наступне завдання", self._div_new,
                                 bg=ACCENT, w=18, h=2)
        self.div_next_btn.pack(side="left", padx=10)

        self._div_new()

    # ── Divisors trainer logic ─────────────────────────────────────────────
    def _div_key(self, ch):
        if self.div_task_done:
            return
        if ch.isdigit():
            if len(self.div_input) < 6:
                self.div_input += ch
        elif ch == "⌫":
            self.div_input = self.div_input[:-1]
        elif ch == "C":
            self.div_input = ""
        if self.div_input_lbl:
            self.div_input_lbl.config(text=self.div_input)

    def _div_new(self):
        self.div_number    = random.randint(2, 60)
        self.div_correct   = self._get_divisors(self.div_number)
        self.div_remaining = list(self.div_correct)
        self.div_found     = []
        self.div_input     = ""
        self.div_task_done = False
        self.div_attempts += 1

        if self.div_num_lbl:    self.div_num_lbl.config(text=str(self.div_number))
        if self.div_input_lbl:  self.div_input_lbl.config(text="", fg=ACCENT)
        if self.div_feed_lbl:   self.div_feed_lbl.config(text="")
        if self.div_check_btn:  self.div_check_btn.config(state="normal",
                                                           bg=GREEN)
        if self.div_next_btn:   self.div_next_btn.config(state="normal",
                                                          bg=ACCENT)
        self._div_update_progress()
        if self.div_score_lbl:
            self.div_score_lbl.config(
                text=f"Правильно: {self.div_score}  /  Завдань: {self.div_attempts}")

    def _div_update_progress(self):
        found_str = ",  ".join(map(str, sorted(self.div_found))) if self.div_found else "—"
        remain    = len(self.div_remaining)
        if self.div_found_lbl:
            self.div_found_lbl.config(text=found_str)
        if self.div_remain_lbl:
            if remain > 0 and not self.div_task_done:
                self.div_remain_lbl.config(
                    text=f"(залишилось знайти: {remain} дільник{'и' if remain > 1 else ''} )",
                    fg=MUTED)
            else:
                self.div_remain_lbl.config(text="")

    def _div_check(self):
        raw = self.div_input.strip()
        if not raw:
            self.div_feed_lbl.config(text="⚠️  Введіть число!", fg=ORANGE)
            return
        try:
            val = int(raw)
        except ValueError:
            self.div_feed_lbl.config(text="❌  Введіть ціле число.", fg=RED)
            return
        finally:
            self.div_input = ""
            if self.div_input_lbl:
                self.div_input_lbl.config(text="")

        if val in self.div_remaining:
            # Correct!
            self.div_remaining.remove(val)
            self.div_found.append(val)
            self._div_update_progress()

            if not self.div_remaining:
                # All found!
                self.div_score += 1
                self.div_task_done = True
                self.div_feed_lbl.config(
                    text=f"🎉  Чудово!  Всі дільники числа {self.div_number} знайдені:  "
                         + ",  ".join(map(str, self.div_correct)),
                    fg=GREEN)
                if self.div_input_lbl:
                    self.div_input_lbl.config(fg=GREEN)
                if self.div_check_btn:
                    self.div_check_btn.config(state="disabled", bg=BTN_NUM)
                if self.div_score_lbl:
                    self.div_score_lbl.config(
                        text=f"Правильно: {self.div_score}  /  Завдань: {self.div_attempts}")
            else:
                self.div_feed_lbl.config(
                    text=f"✅  {val} — дільник!  Знайдіть ще {len(self.div_remaining)}…",
                    fg=GREEN)
        elif val in self.div_found:
            self.div_feed_lbl.config(
                text=f"🔁  {val} вже знайдено! Спробуйте інше число.", fg=ORANGE)
        elif self.div_number % val == 0 and val > self.div_number:
            self.div_feed_lbl.config(
                text=f"❌  {val} більше ніж {self.div_number} — не є дільником.", fg=RED)
        else:
            self.div_feed_lbl.config(
                text=f"❌  {val} не ділить {self.div_number} без остачі.  "
                     f"{self.div_number} ÷ {val} = {self.div_number // val} "
                     f"(остача {self.div_number % val})",
                fg=RED)

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER — MULTIPLES  (tap-to-select, one-by-one checking)
    # ══════════════════════════════════════════════════════════════════════════
    def show_multiples_trainer(self):
        self.clear_main()
        self.mode = "mul_trainer"

        cf = self.current_frame

        # ── Score bar ─────────────────────────────────────────────────────
        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.mul_score_lbl = tk.Label(sbar,
            text=f"Правильно: {self.mul_score}  /  Завдань: {self.mul_attempts}",
            font=F_SCORE, bg=PANEL, fg=GREEN)
        self.mul_score_lbl.pack(side="left", padx=30)

        # ── Centred column ─────────────────────────────────────────────────
        center = tk.Frame(cf, bg=BG)
        center.pack(expand=True)

        # Task
        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=30, pady=14)
        task_f.pack(pady=(18, 10))
        tk.Label(task_f,
                 text="Натисніть ВСІ числа, кратні числу:",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack(side="left", padx=(0, 20))
        self.mul_num_lbl = tk.Label(task_f, text="", font=F_BIG,
                                     bg=PANEL, fg=ACCENT)
        self.mul_num_lbl.pack(side="left")

        # Options grid — 2 rows × 5 cols
        grid_f = tk.Frame(center, bg=BG)
        grid_f.pack(pady=12)
        self.mul_btns = []
        for i in range(10):
            b = tk.Button(grid_f, text="", font=("Segoe UI", 24, "bold"),
                          width=8, height=2,
                          bg=BTN_NUM, fg=TEXT,
                          relief="flat", cursor="hand2",
                          command=lambda idx=i: self._mul_toggle(idx))
            b.grid(row=i // 5, column=i % 5, padx=7, pady=7)
            self.mul_btns.append(b)

        # Feedback
        self.mul_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                      bg=BG, fg=ORANGE,
                                      wraplength=700, justify="center")
        self.mul_feed_lbl.pack(pady=6)

        # Action buttons
        act = tk.Frame(center, bg=BG)
        act.pack(pady=12)
        self.mul_check_btn = btn(act, "✔  Перевірити", self._mul_check,
                                  bg=GREEN, w=14, h=2)
        self.mul_check_btn.pack(side="left", padx=10)
        self.mul_next_btn = btn(act, "▶  Наступне завдання", self._mul_new,
                                 bg=ACCENT, w=18, h=2)
        self.mul_next_btn.pack(side="left", padx=10)

        self._mul_new()

    # ── Multiples trainer logic ────────────────────────────────────────────
    def _gen_mul_opts(self, n):
        opts = set()
        # correct ones
        opts.add(n)
        opts.add(n * random.randint(2, 5))
        opts.add(n * random.randint(6, 10))
        opts.add(n * random.randint(11, 30))
        # traps: divisors of n
        divs = [i for i in range(2, n) if n % i == 0]
        if divs:
            opts.add(random.choice(divs))
        # near-miss: n*k ± 1
        opts.add(n * random.randint(2, 8) + random.randint(1, n - 1))
        # random non-multiples
        while len(opts) < 10:
            v = random.randint(2, n * 12)
            if v % n != 0:
                opts.add(v)
        lst = list(opts)
        random.shuffle(lst)
        return lst[:10]

    def _mul_new(self):
        self.mul_selected.clear()
        if self.mul_feed_lbl: self.mul_feed_lbl.config(text="")
        self.mul_number  = random.randint(3, 20)
        self.mul_options = self._gen_mul_opts(self.mul_number)
        self.mul_correct = {x for x in self.mul_options
                            if x % self.mul_number == 0}
        self.mul_attempts += 1

        if self.mul_num_lbl:
            self.mul_num_lbl.config(text=str(self.mul_number))
        for i, b in enumerate(self.mul_btns):
            b.config(text=str(self.mul_options[i]),
                     bg=BTN_NUM, fg=TEXT, state="normal")

        if self.mul_check_btn: self.mul_check_btn.config(state="normal", bg=GREEN)
        if self.mul_next_btn:  self.mul_next_btn.config(state="normal", bg=ACCENT)
        if self.mul_score_lbl:
            self.mul_score_lbl.config(
                text=f"Правильно: {self.mul_score}  /  Завдань: {self.mul_attempts}")

    def _mul_toggle(self, idx):
        v = self.mul_options[idx]
        b = self.mul_btns[idx]
        if v in self.mul_selected:
            self.mul_selected.remove(v)
            b.config(bg=BTN_NUM, fg=TEXT)
        else:
            self.mul_selected.append(v)
            b.config(bg=ACCENT, fg=WHITE)

    def _mul_check(self):
        user = set(self.mul_selected)
        corr = self.mul_correct
        miss  = corr - user
        extra = user - corr

        if not miss and not extra:
            self.mul_score += 1
            self.mul_feed_lbl.config(
                text=f"🎉  Відмінно!  Усі кратні числа {self.mul_number} знайдені!",
                fg=GREEN)
            self.mul_check_btn.config(state="disabled", bg=BTN_NUM)
        elif extra:
            self.mul_feed_lbl.config(
                text=f"❌  {', '.join(map(str, sorted(extra)))} — НЕ кратні числу {self.mul_number}",
                fg=RED)
        else:
            self.mul_feed_lbl.config(
                text=f"🤔  Пропущено кратні: {', '.join(map(str, sorted(miss)))}",
                fg=ORANGE)

        # Colour all buttons
        for i, v in enumerate(self.mul_options):
            b = self.mul_btns[i]
            if v in corr and v in user:    b.config(bg=GREEN,     fg=WHITE)
            elif v in corr:                b.config(bg=ORANGE_LT, fg=ORANGE)
            elif v in user:                b.config(bg=RED_LT,    fg=RED)
            else:                          b.config(bg=BTN_NUM,   fg=MUTED)

        if self.mul_score_lbl:
            self.mul_score_lbl.config(
                text=f"Правильно: {self.mul_score}  /  Завдань: {self.mul_attempts}")


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()