import tkinter as tk
import random
import math

# ── Palette ───────────────────────────────────────────────────────────────────
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
F_FRAC   = ("Segoe UI", 40, "bold")
F_FRAC_S = ("Segoe UI", 24, "bold")
F_SIGN   = ("Segoe UI", 44, "bold")


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


def frac_w(parent, n, d, bg=PANEL, size="big", color=ACCENT):
    sizes  = {"big": F_FRAC, "small": F_FRAC_S}
    widths = {"big": 66,     "small": 46}
    fn = sizes.get(size, F_FRAC_S)
    bw = widths.get(size, 46)
    f = tk.Frame(parent, bg=bg)
    tk.Label(f, text=str(n), font=fn, bg=bg, fg=color).pack()
    tk.Frame(f, bg=color, height=3, width=bw).pack(pady=2)
    tk.Label(f, text=str(d), font=fn, bg=bg, fg=color).pack()
    return f


def fraction_bar(parent, numer, denom, bg_filled=ACCENT, bg_empty=BTN_NUM,
                 cell_w=50, cell_h=50, bg=PANEL):
    """Row of denom cells, numer filled."""
    # Guard: can't fill more than denom
    fill = min(numer, denom)
    row = tk.Frame(parent, bg=bg)
    for i in range(denom):
        color = bg_filled if i < fill else bg_empty
        fc    = WHITE     if i < fill else MUTED
        cell = tk.Frame(row, bg=color, width=cell_w, height=cell_h,
                        highlightbackground=bg, highlightthickness=1)
        cell.pack(side="left", padx=2)
        cell.pack_propagate(False)
        tk.Label(cell, text="●" if i < fill else "○",
                 font=("Segoe UI", 16), bg=color, fg=fc).pack(expand=True)
    return row


def number_line_ext(parent, marks, bg=PANEL, width=800):
    """
    Extended number line 0 → 2, showing fractions at their positions.
    marks = list of (numerator, denominator, color, label)
    """
    H = 100
    cv = tk.Canvas(parent, bg=bg, width=width, height=H, highlightthickness=0)

    left, right = 50, width - 50
    mid_y = 55
    tick_h = 10
    span = right - left          # pixels for range 0→2

    # Line + arrow
    cv.create_line(left, mid_y, right, mid_y, fill=MUTED, width=2)
    cv.create_line(right-12, mid_y-6, right, mid_y, fill=MUTED, width=2)
    cv.create_line(right-12, mid_y+6, right, mid_y, fill=MUTED, width=2)

    # Ticks at 0, 1, 2
    for val, label in [(0, "0"), (1, "1"), (2, "2")]:
        x = left + val * span / 2
        cv.create_line(x, mid_y - tick_h, x, mid_y + tick_h,
                       fill=TEXT, width=3)
        cv.create_text(x, mid_y + 22, text=label,
                       font=("Segoe UI", 14, "bold"), fill=TEXT)

    # Shade 0–1 zone (правильні) and 1–2 zone (неправильні)
    mid_x = left + span / 2
    cv.create_rectangle(left, mid_y-8, mid_x, mid_y+8,
                        fill=CARD_G, outline="")
    cv.create_rectangle(mid_x, mid_y-8, right-30, mid_y+8,
                        fill=CARD_R, outline="")
    cv.create_line(left, mid_y, right, mid_y, fill=MUTED, width=2)

    # Zone labels
    cv.create_text((left + mid_x) / 2, mid_y - 20,
                   text="правильні дроби (< 1)",
                   font=("Segoe UI", 11), fill=GREEN)
    cv.create_text((mid_x + right - 30) / 2, mid_y - 20,
                   text="неправильні дроби (≥ 1)",
                   font=("Segoe UI", 11), fill=RED)

    for n, d, color, label in marks:
        val = n / d
        x = left + val * span / 2
        cv.create_oval(x-8, mid_y-8, x+8, mid_y+8,
                       fill=color, outline=WHITE, width=2)
        cv.create_text(x, mid_y + 38,
                       text=label,
                       font=("Segoe UI", 11, "bold"), fill=color)

    return cv


# ══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("§ 36. Правильні і неправильні дроби")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()
        self.current_frame = None
        self.mode = None

        # ── Trainer 1: Classify fraction ─────────────────────────────────
        self.t1_n = self.t1_d = 0
        self.t1_score = self.t1_attempts = 0
        self.t1_answered = False
        self.t1_score_lbl = None
        self.t1_frac_frame = None
        self.t1_feed_lbl = None
        self.t1_bar_frame = None
        self.t1_nl_frame = None

        # ── Trainer 2: Compare with 0 / 1 / bigger ───────────────────────
        # Given fraction, choose:  < 1  /  = 1  /  > 1
        self.t2_n = self.t2_d = 0
        self.t2_score = self.t2_attempts = 0
        self.t2_answered = False
        self.t2_score_lbl = None
        self.t2_frac_frame = None
        self.t2_feed_lbl = None

        self._build_chrome()
        self.show_main_menu()

    # ── Chrome ────────────────────────────────────────────────────────────────
    def _build_chrome(self):
        hdr = tk.Frame(self, bg=HDR_BG, height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="§ 36.   Правильні і неправильні дроби",
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
            ("🎯  Правильний чи неправильний?", self.show_trainer_1),
            ("🎯  Порівняй із числом 1",    self.show_trainer_2),
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

    def _scroll_page(self):
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
    # MAIN MENU
    # ══════════════════════════════════════════════════════════════════════════
    def show_main_menu(self):
        self.clear_main()
        self.mode = "menu"
        center = tk.Frame(self.current_frame, bg=BG)
        center.place(relx=.5, rely=.5, anchor="center")

        tk.Label(center, text="Правильні і неправильні дроби",
                 font=("Segoe UI", 44, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 4))
        tk.Label(center, text="§ 36",
                 font=("Segoe UI", 24), bg=BG, fg=ACCENT).pack(pady=(0, 28))

        cards = [
            ("📖", "Теорія",                     CARD_B,  ACCENT,  self.show_theory),
            ("🎯", "Правильний чи\nнеправильний?", CARD_G,  GREEN,   self.show_trainer_1),
            ("🎯", "Порівняй\nіз числом 1",       CARD_Y,  ORANGE,  self.show_trainer_2),
        ]
        row = tk.Frame(center, bg=BG)
        row.pack()
        for icon, title, bg_c, fg_c, cmd in cards:
            c = tk.Frame(row, bg=bg_c, width=230, height=200,
                         highlightbackground=BORDER, highlightthickness=2)
            c.pack(side="left", padx=16)
            c.pack_propagate(False)
            tk.Label(c, text=icon, font=("Segoe UI", 40),
                     bg=bg_c, fg=fg_c).pack(pady=(22, 4))
            tk.Label(c, text=title, font=("Segoe UI", 15, "bold"),
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
        p = self._scroll_page()

        tk.Label(p, text="Правильні і неправильні дроби",
                 font=F_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        hline(p, ACCENT)

        # ── Two-column definition cards ───────────────────────────────────
        two_col = tk.Frame(p, bg=BG)
        two_col.pack(fill="x", pady=8)

        # LEFT: правильний
        left_card = tk.Frame(two_col, bg=CARD_G, padx=22, pady=18,
                             highlightbackground=GREEN, highlightthickness=2)
        left_card.pack(side="left", fill="both", expand=True, padx=(0, 8))
        tk.Label(left_card, text="✅  Правильний дріб",
                 font=F_SUB, bg=CARD_G, fg=GREEN).pack(anchor="w")
        tk.Label(left_card,
                 text="Чисельник  <  знаменника",
                 font=F_BODYB, bg=CARD_G, fg=GREEN).pack(anchor="w", pady=(8, 4))
        tk.Label(left_card,
                 text="Правильний дріб завжди\nменший від 1",
                 font=F_BODY, bg=CARD_G, fg=TEXT).pack(anchor="w")

        # Examples row
        ex_row_l = tk.Frame(left_card, bg=CARD_G)
        ex_row_l.pack(anchor="w", pady=10)
        for n, d in [(3, 8), (1, 2), (5, 6), (2, 7)]:
            frac_w(ex_row_l, n, d, CARD_G, "small", GREEN).pack(side="left", padx=8)

        # Comparison: frac < 1
        cmp_l = tk.Frame(left_card, bg=CARD_G)
        cmp_l.pack(anchor="w", pady=4)
        frac_w(cmp_l, 3, 8, CARD_G, "small", GREEN).pack(side="left")
        tk.Label(cmp_l, text="  <  1", font=("Segoe UI", 22, "bold"),
                 bg=CARD_G, fg=GREEN).pack(side="left")

        # RIGHT: неправильний
        right_card = tk.Frame(two_col, bg=CARD_R, padx=22, pady=18,
                              highlightbackground=RED, highlightthickness=2)
        right_card.pack(side="right", fill="both", expand=True, padx=(8, 0))
        tk.Label(right_card, text="❌  Неправильний дріб",
                 font=F_SUB, bg=CARD_R, fg=RED).pack(anchor="w")
        tk.Label(right_card,
                 text="Чисельник  ≥  знаменника",
                 font=F_BODYB, bg=CARD_R, fg=RED).pack(anchor="w", pady=(8, 4))
        tk.Label(right_card,
                 text="Неправильний дріб завжди\nбільший від 1 або дорівнює 1",
                 font=F_BODY, bg=CARD_R, fg=TEXT).pack(anchor="w")

        ex_row_r = tk.Frame(right_card, bg=CARD_R)
        ex_row_r.pack(anchor="w", pady=10)
        for n, d in [(8, 8), (4, 3), (6, 5), (9, 4)]:
            frac_w(ex_row_r, n, d, CARD_R, "small", RED).pack(side="left", padx=8)

        cmp_r = tk.Frame(right_card, bg=CARD_R)
        cmp_r.pack(anchor="w", pady=4)
        frac_w(cmp_r, 9, 4, CARD_R, "small", RED).pack(side="left")
        tk.Label(cmp_r, text="  >  1", font=("Segoe UI", 22, "bold"),
                 bg=CARD_R, fg=RED).pack(side="left")

        # ── Rule: comparing to 1 ─────────────────────────────────────────
        rule_f = tk.Frame(p, bg=CARD_Y, padx=22, pady=18,
                          highlightbackground=BORDER, highlightthickness=1)
        rule_f.pack(fill="x", pady=8)
        tk.Label(rule_f, text="⚡  Три випадки: порівняння дробу з числом 1",
                 font=F_SUB, bg=CARD_Y, fg=ORANGE).pack(anchor="w", pady=(0, 10))

        cases = [
            (GREEN, "Чисельник < знаменника",  "правильний дріб",  " < 1", [(2, 5)]),
            (ORANGE,"Чисельник = знаменнику",  "= 1",              " = 1", [(5, 5)]),
            (RED,   "Чисельник > знаменника",  "неправильний дріб"," > 1", [(7, 4)]),
        ]
        for color, cond, name, rel, examples in cases:
            row = tk.Frame(rule_f, bg=CARD_Y, pady=6)
            row.pack(anchor="w")
            tk.Label(row, text=f"  {cond}  →  ",
                     font=F_BODY, bg=CARD_Y, fg=MUTED).pack(side="left")
            tk.Label(row, text=name + rel,
                     font=F_BODYB, bg=CARD_Y, fg=color).pack(side="left")
            tk.Label(row, text="     Наприклад: ", font=F_SMALL,
                     bg=CARD_Y, fg=MUTED).pack(side="left")
            for n, d in examples:
                frac_w(row, n, d, CARD_Y, "small", color).pack(side="left", padx=6)

        # ── Special case: 0 numerator ────────────────────────────────────
        zero_f = tk.Frame(p, bg=CARD_V, padx=22, pady=14,
                          highlightbackground=BORDER, highlightthickness=1)
        zero_f.pack(fill="x", pady=8)
        tk.Label(zero_f, text="⚡  Якщо чисельник = 0",
                 font=F_SUB, bg=CARD_V, fg=ACCENT2).pack(anchor="w")
        row_z = tk.Frame(zero_f, bg=CARD_V)
        row_z.pack(anchor="w", pady=8)
        for d in [5, 7, 17]:
            frac_w(row_z, 0, d, CARD_V, "small", ACCENT2).pack(side="left", padx=8)
        tk.Label(zero_f, text="Дріб з нульовим чисельником завжди дорівнює 0.",
                 font=F_BODY, bg=CARD_V, fg=TEXT).pack(anchor="w")

        # ── Visual: bar comparison ────────────────────────────────────────
        vis_f = tk.Frame(p, bg=PANEL, padx=22, pady=18,
                         highlightbackground=BORDER, highlightthickness=1)
        vis_f.pack(fill="x", pady=8)
        tk.Label(vis_f, text="⚡  Наочно: порівняйте дроби з цілим",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(anchor="w", pady=(0, 10))

        bar_examples = [
            (3, 8, GREEN,  "правильний"),
            (8, 8, ORANGE, "= 1"),
            (11, 8, RED,   "неправильний"),
        ]
        bar_row = tk.Frame(vis_f, bg=PANEL)
        bar_row.pack(anchor="w")
        for n, d, color, label in bar_examples:
            col = tk.Frame(bar_row, bg=PANEL, padx=12)
            col.pack(side="left")
            fr_row = tk.Frame(col, bg=PANEL)
            fr_row.pack()
            frac_w(fr_row, n, d, PANEL, "small", color).pack(side="left")
            tk.Label(fr_row, text=f"  ({label})",
                     font=F_SMALL, bg=PANEL, fg=color).pack(side="left")
            # For improper fraction > 1, show two rows: full + partial
            if n <= d:
                fraction_bar(col, n, d, bg_filled=color, bg_empty=BTN_NUM,
                             cell_w=40, cell_h=36, bg=PANEL).pack(pady=4)
            else:
                # First full row
                fraction_bar(col, d, d, bg_filled=color, bg_empty=BTN_NUM,
                             cell_w=40, cell_h=36, bg=PANEL).pack(pady=2)
                # Second partial row
                remainder = n - d
                fraction_bar(col, remainder, d, bg_filled=color, bg_empty=BTN_NUM,
                             cell_w=40, cell_h=36, bg=PANEL).pack(pady=2)
                tk.Label(col, text="(більше ніж одне ціле)",
                         font=F_SMALL, bg=PANEL, fg=RED).pack()

        # ── Number line ───────────────────────────────────────────────────
        nl_f = tk.Frame(p, bg=PANEL, padx=22, pady=18,
                        highlightbackground=BORDER, highlightthickness=1)
        nl_f.pack(fill="x", pady=8)
        tk.Label(nl_f, text="📐  На координатному промені (від 0 до 2)",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack(anchor="w")
        tk.Label(nl_f,
                 text="Правильні дроби — завжди лівіше від 1 (зелена зона).\n"
                      "Неправильні дроби — на позиції 1 або правіше (червона зона).",
                 font=F_BODY, bg=PANEL, fg=TEXT).pack(anchor="w", pady=(6, 12))

        marks = [
            (3, 8, GREEN,  "³⁄₈"),
            (5, 8, GREEN,  "⁵⁄₈"),
            (8, 8, ORANGE, "⁸⁄₈=1"),
            (11, 8, RED,   "¹¹⁄₈"),
            (14, 8, RED,   "¹⁴⁄₈"),
        ]
        nl = number_line_ext(nl_f, marks, bg=PANEL, width=self.SW - 180)
        nl.pack(fill="x")

        theory_card(p, "💡  Запам'ятай",
                    "Правильний дріб:    чисельник < знаменника   →   дріб < 1\n"
                    "Неправильний дріб:  чисельник ≥ знаменника   →   дріб ≥ 1\n\n"
                    "Правильний дріб завжди менший від будь-якого неправильного дробу.",
                    "#f1f5f9", MUTED)

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER 1 — Proper or improper?
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
        tk.Label(sbar, text="Правильний чи неправильний?",
                 font=("Segoe UI", 15, "bold"), bg=PANEL, fg=MUTED).pack(
            side="left", padx=10)
        tk.Label(sbar, text="Дивись: чисельник vs знаменник",
                 font=("Segoe UI", 14, "bold"), bg=PANEL, fg=ACCENT).pack(
            side="right", padx=24)

        center = tk.Frame(cf, bg=BG)
        center.pack(expand=True)

        # Fraction display
        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=36, pady=18)
        task_f.pack(pady=(18, 10))
        tk.Label(task_f, text="Визнач тип дробу:",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack()
        self.t1_frac_frame = tk.Frame(task_f, bg=PANEL)
        self.t1_frac_frame.pack(pady=10)

        # Bar diagram
        self.t1_bar_frame = tk.Frame(center, bg=BG)
        self.t1_bar_frame.pack(pady=6)

        # Two answer buttons
        btns_f = tk.Frame(center, bg=BG)
        btns_f.pack(pady=14)

        self.t1_proper_btn = tk.Button(
            btns_f,
            text="✅  ПРАВИЛЬНИЙ\n(чисельник < знаменника)",
            font=("Segoe UI", 20, "bold"),
            width=24, height=3,
            bg=CARD_G, fg=GREEN,
            relief="flat", cursor="hand2",
            command=lambda: self._t1_answer("proper"))
        self.t1_proper_btn.pack(side="left", padx=20)

        self.t1_improper_btn = tk.Button(
            btns_f,
            text="❌  НЕПРАВИЛЬНИЙ\n(чисельник ≥ знаменника)",
            font=("Segoe UI", 20, "bold"),
            width=24, height=3,
            bg=CARD_R, fg=RED,
            relief="flat", cursor="hand2",
            command=lambda: self._t1_answer("improper"))
        self.t1_improper_btn.pack(side="left", padx=20)

        # Feedback
        self.t1_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                     bg=BG, fg=ORANGE,
                                     wraplength=700, justify="center")
        self.t1_feed_lbl.pack(pady=6)

        # Number line (shown after answer)
        self.t1_nl_frame = tk.Frame(center, bg=BG)
        self.t1_nl_frame.pack(fill="x", padx=40, pady=4)

        mkbtn(center, "▶  Наступне", self._t1_new,
              bg=ACCENT, w=14, h=2).pack(pady=8)

        self._t1_new()

    def _t1_score_text(self):
        return f"Правильно: {self.t1_score}  /  Завдань: {self.t1_attempts}"

    def _t1_new(self):
        self.t1_answered = False
        # Mix: 40% proper, 40% improper, 20% = 1 (equal num/den)
        roll = random.random()
        d = random.randint(2, 12)
        if roll < 0.4:
            n = random.randint(1, d - 1)        # proper
        elif roll < 0.8:
            n = random.randint(d + 1, d + d)    # improper > 1
        else:
            n = d                                # = 1
        self.t1_n, self.t1_d = n, d
        self.t1_attempts += 1

        for w in self.t1_frac_frame.winfo_children():
            w.destroy()
        # Neutral color before answer
        frac_w(self.t1_frac_frame, n, d, PANEL, "big", ACCENT).pack()

        # Rebuild bar — neutral grey before answer
        for w in self.t1_bar_frame.winfo_children():
            w.destroy()
        bar_d = min(d, 12)
        bar_n = min(n, bar_d)
        fraction_bar(self.t1_bar_frame, bar_n, bar_d,
                     bg_filled=BTN_NUM, bg_empty=BTN_NUM,
                     cell_w=48, cell_h=42, bg=BG).pack()

        # Reset UI
        if self.t1_feed_lbl:
            self.t1_feed_lbl.config(text="")
        for w in self.t1_nl_frame.winfo_children():
            w.destroy()
        for b in [self.t1_proper_btn, self.t1_improper_btn]:
            b.config(state="normal")
        self.t1_proper_btn.config(bg=CARD_G, fg=GREEN)
        self.t1_improper_btn.config(bg=CARD_R, fg=RED)
        if self.t1_score_lbl:
            self.t1_score_lbl.config(text=self._t1_score_text())

    def _t1_answer(self, ans):
        if self.t1_answered:
            return
        self.t1_answered = True
        n, d = self.t1_n, self.t1_d
        is_proper = (n < d)
        correct = "proper" if is_proper else "improper"
        color = GREEN if n < d else (ORANGE if n == d else RED)

        # Now reveal the correct colour on fraction + bar
        for w in self.t1_frac_frame.winfo_children():
            w.destroy()
        frac_w(self.t1_frac_frame, n, d, PANEL, "big", color).pack()
        self.t1_frac_frame.update()

        for w in self.t1_bar_frame.winfo_children():
            w.destroy()
        bar_d = min(d, 12)
        bar_n = min(n, bar_d)
        fraction_bar(self.t1_bar_frame, bar_n, bar_d,
                     bg_filled=color, bg_empty=BTN_NUM,
                     cell_w=48, cell_h=42, bg=BG).pack()
        self.t1_bar_frame.update()

        if ans == correct:
            self.t1_score += 1
            if is_proper:
                msg = f"🎉  Правильно!  {n}/{d} — ПРАВИЛЬНИЙ дріб   ({n} < {d},  тому < 1)"
                self.t1_proper_btn.config(bg=GREEN_LT, fg=GREEN)
            elif n == d:
                msg = f"🎉  Правильно!  {n}/{d} — НЕПРАВИЛЬНИЙ дріб  ({n} = {d},  тому = 1)"
                self.t1_improper_btn.config(bg=GREEN_LT, fg=GREEN)
            else:
                msg = f"🎉  Правильно!  {n}/{d} — НЕПРАВИЛЬНИЙ дріб  ({n} > {d},  тому > 1)"
                self.t1_improper_btn.config(bg=GREEN_LT, fg=GREEN)
            if self.t1_feed_lbl:
                self.t1_feed_lbl.config(text=msg, fg=GREEN)
        else:
            if is_proper:
                msg = (f"❌  Ні!  {n}/{d} — ПРАВИЛЬНИЙ дріб   "
                       f"({n} < {d},  значить < 1)")
                self.t1_proper_btn.config(bg=GREEN_LT, fg=GREEN)
                self.t1_improper_btn.config(bg=RED_LT,  fg=RED)
            else:
                rel = "=" if n == d else ">"
                msg = (f"❌  Ні!  {n}/{d} — НЕПРАВИЛЬНИЙ дріб   "
                       f"({n} {rel} {d},  значить {'= 1' if n==d else '> 1'})")
                self.t1_improper_btn.config(bg=GREEN_LT, fg=GREEN)
                self.t1_proper_btn.config(bg=RED_LT, fg=RED)
            if self.t1_feed_lbl:
                self.t1_feed_lbl.config(text=msg, fg=RED)

        for b in [self.t1_proper_btn, self.t1_improper_btn]:
            b.config(state="disabled")

        # Show number line after answer
        marks = [(n, d, GREEN if is_proper else (ORANGE if n == d else RED),
                  f"{n}/{d}")]
        nl = number_line_ext(self.t1_nl_frame, marks, bg=BG,
                             width=self.SW - 100)
        nl.pack(fill="x")

        if self.t1_score_lbl:
            self.t1_score_lbl.config(text=self._t1_score_text())

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER 2 — Compare fraction with 1: choose  < 1 / = 1 / > 1
    # ══════════════════════════════════════════════════════════════════════════
    def show_trainer_2(self):
        self.clear_main()
        self.mode = "trainer2"
        self.t2_answered = False

        cf = self.current_frame
        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.t2_score_lbl = tk.Label(sbar,
            text=self._t2_score_text(), font=F_SCORE, bg=PANEL, fg=GREEN)
        self.t2_score_lbl.pack(side="left", padx=30)
        tk.Label(sbar, text="Порівняй дріб з числом 1",
                 font=("Segoe UI", 15, "bold"), bg=PANEL, fg=MUTED).pack(
            side="left", padx=10)

        center = tk.Frame(cf, bg=BG)
        center.pack(expand=True)

        # Fraction display
        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=36, pady=18)
        task_f.pack(pady=(18, 6))

        cmp_row = tk.Frame(task_f, bg=PANEL)
        cmp_row.pack()
        self.t2_frac_frame = tk.Frame(cmp_row, bg=PANEL)
        self.t2_frac_frame.pack(side="left")
        self.t2_sign_lbl = tk.Label(cmp_row, text="  ?  ",
                                     font=F_SIGN, bg=PANEL, fg=BTN_NUM)
        self.t2_sign_lbl.pack(side="left")
        tk.Label(cmp_row, text="1", font=F_SIGN, bg=PANEL, fg=TEXT).pack(side="left")

        # Bar diagram
        self.t2_bar_frame = tk.Frame(center, bg=BG)
        self.t2_bar_frame.pack(pady=6)

        # Three answer buttons
        btns_f = tk.Frame(center, bg=BG)
        btns_f.pack(pady=14)

        btn_data = [
            ("<  1", "lt", RED,    CARD_R),
            ("=  1", "eq", ORANGE, CARD_Y),
            (">  1", "gt", GREEN,  CARD_G),
        ]
        self.t2_answer_btns = {}
        for label, key, fg_c, bg_c in btn_data:
            b = tk.Button(btns_f,
                          text=label,
                          font=("Segoe UI", 32, "bold"),
                          width=6, height=2,
                          bg=bg_c, fg=fg_c,
                          relief="flat", cursor="hand2",
                          command=lambda k=key: self._t2_answer(k))
            b.pack(side="left", padx=16)
            self.t2_answer_btns[key] = (b, bg_c, fg_c)

        # Feedback
        self.t2_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                     bg=BG, fg=ORANGE,
                                     wraplength=700, justify="center")
        self.t2_feed_lbl.pack(pady=6)

        # Number line
        self.t2_nl_frame = tk.Frame(center, bg=BG)
        self.t2_nl_frame.pack(fill="x", padx=40, pady=4)

        mkbtn(center, "▶  Наступне", self._t2_new,
              bg=ACCENT, w=14, h=2).pack(pady=8)

        self._t2_new()

    def _t2_score_text(self):
        return f"Правильно: {self.t2_score}  /  Завдань: {self.t2_attempts}"

    def _t2_new(self):
        self.t2_answered = False
        d = random.randint(2, 12)
        roll = random.random()
        if roll < 0.4:
            n = random.randint(1, d - 1)
        elif roll < 0.7:
            n = random.randint(d + 1, d + d)
        else:
            n = d
        self.t2_n, self.t2_d = n, d
        self.t2_attempts += 1

        for w in self.t2_frac_frame.winfo_children():
            w.destroy()
        # Neutral colour before answer
        frac_w(self.t2_frac_frame, n, d, PANEL, "big", ACCENT).pack()

        if self.t2_sign_lbl:
            self.t2_sign_lbl.config(text="  ?  ", fg=BTN_NUM)

        for w in self.t2_bar_frame.winfo_children():
            w.destroy()
        bar_d = min(d, 12)
        bar_n = min(n, bar_d)
        fraction_bar(self.t2_bar_frame, bar_n, bar_d,
                     bg_filled=BTN_NUM, bg_empty=BTN_NUM,
                     cell_w=48, cell_h=42, bg=BG).pack()

        if self.t2_feed_lbl:
            self.t2_feed_lbl.config(text="")
        for w in self.t2_nl_frame.winfo_children():
            w.destroy()
        for key, (b, bg_c, fg_c) in self.t2_answer_btns.items():
            b.config(state="normal", bg=bg_c, fg=fg_c)
        if self.t2_score_lbl:
            self.t2_score_lbl.config(text=self._t2_score_text())

    def _t2_answer(self, key):
        if self.t2_answered:
            return
        self.t2_answered = True
        n, d = self.t2_n, self.t2_d

        correct_key = "lt" if n < d else ("eq" if n == d else "gt")
        sign_text   = "<" if n < d else ("=" if n == d else ">")
        sign_color  = RED if n < d else (ORANGE if n == d else GREEN)
        reveal_color = sign_color  # same logic

        # Reveal colour on fraction and bar NOW that answer is given
        for w in self.t2_frac_frame.winfo_children():
            w.destroy()
        frac_w(self.t2_frac_frame, n, d, PANEL, "big", reveal_color).pack()
        self.t2_frac_frame.update()

        for w in self.t2_bar_frame.winfo_children():
            w.destroy()
        bar_d = min(d, 12)
        bar_n = min(n, bar_d)
        fraction_bar(self.t2_bar_frame, bar_n, bar_d,
                     bg_filled=reveal_color, bg_empty=BTN_NUM,
                     cell_w=48, cell_h=42, bg=BG).pack()
        self.t2_bar_frame.update()

        if self.t2_sign_lbl:
            self.t2_sign_lbl.config(text=f"  {sign_text}  ", fg=sign_color)

        if key == correct_key:
            self.t2_score += 1
            msg = (f"🎉  Правильно!   {n}/{d}  {sign_text}  1   "
                   f"(бо {n} {sign_text} {d})")
            msg_color = GREEN
            # Highlight correct button green
            b, bg_c, fg_c = self.t2_answer_btns[key]
            b.config(bg=GREEN_LT, fg=GREEN)
        else:
            msg = (f"❌  Ні!   Правильно:   {n}/{d}  {sign_text}  1   "
                   f"(бо {n} {sign_text} {d})")
            msg_color = RED
            # Show correct in green, wrong in red
            for k, (b, bg_c, fg_c) in self.t2_answer_btns.items():
                if k == correct_key:
                    b.config(bg=GREEN_LT, fg=GREEN)
                elif k == key:
                    b.config(bg=RED_LT, fg=RED)

        if self.t2_feed_lbl:
            self.t2_feed_lbl.config(text=msg, fg=msg_color)

        for k, (b, bg_c, fg_c) in self.t2_answer_btns.items():
            b.config(state="disabled")

        # Number line
        marks = [(n, d, sign_color, f"{n}/{d}")]
        nl = number_line_ext(self.t2_nl_frame, marks, bg=BG,
                             width=self.SW - 100)
        nl.pack(fill="x")

        if self.t2_score_lbl:
            self.t2_score_lbl.config(text=self._t2_score_text())


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
