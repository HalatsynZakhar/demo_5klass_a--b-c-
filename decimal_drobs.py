"""
Інтерактивний тренажер: Десяткові дроби
Запуск: python decimal_visualizer.py
Потрібно: pip install matplotlib
"""

import tkinter as tk
from tkinter import ttk, font
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyBboxPatch, Rectangle, Wedge
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
import numpy as np
import math

# ─── СВІТЛА ТЕМА ────────────────────────────────────────────────────
BG       = "#F5F6FA"
SURFACE  = "#FFFFFF"
SURFACE2 = "#EEF0F7"
BORDER   = "#C8CCE0"
ACCENT   = "#2563EB"   # синій
ACCENT2  = "#0891B2"   # блакитний
ACCENT3  = "#DC2626"   # червоний
ACCENT4  = "#16A34A"   # зелений
ACCENT5  = "#7C3AED"   # фіолетовий
ACCENT6  = "#EA580C"   # помаранчевий
TEXT     = "#1E293B"
TEXT_DIM = "#64748B"
TEXT_MID = "#94A3B8"
GRID_CLR = "#E2E8F0"

PLT_PARAMS = {
    "figure.facecolor":  SURFACE,
    "axes.facecolor":    BG,
    "text.color":        TEXT,
    "axes.labelcolor":   TEXT,
    "xtick.color":       TEXT_DIM,
    "ytick.color":       TEXT_DIM,
    "axes.edgecolor":    BORDER,
    "axes.titlecolor":   TEXT,
    "grid.color":        GRID_CLR,
    "font.family":       "sans-serif",
    "axes.spines.top":   False,
    "axes.spines.right": False,
}


# ─── УТИЛІТИ ────────────────────────────────────────────────────────
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def number_name_uk(val_str):
    """Проста назва числа українською за рядком '0.075' тощо."""
    try:
        parts = val_str.split('.')
        int_p = int(parts[0])
        dec_s = parts[1].rstrip('0') if len(parts) > 1 else ''
    except Exception:
        return ''

    int_names = ['нуль','одна','дві','три','чотири',
                 'п\'ять','шість','сім','вісім','дев\'ять']
    place_names = {1:'десят', 2:'сот', 3:'тисячн', 4:'десятитисячн'}
    place_end1  = {1:'а', 2:'а', 3:'а', 4:'а'}
    place_endN  = {1:'их', 2:'их', 3:'их', 4:'их'}

    result = []
    if int_p > 0:
        suf = ' ціла' if int_p == 1 else ' цілих'
        result.append(str(int_p) + suf)

    if dec_s:
        n = int(dec_s)
        d = 10 ** len(dec_s)
        place = len(dec_s)
        pname = place_names.get(place, '')
        if pname:
            end = place_end1[place] if n == 1 else place_endN[place]
            result.append(f'{n} {pname}{end}')
        else:
            result.append(f'{n}/{d}')

    return ' '.join(result) if result else 'нуль'


def decimal_to_fraction_str(val, precision=10000):
    """Повертає рядок 'n/d' у скороченому вигляді."""
    n = round(val * precision)
    d = precision
    g = gcd(abs(n), d)
    return f"{n//g}/{d//g}" if n != 0 else "0"


class NumberState:
    """Зберігає число як цілі + 5 десяткових розрядів (int)."""
    PLACES = 5  # десяті, соті, тисячні, десятитисячні, стотисячні

    def __init__(self, digits=None):
        # digits[0]=ціла, digits[1]=десяті, ..., digits[5]=стотисячні
        self.digits = list(digits) if digits else [0] * 6

    def get_value(self):
        v = float(self.digits[0])
        for i, d in enumerate(self.digits[1:], 1):
            v += d * (10 ** -i)
        return round(v, 5)

    def get_str(self, dec_places=4):
        int_part = self.digits[0]
        dec_part = ''.join(str(self.digits[i]) for i in range(1, dec_places + 2))
        return f"{int_part}.{dec_part}"

    def set_from_value(self, val):
        val = max(0.0, round(val, 5))
        self.digits[0] = int(val)
        rem = val - self.digits[0]
        for i in range(1, 6):
            rem = round(rem * 10, 5)
            self.digits[i] = int(rem)
            rem -= self.digits[i]

    def add(self, step_val):
        new_val = round(self.get_value() + step_val, 5)
        new_val = max(0.0, new_val)
        self.set_from_value(new_val)


# ════════════════════════════════════════════════════════════════════
#  ГОЛОВНЕ ВІКНО
# ════════════════════════════════════════════════════════════════════
class DecimalVisualizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Десяткові дроби — тренажер для класу")
        self.configure(bg=BG)
        try:
            self.state('zoomed')
        except tk.TclError:
            self.attributes('-zoomed', True)

        plt.rcParams.update(PLT_PARAMS)

        self.state1 = NumberState([0, 7, 5, 0, 0, 0])
        self.dec_places = 2          # скільки розрядів показувати (2–5)
        self.zoom_center = None      # центр масштабування
        self.zoom_range  = 1.0       # відображувана ширина числової прямої
        self._zoom_dragging = False
        self._drag_start_x = None
        self._drag_start_range = None

        self._setup_fonts()
        self._setup_styles()
        self._build_ui()
        self._update_all()

    # ─── FONTS ──────────────────────────────────────────────────────
    def _setup_fonts(self):
        self.fn_big   = font.Font(family="Courier", size=38, weight="bold")
        self.fn_title = font.Font(family="Helvetica", size=13, weight="bold")
        self.fn_body  = font.Font(family="Helvetica", size=11)
        self.fn_small = font.Font(family="Courier",   size=9)
        self.fn_mono  = font.Font(family="Courier",   size=12)
        self.fn_card  = font.Font(family="Courier",   size=16, weight="bold")
        self.fn_name  = font.Font(family="Helvetica", size=10, slant="italic")

    # ─── STYLES ─────────────────────────────────────────────────────
    def _setup_styles(self):
        st = ttk.Style(self)
        st.theme_use("clam")
        st.configure("TFrame",    background=BG)
        st.configure("TLabel",    background=BG, foreground=TEXT,
                     font=("Helvetica", 11))
        st.configure("TNotebook", background=BG, borderwidth=0)
        st.configure("TNotebook.Tab",
                     background=SURFACE2, foreground=TEXT_DIM,
                     padding=[14, 7], font=("Helvetica", 11, "bold"),
                     borderwidth=0)
        st.map("TNotebook.Tab",
               background=[("selected", SURFACE)],
               foreground=[("selected", ACCENT)])
        st.configure("TScale", background=BG, troughcolor=BORDER,
                     sliderrelief="flat", sliderlength=18)
        st.configure("TButton", font=("Helvetica", 11),
                     background=SURFACE2, foreground=TEXT,
                     borderwidth=1, relief="flat", padding=6)
        st.map("TButton",
               background=[("active", BORDER)],
               relief=[("pressed", "sunken")])

    # ─── BUILD UI ───────────────────────────────────────────────────
    def _build_ui(self):
        self.columnconfigure(0, minsize=320)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._build_left_panel()
        self._build_right_panel()

    # ══ LEFT PANEL ══════════════════════════════════════════════════
    def _build_left_panel(self):
        left = tk.Frame(self, bg=SURFACE,
                        highlightbackground=BORDER, highlightthickness=1)
        left.grid(row=0, column=0, sticky="nsew")
        left.columnconfigure(0, weight=1)

        # ── Дисплей числа ──
        disp = tk.Frame(left, bg=SURFACE2)
        disp.grid(row=0, column=0, sticky="ew")

        tk.Label(disp, text="ДЕСЯТКОВА ДРІБ", bg=SURFACE2,
                 fg=TEXT_DIM, font=self.fn_small,
                 padx=20, pady=8).pack(anchor="w")

        num_row = tk.Frame(disp, bg=SURFACE2)
        num_row.pack(padx=20, anchor="w")

        self.lbl_int  = tk.Label(num_row, text="0",  bg=SURFACE2,
                                 fg=TEXT,     font=self.fn_big)
        self.lbl_dot  = tk.Label(num_row, text=".",  bg=SURFACE2,
                                 fg=TEXT_DIM, font=self.fn_big)
        self.lbl_dec  = tk.Label(num_row, text="75", bg=SURFACE2,
                                 fg=ACCENT,   font=self.fn_big)
        for w in (self.lbl_int, self.lbl_dot, self.lbl_dec):
            w.pack(side="left")

        self.lbl_name = tk.Label(disp, text="", bg=SURFACE2,
                                 fg=TEXT_DIM, font=self.fn_name, pady=4)
        self.lbl_name.pack(anchor="w", padx=20)

        # Звичайний дріб
        self.lbl_frac_eq = tk.Label(disp, text="= 3/4", bg=SURFACE2,
                                    fg=ACCENT2, font=self.fn_mono, pady=4)
        self.lbl_frac_eq.pack(anchor="w", padx=20)

        # ── Кількість розрядів ──
        self._sep(left, 1)
        tk.Label(left, text="КІЛЬКІСТЬ РОЗРЯДІВ", bg=SURFACE,
                 fg=TEXT_DIM, font=self.fn_small, padx=20, pady=4
                 ).grid(row=2, column=0, sticky="w")

        pr_frame = tk.Frame(left, bg=SURFACE)
        pr_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 8))

        self.place_btns = []
        labels = ["десяті\n(0.1)", "соті\n(0.01)", "тисячні\n(0.001)",
                  "10-тис\n(0.0001)", "100-тис\n(0.00001)"]
        for i, lbl in enumerate(labels):
            b = tk.Button(pr_frame, text=lbl, relief="flat",
                          font=font.Font(family="Helvetica", size=8),
                          bg=SURFACE2, fg=TEXT_DIM, cursor="hand2",
                          command=lambda n=i+1: self._set_places(n))
            b.grid(row=0, column=i, padx=2, sticky="ew")
            pr_frame.columnconfigure(i, weight=1)
            self.place_btns.append(b)
        self._set_places(2, init=True)

        # ── Повзунки ──
        self._sep(left, 4)
        tk.Label(left, text="ЗНАЧЕННЯ", bg=SURFACE,
                 fg=TEXT_DIM, font=self.fn_small, padx=20, pady=4
                 ).grid(row=5, column=0, sticky="w")

        self.sliders_frame = tk.Frame(left, bg=SURFACE)
        self.sliders_frame.grid(row=6, column=0, sticky="ew",
                                padx=16, pady=(0, 8))
        self.sliders_frame.columnconfigure(1, weight=1)
        self._rebuild_sliders()

        # ── Картки розрядів ──
        self._sep(left, 7)
        tk.Label(left, text="РОЗРЯДИ", bg=SURFACE,
                 fg=TEXT_DIM, font=self.fn_small, padx=20, pady=4
                 ).grid(row=8, column=0, sticky="w")

        self.cards_outer = tk.Frame(left, bg=SURFACE)
        self.cards_outer.grid(row=9, column=0, sticky="ew",
                              padx=16, pady=(0, 8))
        self._rebuild_cards()

        # ── Еквівалентні дроби ──
        self._sep(left, 10)
        tk.Label(left, text="ЗВИЧАЙНІ ДРОБИ", bg=SURFACE,
                 fg=TEXT_DIM, font=self.fn_small, padx=20, pady=4
                 ).grid(row=11, column=0, sticky="w")

        self.frac_outer = tk.Frame(left, bg=SURFACE)
        self.frac_outer.grid(row=12, column=0, sticky="ew",
                             padx=16, pady=(0, 8))
        self.frac_outer.columnconfigure(0, weight=1)

        # ── Кнопки ──
        self._sep(left, 13)
        btn_frame = tk.Frame(left, bg=SURFACE)
        btn_frame.grid(row=14, column=0, sticky="ew", padx=16, pady=8)
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        ttk.Button(btn_frame, text="⏱ Лічильник",
                   command=self._open_counter).grid(row=0, column=0,
                                                    padx=(0,4), sticky="ew")
        ttk.Button(btn_frame, text="⚖ Порівняти",
                   command=self._open_compare).grid(row=0, column=1,
                                                    padx=(4,0), sticky="ew")

    def _sep(self, parent, row):
        tk.Frame(parent, bg=BORDER, height=1).grid(
            row=row, column=0, sticky="ew")

    # ══ RIGHT PANEL ═════════════════════════════════════════════════
    def _build_right_panel(self):
        right = tk.Frame(self, bg=BG)
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        self.nb = ttk.Notebook(right)
        self.nb.grid(row=0, column=0, sticky="ew")
        self.nb.bind("<<NotebookTabChanged>>", self._on_tab_change)

        self.tab_line    = ttk.Frame(self.nb)
        self.tab_grid    = ttk.Frame(self.nb)
        self.tab_pie     = ttk.Frame(self.nb)
        self.tab_place   = ttk.Frame(self.nb)

        self.nb.add(self.tab_line,  text="📏  Числова пряма")
        self.nb.add(self.tab_grid,  text="🟦  Сітка-100")
        self.nb.add(self.tab_pie,   text="🥧  Торт / Дроби")
        self.nb.add(self.tab_place, text="🔢  Розряди")

        # Matplotlib canvas
        self.fig = plt.figure(figsize=(12, 7), facecolor=SURFACE)
        self.mpl_canvas = FigureCanvasTkAgg(self.fig, master=right)
        widget = self.mpl_canvas.get_tk_widget()
        widget.configure(bg=SURFACE, highlightthickness=0)
        widget.grid(row=1, column=0, sticky="nsew")

        # Scroll zoom
        widget.bind("<MouseWheel>",      self._on_mousewheel)
        widget.bind("<Button-4>",        self._on_mousewheel)  # Linux
        widget.bind("<Button-5>",        self._on_mousewheel)  # Linux
        widget.bind("<ButtonPress-1>",   self._on_drag_start)
        widget.bind("<B1-Motion>",       self._on_drag_move)
        widget.bind("<ButtonRelease-1>", self._on_drag_end)

    # ─── СЛАЙДЕРИ (динамічна кількість) ────────────────────────────
    PLACE_LABELS = ["Ціла частина", "Десяті (0.1)", "Соті (0.01)",
                    "Тисячні (0.001)", "Десятитисячні (0.0001)",
                    "Стотисячні (0.00001)"]
    PLACE_COLORS = [TEXT, ACCENT, ACCENT2, ACCENT4, ACCENT5, ACCENT6]

    def _set_places(self, n, init=False):
        self.dec_places = n
        for i, b in enumerate(self.place_btns):
            if i == n - 1:
                b.config(bg=ACCENT, fg="white")
            else:
                b.config(bg=SURFACE2, fg=TEXT_DIM)
        if not init:
            self._rebuild_sliders()
            self._rebuild_cards()
            self._update_all()

    def _rebuild_sliders(self):
        for w in self.sliders_frame.winfo_children():
            w.destroy()
        self.sl_vars = []
        for i in range(self.dec_places + 1):
            var = tk.IntVar(value=self.state1.digits[i])
            lbl_text = self.PLACE_LABELS[i]
            color = self.PLACE_COLORS[i]

            tk.Label(self.sliders_frame, text=lbl_text, bg=SURFACE,
                     fg=TEXT_DIM, font=self.fn_small
                     ).grid(row=i*2, column=0, columnspan=3,
                            sticky="w", pady=(6 if i == 0 else 2, 0))

            sl = tk.Scale(self.sliders_frame, from_=0, to=9,
                          variable=var, orient="horizontal",
                          showvalue=False, bg=SURFACE,
                          troughcolor=SURFACE2, highlightthickness=0,
                          activebackground=color, sliderrelief="flat",
                          command=lambda v, vi=i, vr=var:
                              (vr.set(int(float(v))), self._on_slider(vi, vr)))
            sl.grid(row=i*2+1, column=0, sticky="ew", pady=(0, 0))

            val_lbl = tk.Label(self.sliders_frame, textvariable=var,
                               bg=SURFACE, fg=color,
                               font=self.fn_mono, width=2)
            val_lbl.grid(row=i*2+1, column=1, padx=(6, 0))

            self.sliders_frame.columnconfigure(0, weight=1)
            self.sl_vars.append(var)

    def _on_slider(self, idx, var):
        self.state1.digits[idx] = var.get()
        self._update_all()

    # ─── КАРТКИ РОЗРЯДІВ ────────────────────────────────────────────
    def _rebuild_cards(self):
        for w in self.cards_outer.winfo_children():
            w.destroy()
        n = self.dec_places + 1
        self.pc_frames = []
        self.pc_val_lbl = []

        names = ["Цілі", "Дес.", "Соті", "Тис.", "Дес-тис.", "Сто-тис."]
        mults = ["×1", "×0.1", "×0.01", "×0.001", "×0.0001", "×0.00001"]

        for i in range(n):
            if i > 0:
                tk.Label(self.cards_outer, text="·", bg=SURFACE,
                         fg=TEXT_MID,
                         font=font.Font(family="Helvetica", size=14)
                         ).grid(row=0, column=i*2-1, padx=1)

            f = tk.Frame(self.cards_outer, bg=SURFACE2,
                         highlightbackground=BORDER, highlightthickness=1)
            f.grid(row=0, column=i*2, sticky="nsew")
            self.cards_outer.columnconfigure(i*2, weight=1)

            tk.Label(f, text=names[i], bg=SURFACE2, fg=TEXT_DIM,
                     font=self.fn_small, pady=2).pack()
            vl = tk.Label(f, text="0", bg=SURFACE2, fg=TEXT,
                          font=self.fn_card)
            vl.pack()
            tk.Label(f, text=mults[i], bg=SURFACE2, fg=TEXT_MID,
                     font=self.fn_small, pady=2).pack()
            self.pc_frames.append((f, self.PLACE_COLORS[i]))
            self.pc_val_lbl.append(vl)

    # ─── UPDATE ALL ─────────────────────────────────────────────────
    def _update_all(self, *_):
        s = self.state1
        val = s.get_value()

        # Sync slider vars → digits
        for i, var in enumerate(self.sl_vars):
            var.set(s.digits[i])

        # Display
        int_p = s.digits[0]
        dec_p = ''.join(str(s.digits[j]) for j in range(1, self.dec_places + 2))
        self.lbl_int.config(text=str(int_p))
        self.lbl_dec.config(text=dec_p)
        self.lbl_name.config(text=number_name_uk(f"{int_p}.{dec_p}"))

        frac_str = decimal_to_fraction_str(val)
        self.lbl_frac_eq.config(text=f"= {frac_str}")

        # Cards
        for i, (f, color) in enumerate(self.pc_frames):
            v = s.digits[i]
            active = v > 0
            f.config(highlightbackground=color if active else BORDER)
            self.pc_val_lbl[i].config(
                text=str(v),
                fg=self.PLACE_COLORS[i] if active else TEXT_MID)

        # Fractions list
        self._update_fractions(val)
        self._draw_active_tab()

    def _update_fractions(self, val):
        for w in self.frac_outer.winfo_children():
            w.destroy()
        if val == 0:
            tk.Label(self.frac_outer, text="0 = 0/1",
                     bg=SURFACE, fg=TEXT_DIM, font=self.fn_small).pack(anchor="w")
            return

        denominators = [10, 100, 1000, 10000, 4, 5, 8, 20, 25, 2, 3]
        seen = set()
        fracs = []
        for den in denominators:
            n_raw = round(val * den)
            if n_raw == 0:
                continue
            g = gcd(n_raw, den)
            n, d = n_raw // g, den // g
            if (n, d) not in seen and abs(n/d - val) < 1e-6:
                seen.add((n, d))
                fracs.append((n, d))

        for n, d in fracs[:5]:
            row = tk.Frame(self.frac_outer, bg=SURFACE2,
                           highlightbackground=BORDER, highlightthickness=1)
            row.pack(fill="x", pady=2)
            row.columnconfigure(1, weight=1)
            tk.Label(row, text=f"{n}/{d}", bg=SURFACE2, fg=ACCENT2,
                     font=self.fn_mono, width=9).grid(row=0, column=0,
                                                       padx=6, pady=4)
            bar_bg = tk.Frame(row, bg=SURFACE2, height=8)
            bar_bg.grid(row=0, column=1, sticky="ew", padx=(0, 6))
            pct = min(1.0, n/d)

            def draw_bar(event, bg=bar_bg, p=pct):
                for c in bg.winfo_children():
                    c.destroy()
                w2 = max(1, int(bg.winfo_width() * p))
                tk.Frame(bg, bg=ACCENT2, height=8, width=w2).place(x=0, y=0)
                tk.Frame(bg, bg=BORDER,  height=8,
                         width=bg.winfo_width()-w2).place(x=w2, y=0)

            bar_bg.bind("<Configure>", draw_bar)

    # ─── TAB DISPATCH ────────────────────────────────────────────────
    def _on_tab_change(self, event=None):
        self._draw_active_tab()

    def _draw_active_tab(self):
        tab = self.nb.index(self.nb.select())
        self.fig.clear()
        if tab == 0:
            self._draw_number_line()
        elif tab == 1:
            self._draw_grid()
        elif tab == 2:
            self._draw_pie()
        elif tab == 3:
            self._draw_place()
        self.mpl_canvas.draw_idle()

    # ═══════════════════════════════════════════════════════════════
    #  TAB 0 — ЧИСЛОВА ПРЯМА
    # ═══════════════════════════════════════════════════════════════
    def _draw_number_line(self):
        val = self.state1.get_value()
        if self.zoom_center is None:
            self.zoom_center = val

        half = self.zoom_range / 2
        start = max(0.0, self.zoom_center - half)
        end   = start + self.zoom_range

        ax = self.fig.add_subplot(111)
        ax.set_facecolor(BG)
        ax.set_xlim(start - self.zoom_range * 0.03,
                    end   + self.zoom_range * 0.06)
        ax.set_ylim(-1, 1)
        ax.axis('off')

        zoom_str = f"×{round(1/self.zoom_range, 1)}" if self.zoom_range < 1 else \
                   f"÷{round(self.zoom_range, 1)}" if self.zoom_range > 1 else "×1"

        ax.set_title(f"Числова пряма   [масштаб {zoom_str}]   "
                     f"Колесо миші = zoom · Перетягнення = прокрутка",
                     color=TEXT_DIM, fontsize=10, loc='left', pad=8)

        bar_y = 0.0
        # Arrow
        ax.annotate("", xy=(end + self.zoom_range*0.04, bar_y),
                    xytext=(max(0, start - self.zoom_range*0.01), bar_y),
                    arrowprops=dict(arrowstyle="->", color=TEXT_MID,
                                   lw=1.8, mutation_scale=14))

        # Auto-step
        rng = self.zoom_range
        if rng < 0.002:   step = 0.0001
        elif rng < 0.02:  step = 0.001
        elif rng < 0.2:   step = 0.01
        elif rng < 1.0:   step = 0.1
        elif rng < 2.0:   step = 0.2
        else:             step = 0.5

        t = round(math.ceil(start / step) * step, 8)
        while t <= end + step * 0.01:
            t = round(t, 8)
            if start - step * 0.1 <= t <= end + step * 0.1:
                is_whole = abs(t - round(t)) < 1e-7
                is_tenth = abs(t*10 - round(t*10)) < 1e-6
                is_hund  = abs(t*100 - round(t*100)) < 1e-5

                tick_h = (0.35 if is_whole else
                          0.22 if is_tenth else
                          0.13 if is_hund  else 0.08)
                col  = (TEXT if is_whole else
                        TEXT_DIM if is_tenth else
                        TEXT_MID)
                lw   = 2.0 if is_whole else 1.2 if is_tenth else 0.7

                ax.plot([t, t], [-tick_h, tick_h], color=col, lw=lw, zorder=3)

                show = (is_whole or
                        (rng <= 1.5 and is_tenth) or
                        (rng <= 0.15 and is_hund) or
                        (rng <= 0.015))
                if show:
                    decimals = (0 if is_whole else
                                1 if is_tenth else
                                2 if is_hund  else 4)
                    lbl = f"{t:.{decimals}f}"
                    ax.text(t, -tick_h - 0.13, lbl,
                            ha='center', va='top',
                            color=col,
                            fontsize=(10 if is_whole else
                                      8  if is_tenth else 7),
                            fontfamily='monospace')
            t = round(t + step, 8)

        # Value marker
        if start - self.zoom_range*0.05 <= val <= end + self.zoom_range*0.05:
            vx = val
            # Shade bar from nearest whole
            base = math.floor(val)
            shade_start = max(start, float(base))
            if shade_start < vx:
                ax.axvspan(shade_start, vx, ymin=0.44, ymax=0.56,
                           alpha=0.18, color=ACCENT, zorder=2)

            # Glow
            for r_, a_ in [(0.07, 0.07), (0.04, 0.13), (0.015, 0.22)]:
                ax.axvspan(vx - r_*rng, vx + r_*rng,
                           ymin=0.3, ymax=0.7, alpha=a_, color=ACCENT)

            ax.plot(vx, bar_y, 'o', color=ACCENT, markersize=13, zorder=5,
                    markeredgecolor="white", markeredgewidth=2)
            ax.text(vx, 0.52,
                    f"{val:.{self.dec_places+1}f}",
                    ha='center', va='bottom',
                    color=ACCENT, fontsize=14, fontweight='bold',
                    fontfamily='monospace')

        # Grid integers
        for i in range(int(start), int(end) + 2):
            if start <= i <= end:
                ax.axvline(i, color=GRID_CLR, lw=1, zorder=1)

        self.fig.tight_layout(pad=1.5)

    # ─── Scroll / drag ──────────────────────────────────────────────
    def _on_mousewheel(self, event):
        tab = self.nb.index(self.nb.select())
        if tab != 0:
            return
        val = self.state1.get_value()
        if self.zoom_center is None:
            self.zoom_center = val

        delta = 0
        if event.num == 4 or (hasattr(event, 'delta') and event.delta > 0):
            delta = -1
        elif event.num == 5 or (hasattr(event, 'delta') and event.delta < 0):
            delta = 1

        factor = 1.5
        if delta < 0:
            self.zoom_range = max(0.0001, self.zoom_range / factor)
        else:
            self.zoom_range = min(20.0, self.zoom_range * factor)

        self.fig.clear()
        self._draw_number_line()
        self.mpl_canvas.draw_idle()

    def _on_drag_start(self, event):
        if self.nb.index(self.nb.select()) != 0:
            return
        self._zoom_dragging = True
        self._drag_start_x = event.x
        self._drag_start_range = self.zoom_range
        self._drag_center_start = self.zoom_center if self.zoom_center else self.state1.get_value()

    def _on_drag_move(self, event):
        if not self._zoom_dragging:
            return
        if self.nb.index(self.nb.select()) != 0:
            return
        dx = event.x - self._drag_start_x
        canvas_w = self.mpl_canvas.get_tk_widget().winfo_width()
        shift = -(dx / canvas_w) * self._drag_start_range
        new_center = self._drag_center_start + shift
        self.zoom_center = max(self.zoom_range/2, new_center)
        self.fig.clear()
        self._draw_number_line()
        self.mpl_canvas.draw_idle()

    def _on_drag_end(self, event):
        self._zoom_dragging = False

    # ═══════════════════════════════════════════════════════════════
    #  TAB 1 — СІТКА 100
    # ═══════════════════════════════════════════════════════════════
    def _draw_grid(self):
        val  = self.state1.get_value()
        int_ = self.state1.digits[0]
        t    = self.state1.digits[1]
        h    = self.state1.digits[2]
        cents = t * 10 + h   # соті від дробової частини

        n_whole = int_
        gs = gridspec.GridSpec(1, n_whole + 2 if n_whole > 0 else 2,
                               figure=self.fig,
                               wspace=0.4, left=0.03, right=0.97,
                               top=0.88, bottom=0.10)

        self.fig.text(0.5, 0.96,
                      f"Число {val:.{self.dec_places+1}f} = "
                      f"{int_} {'ціла' if int_==1 else 'цілих'} і "
                      f"{cents}/100 від наступної",
                      ha='center', va='top', color=TEXT,
                      fontsize=13, fontweight='bold')

        col_idx = 0
        # Повні цілі
        for w in range(n_whole):
            ax = self.fig.add_subplot(gs[0, col_idx])
            col_idx += 1
            self._draw_100grid(ax, 100, 0, f"Ціла #{w+1}\n(100/100 = 1)")

        # Дробова частина
        ax2 = self.fig.add_subplot(gs[0, col_idx])
        col_idx += 1
        self._draw_100grid(ax2, cents, h,
                           f"Дробова частина\n{cents}/100 = {val - int_:.{self.dec_places+1}f}")

        # Смужка десятих
        ax3 = self.fig.add_subplot(gs[0, col_idx])
        ax3.set_facecolor(BG)
        ax3.set_xlim(-0.5, 1.5)
        ax3.set_ylim(-0.5, 10.5)
        ax3.axis('off')
        ax3.set_title(f"Десяті\n{t}/10", color=TEXT_DIM, fontsize=10, pad=6)

        for idx in range(10):
            r = 9 - idx
            color = ACCENT if idx < t else SURFACE2
            edgecolor = ACCENT if idx < t else BORDER
            rect = FancyBboxPatch((0.05, r + 0.08), 0.85, 0.78,
                                  boxstyle="round,pad=0.04",
                                  facecolor=color, edgecolor=edgecolor, lw=1.0)
            ax3.add_patch(rect)
            label_color = "white" if idx < t else TEXT_DIM
            ax3.text(0.5, r + 0.5, f"0.{idx+1 if idx < 9 else '0'}",
                     ha='center', va='center',
                     color=label_color, fontsize=8, fontfamily='monospace')

    def _draw_100grid(self, ax, filled_total, extra_hund, title):
        ax.set_facecolor(BG)
        ax.set_xlim(-0.5, 10.5)
        ax.set_ylim(-1.0, 10.5)
        ax.axis('off')
        ax.set_title(title, color=TEXT_DIM, fontsize=10, pad=6)

        full_rows = filled_total // 10
        extra     = filled_total % 10

        for idx in range(100):
            row = 9 - idx // 10
            col = idx % 10
            in_full = idx < full_rows * 10
            in_extra = (full_rows * 10 <= idx < filled_total)
            in_hund  = (idx < extra_hund) and (full_rows == 0)

            if filled_total == 100:
                color, alpha = ACCENT4, 0.85
            elif in_full:
                color, alpha = ACCENT, 0.80
            elif in_extra:
                color, alpha = ACCENT2, 0.85
            else:
                color, alpha = SURFACE2, 1.0
            edge = ACCENT if (in_full or (filled_total==100)) else \
                   ACCENT2 if in_extra else BORDER

            rect = FancyBboxPatch((col+0.04, row+0.04), 0.88, 0.88,
                                  boxstyle="round,pad=0.03",
                                  facecolor=color, edgecolor=edge,
                                  linewidth=0.7, alpha=alpha)
            ax.add_patch(rect)

        # Column numbers
        for c in range(10):
            ax.text(c+0.5, -0.5, str(c+1),
                    ha='center', va='center',
                    color=TEXT_MID, fontsize=6.5, fontfamily='monospace')

        legend = [mpatches.Patch(color=ACCENT,  label="Десяті"),
                  mpatches.Patch(color=ACCENT2, label="Соті"),
                  mpatches.Patch(facecolor=SURFACE2, edgecolor=BORDER, label="Пусто")]
        ax.legend(handles=legend, loc='lower center',
                  bbox_to_anchor=(0.5, -0.10), ncol=3,
                  facecolor=SURFACE, edgecolor=BORDER,
                  labelcolor=TEXT, fontsize=7, framealpha=0.9)

    # ═══════════════════════════════════════════════════════════════
    #  TAB 2 — ТОРТ / ДРОБИ
    # ═══════════════════════════════════════════════════════════════
    def _draw_pie(self):
        val = self.state1.get_value()
        int_ = self.state1.digits[0]
        frac_val = round(val - int_, 5)

        gs = gridspec.GridSpec(1, 3, figure=self.fig,
                               wspace=0.5, left=0.04, right=0.97,
                               top=0.88, bottom=0.12)

        # ── Ліво: Торт ──
        ax1 = self.fig.add_subplot(gs[0])
        ax1.set_facecolor(BG)
        ax1.set_aspect('equal')

        frac_str = decimal_to_fraction_str(frac_val)
        ax1.set_title(f"Дробова частина  {frac_val:.{self.dec_places+1}f}\n= {frac_str}",
                      color=TEXT, fontsize=12, pad=10)

        angle = frac_val * 360
        theta = np.linspace(0, 2*np.pi, 300)

        # Background circle
        ax1.fill(np.cos(theta), np.sin(theta), color=SURFACE2)
        ax1.plot(np.cos(theta), np.sin(theta), color=BORDER, lw=1.5)

        # Filled sector
        if angle > 0:
            t2 = np.linspace(np.pi/2, np.pi/2 - np.radians(angle), 300)
            xs = np.concatenate([[0], np.cos(t2), [0]])
            ys = np.concatenate([[0], np.sin(t2), [0]])
            ax1.fill(xs, ys, color=ACCENT, alpha=0.85)
            ax1.plot(np.cos(t2), np.sin(t2), color=ACCENT, lw=2)

        # Division lines (tenths)
        for i in range(10):
            ang = np.pi/2 - i * 2*np.pi/10
            ax1.plot([0, np.cos(ang)], [0, np.sin(ang)],
                     color=BORDER, lw=0.8, alpha=0.5)
            mid_ang = np.pi/2 - (i + 0.5) * 2*np.pi/10
            ax1.text(0.7*np.cos(mid_ang), 0.7*np.sin(mid_ang),
                     f"0.{i+1 if i<9 else '0'}" if i < 9 else "1.0",
                     ha='center', va='center',
                     color=TEXT_DIM, fontsize=7, fontfamily='monospace')

        ax1.set_xlim(-1.25, 1.25)
        ax1.set_ylim(-1.25, 1.25)
        ax1.axis('off')

        # ── Центр: Звичайний дріб → десятковий ──
        ax2 = self.fig.add_subplot(gs[1])
        ax2.set_facecolor(BG)
        ax2.axis('off')
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.set_title("Звичайний дріб ↔ Десятковий", color=TEXT, fontsize=12, pad=10)

        FAMOUS = [
            (1, 2,   0.5),
            (1, 4,   0.25),
            (3, 4,   0.75),
            (1, 5,   0.2),
            (1, 10,  0.1),
            (3, 10,  0.3),
            (1, 100, 0.01),
        ]
        row_h = 0.95 / (len(FAMOUS) + 1)
        ax2.text(0.5, 0.97, "Дріб → Десяткова", ha='center', va='top',
                 color=TEXT_DIM, fontsize=9)

        for ri, (n, d, dval) in enumerate(FAMOUS):
            y = 0.90 - ri * row_h
            is_match = abs(dval - frac_val) < 0.001
            color = ACCENT if is_match else TEXT_DIM
            weight = 'bold' if is_match else 'normal'
            ax2.text(0.18, y, f"{n}/{d}", ha='center', va='center',
                     color=color, fontsize=11, fontweight=weight,
                     fontfamily='monospace')
            ax2.text(0.38, y, "=", ha='center', va='center',
                     color=TEXT_MID, fontsize=11)
            ax2.text(0.62, y, f"{dval:.2f}", ha='center', va='center',
                     color=color, fontsize=11, fontweight=weight,
                     fontfamily='monospace')
            bar_w = dval * 0.35
            ax2.add_patch(Rectangle((0.63, y-0.025), 0.35, 0.05,
                                    facecolor=SURFACE2, edgecolor=BORDER, lw=0.5))
            ax2.add_patch(Rectangle((0.63, y-0.025), bar_w, 0.05,
                                    facecolor=color if is_match else ACCENT2,
                                    alpha=0.7))

        # ── Право: Якщо int_ > 0 — повні торти ──
        ax3 = self.fig.add_subplot(gs[2])
        ax3.set_facecolor(BG)
        ax3.axis('off')
        ax3.set_xlim(0, 1)
        ax3.set_ylim(0, 1)
        ax3.set_title(f"Загальний вигляд числа {val:.{self.dec_places+1}f}",
                      color=TEXT, fontsize=12, pad=10)

        total_pies = int_ + 1  # цілих + 1 неповний
        cols_p = 3
        rows_p = math.ceil(total_pies / cols_p)
        pw = 0.28
        ph = 0.28
        margin_x = (1.0 - cols_p * pw) / (cols_p + 1)
        margin_y = (1.0 - rows_p * ph) / (rows_p + 1)

        for pi in range(total_pies):
            r, c = divmod(pi, cols_p)
            cx = margin_x + c * (pw + margin_x) + pw/2
            cy = 0.92 - (r * (ph + margin_y) + ph/2)
            is_full = pi < int_
            fill = 1.0 if is_full else frac_val
            color = ACCENT4 if is_full else ACCENT

            theta = np.linspace(0, 2*np.pi, 100)
            xs_c = cx + pw/2 * np.cos(theta)
            ys_c = cy + ph/2 * np.sin(theta)
            ax3.fill(xs_c, ys_c, color=SURFACE2)
            ax3.plot(xs_c, ys_c, color=BORDER, lw=1)

            if fill > 0:
                t2 = np.linspace(np.pi/2, np.pi/2 - fill*2*np.pi, 100)
                xf = np.concatenate([[cx], cx + pw/2*np.cos(t2), [cx]])
                yf = np.concatenate([[cy], cy + ph/2*np.sin(t2), [cy]])
                ax3.fill(xf, yf, color=color, alpha=0.85)

            lbl = "1" if is_full else f"{frac_val:.2f}"
            ax3.text(cx, cy, lbl, ha='center', va='center',
                     color="white" if fill > 0.3 else TEXT_DIM,
                     fontsize=9, fontweight='bold')

    # ═══════════════════════════════════════════════════════════════
    #  TAB 3 — РОЗРЯДИ
    # ═══════════════════════════════════════════════════════════════
    def _draw_place(self):
        s = self.state1
        val = s.get_value()
        n = self.dec_places + 1   # кількість розрядів (разом з цілою)

        gs = gridspec.GridSpec(2, 1, figure=self.fig,
                               hspace=0.7, top=0.90, bottom=0.08,
                               left=0.03, right=0.97)

        # ── TOP: цифри ──
        ax1 = self.fig.add_subplot(gs[0])
        ax1.set_facecolor(BG)
        cols_count = n + (n - 1)   # цифри + крапки між ними
        ax1.set_xlim(0, cols_count)
        ax1.set_ylim(0, 1)
        ax1.axis('off')
        ax1.set_title("Кожна цифра — окремий розряд",
                      color=TEXT_DIM, fontsize=11, loc='left', pad=8)

        names = ["Одиниці", "Десяті", "Соті", "Тисячні",
                 "Дес-тис.", "Сто-тис."]
        mults = ["× 1", "× 0.1", "× 0.01", "× 0.001", "× 0.0001", "× 0.00001"]

        for i in range(n):
            xi = i * 2
            # крапка між цілою та дробовою
            if i == 1:
                ax1.text(xi - 0.5, 0.5, "·",
                         ha='center', va='center',
                         color=TEXT_DIM, fontsize=36, fontweight='bold')

            v = s.digits[i]
            color = self.PLACE_COLORS[i]
            active = v > 0

            bg = color + "22" if active else "#F1F5F9"
            edge = color if active else BORDER
            rect = FancyBboxPatch((xi + 0.05, 0.05), 0.85, 0.90,
                                  boxstyle="round,pad=0.04",
                                  facecolor=bg, edgecolor=edge,
                                  linewidth=2 if active else 1)
            ax1.add_patch(rect)
            ax1.text(xi + 0.5, 0.82, names[i],
                     ha='center', va='center',
                     color=color if active else TEXT_DIM, fontsize=8,
                     fontfamily='monospace')
            ax1.text(xi + 0.5, 0.50, str(v),
                     ha='center', va='center',
                     color=color if active else TEXT_MID,
                     fontsize=28, fontweight='bold', fontfamily='monospace')
            ax1.text(xi + 0.5, 0.16, mults[i],
                     ha='center', va='center',
                     color=TEXT_DIM, fontsize=7.5, fontfamily='monospace')

        # ── BOTTOM: формула ──
        ax2 = self.fig.add_subplot(gs[1])
        ax2.set_facecolor(SURFACE)
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 1)
        ax2.axis('off')
        ax2.set_title("Розклад числа", color=TEXT_DIM, fontsize=11,
                      loc='left', pad=8)

        parts = []
        mult_vals = [1, 0.1, 0.01, 0.001, 0.0001, 0.00001]
        for i in range(n):
            v = s.digits[i]
            if v > 0:
                result = v * mult_vals[i]
                txt = f"{v} × {mult_vals[i]} = {result:.{max(i,1)}f}"
                parts.append((txt, self.PLACE_COLORS[i]))
        if not parts:
            parts = [("0 × 1 = 0", TEXT_MID)]

        gap = 10 / (len(parts) + 1)
        for pi, (txt, col) in enumerate(parts):
            xc = gap * (pi + 1)
            ax2.text(xc, 0.70, txt, ha='center', va='center',
                     color=col, fontsize=11, fontfamily='monospace',
                     fontweight='bold')
            if pi < len(parts) - 1:
                ax2.text(xc + gap*0.5, 0.70, "+",
                         ha='center', va='center',
                         color=TEXT_DIM, fontsize=14)

        ax2.text(5, 0.25,
                 f"= {val:.{self.dec_places+1}f}   "
                 f"({number_name_uk(str(round(val, self.dec_places+1)))})",
                 ha='center', va='center', color=ACCENT,
                 fontsize=15, fontweight='bold', fontfamily='monospace')

        # Таблиця розрядів
        table_data = [names[:n], [str(s.digits[i]) for i in range(n)]]
        table = ax1.table(cellText=[table_data[1]],
                          colLabels=table_data[0],
                          loc='bottom', bbox=[0.0, -0.55, 1.0, 0.45])
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        for (r, c), cell in table.get_celld().items():
            cell.set_facecolor(SURFACE if r == 0 else BG)
            cell.set_edgecolor(BORDER)
            cell.set_text_props(color=self.PLACE_COLORS[c] if r == 1 else TEXT_DIM,
                                fontfamily='monospace', fontweight='bold')

    # ═══════════════════════════════════════════════════════════════
    #  ВІКНО ПОРІВНЯННЯ
    # ═══════════════════════════════════════════════════════════════
    def _open_compare(self):
        CompareWindow(self)

    # ═══════════════════════════════════════════════════════════════
    #  ВІКНО ЛІЧИЛЬНИКА
    # ═══════════════════════════════════════════════════════════════
    def _open_counter(self):
        CounterWindow(self)


# ════════════════════════════════════════════════════════════════════
#  ВІКНО ПОРІВНЯННЯ ДВОХ ЧИСЕЛ
# ════════════════════════════════════════════════════════════════════
class CompareWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Порівняння двох чисел")
        self.configure(bg=BG)
        self.geometry("1000x620")

        self.state_a = NumberState([0, 3, 0, 0, 0, 0])
        self.state_b = NumberState([0, 7, 5, 0, 0, 0])
        self.dec_places = 2
        self.zoom_range = 1.0
        self.zoom_center = 0.5

        self._build()
        self._update()

    def _build(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)

        # ── Number A ──
        fa = tk.LabelFrame(self, text=" Число A ", bg=SURFACE,
                           fg=ACCENT3, font=("Helvetica", 12, "bold"),
                           highlightbackground=BORDER)
        fa.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.vars_a, self.disp_a = self._make_num_panel(fa, self.state_a, ACCENT3)

        # ── Number B ──
        fb = tk.LabelFrame(self, text=" Число B ", bg=SURFACE,
                           fg=ACCENT4, font=("Helvetica", 12, "bold"),
                           highlightbackground=BORDER)
        fb.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        self.vars_b, self.disp_b = self._make_num_panel(fb, self.state_b, ACCENT4)

        # ── Result ──
        fc = tk.Frame(self, bg=BG)
        fc.grid(row=0, column=1, padx=10, pady=10)
        self.lbl_result = tk.Label(fc, text="", bg=BG, fg=TEXT,
                                   font=font.Font(family="Courier", size=20, weight="bold"))
        self.lbl_result.pack()
        self.lbl_diff = tk.Label(fc, text="", bg=BG, fg=TEXT_DIM,
                                 font=font.Font(family="Helvetica", size=11))
        self.lbl_diff.pack(pady=4)

        # ── Canvas ──
        fig_frame = tk.Frame(self, bg=BG)
        fig_frame.grid(row=1, column=0, columnspan=3, sticky="nsew",
                       padx=10, pady=(0, 10))
        fig_frame.rowconfigure(0, weight=1)
        fig_frame.columnconfigure(0, weight=1)

        self.fig = plt.figure(figsize=(10, 5), facecolor=SURFACE)
        self.canvas = FigureCanvasTkAgg(self.fig, master=fig_frame)
        self.canvas.get_tk_widget().configure(bg=SURFACE, highlightthickness=0)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.canvas.get_tk_widget().bind("<MouseWheel>", self._scroll)
        self.canvas.get_tk_widget().bind("<Button-4>",   self._scroll)
        self.canvas.get_tk_widget().bind("<Button-5>",   self._scroll)

    def _make_num_panel(self, parent, state, color):
        parent.columnconfigure(0, weight=1)
        PLACE_LABELS = ["Ціла", "Десяті", "Соті", "Тисячні", "Дес-тис."]
        disp_var = tk.StringVar(value="0.00")
        tk.Label(parent, textvariable=disp_var, bg=SURFACE, fg=color,
                 font=font.Font(family="Courier", size=28, weight="bold")
                 ).grid(row=0, column=0, columnspan=2, pady=6)

        vars_ = []
        for i in range(self.dec_places + 1):
            v = tk.IntVar(value=state.digits[i])
            tk.Label(parent, text=PLACE_LABELS[i], bg=SURFACE,
                     fg=TEXT_DIM, font=("Helvetica", 9)
                     ).grid(row=i*2+1, column=0, columnspan=2, sticky="w", padx=8)
            sl = tk.Scale(parent, from_=0, to=9, variable=v,
                          orient="horizontal", showvalue=True,
                          bg=SURFACE, troughcolor=SURFACE2,
                          highlightthickness=0, activebackground=color,
                          sliderrelief="flat",
                          command=lambda val, vi=i, vr=v, st=state:
                              (st.__setattr__('digits',
                                  [st.digits[j] if j != vi else int(float(val))
                                   for j in range(6)]),
                               self._update()))
            sl.grid(row=i*2+2, column=0, columnspan=2, sticky="ew", padx=8)
            vars_.append(v)
        return vars_, disp_var

    def _update(self):
        va = self.state_a.get_value()
        vb = self.state_b.get_value()
        self.disp_a.set(f"{va:.{self.dec_places+1}f}")
        self.disp_b.set(f"{vb:.{self.dec_places+1}f}")

        if va < vb:
            sym, txt = "<", f"{va:.4f}  <  {vb:.4f}"
            diff_txt = f"Різниця: {vb-va:.4f}  (B більше на {vb-va:.4f})"
        elif va > vb:
            sym, txt = ">", f"{va:.4f}  >  {vb:.4f}"
            diff_txt = f"Різниця: {va-vb:.4f}  (A більше на {va-vb:.4f})"
        else:
            sym, txt = "=", f"{va:.4f}  =  {vb:.4f}"
            diff_txt = "Числа рівні"

        self.lbl_result.config(text=sym, fg=(ACCENT3 if sym==">" else
                                              ACCENT4 if sym=="<" else ACCENT5))
        self.lbl_diff.config(text=diff_txt)

        self.zoom_center = (va + vb) / 2
        rng = max(abs(vb - va) * 2.5, 0.5)
        self.zoom_range = min(rng, 5.0)

        self._draw()

    def _scroll(self, event):
        if event.num == 4 or (hasattr(event, 'delta') and event.delta > 0):
            self.zoom_range = max(0.01, self.zoom_range / 1.5)
        else:
            self.zoom_range = min(10.0, self.zoom_range * 1.5)
        self._draw()

    def _draw(self):
        va = self.state_a.get_value()
        vb = self.state_b.get_value()
        self.fig.clear()

        gs = gridspec.GridSpec(2, 1, figure=self.fig,
                               hspace=0.6, top=0.88, bottom=0.10,
                               left=0.05, right=0.96)

        # ── Числова пряма ──
        ax = self.fig.add_subplot(gs[0])
        ax.set_facecolor(BG)
        ax.axis('off')

        half = self.zoom_range / 2
        start = max(0.0, self.zoom_center - half)
        end   = start + self.zoom_range

        ax.set_xlim(start - self.zoom_range*0.04,
                    end   + self.zoom_range*0.06)
        ax.set_ylim(-1, 1)
        ax.set_title("Числова пряма — порівняння A і B",
                     color=TEXT_DIM, fontsize=11, loc='left', pad=8)

        # Arrow
        ax.annotate("", xy=(end + self.zoom_range*0.04, 0),
                    xytext=(max(0, start - 0.01), 0),
                    arrowprops=dict(arrowstyle="->", color=TEXT_MID,
                                   lw=1.8, mutation_scale=14))

        rng = self.zoom_range
        step = (0.001 if rng < 0.02 else 0.01 if rng < 0.2 else
                0.1   if rng < 1.0  else 0.2  if rng < 2.0 else 0.5)

        t = round(math.ceil(start / step) * step, 8)
        while t <= end + step*0.01:
            t = round(t, 8)
            if start <= t <= end:
                is_whole = abs(t - round(t)) < 1e-7
                is_tenth = abs(t*10 - round(t*10)) < 1e-5
                h = 0.3 if is_whole else 0.18 if is_tenth else 0.1
                col = TEXT if is_whole else TEXT_DIM if is_tenth else TEXT_MID
                ax.plot([t, t], [-h, h], color=col,
                        lw=1.8 if is_whole else 1.0)
                if is_whole or (rng <= 1.5 and is_tenth):
                    dec = 0 if is_whole else 1 if is_tenth else 2
                    ax.text(t, -h-0.12, f"{t:.{dec}f}",
                            ha='center', va='top',
                            color=col, fontsize=9 if is_whole else 7,
                            fontfamily='monospace')
            t = round(t + step, 8)

        # A and B markers
        for v, col, label, y_off in [(va, ACCENT3, "A", 0.5),
                                      (vb, ACCENT4, "B", -0.5)]:
            if start - rng*0.05 <= v <= end + rng*0.05:
                ax.plot(v, 0, 'o', color=col, markersize=12, zorder=5,
                        markeredgecolor="white", markeredgewidth=2)
                ax.text(v, y_off, f"{label} = {v:.{self.dec_places+1}f}",
                        ha='center', va='center',
                        color=col, fontsize=11, fontweight='bold',
                        fontfamily='monospace')
                ax.plot([v, v], [0, y_off*0.7], color=col,
                        lw=1, linestyle='--', alpha=0.5)

        # Bracket between A and B
        if abs(va - vb) > 0.0001:
            lo, hi = min(va, vb), max(va, vb)
            if start <= lo and hi <= end:
                ax.annotate("", xy=(hi, -0.15), xytext=(lo, -0.15),
                            arrowprops=dict(arrowstyle="<->", color=ACCENT5,
                                           lw=1.5))
                mid = (lo + hi) / 2
                ax.text(mid, -0.32, f"різниця {abs(vb-va):.4f}",
                        ha='center', va='top',
                        color=ACCENT5, fontsize=8, fontfamily='monospace')

        # ── Bar comparison ──
        ax2 = self.fig.add_subplot(gs[1])
        ax2.set_facecolor(BG)
        ax2.axis('off')
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.set_title("Порівняння розмірів", color=TEXT_DIM, fontsize=11,
                      loc='left', pad=8)

        max_v = max(va, vb, 0.001)
        for yi, (v, col, label) in enumerate([(va, ACCENT3, "A"),
                                               (vb, ACCENT4, "B")]):
            y = 0.75 - yi * 0.42
            ax2.text(0.03, y, label, ha='center', va='center',
                     color=col, fontsize=14, fontweight='bold')
            bar_len = 0.80 * v / max_v
            ax2.add_patch(Rectangle((0.08, y-0.10), 0.80, 0.20,
                                    facecolor=SURFACE2, edgecolor=BORDER, lw=0.8))
            ax2.add_patch(Rectangle((0.08, y-0.10), bar_len, 0.20,
                                    facecolor=col, alpha=0.80))
            ax2.text(0.09 + bar_len, y, f"  {v:.{self.dec_places+1}f}",
                     ha='left', va='center',
                     color=col, fontsize=12, fontweight='bold',
                     fontfamily='monospace')

        self.canvas.draw_idle()


# ════════════════════════════════════════════════════════════════════
#  ВІКНО ЛІЧИЛЬНИКА
# ════════════════════════════════════════════════════════════════════
class CounterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Лічильник десяткових дробей")
        self.configure(bg=BG)
        self.geometry("860x620")

        self.value = 0.0
        self.step_var   = tk.StringVar(value="0.1")
        self.history    = [0.0]
        self.max_hist   = 30

        self._build()
        self._draw()

    def _build(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # ── Controls ──
        ctrl = tk.Frame(self, bg=SURFACE,
                        highlightbackground=BORDER, highlightthickness=1)
        ctrl.grid(row=0, column=0, sticky="ew", padx=10, pady=8)

        # Big display
        disp = tk.Frame(ctrl, bg=SURFACE)
        disp.pack(side="left", padx=20, pady=8)
        self.lbl_val = tk.Label(disp, text="0.0",
                                bg=SURFACE, fg=ACCENT,
                                font=font.Font(family="Courier",
                                              size=52, weight="bold"))
        self.lbl_val.pack()
        self.lbl_name = tk.Label(disp, text="нуль", bg=SURFACE,
                                 fg=TEXT_DIM,
                                 font=font.Font(family="Helvetica",
                                               size=11, slant="italic"))
        self.lbl_name.pack()

        # Step controls
        step_frame = tk.Frame(ctrl, bg=SURFACE)
        step_frame.pack(side="left", padx=20)
        tk.Label(step_frame, text="Крок:", bg=SURFACE, fg=TEXT_DIM,
                 font=("Helvetica", 12)).pack()

        STEPS = ["0.001", "0.01", "0.1", "1", "0.25", "0.5"]
        self.step_btns = {}
        for s in STEPS:
            b = tk.Button(step_frame, text=s, bg=SURFACE2, fg=TEXT_DIM,
                          font=("Courier", 11), relief="flat",
                          cursor="hand2", width=6,
                          command=lambda sv=s: self._set_step(sv))
            b.pack(side="left", padx=2)
            self.step_btns[s] = b

        tk.Label(step_frame, text="або введи:", bg=SURFACE,
                 fg=TEXT_DIM, font=("Helvetica", 10)).pack(side="left", padx=(8,2))
        tk.Entry(step_frame, textvariable=self.step_var, width=8,
                 font=("Courier", 12), bg=SURFACE2,
                 relief="flat", bd=4).pack(side="left")

        # Buttons
        btn_frame = tk.Frame(ctrl, bg=SURFACE)
        btn_frame.pack(side="left", padx=20)

        tk.Button(btn_frame, text="＋", bg=ACCENT, fg="white",
                  font=font.Font(family="Helvetica", size=24, weight="bold"),
                  relief="flat", width=3, cursor="hand2",
                  command=self._add).pack(pady=4)
        tk.Button(btn_frame, text="－", bg=ACCENT3, fg="white",
                  font=font.Font(family="Helvetica", size=24, weight="bold"),
                  relief="flat", width=3, cursor="hand2",
                  command=self._sub).pack(pady=4)

        # Reset
        reset_frame = tk.Frame(ctrl, bg=SURFACE)
        reset_frame.pack(side="left", padx=10)
        tk.Button(reset_frame, text="Скинути\nдо 0",
                  bg=SURFACE2, fg=TEXT_DIM,
                  font=("Helvetica", 10), relief="flat",
                  cursor="hand2", command=self._reset).pack()
        tk.Button(reset_frame, text="Задати\nзначення",
                  bg=SURFACE2, fg=TEXT_DIM,
                  font=("Helvetica", 10), relief="flat",
                  cursor="hand2", command=self._set_val).pack(pady=4)

        self.lbl_overflow = tk.Label(ctrl, text="", bg=SURFACE,
                                     fg=ACCENT4,
                                     font=font.Font(family="Helvetica",
                                                   size=13, weight="bold"))
        self.lbl_overflow.pack(side="left", padx=10)

        # Canvas
        fig_frame = tk.Frame(self, bg=BG)
        fig_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))
        fig_frame.rowconfigure(0, weight=1)
        fig_frame.columnconfigure(0, weight=1)

        self.fig = plt.figure(figsize=(9, 5), facecolor=SURFACE)
        self.canvas = FigureCanvasTkAgg(self.fig, master=fig_frame)
        self.canvas.get_tk_widget().configure(bg=SURFACE, highlightthickness=0)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self._set_step("0.1")

    def _set_step(self, s):
        self.step_var.set(s)
        for sv, b in self.step_btns.items():
            b.config(bg=ACCENT if sv == s else SURFACE2,
                     fg="white" if sv == s else TEXT_DIM)

    def _get_step(self):
        try:
            return float(self.step_var.get())
        except ValueError:
            return 0.1

    def _add(self):
        prev = round(self.value, 5)
        self.value = round(self.value + self._get_step(), 5)
        self._check_overflow(prev)
        self._push_history()
        self._update_display()
        self._draw()

    def _sub(self):
        prev = round(self.value, 5)
        self.value = max(0.0, round(self.value - self._get_step(), 5))
        self._push_history()
        self._update_display()
        self._draw()

    def _reset(self):
        self.value = 0.0
        self.history = [0.0]
        self.lbl_overflow.config(text="")
        self._update_display()
        self._draw()

    def _set_val(self):
        win = tk.Toplevel(self)
        win.title("Задати значення")
        win.configure(bg=BG)
        win.geometry("280x120")
        var = tk.StringVar(value=str(self.value))
        tk.Label(win, text="Введи нове значення:", bg=BG, fg=TEXT,
                 font=("Helvetica", 11)).pack(pady=8)
        tk.Entry(win, textvariable=var, font=("Courier", 14),
                 bg=SURFACE, relief="flat", bd=4, width=14).pack()
        def ok():
            try:
                self.value = round(float(var.get()), 5)
                self.history.append(self.value)
                self._update_display()
                self._draw()
                win.destroy()
            except ValueError:
                pass
        tk.Button(win, text="OK", bg=ACCENT, fg="white",
                  font=("Helvetica", 11), relief="flat",
                  command=ok).pack(pady=8)

    def _check_overflow(self, prev):
        prev_int = int(prev)
        new_int  = int(self.value)
        if new_int > prev_int:
            self.lbl_overflow.config(
                text=f"↑ Переповнення! {prev:.4f} + {self._get_step()} → {self.value:.4f}  "
                     f"(нова ціла!)")
            self.after(2500, lambda: self.lbl_overflow.config(text=""))
        else:
            self.lbl_overflow.config(text="")

    def _push_history(self):
        self.history.append(round(self.value, 5))
        if len(self.history) > self.max_hist:
            self.history = self.history[-self.max_hist:]

    def _update_display(self):
        v = self.value
        self.lbl_val.config(text=f"{v:.4f}".rstrip('0').rstrip('.') or "0")
        self.lbl_name.config(text=number_name_uk(f"{v:.4f}"))

    def _draw(self):
        v = self.value
        self.fig.clear()

        gs = gridspec.GridSpec(1, 3, figure=self.fig,
                               wspace=0.45, left=0.05, right=0.97,
                               top=0.88, bottom=0.12)

        # ── Ліво: «Вода у склянці» ──
        ax1 = self.fig.add_subplot(gs[0])
        ax1.set_facecolor(BG)
        ax1.set_xlim(-0.1, 1.1)

        # Цілих "склянок" + поточна
        int_part  = int(v)
        frac_part = v - int_part
        total_cups = max(int_part + 1, 1)
        ax1.set_ylim(-0.5, total_cups + 0.2)
        ax1.axis('off')
        ax1.set_title("Склянки (ціла = 1 повна)", color=TEXT_DIM,
                      fontsize=11, pad=8)

        for ci in range(int_part):
            y0 = ci
            ax1.add_patch(Rectangle((0.1, y0+0.05), 0.8, 0.85,
                                    facecolor=ACCENT2, alpha=0.7,
                                    edgecolor=ACCENT, lw=1.5))
            ax1.add_patch(Rectangle((0.05, y0), 0.90, 0.95,
                                    facecolor='none',
                                    edgecolor=TEXT_DIM, lw=2))
            ax1.text(0.5, y0+0.475, "1.0",
                     ha='center', va='center',
                     color="white", fontsize=13, fontweight='bold',
                     fontfamily='monospace')

        # Поточна (неповна)
        y0 = int_part
        fill_h = frac_part * 0.85
        ax1.add_patch(Rectangle((0.05, y0), 0.90, 0.95,
                                facecolor='none',
                                edgecolor=TEXT_DIM, lw=2))
        if fill_h > 0:
            ax1.add_patch(Rectangle((0.10, y0+0.05), 0.80, fill_h,
                                    facecolor=ACCENT, alpha=0.75))
        ax1.text(0.5, y0+0.5, f"{frac_part:.3f}",
                 ha='center', va='center',
                 color=ACCENT if frac_part > 0.3 else TEXT_DIM,
                 fontsize=12, fontweight='bold', fontfamily='monospace')

        # ── Центр: Числова пряма ──
        ax2 = self.fig.add_subplot(gs[1])
        ax2.set_facecolor(BG)
        ax2.axis('off')

        # Визначаємо діапазон
        lo = max(0, math.floor(v) - 0.2)
        hi = max(lo + 1.5, v + 0.5)
        ax2.set_xlim(lo - 0.05, hi + 0.08)
        ax2.set_ylim(-1, 1)
        ax2.set_title("Положення на прямій", color=TEXT_DIM,
                      fontsize=11, pad=8)

        ax2.annotate("", xy=(hi+0.06, 0), xytext=(lo, 0),
                     arrowprops=dict(arrowstyle="->", color=TEXT_MID,
                                     lw=1.5, mutation_scale=12))

        rng2 = hi - lo
        step2 = 0.1 if rng2 <= 2 else 0.5
        t = round(math.ceil(lo / step2) * step2, 5)
        while t <= hi:
            t = round(t, 5)
            is_whole = abs(t - round(t)) < 1e-6
            h2 = 0.30 if is_whole else 0.15
            col2 = TEXT if is_whole else TEXT_DIM
            ax2.plot([t, t], [-h2, h2], color=col2,
                     lw=1.8 if is_whole else 0.9)
            ax2.text(t, -h2-0.12, f"{t:.{0 if is_whole else 1}f}",
                     ha='center', va='top', color=col2,
                     fontsize=9 if is_whole else 7, fontfamily='monospace')
            t = round(t + step2, 5)

        ax2.plot(v, 0, 'o', color=ACCENT, markersize=13, zorder=5,
                 markeredgecolor="white", markeredgewidth=2)
        ax2.text(v, 0.45, f"{v:.4f}",
                 ha='center', va='bottom', color=ACCENT,
                 fontsize=12, fontweight='bold', fontfamily='monospace')

        # ── Право: Історія ──
        ax3 = self.fig.add_subplot(gs[2])
        ax3.set_facecolor(BG)
        ax3.set_title("Історія змін", color=TEXT_DIM, fontsize=11, pad=8)

        h_arr = self.history[-20:]
        if len(h_arr) > 1:
            xs = list(range(len(h_arr)))
            ax3.plot(xs, h_arr, color=ACCENT, lw=2, marker='o',
                     markersize=5, markerfacecolor=ACCENT2,
                     markeredgecolor="white", markeredgewidth=1)
            # Highlight integer crossings
            for i in range(1, len(h_arr)):
                if int(h_arr[i]) != int(h_arr[i-1]):
                    ax3.axvline(i, color=ACCENT4, lw=1.5,
                                linestyle='--', alpha=0.7)
                    ax3.text(i, (h_arr[i]+h_arr[i-1])/2,
                             " ціла!", color=ACCENT4, fontsize=7,
                             va='center')
            ax3.fill_between(xs, h_arr, alpha=0.12, color=ACCENT)
        else:
            ax3.plot([0], h_arr, 'o', color=ACCENT, markersize=8)

        ax3.set_xlabel("Кроки", color=TEXT_DIM, fontsize=9)
        ax3.set_ylabel("Значення", color=TEXT_DIM, fontsize=9)
        ax3.tick_params(colors=TEXT_DIM, labelsize=8)
        ax3.spines['bottom'].set_color(BORDER)
        ax3.spines['left'].set_color(BORDER)
        ax3.set_facecolor(BG)

        self.canvas.draw_idle()


# ════════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    plt.rcParams.update(PLT_PARAMS)
    app = DecimalVisualizerApp()
    app.mainloop()