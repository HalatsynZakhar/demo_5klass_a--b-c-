import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.gridspec as gridspec
import numpy as np
import random
import re

# ── Palette ─────────────────────────────────────────────────────────────
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

# ── Fonts ───────────────────────────────────────────────────────────────
F_TITLE  = ("Segoe UI", 34, "bold")
F_HEAD   = ("Segoe UI", 26, "bold")
F_SUB    = ("Segoe UI", 20, "bold")
F_BODY   = ("Segoe UI", 17)
F_BODYB  = ("Segoe UI", 17, "bold")
F_BTN    = ("Segoe UI", 19, "bold")
F_NAV    = ("Segoe UI", 14, "bold")
F_SCORE  = ("Segoe UI", 20, "bold")
F_NUM    = ("Segoe UI", 26, "bold")
F_SMALL  = ("Segoe UI", 13)
F_FRAC_S = ("Segoe UI", 24, "bold")


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
             justify="left", wraplength=1200, anchor="w").pack(fill="x", pady=(6, 0))
    return f


def draw_pie_canvas(parent, n, d, color, radius=36, bg=WHITE):
    cv = tk.Canvas(parent, width=radius * 2 + 12, height=radius * 2 + 12,
                   bg=bg, highlightthickness=0)
    cx, cy = radius + 6, radius + 6
    cv.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                   fill="#f3f4f6", outline=MUTED)
    if d > 0:
        step = 360 / d
        for i in range(min(n, d)):
            cv.create_arc(cx - radius, cy - radius, cx + radius, cy + radius,
                          start=90 - i * step, extent=-step,
                          fill=color, outline=bg)
        for i in range(d):
            angle = np.deg2rad(90 - i * step)
            cv.create_line(cx, cy,
                           cx + radius * np.cos(angle),
                           cy - radius * np.sin(angle),
                           fill=MUTED)
    return cv


def draw_frac_inline(parent, n, d, color=ACCENT, bg=WHITE, size=24):
    f = tk.Frame(parent, bg=bg)
    fn = ("Segoe UI", size, "bold")
    bw = max(len(str(n)), len(str(d))) * (size // 2) + 18
    tk.Label(f, text=str(n), font=fn, bg=bg, fg=color).pack()
    tk.Frame(f, bg=color, height=3, width=bw).pack(pady=2)
    tk.Label(f, text=str(d), font=fn, bg=bg, fg=color).pack()
    return f


class SolutionWindow(tk.Toplevel):
    def __init__(self, parent, solution_steps):
        super().__init__(parent)
        self.title("Рішення завдання")
        self.configure(bg=BG)
        self.geometry("900x650")

        hdr = tk.Frame(self, bg=HDR_BG, height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="Рішення завдання", bg=HDR_BG, fg=WHITE,
                 font=("Segoe UI", 18, "bold")).pack(side="left", padx=20)
        mkbtn(hdr, "Закрити", self.destroy, bg=RED,
              font=("Segoe UI", 12, "bold"), w=10, h=1).pack(side="right", padx=16, pady=12)

        sc = tk.Canvas(self, bg=BG, highlightthickness=0)
        vsb = tk.Scrollbar(self, orient="vertical", command=sc.yview)
        sc.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        sc.pack(side="left", fill="both", expand=True)
        outer = tk.Frame(sc, bg=BG)
        win_id = sc.create_window((0, 0), window=outer, anchor="nw")
        outer.bind("<Configure>", lambda e: sc.configure(scrollregion=sc.bbox("all")))
        sc.bind("<Configure>", lambda e: sc.itemconfig(win_id, width=e.width))

        pad = tk.Frame(outer, bg=BG)
        pad.pack(fill="both", expand=True, padx=30, pady=20)

        for style, text in solution_steps:
            card = tk.Frame(pad, bg=PANEL, padx=16, pady=12,
                            highlightbackground=BORDER, highlightthickness=1)
            card.pack(fill="x", pady=8)
            lines = text.split("\n")
            tk.Label(card, text=lines[0], font=F_SUB if style == "bold" else F_BODY,
                     bg=PANEL, fg=TEXT, anchor="w", justify="left").pack(anchor="w")

            for line in lines[1:]:
                if "->" in line:
                    parts = line.split("->")
                    frac_frame = tk.Frame(card, bg=PANEL)
                    frac_frame.pack(anchor="w", pady=8)
                    for i, part in enumerate(parts):
                        if i > 0:
                            tk.Label(frac_frame, text="  =  ", font=F_FRAC_S,
                                     bg=PANEL, fg=TEXT).pack(side=tk.LEFT, padx=8)
                        self._draw_fraction_expression(frac_frame, part.strip())
                else:
                    tk.Label(card, text=line, font=F_BODY, bg=PANEL, fg=TEXT,
                             anchor="w", justify="left", wraplength=820).pack(anchor="w", pady=2)

    def _draw_fraction_expression(self, parent, expression):
        tokens = re.split(r'(\s[+-]\s|=)', expression)
        for token in tokens:
            token = token.strip()
            if not token:
                continue
            if "/" in token:
                try:
                    if " " in token:
                        whole_part, frac_part = token.split(" ")
                        n_str, d_str = frac_part.split("/")
                        tk.Label(parent, text=f"{whole_part}", font=F_FRAC_S,
                                 bg=PANEL, fg=TEXT).pack(side=tk.LEFT, padx=(0, 5))
                    else:
                        n_str, d_str = token.replace("(", "").replace(")", "").split("/")
                except ValueError:
                    tk.Label(parent, text=token, font=F_FRAC_S, bg=PANEL, fg=TEXT).pack(side=tk.LEFT)
                    continue
                canvas = tk.Canvas(parent, height=60, bg=PANEL, highlightthickness=0)
                canvas.pack(side=tk.LEFT)
                n_w = len(n_str) * 12 + 10
                d_w = len(d_str) * 12 + 10
                max_w = max(n_w, d_w) + 10
                canvas.config(width=max_w)
                canvas.create_text(max_w / 2, 15, text=n_str, font=F_FRAC_S, anchor="center", fill=ACCENT)
                canvas.create_line(2, 30, max_w - 2, 30, width=3, fill=ACCENT)
                canvas.create_text(max_w / 2, 45, text=d_str, font=F_FRAC_S, anchor="center", fill=ACCENT)
            else:
                tk.Label(parent, text=f" {token} ", font=F_FRAC_S, bg=PANEL, fg=TEXT).pack(side=tk.LEFT)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Віднімання дробів з однаковими знаменниками")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()

        self.MAX_CIRCLES = 6
        self.MAX_SLIDER_VAL = 50
        self.color1, self.color2, self.empty_color = "deepskyblue", "salmon", "#E0E0E0"

        self.task_n1, self.task_n2, self.task_d = 0, 0, 1
        self.correct_n, self.correct_d = 0, 1

        self.ans_n_var = tk.IntVar(value=1)
        self.ans_d_var = tk.IntVar(value=1)
        self.result_status_var = tk.StringVar()

        self.task_canvas = None
        self.figure = None
        self.canvas = None
        self.ans_controls = None
        self.result_status_label = None

        self._build_chrome()
        self.show_main_menu()

    # ── Chrome ──────────────────────────────────────────────────────────
    def _build_chrome(self):
        hdr = tk.Frame(self, bg=HDR_BG, height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="Віднімання дробів з однаковими знаменниками",
                 bg=HDR_BG, fg=WHITE, font=("Segoe UI", 21, "bold")).pack(side="left", padx=30)
        mkbtn(hdr, "✕  Вийти", self.destroy, bg=RED,
              font=("Segoe UI", 13, "bold"), w=9, h=1).pack(side="right", padx=18, pady=16)

        nav = tk.Frame(self, bg=NAV_BG, height=52)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        for label, cmd in [
            ("🏠  Меню", self.show_main_menu),
            ("📘  Теорія", self.show_theory),
            ("🎯  Практика", self.show_practice),
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
        self.current_frame = None

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
        outer.bind("<Configure>", lambda e: sc.configure(scrollregion=sc.bbox("all")))
        sc.bind("<Configure>", lambda e: sc.itemconfig(win, width=e.width))
        p = tk.Frame(outer, bg=BG)
        p.pack(fill="both", expand=True, padx=60, pady=28)
        return p

    # ── Menu ────────────────────────────────────────────────────────────
    def show_main_menu(self):
        self.clear_main()
        center = tk.Frame(self.current_frame, bg=BG)
        center.place(relx=.5, rely=.5, anchor="center")

        tk.Label(center, text="Віднімання дробів", font=("Segoe UI", 50, "bold"),
                 bg=BG, fg=TEXT).pack(pady=(0, 4))
        tk.Label(center, text="однакові знаменники • 5 клас",
                 font=("Segoe UI", 24), bg=BG, fg=ACCENT).pack(pady=(0, 28))

        cards = [
            ("📘", "Теорія",   CARD_B,  ACCENT,  self.show_theory),
            ("🎯", "Практика", CARD_Y,  ORANGE,  self.show_practice),
        ]
        row = tk.Frame(center, bg=BG)
        row.pack()
        for icon, title, bg_c, fg_c, cmd in cards:
            c = tk.Frame(row, bg=bg_c, width=240, height=200,
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

        tk.Label(center, text="Обери розділ або скористайся меню зверху",
                 font=F_SMALL, bg=BG, fg=MUTED).pack(pady=18)

    # ── Theory ──────────────────────────────────────────────────────────
    def show_theory(self):
        self.clear_main()
        p = self._scroll_page()

        tk.Label(p, text="Віднімання дробів з однаковими знаменниками",
                 font=F_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        tk.Label(p, text="Основне правило та приклади",
                 font=F_SUB, bg=BG, fg=ACCENT).pack(anchor="w", pady=(0, 10))
        hline(p)

        theory_card(
            p,
            "Правило",
            "Якщо знаменники однакові, віднімаємо тільки чисельники, а знаменник не змінюється.",
            CARD_B
        )
        theory_card(
            p,
            "Кроки",
            "1) Переконайся, що знаменники однакові.\n"
            "2) Обчисли різницю чисельників.\n"
            "3) Запиши відповідь з тим самим знаменником.\n"
            "4) За потреби можна скоротити дріб.",
            CARD_G
        )
        theory_card(
            p,
            "Приклад",
            "Беремо дріб із чисельником 5 та знаменником 8 і віднімаємо дріб\n"
            "із чисельником 3 та тим самим знаменником 8.\n"
            "Різниця чисельників: 5 − 3 = 2, знаменник лишається 8.",
            CARD_V
        )
        theory_card(
            p,
            "Нуль",
            "Якщо чисельники рівні, то різниця дорівнює нулю.",
            CARD_Y
        )

        # Візуалізація теорії (тортики)
        viz = tk.Frame(p, bg=PANEL, padx=18, pady=12,
                       highlightbackground=BORDER, highlightthickness=1)
        viz.pack(fill="x", pady=10)
        tk.Label(viz, text="Візуалізація прикладу", font=F_SUB,
                 bg=PANEL, fg=MUTED).pack(anchor="w")
        row = tk.Frame(viz, bg=PANEL)
        row.pack(pady=8)
        draw_pie_canvas(row, 5, 8, self.color1, radius=36, bg=PANEL).pack(side="left", padx=6)
        tk.Label(row, text="−", font=F_HEAD, bg=PANEL, fg=MUTED).pack(side="left", padx=6)
        draw_pie_canvas(row, 3, 8, self.color2, radius=36, bg=PANEL).pack(side="left", padx=6)
        tk.Label(row, text="=", font=F_HEAD, bg=PANEL, fg=MUTED).pack(side="left", padx=6)
        draw_pie_canvas(row, 2, 8, GREEN, radius=36, bg=PANEL).pack(side="left", padx=6)
        row_f = tk.Frame(viz, bg=PANEL)
        row_f.pack(pady=(2, 8))
        draw_frac_inline(row_f, 5, 8, color=ACCENT, bg=PANEL, size=22).pack(side="left", padx=8)
        tk.Label(row_f, text="−", font=F_HEAD, bg=PANEL, fg=MUTED).pack(side="left", padx=6)
        draw_frac_inline(row_f, 3, 8, color=ACCENT2, bg=PANEL, size=22).pack(side="left", padx=8)
        tk.Label(row_f, text="=", font=F_HEAD, bg=PANEL, fg=MUTED).pack(side="left", padx=6)
        draw_frac_inline(row_f, 2, 8, color=GREEN, bg=PANEL, size=22).pack(side="left", padx=8)

        # Додаткова візуальна демонстрація
        viz2 = tk.Frame(p, bg=PANEL, padx=18, pady=12,
                        highlightbackground=BORDER, highlightthickness=1)
        viz2.pack(fill="x", pady=10)
        tk.Label(viz2, text="Кроки на тортиках", font=F_SUB,
                 bg=PANEL, fg=MUTED).pack(anchor="w")
        r2 = tk.Frame(viz2, bg=PANEL)
        r2.pack(pady=8)
        draw_pie_canvas(r2, 6, 10, self.color1, radius=34, bg=PANEL).pack(side="left", padx=6)
        tk.Label(r2, text="−", font=F_HEAD, bg=PANEL, fg=MUTED).pack(side="left", padx=6)
        draw_pie_canvas(r2, 4, 10, self.color2, radius=34, bg=PANEL).pack(side="left", padx=6)
        tk.Label(r2, text="=", font=F_HEAD, bg=PANEL, fg=MUTED).pack(side="left", padx=6)
        draw_pie_canvas(r2, 2, 10, GREEN, radius=34, bg=PANEL).pack(side="left", padx=6)
        r2f = tk.Frame(viz2, bg=PANEL)
        r2f.pack(pady=(2, 8))
        draw_frac_inline(r2f, 6, 10, color=ACCENT, bg=PANEL, size=22).pack(side="left", padx=8)
        tk.Label(r2f, text="−", font=F_HEAD, bg=PANEL, fg=MUTED).pack(side="left", padx=6)
        draw_frac_inline(r2f, 4, 10, color=ACCENT2, bg=PANEL, size=22).pack(side="left", padx=8)
        tk.Label(r2f, text="=", font=F_HEAD, bg=PANEL, fg=MUTED).pack(side="left", padx=6)
        draw_frac_inline(r2f, 2, 10, color=GREEN, bg=PANEL, size=22).pack(side="left", padx=8)

    # ── Practice ────────────────────────────────────────────────────────
    def show_practice(self):
        self.clear_main()

        cf = self.current_frame

        sbar = tk.Frame(cf, bg=PANEL, height=56,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        tk.Label(sbar, text="🎯  Практика — віднімай дроби з однаковими знаменниками",
                 font=F_SCORE, bg=PANEL, fg=ORANGE).pack(side="left", padx=30)

        ws = tk.Frame(cf, bg=BG)
        ws.pack(fill="both", expand=True, padx=20, pady=14)

        left = tk.Frame(ws, bg=PANEL,
                        highlightbackground=BORDER, highlightthickness=1,
                        width=int(self.SW * 0.25))
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)

        tk.Label(left, text="📋  Завдання", font=F_SUB, bg=PANEL, fg=MUTED).pack(anchor="w", padx=20, pady=(10, 4))
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x")

        self.task_canvas = tk.Canvas(left, height=70, bg=PANEL, highlightthickness=0)
        self.task_canvas.pack(fill="x", padx=20, pady=10)

        toolbar = tk.Frame(left, bg=PANEL)
        toolbar.pack(fill="x", padx=20, pady=(4, 8))
        self.result_status_label = tk.Label(toolbar, textvariable=self.result_status_var,
                                            font=F_BODYB, bg=PANEL, fg=GREEN)
        self.result_status_label.pack(side="left", expand=True, anchor="w")
        mkbtn(toolbar, "🆕  Нове", self._generate_new_task, bg=ORANGE,
              w=10, h=1, font=("Segoe UI", 12, "bold")).pack(side="right", padx=6)
        mkbtn(toolbar, "🧾  Рішення", self._open_solution_window, bg=ACCENT2,
              w=11, h=1, font=("Segoe UI", 12, "bold")).pack(side="right", padx=6)

        self.ans_controls = self._create_fraction_controls(left)

        right = tk.Frame(ws, bg=PANEL,
                         highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        tk.Label(right, text="🧁  Тортики (візуалізація)", font=F_SUB, bg=PANEL, fg=MUTED).pack(anchor="w", padx=20, pady=(10, 4))
        tk.Frame(right, bg=BORDER, height=1).pack(fill="x")

        plot_frame = tk.Frame(right, bg=PANEL)
        plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.figure = plt.figure(figsize=(14, 6), dpi=90)
        self.canvas = FigureCanvasTkAgg(self.figure, plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._generate_new_task()

    def _create_fraction_controls(self, parent):
        frame = tk.Frame(parent, bg=PANEL)
        frame.pack(fill="x", padx=20, pady=10)
        tk.Label(frame, text="Ваша відповідь:", font=F_SUB, bg=PANEL, fg=ACCENT).pack(anchor="w", pady=(0, 8))

        num_widgets = self._create_slider_unit(frame, "Чисельник:", self.ans_n_var, ACCENT2)
        num_widgets["frame"].pack(pady=5, fill="x")
        tk.Frame(frame, bg=BORDER, height=1).pack(pady=6, fill="x")

        den_widgets = self._create_slider_unit(frame, "Знаменник:", self.ans_d_var, ACCENT)
        den_widgets["frame"].pack(pady=5, fill="x")

        return {"frame": frame, "num": num_widgets, "den": den_widgets}

    def _create_slider_unit(self, parent, label_text, var, color):
        frame = tk.Frame(parent, bg=PANEL)
        tk.Label(frame, text=label_text, font=F_BODYB, bg=PANEL, fg=color).grid(row=0, column=0, columnspan=4, sticky="w")
        btn_minus = tk.Button(frame, text="−", font=("Segoe UI", 18, "bold"),
                              width=2, bg=BTN_NUM, fg=TEXT, relief="flat",
                              cursor="hand2", command=lambda v=var: self._adjust_value(v, -1))
        btn_minus.grid(row=1, column=0, padx=(0, 6), pady=4)
        scale = tk.Scale(frame, from_=0, to=self.MAX_SLIDER_VAL, variable=var,
                         command=lambda val, v=var: self._on_slider_change(val, v),
                         orient="horizontal", showvalue=0, bg=PANEL, troughcolor=BTN_NUM,
                         highlightthickness=0, length=300)
        scale.grid(row=1, column=1, sticky="ew", pady=4)
        frame.columnconfigure(1, weight=1)
        btn_plus = tk.Button(frame, text="+", font=("Segoe UI", 18, "bold"),
                             width=2, bg=BTN_NUM, fg=TEXT, relief="flat",
                             cursor="hand2", command=lambda v=var: self._adjust_value(v, 1))
        btn_plus.grid(row=1, column=2, padx=6, pady=4)
        tk.Label(frame, textvariable=var, font=F_BODYB, bg=PANEL, fg=color, width=4).grid(row=1, column=3, padx=(10, 0), pady=4)
        return {"frame": frame, "scale": scale, "plus": btn_plus, "minus": btn_minus}

    def _adjust_value(self, var, delta):
        new_val = var.get() + delta
        if var == self.ans_d_var and new_val < 1:
            new_val = 1
        if var != self.ans_d_var and new_val < 0:
            new_val = 0
        var.set(new_val)
        self._on_slider_change()

    def _on_slider_change(self, value=None, var=None):
        if var is not None and value is not None:
            var.set(int(float(value)))

        if self.ans_d_var.get() < 1:
            self.ans_d_var.set(1)
        if self.ans_n_var.get() < 0:
            self.ans_n_var.set(0)
        self.visualize()
        self._check_user_answer()

    def _generate_new_task(self):
        d = random.randint(3, 15)
        n1 = random.randint(2, d - 1)
        n2 = random.randint(1, n1)
        self._load_state((n1, n2, d))

    def _load_state(self, state):
        self._set_controls_state(tk.NORMAL)
        self.result_status_var.set("")
        n1, n2, d = state
        self.task_n1, self.task_n2, self.task_d = n1, n2, d
        self.correct_n = n1 - n2
        self.correct_d = d
        self.ans_n_var.set(1)
        self.ans_d_var.set(1)
        self._update_task_display()
        self._on_slider_change()

    def _update_task_display(self):
        self.task_canvas.delete("all")
        self.task_canvas.bind("<Configure>", lambda e: self._draw_task_text(), add="+")
        self.update_idletasks()
        self._draw_task_text()

    def _draw_task_text(self):
        self.task_canvas.delete("all")
        canvas_w, canvas_h = self.task_canvas.winfo_width(), self.task_canvas.winfo_height()
        if canvas_w < 50:
            return

        prefix_text = "Завдання: "
        prefix_len = len(prefix_text) * 10 + 8
        self.task_canvas.create_text(10, canvas_h / 2, text=prefix_text, font=F_BODY, anchor="w", fill=ACCENT)
        x_pos = prefix_len + 10

        def draw_frac(n, d, x):
            n_w = len(str(n)) * 12 + 10
            d_w = len(str(d)) * 12 + 10
            max_w = max(n_w, d_w) + 10
            self.task_canvas.create_text(x + max_w / 2, canvas_h / 2 - 16, text=str(n), font=F_FRAC_S, anchor="center")
            self.task_canvas.create_line(x, canvas_h / 2, x + max_w, canvas_h / 2, width=3)
            self.task_canvas.create_text(x + max_w / 2, canvas_h / 2 + 16, text=str(d), font=F_FRAC_S, anchor="center")
            return x + max_w + 20

        x_pos = draw_frac(self.task_n1, self.task_d, x_pos)
        self.task_canvas.create_text(x_pos, canvas_h / 2, text="−", font=F_FRAC_S, anchor="center")
        x_pos += 40
        draw_frac(self.task_n2, self.task_d, x_pos)

    def _set_controls_state(self, state):
        for key in ["num", "den"]:
            self.ans_controls[key]["scale"].config(state=state)
            self.ans_controls[key]["plus"].config(state=state)
            self.ans_controls[key]["minus"].config(state=state)

    def visualize(self):
        self.figure.clear()

        gs_main = gridspec.GridSpec(2, 3, figure=self.figure, height_ratios=[1, 9], hspace=0.1)
        ax_title1, ax_title2, ax_title3 = (self.figure.add_subplot(gs_main[0, i], facecolor="none") for i in range(3))
        for ax in [ax_title1, ax_title2, ax_title3]:
            ax.axis("off")

        ax_title1.set_title(self.format_user_input_title("Зменшуване", self.task_n1, self.task_d), fontsize=18)
        ax_title2.set_title(self.format_user_input_title("Від'ємник", self.task_n2, self.task_d), fontsize=18)

        user_n, user_d = self.ans_n_var.get(), self.ans_d_var.get()
        ax_title3.set_title(self.format_user_input_title("Ваша відповідь", user_n, user_d), fontsize=18, color="green")

        ax1, ax2, ax3 = (self.figure.add_subplot(gs_main[1, i]) for i in range(3))

        self._draw_overlapping_circles(ax1, self.task_n1, self.task_d, self.color1)
        self._draw_overlapping_circles(ax2, self.task_n2, self.task_d, self.color2)

        user_improper_n = user_n
        if user_n == 0 and self.correct_n != 0:
            self.draw_placeholder(ax3, "Введіть\nрезультат")
        else:
            self._draw_overlapping_circles(ax3, user_improper_n, user_d, "mediumseagreen")

        self.figure.tight_layout(pad=2.0)
        self.canvas.draw()

    def _check_user_answer(self):
        user_n = self.ans_n_var.get()
        user_d = self.ans_d_var.get()

        if user_d == 0:
            self.result_status_var.set("Знаменник не може бути нулем!")
            self.result_status_label.config(fg=RED)
            return

        if self.correct_n == 0:
            if user_n == 0:
                self.result_status_var.set("✔ ВІДМІННО! Дроби однакові, різниця дорівнює нулю.")
                self.result_status_label.config(fg=GREEN)
                self._set_controls_state(tk.DISABLED)
            else:
                self.result_status_var.set("")
            return

        if user_n == 0:
            self.result_status_var.set("")
            return

        if user_d != self.correct_d:
            self.result_status_var.set("Пам'ятайте: знаменник залишається тим самим!")
            self.result_status_label.config(fg=RED)
            return

        if user_n == self.correct_n and user_d == self.correct_d:
            self.result_status_var.set("✔ ВІДМІННО! Абсолютно правильна відповідь.")
            self.result_status_label.config(fg=GREEN)
            self._set_controls_state(tk.DISABLED)
        else:
            self.result_status_var.set("Поки що неправильно. Спробуйте ще!")
            self.result_status_label.config(fg=RED)

    def format_user_input_title(self, base_title, n, d):
        if d == 0:
            return base_title
        frac_str = f"{n} з {d}" if n > 0 or d != 0 else ""

        if n == 0 and d != 0:
            return f"{base_title}\n$0$"
        return f"{base_title}\n{frac_str}"

    def _draw_overlapping_circles(self, ax, n, d, color):
        ax.axis("off")
        ax.set_aspect("equal", adjustable="box")
        if d == 0:
            return
        whole, frac_n = divmod(n, d)
        total_circles = whole + (1 if frac_n > 0 else 0)
        if total_circles == 0 and n == 0:
            self.draw_fraction_pie(ax, [0], [color], d, center=(0, 0))
            return

        radius = 2.4
        overlap = 0.65
        step = 2 * radius * overlap
        actual_width = (total_circles - 1) * step + 2 * radius if total_circles > 0 else 0

        max_width_circles = max(self.MAX_CIRCLES, total_circles)
        max_width = (max_width_circles - 1) * step + 2 * radius

        start_x = -actual_width / 2 + radius
        for i in range(whole):
            self.draw_fraction_pie(ax, [d], [color], d, center=(start_x + i * step, 0), radius=radius)
        if frac_n > 0:
            self.draw_fraction_pie(ax, [frac_n], [color], d, center=(start_x + whole * step, 0), radius=radius)

        ax.set_xlim(-max_width / 2 - 0.2, max_width / 2 + 0.2)
        ax.set_ylim(-radius - 1.4, radius + 0.2)

    def _build_solution_for_task(self):
        n1, n2, d = self.task_n1, self.task_n2, self.task_d
        self.solution_steps = []

        self.solution_steps.append(("bold", "--- ПРАВИЛО 5 КЛАСУ ---"))
        self.solution_steps.append(("normal",
                                    "При відніманні дробів з однаковими знаменниками:\n"
                                    "від чисельника зменшуваного віднімають чисельник від'ємника,\n"
                                    "а знаменник залишається тим самим."))

        diff_n = n1 - n2

        if diff_n == 0:
            self.solution_steps.extend([
                ("bold", "--- КРОК 1: ВІДНІМАЄМО ЧИСЕЛЬНИКИ ---"),
                ("normal", f"Чисельники однакові: {n1} - {n2} = 0."),
                ("normal", "Якщо чисельник дорівнює нулю, то весь дріб дорівнює нулю."),
                ("bold", "Кінцева відповідь: 0")
            ])
            return

        self.solution_steps.extend([
            ("bold", "--- КРОК 1: ВІДНІМАЄМО ЧИСЕЛЬНИКИ ---"),
            ("normal", f"Чисельники: {n1} - {n2} = {diff_n}."),
            ("normal", f"Знаменник залишається {d}.")
        ])

        self.solution_steps.append(("bold", f"Кінцева відповідь: чисельник {diff_n}, знаменник {d}"))

    def draw_fraction_pie(self, ax, numerators, colors, denominator, center=(0, 0), radius=1.0):
        sizes, final_colors = [], []
        total_num = sum(numerators)
        if total_num > 0:
            sizes.extend([n for n in numerators if n > 0])
            final_colors.extend(colors[:len(sizes)])
        if denominator - total_num > 0:
            sizes.append(denominator - total_num)
            final_colors.append(self.empty_color)
        if not sizes:
            sizes, final_colors = [1], [self.empty_color]

        ax.pie(sizes, radius=radius * 3.7, center=center, colors=final_colors, startangle=90, counterclock=False,
               wedgeprops={"edgecolor": "black", "linewidth": 0.8})
        if denominator <= 20:
            for j in range(denominator):
                angle = np.deg2rad(90 - j * (360.0 / denominator))
                x1, y1 = center
                x2 = x1 + (radius * 3.7) * np.cos(angle)
                y2 = y1 + (radius * 3.7) * np.sin(angle)
                ax.plot([x1, x2], [y1, y2], color="black", lw=1.2, alpha=0.9)

    def draw_placeholder(self, ax, text):
        ax.axis("off")
        ax.text(0.5, 0.5, text, ha="center", va="center", fontsize=20, color="grey",
                transform=ax.transAxes, wrap=True)

    def _open_solution_window(self):
        self._build_solution_for_task()
        SolutionWindow(self, self.solution_steps)


if __name__ == "__main__":
    app = App()
    app.mainloop()
