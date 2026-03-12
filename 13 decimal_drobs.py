"""
Інтерактивний тренажер: Десяткові дроби
pip install matplotlib
"""
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyBboxPatch, Rectangle
import matplotlib.patches as mpatches
import numpy as np
import math

# ══════════════════════════════════════════════════════════════════
#  КОЛЬОРИ  (контрастна світла тема)
# ══════════════════════════════════════════════════════════════════
BG       = "#F0F2F8"
SURFACE  = "#FFFFFF"
SRF2     = "#E4E8F4"
BORDER   = "#9AA3C2"
C_BLUE   = "#1A56DB"
C_CYAN   = "#0E7490"
C_RED    = "#B91C1C"
C_GREEN  = "#166534"
C_PURP   = "#6D28D9"
C_ORANGE = "#C2410C"
TEXT     = "#0F172A"
TEXT2    = "#374151"
TEXT3    = "#6B7280"
GRID_C   = "#CBD5E1"

PLACE_COLORS = [TEXT, C_BLUE, C_CYAN, C_GREEN, C_PURP, C_ORANGE]
PLACE_NAMES  = ["Одиниці","Десяті","Соті","Тисячні","Дес-тис.","Сто-тис."]
PLACE_MULTS  = ["x1","x0.1","x0.01","x0.001","x0.0001","x0.00001"]
PLACE_LABELS_LONG = [
    "Ціла частина",
    "Десяті  (0.1)",
    "Соті    (0.01)",
    "Тисячні (0.001)",
    "Дес-тисячні (0.0001)",
    "Сто-тисячні (0.00001)",
]

PLT = {
    "figure.facecolor": SURFACE,
    "axes.facecolor":   BG,
    "text.color":       TEXT,
    "axes.labelcolor":  TEXT2,
    "xtick.color":      TEXT2,
    "ytick.color":      TEXT2,
    "axes.edgecolor":   BORDER,
    "axes.titlecolor":  TEXT,
    "grid.color":       GRID_C,
    "font.family":      "sans-serif",
}

# ══════════════════════════════════════════════════════════════════
#  УТИЛІТИ
# ══════════════════════════════════════════════════════════════════
def gcd(a, b):
    while b: a, b = b, a % b
    return a

def frac_str(val, precision=100000):
    n = round(val * precision)
    d = precision
    g = gcd(abs(n), d)
    return f"{n//g}/{d//g}" if n else "0"

def num_name(digits, places):
    int_p = digits[0]
    dec_s = "".join(str(digits[i]) for i in range(1, places+2)).rstrip("0")
    parts = []
    if int_p:
        parts.append(f"{int_p} {'ціла' if int_p==1 else 'цілих'}")
    if dec_s:
        n   = int(dec_s)
        pos = len(dec_s)
        pn  = {1:"десят",2:"сот",3:"тисячн",4:"десятитисячн"}.get(pos,"")
        end = "а" if n==1 else "их"
        parts.append(f"{n} {pn}{end}" if pn else f"{n}/10^{pos}")
    return " ".join(parts) or "нуль"

def auto_step(zoom_range):
    for thr, stp in [(0.0003,0.00001),(0.003,0.0001),(0.03,0.001),
                     (0.3,0.01),(1.5,0.1),(3,0.2),(8,0.5)]:
        if zoom_range < thr: return stp
    return 1.0

def fmt(val, places):
    """Форматує число з комою як роздільником (5 клас)."""
    return f"{val:.{places}f}".replace(".", ",")

def fmt_tick(val, decimals):
    """Підпис ділення на осі з комою."""
    return f"{val:.{decimals}f}".replace(".", ",")

def digits_to_val(digits):
    v = float(digits[0])
    for i in range(1, 6):
        v += digits[i] * (10**-i)
    return round(v, 5)


# ══════════════════════════════════════════════════════════════════
#  ГОЛОВНИЙ КЛАС
# ══════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Десяткові дроби — тренажер")
        self.configure(bg=BG)
        try:    self.state("zoomed")
        except: self.attributes("-zoomed", True)

        plt.rcParams.update(PLT)

        # стан головного числа
        self.digits = [0, 7, 5, 0, 0, 0]
        self.places = 2

        # числова пряма
        self.zoom_range  = 1.0
        self.zoom_center = 0.75
        self._drag_x0    = None
        self._drag_c0    = None

        # лічильник
        self.ctr_val  = 0.0
        self.ctr_hist = [0.0]
        self._ctr_step_var = tk.StringVar(value="0.1")

        # порівняння
        self.cmp_a = [0, 3, 0, 0, 0, 0]
        self.cmp_b = [0, 7, 5, 0, 0, 0]

        # refs для динамічних слайдерів
        self._sl_refs  = []   # list of (Scale, label_widget, Spinbox, IntVar)
        self._card_refs = []  # list of (Frame, Label, color)

        self._setup_styles()
        self._build_ui()
        self.after(80, self._full_refresh)

    # ──────────────────────────────────────────────────────────────
    def _setup_styles(self):
        st = ttk.Style(self)
        st.theme_use("clam")
        st.configure("TFrame",        background=BG)
        st.configure("TLabel",        background=BG, foreground=TEXT,
                     font=("Helvetica",11))
        st.configure("TNotebook",     background=BG, borderwidth=0)
        st.configure("TNotebook.Tab", background=SRF2, foreground=TEXT2,
                     padding=[14,8], font=("Helvetica",11,"bold"),
                     borderwidth=0)
        st.map("TNotebook.Tab",
               background=[("selected", SURFACE)],
               foreground=[("selected", C_BLUE)])

    # ══ UI ════════════════════════════════════════════════════════
    def _build_ui(self):
        self.columnconfigure(0, minsize=310, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self._build_left()
        self._build_right()

    # ── ЛІВА ПАНЕЛЬ ───────────────────────────────────────────────
    def _build_left(self):
        self._left = tk.Frame(self, bg=SURFACE,
                              highlightbackground=BORDER, highlightthickness=2)
        self._left.grid(row=0, column=0, sticky="nsew")
        self._left.columnconfigure(0, weight=1)

        row = [0]
        def nrow():
            r = row[0]; row[0] += 1; return r
        def sep():
            tk.Frame(self._left, bg=BORDER, height=2
                     ).grid(row=nrow(), column=0, sticky="ew")

        # ── Дисплей ──────────────────────────────────────────────
        disp = tk.Frame(self._left, bg=SRF2)
        disp.grid(row=nrow(), column=0, sticky="ew")

        tk.Label(disp, text="ЧИСЛО", bg=SRF2, fg=TEXT3,
                 font=("Courier",9), padx=14, pady=6).pack(anchor="w")
        nr = tk.Frame(disp, bg=SRF2)
        nr.pack(anchor="w", padx=14)
        self.lbl_int = tk.Label(nr, text="0",  bg=SRF2, fg=TEXT,
                                font=("Courier",40,"bold"))
        self.lbl_dot = tk.Label(nr, text=",",  bg=SRF2, fg=TEXT3,
                                font=("Courier",40,"bold"))
        self.lbl_dec = tk.Label(nr, text="75", bg=SRF2, fg=C_BLUE,
                                font=("Courier",40,"bold"))
        for w in (self.lbl_int, self.lbl_dot, self.lbl_dec):
            w.pack(side="left")
        self.lbl_name = tk.Label(disp, text="", bg=SRF2, fg=TEXT3,
                                 font=("Helvetica",10,"italic"), pady=2)
        self.lbl_name.pack(anchor="w", padx=14)
        self.lbl_frac = tk.Label(disp, text="= 3/4", bg=SRF2, fg=C_CYAN,
                                 font=("Courier",12,"bold"), pady=3)
        self.lbl_frac.pack(anchor="w", padx=14)

        # ── Кількість розрядів ───────────────────────────────────
        sep()
        tk.Label(self._left, text="КІЛЬКІСТЬ РОЗРЯДІВ", bg=SURFACE, fg=TEXT3,
                 font=("Courier",9), padx=14, pady=5
                 ).grid(row=nrow(), column=0, sticky="w")
        pr = tk.Frame(self._left, bg=SURFACE)
        pr.grid(row=nrow(), column=0, sticky="ew", padx=10, pady=(0,6))
        for i in range(5):
            pr.columnconfigure(i, weight=1)
        self._place_btns = []
        pl_labels = ["Дес.\n0.1","Соті\n0.01","Тис.\n0.001",
                     "Дес-тис\n.0001","Сто-тис\n.00001"]
        for i, lbl in enumerate(pl_labels):
            b = tk.Button(pr, text=lbl, relief="flat", cursor="hand2",
                          font=("Helvetica",8),
                          command=lambda n=i+1: self._set_places(n))
            b.grid(row=0, column=i, padx=2, sticky="ew", ipady=4)
            self._place_btns.append(b)
        self._refresh_place_btns()

        # ── Повзунки ─────────────────────────────────────────────
        sep()
        tk.Label(self._left, text="ЗНАЧЕННЯ", bg=SURFACE, fg=TEXT3,
                 font=("Courier",9), padx=14, pady=5
                 ).grid(row=nrow(), column=0, sticky="w")
        self._sl_frame = tk.Frame(self._left, bg=SURFACE)
        self._sl_frame.grid(row=nrow(), column=0, sticky="ew",
                            padx=12, pady=(0,4))
        self._sl_frame.columnconfigure(0, weight=1)
        self._rebuild_sliders()

        # ── Картки ───────────────────────────────────────────────
        sep()
        tk.Label(self._left, text="РОЗРЯДИ", bg=SURFACE, fg=TEXT3,
                 font=("Courier",9), padx=14, pady=5
                 ).grid(row=nrow(), column=0, sticky="w")
        self._cards_frame = tk.Frame(self._left, bg=SURFACE)
        self._cards_frame.grid(row=nrow(), column=0, sticky="ew",
                               padx=12, pady=(0,6))
        self._rebuild_cards()

        # ── Еквіваленти ──────────────────────────────────────────
        sep()
        tk.Label(self._left, text="ЗВИЧАЙНІ ДРОБИ", bg=SURFACE, fg=TEXT3,
                 font=("Courier",9), padx=14, pady=5
                 ).grid(row=nrow(), column=0, sticky="w")
        self._frac_frame = tk.Frame(self._left, bg=SURFACE)
        self._frac_frame.grid(row=nrow(), column=0, sticky="ew",
                              padx=12, pady=(0,6))
        self._frac_frame.columnconfigure(0, weight=1)

    # ── ПРАВА ПАНЕЛЬ ──────────────────────────────────────────────
    def _build_right(self):
        right = tk.Frame(self, bg=BG)
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        self.nb = ttk.Notebook(right)
        self.nb.grid(row=0, column=0, sticky="ew")
        self.nb.bind("<<NotebookTabChanged>>", self._on_tab)

        tabs = [
            ("📏 Числова пряма", "_tab_line"),
            ("🟦 Сітка-100",     "_tab_grid"),
            ("🥧 Торт/Дроби",    "_tab_pie"),
            ("🔢 Розряди",       "_tab_place"),
            ("⏱ Лічильник",     "_tab_ctr"),
            ("⚖ Порівняння",    "_tab_cmp"),
        ]
        for title, attr in tabs:
            f = ttk.Frame(self.nb)
            self.nb.add(f, text=title)
            setattr(self, attr, f)

        # Рядок 1 — панель керування (лічильник / порівняння)
        self._ctrl_row = tk.Frame(right, bg=SURFACE)
        self._ctrl_row.grid(row=1, column=0, sticky="ew")
        right.rowconfigure(0, weight=0)
        right.rowconfigure(1, weight=0)

        # Рядок 2 — Matplotlib canvas
        right.rowconfigure(2, weight=1)
        self.fig = plt.figure(figsize=(12,7), facecolor=SURFACE)
        self.mpl = FigureCanvasTkAgg(self.fig, master=right)
        w = self.mpl.get_tk_widget()
        w.configure(bg=SURFACE, highlightthickness=0)
        w.grid(row=2, column=0, sticky="nsew")

        w.bind("<MouseWheel>",      self._wheel)
        w.bind("<Button-4>",        self._wheel)
        w.bind("<Button-5>",        self._wheel)
        w.bind("<ButtonPress-1>",   self._drag_start)
        w.bind("<B1-Motion>",       self._drag_move)
        w.bind("<ButtonRelease-1>", self._drag_end)

        # Будуємо приховані панелі в ctrl_row
        self._build_ctr_overlay(self._ctrl_row)
        self._build_cmp_overlay(self._ctrl_row)

    # ══ СЛАЙДЕРИ ════════════════════════════════════════════════════
    def _rebuild_sliders(self):
        for w in self._sl_frame.winfo_children():
            w.destroy()
        self._sl_refs = []

        for i in range(self.places + 1):
            color = PLACE_COLORS[i]
            # Мітка
            tk.Label(self._sl_frame, text=PLACE_LABELS_LONG[i],
                     bg=SURFACE, fg=TEXT2, font=("Helvetica",10)
                     ).grid(row=i*3, column=0, columnspan=3,
                            sticky="w", pady=(8 if i==0 else 4, 0))
            # Шкала
            sl = tk.Scale(self._sl_frame,
                          from_=0, to=9,
                          orient="horizontal",
                          showvalue=False,
                          bg=SURFACE, fg=TEXT,
                          troughcolor=SRF2,
                          activebackground=color,
                          highlightthickness=0,
                          sliderlength=24, sliderrelief="flat",
                          width=16,
                          command=lambda v, idx=i: self._sl_cb(idx, int(float(v))))
            sl.set(self.digits[i])
            sl.grid(row=i*3+1, column=0, sticky="ew")

            val_lbl = tk.Label(self._sl_frame, text=str(self.digits[i]),
                               bg=SURFACE, fg=color,
                               font=("Courier",14,"bold"), width=2, anchor="e")
            val_lbl.grid(row=i*3+1, column=1, padx=(6,2))

            var = tk.IntVar(value=self.digits[i])
            sp  = tk.Spinbox(self._sl_frame, from_=0, to=9,
                             textvariable=var, width=3,
                             font=("Courier",12), relief="flat",
                             bg=SRF2, fg=color, bd=2,
                             command=lambda vi=i, vr=var: self._sp_cb(vi, vr))
            sp.bind("<Return>", lambda e, vi=i, vr=var: self._sp_cb(vi, vr))
            sp.bind("<FocusOut>", lambda e, vi=i, vr=var: self._sp_cb(vi, vr))
            sp.grid(row=i*3+1, column=2, padx=(2,0))

            self._sl_refs.append((sl, val_lbl, sp, var))

        self._sl_frame.columnconfigure(0, weight=1)

    def _sl_cb(self, idx, v):
        self.digits[idx] = v
        sl, lbl, sp, var = self._sl_refs[idx]
        lbl.config(text=str(v))
        var.set(v)
        self._refresh_display()
        self._redraw()

    def _sp_cb(self, idx, var):
        try:    v = max(0, min(9, int(var.get())))
        except: return
        self.digits[idx] = v
        var.set(v)
        sl, lbl, sp, vr = self._sl_refs[idx]
        sl.set(v)
        lbl.config(text=str(v))
        self._refresh_display()
        self._redraw()

    def _sync_sliders(self):
        for i, (sl, lbl, sp, var) in enumerate(self._sl_refs):
            v = self.digits[i]
            sl.set(v)
            lbl.config(text=str(v))
            var.set(v)

    # ══ РОЗРЯДИ ═════════════════════════════════════════════════════
    def _rebuild_cards(self):
        for w in self._cards_frame.winfo_children():
            w.destroy()
        self._card_refs = []
        n = self.places + 1
        for i in range(n):
            if i > 0:
                tk.Label(self._cards_frame, text="·", bg=SURFACE,
                         fg=TEXT3, font=("Helvetica",14,"bold")
                         ).grid(row=0, column=i*2-1)
            color = PLACE_COLORS[i]
            f = tk.Frame(self._cards_frame, bg=SRF2,
                         highlightbackground=BORDER, highlightthickness=1)
            f.grid(row=0, column=i*2, sticky="nsew", padx=1)
            self._cards_frame.columnconfigure(i*2, weight=1)
            tk.Label(f, text=PLACE_NAMES[i], bg=SRF2, fg=TEXT3,
                     font=("Helvetica",8), pady=2).pack()
            vl = tk.Label(f, text="0", bg=SRF2, fg=TEXT3,
                          font=("Courier",16,"bold"))
            vl.pack()
            tk.Label(f, text=PLACE_MULTS[i], bg=SRF2, fg=TEXT3,
                     font=("Helvetica",7), pady=2).pack()
            self._card_refs.append((f, vl, color))

    def _update_cards(self):
        for i, (f, vl, color) in enumerate(self._card_refs):
            v = self.digits[i]
            act = v > 0
            f.config(highlightbackground=color if act else BORDER,
                     highlightthickness=2 if act else 1)
            vl.config(text=str(v), fg=color if act else TEXT3)

    # ══ КІЛЬКІСТЬ РОЗРЯДІВ ══════════════════════════════════════════
    def _set_places(self, n):
        for i in range(n+1, 6):
            self.digits[i] = 0
        self.places = n
        self._refresh_place_btns()
        self._rebuild_sliders()
        self._rebuild_cards()
        self._full_refresh()

    def _refresh_place_btns(self):
        for i, b in enumerate(self._place_btns):
            act = (i == self.places - 1)
            b.config(bg=C_BLUE if act else SRF2,
                     fg="white" if act else TEXT2,
                     relief="sunken" if act else "flat")

    # ══ ДИСПЛЕЙ ═════════════════════════════════════════════════════
    def _refresh_display(self):
        val   = digits_to_val(self.digits)
        int_p = self.digits[0]
        dec_p = "".join(str(self.digits[i]) for i in range(1, self.places+1))
        self.lbl_int.config(text=str(int_p))
        self.lbl_dec.config(text=dec_p)
        self.lbl_name.config(text=num_name(self.digits, self.places))
        self.lbl_frac.config(text=f"= {frac_str(val)}")
        self._update_cards()
        self._update_frac_list(val)

    def _update_frac_list(self, val):
        for w in self._frac_frame.winfo_children():
            w.destroy()
        if val == 0:
            tk.Label(self._frac_frame, text="0 = 0/1",
                     bg=SURFACE, fg=TEXT3, font=("Courier",10)).pack(anchor="w")
            return
        seen, fracs = set(), []
        for den in [10,100,1000,10000,4,5,8,20,25,2,3]:
            nr = round(val*den)
            if nr == 0: continue
            g = gcd(nr, den)
            n, d = nr//g, den//g
            if (n,d) not in seen and abs(n/d-val) < 1e-6:
                seen.add((n,d)); fracs.append((n,d))
        for n, d in fracs[:5]:
            row = tk.Frame(self._frac_frame, bg=SRF2,
                           highlightbackground=BORDER, highlightthickness=1)
            row.pack(fill="x", pady=2)
            row.columnconfigure(1, weight=1)
            tk.Label(row, text=f"{n}/{d}", bg=SRF2, fg=C_CYAN,
                     font=("Courier",11,"bold"), width=9
                     ).grid(row=0, column=0, padx=6, pady=4)
            bb = tk.Frame(row, bg=SRF2, height=8)
            bb.grid(row=0, column=1, sticky="ew", padx=(0,6))
            p = min(1.0, n/d)
            def draw(e, bg=bb, pct=p):
                for c in bg.winfo_children(): c.destroy()
                w2 = max(1, int(bg.winfo_width()*pct))
                tk.Frame(bg, bg=C_CYAN, height=8, width=w2).place(x=0,y=0)
                tk.Frame(bg, bg=BORDER, height=8,
                         width=max(0,bg.winfo_width()-w2)).place(x=w2,y=0)
            bb.bind("<Configure>", draw)

    # ══ REFRESH ═════════════════════════════════════════════════════
    def _full_refresh(self):
        self._sync_sliders()
        self._refresh_display()
        self._redraw()

    def _redraw(self):
        self.fig.clear()
        tab = self.nb.index(self.nb.select())
        [self._draw_line, self._draw_grid, self._draw_pie,
         self._draw_place, self._draw_ctr, self._draw_cmp][tab]()
        self.mpl.draw_idle()

    def _on_tab(self, event=None):
        tab = self.nb.index(self.nb.select())
        # Показати потрібну панель у ctrl_row, сховати зайві
        for w in self._ctrl_row.winfo_children():
            w.pack_forget()
        if tab == 4 and hasattr(self, "_ctr_overlay"):
            self._ctr_overlay.pack(fill="x")
        elif tab == 5 and hasattr(self, "_cmp_overlay"):
            self._cmp_overlay.pack(fill="x")
        self._redraw()

    # ══ МАСШТАБ ═════════════════════════════════════════════════════
    def _wheel(self, event):
        if self.nb.index(self.nb.select()) != 0: return
        # фіксація навколо поточної точки
        self.zoom_center = digits_to_val(self.digits)
        factor = 1.6
        if event.num == 4 or (hasattr(event,"delta") and event.delta > 0):
            self.zoom_range = max(0.0002, self.zoom_range / factor)
        else:
            self.zoom_range = min(20.0, self.zoom_range * factor)
        self.fig.clear(); self._draw_line(); self.mpl.draw_idle()

    def _drag_start(self, event):
        if self.nb.index(self.nb.select()) != 0: return
        self._drag_x0 = event.x
        self._drag_c0 = self.zoom_center

    def _drag_move(self, event):
        if self._drag_x0 is None: return
        if self.nb.index(self.nb.select()) != 0: return
        cw    = self.mpl.get_tk_widget().winfo_width()
        shift = -(event.x - self._drag_x0) / cw * self.zoom_range
        self.zoom_center = max(self.zoom_range/2, self._drag_c0 + shift)
        self.fig.clear(); self._draw_line(); self.mpl.draw_idle()

    def _drag_end(self, event): self._drag_x0 = None

    # ══════════════════════════════════════════════════════════════
    #  TAB 0 — ЧИСЛОВА ПРЯМА
    # ══════════════════════════════════════════════════════════════
    def _draw_line(self):
        val = digits_to_val(self.digits)
        # при не-drag: завжди центруємо на значенні
        if self._drag_x0 is None:
            self.zoom_center = val

        half  = self.zoom_range / 2
        start = max(0.0, self.zoom_center - half)
        end   = start + self.zoom_range
        step  = auto_step(self.zoom_range)

        ax = self.fig.add_subplot(111)
        ax.set_facecolor(BG)
        ax.set_xlim(start - self.zoom_range*0.03,
                    end   + self.zoom_range*0.06)
        ax.set_ylim(-1, 1)
        ax.axis("off")

        if self.zoom_range < 1:
            zoom_lbl = f"x{round(1/self.zoom_range,1)}"
        elif self.zoom_range > 1:
            zoom_lbl = f"1/{round(self.zoom_range,1)}"
        else:
            zoom_lbl = "x1"
        ax.set_title(
            f"Числова пряма  [zoom {zoom_lbl}]   "
            "Колесо миші = наближення до точки  ·  Перетягнення = прокрутка",
            color=TEXT3, fontsize=10, loc="left", pad=10)

        ax.annotate("", xy=(end+self.zoom_range*0.04, 0),
                    xytext=(max(0, start-0.005), 0),
                    arrowprops=dict(arrowstyle="->", color=BORDER,
                                   lw=2, mutation_scale=14))

        t = round(math.ceil(start/step)*step, 8)
        while t <= end + step*0.01:
            t = round(t, 8)
            if start - step*0.1 <= t <= end + step*0.1:
                is_w = abs(t - round(t)) < 1e-7
                is_t = abs(t*10 - round(t*10)) < 1e-5
                is_h = abs(t*100 - round(t*100)) < 1e-4
                hh   = 0.38 if is_w else 0.24 if is_t else 0.14 if is_h else 0.08
                col  = TEXT  if is_w else TEXT2 if is_t else BORDER
                lw   = 2.0   if is_w else 1.3  if is_t else 0.8
                ax.plot([t,t], [-hh, hh], color=col, lw=lw, zorder=3)
                show = (is_w
                        or (self.zoom_range <= 2   and is_t)
                        or (self.zoom_range <= 0.2 and is_h)
                        or self.zoom_range <= 0.02)
                if show:
                    dc = 0 if is_w else 1 if is_t else 2 if is_h else 4
                    ax.text(t, -hh-0.13, fmt_tick(t, dc),
                            ha="center", va="top",
                            color=col, fontsize=(10 if is_w else 8 if is_t else 7),
                            fontfamily="monospace")
            t = round(t + step, 8)

        if start - self.zoom_range*0.06 <= val <= end + self.zoom_range*0.06:
            base = math.floor(val)
            s2   = max(start, float(base))
            if s2 < val:
                ax.axvspan(s2, val, ymin=0.44, ymax=0.56,
                           alpha=0.20, color=C_BLUE, zorder=1)
            for r_, a_ in [(0.08,0.05),(0.04,0.11),(0.015,0.20)]:
                ax.axvspan(val-r_*self.zoom_range, val+r_*self.zoom_range,
                           ymin=0.30, ymax=0.70, alpha=a_, color=C_BLUE)
            ax.plot(val, 0, "o", color=C_BLUE, markersize=15, zorder=5,
                    markeredgecolor="white", markeredgewidth=2.5)
            dp = self.places
            ax.text(val, 0.56, fmt(val, dp),
                    ha="center", va="bottom",
                    color=C_BLUE, fontsize=16, fontweight="bold",
                    fontfamily="monospace")

        self.fig.tight_layout(pad=1.5)

    # ══════════════════════════════════════════════════════════════
    #  TAB 1 — СІТКА 100
    # ══════════════════════════════════════════════════════════════
    def _draw_grid(self):
        val   = digits_to_val(self.digits)
        int_  = self.digits[0]
        t     = self.digits[1]
        h     = self.digits[2]
        cents = t*10 + h

        ncols = int_ + 2
        gs = gridspec.GridSpec(1, ncols, figure=self.fig,
                               wspace=0.4, left=0.02, right=0.98,
                               top=0.88, bottom=0.08)
        self.fig.text(0.5, 0.97,
                      f"{fmt(val, self.places)}  =  "
                      f"{int_} {'ціла' if int_==1 else 'цілих'}  +  {cents}/100",
                      ha="center", va="top",
                      color=TEXT, fontsize=13, fontweight="bold")
        col = 0
        for w in range(int_):
            ax = self.fig.add_subplot(gs[0, col]); col+=1
            self._grid100(ax, 100, f"Ціла #{w+1}")
        ax2 = self.fig.add_subplot(gs[0, col]); col+=1
        self._grid100(ax2, cents,
                      f"Дробова\n{cents}/100 = {fmt(val-int_, self.places)}")
        ax3 = self.fig.add_subplot(gs[0, col])
        ax3.set_facecolor(BG); ax3.axis("off")
        ax3.set_xlim(-0.5, 1.5); ax3.set_ylim(-0.5, 10.5)
        ax3.set_title(f"Десяті\n{t}/10", color=TEXT2, fontsize=10, pad=6)
        for idx in range(10):
            r = 9-idx
            filled = idx < t
            clr    = C_BLUE if filled else SRF2
            eclr   = C_BLUE if filled else BORDER
            ax3.add_patch(FancyBboxPatch((0.06,r+0.08),0.82,0.78,
                boxstyle="round,pad=0.04",
                facecolor=clr, edgecolor=eclr, lw=1.2))
            ax3.text(0.5, r+0.5,
                     f"0.{idx+1}" if idx < 9 else "1.0",
                     ha="center", va="center",
                     color="white" if filled else TEXT3,
                     fontsize=8, fontfamily="monospace")

    def _grid100(self, ax, filled, title):
        ax.set_facecolor(BG); ax.axis("off")
        ax.set_xlim(-0.5,10.5); ax.set_ylim(-1.0,10.5)
        ax.set_title(title, color=TEXT2, fontsize=10, pad=6)
        full_r = filled//10
        for idx in range(100):
            row = 9-idx//10; col = idx%10
            in_full  = idx < full_r*10
            in_extra = full_r*10 <= idx < filled
            if filled==100:   clr,al = C_GREEN,0.8
            elif in_full:     clr,al = C_BLUE, 0.75
            elif in_extra:    clr,al = C_CYAN, 0.85
            else:             clr,al = SRF2,   1.0
            eclr = C_BLUE if in_full else C_CYAN if in_extra else BORDER
            ax.add_patch(FancyBboxPatch(
                (col+0.04,row+0.04),0.88,0.88,
                boxstyle="round,pad=0.03",
                facecolor=clr, edgecolor=eclr, lw=0.6, alpha=al))
        for c in range(10):
            ax.text(c+0.5,-0.5,str(c+1),ha="center",va="center",
                    color=TEXT3,fontsize=6.5,fontfamily="monospace")
        legend = [mpatches.Patch(color=C_BLUE, label="Десяті"),
                  mpatches.Patch(color=C_CYAN, label="Соті"),
                  mpatches.Patch(facecolor=SRF2,edgecolor=BORDER,label="Пусто")]
        ax.legend(handles=legend, loc="lower center",
                  bbox_to_anchor=(0.5,-0.10), ncol=3,
                  facecolor=SURFACE, edgecolor=BORDER,
                  labelcolor=TEXT2, fontsize=7, framealpha=0.9)

    # ══════════════════════════════════════════════════════════════
    #  TAB 2 — ТОРТ / ДРОБИ
    # ══════════════════════════════════════════════════════════════
    def _draw_pie(self):
        val  = digits_to_val(self.digits)
        int_ = self.digits[0]
        frac = round(val - int_, 5)

        gs = gridspec.GridSpec(1, 3, figure=self.fig,
                               wspace=0.5, left=0.03, right=0.97,
                               top=0.88, bottom=0.10)
        ax1 = self.fig.add_subplot(gs[0])
        ax1.set_facecolor(BG); ax1.set_aspect("equal"); ax1.axis("off")
        ax1.set_title(
            f"Дробова частина  {fmt(frac, self.places)}\n= {frac_str(frac)}",
            color=TEXT, fontsize=12, pad=10)
        th = np.linspace(0, 2*np.pi, 300)
        ax1.fill(np.cos(th), np.sin(th), color=SRF2)
        ax1.plot(np.cos(th), np.sin(th), color=BORDER, lw=2)
        if frac > 0:
            ang = frac*2*np.pi
            t2  = np.linspace(np.pi/2, np.pi/2-ang, 300)
            xs  = np.concatenate([[0], np.cos(t2), [0]])
            ys  = np.concatenate([[0], np.sin(t2), [0]])
            ax1.fill(xs, ys, color=C_BLUE, alpha=0.80)
            ax1.plot(np.cos(t2), np.sin(t2), color=C_BLUE, lw=2)
        for i in range(10):
            a2 = np.pi/2 - i*2*np.pi/10
            ax1.plot([0,np.cos(a2)],[0,np.sin(a2)],
                     color=BORDER, lw=0.8, alpha=0.6)
            ma = np.pi/2 - (i+0.5)*2*np.pi/10
            ax1.text(0.72*np.cos(ma), 0.72*np.sin(ma),
                     f"0.{i+1}" if i<9 else "1.0",
                     ha="center",va="center",
                     color=TEXT3,fontsize=7,fontfamily="monospace")
        ax1.set_xlim(-1.3,1.3); ax1.set_ylim(-1.3,1.3)

        FAMOUS = [(1,2,0.5),(1,4,0.25),(3,4,0.75),(1,5,0.2),
                  (2,5,0.4),(1,10,0.1),(3,10,0.3),(1,100,0.01)]
        ax2 = self.fig.add_subplot(gs[1])
        ax2.set_facecolor(BG); ax2.axis("off")
        ax2.set_xlim(0,1); ax2.set_ylim(0,1)
        ax2.set_title("Звичайні дроби <-> Десяткові",
                      color=TEXT, fontsize=12, pad=10)
        rh = 0.95/(len(FAMOUS)+1)
        ax2.text(0.5,0.97,"Дріб → Десяткова",ha="center",va="top",
                 color=TEXT3,fontsize=9)
        for ri,(n,d,dv) in enumerate(FAMOUS):
            y = 0.90-ri*rh
            match = abs(dv-frac)<0.001
            clr = C_BLUE if match else TEXT3
            fw  = "bold" if match else "normal"
            ax2.text(0.15,y,f"{n}/{d}",ha="center",va="center",
                     color=clr,fontsize=11,fontweight=fw,fontfamily="monospace")
            ax2.text(0.36,y,"=",ha="center",va="center",
                     color=TEXT3,fontsize=11)
            ax2.text(0.56,y,f"{dv:.2f}".replace(".",","),ha="center",va="center",
                     color=clr,fontsize=11,fontweight=fw,fontfamily="monospace")
            ax2.add_patch(Rectangle((0.63,y-0.025),0.34,0.05,
                facecolor=SRF2,edgecolor=BORDER,lw=0.5))
            ax2.add_patch(Rectangle((0.63,y-0.025),0.34*dv,0.05,
                facecolor=clr if match else C_CYAN,alpha=0.75))

        ax3 = self.fig.add_subplot(gs[2])
        ax3.set_facecolor(BG); ax3.axis("off")
        ax3.set_xlim(0,1); ax3.set_ylim(0,1)
        ax3.set_title(f"Число {fmt(val, self.places)} у вигляді тортів",
                      color=TEXT, fontsize=12, pad=10)
        total = int_+1
        cols3 = 3
        rows3 = math.ceil(total/cols3)
        pw = 0.26; ph = 0.26
        mx = (1-cols3*pw)/(cols3+1)
        my = (0.9-rows3*ph)/(rows3+1)
        for pi in range(total):
            r,c = divmod(pi,cols3)
            cx  = mx + c*(pw+mx) + pw/2
            cy  = 0.92 - (r*(ph+my)+ph/2)
            full = pi<int_
            fill = 1.0 if full else frac
            clr  = C_GREEN if full else C_BLUE
            th2  = np.linspace(0,2*np.pi,80)
            ax3.fill(cx+pw/2*np.cos(th2), cy+ph/2*np.sin(th2), color=SRF2)
            ax3.plot(cx+pw/2*np.cos(th2), cy+ph/2*np.sin(th2),
                     color=BORDER, lw=1)
            if fill > 0:
                t3 = np.linspace(np.pi/2, np.pi/2-fill*2*np.pi, 80)
                xf = np.concatenate([[cx], cx+pw/2*np.cos(t3), [cx]])
                yf = np.concatenate([[cy], cy+ph/2*np.sin(t3), [cy]])
                ax3.fill(xf, yf, color=clr, alpha=0.82)
            lbl = "1" if full else f"{frac:.2f}".replace(".",",").replace(".",",")
            ax3.text(cx, cy, lbl, ha="center", va="center",
                     color="white" if fill>0.3 else TEXT3,
                     fontsize=8, fontweight="bold")

    # ══════════════════════════════════════════════════════════════
    #  TAB 3 — РОЗРЯДИ
    # ══════════════════════════════════════════════════════════════
    def _draw_place(self):
        val = digits_to_val(self.digits)
        n   = self.places + 1

        gs = gridspec.GridSpec(2, 1, figure=self.fig,
                               hspace=0.75, top=0.90, bottom=0.06,
                               left=0.03, right=0.97)
        ax1 = self.fig.add_subplot(gs[0])
        ax1.set_facecolor(BG)
        ax1.set_xlim(0, n*2); ax1.set_ylim(0,1); ax1.axis("off")
        ax1.set_title("Кожна цифра — окремий розряд",
                      color=TEXT2, fontsize=11, loc="left", pad=8)
        for i in range(n):
            xi    = i*2
            v     = self.digits[i]
            color = PLACE_COLORS[i]
            active= v > 0
            if i == 1:
                ax1.text(xi-0.5, 0.5, ",", ha="center", va="center",
                         color=TEXT3, fontsize=36, fontweight="bold")
            bg_c = color+"22" if active else "#F1F5F9"
            ax1.add_patch(FancyBboxPatch((xi+0.06,0.05),0.84,0.90,
                boxstyle="round,pad=0.04",
                facecolor=bg_c,
                edgecolor=color if active else BORDER,
                linewidth=2.5 if active else 1))
            ax1.text(xi+0.5, 0.82, PLACE_NAMES[i],
                     ha="center",va="center",
                     color=color if active else TEXT3,
                     fontsize=8,fontfamily="monospace")
            ax1.text(xi+0.5, 0.50, str(v),
                     ha="center",va="center",
                     color=color if active else TEXT3,
                     fontsize=30,fontweight="bold",fontfamily="monospace")
            ax1.text(xi+0.5, 0.17, PLACE_MULTS[i],
                     ha="center",va="center",
                     color=TEXT3,fontsize=8,fontfamily="monospace")
        try:
            tbl = ax1.table(cellText=[[str(self.digits[i]) for i in range(n)]],
                            colLabels=PLACE_NAMES[:n],
                            loc="bottom", bbox=[0.0,-0.55,1.0,0.44])
            tbl.auto_set_font_size(False); tbl.set_fontsize(9)
            for (r,c), cell in tbl.get_celld().items():
                cell.set_facecolor(SRF2 if r==0 else SURFACE)
                cell.set_edgecolor(BORDER)
                cell.set_text_props(
                    color=PLACE_COLORS[c] if r==1 else TEXT3,
                    fontfamily="monospace", fontweight="bold")
        except Exception: pass

        ax2 = self.fig.add_subplot(gs[1])
        ax2.set_facecolor(SURFACE); ax2.axis("off")
        ax2.set_xlim(0,10); ax2.set_ylim(0,1)
        ax2.set_title("Розклад числа", color=TEXT2, fontsize=11,
                      loc="left", pad=8)
        mvs = [1,0.1,0.01,0.001,0.0001,0.00001]
        parts = []
        for i in range(n):
            if self.digits[i] > 0:
                r = round(self.digits[i]*mvs[i], 5)
                parts.append((f"{self.digits[i]}x{mvs[i]}={r:.{max(i,1)}f}",
                               PLACE_COLORS[i]))
        if not parts: parts = [("0x1=0", TEXT3)]
        gap = 10/(len(parts)+1)
        for pi,(txt,col) in enumerate(parts):
            xc = gap*(pi+1)
            ax2.text(xc, 0.70, txt, ha="center",va="center",
                     color=col,fontsize=10,fontfamily="monospace",fontweight="bold")
            if pi < len(parts)-1:
                ax2.text(xc+gap*0.5, 0.70, "+",
                         ha="center",va="center",color=TEXT3,fontsize=14)
        ax2.text(5, 0.22,
                 f"= {fmt(val, self.places)}   ({num_name(self.digits, self.places)})",
                 ha="center",va="center",
                 color=C_BLUE,fontsize=14,fontweight="bold",
                 fontfamily="monospace")

    # ══════════════════════════════════════════════════════════════
    #  TAB 4 — ЛІЧИЛЬНИК
    # ══════════════════════════════════════════════════════════════
    def _build_ctr_overlay(self, parent):
        ctrl = tk.Frame(parent, bg=SURFACE,
                        highlightbackground=BORDER, highlightthickness=2)
        self._ctr_overlay = ctrl
        # Буде показано через pack у _on_tab

        tk.Label(ctrl, text="Крок:", bg=SURFACE, fg=TEXT2,
                 font=("Helvetica",11)).pack(side="left",padx=(12,4),pady=10)
        step_e = tk.Entry(ctrl, textvariable=self._ctr_step_var,
                          width=7, font=("Courier",12),
                          bg=SRF2, fg=TEXT, relief="flat", bd=3)
        step_e.pack(side="left", pady=10)

        self._ctr_step_btns = {}
        for s in ["0.001","0.01","0.1","1","0.25","0.5"]:
            b = tk.Button(ctrl, text=s, bg=SRF2, fg=TEXT2,
                          font=("Courier",10), relief="flat", cursor="hand2",
                          padx=6,
                          command=lambda sv=s: self._ctr_set_step(sv))
            b.pack(side="left", padx=2, pady=10)
            self._ctr_step_btns[s] = b
        self._ctr_set_step("0.1")

        tk.Button(ctrl, text="  +  ", bg=C_BLUE, fg="white",
                  font=("Helvetica",14,"bold"), relief="flat", cursor="hand2",
                  command=self._ctr_add).pack(side="left", padx=(16,4), pady=8)
        tk.Button(ctrl, text="  -  ", bg=C_RED,  fg="white",
                  font=("Helvetica",14,"bold"), relief="flat", cursor="hand2",
                  command=self._ctr_sub).pack(side="left", padx=4, pady=8)
        tk.Button(ctrl, text="Скинути", bg=SRF2, fg=TEXT2,
                  font=("Helvetica",10), relief="flat", cursor="hand2",
                  command=self._ctr_reset).pack(side="left", padx=10, pady=8)

        self._ctr_msg = tk.Label(ctrl, text="", bg=SURFACE, fg=C_GREEN,
                                 font=("Helvetica",11,"bold"))
        self._ctr_msg.pack(side="left", padx=10)

    def _ctr_set_step(self, s):
        self._ctr_step_var.set(s)
        for sv, b in self._ctr_step_btns.items():
            b.config(bg=C_BLUE if sv==s else SRF2,
                     fg="white" if sv==s else TEXT2)

    def _ctr_step(self):
        try:    return float(self._ctr_step_var.get())
        except: return 0.1

    def _ctr_add(self):
        prev = self.ctr_val
        self.ctr_val = round(prev + self._ctr_step(), 5)
        if int(self.ctr_val) > int(prev):
            self._ctr_msg.config(
                text=f"Переповнення! {fmt(prev,4)} + {str(self._ctr_step()).replace(chr(46),chr(44))} = {fmt(self.ctr_val,4)}  (нова ціла!)")
            self.after(2500, lambda: self._ctr_msg.config(text=""))
        self.ctr_hist.append(self.ctr_val)
        if len(self.ctr_hist) > 60: self.ctr_hist = self.ctr_hist[-60:]
        self._redraw()

    def _ctr_sub(self):
        self.ctr_val = max(0.0, round(self.ctr_val - self._ctr_step(), 5))
        self.ctr_hist.append(self.ctr_val)
        if len(self.ctr_hist) > 60: self.ctr_hist = self.ctr_hist[-60:]
        self._redraw()

    def _ctr_reset(self):
        self.ctr_val  = 0.0
        self.ctr_hist = [0.0]
        self._ctr_msg.config(text="")
        self._redraw()

    def _draw_ctr(self):
        v    = self.ctr_val
        int_ = int(v)
        frac = round(v - int_, 5)
        hist = self.ctr_hist[-28:]

        gs = gridspec.GridSpec(1, 3, figure=self.fig,
                               wspace=0.45, left=0.05, right=0.97,
                               top=0.82, bottom=0.12)
        self.fig.text(0.5, 0.97,
                      f"{v:.5f}".replace(".",",").rstrip("0").rstrip(",") or "0",
                      ha="center", va="top",
                      color=C_BLUE, fontsize=26, fontweight="bold",
                      fontfamily="monospace")
        self.fig.text(0.5, 0.90,
                      f"крок = {str(self._ctr_step()).replace(chr(46), chr(44))}",
                      ha="center", va="top",
                      color=TEXT3, fontsize=10)

        # Склянки
        ax1 = self.fig.add_subplot(gs[0])
        ax1.set_facecolor(BG); ax1.axis("off")
        n_c = max(int_+1, 1)
        ax1.set_xlim(-0.1,1.1); ax1.set_ylim(-0.3, n_c+0.1)
        ax1.set_title("Склянки (1 повна = 1 ціла)",
                      color=TEXT2, fontsize=11, pad=8)
        for ci in range(int_):
            y0 = ci
            ax1.add_patch(Rectangle((0.05,y0+0.04),0.90,0.87,
                facecolor=C_CYAN, alpha=0.60, edgecolor=C_CYAN, lw=0))
            ax1.add_patch(Rectangle((0.05,y0),0.90,0.95,
                facecolor="none", edgecolor=TEXT2, lw=2.5))
            ax1.text(0.5,y0+0.47,"1.0",
                     ha="center",va="center",
                     color=TEXT,fontsize=12,fontweight="bold",
                     fontfamily="monospace")
        y0 = int_
        fh = frac*0.87
        ax1.add_patch(Rectangle((0.05,y0),0.90,0.95,
            facecolor="none", edgecolor=TEXT2, lw=2.5))
        if fh > 0:
            ax1.add_patch(Rectangle((0.10,y0+0.04),0.80,fh,
                facecolor=C_BLUE, alpha=0.72))
        ax1.text(0.5,y0+0.5,
                 f"{frac:.4f}".replace(".",",").rstrip("0").rstrip(",") or "0",
                 ha="center",va="center",
                 color=C_BLUE if frac>0.35 else TEXT3,
                 fontsize=11,fontweight="bold",fontfamily="monospace")

        # Числова пряма
        ax2 = self.fig.add_subplot(gs[1])
        ax2.set_facecolor(BG); ax2.axis("off")
        lo = max(0, math.floor(v)-0.1)
        hi = max(lo+1.2, v+0.4)
        ax2.set_xlim(lo-0.05, hi+0.08); ax2.set_ylim(-1,1)
        ax2.set_title("Положення на прямій",color=TEXT2,fontsize=11,pad=8)
        ax2.annotate("",xy=(hi+0.06,0),xytext=(lo,0),
                     arrowprops=dict(arrowstyle="->",color=BORDER,
                                     lw=1.5,mutation_scale=12))
        rng2 = hi-lo
        s2   = 0.1 if rng2<=2 else 0.5
        tt   = round(math.ceil(lo/s2)*s2, 5)
        while tt <= hi:
            tt = round(tt,5)
            iw = abs(tt-round(tt))<1e-6
            hh = 0.28 if iw else 0.14
            ax2.plot([tt,tt],[-hh,hh],
                     color=TEXT if iw else TEXT3,
                     lw=1.8 if iw else 0.9)
            ax2.text(tt,-hh-0.12,
                     fmt_tick(tt, 0 if iw else 1),
                     ha="center",va="top",
                     color=TEXT if iw else TEXT3,
                     fontsize=9 if iw else 7,fontfamily="monospace")
            tt = round(tt+s2,5)
        ax2.plot(v,0,"o",color=C_BLUE,markersize=13,zorder=5,
                 markeredgecolor="white",markeredgewidth=2.5)
        ax2.text(v,0.45,f"{v:.4f}".replace(".",","),
                 ha="center",va="bottom",
                 color=C_BLUE,fontsize=12,fontweight="bold",
                 fontfamily="monospace")

        # Історія
        ax3 = self.fig.add_subplot(gs[2])
        ax3.set_facecolor(BG)
        ax3.set_title("Історія кроків",color=TEXT2,fontsize=11,pad=8)
        if len(hist) > 1:
            xs = list(range(len(hist)))
            ax3.plot(xs, hist, color=C_BLUE, lw=2.5, marker="o",
                     markersize=5, markerfacecolor=C_CYAN,
                     markeredgecolor="white", markeredgewidth=1.5)
            ax3.fill_between(xs, hist, alpha=0.10, color=C_BLUE)
            for i in range(1,len(hist)):
                if int(hist[i]) != int(hist[i-1]):
                    ax3.axvline(i, color=C_GREEN, lw=2,
                                linestyle="--", alpha=0.8)
                    ax3.text(i+0.1,(hist[i]+hist[i-1])/2,
                             " ціла!", color=C_GREEN,fontsize=8,va="center")
        else:
            ax3.plot([0],hist,"o",color=C_BLUE,markersize=8)
        ax3.tick_params(colors=TEXT2,labelsize=8)
        for sp in ["bottom","left"]:
            ax3.spines[sp].set_color(BORDER)
        ax3.set_xlabel("Кроки",color=TEXT3,fontsize=9)
        ax3.set_ylabel("Значення",color=TEXT3,fontsize=9)

    # ══════════════════════════════════════════════════════════════
    #  TAB 5 — ПОРІВНЯННЯ
    # ══════════════════════════════════════════════════════════════
    def _build_cmp_overlay(self, parent):
        ctrl = tk.Frame(parent, bg=SURFACE,
                        highlightbackground=BORDER, highlightthickness=2)
        self._cmp_overlay = ctrl
        # Буде показано через pack у _on_tab

        LABS = ["Од.","Дес.","Соті","Тис.","Дес-тис."]

        for side, (digits, lbl_text, color) in enumerate([
            (self.cmp_a, "A", C_RED),
            (self.cmp_b, "B", C_GREEN),
        ]):
            frm = tk.Frame(ctrl, bg=SURFACE)
            frm.pack(side="left", padx=(16 if side==0 else 30, 4), pady=8)
            tk.Label(frm, text=f"Число {lbl_text}:", bg=SURFACE,
                     fg=color, font=("Helvetica",11,"bold")
                     ).pack(side="left", padx=(0,6))
            for i in range(self.places+1):
                tk.Label(frm, text=LABS[i]+":", bg=SURFACE,
                         fg=TEXT3, font=("Helvetica",9)).pack(side="left")
                var = tk.IntVar(value=digits[i])
                sp  = tk.Spinbox(frm, from_=0, to=9, textvariable=var,
                                 width=2, font=("Courier",13),
                                 relief="flat", bg=SRF2, fg=color, bd=2,
                                 command=lambda vi=i, vr=var, d=digits:
                                     self._cmp_cb(vi,vr,d))
                sp.bind("<Return>",
                        lambda e, vi=i, vr=var, d=digits:
                            self._cmp_cb(vi,vr,d))
                sp.bind("<FocusOut>",
                        lambda e, vi=i, vr=var, d=digits:
                            self._cmp_cb(vi,vr,d))
                sp.pack(side="left", padx=(2,8))

    def _cmp_cb(self, idx, var, digits):
        try:    v = max(0, min(9, int(var.get())))
        except: return
        digits[idx] = v
        var.set(v)
        self._redraw()

    def _draw_cmp(self):
        va = digits_to_val(self.cmp_a)
        vb = digits_to_val(self.cmp_b)

        gs = gridspec.GridSpec(2, 1, figure=self.fig,
                               hspace=0.65, top=0.86, bottom=0.08,
                               left=0.05, right=0.96)

        if   va < vb: sym,clr = "<", C_GREEN
        elif va > vb: sym,clr = ">", C_RED
        else:         sym,clr = "=", C_PURP

        self.fig.text(0.5, 0.97,
                      f"A = {fmt(va, self.places)}   {sym}   B = {fmt(vb, self.places)}"
                      f"     різниця: {fmt(abs(vb-va), self.places)}",
                      ha="center", va="top",
                      color=clr, fontsize=16, fontweight="bold",
                      fontfamily="monospace")

        ax1 = self.fig.add_subplot(gs[0])
        ax1.set_facecolor(BG); ax1.axis("off")
        rng = max(abs(vb-va)*2.5, 0.5)
        lo  = max(0.0, (va+vb)/2 - rng/2)
        hi  = lo + rng
        ax1.set_xlim(lo-rng*0.04, hi+rng*0.06)
        ax1.set_ylim(-1,1)
        ax1.set_title("Числова пряма — порівняння A та B",
                      color=TEXT2, fontsize=11, loc="left", pad=8)
        ax1.annotate("",xy=(hi+rng*0.04,0),xytext=(max(0,lo-0.01),0),
                     arrowprops=dict(arrowstyle="->",color=BORDER,
                                     lw=1.8,mutation_scale=14))
        step = auto_step(rng)
        t = round(math.ceil(lo/step)*step,8)
        while t <= hi+step*0.01:
            t = round(t,8)
            if lo<=t<=hi:
                iw = abs(t-round(t))<1e-7
                it = abs(t*10-round(t*10))<1e-5
                hh = 0.30 if iw else 0.18 if it else 0.10
                col2 = TEXT if iw else TEXT3
                ax1.plot([t,t],[-hh,hh],color=col2,lw=1.8 if iw else 0.9)
                if iw or (rng<=2 and it):
                    dc = 0 if iw else 1 if it else 2
                    ax1.text(t,-hh-0.12,fmt_tick(t,dc),
                             ha="center",va="top",color=col2,
                             fontsize=9 if iw else 7,fontfamily="monospace")
            t = round(t+step,8)
        for v,col,lbl,yo in [(va,C_RED,"A",0.52),(vb,C_GREEN,"B",-0.52)]:
            if lo-rng*0.06<=v<=hi+rng*0.06:
                ax1.plot(v,0,"o",color=col,markersize=13,zorder=5,
                         markeredgecolor="white",markeredgewidth=2.5)
                ax1.text(v,yo,f"{lbl}={fmt(v, self.places)}",
                         ha="center",va="center",
                         color=col,fontsize=12,fontweight="bold",
                         fontfamily="monospace")
                ax1.plot([v,v],[0,yo*0.72],color=col,lw=1.2,
                         linestyle="--",alpha=0.5)
        if abs(va-vb)>0.0001:
            lo2,hi2 = min(va,vb),max(va,vb)
            if lo<=lo2 and hi2<=hi:
                ax1.annotate("",xy=(hi2,-0.18),xytext=(lo2,-0.18),
                             arrowprops=dict(arrowstyle="<->",
                                             color=C_PURP,lw=1.8))
                ax1.text((lo2+hi2)/2,-0.34,
                         f"різниця {fmt(abs(vb-va), self.places)}",
                         ha="center",va="top",
                         color=C_PURP,fontsize=9,fontfamily="monospace")

        ax2 = self.fig.add_subplot(gs[1])
        ax2.set_facecolor(BG); ax2.axis("off")
        ax2.set_xlim(0,1); ax2.set_ylim(0,1)
        ax2.set_title("Порівняння розмірів",
                      color=TEXT2,fontsize=11,loc="left",pad=8)
        mx = max(va,vb,0.001)
        for yi,(v,col,lbl) in enumerate([(va,C_RED,"A"),(vb,C_GREEN,"B")]):
            y = 0.75-yi*0.42
            ax2.text(0.03,y,lbl,ha="center",va="center",
                     color=col,fontsize=14,fontweight="bold")
            ax2.add_patch(Rectangle((0.08,y-0.11),0.80,0.22,
                facecolor=SRF2,edgecolor=BORDER,lw=1))
            ax2.add_patch(Rectangle((0.08,y-0.11),0.80*v/mx,0.22,
                facecolor=col,alpha=0.78))
            ax2.text(0.09+0.80*v/mx, y, f"  {fmt(v, self.places)}",
                     ha="left",va="center",
                     color=col,fontsize=12,fontweight="bold",
                     fontfamily="monospace")


# ══════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    plt.rcParams.update(PLT)
    app = App()
    app.mainloop()
