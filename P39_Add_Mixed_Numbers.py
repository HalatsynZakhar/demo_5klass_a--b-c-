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
TEAL      = "#0f766e"
TEAL_LT   = "#ccfbf1"

# Per-circle colours for addends
C1 = "#3b82f6"   # blue  – перший доданок
C2 = "#f97316"   # orange – другий доданок / від'ємник
C_ANS_OK  = "#16a34a"   # green  – правильна відповідь
C_ANS_BAD = "#dc2626"   # red    – неправильна відповідь
C_EMPTY   = "#e2e8f0"   # light grey – пуста частина кола

# ── Fonts ─────────────────────────────────────────────────────────────────────
F_TITLE  = ("Segoe UI", 34, "bold")
F_HEAD   = ("Segoe UI", 26, "bold")
F_SUB    = ("Segoe UI", 20, "bold")
F_BODY   = ("Segoe UI", 17)
F_BODYB  = ("Segoe UI", 17, "bold")
F_BIG    = ("Segoe UI", 60, "bold")
F_BTN    = ("Segoe UI", 19, "bold")
F_NAV    = ("Segoe UI", 14, "bold")
F_SCORE  = ("Segoe UI", 20, "bold")
F_FEED   = ("Segoe UI", 18, "bold")
F_NUM    = ("Segoe UI", 26, "bold")
F_SMALL  = ("Segoe UI", 13)
F_FRAC   = ("Segoe UI", 38, "bold")
F_FRAC_S = ("Segoe UI", 24, "bold")
F_MIXED  = ("Segoe UI", 38, "bold")
F_STEP   = ("Segoe UI", 18, "bold")
F_STEP_V = ("Segoe UI", 18)
F_CTRL   = ("Segoe UI", 28, "bold")   # +/- buttons


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
    tk.Label(f, text=title, font=F_SUB, bg=bg_c, fg=fg_title, anchor="w").pack(fill="x")
    tk.Label(f, text=body, font=F_BODY, bg=bg_c, fg=TEXT,
             justify="left", wraplength=1300, anchor="w").pack(fill="x", pady=(6, 0))
    return f


# ── Visual fraction / mixed widgets ──────────────────────────────────────────
def frac_w(parent, n, d, bg=PANEL, size="big", color=ACCENT):
    sizes  = {"big": F_FRAC,  "small": F_FRAC_S}
    widths = {"big": 66,      "small": 46}
    fn, bw = sizes.get(size, F_FRAC_S), widths.get(size, 46)
    f = tk.Frame(parent, bg=bg)
    tk.Label(f, text=str(n), font=fn, bg=bg, fg=color).pack()
    tk.Frame(f, bg=color, height=3, width=bw).pack(pady=2)
    tk.Label(f, text=str(d), font=fn, bg=bg, fg=color).pack()
    return f


def mixed_w(parent, whole, n, d, bg=PANEL, size="big",
            color_whole=TEXT, color_frac=ACCENT):
    sizes  = {"big": F_FRAC,  "small": F_FRAC_S}
    wmixed = {"big": F_MIXED, "small": ("Segoe UI", 24, "bold")}
    widths = {"big": 66,      "small": 46}
    fn, wn, bw = sizes.get(size), wmixed.get(size), widths.get(size)
    frame = tk.Frame(parent, bg=bg)
    tk.Label(frame, text=str(whole), font=wn, bg=bg, fg=color_whole).pack(
        side="left", padx=(0, 4))
    frac_part = tk.Frame(frame, bg=bg)
    frac_part.pack(side="left")
    tk.Label(frac_part, text=str(n), font=fn, bg=bg, fg=color_frac).pack()
    tk.Frame(frac_part, bg=color_frac, height=3, width=bw).pack(pady=2)
    tk.Label(frac_part, text=str(d), font=fn, bg=bg, fg=color_frac).pack()
    return frame


def num_w(parent, n, bg=PANEL, size="big", color=TEXT):
    """Plain natural number widget (same height as fraction)."""
    fn = F_FRAC if size == "big" else F_FRAC_S
    f = tk.Frame(parent, bg=bg)
    tk.Label(f, text=str(n), font=fn, bg=bg, fg=color).pack(pady=10)
    return f


# ── Pie-circle canvas (pure tkinter, no matplotlib) ──────────────────────────
def draw_pie_circles(parent, numer, denom, color=C1,
                     radius=46, bg=PANEL, max_circles=7):
    """
    Draw numer/denom as filled pie slices across multiple circles.
    Whole circles first, then partial remainder.
    Returns the Canvas widget.
    """
    if denom <= 0:
        return tk.Canvas(parent, bg=bg, width=0, height=0, highlightthickness=0)
    whole = numer // denom
    rem   = numer % denom
    circles = [denom] * whole + ([rem] if rem > 0 else [])
    if not circles:
        circles = [0]   # show one empty circle for zero

    # cap display circles to avoid overflow on very large numbers
    circles = circles[:max_circles]

    pad = 10
    W = len(circles) * (radius * 2 + pad) + pad
    H = radius * 2 + pad * 2
    cv = tk.Canvas(parent, bg=bg, width=W, height=H, highlightthickness=0)

    for idx, filled in enumerate(circles):
        cx = pad + radius + idx * (radius * 2 + pad)
        cy = H // 2
        # background
        cv.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                       fill=C_EMPTY, outline=MUTED, width=2)
        if filled > 0:
            if filled == denom:
                # Full circle — fill with solid oval (arc extent=360 renders empty in tkinter)
                cv.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                               fill=color, outline=bg, width=1)
            else:
                step = 360.0 / denom
                for s in range(min(filled, denom)):
                    start = 90 - s * step
                    cv.create_arc(cx - radius, cy - radius, cx + radius, cy + radius,
                                  start=start, extent=-step,
                                  fill=color, outline=bg, width=1, style="pieslice")
        # divider lines
        for s in range(denom):
            angle = math.radians(90 - s * 360 / denom)
            cv.create_line(cx, cy,
                           cx + radius * math.cos(angle),
                           cy - radius * math.sin(angle),
                           fill=MUTED, width=1)
        # outline ring
        cv.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                       fill="", outline=MUTED, width=2)
    return cv


# ── +/− control row (no keyboard, mouse-only) ────────────────────────────────
def make_ctrl_row(parent, label, intvar, lo, hi, color, on_change_fn, bg=PANEL):
    """Returns frame with label + − [value] + buttons."""
    frame = tk.Frame(parent, bg=bg)
    tk.Label(frame, text=label, font=F_BODYB, bg=bg, fg=color,
             width=20, anchor="w").pack(side="left")

    def dec():
        v = intvar.get()
        if v > lo:
            intvar.set(v - 1)
            on_change_fn()

    def inc():
        v = intvar.get()
        if v < hi:
            intvar.set(v + 1)
            on_change_fn()

    b_m = tk.Button(frame, text="−", font=F_CTRL, width=3, height=1,
                    bg=BTN_NUM, fg=TEXT, relief="flat", cursor="hand2",
                    command=dec)
    b_m.pack(side="left", padx=6)

    val_lbl = tk.Label(frame, textvariable=intvar,
                       font=("Segoe UI", 32, "bold"),
                       bg=bg, fg=color, width=4)
    val_lbl.pack(side="left")

    b_p = tk.Button(frame, text="+", font=F_CTRL, width=3, height=1,
                    bg=BTN_NUM, fg=TEXT, relief="flat", cursor="hand2",
                    command=inc)
    b_p.pack(side="left", padx=6)
    return frame, b_m, b_p


# ══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("§ 38. Додавання та віднімання дробів і мішаних чисел")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()
        self.current_frame = None
        self.mode = None

        # ── Practice state ────────────────────────────────────────────────
        self.op        = "+"          # "+" or "−"
        self.task_type = "frac"       # "frac" | "mixed"
        # task values (stored as improper numerators over common d)
        self.t_n1 = self.t_n2 = 0
        self.t_d  = 1
        # user answer vars
        self.u_whole = tk.IntVar(value=0)
        self.u_num   = tk.IntVar(value=0)
        self.u_den   = tk.IntVar(value=1)
        # correct answer (improper form)
        self.correct_n = 0
        self.correct_d = 1
        # UI refs
        self.score = self.attempts = 0
        self.score_lbl    = None
        self.task_frame   = None      # holds task expression widgets
        self.pie1_frame   = None
        self.pie2_frame   = None
        self.pie_ans_frame = None
        self.feed_lbl     = None
        self.next_btn     = None
        self.ctrl_whole   = None
        self.ctrl_num     = None
        self.ctrl_den     = None

        self._build_chrome()
        self.show_main_menu()

    # ── Chrome ────────────────────────────────────────────────────────────────
    def _build_chrome(self):
        hdr = tk.Frame(self, bg=HDR_BG, height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr,
                 text="§ 38.   Додавання та віднімання дробів і мішаних чисел",
                 bg=HDR_BG, fg=WHITE,
                 font=("Segoe UI", 20, "bold")).pack(side="left", padx=30)
        mkbtn(hdr, "✕  Вийти", self.destroy, bg="#b91c1c",
              font=("Segoe UI", 13, "bold"), w=9, h=1).pack(
            side="right", padx=18, pady=16)

        nav = tk.Frame(self, bg=NAV_BG, height=52)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        for label, cmd in [
            ("🏠  Меню",        self.show_main_menu),
            ("📖  Теорія",      self.show_theory),
            ("🎯  Практика",    self.show_practice),
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

        tk.Label(center,
                 text="Додавання та віднімання",
                 font=("Segoe UI", 46, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 4))
        tk.Label(center,
                 text="дробів і мішаних чисел   §38",
                 font=("Segoe UI", 24), bg=BG, fg=ACCENT).pack(pady=(0, 28))

        cards = [
            ("📖", "Теорія",   CARD_B, ACCENT, self.show_theory),
            ("🎯", "Практика", CARD_G, GREEN,  self.show_practice),
        ]
        row = tk.Frame(center, bg=BG)
        row.pack()
        for icon, title, bg_c, fg_c, cmd in cards:
            c = tk.Frame(row, bg=bg_c, width=240, height=210,
                         highlightbackground=BORDER, highlightthickness=2)
            c.pack(side="left", padx=20)
            c.pack_propagate(False)
            tk.Label(c, text=icon, font=("Segoe UI", 44),
                     bg=bg_c, fg=fg_c).pack(pady=(24, 4))
            tk.Label(c, text=title, font=("Segoe UI", 18, "bold"),
                     bg=bg_c, fg=fg_c).pack()
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

        tk.Label(p, text="Додавання та віднімання дробів і мішаних чисел",
                 font=F_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        hline(p, ACCENT)

        # ── Rule: addition ────────────────────────────────────────────────
        add_f = tk.Frame(p, bg=CARD_B, padx=22, pady=18,
                         highlightbackground=ACCENT, highlightthickness=2)
        add_f.pack(fill="x", pady=8)
        tk.Label(add_f, text="➕  Додавання дробів з однаковими знаменниками",
                 font=F_SUB, bg=CARD_B, fg=ACCENT).pack(anchor="w")
        tk.Label(add_f,
                 text="Знаменник залишається.  Чисельники ДОДАЮТЬСЯ.",
                 font=F_BODYB, bg=CARD_B, fg=TEXT).pack(anchor="w", pady=(8, 4))

        # Visual: 1/4 + 2/4 = 3/4
        ex1_row = tk.Frame(add_f, bg=CARD_B)
        ex1_row.pack(anchor="w", pady=8)
        frac_w(ex1_row, 1, 4, CARD_B, "big", ACCENT).pack(side="left")
        tk.Label(ex1_row, text="  +  ", font=F_BIG, bg=CARD_B, fg=TEXT).pack(side="left")
        frac_w(ex1_row, 2, 4, CARD_B, "big", ACCENT2).pack(side="left")
        tk.Label(ex1_row, text="  =  ", font=F_BIG, bg=CARD_B, fg=TEXT).pack(side="left")
        frac_w(ex1_row, 3, 4, CARD_B, "big", GREEN).pack(side="left")
        tk.Label(ex1_row, text="    (1 + 2 = 3,  знаменник 4 незмінний)",
                 font=F_BODY, bg=CARD_B, fg=MUTED).pack(side="left", padx=16)

        pie_row1 = tk.Frame(add_f, bg=CARD_B)
        pie_row1.pack(anchor="w", pady=6)
        draw_pie_circles(pie_row1, 1, 4, C1,    radius=42, bg=CARD_B).pack(side="left", padx=8)
        tk.Label(pie_row1, text="+", font=F_HEAD, bg=CARD_B, fg=MUTED).pack(side="left")
        draw_pie_circles(pie_row1, 2, 4, C2,    radius=42, bg=CARD_B).pack(side="left", padx=8)
        tk.Label(pie_row1, text="=", font=F_HEAD, bg=CARD_B, fg=MUTED).pack(side="left")
        draw_pie_circles(pie_row1, 3, 4, C_ANS_OK, radius=42, bg=CARD_B).pack(side="left", padx=8)

        # ── Rule: subtraction ─────────────────────────────────────────────
        sub_f = tk.Frame(p, bg=CARD_R, padx=22, pady=18,
                         highlightbackground=RED, highlightthickness=2)
        sub_f.pack(fill="x", pady=8)
        tk.Label(sub_f, text="➖  Віднімання дробів з однаковими знаменниками",
                 font=F_SUB, bg=CARD_R, fg=RED).pack(anchor="w")
        tk.Label(sub_f,
                 text="Знаменник залишається.  Чисельники ВІДНІМАЮТЬСЯ.",
                 font=F_BODYB, bg=CARD_R, fg=TEXT).pack(anchor="w", pady=(8, 4))

        ex2_row = tk.Frame(sub_f, bg=CARD_R)
        ex2_row.pack(anchor="w", pady=8)
        frac_w(ex2_row, 5, 8, CARD_R, "big", ACCENT).pack(side="left")
        tk.Label(ex2_row, text="  −  ", font=F_BIG, bg=CARD_R, fg=TEXT).pack(side="left")
        frac_w(ex2_row, 3, 8, CARD_R, "big", ACCENT2).pack(side="left")
        tk.Label(ex2_row, text="  =  ", font=F_BIG, bg=CARD_R, fg=TEXT).pack(side="left")
        frac_w(ex2_row, 2, 8, CARD_R, "big", RED).pack(side="left")
        tk.Label(ex2_row, text="    (5 − 3 = 2,  знаменник 8 незмінний)",
                 font=F_BODY, bg=CARD_R, fg=MUTED).pack(side="left", padx=16)

        pie_row2 = tk.Frame(sub_f, bg=CARD_R)
        pie_row2.pack(anchor="w", pady=6)
        draw_pie_circles(pie_row2, 5, 8, C1,    radius=42, bg=CARD_R).pack(side="left", padx=8)
        tk.Label(pie_row2, text="−", font=F_HEAD, bg=CARD_R, fg=MUTED).pack(side="left")
        draw_pie_circles(pie_row2, 3, 8, C2,    radius=42, bg=CARD_R).pack(side="left", padx=8)
        tk.Label(pie_row2, text="=", font=F_HEAD, bg=CARD_R, fg=MUTED).pack(side="left")
        draw_pie_circles(pie_row2, 2, 8, RED,   radius=42, bg=CARD_R).pack(side="left", padx=8)

        # ── Mixed numbers: addition ───────────────────────────────────────
        carry_f = tk.Frame(p, bg=CARD_G, padx=22, pady=18,
                           highlightbackground=GREEN, highlightthickness=2)
        carry_f.pack(fill="x", pady=8)
        tk.Label(carry_f, text="🔢  Додавання мішаних чисел",
                 font=F_SUB, bg=CARD_G, fg=GREEN).pack(anchor="w")

        for step, color, txt in [
            ("Крок 1", ACCENT,
             "Цілі частини + цілі частини,  дробові + дробові  (знаменник спільний)"),
            ("Крок 2", GREEN,
             "Якщо дробова частина стала неправильним дробом (чисельник ≥ знаменника) —\n"
             "     виділяємо з неї цілу частину і додаємо до цілих"),
        ]:
            row = tk.Frame(carry_f, bg=CARD_G)
            row.pack(anchor="w", pady=4)
            tk.Label(row, text=f"  {step}:  ", font=F_STEP, bg=CARD_G,
                     fg=color, width=10, anchor="w").pack(side="left")
            tk.Label(row, text=txt, font=F_STEP_V, bg=CARD_G, fg=TEXT,
                     justify="left", wraplength=1200).pack(side="left")

        # Example A: no carry  →  1²⁄₇ + 3¹⁄₇ = 4³⁄₇
        ex_add_a = tk.Frame(carry_f, bg=PANEL, padx=16, pady=12,
                            highlightbackground=BORDER, highlightthickness=1)
        ex_add_a.pack(fill="x", pady=(8, 4))
        tk.Label(ex_add_a, text="Приклад А  (без переходу через ціле):",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(anchor="w")

        for label, color, calc, explain in [
            ("Крок 1", ACCENT,
             "1 + 3 = 4   та   2 + 1 = 3",
             "Цілі окремо, дробові окремо"),
            ("Крок 2", GREEN,
             "3/7 — правильний дріб (3 < 7)",
             "Нічого виділяти не треба"),
        ]:
            r = tk.Frame(ex_add_a, bg=CARD_G, padx=14, pady=7,
                         highlightbackground=BORDER, highlightthickness=1)
            r.pack(fill="x", pady=3)
            tk.Label(r, text=label, font=F_STEP, bg=CARD_G, fg=color,
                     width=8, anchor="w").pack(side="left")
            tk.Label(r, text=calc, font=("Segoe UI", 18, "bold"),
                     bg=CARD_G, fg=color).pack(side="left", padx=12)
            tk.Label(r, text=f"({explain})", font=F_SMALL,
                     bg=CARD_G, fg=MUTED).pack(side="left")

        ra = tk.Frame(ex_add_a, bg=PANEL)
        ra.pack(anchor="w", pady=8)
        mixed_w(ra, 1, 2, 7, PANEL, "big", TEXT, ACCENT).pack(side="left")
        tk.Label(ra, text="  +  ", font=F_HEAD, bg=PANEL, fg=TEXT).pack(side="left")
        mixed_w(ra, 3, 1, 7, PANEL, "big", TEXT, ACCENT2).pack(side="left")
        tk.Label(ra, text="  =  ", font=F_HEAD, bg=PANEL, fg=TEXT).pack(side="left")
        mixed_w(ra, 4, 3, 7, PANEL, "big", GREEN, GREEN).pack(side="left")

        # Example B: with carry  →  1³⁄₅ + 2⁴⁄₅ = ?
        # Step 1: 1+2=3 цілих,  3+4=7 → 7/5 неправильний
        # Step 2: 7/5 = 1 і 2/5 → цілих 3+1=4, дробова 2/5
        ex_add_b = tk.Frame(carry_f, bg=PANEL, padx=16, pady=12,
                            highlightbackground=BORDER, highlightthickness=1)
        ex_add_b.pack(fill="x", pady=(4, 8))
        tk.Label(ex_add_b, text="Приклад Б  (дробові частини дають неправильний дріб):",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(anchor="w")

        for label, color, calc, explain in [
            ("Крок 1", ACCENT,
             "1 + 2 = 3   та   3 + 4 = 7",
             "Цілі: 3.  Дробові: 7/5"),
            ("Крок 2", GREEN,
             "7/5 = 1 і 2/5   →   3 + 1 = 4  цілих,   дробова = 2/5",
             "7 ≥ 5 → виділяємо 1 цілу з дробової"),
        ]:
            r = tk.Frame(ex_add_b, bg=CARD_G, padx=14, pady=7,
                         highlightbackground=BORDER, highlightthickness=1)
            r.pack(fill="x", pady=3)
            tk.Label(r, text=label, font=F_STEP, bg=CARD_G, fg=color,
                     width=8, anchor="w").pack(side="left")
            tk.Label(r, text=calc, font=("Segoe UI", 18, "bold"),
                     bg=CARD_G, fg=color).pack(side="left", padx=12)
            tk.Label(r, text=f"({explain})", font=F_SMALL,
                     bg=CARD_G, fg=MUTED).pack(side="left")

        rb = tk.Frame(ex_add_b, bg=PANEL)
        rb.pack(anchor="w", pady=8)
        mixed_w(rb, 1, 3, 5, PANEL, "big", TEXT, ACCENT).pack(side="left")
        tk.Label(rb, text="  +  ", font=F_HEAD, bg=PANEL, fg=TEXT).pack(side="left")
        mixed_w(rb, 2, 4, 5, PANEL, "big", TEXT, ACCENT2).pack(side="left")
        tk.Label(rb, text="  =  ", font=F_HEAD, bg=PANEL, fg=TEXT).pack(side="left")
        # intermediate: 3 і 7/5
        mixed_w(rb, 3, 7, 5, PANEL, "big", ORANGE, ORANGE).pack(side="left")
        tk.Label(rb, text="  =  ", font=F_HEAD, bg=PANEL, fg=TEXT).pack(side="left")
        mixed_w(rb, 4, 2, 5, PANEL, "big", GREEN, GREEN).pack(side="left")

        pie_rb = tk.Frame(ex_add_b, bg=PANEL)
        pie_rb.pack(anchor="w", pady=6)
        draw_pie_circles(pie_rb, 8,  5, C1,       radius=34, bg=PANEL).pack(side="left", padx=6)
        tk.Label(pie_rb, text="+", font=F_HEAD, bg=PANEL, fg=MUTED).pack(side="left")
        draw_pie_circles(pie_rb, 14, 5, C2,       radius=34, bg=PANEL).pack(side="left", padx=6)
        tk.Label(pie_rb, text="=", font=F_HEAD, bg=PANEL, fg=MUTED).pack(side="left")
        draw_pie_circles(pie_rb, 22, 5, C_ANS_OK, radius=34, bg=PANEL).pack(side="left", padx=6)

        # ── Mixed numbers: subtraction ────────────────────────────────────
        sub_mix_f = tk.Frame(p, bg=CARD_V, padx=22, pady=18,
                             highlightbackground=ACCENT2, highlightthickness=2)
        sub_mix_f.pack(fill="x", pady=8)
        tk.Label(sub_mix_f, text="🔢  Віднімання мішаних чисел",
                 font=F_SUB, bg=CARD_V, fg=ACCENT2).pack(anchor="w")

        for step, color, txt in [
            ("Крок 1", ACCENT,
             "Перевіряємо: чисельник зменшуваного ≥ чисельника від'ємника?\n"
             "     Якщо ні — «позичаємо» 1 цілу зі зменшуваного:\n"
             "     додаємо знаменник до чисельника дробової частини  і  зменшуємо цілу на 1"),
            ("Крок 2", ACCENT2,
             "Від цілої частини відніміть цілу,  від дробової — дробову"),
            ("Крок 3", MUTED,
             "Якщо чисельник результату = 0 — дробову частину НЕ записуємо"),
        ]:
            row = tk.Frame(sub_mix_f, bg=CARD_V)
            row.pack(anchor="w", pady=4)
            tk.Label(row, text=f"  {step}:  ", font=F_STEP, bg=CARD_V,
                     fg=color, width=10, anchor="w").pack(side="left")
            tk.Label(row, text=txt, font=F_STEP_V, bg=CARD_V, fg=TEXT,
                     justify="left", wraplength=1200).pack(side="left")

        # Example C: no borrow  →  5³⁄₇ − 2¹⁄₇ = 3²⁄₇
        ex_sub_c = tk.Frame(sub_mix_f, bg=PANEL, padx=16, pady=12,
                            highlightbackground=BORDER, highlightthickness=1)
        ex_sub_c.pack(fill="x", pady=(8, 4))
        tk.Label(ex_sub_c, text="Приклад В  (без позичання):",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(anchor="w")

        for label, color, calc, explain in [
            ("Крок 1", ACCENT,
             "3 ≥ 1  ✅",
             "Чисельник зменшуваного (3) ≥ від'ємника (1) — позичати не треба"),
            ("Крок 2", ACCENT2,
             "5 − 2 = 3   та   3 − 1 = 2",
             "Цілі окремо, дробові окремо"),
        ]:
            r = tk.Frame(ex_sub_c, bg=CARD_V, padx=14, pady=7,
                         highlightbackground=BORDER, highlightthickness=1)
            r.pack(fill="x", pady=3)
            tk.Label(r, text=label, font=F_STEP, bg=CARD_V, fg=color,
                     width=8, anchor="w").pack(side="left")
            tk.Label(r, text=calc, font=("Segoe UI", 18, "bold"),
                     bg=CARD_V, fg=color).pack(side="left", padx=12)
            tk.Label(r, text=f"({explain})", font=F_SMALL,
                     bg=CARD_V, fg=MUTED).pack(side="left")

        rc = tk.Frame(ex_sub_c, bg=PANEL)
        rc.pack(anchor="w", pady=8)
        mixed_w(rc, 5, 3, 7, PANEL, "big", TEXT, ACCENT).pack(side="left")
        tk.Label(rc, text="  −  ", font=F_HEAD, bg=PANEL, fg=TEXT).pack(side="left")
        mixed_w(rc, 2, 1, 7, PANEL, "big", TEXT, ACCENT2).pack(side="left")
        tk.Label(rc, text="  =  ", font=F_HEAD, bg=PANEL, fg=TEXT).pack(side="left")
        mixed_w(rc, 3, 2, 7, PANEL, "big", GREEN, GREEN).pack(side="left")

        # Example D: with borrow  →  4²⁄₅ − 1⁴⁄₅
        # Borrow: 4²⁄₅ → 3 і (2+5)/5 = 3⁷⁄₅
        # Then: 3−1=2,  7−4=3  →  2³⁄₅
        ex_sub_d = tk.Frame(sub_mix_f, bg=PANEL, padx=16, pady=12,
                            highlightbackground=BORDER, highlightthickness=1)
        ex_sub_d.pack(fill="x", pady=(4, 8))
        tk.Label(ex_sub_d, text="Приклад Г  (треба позичити цілу частину):",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(anchor="w")

        for label, color, calc, explain in [
            ("Крок 1", ACCENT,
             "2 < 4  ❌   →   4²⁄₅ = 3⁷⁄₅   (2 + 5 = 7,  цілих 4 → 3)",
             "Чисельник 2 < 4 → позичаємо: +5 до чисельника, −1 до цілої"),
            ("Крок 2", ACCENT2,
             "3 − 1 = 2   та   7 − 4 = 3",
             "Цілі: 2.  Дробові: 3/5"),
        ]:
            r = tk.Frame(ex_sub_d, bg=CARD_V, padx=14, pady=7,
                         highlightbackground=BORDER, highlightthickness=1)
            r.pack(fill="x", pady=3)
            tk.Label(r, text=label, font=F_STEP, bg=CARD_V, fg=color,
                     width=8, anchor="w").pack(side="left")
            tk.Label(r, text=calc, font=("Segoe UI", 18, "bold"),
                     bg=CARD_V, fg=color).pack(side="left", padx=12)
            tk.Label(r, text=f"({explain})", font=F_SMALL,
                     bg=CARD_V, fg=MUTED).pack(side="left")

        rd = tk.Frame(ex_sub_d, bg=PANEL)
        rd.pack(anchor="w", pady=8)
        mixed_w(rd, 4, 2, 5, PANEL, "big", TEXT, ACCENT).pack(side="left")
        tk.Label(rd, text="  −  ", font=F_HEAD, bg=PANEL, fg=TEXT).pack(side="left")
        mixed_w(rd, 1, 4, 5, PANEL, "big", TEXT, ACCENT2).pack(side="left")
        tk.Label(rd, text="  =  ", font=F_HEAD, bg=PANEL, fg=TEXT).pack(side="left")
        # Show borrow step
        mixed_w(rd, 3, 7, 5, PANEL, "big", ORANGE, ORANGE).pack(side="left")
        tk.Label(rd, text="  −  ", font=F_HEAD, bg=PANEL, fg=TEXT).pack(side="left")
        mixed_w(rd, 1, 4, 5, PANEL, "big", TEXT, ACCENT2).pack(side="left")
        tk.Label(rd, text="  =  ", font=F_HEAD, bg=PANEL, fg=TEXT).pack(side="left")
        mixed_w(rd, 2, 3, 5, PANEL, "big", GREEN, GREEN).pack(side="left")

        # Example E: result whole only  →  3³⁄₈ − 1³⁄₈ = 2
        ex_sub_e = tk.Frame(sub_mix_f, bg=CARD_Y, padx=16, pady=12,
                            highlightbackground=BORDER, highlightthickness=1)
        ex_sub_e.pack(fill="x", pady=(4, 8))
        tk.Label(ex_sub_e, text="Приклад Д  (дробова частина = 0 → не записуємо):",
                 font=F_BODYB, bg=CARD_Y, fg=TEXT).pack(anchor="w")
        re_row = tk.Frame(ex_sub_e, bg=CARD_Y)
        re_row.pack(anchor="w", pady=6)
        mixed_w(re_row, 3, 3, 8, CARD_Y, "big", TEXT, ACCENT).pack(side="left")
        tk.Label(re_row, text="  −  ", font=F_HEAD, bg=CARD_Y, fg=TEXT).pack(side="left")
        mixed_w(re_row, 1, 3, 8, CARD_Y, "big", TEXT, ACCENT2).pack(side="left")
        tk.Label(re_row, text="  =  ", font=F_HEAD, bg=CARD_Y, fg=TEXT).pack(side="left")
        tk.Label(re_row, text="2",
                 font=F_FRAC, bg=CARD_Y, fg=GREEN).pack(side="left", padx=8, pady=10)
        tk.Label(ex_sub_e,
                 text="3 − 1 = 2  (цілі),   3 − 3 = 0  (дробова нуль → не пишемо)",
                 font=F_BODY, bg=CARD_Y, fg=MUTED).pack(anchor="w")

        # ── Number line ───────────────────────────────────────────────────
        nl_f = tk.Frame(p, bg=PANEL, padx=22, pady=18,
                        highlightbackground=BORDER, highlightthickness=1)
        nl_f.pack(fill="x", pady=8)
        tk.Label(nl_f, text="📐  На координатному промені: перехід через ціле",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack(anchor="w")
        tk.Label(nl_f,
                 text="Приклад:  3/5  +  4/5  =  7/5  =  1 і 2/5\n"
                      "Стрілка перетинає позначку «1» — сума більша за ціле число!",
                 font=F_BODY, bg=PANEL, fg=TEXT).pack(anchor="w", pady=(6, 12))
        self._draw_number_line(nl_f, denom=5, n1=3, n2=4,
                               width=self.SW - 200, bg=PANEL)

        theory_card(p, "💡  Запам'ятай",
                    "Додавання:  цілі + цілі,  дробові + дробові.\n"
                    "   Якщо дробова частина стала ≥ знаменника → виділяємо 1 цілу з дробової.\n\n"
                    "Віднімання:  якщо чисельник зменшуваного < від'ємника → позичаємо 1 цілу\n"
                    "   (додаємо знаменник до чисельника, ціла частина −1).\n"
                    "   Потім: цілі − цілі,  дробові − дробові.\n"
                    "   Якщо дробова частина = 0 → дріб не записуємо.",
                    "#f1f5f9", MUTED)

    def _draw_number_line(self, parent, denom, n1, n2, width=800, bg=PANEL):
        """
        Draw number line 0..2 showing:
          - first arc:  0  →  n1/d
          - second arc: n1/d → (n1+n2)/d   (may cross 1)
          - vertical barrier at 1 highlighted in red when sum > d
        """
        H = 140
        cv = tk.Canvas(parent, bg=bg, width=width, height=H, highlightthickness=0)
        cv.pack(fill="x")

        left, right = 70, width - 60
        ly = 80       # main line y
        span = right - left   # pixels representing 0→2

        total = n1 + n2
        crosses_one = total > denom   # sum exceeds 1

        # ── Shaded background zones ────────────────────────────────────
        mid = left + span // 2   # position of 1
        cv.create_rectangle(left, ly - 8, mid,       ly + 8, fill=GREEN_LT,  outline="")
        cv.create_rectangle(mid,  ly - 8, right - 20, ly + 8, fill=CARD_Y, outline="")

        # ── Main line ──────────────────────────────────────────────────
        cv.create_line(left, ly, right, ly, fill=MUTED, width=3)
        cv.create_line(right-14, ly-7, right, ly, fill=MUTED, width=3)
        cv.create_line(right-14, ly+7, right, ly, fill=MUTED, width=3)

        # ── Ticks & labels ─────────────────────────────────────────────
        for i in range(denom * 2 + 1):
            x = left + i * span // (denom * 2)
            is_whole = (i % denom == 0)
            th = 16 if is_whole else 8
            lw = 3  if is_whole else 1
            cv.create_line(x, ly - th, x, ly + th, fill=TEXT if is_whole else MUTED, width=lw)
            if is_whole:
                cv.create_text(x, ly + 30, text=str(i // denom),
                               font=("Segoe UI", 15, "bold"), fill=TEXT)
            else:
                # small fraction label for every tick
                cv.create_text(x, ly + 22, text=f"{i}/{denom}",
                               font=("Segoe UI", 10), fill=MUTED)

        def px(n, d):
            return left + int(n / d * span / 2)

        x0 = px(0,  1)
        xA = px(n1, denom)
        xB = px(total, denom)
        x1 = mid   # position of integer 1

        # ── Red barrier at 1 if sum crosses ───────────────────────────
        if crosses_one:
            cv.create_line(x1, ly - 30, x1, ly + 30, fill=RED, width=3, dash=(6, 3))
            cv.create_text(x1, ly - 40,
                           text="← перехід через 1! →",
                           font=("Segoe UI", 11, "bold"), fill=RED)

        # ── Arc 1: 0 → n1/d  (blue) ───────────────────────────────────
        arc_h1 = 52
        cv.create_arc(x0, ly - arc_h1, xA, ly + arc_h1,
                      start=0, extent=180, style="arc",
                      outline=C1, width=4)
        cv.create_text((x0 + xA) / 2, ly - arc_h1 - 14,
                       text=f"+{n1}/{denom}", font=("Segoe UI", 13, "bold"), fill=C1)

        # ── Arc 2: n1/d → total/d  (orange, may cross 1) ──────────────
        arc_h2 = 72
        cv.create_arc(xA, ly - arc_h2, xB, ly + arc_h2,
                      start=0, extent=180, style="arc",
                      outline=C2, width=4)
        cv.create_text((xA + xB) / 2, ly - arc_h2 - 14,
                       text=f"+{n2}/{denom}", font=("Segoe UI", 13, "bold"), fill=C2)

        # ── Dots ───────────────────────────────────────────────────────
        dot_items = [(x0, "0", MUTED), (xA, f"{n1}/{denom}", C1)]
        if crosses_one:
            # label result as mixed number
            w_res = total // denom
            r_res = total % denom
            res_label = f"{w_res} і {r_res}/{denom}"
        else:
            res_label = f"{total}/{denom}"
        dot_items.append((xB, res_label, C_ANS_OK))

        for x, label, color in dot_items:
            cv.create_oval(x - 8, ly - 8, x + 8, ly + 8,
                           fill=color, outline=WHITE, width=2)
            cv.create_text(x, ly + 50,
                           text=label, font=("Segoe UI", 12, "bold"), fill=color)

    # ══════════════════════════════════════════════════════════════════════════
    # PRACTICE
    # ══════════════════════════════════════════════════════════════════════════
    def show_practice(self):
        self.clear_main()
        self.mode = "practice"

        cf = self.current_frame

        # ── Score bar ─────────────────────────────────────────────────────
        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.score_lbl = tk.Label(sbar,
            text=self._score_text(), font=F_SCORE, bg=PANEL, fg=GREEN)
        self.score_lbl.pack(side="left", padx=30)
        tk.Label(sbar,
                 text="🎯  Змінюй числа кнопками — кружечки оновляться",
                 font=("Segoe UI", 15, "bold"), bg=PANEL, fg=TEAL).pack(
            side="left", padx=10)

        # ── Two-column workspace ───────────────────────────────────────────
        ws = tk.Frame(cf, bg=BG)
        ws.pack(fill="both", expand=True, padx=16, pady=12)

        # LEFT — task + pie visualization ─────────────────────────────────
        left = tk.Frame(ws, bg=PANEL,
                        highlightbackground=BORDER, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        tk.Label(left, text="📋  Завдання",
                 font=F_SUB, bg=PANEL, fg=MUTED).pack(anchor="w", padx=20, pady=(10, 4))
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x")

        # Task expression (rebuilt on new task)
        self.task_frame = tk.Frame(left, bg=PANEL, pady=12)
        self.task_frame.pack(fill="x", padx=20)

        # Pie row labels
        pie_labels_f = tk.Frame(left, bg=PANEL)
        pie_labels_f.pack(fill="x", padx=20, pady=(8, 0))

        self.pie_label1 = tk.Label(pie_labels_f, text="",
                                    font=F_BODYB, bg=PANEL, fg=C1)
        self.pie_label1.pack(side="left", padx=8)
        self.pie_label2 = tk.Label(pie_labels_f, text="",
                                    font=F_BODYB, bg=PANEL, fg=C2)
        self.pie_label2.pack(side="left", padx=8)

        # Pie display frame (2 rows: task pies, answer pie)
        pies_outer = tk.Frame(left, bg=PANEL)
        pies_outer.pack(fill="both", expand=True, padx=20, pady=6)

        # Row 1: task pies side by side
        task_pies_row = tk.Frame(pies_outer, bg=PANEL)
        task_pies_row.pack(anchor="w")
        self.pie1_frame = tk.Frame(task_pies_row, bg=PANEL)
        self.pie1_frame.pack(side="left", padx=(0, 20))
        self.pie2_frame = tk.Frame(task_pies_row, bg=PANEL)
        self.pie2_frame.pack(side="left")

        # Separator
        tk.Frame(pies_outer, bg=BORDER, height=1).pack(fill="x", pady=8)

        # Row 2: answer pie
        tk.Label(pies_outer, text="Твоя відповідь (оновлюється):",
                 font=F_BODYB, bg=PANEL, fg=MUTED).pack(anchor="w")
        self.pie_ans_frame = tk.Frame(pies_outer, bg=PANEL)
        self.pie_ans_frame.pack(anchor="w", pady=4)

        # RIGHT — answer controls ──────────────────────────────────────────
        right = tk.Frame(ws, bg=PANEL,
                         highlightbackground=BORDER, highlightthickness=1,
                         width=int(self.SW * 0.38))
        right.pack(side="right", fill="both")
        right.pack_propagate(False)

        tk.Label(right, text="✏️  Введи відповідь",
                 font=F_SUB, bg=PANEL, fg=MUTED).pack(anchor="w", padx=20, pady=(10, 4))
        tk.Frame(right, bg=BORDER, height=1).pack(fill="x")

        ctrl_area = tk.Frame(right, bg=PANEL)
        ctrl_area.pack(fill="x", padx=20, pady=14)

        # Live answer display (drawn as fraction/mixed)
        self.ans_disp_f = tk.Frame(ctrl_area, bg=PANEL)
        self.ans_disp_f.pack(anchor="w", pady=(0, 12))

        # Controls — save plus-button refs for dynamic capping
        self.ctrl_whole, self._btn_whole_m, self._btn_whole_p = make_ctrl_row(
            ctrl_area, "Ціла частина:",  self.u_whole, 0, 30, GREEN, self._on_change)
        self.ctrl_whole.pack(fill="x", pady=8)

        self.ctrl_num, self._btn_num_m, self._btn_num_p = make_ctrl_row(
            ctrl_area, "Чисельник:",     self.u_num,   0, 99, ACCENT2, self._on_change)
        self.ctrl_num.pack(fill="x", pady=8)

        self.ctrl_den, self._btn_den_m, self._btn_den_p = make_ctrl_row(
            ctrl_area, "Знаменник:",     self.u_den,   1, 30, ACCENT, self._on_change)
        self.ctrl_den.pack(fill="x", pady=8)

        # Feedback
        self.feed_lbl = tk.Label(right, text="",
                                  font=F_FEED, bg=PANEL, fg=GREEN,
                                  wraplength=int(self.SW * 0.36),
                                  justify="center")
        self.feed_lbl.pack(pady=6)

        # Hint: show correct answer
        self.hint_lbl = tk.Label(right, text="",
                                  font=("Segoe UI", 15), bg=PANEL, fg=MUTED,
                                  wraplength=int(self.SW * 0.36),
                                  justify="center")
        self.hint_lbl.pack(pady=2)

        # Buttons
        act = tk.Frame(right, bg=PANEL)
        act.pack(side="bottom", pady=16)
        mkbtn(act, "💡  Показати відповідь", self._show_hint,
              bg=ORANGE, w=18, h=2).pack(side="left", padx=8)
        self.next_btn = mkbtn(act, "▶  Нове завдання", self._new_task,
                               bg=ACCENT, w=16, h=2)
        self.next_btn.pack(side="left", padx=8)

        self._new_task()

    # ── Practice helpers ──────────────────────────────────────────────────────
    def _score_text(self):
        return f"Правильно: {self.score}  /  Завдань: {self.attempts}"

    def _new_task(self):
        # Choose operation and type
        self.op        = random.choice(["+", "−"])
        self.task_type = random.choice(["frac", "frac", "mixed"])  # 2/3 plain fracs, 1/3 mixed
        d = random.randint(3, 10)
        self.t_d = d

        if self.task_type == "frac":
            if self.op == "+":
                n1 = random.randint(1, d - 1)
                n2 = random.randint(1, d * 2 - n1)   # may cross 1
            else:
                n1 = random.randint(2, d * 2)
                n2 = random.randint(1, n1)
        else:
            # mixed: generate as whole + fraction
            w1 = random.randint(0, 3)
            fn1 = random.randint(1, d - 1)
            w2 = random.randint(0, 3)
            fn2 = random.randint(1, d - 1)
            n1 = w1 * d + fn1
            n2 = w2 * d + fn2
            if self.op == "−" and n2 > n1:
                n1, n2 = n2, n1   # ensure non-negative

        self.t_n1, self.t_n2 = n1, n2
        corr = n1 + n2 if self.op == "+" else n1 - n2
        self.correct_n = corr
        self.correct_d = d
        self.attempts += 1
        self._task_scored = False   # reset per-task score guard

        # Reset user inputs to neutral starting values
        self.u_whole.set(0)
        self.u_num.set(1)
        self.u_den.set(1)

        if self.hint_lbl: self.hint_lbl.config(text="")
        if self.feed_lbl: self.feed_lbl.config(text="")

        # Re-enable controls (they may have been locked by previous correct answer)
        self._enable_controls()

        # Rebuild task expression
        self._draw_task_expr()
        self._draw_task_pies()
        self._on_change()

        if self.score_lbl:
            self.score_lbl.config(text=self._score_text())

    def _draw_task_expr(self):
        """Rebuild the task expression row."""
        for w in self.task_frame.winfo_children():
            w.destroy()

        row = tk.Frame(self.task_frame, bg=PANEL)
        row.pack()
        d = self.t_d
        n1, n2 = self.t_n1, self.t_n2

        # Draw first operand
        self._draw_number_or_mixed(row, n1, d, PANEL, "big", C1)

        tk.Label(row,
                 text=f"  {self.op}  ",
                 font=("Segoe UI", 48, "bold"),
                 bg=PANEL, fg=ORANGE).pack(side="left")

        # Draw second operand
        self._draw_number_or_mixed(row, n2, d, PANEL, "big", C2)

        tk.Label(row, text="  =  ?",
                 font=("Segoe UI", 48, "bold"),
                 bg=PANEL, fg=MUTED).pack(side="left")

    def _draw_number_or_mixed(self, parent, numer, denom, bg, size, color):
        """Draw numer/denom: if whole part > 0 draw as mixed, else as fraction."""
        whole = numer // denom
        rem   = numer % denom
        if whole > 0 and rem > 0:
            mixed_w(parent, whole, rem, denom, bg, size, color, color).pack(side="left")
        elif whole > 0:
            # pure natural number
            fn = F_FRAC if size == "big" else F_FRAC_S
            tk.Label(parent, text=str(whole), font=fn, bg=bg, fg=color).pack(
                side="left", padx=6, pady=10)
        else:
            frac_w(parent, rem, denom, bg, size, color).pack(side="left")

    def _draw_task_pies(self):
        d = self.t_d

        # Label pie 1
        n1, n2 = self.t_n1, self.t_n2
        w1, r1 = n1 // d, n1 % d
        w2, r2 = n2 // d, n2 % d

        lbl1 = self._frac_label(w1, r1, d)
        lbl2 = self._frac_label(w2, r2, d)
        op_word = "Перший доданок:" if self.op == "+" else "Зменшуване:"
        op_word2 = "Другий доданок:" if self.op == "+" else "Від'ємник:"
        if self.pie_label1: self.pie_label1.config(text=f"{op_word} {lbl1}")
        if self.pie_label2: self.pie_label2.config(text=f"  {op_word2} {lbl2}")

        for frame, n, color in [
            (self.pie1_frame, n1, C1),
            (self.pie2_frame, n2, C2),
        ]:
            for w in frame.winfo_children():
                w.destroy()
            cv = draw_pie_circles(frame, n, d, color, radius=40, bg=PANEL)
            cv.pack()

    def _frac_label(self, whole, num, den):
        if whole > 0 and num > 0:
            return f"{whole} і {num}/{den}"
        elif whole > 0:
            return str(whole)
        else:
            return f"{num}/{den}"

    def _on_change(self, *_):
        """Rebuild answer pie and check."""
        # Guard: do nothing if practice controls don't exist yet
        if self.feed_lbl is None:
            return

        wh = self.u_whole.get()
        n  = self.u_num.get()
        d  = max(1, self.u_den.get())

        # Clamp negatives
        if wh < 0: self.u_whole.set(0); wh = 0
        if n  < 0: self.u_num.set(0);   n  = 0
        if d  < 1: self.u_den.set(1);   d  = 1

        ans_n = wh * d + n

        # ── Cap: max 7 circles displayable ────────────────────────────
        # circles_used = whole full circles + 1 partial (if remainder > 0)
        MAX_CIRCLES = 7
        circles_used = ans_n // d + (1 if ans_n % d > 0 else 0)
        at_limit = circles_used >= MAX_CIRCLES
        for btn in [getattr(self, '_btn_whole_p', None),
                    getattr(self, '_btn_num_p',   None)]:
            if btn and btn.winfo_exists():
                btn.config(state="disabled" if at_limit else "normal")
        for w in self.ans_disp_f.winfo_children():
            w.destroy()
        # Draw as-entered: whole part + fraction n/d  (NO auto-conversion)
        row_ans = tk.Frame(self.ans_disp_f, bg=PANEL)
        row_ans.pack(side="left")
        if wh > 0 and n > 0:
            # whole + fraction side by side
            mixed_w(row_ans, wh, n, d, PANEL, "big", TEXT, ACCENT2).pack(side="left")
        elif wh > 0:
            # only whole
            tk.Label(row_ans, text=str(wh), font=F_FRAC,
                     bg=PANEL, fg=TEXT).pack(side="left", padx=6, pady=10)
        elif n > 0:
            # only fraction
            frac_w(row_ans, n, d, PANEL, "big", ACCENT2).pack(side="left")
        else:
            tk.Label(row_ans, text="0", font=F_FRAC,
                     bg=PANEL, fg=MUTED).pack(side="left", padx=6, pady=10)

        # ── Validate: чисельник має бути < знаменника ─────────────────
        # If the fractional part is improper (n >= d) show a warning, not correct
        improper_frac = (n >= d)

        # ── Rebuild answer pie ─────────────────────────────────────────
        for w in self.pie_ans_frame.winfo_children():
            w.destroy()

        mathematically_ok = self._is_correct()
        ok = mathematically_ok and not improper_frac

        if ans_n == 0:
            pie_color = MUTED
        elif ok:
            pie_color = C_ANS_OK
        else:
            pie_color = C_ANS_BAD

        cv = draw_pie_circles(self.pie_ans_frame, ans_n, d, pie_color, radius=40, bg=PANEL)
        cv.pack(side="left", padx=4)

        t_d = self.t_d
        corr_n = self.correct_n
        corr_w = corr_n // t_d
        corr_r = corr_n % t_d
        correct_lbl = self._frac_label(corr_w, corr_r, t_d)
        tk.Label(self.pie_ans_frame,
                 text=f"  ←  правильна відповідь:  {correct_lbl}" if ok else "",
                 font=F_BODYB, bg=PANEL, fg=GREEN).pack(side="left")

        # ── Feedback ───────────────────────────────────────────────────
        if ok:
            # Only increment score once per task (guard with self._task_scored)
            if not getattr(self, '_task_scored', False):
                self.score += 1
                self._task_scored = True
                if self.score_lbl:
                    self.score_lbl.config(text=self._score_text())
                self._disable_controls()
            self.feed_lbl.config(text="🎉  Правильно!", fg=GREEN)
            if self.hint_lbl:
                self.hint_lbl.config(text="")

        elif mathematically_ok and improper_frac:
            self.feed_lbl.config(
                text=f"⚠️  Майже! Чисельник ({n}) ≥ знаменника ({d}).\n"
                     f"Виділи цілу частину із дробової — запиши у правильній формі.",
                fg=ORANGE)
            if self.hint_lbl:
                self.hint_lbl.config(text="")

        else:
            if ans_n > 0:
                self.feed_lbl.config(text="", fg=TEXT)
            else:
                self.feed_lbl.config(text="")

    def _is_correct(self):
        wh = self.u_whole.get()
        n  = self.u_num.get()
        d  = max(1, self.u_den.get())
        ans_n = wh * d + n
        # Cross-multiply: ans_n/d == correct_n/correct_d
        return ans_n * self.correct_d == self.correct_n * d

    def _enable_controls(self):
        """Restore +/- buttons to normal state."""
        for ctrl in [self.ctrl_whole, self.ctrl_num, self.ctrl_den]:
            if ctrl:
                for child in ctrl.winfo_children():
                    if isinstance(child, tk.Button):
                        child.config(state="normal", bg=BTN_NUM)
        # Cap-related + buttons are re-evaluated by _on_change after this

    def _disable_controls(self):
        """Grey out +/- buttons after correct answer until next task."""
        for ctrl in [self.ctrl_whole, self.ctrl_num, self.ctrl_den]:
            if ctrl:
                for child in ctrl.winfo_children():
                    if isinstance(child, tk.Button):
                        child.config(state="disabled", bg=BTN_NUM)

    def _show_hint(self):
        d = self.correct_d
        n = self.correct_n
        w, r = n // d, n % d
        lbl = self._frac_label(w, r, d)
        if self.hint_lbl:
            self.hint_lbl.config(
                text=f"Правильна відповідь:  {lbl}",
                fg=ORANGE)
        # Set user vars to correct answer so pies match
        self.u_whole.set(w)
        self.u_num.set(r)
        self.u_den.set(d)
        self._on_change()


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
