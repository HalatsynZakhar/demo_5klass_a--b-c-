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
F_SIGN   = ("Segoe UI", 52, "bold")   # < > =


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
    """Visual fraction widget."""
    sizes  = {"big": F_FRAC, "small": F_FRAC_S}
    widths = {"big": 60,     "small": 44}
    fn = sizes.get(size, F_FRAC_S)
    bw = widths.get(size, 44)
    f = tk.Frame(parent, bg=bg)
    tk.Label(f, text=str(n), font=fn, bg=bg, fg=color).pack()
    tk.Frame(f, bg=color, height=3, width=bw).pack(pady=2)
    tk.Label(f, text=str(d), font=fn, bg=bg, fg=color).pack()
    return f


def build_numpad(parent, key_fn, bg=BG):
    np = tk.Frame(parent, bg=bg)
    for row_chars in [("7","8","9"),("4","5","6"),("1","2","3"),("C","0","⌫")]:
        rf = tk.Frame(np, bg=bg)
        rf.pack(pady=4)
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


# ── Bar diagram: fraction as filled/empty blocks ──────────────────────────────
def fraction_bar(parent, numer, denom, bg_filled=ACCENT, bg_empty=BTN_NUM,
                 cell_w=52, cell_h=52, bg=PANEL):
    """Draw a row of `denom` cells, first `numer` are filled."""
    row = tk.Frame(parent, bg=bg)
    for i in range(denom):
        color = bg_filled if i < numer else bg_empty
        fc    = WHITE     if i < numer else MUTED
        cell = tk.Frame(row, bg=color, width=cell_w, height=cell_h,
                        highlightbackground=bg,
                        highlightthickness=1)
        cell.pack(side="left", padx=2)
        cell.pack_propagate(False)
        tk.Label(cell, text="●" if i < numer else "○",
                 font=("Segoe UI", 16), bg=color, fg=fc).pack(expand=True)
    return row


# ── Number line widget ─────────────────────────────────────────────────────────
def number_line(parent, denom, mark1, mark2, bg=PANEL, width=700):
    """
    Draw a number line from 0 to 1, divided into `denom` equal parts.
    mark1 and mark2 are numerators to mark (as fractions /denom).
    Returns canvas.
    """
    H = 80
    cv = tk.Canvas(parent, bg=bg, width=width, height=H,
                   highlightthickness=0)

    left, right = 60, width - 60
    mid_y = 44
    tick_h = 10

    # Line
    cv.create_line(left, mid_y, right, mid_y, fill=MUTED, width=2)
    # Arrows
    cv.create_line(right - 12, mid_y - 6, right, mid_y, fill=MUTED, width=2)
    cv.create_line(right - 12, mid_y + 6, right, mid_y, fill=MUTED, width=2)

    step = (right - left) / denom

    for i in range(denom + 1):
        x = left + i * step
        cv.create_line(x, mid_y - tick_h, x, mid_y + tick_h, fill=MUTED, width=2)
        if i == 0:
            cv.create_text(x, mid_y + 22, text="0", font=F_SMALL, fill=MUTED)
        elif i == denom:
            cv.create_text(x, mid_y + 22, text="1", font=F_SMALL, fill=MUTED)

    def mark(num, color, label_offset=-18):
        x = left + num * step
        cv.create_oval(x - 8, mid_y - 8, x + 8, mid_y + 8,
                       fill=color, outline=color)
        cv.create_text(x, mid_y + label_offset,
                       text=f"{num}/{denom}", font=("Segoe UI", 12, "bold"),
                       fill=color)

    colors = [ACCENT, RED, GREEN, ORANGE]
    for idx, m in enumerate([mark1, mark2]):
        if m is not None:
            mark(m, colors[idx % len(colors)])

    return cv


# ══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("§ 35. Порівняння дробів з однаковими знаменниками")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()
        self.current_frame = None
        self.mode = None

        # ── Trainer 1: choose < > = ──────────────────────────────────────
        self.t1_a = self.t1_b = self.t1_d = 0
        self.t1_score = self.t1_attempts = 0
        self.t1_score_lbl  = None
        self.t1_feed_lbl   = None
        self.t1_sign_lbl   = None
        self.t1_frac1_f    = None
        self.t1_frac2_f    = None
        self.t1_bar1_f     = None
        self.t1_bar2_f     = None
        self.t1_answered   = False

        # ── Trainer 2: sort 3 fractions ──────────────────────────────────
        self.t2_denom   = 0
        self.t2_numers  = []      # [a, b, c]
        self.t2_order   = []      # indices: what user clicked so far
        self.t2_btns    = []
        self.t2_score   = 0
        self.t2_attempts = 0
        self.t2_score_lbl = None
        self.t2_feed_lbl  = None
        self.t2_seq_lbl   = None
        self.t2_check_btn = None

        self._build_chrome()
        self.show_main_menu()

    # ── Chrome ────────────────────────────────────────────────────────────────
    def _build_chrome(self):
        hdr = tk.Frame(self, bg=HDR_BG, height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr,
                 text="§ 35.   Порівняння звичайних дробів з однаковими знаменниками",
                 bg=HDR_BG, fg=WHITE,
                 font=("Segoe UI", 20, "bold")).pack(side="left", padx=30)
        mkbtn(hdr, "✕  Вийти", self.destroy, bg="#b91c1c",
              font=("Segoe UI", 13, "bold"), w=9, h=1).pack(
            side="right", padx=18, pady=16)

        nav = tk.Frame(self, bg=NAV_BG, height=52)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        for label, cmd in [
            ("🏠  Меню",            self.show_main_menu),
            ("📖  Теорія",          self.show_theory),
            ("🎯  Постав знак",     self.show_trainer_1),
            ("🎯  Впорядкуй дроби", self.show_trainer_2),
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

        tk.Label(center, text="Порівняння дробів",
                 font=("Segoe UI", 48, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 4))
        tk.Label(center, text="з однаковими знаменниками   §35",
                 font=("Segoe UI", 24), bg=BG, fg=ACCENT).pack(pady=(0, 28))

        cards = [
            ("📖", "Теорія",           CARD_B, ACCENT,  self.show_theory),
            ("🎯", "Постав знак\n< > =", CARD_G, GREEN, self.show_trainer_1),
            ("🎯", "Впорядкуй\nдроби",  CARD_Y, ORANGE, self.show_trainer_2),
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

        tk.Label(p, text="Порівняння дробів з однаковими знаменниками",
                 font=F_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        hline(p, ACCENT)

        # ── Main rule ─────────────────────────────────────────────────────
        rule_f = tk.Frame(p, bg=CARD_B, padx=22, pady=18,
                          highlightbackground=ACCENT, highlightthickness=2)
        rule_f.pack(fill="x", pady=8)
        tk.Label(rule_f, text="📌  Правило",
                 font=F_SUB, bg=CARD_B, fg=ACCENT).pack(anchor="w")
        tk.Label(rule_f,
                 text="З двох дробів з однаковими знаменниками:",
                 font=F_BODY, bg=CARD_B, fg=TEXT).pack(anchor="w", pady=(8, 4))

        rows_rule = [
            (GREEN,  "●  БІЛЬШИЙ — той, чисельник якого БІЛЬШИЙ"),
            (RED,    "●  МЕНШИЙ  — той, чисельник якого МЕНШИЙ"),
            (ORANGE, "●  РІВНІ    — якщо чисельники однакові"),
        ]
        for color, txt in rows_rule:
            tk.Label(rule_f, text=txt, font=F_BODYB, bg=CARD_B, fg=color,
                     anchor="w").pack(anchor="w", pady=2)

        tk.Label(rule_f,
                 text="\nЗнаменники однакові → дивись лише на чисельники!",
                 font=("Segoe UI", 18, "bold"), bg=CARD_B, fg=ACCENT).pack(anchor="w")

        # ── Cake visual ───────────────────────────────────────────────────
        cake_f = tk.Frame(p, bg=PANEL, padx=22, pady=20,
                          highlightbackground=BORDER, highlightthickness=1)
        cake_f.pack(fill="x", pady=8)
        tk.Label(cake_f, text="🎂  Наочний приклад: торт розрізали на 8 рівних частин",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(anchor="w", pady=(0, 12))

        plates = tk.Frame(cake_f, bg=PANEL)
        plates.pack(anchor="w")

        for numer, label_color, plate_label in [
            (1, ACCENT, "Тарілка 1"),
            (3, RED,    "Тарілка 2"),
        ]:
            col = tk.Frame(plates, bg=PANEL, padx=16)
            col.pack(side="left", padx=12)
            tk.Label(col, text=plate_label, font=F_BODYB,
                     bg=PANEL, fg=label_color).pack(anchor="w", pady=(0, 4))
            fraction_bar(col, numer, 8,
                         bg_filled=label_color, bg_empty=BTN_NUM,
                         cell_w=46, cell_h=46, bg=PANEL).pack(anchor="w")
            fr_row = tk.Frame(col, bg=PANEL)
            fr_row.pack(anchor="w", pady=6)
            tk.Label(fr_row, text="Дістала:  ", font=F_BODY,
                     bg=PANEL, fg=MUTED).pack(side="left")
            frac_w(fr_row, numer, 8, PANEL, "small", label_color).pack(side="left")
            tk.Label(fr_row, text=f"  торта", font=F_BODY,
                     bg=PANEL, fg=MUTED).pack(side="left")

        verdict_row = tk.Frame(cake_f, bg=PANEL)
        verdict_row.pack(anchor="w", pady=10)
        frac_w(verdict_row, 1, 8, PANEL, "big", ACCENT).pack(side="left")
        tk.Label(verdict_row, text="  <  ", font=F_SIGN,
                 bg=PANEL, fg=ORANGE).pack(side="left")
        frac_w(verdict_row, 3, 8, PANEL, "big", RED).pack(side="left")
        tk.Label(verdict_row, text="   бо  1 < 3",
                 font=F_BODYB, bg=PANEL, fg=MUTED).pack(side="left", padx=20)

        # ── Examples with bars ────────────────────────────────────────────
        ex_f = tk.Frame(p, bg=CARD_G, padx=22, pady=18,
                        highlightbackground=BORDER, highlightthickness=1)
        ex_f.pack(fill="x", pady=8)
        tk.Label(ex_f, text="✏️  Більше прикладів",
                 font=F_SUB, bg=CARD_G, fg=GREEN).pack(anchor="w", pady=(0, 10))

        examples = [
            (2, 5, 10, "<"),
            (7, 3, 12, ">"),
            (4, 4, 9,  "="),
        ]
        for a, b, d, sign in examples:
            ex_row = tk.Frame(ex_f, bg=CARD_G, pady=6)
            ex_row.pack(anchor="w")

            frac_w(ex_row, a, d, CARD_G, "small", ACCENT).pack(side="left")

            sign_color = {">": GREEN, "<": RED, "=": ORANGE}[sign]
            tk.Label(ex_row, text=f"  {sign}  ", font=("Segoe UI", 28, "bold"),
                     bg=CARD_G, fg=sign_color).pack(side="left")

            frac_w(ex_row, b, d, CARD_G, "small", ACCENT2).pack(side="left")

            reason = f"бо {a} {sign} {b}" if a != b else f"бо {a} = {b}"
            tk.Label(ex_row, text=f"     ({reason},  знаменники однакові: {d})",
                     font=F_SMALL, bg=CARD_G, fg=MUTED).pack(side="left", padx=12)

        # ── Number line section ───────────────────────────────────────────
        nl_f = tk.Frame(p, bg=PANEL, padx=22, pady=18,
                        highlightbackground=BORDER, highlightthickness=1)
        nl_f.pack(fill="x", pady=8)
        tk.Label(nl_f, text="📐  На координатному промені",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack(anchor="w")
        tk.Label(nl_f,
                 text="Більшому дробу відповідає точка правіше,  меншому — лівіше.",
                 font=F_BODY, bg=PANEL, fg=TEXT).pack(anchor="w", pady=(6, 10))

        # Draw number line for 1/8 and 3/8
        nl_demo = number_line(nl_f, 8, 1, 3, bg=PANEL, width=self.SW - 160)
        nl_demo.pack(fill="x", anchor="w")

        ann_row = tk.Frame(nl_f, bg=PANEL)
        ann_row.pack(anchor="w", pady=8)
        frac_w(ann_row, 1, 8, PANEL, "small", ACCENT).pack(side="left")
        tk.Label(ann_row, text="  лежить лівіше  →  менший,     ",
                 font=F_BODY, bg=PANEL, fg=MUTED).pack(side="left")
        frac_w(ann_row, 3, 8, PANEL, "small", RED).pack(side="left")
        tk.Label(ann_row, text="  лежить правіше  →  більший",
                 font=F_BODY, bg=PANEL, fg=MUTED).pack(side="left")

        # ── Interactive demo ──────────────────────────────────────────────
        demo_f = tk.Frame(p, bg=CARD_Y, padx=22, pady=18,
                          highlightbackground=BORDER, highlightthickness=1)
        demo_f.pack(fill="x", pady=8)
        tk.Label(demo_f, text="🔢  Введи два дроби з однаковим знаменником — побачиш порівняння",
                 font=F_BODYB, bg=CARD_Y, fg=TEXT).pack(anchor="w")

        # Three input fields: A (numerator 1), D (denominator), B (numerator 2)
        # Each field is a small frame showing the fraction visually
        demo_state = {"field": "a", "a": "", "b": "", "d": ""}

        fields_row = tk.Frame(demo_f, bg=CARD_Y)
        fields_row.pack(anchor="w", pady=12)

        # --- Fraction 1 display (a over d) ---
        f1_wrap = tk.Frame(fields_row, bg=CARD_Y, padx=8)
        f1_wrap.pack(side="left")
        tk.Label(f1_wrap, text="Перший дріб:", font=F_SMALL, bg=CARD_Y, fg=MUTED).pack()
        demo_frac1 = tk.Frame(f1_wrap, bg=BTN_NUM, padx=10, pady=6,
                              highlightbackground=ACCENT, highlightthickness=3)
        demo_frac1.pack()
        demo_num1_lbl = tk.Label(demo_frac1, text="?", font=F_FRAC,
                                  bg=BTN_NUM, fg=ACCENT, width=3)
        demo_num1_lbl.pack()
        tk.Frame(demo_frac1, bg=ACCENT, height=3, width=60).pack(pady=2)
        demo_den1_lbl = tk.Label(demo_frac1, text="?", font=F_FRAC,
                                  bg=BTN_NUM, fg=MUTED, width=3)
        demo_den1_lbl.pack()

        tk.Label(fields_row, text="        ", bg=CARD_Y).pack(side="left")  # spacer

        # --- Fraction 2 display (b over d) ---
        f2_wrap = tk.Frame(fields_row, bg=CARD_Y, padx=8)
        f2_wrap.pack(side="left")
        tk.Label(f2_wrap, text="Другий дріб:", font=F_SMALL, bg=CARD_Y, fg=MUTED).pack()
        demo_frac2 = tk.Frame(f2_wrap, bg=BTN_NUM, padx=10, pady=6,
                              highlightbackground=BORDER, highlightthickness=1)
        demo_frac2.pack()
        demo_num2_lbl = tk.Label(demo_frac2, text="?", font=F_FRAC,
                                  bg=BTN_NUM, fg=ACCENT2, width=3)
        demo_num2_lbl.pack()
        tk.Frame(demo_frac2, bg=ACCENT2, height=3, width=60).pack(pady=2)
        demo_den2_lbl = tk.Label(demo_frac2, text="?", font=F_FRAC,
                                  bg=BTN_NUM, fg=MUTED, width=3)
        demo_den2_lbl.pack()

        # Field selector buttons
        sel_row = tk.Frame(demo_f, bg=CARD_Y)
        sel_row.pack(anchor="w", pady=(4, 8))

        def activate_field(field_key):
            demo_state["field"] = field_key
            # Highlight active field box
            demo_frac1.config(
                highlightbackground=ACCENT if field_key == "a" else BORDER,
                highlightthickness=3 if field_key == "a" else 1)
            demo_frac2.config(
                highlightbackground=ACCENT2 if field_key == "b" else BORDER,
                highlightthickness=3 if field_key == "b" else 1)
            # Update denominator labels immediately when d changes
            for lbl in sel_labels:
                pass

        sel_labels = []
        for key, label, color in [
            ("a", "✏️ Чисельник 1", ACCENT),
            ("d", "✏️ Знаменник",   ORANGE),
            ("b", "✏️ Чисельник 2", ACCENT2),
        ]:
            b_sel = tk.Button(sel_row, text=label,
                              font=("Segoe UI", 13, "bold"),
                              bg=BTN_NUM, fg=color,
                              relief="flat", cursor="hand2", padx=10, pady=6,
                              command=lambda k=key: activate_field(k))
            b_sel.pack(side="left", padx=5)
            sel_labels.append(b_sel)

        # Result display (visual fractions with sign)
        demo_result_row = tk.Frame(demo_f, bg=CARD_Y)
        demo_result_row.pack(anchor="w", pady=4)

        demo_nl_frame = tk.Frame(demo_f, bg=CARD_Y)
        demo_nl_frame.pack(fill="x", pady=4)

        def _update_demo_display():
            a_s = demo_state["a"]
            b_s = demo_state["b"]
            d_s = demo_state["d"]
            a_v = int(a_s) if a_s else None
            b_v = int(b_s) if b_s else None
            d_v = int(d_s) if d_s else None

            # Update fraction displays
            demo_num1_lbl.config(text=a_s if a_s else "?")
            demo_num2_lbl.config(text=b_s if b_s else "?")
            d_show = d_s if d_s else "?"
            demo_den1_lbl.config(text=d_show)
            demo_den2_lbl.config(text=d_show)

            # Clear result / number line if incomplete
            for w in demo_result_row.winfo_children():
                w.destroy()
            for w in demo_nl_frame.winfo_children():
                w.destroy()

            if a_v is None or b_v is None or d_v is None or d_v <= 0:
                return

            sign = "<" if a_v < b_v else (">" if a_v > b_v else "=")
            sign_color = RED if sign == "<" else (GREEN if sign == ">" else ORANGE)

            # Visual result row: [frac1]  sign  [frac2]  explanation
            frac_w(demo_result_row, a_v, d_v, CARD_Y, "small", ACCENT).pack(side="left")
            tk.Label(demo_result_row, text=f"  {sign}  ",
                     font=("Segoe UI", 32, "bold"), bg=CARD_Y,
                     fg=sign_color).pack(side="left")
            frac_w(demo_result_row, b_v, d_v, CARD_Y, "small", ACCENT2).pack(side="left")
            tk.Label(demo_result_row,
                     text=f"     бо  {a_v}  {sign}  {b_v}   "
                          f"(знаменники однакові: {d_v})",
                     font=F_BODY, bg=CARD_Y, fg=MUTED).pack(side="left", padx=16)

            # Wide number line
            nl = number_line(demo_nl_frame, d_v, a_v, b_v,
                             bg=CARD_Y, width=self.SW - 200)
            nl.config(width=self.SW - 200)
            nl.pack(fill="x")

        def _demo_key(ch):
            field = demo_state["field"]
            cur = demo_state[field]
            if ch.isdigit():
                if len(cur) < 3:
                    demo_state[field] = cur + ch
            elif ch == "⌫":
                demo_state[field] = cur[:-1]
            elif ch == "C":
                demo_state[field] = ""
            _update_demo_display()

        # Mini numpad
        np_f = tk.Frame(demo_f, bg=CARD_Y)
        np_f.pack(anchor="w", pady=4)
        for row_chars in [("7","8","9"),("4","5","6"),("1","2","3"),("C","0","⌫")]:
            rf = tk.Frame(np_f, bg=CARD_Y)
            rf.pack(pady=3)
            for ch in row_chars:
                if ch.isdigit():   bc, fc = BTN_NUM, TEXT
                elif ch == "C":    bc, fc = RED_LT,  RED
                else:              bc, fc = CARD_V,  ACCENT2
                b = tk.Button(rf, text=ch,
                              font=("Segoe UI", 20, "bold"),
                              width=4, height=1,
                              bg=bc, fg=fc, relief="flat", cursor="hand2",
                              command=lambda c=ch: _demo_key(c))
                b.pack(side="left", padx=4)
                orig = bc
                b.bind("<Enter>", lambda e, x=b, o=orig: x.config(bg=_darken(o, 18)))
                b.bind("<Leave>", lambda e, x=b, o=orig: x.config(bg=o))

        # Activate first field by default
        activate_field("a")

        theory_card(p, "💡  Запам'ятай",
                    "Щоб порівняти дроби з однаковими знаменниками:\n"
                    "1. Подивись тільки на ЧИСЕЛЬНИКИ.\n"
                    "2. Більший чисельник → більший дріб.\n"
                    "3. Менший чисельник → менший дріб.\n"
                    "4. Однакові чисельники → дроби рівні.",
                    "#f1f5f9", MUTED)

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER 1 — Put the sign  <  >  =
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
        tk.Label(sbar, text="Постав знак  <  >  або  =",
                 font=("Segoe UI", 15, "bold"), bg=PANEL, fg=MUTED).pack(
            side="left", padx=10)
        tk.Label(sbar, text="Дивись лише на ЧИСЕЛЬНИКИ",
                 font=("Segoe UI", 14, "bold"), bg=PANEL, fg=ACCENT).pack(
            side="right", padx=24)

        center = tk.Frame(cf, bg=BG)
        center.pack(expand=True)

        # ── Fraction pair display ─────────────────────────────────────────
        pair_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=30, pady=18)
        pair_f.pack(pady=(16, 8))

        display_row = tk.Frame(pair_f, bg=PANEL)
        display_row.pack()

        # Left fraction
        self.t1_frac1_f = tk.Frame(display_row, bg=PANEL)
        self.t1_frac1_f.pack(side="left", padx=20)

        # Sign placeholder
        self.t1_sign_lbl = tk.Label(display_row, text="?",
                                     font=F_SIGN, bg=PANEL, fg=BTN_NUM)
        self.t1_sign_lbl.pack(side="left", padx=20)

        # Right fraction
        self.t1_frac2_f = tk.Frame(display_row, bg=PANEL)
        self.t1_frac2_f.pack(side="left", padx=20)

        # ── Bar diagrams (side by side) ───────────────────────────────────
        bars_f = tk.Frame(center, bg=BG)
        bars_f.pack(pady=8)

        self.t1_bar1_wrap = tk.Frame(bars_f, bg=BG)
        self.t1_bar1_wrap.pack(side="left", padx=20)
        self.t1_bar2_wrap = tk.Frame(bars_f, bg=BG)
        self.t1_bar2_wrap.pack(side="left", padx=20)

        # ── Answer buttons ────────────────────────────────────────────────
        signs_f = tk.Frame(center, bg=BG)
        signs_f.pack(pady=12)
        for sign_text, color in [("<", RED), ("=", ORANGE), (">", GREEN)]:
            b = tk.Button(signs_f, text=sign_text,
                          font=("Segoe UI", 48, "bold"),
                          width=3, height=1,
                          bg=BTN_NUM, fg=color,
                          relief="flat", cursor="hand2",
                          command=lambda s=sign_text: self._t1_answer(s))
            b.pack(side="left", padx=16)
            orig = BTN_NUM
            b.bind("<Enter>", lambda e, x=b, c=color: x.config(bg=_darken(BTN_NUM, 20)))
            b.bind("<Leave>", lambda e, x=b: x.config(bg=BTN_NUM))

        # ── Feedback ─────────────────────────────────────────────────────
        self.t1_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                     bg=BG, fg=ORANGE,
                                     wraplength=700, justify="center")
        self.t1_feed_lbl.pack(pady=4)

        # ── Number line (shown after answer) ─────────────────────────────
        self.t1_nl_frame = tk.Frame(center, bg=BG)
        self.t1_nl_frame.pack(pady=4)

        mkbtn(center, "▶  Наступне", self._t1_new,
              bg=ACCENT, w=14, h=2).pack(pady=8)

        self._t1_new()

    def _t1_score_text(self):
        return f"Правильно: {self.t1_score}  /  Завдань: {self.t1_attempts}"

    def _t1_new(self):
        self.t1_answered = False
        d = random.choice([4, 5, 6, 8, 10, 12])
        # Mix: some equal, mostly unequal
        if random.random() < 0.2:
            a = b = random.randint(1, d - 1)
        else:
            a = random.randint(1, d - 1)
            b = random.randint(1, d - 1)
        self.t1_a, self.t1_b, self.t1_d = a, b, d
        self.t1_attempts += 1

        # Rebuild fraction widgets
        for w in self.t1_frac1_f.winfo_children():
            w.destroy()
        for w in self.t1_frac2_f.winfo_children():
            w.destroy()
        frac_w(self.t1_frac1_f, a, d, PANEL, "big", ACCENT).pack()
        frac_w(self.t1_frac2_f, b, d, PANEL, "big", ACCENT2).pack()

        if self.t1_sign_lbl:
            self.t1_sign_lbl.config(text="?", fg=BTN_NUM)

        # Rebuild bars
        for w in self.t1_bar1_wrap.winfo_children():
            w.destroy()
        for w in self.t1_bar2_wrap.winfo_children():
            w.destroy()

        tk.Label(self.t1_bar1_wrap, text="", font=F_SMALL, bg=BG).pack()  # spacer
        fraction_bar(self.t1_bar1_wrap, a, d,
                     bg_filled=ACCENT, bg_empty=BTN_NUM,
                     cell_w=44, cell_h=44, bg=BG).pack()

        tk.Label(self.t1_bar2_wrap, text="", font=F_SMALL, bg=BG).pack()
        fraction_bar(self.t1_bar2_wrap, b, d,
                     bg_filled=ACCENT2, bg_empty=BTN_NUM,
                     cell_w=44, cell_h=44, bg=BG).pack()

        if self.t1_feed_lbl: self.t1_feed_lbl.config(text="")
        for w in self.t1_nl_frame.winfo_children():
            w.destroy()
        if self.t1_score_lbl:
            self.t1_score_lbl.config(text=self._t1_score_text())

    def _t1_answer(self, sign):
        if self.t1_answered:
            return
        self.t1_answered = True
        a, b, d = self.t1_a, self.t1_b, self.t1_d
        correct = "<" if a < b else (">" if a > b else "=")

        if sign == correct:
            self.t1_score += 1
            color = RED if correct == "<" else (GREEN if correct == ">" else ORANGE)
            if self.t1_sign_lbl:
                self.t1_sign_lbl.config(text=correct, fg=color)
            if self.t1_feed_lbl:
                self.t1_feed_lbl.config(
                    text=f"🎉  Правильно!   {a}/{d}  {correct}  {b}/{d}   "
                         f"(бо {a} {correct} {b})",
                    fg=GREEN)
        else:
            if self.t1_sign_lbl:
                color = RED if correct == "<" else (GREEN if correct == ">" else ORANGE)
                self.t1_sign_lbl.config(text=correct, fg=color)
            if self.t1_feed_lbl:
                self.t1_feed_lbl.config(
                    text=f"❌  Ні!  Правильний знак:  {correct}\n"
                         f"{a}/{d}  {correct}  {b}/{d}   (бо {a} {correct} {b})",
                    fg=RED)

        # Show number line after answer
        for w in self.t1_nl_frame.winfo_children():
            w.destroy()
        if a != b:
            nl = number_line(self.t1_nl_frame, d, a, b,
                             bg=BG, width=self.SW - 100)
            nl.pack(fill="x")

        if self.t1_score_lbl:
            self.t1_score_lbl.config(text=self._t1_score_text())

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER 2 — Sort 3 fractions (ascending)
    # Tap fractions in ascending order to build the sequence
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
        tk.Label(sbar,
                 text="Натискай дроби від НАЙМЕНШОГО до НАЙБІЛЬШОГО",
                 font=("Segoe UI", 15, "bold"), bg=PANEL, fg=MUTED).pack(
            side="left", padx=10)

        center = tk.Frame(cf, bg=BG)
        center.pack(expand=True)

        # Instructions
        instr_f = tk.Frame(center, bg=PANEL,
                           highlightbackground=BORDER, highlightthickness=1,
                           padx=24, pady=10)
        instr_f.pack(pady=(14, 8))
        tk.Label(instr_f,
                 text="Впорядкуй три дроби за зростанням:",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack()
        tk.Label(instr_f,
                 text="Натискай на дроби знизу в порядку від найменшого до найбільшого.",
                 font=F_SMALL, bg=PANEL, fg=MUTED).pack()

        # Sequence being built (top display)
        seq_header = tk.Frame(center, bg=BG)
        seq_header.pack(pady=4)
        tk.Label(seq_header, text="Твоя послідовність:",
                 font=F_BODYB, bg=BG, fg=MUTED).pack(side="left", padx=(0, 10))
        self.t2_seq_frame = tk.Frame(seq_header, bg=BG)
        self.t2_seq_frame.pack(side="left")
        self.t2_seq_lbl = tk.Label(self.t2_seq_frame, text="_ _ _",
                                    font=F_HEAD, bg=BG, fg=BTN_NUM)
        self.t2_seq_lbl.pack()

        # Fraction buttons (3 cards to tap)
        self.t2_btn_frame = tk.Frame(center, bg=BG)
        self.t2_btn_frame.pack(pady=12)

        # Bar diagrams (side by side, appear immediately)
        self.t2_bars_frame = tk.Frame(center, bg=BG)
        self.t2_bars_frame.pack(pady=6)

        # Feedback
        self.t2_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                     bg=BG, fg=ORANGE,
                                     wraplength=700, justify="center")
        self.t2_feed_lbl.pack(pady=4)

        act = tk.Frame(center, bg=BG)
        act.pack(pady=8)
        self.t2_check_btn = mkbtn(act, "✔  Перевірити", self._t2_check,
                                   bg=GREEN, w=14, h=2)
        self.t2_check_btn.pack(side="left", padx=10)
        mkbtn(act, "🔄  Скинути", self._t2_reset,
              bg=ORANGE_LT if True else BTN_NUM,
              fg=ORANGE, w=10, h=2).pack(side="left", padx=10)
        mkbtn(act, "▶  Наступне", self._t2_new,
              bg=ACCENT, w=12, h=2).pack(side="left", padx=10)

        self._t2_new()

    def _t2_score_text(self):
        return f"Правильно: {self.t2_score}  /  Завдань: {self.t2_attempts}"

    def _t2_new(self):
        d = random.choice([5, 6, 8, 10, 12])
        numers = random.sample(range(1, d), 3)
        while len(set(numers)) < 3:
            numers = random.sample(range(1, d), 3)
        self.t2_denom  = d
        self.t2_numers = numers
        self.t2_order  = []
        self.t2_attempts += 1

        self._t2_rebuild_btns()
        self._t2_rebuild_bars()
        self._t2_update_seq_display()

        if self.t2_feed_lbl:  self.t2_feed_lbl.config(text="")
        if self.t2_check_btn: self.t2_check_btn.config(state="normal", bg=GREEN)
        if self.t2_score_lbl: self.t2_score_lbl.config(text=self._t2_score_text())

    def _t2_rebuild_btns(self):
        for w in self.t2_btn_frame.winfo_children():
            w.destroy()
        self.t2_btns = []
        colors = [ACCENT, ACCENT2, TEAL]
        for idx, n in enumerate(self.t2_numers):
            color = colors[idx % len(colors)]
            b = tk.Button(self.t2_btn_frame,
                          text="",   # will contain a frame
                          font=F_FRAC,
                          width=5, height=3,
                          bg=BTN_NUM, fg=color,
                          relief="flat", cursor="hand2",
                          command=lambda i=idx: self._t2_tap(i))
            b.pack(side="left", padx=14)
            self.t2_btns.append(b)
            # Draw fraction inside button — use a label workaround with a small canvas
            b.config(text=f"{n}\n─\n{self.t2_denom}")

    def _t2_rebuild_bars(self):
        for w in self.t2_bars_frame.winfo_children():
            w.destroy()
        colors = [ACCENT, ACCENT2, TEAL]
        for idx, n in enumerate(self.t2_numers):
            col = tk.Frame(self.t2_bars_frame, bg=BG, padx=8)
            col.pack(side="left")
            fraction_bar(col, n, self.t2_denom,
                         bg_filled=colors[idx % len(colors)],
                         bg_empty=BTN_NUM,
                         cell_w=40, cell_h=36, bg=BG).pack()

    def _t2_tap(self, idx):
        if idx in self.t2_order or len(self.t2_order) >= 3:
            return
        # Check if already answered correctly
        if self.t2_check_btn and str(self.t2_check_btn["state"]) == "disabled":
            return
        self.t2_order.append(idx)
        # Grey out the tapped button
        self.t2_btns[idx].config(bg=_darken(BTN_NUM, 20), state="disabled")
        self._t2_update_seq_display()
        # Auto-check once all 3 selected
        if len(self.t2_order) == 3:
            self._t2_check()

    def _t2_update_seq_display(self):
        for w in self.t2_seq_frame.winfo_children():
            w.destroy()
        d = self.t2_denom
        colors = [ACCENT, ACCENT2, TEAL]
        if not self.t2_order:
            tk.Label(self.t2_seq_frame, text="_ _ _",
                     font=F_HEAD, bg=BG, fg=BTN_NUM).pack()
            return
        row = tk.Frame(self.t2_seq_frame, bg=BG)
        row.pack()
        for pos, idx in enumerate(self.t2_order):
            n = self.t2_numers[idx]
            frac_w(row, n, d, BG, "small", colors[idx % len(colors)]).pack(
                side="left", padx=6)
            if pos < len(self.t2_order) - 1:
                tk.Label(row, text=" < ", font=F_BODYB, bg=BG, fg=MUTED).pack(side="left")

    def _t2_reset(self):
        self.t2_order = []
        self._t2_rebuild_btns()
        self._t2_update_seq_display()
        if self.t2_feed_lbl:  self.t2_feed_lbl.config(text="")
        if self.t2_check_btn: self.t2_check_btn.config(state="normal", bg=GREEN)

    def _t2_check(self):
        if len(self.t2_order) < 3:
            if self.t2_feed_lbl:
                self.t2_feed_lbl.config(
                    text="⚠️  Натисни всі три дроби у потрібному порядку!",
                    fg=ORANGE)
            return

        d = self.t2_denom
        numers = self.t2_numers
        correct_order = sorted(range(3), key=lambda i: numers[i])
        correct_numers = sorted(numers)

        if self.t2_order == correct_order:
            self.t2_score += 1
            correct_str = "  <  ".join(f"{n}/{d}" for n in correct_numers)
            if self.t2_feed_lbl:
                self.t2_feed_lbl.config(
                    text=f"🎉  Чудово!   Правильний порядок:   {correct_str}",
                    fg=GREEN)
            if self.t2_check_btn:
                self.t2_check_btn.config(state="disabled", bg=BTN_NUM)
        else:
            correct_str = "  <  ".join(f"{n}/{d}" for n in correct_numers)
            if self.t2_feed_lbl:
                self.t2_feed_lbl.config(
                    text=f"❌  Не так!   Правильний порядок:   {correct_str}\n"
                         f"Дивись на чисельники: {sorted(numers)}",
                    fg=RED)
            if self.t2_check_btn:
                self.t2_check_btn.config(state="disabled", bg=BTN_NUM)

        if self.t2_score_lbl:
            self.t2_score_lbl.config(text=self._t2_score_text())


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
