import tkinter as tk
import random
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

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
TEAL_LT   = "#ccfbf1"
TEAL      = "#0f766e"

# ── Fonts ─────────────────────────────────────────────────────────────────────
F_TITLE  = ("Segoe UI", 34, "bold")
F_HEAD   = ("Segoe UI", 26, "bold")
F_SUB    = ("Segoe UI", 20, "bold")
F_BODY   = ("Segoe UI", 17)
F_BODYB  = ("Segoe UI", 17, "bold")
F_BIG    = ("Segoe UI", 64, "bold")
F_BTN    = ("Segoe UI", 19, "bold")
F_NAV    = ("Segoe UI", 14, "bold")
F_SCORE  = ("Segoe UI", 20, "bold")
F_FEED   = ("Segoe UI", 16)
F_NUM    = ("Segoe UI", 26, "bold")
F_SMALL  = ("Segoe UI", 13)
F_FRAC   = ("Segoe UI", 40, "bold")
F_FRAC_S = ("Segoe UI", 24, "bold")
F_MIXED  = ("Segoe UI", 40, "bold")   # for whole part of mixed number
F_STEP   = ("Segoe UI", 18, "bold")
F_STEP_V = ("Segoe UI", 18)


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


def frac_w(parent, n, d, bg=PANEL, size="big", color=ACCENT):
    sizes  = {"big": F_FRAC,  "small": F_FRAC_S}
    widths = {"big": 66,      "small": 46}
    fn = sizes.get(size, F_FRAC_S)
    bw = widths.get(size, 46)
    f = tk.Frame(parent, bg=bg)
    tk.Label(f, text=str(n), font=fn, bg=bg, fg=color).pack()
    tk.Frame(f, bg=color, height=3, width=bw).pack(pady=2)
    tk.Label(f, text=str(d), font=fn, bg=bg, fg=color).pack()
    return f


def mixed_w(parent, whole, n, d, bg=PANEL, size="big",
            color_whole=TEXT, color_frac=ACCENT):
    """Draw a mixed number: whole + fraction side by side."""
    sizes  = {"big": F_FRAC,  "small": F_FRAC_S}
    mixed  = {"big": F_MIXED, "small": ("Segoe UI", 24, "bold")}
    widths = {"big": 66,      "small": 46}
    fn = sizes.get(size, F_FRAC_S)
    wn = mixed.get(size, ("Segoe UI", 24, "bold"))
    bw = widths.get(size, 46)
    frame = tk.Frame(parent, bg=bg)
    tk.Label(frame, text=str(whole), font=wn, bg=bg, fg=color_whole).pack(side="left", padx=(0, 4))
    frac_part = tk.Frame(frame, bg=bg)
    frac_part.pack(side="left")
    tk.Label(frac_part, text=str(n), font=fn, bg=bg, fg=color_frac).pack()
    tk.Frame(frac_part, bg=color_frac, height=3, width=bw).pack(pady=2)
    tk.Label(frac_part, text=str(d), font=fn, bg=bg, fg=color_frac).pack()
    return frame


def pie_canvas(parent, numer, denom, color=ACCENT, bg=PANEL,
               radius=40, show_extra=True):
    """
    Draw numer/denom as filled pie cells (circles cut into denom slices).
    Shows full circles for whole parts, partial for remainder.
    """
    if denom <= 0:
        return tk.Frame(parent, bg=bg)
    whole = numer // denom
    rem   = numer % denom
    circles = [denom] * whole + ([rem] if rem > 0 else [])
    if not circles:
        circles = [0]

    n_circ = len(circles)
    W = n_circ * (radius * 2 + 12) + 20
    H = radius * 2 + 20
    cv = tk.Canvas(parent, bg=bg, width=W, height=H, highlightthickness=0)

    import math as _m
    cx_start = radius + 10
    for idx, filled in enumerate(circles):
        cx = cx_start + idx * (radius * 2 + 12)
        cy = H // 2
        # Background circle
        cv.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                       fill=BTN_NUM, outline=MUTED, width=1)
        if filled > 0:
            # Draw filled slices
            step = 360.0 / denom
            for s in range(filled):
                start_deg = 90 - s * step
                cv.create_arc(cx - radius, cy - radius, cx + radius, cy + radius,
                              start=start_deg, extent=-step,
                              fill=color, outline=bg, width=1, style="pieslice")
        # Outline
        cv.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                       fill="", outline=MUTED, width=2)
        # Dividers
        for s in range(denom):
            angle = _m.radians(90 - s * 360 / denom)
            cv.create_line(cx, cy,
                           cx + radius * _m.cos(angle),
                           cy - radius * _m.sin(angle),
                           fill=MUTED, width=1)
    return cv


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


# ══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("§ 37. Мішані числа")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()
        self.current_frame = None
        self.mode = None

        # ── Trainer 1: Improper → Mixed (step by step) ───────────────────
        # Given a/b, find whole and remainder
        self.t1_n = self.t1_d = 0
        self.t1_step = 1          # 1=enter whole, 2=enter remainder num
        self.t1_whole_val = 0
        self.t1_input = ""
        self.t1_score = self.t1_attempts = 0
        self.t1_done = False
        self.t1_score_lbl    = None
        self.t1_frac_frame   = None
        self.t1_step_lbl     = None
        self.t1_inp_lbl      = None
        self.t1_feed_lbl     = None
        self.t1_check_btn    = None
        self.t1_step1_res    = None   # label confirming step 1
        self.t1_result_frame = None   # shows built mixed number

        # ── Trainer 2: Mixed → Improper (step by step) ───────────────────
        # Given whole + n/d, find improper numerator (= whole*d + n)
        self.t2_whole = self.t2_n = self.t2_d = 0
        self.t2_step = 1          # 1=multiply, 2=add
        self.t2_mul_val = 0
        self.t2_input = ""
        self.t2_score = self.t2_attempts = 0
        self.t2_done = False
        self.t2_score_lbl   = None
        self.t2_mixed_frame = None
        self.t2_step_lbl    = None
        self.t2_inp_lbl     = None
        self.t2_feed_lbl    = None
        self.t2_check_btn   = None
        self.t2_step1_res   = None
        self.t2_result_frame = None

        # ── Trainer 3: Visual interactive (sliders + live pie) ───────────
        self.t3_task_type  = "imp2mix"   # "imp2mix" or "mix2imp"
        self.t3_imp_n = self.t3_imp_d = 0
        self.t3_mix_whole = self.t3_mix_n = self.t3_mix_d = 0
        # user answer vars (IntVar for +/- buttons)
        self.t3_u_whole = None
        self.t3_u_num   = None
        self.t3_u_den   = None
        self.t3_score   = 0
        self.t3_attempts = 0
        # UI refs
        self.t3_score_lbl      = None
        self.t3_task_canvas    = None   # Canvas for task display
        self.t3_task_cv_font   = ("Segoe UI", 32, "bold")
        self.t3_task_pie_cv    = None   # Canvas for task pie
        self.t3_answer_pie_cv  = None   # Canvas for answer pie (live)
        self.t3_answer_pie_frm = None   # frame containing answer pie
        self.t3_success_lbl    = None
        self.t3_new_btn        = None
        self.t3_whole_ctrl     = None
        self.t3_num_ctrl       = None
        self.t3_den_ctrl       = None

        self._build_chrome()
        self.show_main_menu()

    # ── Chrome ────────────────────────────────────────────────────────────────
    def _build_chrome(self):
        hdr = tk.Frame(self, bg=HDR_BG, height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="§ 37.   Мішані числа",
                 bg=HDR_BG, fg=WHITE,
                 font=("Segoe UI", 21, "bold")).pack(side="left", padx=30)
        mkbtn(hdr, "✕  Вийти", self.destroy, bg="#b91c1c",
              font=("Segoe UI", 13, "bold"), w=9, h=1).pack(
            side="right", padx=18, pady=16)

        nav = tk.Frame(self, bg=NAV_BG, height=52)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        for label, cmd in [
            ("🏠  Меню",                    self.show_main_menu),
            ("📖  Теорія",                  self.show_theory),
            ("🎯  Неправильний → мішане",   self.show_trainer_1),
            ("🎯  Мішане → неправильний",   self.show_trainer_2),
            ("🔵  Візуальна практика",       self.show_trainer_3),
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

        tk.Label(center, text="Мішані числа",
                 font=("Segoe UI", 50, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 4))
        tk.Label(center, text="перетворення дробів   §37",
                 font=("Segoe UI", 24), bg=BG, fg=ACCENT).pack(pady=(0, 28))

        cards = [
            ("📖", "Теорія",                   CARD_B,  ACCENT,  self.show_theory),
            ("🎯", "Неправильний\n→ мішане",    CARD_G,  GREEN,   self.show_trainer_1),
            ("🎯", "Мішане\n→ неправильний",    CARD_V,  ACCENT2, self.show_trainer_2),
            ("🔵", "Візуальна\nпрактика",       CARD_Y,  ORANGE,  self.show_trainer_3),
        ]
        row = tk.Frame(center, bg=BG)
        row.pack()
        for icon, title, bg_c, fg_c, cmd in cards:
            c = tk.Frame(row, bg=bg_c, width=230, height=200,
                         highlightbackground=BORDER, highlightthickness=2)
            c.pack(side="left", padx=16)
            c.pack_propagate(False)
            tk.Label(c, text=icon, font=("Segoe UI", 40), bg=bg_c, fg=fg_c).pack(pady=(22, 4))
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

        tk.Label(p, text="Мішані числа", font=F_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        hline(p, ACCENT)

        # ── Definition ────────────────────────────────────────────────────
        def_f = tk.Frame(p, bg=CARD_B, padx=22, pady=16,
                         highlightbackground=ACCENT, highlightthickness=2)
        def_f.pack(fill="x", pady=8)
        tk.Label(def_f, text="📌  Означення",
                 font=F_SUB, bg=CARD_B, fg=ACCENT).pack(anchor="w")
        tk.Label(def_f,
                 text="Неправильний дріб, записаний у вигляді ЦІЛОЇ і ДРОБОВОЇ частин,\n"
                      "називають МІШАНИМ ЧИСЛОМ.",
                 font=F_BODY, bg=CARD_B, fg=TEXT, justify="left").pack(anchor="w", pady=(8, 6))

        eg_row = tk.Frame(def_f, bg=CARD_B)
        eg_row.pack(anchor="w", pady=4)
        tk.Label(eg_row, text="Приклади мішаних чисел:  ",
                 font=F_BODY, bg=CARD_B, fg=MUTED).pack(side="left")
        for w, n, d in [(1, 3, 8), (7, 2, 5), (200, 1, 4), (1, 1, 25)]:
            mixed_w(eg_row, w, n, d, CARD_B, "small", TEXT, ACCENT).pack(
                side="left", padx=10)

        # Parts annotation
        annot_f = tk.Frame(def_f, bg=CARD_B, pady=6)
        annot_f.pack(anchor="w")
        mixed_w(annot_f, 1, 3, 8, CARD_B, "big", GREEN, ACCENT2).pack(side="left")
        ann_text = tk.Frame(annot_f, bg=CARD_B)
        ann_text.pack(side="left", padx=24)
        tk.Label(ann_text, text="1  — ціла частина (зелена)",
                 font=F_BODYB, bg=CARD_B, fg=GREEN).pack(anchor="w")
        tk.Label(ann_text, text="3/8  — дробова частина (фіолетова)",
                 font=F_BODYB, bg=CARD_B, fg=ACCENT2).pack(anchor="w")

        # ── Improper → Mixed: algorithm ───────────────────────────────────
        alg1_f = tk.Frame(p, bg=CARD_G, padx=22, pady=18,
                          highlightbackground=GREEN, highlightthickness=2)
        alg1_f.pack(fill="x", pady=8)
        tk.Label(alg1_f, text="🔑  Неправильний дріб  →  мішане число",
                 font=F_SUB, bg=CARD_G, fg=GREEN).pack(anchor="w")

        tk.Label(alg1_f,
                 text="Поділи чисельник на знаменник із остачею:",
                 font=F_BODY, bg=CARD_G, fg=TEXT).pack(anchor="w", pady=(8, 4))

        for i, (step, color, txt) in enumerate([
            ("Крок 1", ACCENT,  "Неповна частка → ціла частина мішаного числа"),
            ("Крок 2", ACCENT2, "Остача → чисельник дробової частини"),
            ("Крок 3", MUTED,   "Знаменник залишається тим самим"),
        ]):
            row = tk.Frame(alg1_f, bg=CARD_G)
            row.pack(anchor="w", pady=3)
            tk.Label(row, text=f"  {step}:  ", font=F_STEP, bg=CARD_G,
                     fg=color, width=10, anchor="w").pack(side="left")
            tk.Label(row, text=txt, font=F_STEP_V, bg=CARD_G, fg=TEXT).pack(side="left")

        # Example 11/8
        ex1_f = tk.Frame(alg1_f, bg=PANEL, padx=16, pady=12,
                         highlightbackground=BORDER, highlightthickness=1)
        ex1_f.pack(fill="x", pady=10)
        ex1_title = tk.Frame(ex1_f, bg=PANEL)
        ex1_title.pack(anchor="w")
        tk.Label(ex1_title, text="Приклад:  ", font=F_BODYB, bg=PANEL, fg=TEXT).pack(side="left")
        frac_w(ex1_title, 11, 8, PANEL, "small", ACCENT).pack(side="left", padx=6)
        tk.Label(ex1_title, text="  →  ?", font=F_BODYB, bg=PANEL, fg=TEXT).pack(side="left")

        for label, color, calc, explain in [
            ("Крок 1", ACCENT,  "11  :  8  =  1  (остача 3)", "Ціла частина = 1"),
            ("Крок 2", ACCENT2, "Остача = 3",                  "Чисельник дробової частини = 3"),
            ("Крок 3", MUTED,   "Знаменник = 8",               "Залишається"),
        ]:
            row = tk.Frame(ex1_f, bg=CARD_G, padx=14, pady=7,
                           highlightbackground=BORDER, highlightthickness=1)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, font=F_STEP, bg=CARD_G, fg=color,
                     width=8, anchor="w").pack(side="left")
            tk.Label(row, text=calc, font=("Segoe UI", 18, "bold"),
                     bg=CARD_G, fg=color).pack(side="left", padx=12)
            tk.Label(row, text=f"({explain})", font=F_SMALL,
                     bg=CARD_G, fg=MUTED).pack(side="left")

        ans1 = tk.Frame(ex1_f, bg=PANEL)
        ans1.pack(anchor="w", pady=8)
        tk.Label(ans1, text="Відповідь:  ", font=F_HEAD, bg=PANEL, fg=TEXT).pack(side="left")
        frac_w(ans1, 11, 8, PANEL, "small", ACCENT).pack(side="left", padx=6)
        tk.Label(ans1, text="  =  ", font=F_HEAD, bg=PANEL, fg=MUTED).pack(side="left")
        mixed_w(ans1, 1, 3, 8, PANEL, "big", GREEN, ACCENT2).pack(side="left", padx=6)

        # Example 42/5
        ex2_f = tk.Frame(alg1_f, bg=CARD_Y, padx=16, pady=12,
                         highlightbackground=BORDER, highlightthickness=1)
        ex2_f.pack(fill="x", pady=6)
        ex2_r = tk.Frame(ex2_f, bg=CARD_Y)
        ex2_r.pack(anchor="w")
        tk.Label(ex2_r, text="Ще приклад:  ", font=F_BODYB, bg=CARD_Y, fg=TEXT).pack(side="left")
        frac_w(ex2_r, 42, 5, CARD_Y, "small", ACCENT).pack(side="left", padx=6)
        tk.Label(ex2_r, text="  →  42 : 5 = 8 (остача 2)  →  ",
                 font=F_BODY, bg=CARD_Y, fg=TEXT).pack(side="left")
        mixed_w(ex2_r, 8, 2, 5, CARD_Y, "big", GREEN, ACCENT2).pack(side="left", padx=6)

        # ── Mixed → Improper: algorithm ───────────────────────────────────
        alg2_f = tk.Frame(p, bg=CARD_V, padx=22, pady=18,
                          highlightbackground=ACCENT2, highlightthickness=2)
        alg2_f.pack(fill="x", pady=8)
        tk.Label(alg2_f, text="🔑  Мішане число  →  неправильний дріб",
                 font=F_SUB, bg=CARD_V, fg=ACCENT2).pack(anchor="w")

        tk.Label(alg2_f,
                 text="Знайди новий чисельник:",
                 font=F_BODY, bg=CARD_V, fg=TEXT).pack(anchor="w", pady=(8, 4))

        for step, color, txt in [
            ("Крок 1", ACCENT,  "Ціла частина  ×  знаменник"),
            ("Крок 2", ACCENT2, "Додай чисельник дробової частини  →  новий чисельник"),
            ("Крок 3", MUTED,   "Знаменник залишається тим самим"),
        ]:
            row = tk.Frame(alg2_f, bg=CARD_V)
            row.pack(anchor="w", pady=3)
            tk.Label(row, text=f"  {step}:  ", font=F_STEP, bg=CARD_V,
                     fg=color, width=10, anchor="w").pack(side="left")
            tk.Label(row, text=txt, font=F_STEP_V, bg=CARD_V, fg=TEXT).pack(side="left")

        ex3_f = tk.Frame(alg2_f, bg=PANEL, padx=16, pady=12,
                         highlightbackground=BORDER, highlightthickness=1)
        ex3_f.pack(fill="x", pady=10)
        ex3_title = tk.Frame(ex3_f, bg=PANEL)
        ex3_title.pack(anchor="w")
        tk.Label(ex3_title, text="Приклад:  ", font=F_BODYB, bg=PANEL, fg=TEXT).pack(side="left")
        mixed_w(ex3_title, 2, 3, 7, PANEL, "small", TEXT, ACCENT).pack(side="left", padx=6)
        tk.Label(ex3_title, text="  →  ?", font=F_BODYB, bg=PANEL, fg=TEXT).pack(side="left")

        for label, color, calc, explain in [
            ("Крок 1", ACCENT,  "2  ×  7  =  14", "Ціла × знаменник"),
            ("Крок 2", ACCENT2, "14 + 3  =  17",   "Новий чисельник"),
            ("Крок 3", MUTED,   "Знаменник = 7",   "Незмінний"),
        ]:
            row = tk.Frame(ex3_f, bg=CARD_V, padx=14, pady=7,
                           highlightbackground=BORDER, highlightthickness=1)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, font=F_STEP, bg=CARD_V, fg=color,
                     width=8, anchor="w").pack(side="left")
            tk.Label(row, text=calc, font=("Segoe UI", 18, "bold"),
                     bg=CARD_V, fg=color).pack(side="left", padx=12)
            tk.Label(row, text=f"({explain})", font=F_SMALL,
                     bg=CARD_V, fg=MUTED).pack(side="left")

        ans3 = tk.Frame(ex3_f, bg=PANEL)
        ans3.pack(anchor="w", pady=8)
        tk.Label(ans3, text="Відповідь:  ", font=F_HEAD, bg=PANEL, fg=TEXT).pack(side="left")
        mixed_w(ans3, 2, 3, 7, PANEL, "big", GREEN, ACCENT2).pack(side="left", padx=6)
        tk.Label(ans3, text="  =  ", font=F_HEAD, bg=PANEL, fg=MUTED).pack(side="left")
        frac_w(ans3, 17, 7, PANEL, "small", ACCENT).pack(side="left", padx=6)

        # ── Special cases ────────────────────────────────────────────────
        spec_f = tk.Frame(p, bg=CARD_Y, padx=22, pady=16,
                          highlightbackground=BORDER, highlightthickness=1)
        spec_f.pack(fill="x", pady=8)
        tk.Label(spec_f, text="⚡  Особливі випадки",
                 font=F_SUB, bg=CARD_Y, fg=ORANGE).pack(anchor="w", pady=(0, 8))

        cases = [
            ("Чисельник ділиться на знаменник без остачі →  натуральне число",
             [(6, 3, "= 2"), (15, 5, "= 3"), (12, 4, "= 3")]),
            ("Правильний дріб:  ціла частина = 0  (немає цілої частини)",
             [(3, 8, "< 1"), (1, 2, "< 1")]),
        ]
        for desc, examples in cases:
            tk.Label(spec_f, text=desc, font=F_BODYB, bg=CARD_Y, fg=TEXT,
                     anchor="w").pack(anchor="w", pady=(4, 2))
            row = tk.Frame(spec_f, bg=CARD_Y)
            row.pack(anchor="w", pady=(0, 8))
            for n, d, result in examples:
                frac_w(row, n, d, CARD_Y, "small", ACCENT).pack(side="left", padx=4)
                tk.Label(row, text=f" {result}   ", font=F_BODY,
                         bg=CARD_Y, fg=GREEN).pack(side="left")

        # ── Visual: pie circles ───────────────────────────────────────────
        vis_f = tk.Frame(p, bg=PANEL, padx=22, pady=18,
                         highlightbackground=BORDER, highlightthickness=1)
        vis_f.pack(fill="x", pady=8)
        tk.Label(vis_f, text="🔵  Наочно: неправильний дріб як кола",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(anchor="w", pady=(0, 10))

        pie_examples = [(11, 8), (7, 3), (5, 4)]
        pie_row = tk.Frame(vis_f, bg=PANEL)
        pie_row.pack(anchor="w")
        for n, d in pie_examples:
            col = tk.Frame(pie_row, bg=PANEL, padx=16)
            col.pack(side="left")
            fr_row = tk.Frame(col, bg=PANEL)
            fr_row.pack()
            frac_w(fr_row, n, d, PANEL, "small", ACCENT).pack(side="left")
            tk.Label(fr_row, text="  =  ", font=F_BODY, bg=PANEL, fg=MUTED).pack(side="left")
            whole = n // d
            rem   = n % d
            if rem:
                mixed_w(fr_row, whole, rem, d, PANEL, "small", GREEN, ACCENT2).pack(side="left")
            else:
                tk.Label(fr_row, text=str(whole), font=F_FRAC_S,
                         bg=PANEL, fg=GREEN).pack(side="left")
            pie_canvas(col, n, d, ACCENT, PANEL, radius=34).pack(pady=4)

        theory_card(p, "💡  Запам'ятай",
                    "Неправильний → мішане:   ділимо чисельник на знаменник.\n"
                    "   Частка → ціла частина.   Остача → чисельник дробової частини.\n\n"
                    "Мішане → неправильний:   ціла × знаменник + чисельник = новий чисельник.\n"
                    "   Знаменник не змінюється.",
                    "#f1f5f9", MUTED)

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER 1 — Improper → Mixed  (two explicit steps)
    # ══════════════════════════════════════════════════════════════════════════
    def show_trainer_1(self):
        self.clear_main()
        self.mode = "trainer1"
        self.t1_done = False

        cf = self.current_frame

        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.t1_score_lbl = tk.Label(sbar,
            text=self._t1_score_text(), font=F_SCORE, bg=PANEL, fg=GREEN)
        self.t1_score_lbl.pack(side="left", padx=30)
        tk.Label(sbar, text="Запиши неправильний дріб як мішане число  (2 кроки)",
                 font=("Segoe UI", 15, "bold"), bg=PANEL, fg=MUTED).pack(side="left", padx=10)
        tk.Label(sbar, text="Алгоритм:  ÷  →  частка (ціла)  +  остача (чисельник)",
                 font=("Segoe UI", 13, "bold"), bg=PANEL, fg=GREEN).pack(side="right", padx=20)

        # ── 2-step banner ─────────────────────────────────────────────────
        center = tk.Frame(cf, bg=BG)
        center.pack(expand=True)

        banner = tk.Frame(center, bg=CARD_G, padx=18, pady=8,
                          highlightbackground=GREEN, highlightthickness=2)
        banner.pack(fill="x", padx=40, pady=(10, 4))
        tk.Label(banner,
                 text="📋  Крок 1 → введи ЦІЛУ ЧАСТИНУ (частка від ділення) і натисни «Перевірити»\n"
                      "     Крок 2 → введи ЧИСЕЛЬНИК дробової частини (остача) і натисни «Перевірити»",
                 font=("Segoe UI", 14, "bold"), bg=CARD_G, fg=GREEN,
                 justify="center").pack()

        # Task display
        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=28, pady=16)
        task_f.pack(pady=(8, 4))
        tk.Label(task_f, text="Запиши як мішане число:",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack()
        self.t1_frac_frame = tk.Frame(task_f, bg=PANEL)
        self.t1_frac_frame.pack(pady=8)

        # Step boxes
        steps_row = tk.Frame(center, bg=BG)
        steps_row.pack(pady=6)
        self.t1_step_boxes = []
        for label, desc in [("Крок 1", "Ціла частина = ?"),
                             ("Крок 2", "Чисельник (остача) = ?")]:
            box = tk.Frame(steps_row, bg=BTN_NUM, padx=18, pady=10,
                           highlightbackground=BORDER, highlightthickness=1, width=300)
            box.pack(side="left", padx=10)
            box.pack_propagate(False)
            tk.Label(box, text=label, font=F_STEP, bg=BTN_NUM, fg=MUTED).pack()
            lbl = tk.Label(box, text=desc, font=F_STEP_V, bg=BTN_NUM, fg=MUTED)
            lbl.pack()
            self.t1_step_boxes.append((box, lbl))

        # Step 1 confirmed result
        self.t1_step1_res = tk.Label(center, text="",
                                      font=("Segoe UI", 17, "bold"), bg=BG, fg=GREEN)
        self.t1_step1_res.pack(pady=2)

        # Current step instruction
        self.t1_step_lbl = tk.Label(center, text="", font=F_SUB, bg=BG, fg=ACCENT)
        self.t1_step_lbl.pack(pady=4)

        # Input display
        inp_f = tk.Frame(center, bg=BTN_NUM,
                         highlightbackground=ACCENT, highlightthickness=2,
                         padx=14, pady=6)
        inp_f.pack(pady=4)
        tk.Label(inp_f, text="Відповідь:", font=F_BODYB, bg=BTN_NUM, fg=MUTED).pack(side="left")
        self.t1_inp_lbl = tk.Label(inp_f, text="",
                                    font=("Segoe UI", 44, "bold"),
                                    bg=BTN_NUM, fg=ACCENT, width=4)
        self.t1_inp_lbl.pack(side="left", padx=10)

        # Result display (shown after both steps done)
        self.t1_result_frame = tk.Frame(center, bg=BG)
        self.t1_result_frame.pack(pady=4)

        self.t1_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                     bg=BG, fg=ORANGE,
                                     wraplength=680, justify="center")
        self.t1_feed_lbl.pack(pady=4)

        build_numpad(center, self._t1_key).pack(pady=6)

        act = tk.Frame(center, bg=BG)
        act.pack(pady=8)
        self.t1_check_btn = mkbtn(act, "✔  Перевірити", self._t1_check,
                                   bg=GREEN, w=14, h=2)
        self.t1_check_btn.pack(side="left", padx=10)
        mkbtn(act, "▶  Наступне", self._t1_new, bg=ACCENT, w=12, h=2).pack(side="left", padx=10)

        self._t1_new()

    def _t1_score_text(self):
        return f"Правильно: {self.t1_score}  /  Завдань: {self.t1_attempts}"

    def _t1_new(self):
        d = random.randint(2, 10)
        # Ensure remainder != 0
        while True:
            n = random.randint(d + 1, d * 6)
            if n % d != 0:
                break
        self.t1_n, self.t1_d = n, d
        self.t1_step = 1
        self.t1_input = ""
        self.t1_whole_val = 0
        self.t1_done = False
        self.t1_attempts += 1

        for w in self.t1_frac_frame.winfo_children():
            w.destroy()
        frac_w(self.t1_frac_frame, n, d, PANEL, "big", ACCENT).pack()

        for w in self.t1_result_frame.winfo_children():
            w.destroy()
        if self.t1_step1_res: self.t1_step1_res.config(text="")
        if self.t1_inp_lbl:   self.t1_inp_lbl.config(text="", fg=ACCENT)
        if self.t1_feed_lbl:  self.t1_feed_lbl.config(text="")
        if self.t1_check_btn: self.t1_check_btn.config(state="normal", bg=GREEN)
        if self.t1_score_lbl: self.t1_score_lbl.config(text=self._t1_score_text())
        self._t1_set_step_label()
        self._t1_highlight_step(1)

    def _t1_highlight_step(self, step):
        for i, (box, lbl) in enumerate(self.t1_step_boxes):
            if i + 1 == step:
                box.config(bg=CARD_G, highlightbackground=GREEN, highlightthickness=2)
                lbl.config(bg=CARD_G, fg=GREEN)
                box.winfo_children()[0].config(bg=CARD_G, fg=GREEN)
            else:
                box.config(bg=BTN_NUM, highlightbackground=BORDER, highlightthickness=1)
                lbl.config(bg=BTN_NUM, fg=MUTED)
                box.winfo_children()[0].config(bg=BTN_NUM, fg=MUTED)

    def _t1_set_step_label(self):
        n, d = self.t1_n, self.t1_d
        if self.t1_step == 1:
            if self.t1_step_lbl:
                self.t1_step_lbl.config(
                    text=f"Крок 1:   {n}  :  {d}  =  ?  (неповна частка — ціла частина)",
                    fg=ACCENT)
        else:
            whole = self.t1_whole_val
            if self.t1_step_lbl:
                self.t1_step_lbl.config(
                    text=f"Крок 2:   {n}  -  {whole} × {d}  =  ?  (остача — чисельник дробової)",
                    fg=ACCENT2)

    def _t1_key(self, ch):
        if self.t1_done: return
        if ch.isdigit():
            if len(self.t1_input) < 5: self.t1_input += ch
        elif ch == "⌫": self.t1_input = self.t1_input[:-1]
        elif ch == "C":  self.t1_input = ""
        if self.t1_inp_lbl: self.t1_inp_lbl.config(text=self.t1_input)

    def _t1_check(self):
        if not self.t1_input.strip():
            if self.t1_feed_lbl:
                self.t1_feed_lbl.config(text="⚠️  Введіть число!", fg=ORANGE)
            return
        val = int(self.t1_input)
        self.t1_input = ""
        if self.t1_inp_lbl: self.t1_inp_lbl.config(text="")

        n, d = self.t1_n, self.t1_d
        correct_whole = n // d
        correct_rem   = n % d

        if self.t1_step == 1:
            if val == correct_whole:
                self.t1_whole_val = val
                self.t1_step = 2
                if self.t1_step1_res:
                    self.t1_step1_res.config(
                        text=f"✅  Крок 1:   {n} ÷ {d} = {val}  (ціла частина знайдена!)",
                        fg=GREEN)
                if self.t1_feed_lbl:
                    self.t1_feed_lbl.config(
                        text=f"Правильно!  Тепер введи ОСТАЧУ:   {n} - {val}×{d} = ?",
                        fg=GREEN)
                self._t1_set_step_label()
                self._t1_highlight_step(2)
            else:
                if self.t1_feed_lbl:
                    self.t1_feed_lbl.config(
                        text=f"❌  {n} ÷ {d} ≠ {val}.   Підказка: {n} ÷ {d} = {correct_whole} (остача {correct_rem})",
                        fg=RED)
        else:
            if val == correct_rem:
                self.t1_score += 1
                self.t1_done = True
                if self.t1_check_btn: self.t1_check_btn.config(state="disabled", bg=BTN_NUM)
                if self.t1_feed_lbl:
                    self.t1_feed_lbl.config(
                        text=f"🎉  Чудово!   {n}/{d}  =  {correct_whole}  і  {correct_rem}/{d}",
                        fg=GREEN)
                # Show the resulting mixed number visually
                for w in self.t1_result_frame.winfo_children():
                    w.destroy()
                res_row = tk.Frame(self.t1_result_frame, bg=BG)
                res_row.pack()
                frac_w(res_row, n, d, BG, "small", ACCENT).pack(side="left")
                tk.Label(res_row, text="  =  ", font=F_HEAD, bg=BG, fg=MUTED).pack(side="left")
                mixed_w(res_row, correct_whole, correct_rem, d,
                        BG, "big", GREEN, ACCENT2).pack(side="left", padx=6)
                # Pie circles
                pie_canvas(self.t1_result_frame, n, d, ACCENT, BG, radius=28).pack(pady=4)
            else:
                if self.t1_feed_lbl:
                    self.t1_feed_lbl.config(
                        text=f"❌  Остача від ділення {n} ÷ {d} ≠ {val}.   "
                             f"Порахуй: {n} - {self.t1_whole_val}×{d} = {n - self.t1_whole_val*d}",
                        fg=RED)

        if self.t1_score_lbl: self.t1_score_lbl.config(text=self._t1_score_text())

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER 2 — Mixed → Improper  (two explicit steps)
    # ══════════════════════════════════════════════════════════════════════════
    def show_trainer_2(self):
        self.clear_main()
        self.mode = "trainer2"
        self.t2_done = False

        cf = self.current_frame

        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.t2_score_lbl = tk.Label(sbar,
            text=self._t2_score_text(), font=F_SCORE, bg=PANEL, fg=GREEN)
        self.t2_score_lbl.pack(side="left", padx=30)
        tk.Label(sbar, text="Запиши мішане число як неправильний дріб  (2 кроки)",
                 font=("Segoe UI", 15, "bold"), bg=PANEL, fg=MUTED).pack(side="left", padx=10)
        tk.Label(sbar, text="Алгоритм:  ціла × знаменник  +  чисельник",
                 font=("Segoe UI", 13, "bold"), bg=PANEL, fg=ACCENT2).pack(side="right", padx=20)

        center = tk.Frame(cf, bg=BG)
        center.pack(expand=True)

        # Banner
        banner = tk.Frame(center, bg=CARD_V, padx=18, pady=8,
                          highlightbackground=ACCENT2, highlightthickness=2)
        banner.pack(fill="x", padx=40, pady=(10, 4))
        tk.Label(banner,
                 text="📋  Крок 1 → введи добуток  (ціла × знаменник)  і натисни «Перевірити»\n"
                      "     Крок 2 → введи нову цілу ЧИСЕЛЬНИКА  (добуток + чисельник)  і натисни «Перевірити»",
                 font=("Segoe UI", 14, "bold"), bg=CARD_V, fg=ACCENT2,
                 justify="center").pack()

        # Task display
        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=28, pady=16)
        task_f.pack(pady=(8, 4))
        tk.Label(task_f, text="Запиши як неправильний дріб:",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack()
        self.t2_mixed_frame = tk.Frame(task_f, bg=PANEL)
        self.t2_mixed_frame.pack(pady=8)

        # Step boxes
        steps_row = tk.Frame(center, bg=BG)
        steps_row.pack(pady=6)
        self.t2_step_boxes = []
        for label, desc in [("Крок 1", "Ціла × знаменник = ?"),
                             ("Крок 2", "Результат + чисельник = ?")]:
            box = tk.Frame(steps_row, bg=BTN_NUM, padx=18, pady=10,
                           highlightbackground=BORDER, highlightthickness=1, width=300)
            box.pack(side="left", padx=10)
            box.pack_propagate(False)
            tk.Label(box, text=label, font=F_STEP, bg=BTN_NUM, fg=MUTED).pack()
            lbl = tk.Label(box, text=desc, font=F_STEP_V, bg=BTN_NUM, fg=MUTED)
            lbl.pack()
            self.t2_step_boxes.append((box, lbl))

        self.t2_step1_res = tk.Label(center, text="",
                                      font=("Segoe UI", 17, "bold"), bg=BG, fg=GREEN)
        self.t2_step1_res.pack(pady=2)

        self.t2_step_lbl = tk.Label(center, text="", font=F_SUB, bg=BG, fg=ACCENT2)
        self.t2_step_lbl.pack(pady=4)

        inp_f = tk.Frame(center, bg=BTN_NUM,
                         highlightbackground=ACCENT2, highlightthickness=2,
                         padx=14, pady=6)
        inp_f.pack(pady=4)
        tk.Label(inp_f, text="Відповідь:", font=F_BODYB, bg=BTN_NUM, fg=MUTED).pack(side="left")
        self.t2_inp_lbl = tk.Label(inp_f, text="",
                                    font=("Segoe UI", 44, "bold"),
                                    bg=BTN_NUM, fg=ACCENT2, width=4)
        self.t2_inp_lbl.pack(side="left", padx=10)

        self.t2_result_frame = tk.Frame(center, bg=BG)
        self.t2_result_frame.pack(pady=4)

        self.t2_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                     bg=BG, fg=ORANGE,
                                     wraplength=680, justify="center")
        self.t2_feed_lbl.pack(pady=4)

        build_numpad(center, self._t2_key).pack(pady=6)

        act = tk.Frame(center, bg=BG)
        act.pack(pady=8)
        self.t2_check_btn = mkbtn(act, "✔  Перевірити", self._t2_check,
                                   bg=GREEN, w=14, h=2)
        self.t2_check_btn.pack(side="left", padx=10)
        mkbtn(act, "▶  Наступне", self._t2_new, bg=ACCENT2, w=12, h=2).pack(side="left", padx=10)

        self._t2_new()

    def _t2_score_text(self):
        return f"Правильно: {self.t2_score}  /  Завдань: {self.t2_attempts}"

    def _t2_new(self):
        d = random.randint(2, 10)
        n = random.randint(1, d - 1)
        whole = random.randint(1, 8)
        self.t2_whole, self.t2_n, self.t2_d = whole, n, d
        self.t2_step = 1
        self.t2_input = ""
        self.t2_mul_val = 0
        self.t2_done = False
        self.t2_attempts += 1

        for w in self.t2_mixed_frame.winfo_children():
            w.destroy()
        mixed_w(self.t2_mixed_frame, whole, n, d, PANEL, "big", GREEN, ACCENT2).pack()

        for w in self.t2_result_frame.winfo_children():
            w.destroy()
        if self.t2_step1_res: self.t2_step1_res.config(text="")
        if self.t2_inp_lbl:   self.t2_inp_lbl.config(text="", fg=ACCENT2)
        if self.t2_feed_lbl:  self.t2_feed_lbl.config(text="")
        if self.t2_check_btn: self.t2_check_btn.config(state="normal", bg=GREEN)
        if self.t2_score_lbl: self.t2_score_lbl.config(text=self._t2_score_text())
        self._t2_set_step_label()
        self._t2_highlight_step(1)

    def _t2_highlight_step(self, step):
        for i, (box, lbl) in enumerate(self.t2_step_boxes):
            if i + 1 == step:
                box.config(bg=CARD_V, highlightbackground=ACCENT2, highlightthickness=2)
                lbl.config(bg=CARD_V, fg=ACCENT2)
                box.winfo_children()[0].config(bg=CARD_V, fg=ACCENT2)
            else:
                box.config(bg=BTN_NUM, highlightbackground=BORDER, highlightthickness=1)
                lbl.config(bg=BTN_NUM, fg=MUTED)
                box.winfo_children()[0].config(bg=BTN_NUM, fg=MUTED)

    def _t2_set_step_label(self):
        w, n, d = self.t2_whole, self.t2_n, self.t2_d
        if self.t2_step == 1:
            if self.t2_step_lbl:
                self.t2_step_lbl.config(
                    text=f"Крок 1:   {w}  ×  {d}  =  ?   (ціла частина × знаменник)",
                    fg=ACCENT)
        else:
            mul = self.t2_mul_val
            if self.t2_step_lbl:
                self.t2_step_lbl.config(
                    text=f"Крок 2:   {mul}  +  {n}  =  ?   (добуток + чисельник = новий чисельник)",
                    fg=ACCENT2)

    def _t2_key(self, ch):
        if self.t2_done: return
        if ch.isdigit():
            if len(self.t2_input) < 5: self.t2_input += ch
        elif ch == "⌫": self.t2_input = self.t2_input[:-1]
        elif ch == "C":  self.t2_input = ""
        if self.t2_inp_lbl: self.t2_inp_lbl.config(text=self.t2_input)

    def _t2_check(self):
        if not self.t2_input.strip():
            if self.t2_feed_lbl:
                self.t2_feed_lbl.config(text="⚠️  Введіть число!", fg=ORANGE)
            return
        val = int(self.t2_input)
        self.t2_input = ""
        if self.t2_inp_lbl: self.t2_inp_lbl.config(text="")

        w, n, d = self.t2_whole, self.t2_n, self.t2_d
        correct_mul  = w * d
        correct_num  = correct_mul + n

        if self.t2_step == 1:
            if val == correct_mul:
                self.t2_mul_val = val
                self.t2_step = 2
                if self.t2_step1_res:
                    self.t2_step1_res.config(
                        text=f"✅  Крок 1:   {w} × {d} = {val}   (добуток знайдено!)",
                        fg=GREEN)
                if self.t2_feed_lbl:
                    self.t2_feed_lbl.config(
                        text=f"Правильно!  Тепер додай чисельник:   {val} + {n} = ?",
                        fg=GREEN)
                self._t2_set_step_label()
                self._t2_highlight_step(2)
            else:
                if self.t2_feed_lbl:
                    self.t2_feed_lbl.config(
                        text=f"❌  {w} × {d} ≠ {val}.   Правильно: {w} × {d} = {correct_mul}",
                        fg=RED)
        else:
            if val == correct_num:
                self.t2_score += 1
                self.t2_done = True
                if self.t2_check_btn: self.t2_check_btn.config(state="disabled", bg=BTN_NUM)
                if self.t2_feed_lbl:
                    self.t2_feed_lbl.config(
                        text=f"🎉  Чудово!   {w} і {n}/{d}  =  {correct_num}/{d}",
                        fg=GREEN)
                # Show result visually
                for w2 in self.t2_result_frame.winfo_children():
                    w2.destroy()
                res_row = tk.Frame(self.t2_result_frame, bg=BG)
                res_row.pack()
                mixed_w(res_row, w, n, d, BG, "big", GREEN, ACCENT2).pack(side="left")
                tk.Label(res_row, text="  =  ", font=F_HEAD, bg=BG, fg=MUTED).pack(side="left")
                frac_w(res_row, correct_num, d, BG, "small", ACCENT).pack(side="left", padx=6)
                pie_canvas(self.t2_result_frame, correct_num, d, ACCENT, BG, radius=28).pack(pady=4)
            else:
                if self.t2_feed_lbl:
                    self.t2_feed_lbl.config(
                        text=f"❌  {self.t2_mul_val} + {n} ≠ {val}.   "
                             f"Правильно: {self.t2_mul_val} + {n} = {correct_num}",
                        fg=RED)

        if self.t2_score_lbl: self.t2_score_lbl.config(text=self._t2_score_text())

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER 3 — Visual interactive: live pie + +/- controls
    # Inspired by the matplotlib version, rewritten in pure tkinter.
    # Task and answer both shown as pie-circle diagrams that update live.
    # ══════════════════════════════════════════════════════════════════════════
    def show_trainer_3(self):
        self.clear_main()
        self.mode = "trainer3"

        # Init IntVars
        self.t3_u_whole = tk.IntVar(value=0)
        self.t3_u_num   = tk.IntVar(value=0)
        self.t3_u_den   = tk.IntVar(value=1)

        cf = self.current_frame

        # ── Score bar ─────────────────────────────────────────────────────
        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.t3_score_lbl = tk.Label(sbar,
            text=self._t3_score_text(), font=F_SCORE, bg=PANEL, fg=GREEN)
        self.t3_score_lbl.pack(side="left", padx=30)
        tk.Label(sbar, text="🔵  Візуальна практика — зміни числа, кружечки оновляться",
                 font=("Segoe UI", 15, "bold"), bg=PANEL, fg=ORANGE).pack(side="left", padx=10)

        # ── Main two-column layout ─────────────────────────────────────────
        ws = tk.Frame(cf, bg=BG)
        ws.pack(fill="both", expand=True, padx=20, pady=14)

        # ── LEFT — task + task pie ─────────────────────────────────────────
        left = tk.Frame(ws, bg=PANEL,
                        highlightbackground=BORDER, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        tk.Label(left, text="📋  Завдання",
                 font=F_SUB, bg=PANEL, fg=MUTED).pack(anchor="w", padx=20, pady=(10, 4))
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x")

        # Task type label
        self.t3_type_lbl = tk.Label(left, text="", font=F_BODYB,
                                     bg=PANEL, fg=TEXT)
        self.t3_type_lbl.pack(pady=(10, 4))

        # Task fraction/mixed display (Canvas-drawn)
        self.t3_task_canvas = tk.Canvas(left, bg=PANEL, height=100,
                                         highlightthickness=0)
        self.t3_task_canvas.pack(fill="x", padx=30, pady=4)

        # Task pie
        self.t3_task_pie_frm = tk.Frame(left, bg=PANEL)
        self.t3_task_pie_frm.pack(pady=8)

        # ── RIGHT — answer controls + answer pie ───────────────────────────
        right = tk.Frame(ws, bg=PANEL,
                         highlightbackground=BORDER, highlightthickness=1,
                         width=int(self.SW * 0.48))
        right.pack(side="right", fill="both")
        right.pack_propagate(False)

        tk.Label(right, text="✏️  Твоя відповідь",
                 font=F_SUB, bg=PANEL, fg=MUTED).pack(anchor="w", padx=20, pady=(10, 4))
        tk.Frame(right, bg=BORDER, height=1).pack(fill="x")

        ctrl_area = tk.Frame(right, bg=PANEL)
        ctrl_area.pack(fill="x", padx=20, pady=14)

        # Answer display (Canvas-drawn, updates live)
        self.t3_answer_disp = tk.Canvas(right, bg=PANEL, height=100,
                                         highlightthickness=0)
        self.t3_answer_disp.pack(fill="x", padx=30, pady=4)

        # Answer pie (live, rebuilt on every change)
        self.t3_answer_pie_frm = tk.Frame(right, bg=PANEL)
        self.t3_answer_pie_frm.pack(pady=6)

        # Success / feedback label
        self.t3_success_lbl = tk.Label(right, text="",
                                        font=("Segoe UI", 22, "bold"),
                                        bg=PANEL, fg=GREEN,
                                        wraplength=int(self.SW * 0.45))
        self.t3_success_lbl.pack(pady=6)

        # ── +/- control rows ───────────────────────────────────────────────
        def make_control(parent, label, intvar, lo, hi, col):
            frame = tk.Frame(parent, bg=PANEL)
            tk.Label(frame, text=label, font=F_BODYB, bg=PANEL, fg=col,
                     width=18, anchor="w").pack(side="left")
            # minus
            def dec():
                v = intvar.get()
                if v > lo: intvar.set(v - 1)
                self._t3_on_change()
            def inc():
                v = intvar.get()
                if v < hi: intvar.set(v + 1)
                self._t3_on_change()
            b_m = tk.Button(frame, text="−", font=("Segoe UI", 22, "bold"),
                            width=3, bg=BTN_NUM, fg=TEXT, relief="flat",
                            cursor="hand2", command=dec)
            b_m.pack(side="left", padx=6)
            val_lbl = tk.Label(frame, textvariable=intvar,
                               font=("Segoe UI", 28, "bold"), bg=PANEL,
                               fg=col, width=4)
            val_lbl.pack(side="left")
            b_p = tk.Button(frame, text="+", font=("Segoe UI", 22, "bold"),
                            width=3, bg=BTN_NUM, fg=TEXT, relief="flat",
                            cursor="hand2", command=inc)
            b_p.pack(side="left", padx=6)
            return frame, b_m, b_p

        self.t3_whole_ctrl, *_ = make_control(
            ctrl_area, "Ціла частина:",  self.t3_u_whole, 0, 20, GREEN)
        self.t3_whole_ctrl.pack(fill="x", pady=6)

        self.t3_num_ctrl, *_ = make_control(
            ctrl_area, "Чисельник:",     self.t3_u_num,   0, 99, ACCENT2)
        self.t3_num_ctrl.pack(fill="x", pady=6)

        self.t3_den_ctrl, *_ = make_control(
            ctrl_area, "Знаменник:",     self.t3_u_den,   1, 20, ACCENT)
        self.t3_den_ctrl.pack(fill="x", pady=6)

        # ── Action buttons ─────────────────────────────────────────────────
        act = tk.Frame(right, bg=PANEL)
        act.pack(pady=8)
        mkbtn(act, "✔  Перевірити", self._t3_check,
              bg=GREEN, w=14, h=2).pack(side="left", padx=10)
        self.t3_new_btn = mkbtn(act, "✨  Нове завдання", self._t3_new,
                                 bg=ORANGE, w=16, h=2)
        self.t3_new_btn.pack(side="left", padx=10)

        self._t3_new()

    # ── Trainer 3 helpers ─────────────────────────────────────────────────────
    def _t3_score_text(self):
        return f"Правильно: {self.t3_score}  /  Завдань: {self.t3_attempts}"

    def _t3_new(self):
        self.t3_task_type = random.choice(["imp2mix", "mix2imp"])
        d = random.randint(2, 8)

        if self.t3_task_type == "imp2mix":
            # Generate improper fraction with non-zero remainder
            while True:
                n = random.randint(d + 1, d * 5)
                if n % d != 0:
                    break
            self.t3_imp_n, self.t3_imp_d = n, d
            # Correct answer
            self.t3_mix_whole = n // d
            self.t3_mix_n     = n % d
            self.t3_mix_d     = d
        else:
            # Generate mixed number
            whole = random.randint(1, 6)
            frac_n = random.randint(1, d - 1)
            self.t3_mix_whole, self.t3_mix_n, self.t3_mix_d = whole, frac_n, d
            # Correct answer (improper)
            self.t3_imp_n = whole * d + frac_n
            self.t3_imp_d = d

        self.t3_attempts += 1

        # Reset user inputs
        self.t3_u_whole.set(0)
        self.t3_u_num.set(0)
        self.t3_u_den.set(1)

        # Update controls visibility per task type
        self._t3_set_control_state()

        if self.t3_success_lbl:
            self.t3_success_lbl.config(text="")

        # Draw task display
        self._t3_draw_task()
        self._t3_draw_task_pie()
        self._t3_on_change()   # draws answer pie + checks

        if self.t3_score_lbl:
            self.t3_score_lbl.config(text=self._t3_score_text())

    def _t3_set_control_state(self):
        """Show/hide ціла частина depending on task type."""
        if self.t3_task_type == "imp2mix":
            # User enters mixed number: whole + num/den needed
            if self.t3_type_lbl:
                self.t3_type_lbl.config(
                    text="Неправильний дріб → мішане число",
                    fg=GREEN)
            if self.t3_whole_ctrl:
                self.t3_whole_ctrl.pack(fill="x", pady=6)
        else:
            # User enters improper: only num/den, no whole
            if self.t3_type_lbl:
                self.t3_type_lbl.config(
                    text="Мішане число → неправильний дріб",
                    fg=ACCENT2)
            if self.t3_whole_ctrl:
                self.t3_whole_ctrl.pack_forget()
            self.t3_u_whole.set(0)

    def _t3_draw_task(self):
        """Draw the task fraction/mixed number on the task canvas."""
        cv = self.t3_task_canvas
        if not cv:
            return
        cv.delete("all")
        cv.update_idletasks()
        W = cv.winfo_width() or 400
        H = 100
        cy = H // 2
        fnt_big = ("Segoe UI", 38, "bold")
        fnt_sm  = ("Segoe UI", 26, "bold")

        if self.t3_task_type == "imp2mix":
            # Draw improper fraction centred
            n, d = self.t3_imp_n, self.t3_imp_d
            nw = len(str(n)) * 24 + 16
            dw = len(str(d)) * 24 + 16
            bw = max(nw, dw) + 10
            x = W // 2 - bw // 2
            cv.create_text(x + bw//2, cy - 24, text=str(n), font=fnt_big, fill=ACCENT)
            cv.create_line(x, cy, x + bw, cy, width=4, fill=ACCENT)
            cv.create_text(x + bw//2, cy + 24, text=str(d), font=fnt_big, fill=ACCENT)
        else:
            # Draw mixed number centred
            wh = self.t3_mix_whole
            n, d = self.t3_mix_n, self.t3_mix_d
            ww = len(str(wh)) * 28 + 10
            nw = len(str(n)) * 22 + 10
            dw = len(str(d)) * 22 + 10
            fw = max(nw, dw) + 10
            total = ww + fw + 8
            x0 = W // 2 - total // 2
            cv.create_text(x0 + ww//2, cy, text=str(wh), font=("Segoe UI", 42, "bold"),
                           fill=GREEN)
            fx = x0 + ww + 8
            cv.create_text(fx + fw//2, cy - 22, text=str(n), font=fnt_sm, fill=ACCENT2)
            cv.create_line(fx, cy, fx + fw, cy, width=3, fill=ACCENT2)
            cv.create_text(fx + fw//2, cy + 22, text=str(d), font=fnt_sm, fill=ACCENT2)

    def _t3_draw_task_pie(self):
        """Draw pie for the task."""
        frm = self.t3_task_pie_frm
        if not frm:
            return
        for w in frm.winfo_children():
            w.destroy()
        if self.t3_task_type == "imp2mix":
            n, d = self.t3_imp_n, self.t3_imp_d
        else:
            wh = self.t3_mix_whole
            n  = wh * self.t3_mix_d + self.t3_mix_n
            d  = self.t3_mix_d
        cv = self._draw_pie_on_frame(frm, n, d, ACCENT, PANEL, radius=38)
        cv.pack()

    def _draw_pie_on_frame(self, parent, numer, denom, color, bg, radius=38):
        """Draw numer/denom as pie circles on a Canvas and return it."""
        import math as _m
        if denom <= 0:
            return tk.Canvas(parent, bg=bg, width=10, height=10,
                             highlightthickness=0)
        whole = numer // denom
        rem   = numer % denom
        circles = [denom] * whole + ([rem] if rem > 0 else [])
        if not circles:
            circles = [0]
        n_circ = len(circles)
        pad = 10
        W = n_circ * (radius * 2 + pad) + pad
        H = radius * 2 + pad * 2
        cv = tk.Canvas(parent, bg=bg, width=W, height=H, highlightthickness=0)
        for idx, filled in enumerate(circles):
            cx = pad + radius + idx * (radius * 2 + pad)
            cy = H // 2
            # background
            cv.create_oval(cx-radius, cy-radius, cx+radius, cy+radius,
                           fill=BTN_NUM, outline=MUTED, width=2)
            if filled > 0:
                step = 360.0 / denom
                for s in range(filled):
                    start = 90 - s * step
                    cv.create_arc(cx-radius, cy-radius, cx+radius, cy+radius,
                                  start=start, extent=-step,
                                  fill=color, outline=bg, width=1,
                                  style="pieslice")
            # dividers
            for s in range(denom):
                angle = _m.radians(90 - s * 360 / denom)
                cv.create_line(cx, cy,
                               cx + radius * _m.cos(angle),
                               cy - radius * _m.sin(angle),
                               fill=MUTED, width=1)
            # outline
            cv.create_oval(cx-radius, cy-radius, cx+radius, cy+radius,
                           fill="", outline=MUTED, width=2)
        return cv

    def _t3_draw_answer_display(self):
        """Draw user's current answer as fraction/mixed on the answer canvas."""
        cv = self.t3_answer_disp
        if not cv:
            return
        cv.delete("all")
        cv.update_idletasks()
        W = cv.winfo_width() or 400
        H = 100
        cy = H // 2
        fnt_big = ("Segoe UI", 38, "bold")
        fnt_sm  = ("Segoe UI", 26, "bold")

        wh = self.t3_u_whole.get()
        n  = self.t3_u_num.get()
        d  = max(1, self.t3_u_den.get())

        if self.t3_task_type == "imp2mix":
            # Show as mixed number
            ww = len(str(wh)) * 28 + 10
            nw = len(str(n)) * 22 + 10
            dw = len(str(d)) * 22 + 10
            fw = max(nw, dw) + 10
            total = ww + fw + 8
            x0 = W // 2 - total // 2
            col_wh = GREEN if wh > 0 else BTN_NUM
            cv.create_text(x0 + ww//2, cy, text=str(wh),
                           font=("Segoe UI", 42, "bold"), fill=col_wh)
            fx = x0 + ww + 8
            cv.create_text(fx + fw//2, cy - 22, text=str(n), font=fnt_sm, fill=ACCENT2)
            cv.create_line(fx, cy, fx + fw, cy, width=3, fill=ACCENT2)
            cv.create_text(fx + fw//2, cy + 22, text=str(d), font=fnt_sm, fill=ACCENT2)
        else:
            # Show as improper fraction (whole ignored)
            nw = len(str(n)) * 24 + 16
            dw = len(str(d)) * 24 + 16
            bw = max(nw, dw) + 10
            x = W // 2 - bw // 2
            cv.create_text(x + bw//2, cy - 24, text=str(n), font=fnt_big, fill=ACCENT)
            cv.create_line(x, cy, x + bw, cy, width=4, fill=ACCENT)
            cv.create_text(x + bw//2, cy + 24, text=str(d), font=fnt_big, fill=ACCENT)

    def _t3_on_change(self, *_):
        """Called whenever any user control changes. Redraws answer pie + checks live."""
        wh = self.t3_u_whole.get()
        n  = self.t3_u_num.get()
        d  = max(1, self.t3_u_den.get())

        # Clamp
        if d < 1:
            self.t3_u_den.set(1); d = 1
        if wh < 0: self.t3_u_whole.set(0); wh = 0
        if n < 0:  self.t3_u_num.set(0);   n  = 0

        # Redraw answer display
        self._t3_draw_answer_display()

        # Compute numerator for pie
        if self.t3_task_type == "imp2mix":
            pie_n = wh * d + n
            pie_d = d
        else:
            pie_n = n      # user enters improper: whole ignored
            pie_d = d

        # Rebuild answer pie with live colour (green = correct, amber = not yet)
        frm = self.t3_answer_pie_frm
        if frm:
            for w in frm.winfo_children():
                w.destroy()
            ok = self._t3_is_correct()
            pie_color = GREEN if ok else ORANGE
            cv = self._draw_pie_on_frame(frm, pie_n, pie_d, pie_color, PANEL, radius=38)
            cv.pack()

        # Live correctness indicator
        ok = self._t3_is_correct()
        if self.t3_success_lbl:
            if ok:
                self.t3_success_lbl.config(
                    text="🎉  Кружечки збіглися — правильно!\nНатисни «Нове завдання»",
                    fg=GREEN)
            else:
                self.t3_success_lbl.config(text="")

    def _t3_is_correct(self):
        wh = self.t3_u_whole.get()
        n  = self.t3_u_num.get()
        d  = max(1, self.t3_u_den.get())

        if self.t3_task_type == "imp2mix":
            # User entered mixed: check wh==correct_whole, n/d == correct_rem/d
            if wh != self.t3_mix_whole:
                return False
            # Accept equivalent fractions
            if d == 0:
                return False
            g1 = math.gcd(n, d)
            g2 = math.gcd(self.t3_mix_n, self.t3_mix_d)
            return (n // g1 == self.t3_mix_n // g2 and
                    d // g1 == self.t3_mix_d // g2)
        else:
            # User entered improper: wh should be 0, check n/d
            g1 = math.gcd(n, d)
            g2 = math.gcd(self.t3_imp_n, self.t3_imp_d)
            return (n // g1 == self.t3_imp_n // g2 and
                    d // g1 == self.t3_imp_d // g2)

    def _t3_check(self):
        if self._t3_is_correct():
            self.t3_score += 1
            # Repaint answer pie green
            self._t3_on_change()
            if self.t3_success_lbl:
                self.t3_success_lbl.config(
                    text="🎉  Чудово!  Натисни «Нове завдання»",
                    fg=GREEN)
        else:
            # Show correct answer hint
            if self.t3_task_type == "imp2mix":
                n, d = self.t3_imp_n, self.t3_imp_d
                wh, rn, rd = self.t3_mix_whole, self.t3_mix_n, self.t3_mix_d
                hint = f"Правильно:  {n}/{d}  =  {wh} і {rn}/{rd}"
            else:
                wh, rn, rd = self.t3_mix_whole, self.t3_mix_n, self.t3_mix_d
                imp = wh * rd + rn
                hint = f"Правильно:  {wh} і {rn}/{rd}  =  {imp}/{rd}"
            if self.t3_success_lbl:
                self.t3_success_lbl.config(text=f"❌  {hint}", fg=RED)
        if self.t3_score_lbl:
            self.t3_score_lbl.config(text=self._t3_score_text())


# ──────────────────────────────────────────────────────────────────────────────
# Trainer 3 (matplotlib version) — overrides above implementation
# ──────────────────────────────────────────────────────────────────────────────
    def show_trainer_3(self):
        self.clear_main()
        self.mode = "trainer3"

        self.t3_user_whole_var = tk.IntVar(value=0)
        self.t3_user_num_var = tk.IntVar(value=0)
        self.t3_user_den_var = tk.IntVar(value=1)
        self.t3_success_var = tk.StringVar()
        self.t3_solved = False

        cf = self.current_frame

        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.t3_score_lbl = tk.Label(
            sbar, text=self._t3_score_text(), font=F_SCORE, bg=PANEL, fg=GREEN
        )
        self.t3_score_lbl.pack(side="left", padx=30)
        tk.Label(
            sbar,
            text="Візуальна практика — керуй числами і дивись на частини",
            font=("Segoe UI", 15, "bold"), bg=PANEL, fg=ORANGE
        ).pack(side="left", padx=10)

        ws = tk.Frame(cf, bg=BG)
        ws.pack(fill="both", expand=True, padx=20, pady=14)

        left = tk.Frame(ws, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left, text="Завдання", font=F_SUB, bg=PANEL, fg=MUTED).pack(
            anchor="w", padx=20, pady=(12, 4)
        )
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x")

        self.t3_task_canvas = tk.Canvas(left, height=90, bg=PANEL, highlightthickness=0)
        self.t3_task_canvas.pack(fill="x", padx=20, pady=10)

        toolbar = tk.Frame(left, bg=PANEL)
        toolbar.pack(fill="x", padx=20, pady=(4, 8))
        self.t3_success_label = tk.Label(
            toolbar, textvariable=self.t3_success_var, font=F_BODYB, fg=GREEN, bg=PANEL
        )
        self.t3_success_label.pack(side="left", expand=True, anchor="w")
        mkbtn(toolbar, "Нове", self._t3_new_task, bg=ORANGE,
              w=10, h=1, font=("Segoe UI", 12, "bold")).pack(side="right", padx=6)
        mkbtn(toolbar, "Рішення", self._t3_open_solution_window, bg=ACCENT2,
              w=11, h=1, font=("Segoe UI", 12, "bold")).pack(side="right", padx=6)

        self.t3_controls = {}
        self.t3_controls["whole"] = self._t3_create_slider_unit(
            left, "Ціла частина:", self.t3_user_whole_var, GREEN
        )
        self.t3_controls["whole"]["frame"].pack(fill="x", padx=20, pady=6)
        self.t3_controls["num"] = self._t3_create_slider_unit(
            left, "Чисельник:", self.t3_user_num_var, ACCENT2
        )
        self.t3_controls["num"]["frame"].pack(fill="x", padx=20, pady=6)
        self.t3_controls["den"] = self._t3_create_slider_unit(
            left, "Знаменник:", self.t3_user_den_var, ACCENT
        )
        self.t3_controls["den"]["frame"].pack(fill="x", padx=20, pady=6)

        right = tk.Frame(ws, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        tk.Label(right, text="Візуалізація", font=F_SUB, bg=PANEL, fg=MUTED).pack(
            anchor="w", padx=20, pady=(12, 4)
        )
        tk.Frame(right, bg=BORDER, height=1).pack(fill="x")

        plot_frame = tk.Frame(right, bg=PANEL)
        plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.t3_figure = plt.figure(figsize=(12, 6), dpi=90)
        self.t3_canvas = FigureCanvasTkAgg(self.t3_figure, plot_frame)
        self.t3_canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        self._t3_new_task()

    def _t3_create_slider_unit(self, parent, label_text, var, color):
        frame = tk.Frame(parent, bg=PANEL)
        tk.Label(frame, text=label_text, font=F_BODYB, bg=PANEL, fg=color).grid(
            row=0, column=0, columnspan=4, sticky="w"
        )
        btn_minus = tk.Button(
            frame, text="−", font=("Segoe UI", 18, "bold"),
            width=2, bg=BTN_NUM, fg=TEXT, relief="flat", cursor="hand2",
            command=lambda v=var: self._t3_adjust_value(v, -1)
        )
        btn_minus.grid(row=1, column=0, padx=(0, 6), pady=4)
        scale = tk.Scale(
            frame, from_=0, to=99, variable=var,
            command=lambda val, v=var: self._t3_on_slider_change(val, v),
            orient="horizontal", showvalue=0, bg=PANEL, troughcolor=BTN_NUM,
            highlightthickness=0, length=300
        )
        scale.grid(row=1, column=1, sticky="ew", pady=4)
        frame.columnconfigure(1, weight=1)
        btn_plus = tk.Button(
            frame, text="+", font=("Segoe UI", 18, "bold"),
            width=2, bg=BTN_NUM, fg=TEXT, relief="flat", cursor="hand2",
            command=lambda v=var: self._t3_adjust_value(v, 1)
        )
        btn_plus.grid(row=1, column=2, padx=6, pady=4)
        val_lbl = tk.Label(frame, textvariable=var, font=F_BODYB, bg=PANEL, fg=color, width=4)
        val_lbl.grid(row=1, column=3, padx=(10, 0), pady=4)
        return {"frame": frame, "scale": scale, "plus": btn_plus, "minus": btn_minus}

    def _t3_adjust_value(self, var, delta):
        var.set(var.get() + delta)
        self._t3_on_slider_change()

    def _t3_score_text(self):
        return f"Правильно: {self.t3_score}  /  Завдань: {self.t3_attempts}"

    def _t3_on_slider_change(self, value=None, var=None):
        if var is not None and value is not None:
            var.set(int(float(value)))

        if self.t3_user_den_var.get() < 1:
            self.t3_user_den_var.set(1)
        if self.t3_user_whole_var.get() < 0:
            self.t3_user_whole_var.set(0)
        if self.t3_user_num_var.get() < 0:
            self.t3_user_num_var.set(0)

        if self.t3_task_type == "improper_to_mixed":
            if self.t3_user_num_var.get() >= self.t3_user_den_var.get() and self.t3_user_den_var.get() > 0:
                self.t3_user_num_var.set(self.t3_user_den_var.get() - 1 if self.t3_user_den_var.get() > 1 else 0)

        self.t3_controls["whole"]["scale"].config(to=5 + 9 * self.t3_user_den_var.get())
        self.t3_controls["den"]["scale"].config(to=10)

        if self.t3_task_type == "improper_to_mixed":
            self.t3_controls["num"]["scale"].config(
                to=self.t3_user_den_var.get() - 1 if self.t3_user_den_var.get() > 1 else 0
            )
        else:
            self.t3_controls["num"]["scale"].config(to=99)

        self._t3_check_answer()
        self._t3_visualize_fractions()

    def _t3_update_task_display(self):
        self.t3_task_canvas.delete("all")
        self.t3_task_canvas.bind("<Configure>", self._t3_draw_task_content, add="+")
        self.update_idletasks()
        self._t3_draw_task_content()

    def _t3_draw_task_content(self, event=None):
        self.t3_task_canvas.delete("all")
        canvas_w, canvas_h = self.t3_task_canvas.winfo_width(), self.t3_task_canvas.winfo_height()
        if canvas_w < 50:
            return

        prefix_text = "Завдання: "
        prefix_len = len(prefix_text) * 10 + 8
        self.t3_task_canvas.create_text(
            10, canvas_h / 2, text=prefix_text, font=F_BODY, anchor="w", fill=ACCENT
        )
        x_pos = prefix_len + 10

        if self.t3_task_type == "mixed_to_improper":
            whole_str = str(self.t3_mixed_whole)
            whole_w = len(whole_str) * 18 + 10
            self.t3_task_canvas.create_text(
                x_pos + whole_w / 2, canvas_h / 2, text=whole_str,
                font=F_FRAC_S, anchor="center", fill=GREEN
            )

            frac_x_offset = x_pos + whole_w + 5
            num_str, den_str = str(self.t3_mixed_num), str(self.t3_mixed_den)
            num_w = len(num_str) * 12 + 10
            den_w = len(den_str) * 12 + 10
            max_frac_w = max(num_w, den_w) + 10

            self.t3_task_canvas.create_text(
                frac_x_offset + max_frac_w / 2, canvas_h / 2 - 20,
                text=num_str, font=F_FRAC_S, anchor="center", fill=ACCENT2
            )
            self.t3_task_canvas.create_line(
                frac_x_offset, canvas_h / 2, frac_x_offset + max_frac_w, canvas_h / 2,
                width=3, fill=ACCENT2
            )
            self.t3_task_canvas.create_text(
                frac_x_offset + max_frac_w / 2, canvas_h / 2 + 20,
                text=den_str, font=F_FRAC_S, anchor="center", fill=ACCENT2
            )
        else:
            num_str, den_str = str(self.t3_improper_num), str(self.t3_improper_den)
            num_w = len(num_str) * 12 + 10
            den_w = len(den_str) * 12 + 10
            max_w = max(num_w, den_w) + 10

            self.t3_task_canvas.create_text(
                x_pos + max_w / 2, canvas_h / 2 - 20,
                text=num_str, font=F_FRAC_S, anchor="center", fill=ACCENT
            )
            self.t3_task_canvas.create_line(
                x_pos, canvas_h / 2, x_pos + max_w, canvas_h / 2, width=3, fill=ACCENT
            )
            self.t3_task_canvas.create_text(
                x_pos + max_w / 2, canvas_h / 2 + 20,
                text=den_str, font=F_FRAC_S, anchor="center", fill=ACCENT
            )

    def _t3_open_solution_window(self):
        self._t3_build_solution_for_task()
        win = tk.Toplevel(self)
        win.title("Рішення завдання")
        win.configure(bg=BG)
        win.geometry("900x650")

        hdr = tk.Frame(win, bg=HDR_BG, height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="Рішення завдання", bg=HDR_BG, fg=WHITE,
                 font=("Segoe UI", 18, "bold")).pack(side="left", padx=20)
        mkbtn(hdr, "Закрити", win.destroy, bg=RED,
              font=("Segoe UI", 12, "bold"), w=10, h=1).pack(side="right", padx=16, pady=12)

        sc = tk.Canvas(win, bg=BG, highlightthickness=0)
        vsb = tk.Scrollbar(win, orient="vertical", command=sc.yview)
        sc.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        sc.pack(side="left", fill="both", expand=True)
        outer = tk.Frame(sc, bg=BG)
        win_id = sc.create_window((0, 0), window=outer, anchor="nw")
        outer.bind("<Configure>", lambda e: sc.configure(scrollregion=sc.bbox("all")))
        sc.bind("<Configure>", lambda e: sc.itemconfig(win_id, width=e.width))

        pad = tk.Frame(outer, bg=BG)
        pad.pack(fill="both", expand=True, padx=30, pady=20)

        for style, text in self.t3_solution_steps:
            card = tk.Frame(pad, bg=PANEL, padx=16, pady=12,
                            highlightbackground=BORDER, highlightthickness=1)
            card.pack(fill="x", pady=8)
            tk.Label(card, text=text, font=F_BODY if style == "normal" else F_SUB,
                     bg=PANEL, fg=TEXT, anchor="w", justify="left", wraplength=820).pack(anchor="w")

    def _t3_set_controls_state(self, state):
        for controls in [self.t3_controls["whole"], self.t3_controls["num"], self.t3_controls["den"]]:
            controls["scale"].config(state=state)
            controls["plus"].config(state=state)
            controls["minus"].config(state=state)

    def _t3_new_task(self):
        self._t3_set_controls_state(tk.NORMAL)
        self.t3_success_var.set("")
        self.t3_solved = False

        self.t3_task_type = random.choice(["mixed_to_improper", "improper_to_mixed"])

        den = random.randint(2, 10)
        num_frac = random.randint(1, den - 1)
        whole = random.randint(1, 5)

        if self.t3_task_type == "mixed_to_improper":
            self.t3_mixed_whole = whole
            self.t3_mixed_num = num_frac
            self.t3_mixed_den = den
            self.t3_improper_num = whole * den + num_frac
            self.t3_improper_den = den
            self.t3_user_whole_var.set(0)
            self.t3_user_num_var.set(0)
            self.t3_user_den_var.set(1)
            self._t3_set_control_visibility(whole_part=False)
        else:
            while True:
                improper_num = random.randint(den + 1, den * 6)
                if improper_num % den != 0:
                    break
            self.t3_improper_num = improper_num
            self.t3_improper_den = den
            self.t3_mixed_whole = improper_num // den
            self.t3_mixed_num = improper_num % den
            self.t3_mixed_den = den
            self.t3_user_whole_var.set(0)
            self.t3_user_num_var.set(0)
            self.t3_user_den_var.set(1)
            self._t3_set_control_visibility(whole_part=True)

        self.t3_attempts += 1
        if self.t3_score_lbl:
            self.t3_score_lbl.config(text=self._t3_score_text())

        self._t3_update_task_display()
        self._t3_on_slider_change()

    def _t3_set_control_visibility(self, whole_part):
        state_whole_ctrl = tk.NORMAL if whole_part else tk.DISABLED
        self.t3_controls["whole"]["scale"].config(state=state_whole_ctrl)
        self.t3_controls["whole"]["plus"].config(state=state_whole_ctrl)
        self.t3_controls["whole"]["minus"].config(state=state_whole_ctrl)

        self.t3_controls["den"]["scale"].config(to=10)
        if whole_part:
            self.t3_controls["num"]["scale"].config(
                to=self.t3_user_den_var.get() - 1 if self.t3_user_den_var.get() > 1 else 0
            )
        else:
            self.t3_controls["num"]["scale"].config(to=99)

    def _t3_check_answer(self):
        user_w = self.t3_user_whole_var.get()
        user_n = self.t3_user_num_var.get()
        user_d = self.t3_user_den_var.get()

        if user_d == 0:
            self.t3_success_var.set("")
            return

        is_correct = False

        if self.t3_task_type == "mixed_to_improper":
            if user_w != 0:
                self.t3_success_var.set("")
                return
            gcd_user = math.gcd(user_n, user_d)
            simplified_user_n = user_n // gcd_user
            simplified_user_d = user_d // gcd_user
            gcd_correct = math.gcd(self.t3_improper_num, self.t3_improper_den)
            simplified_correct_n = self.t3_improper_num // gcd_correct
            simplified_correct_d = self.t3_improper_den // gcd_correct
            if simplified_user_n == simplified_correct_n and simplified_user_d == simplified_correct_d:
                is_correct = True
        else:
            if user_n >= user_d and user_d > 0:
                self.t3_success_var.set("")
                return
            if user_w == self.t3_mixed_whole:
                gcd_user_frac = math.gcd(user_n, user_d)
                gcd_correct_frac = math.gcd(self.t3_mixed_num, self.t3_mixed_den)
                if (user_n // gcd_user_frac == self.t3_mixed_num // gcd_correct_frac and
                        user_d // gcd_user_frac == self.t3_mixed_den // gcd_correct_frac):
                    is_correct = True

        if is_correct:
            self.t3_success_var.set("ПРАВИЛЬНО!")
            if not self.t3_solved:
                self.t3_solved = True
                self.t3_score += 1
                if self.t3_score_lbl:
                    self.t3_score_lbl.config(text=self._t3_score_text())
            self._t3_set_controls_state(tk.DISABLED)
        else:
            self.t3_success_var.set("")

    def _t3_build_solution_for_task(self):
        if self.t3_task_type == "mixed_to_improper":
            w, n, d = self.t3_mixed_whole, self.t3_mixed_num, self.t3_mixed_den
            step1_res = w * d
            final_num = step1_res + n
            self.t3_solution_steps = [
                ("bold", f"Перетворення мішаного числа {w} {n}/{d} в неправильний дріб"),
                ("normal", f"{w} × {d} = {step1_res}"),
                ("normal", f"{step1_res} + {n} = {final_num}"),
                ("normal", f"{w} {n}/{d} -> {final_num}/{d}")
            ]
        else:
            num_imp, den_imp = self.t3_improper_num, self.t3_improper_den
            whole_res = num_imp // den_imp
            remainder_res = num_imp % den_imp
            simplified_num, simplified_den = remainder_res, den_imp
            if remainder_res != 0:
                gcd_frac = math.gcd(remainder_res, den_imp)
                simplified_num = remainder_res // gcd_frac
                simplified_den = den_imp // gcd_frac
            self.t3_solution_steps = [
                ("bold", f"Перетворення неправильного дробу {num_imp}/{den_imp} в мішане число"),
                ("normal", f"{num_imp} ÷ {den_imp} = {whole_res} (ціла частина) з залишком {remainder_res}"),
                ("normal", f"({num_imp}/{den_imp}) -> {whole_res} {remainder_res}/{den_imp}"),
                ("normal", f"Скорочуємо: {remainder_res}/{den_imp} -> {simplified_num}/{simplified_den}")
            ]

    def _t3_visualize_fractions(self):
        self.t3_figure.clear()

        task_num_for_pie = 0
        task_den_for_pie = 1
        task_title_text = ""

        if self.t3_task_type == "mixed_to_improper":
            task_num_for_pie = self.t3_mixed_whole * self.t3_mixed_den + self.t3_mixed_num
            task_den_for_pie = self.t3_mixed_den
            task_title_text = f"Завдання: {self.t3_mixed_whole} $\\frac{{{self.t3_mixed_num}}}{{{self.t3_mixed_den}}}$"
        elif self.t3_task_type == "improper_to_mixed":
            task_num_for_pie = self.t3_improper_num
            task_den_for_pie = self.t3_improper_den
            task_title_text = f"Завдання: $\\frac{{{self.t3_improper_num}}}{{{self.t3_improper_den}}}$"

        user_num_for_pie = 0
        user_den_for_pie = 1
        user_title_text = ""

        if self.t3_user_den_var.get() > 0:
            user_num_for_pie = self.t3_user_whole_var.get() * self.t3_user_den_var.get() + self.t3_user_num_var.get()
            user_den_for_pie = self.t3_user_den_var.get()

        if self.t3_task_type == "improper_to_mixed":
            user_title_text = f"Ваша відповідь: {self.t3_user_whole_var.get()} $\\frac{{{self.t3_user_num_var.get()}}}{{{self.t3_user_den_var.get()}}}$"
        else:
            user_title_text = f"Ваша відповідь: $\\frac{{{self.t3_user_num_var.get()}}}{{{self.t3_user_den_var.get()}}}$"

        ax1 = self.t3_figure.add_subplot(1, 2, 1)
        ax2 = self.t3_figure.add_subplot(1, 2, 2)

        self._t3_draw_fraction_pie(ax1, task_num_for_pie, task_den_for_pie, task_title_text, "mediumseagreen")
        self._t3_draw_fraction_pie(ax2, user_num_for_pie, user_den_for_pie, user_title_text, "salmon")

        self.t3_figure.tight_layout(pad=3.0)
        self.t3_canvas.draw()

    def _t3_draw_fraction_pie(self, ax, numerator, denominator, title, color):
        ax.clear()
        ax.set_title(title, fontsize=20, pad=20)
        ax.set_aspect("equal")
        ax.axis("off")

        if denominator <= 0:
            return

        whole_part = numerator // denominator
        fractional_numerator = numerator % denominator

        pies_to_draw = []
        for _ in range(whole_part):
            pies_to_draw.append(denominator)
        if fractional_numerator > 0:
            pies_to_draw.append(fractional_numerator)
        if not pies_to_draw and numerator == 0:
            pies_to_draw.append(0)

        num_pies = len(pies_to_draw)
        if num_pies == 0:
            return

        pie_radius = 0.9 / (2 * num_pies)

        for i, num in enumerate(pies_to_draw):
            x_center = (2 * i + 1) / (2 * num_pies)
            y_center = 0.5

            if num > 0:
                sizes = [num, denominator - num] if denominator - num > 0 else [num]
                colors = [color, "#E0E0E0"] if denominator - num > 0 else [color]
            else:
                sizes = [1]
                colors = ["#E0E0E0"]

            ax.pie(
                sizes, colors=colors, startangle=90, counterclock=False,
                radius=pie_radius, center=(x_center, y_center),
                wedgeprops={"edgecolor": "black", "linewidth": 1}
            )

            if denominator <= 20:
                for j in range(denominator):
                    angle = np.deg2rad(90 - j * (360.0 / denominator))
                    x1 = x_center
                    y1 = y_center
                    x2 = x_center + pie_radius * np.cos(angle)
                    y2 = y_center + pie_radius * np.sin(angle)
                    ax.plot([x1, x2], [y1, y2], color="black", lw=0.7, alpha=0.6)

        ax.set_ylim(0, 1)
        ax.set_xlim(0, 1)

# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
