import tkinter as tk
from tkinter import ttk, font
import random
import math
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.gridspec as gridspec
import numpy as np

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
F_FRAC   = ("Segoe UI", 44, "bold")
F_FRAC_S = ("Segoe UI", 26, "bold")
F_SIGN   = ("Segoe UI", 52, "bold")

# ── Helpers ───────────────────────────────────────────────────────────────────
def _darken(h, a=30):
    r = max(0, int(h[1:3], 16) - a)
    g = max(0, int(h[3:5], 16) - a)
    b = max(0, int(h[5:7], 16) - a)
    return f"#{r:02x}{g:02x}{b:02x}"

def mkbtn(parent, text, cmd, bg=ACCENT, fg=WHITE, font=F_BTN, w=12, h=2, px=6, py=6):
    b = tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg,
                  font=font, width=w, height=h,
                  relief="flat", bd=0, cursor="hand2",
                  activebackground=bg, activeforeground=fg,
                  padx=px, pady=py)
    orig = bg
    b.bind("<Enter>", lambda e: b.config(bg=_darken(orig, 25)))
    b.bind("<Leave>", lambda e: b.config(bg=orig))
    return b

def theory_card(parent, title, body, bg_c, fg_title=TEXT):
    f = tk.Frame(parent, bg=bg_c, padx=40, pady=30,
                 highlightbackground=BORDER, highlightthickness=1)
    f.pack(fill="x", pady=15, padx=100)
    tk.Label(f, text=title, font=F_TITLE, bg=bg_c, fg=fg_title, anchor="center").pack(fill="x")
    tk.Label(f, text=body, font=F_HEAD, bg=bg_c, fg=TEXT,
             justify="center", wraplength=1000, anchor="center").pack(fill="x", pady=(20, 0))
    return f

def frac_w(parent, n, d, w_part=0, bg=PANEL, size="big", color=ACCENT):
    """Вертикальний дріб з горизонтальною рискою."""
    sizes  = {"big": F_FRAC, "small": F_FRAC_S}
    widths = {"big": 70,     "small": 48}
    fn = sizes.get(size, F_FRAC_S)
    bw = widths.get(size, 48)
    f = tk.Frame(parent, bg=bg)
    if w_part and w_part > 0:
        tk.Label(f, text=str(w_part), font=fn, bg=bg, fg=color).pack(side="left", padx=(0, 5), pady=(10, 0))
    frac_f = tk.Frame(f, bg=bg)
    frac_f.pack(side="left")
    tk.Label(frac_f, text=str(n), font=fn, bg=bg, fg=color).pack()
    tk.Frame(frac_f, bg=color, height=3, width=bw).pack(pady=2)
    tk.Label(frac_f, text=str(d), font=fn, bg=bg, fg=color).pack()
    return f

def draw_pie_canvas(parent, n, d, color, radius=50, bg=WHITE):
    """Малювання кола на Canvas для розділу Теорія."""
    cv = tk.Canvas(parent, width=radius*2+20, height=radius*2+20, bg=bg, highlightthickness=0)
    cx, cy = radius+10, radius+10
    cv.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, fill="#f3f4f6", outline=MUTED, width=2)
    if d > 0:
        step = 360 / d
        for i in range(min(n, d)):
            cv.create_arc(cx-radius, cy-radius, cx+radius, cy+radius, start=90-i*step, extent=-step, fill=color, outline=WHITE, width=1)
        for i in range(d):
            angle = math.radians(90 - i*step)
            cv.create_line(cx, cy, cx+radius*math.cos(angle), cy-radius*math.sin(angle), fill=MUTED, width=1)
    return cv

def draw_beam_theory(parent):
    """Малювання координатного променя для Теорії."""
    f = tk.Frame(parent, bg=WHITE, padx=40, pady=30, highlightbackground=BORDER, highlightthickness=1)
    f.pack(fill="x", padx=100, pady=15)
    tk.Label(f, text="📍 На координатному промені:", font=F_TITLE, bg=WHITE, fg=TEAL).pack(anchor="center", pady=(0, 20))
    cv = tk.Canvas(f, bg=WHITE, height=180, highlightthickness=0)
    cv.pack(fill="x")
    cv.update_idletasks()
    W = cv.winfo_width() or 1000
    margin = 80
    ly = 100
    cv.create_line(margin, ly, W-40, ly, width=3, arrow=tk.LAST)
    unit = (W - 2*margin) // 2
    for i in range(19): # Мітки для дев'ятих часток
        x = margin + i * (unit / 9)
        th = 15 if i % 9 == 0 else 8
        cv.create_line(x, ly-th, x, ly+th, width=2)
        if i % 9 == 0:
            cv.create_text(x, ly+40, text=str(i//9), font=F_HEAD)
    # Стрибки (дуги)
    cv.create_arc(margin, ly-50, margin+2*(unit/9), ly+50, start=0, extent=180, style=tk.ARC, outline=ACCENT, width=4)
    cv.create_text(margin+(unit/9), ly-70, text="2/9", font=F_SUB, fill=ACCENT)
    cv.create_arc(margin+2*(unit/9), ly-70, margin+7*(unit/9), ly+70, start=0, extent=180, style=tk.ARC, outline=ACCENT2, width=4)
    cv.create_text(margin+4.5*(unit/9), ly-90, text="5/9", font=F_SUB, fill=ACCENT2)
    cv.create_text(margin+7*(unit/9), ly+40, text="7/9", font=F_HEAD, fill=GREEN)

# ── Window and App Classes ──────────────────────────────────────────────────
class SolutionWindow(tk.Toplevel):
    def __init__(self, parent, solution_steps):
        super().__init__(parent)
        self.title("Рішення завдання")
        self.geometry("900x700")
        self.configure(bg=BG)
        sc = tk.Canvas(self, bg=BG, highlightthickness=0); sc.pack(side="left", fill="both", expand=True)
        vsb = tk.Scrollbar(self, orient="vertical", command=sc.yview); vsb.pack(side="right", fill="y")
        p = tk.Frame(sc, bg=BG); sc.create_window((0,0), window=p, anchor="nw")
        p.bind("<Configure>", lambda e: sc.configure(scrollregion=sc.bbox("all")))
        for style, text in solution_steps:
            f = tk.Frame(p, bg=WHITE, padx=20, pady=15, highlightbackground=BORDER, highlightthickness=1)
            f.pack(fill="x", padx=20, pady=10)
            lines = text.split('\n')
            tk.Label(f, text=lines[0], font=F_BODYB if style=="bold" else F_BODY, bg=WHITE, fg=ACCENT if style=="bold" else TEXT, anchor="w").pack(fill="x")
            for line in lines[1:]:
                if "->" in line:
                    parts = line.split("->")
                    ff = tk.Frame(f, bg=WHITE); ff.pack(anchor="w", pady=10)
                    for i, part in enumerate(parts):
                        if i > 0: tk.Label(ff, text=" = ", font=F_HEAD, bg=WHITE).pack(side="left", padx=10)
                        self._draw_expr(ff, part.strip())
                else: tk.Label(f, text=line, font=F_BODY, bg=WHITE, fg=MUTED, anchor="w").pack(fill="x")

    def _draw_expr(self, parent, expr):
        tokens = re.split(r'(\s[+-]\s|=)', expr)
        for t in tokens:
            t = t.strip()
            if "/" in t:
                n, d = t.replace("(","").replace(")","").split("/")
                frac_w(parent, n, d, bg=WHITE, size="small").pack(side="left")
            elif t: tk.Label(parent, text=f" {t} ", font=F_HEAD, bg=WHITE).pack(side="left")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("§ 38. Додавання і віднімання дробів")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        
        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()
        
        self.task_n1 = self.task_n2 = self.task_d = 0
        self.operation = "+"
        self.score = self.total = 0
        self.correct_flag = False
        
        self.ans_n_var = tk.IntVar(value=1)
        self.ans_d_var = tk.IntVar(value=1)
        
        self.ans_n_var.trace_add("write", lambda *a: self._auto_check())
        self.ans_d_var.trace_add("write", lambda *a: self._auto_check())

        self.current_frame = None
        self._build_chrome()
        self.show_main_menu()

    def _build_chrome(self):
        hdr = tk.Frame(self, bg=HDR_BG, height=70); hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="§ 38. Додавання і віднімання звичайних дробів", bg=HDR_BG, fg=WHITE, font=("Segoe UI", 21, "bold")).pack(side="left", padx=30)
        mkbtn(hdr, "✕  Вийти", self.destroy, bg=RED, w=9, h=1).pack(side="right", padx=18, pady=16)

        nav = tk.Frame(self, bg=NAV_BG, height=52); nav.pack(fill="x")
        for label, cmd in [("🏠 Меню", self.show_main_menu), ("📖 Теорія", self.show_theory), ("🎯 Практика", self.show_practice)]:
            b = tk.Button(nav, text=label, command=cmd, bg=NAV_BG, fg=NAV_FG, font=F_NAV, relief="flat", bd=0, cursor="hand2", padx=20, pady=14)
            b.pack(side="left")
            b.bind("<Enter>", lambda e, x=b: x.config(bg=ACCENT)); b.bind("<Leave>", lambda e, x=b: x.config(bg=NAV_BG))

        self.main_area = tk.Frame(self, bg=BG); self.main_area.pack(fill="both", expand=True)

    def clear_main(self):
        if self.current_frame: self.current_frame.destroy()
        self.current_frame = tk.Frame(self.main_area, bg=BG); self.current_frame.pack(expand=True, fill="both")

    def show_main_menu(self):
        self.clear_main()
        c = tk.Frame(self.current_frame, bg=BG); c.place(relx=.5, rely=.5, anchor="center")
        tk.Label(c, text="Додавання і віднімання дробів", font=F_TITLE, bg=BG).pack(pady=20)
        row = tk.Frame(c, bg=BG); row.pack()
        for i, t, bg, cmd in [("📖", "Теорія", CARD_B, self.show_theory), ("🎯", "Практика", CARD_G, self.show_practice)]:
            f = tk.Frame(row, bg=bg, width=250, height=220, highlightbackground=BORDER, highlightthickness=2); f.pack(side="left", padx=20); f.pack_propagate(False)
            tk.Label(f, text=i, font=("Segoe UI", 50), bg=bg).pack(pady=20); tk.Label(f, text=t, font=F_SUB, bg=bg).pack()
            f.bind("<Button-1>", lambda e, f=cmd: f())

    def show_theory(self):
        self.clear_main()
        sc = tk.Canvas(self.current_frame, bg=BG, highlightthickness=0); sc.pack(side="left", fill="both", expand=True)
        vsb = tk.Scrollbar(self.current_frame, orient="vertical", command=sc.yview); vsb.pack(side="right", fill="y")
        sc.configure(yscrollcommand=vsb.set)
        p = tk.Frame(sc, bg=BG)
        window_id = sc.create_window(self.SW//2, 0, window=p, anchor="n")
        sc.bind("<Configure>", lambda e: sc.itemconfig(window_id, width=e.width))
        p.bind("<Configure>", lambda e: sc.configure(scrollregion=sc.bbox("all")))
        
        theory_card(p, "➕ Додавання дробів", "Щоб додати дроби з однаковими знаменниками, треба додати їхні чисельники і залишити той самий знаменник.", CARD_B, ACCENT)
        ex1 = tk.Frame(p, bg=WHITE, padx=40, pady=30, highlightbackground=BORDER, highlightthickness=1); ex1.pack(fill="x", padx=100, pady=15)
        row1 = tk.Frame(ex1, bg=WHITE); row1.pack()
        frac_w(row1, 1, 4, bg=WHITE, size="big").pack(side="left", padx=20)
        tk.Label(row1, text="+", font=F_BIG, bg=WHITE).pack(side="left")
        frac_w(row1, 2, 4, bg=WHITE, size="big").pack(side="left", padx=20)
        tk.Label(row1, text="=", font=F_BIG, bg=WHITE).pack(side="left")
        frac_w(row1, 3, 4, bg=WHITE, size="big", color=GREEN).pack(side="left", padx=20)
        row2 = tk.Frame(ex1, bg=WHITE); row2.pack(pady=30)
        draw_pie_canvas(row2, 1, 4, ACCENT, radius=60).pack(side="left", padx=15)
        tk.Label(row2, text="+", font=F_BIG, bg=WHITE, fg=MUTED).pack(side="left")
        draw_pie_canvas(row2, 2, 4, ACCENT2, radius=60).pack(side="left", padx=15)
        tk.Label(row2, text="=", font=F_BIG, bg=WHITE, fg=MUTED).pack(side="left")
        draw_pie_canvas(row2, 3, 4, GREEN, radius=60).pack(side="left", padx=15)
        theory_card(p, "➖ Віднімання дробів", "Щоб відняти дроби з однаковими знаменниками, треба від чисельника зменшуваного відняти чисельник від’ємника і залишити той самий знаменник.", CARD_R, RED)
        draw_beam_theory(p)
        theory_card(p, "🔄 Результат", "Якщо результатом є неправильний дріб, його перетворюють на мішане число.", CARD_Y, ORANGE)
        tk.Frame(p, bg=BG, height=50).pack()

    def show_practice(self):
        self.clear_main()
        top = tk.Frame(self.current_frame, bg=PANEL, height=60, highlightbackground=BORDER, highlightthickness=1); top.pack(fill="x")
        self.score_lbl = tk.Label(top, text=f"Рахунок: {self.score}/{self.total}", font=F_SCORE, bg=PANEL, fg=GREEN); self.score_lbl.pack(side="left", padx=20)
        ws = tk.Frame(self.current_frame, bg=BG); ws.pack(fill="both", expand=True, padx=20, pady=10)
        left = tk.Frame(ws, bg=PANEL, highlightbackground=BORDER, highlightthickness=1); left.pack(side="left", fill="both", expand=True, padx=5)
        self.task_expr_f = tk.Frame(left, bg=WHITE, pady=20); self.task_expr_f.pack(fill="x")
        self.fig = plt.figure(figsize=(8, 4), dpi=90); self.canvas_plt = FigureCanvasTkAgg(self.fig, left)
        self.canvas_plt.get_tk_widget().pack(fill="both", expand=True, pady=10)
        right = tk.Frame(ws, bg=PANEL, highlightbackground=BORDER, highlightthickness=1, width=480); right.pack(side="right", fill="both", padx=5); right.pack_propagate(False)
        tk.Label(right, text="Ваша відповідь:", font=F_SUB, bg=PANEL, fg=ACCENT).pack(pady=15)
        def make_slider(parent, label, var, lo, hi, color):
            f = tk.Frame(parent, bg=PANEL, pady=10); f.pack(fill="x", padx=30)
            tk.Label(f, text=label, font=F_BODYB, bg=PANEL, fg=color).pack(anchor="w")
            row = tk.Frame(f, bg=PANEL); row.pack(fill="x")
            tk.Button(row, text="-", font=F_HEAD, width=2, command=lambda: self._adj(var, -1)).pack(side="left")
            ttk.Scale(row, from_=lo, to=hi, variable=var, orient="horizontal", command=lambda v: self._sync(var, v)).pack(side="left", fill="x", expand=True, padx=10)
            tk.Button(row, text="+", font=F_HEAD, width=2, command=lambda: self._adj(var, 1)).pack(side="left")
            tk.Label(row, textvariable=var, font=F_HEAD, width=3, bg=PANEL).pack(side="left", padx=5)
        make_slider(right, "Чисельник:", self.ans_n_var, 0, 30, ACCENT2)
        make_slider(right, "Знаменник:", self.ans_d_var, 1, 30, ACCENT)
        self.feed_lbl = tk.Label(right, text="", font=F_FEED, bg=PANEL); self.feed_lbl.pack(pady=20)
        btns = tk.Frame(right, bg=PANEL); btns.pack(side="bottom", pady=30)
        self.btn_next = mkbtn(btns, "▶ Наступне", self._new_task, bg=ACCENT, w=14)
        self.btn_next.pack(side="left", padx=10)
        self.btn_next.config(state="disabled", bg=BTN_NUM)
        mkbtn(btns, "💡 Підказка", self._show_sol, bg=ORANGE, w=12).pack(side="left", padx=10)
        self._new_task()

    def _adj(self, var, d):
        if self.correct_flag: return
        val = var.get() + d
        if var == self.ans_d_var and val < 1: val = 1
        elif val < 0: val = 0
        var.set(val)

    def _sync(self, var, val):
        if self.correct_flag: return
        var.set(int(float(val)))

    def _new_task(self):
        self.correct_flag = False
        if hasattr(self, 'btn_next'): self.btn_next.config(state="disabled", bg=BTN_NUM)
        self.operation = random.choice(["+", "-"])
        self.task_d = random.randint(4, 15)
        if self.operation == "+":
            self.task_n1 = random.randint(1, self.task_d-1)
            self.task_n2 = random.randint(1, self.task_d - self.task_n1)
        else:
            self.task_n1 = random.randint(2, self.task_d-1)
            self.task_n2 = random.randint(1, self.task_n1)
        self.ans_n_var.set(1); self.ans_d_var.set(1)
        self.feed_lbl.config(text="", fg=TEXT)
        for w in self.task_expr_f.winfo_children(): w.destroy()
        row = tk.Frame(self.task_expr_f, bg=WHITE); row.pack()
        frac_w(row, self.task_n1, self.task_d, bg=WHITE).pack(side="left", padx=15)
        tk.Label(row, text=self.operation, font=F_SIGN, bg=WHITE, fg=ORANGE).pack(side="left")
        frac_w(row, self.task_n2, self.task_d, bg=WHITE).pack(side="left", padx=15)
        tk.Label(row, text="= ?", font=F_SIGN, bg=WHITE, fg=ORANGE).pack(side="left", padx=10)
        self._draw_plt()

    def _draw_plt(self):
        un, ud = self.ans_n_var.get(), self.ans_d_var.get()
        self.fig.clear(); gs = gridspec.GridSpec(1, 3, figure=self.fig)
        ax1 = self.fig.add_subplot(gs[0, 0]); ax2 = self.fig.add_subplot(gs[0, 1]); ax3 = self.fig.add_subplot(gs[0, 2])
        self._pie(ax1, self.task_n1, self.task_d, "Перший дріб" if self.operation=="+" else "Зменшуване", ACCENT)
        self._pie(ax2, self.task_n2, self.task_d, "Другий дріб" if self.operation=="+" else "Від’ємник", ACCENT2)
        pie_color = "mediumseagreen" if self.correct_flag else "salmon"
        self._pie(ax3, un, ud, "Твій результат", pie_color)
        self.fig.tight_layout(); self.canvas_plt.draw()

    def _pie(self, ax, n, d, title, color):
        ax.clear(); ax.set_title(title, fontsize=12, pad=10); ax.axis('off')
        if d <= 0: return
        if n > d:
            ax.pie([1], colors=[color], wedgeprops={"edgecolor":"black", "linewidth":1})
            ax.set_title(title + "\n(> 1)", fontsize=10)
        else:
            # Малювання окремих часток (1/d кожна)
            ax.pie([1]*d, colors=[color]*n + ["#f3f4f6"]*(d-n), startangle=90, counterclock=False, wedgeprops={"edgecolor":"black", "linewidth":0.5})

    def _auto_check(self):
        un, ud = self.ans_n_var.get(), self.ans_d_var.get()
        self._draw_plt()
        if self.correct_flag or ud == 0: return
        corr_n = (self.task_n1 + self.task_n2) if self.operation=="+" else (self.task_n1 - self.task_n2)
        if un * self.task_d == corr_n * ud:
            self.correct_flag = True; self.score += 1; self.total += 1
            self.feed_lbl.config(text="✅ Правильно! Тепер можна йти далі.", fg=GREEN)
            self.score_lbl.config(text=f"Рахунок: {self.score}/{self.total}")
            self.btn_next.config(state="normal", bg=ACCENT)
            self._draw_plt()

    def _show_sol(self):
        d, n1, n2 = self.task_d, self.task_n1, self.task_n2
        res_n = (n1+n2) if self.operation=="+" else (n1-n2)
        op_name = "додаємо" if self.operation=="+" else "віднімаємо"
        steps = [("bold", f"Крок 1: Обчислюємо чисельник"), ("normal", f"Знаменник залишаємо {d}. Чисельники {op_name}:"), ("normal", f"{n1}/{d} {self.operation} {n2}/{d} -> ({n1}{self.operation}{n2})/{d} -> {res_n}/{d}")]
        SolutionWindow(self, steps)

if __name__ == "__main__":
    App().mainloop()
