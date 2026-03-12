"""
Інтерактивний тренажер: Десяткові дроби
Запуск: python decimal_visualizer.py
Потрібні бібліотеки: pip install matplotlib
"""

import tkinter as tk
from tkinter import ttk, font
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyBboxPatch, Rectangle
import matplotlib.patches as mpatches
import numpy as np
import math


# ─── КОЛЬОРИ ────────────────────────────────────────────────────────
BG         = "#0d0f14"
SURFACE    = "#161922"
SURFACE2   = "#1e2330"
BORDER     = "#2a3045"
ACCENT     = "#f0c040"
ACCENT2    = "#4fc3f7"
ACCENT3    = "#ef5350"
ACCENT4    = "#66bb6a"
ACCENT5    = "#ce93d8"
TEXT       = "#e8eaf0"
TEXT_DIM   = "#6b7590"


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def to_fraction(decimal_val, max_den=1000):
    """Перетворює десяткову дріб на звичайну (чисельник, знаменник)."""
    cents = round(decimal_val * 100)
    den = 100
    g = gcd(abs(cents), den)
    return cents // g, den // g


def number_name(int_part, tenths, hundredths):
    """Назва числа українською."""
    int_words = ['нуль','одна','дві','три','чотири',
                 'п\'ять','шість','сім','вісім','дев\'ять']
    result = []
    if int_part > 0:
        s = int_words[int_part] + (' ціла' if int_part == 1 else ' цілих')
        result.append(s)
    dec = tenths * 10 + hundredths
    if dec > 0:
        if hundredths == 0:
            s = int_words[tenths] + (' десята' if tenths == 1 else ' десятих')
        elif tenths == 0:
            s = int_words[hundredths] + (' сота' if hundredths == 1 else ' сотих')
        else:
            s = str(dec) + (' сота' if dec == 1 else ' сотих')
        result.append(s)
    return ' '.join(result) if result else 'нуль'


class DecimalVisualizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Десяткові дроби — інтерактивний тренажер")
        self.configure(bg=BG)
        try:
            self.state('zoomed')
        except tk.TclError:
            self.attributes('-zoomed', True)

        self.int_var    = tk.IntVar(value=0)
        self.tenth_var  = tk.IntVar(value=7)
        self.hund_var   = tk.IntVar(value=5)
        self.zoom_level = 1
        self.zoom_steps = [1, 2, 5, 10]
        self.active_tab = "line"

        self._setup_fonts()
        self._setup_styles()
        self._build_ui()
        self._update_all()

    # ─── FONTS & STYLES ────────────────────────────────────────────
    def _setup_fonts(self):
        self.fn_big    = font.Font(family="Courier", size=42, weight="bold")
        self.fn_title  = font.Font(family="Helvetica", size=14, weight="bold")
        self.fn_body   = font.Font(family="Helvetica", size=12)
        self.fn_small  = font.Font(family="Courier",   size=10)
        self.fn_mono   = font.Font(family="Courier",   size=12)
        self.fn_card   = font.Font(family="Courier",   size=18, weight="bold")
        self.fn_name   = font.Font(family="Helvetica", size=11, slant="italic")

    def _setup_styles(self):
        st = ttk.Style(self)
        st.theme_use("clam")

        for w, cfg in {
            "TFrame":    {"background": BG},
            "TLabel":    {"background": BG, "foreground": TEXT,
                          "font": ("Helvetica", 12)},
            "TNotebook": {"background": BG, "borderwidth": 0},
            "TNotebook.Tab": {
                "background": SURFACE2, "foreground": TEXT_DIM,
                "padding": [14, 8], "font": ("Helvetica", 11, "bold"),
                "borderwidth": 0,
            },
            "TScale":    {"background": BG, "troughcolor": BORDER,
                          "sliderrelief": "flat"},
        }.items():
            st.configure(w, **cfg)

        st.map("TNotebook.Tab",
               background=[("selected", SURFACE)],
               foreground=[("selected", ACCENT)])

    # ─── BUILD UI ──────────────────────────────────────────────────
    def _build_ui(self):
        self.columnconfigure(0, minsize=300)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ── LEFT PANEL ──────────────────────────────────────────────
        left = tk.Frame(self, bg=SURFACE, bd=0,
                        highlightbackground=BORDER, highlightthickness=1)
        left.grid(row=0, column=0, sticky="nsew")
        left.columnconfigure(0, weight=1)

        # Number display
        disp = tk.Frame(left, bg=SURFACE2)
        disp.grid(row=0, column=0, sticky="ew", pady=(0, 1))
        tk.Label(disp, text="ДЕСЯТКОВА ДРІБ", bg=SURFACE2,
                 fg=TEXT_DIM, font=self.fn_small,
                 padx=20, pady=10).pack(anchor="w")

        self.num_display_frame = tk.Frame(disp, bg=SURFACE2)
        self.num_display_frame.pack(pady=(4, 4), padx=20, anchor="w")

        self.lbl_int   = tk.Label(self.num_display_frame, text="0",
                                  bg=SURFACE2, fg=TEXT, font=self.fn_big)
        self.lbl_dot   = tk.Label(self.num_display_frame, text=".",
                                  bg=SURFACE2, fg=TEXT_DIM, font=self.fn_big)
        self.lbl_dec   = tk.Label(self.num_display_frame, text="75",
                                  bg=SURFACE2, fg=ACCENT, font=self.fn_big)
        for w in (self.lbl_int, self.lbl_dot, self.lbl_dec):
            w.pack(side="left")

        self.lbl_name = tk.Label(disp, text="", bg=SURFACE2, fg=TEXT_DIM,
                                 font=self.fn_name, pady=4)
        self.lbl_name.pack(anchor="w", padx=20)

        # Sliders
        sliders_frame = tk.Frame(left, bg=SURFACE)
        sliders_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        sliders_frame.columnconfigure(1, weight=1)

        self._make_slider(sliders_frame, "Ціла частина",  self.int_var,   0, 9,  0)
        self._make_slider(sliders_frame, "Десяті",        self.tenth_var, 0, 9,  1)
        self._make_slider(sliders_frame, "Соті",          self.hund_var,  0, 9,  2)

        # Place-value cards
        tk.Frame(left, bg=BORDER, height=1).grid(row=2, column=0, sticky="ew")
        cards_title = tk.Label(left, text="РОЗРЯДИ", bg=SURFACE,
                               fg=TEXT_DIM, font=self.fn_small, padx=20, pady=6)
        cards_title.grid(row=3, column=0, sticky="w")

        cards_frame = tk.Frame(left, bg=SURFACE)
        cards_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 10))
        for i in range(3):
            cards_frame.columnconfigure(i, weight=1)

        self.pc_frames = []
        self.pc_val_labels = []
        cards_data = [
            ("Цілі", "× 1", TEXT),
            ("Десяті", "× 0.1", ACCENT2),
            ("Соті", "× 0.01", ACCENT4),
        ]
        for i, (name, mult, color) in enumerate(cards_data):
            f = tk.Frame(cards_frame, bg=SURFACE2,
                         highlightbackground=BORDER, highlightthickness=1)
            f.grid(row=0, column=i, padx=(0 if i == 0 else 4, 0), sticky="ew")
            tk.Label(f, text=name, bg=SURFACE2, fg=TEXT_DIM,
                     font=self.fn_small, pady=4).pack()
            val_lbl = tk.Label(f, text="0", bg=SURFACE2, fg=TEXT,
                               font=self.fn_card)
            val_lbl.pack()
            tk.Label(f, text=mult, bg=SURFACE2, fg=TEXT_DIM,
                     font=self.fn_small, pady=4).pack()
            self.pc_frames.append((f, color))
            self.pc_val_labels.append(val_lbl)

        # Fraction equivalents
        tk.Frame(left, bg=BORDER, height=1).grid(row=5, column=0, sticky="ew")
        tk.Label(left, text="ЗВИЧАЙНІ ДРОБИ (еквіваленти)", bg=SURFACE,
                 fg=TEXT_DIM, font=self.fn_small, padx=20, pady=6).grid(row=6, column=0, sticky="w")

        self.frac_frame = tk.Frame(left, bg=SURFACE)
        self.frac_frame.grid(row=7, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.frac_frame.columnconfigure(0, weight=1)

        # ── RIGHT PANEL ─────────────────────────────────────────────
        right = tk.Frame(self, bg=BG)
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        # Tabs
        self.nb = ttk.Notebook(right)
        self.nb.grid(row=0, column=0, sticky="ew")

        self.tab_line    = ttk.Frame(self.nb, style="TFrame")
        self.tab_grid    = ttk.Frame(self.nb, style="TFrame")
        self.tab_compare = ttk.Frame(self.nb, style="TFrame")
        self.tab_place   = ttk.Frame(self.nb, style="TFrame")

        self.nb.add(self.tab_line,    text="📏  Числова пряма")
        self.nb.add(self.tab_grid,    text="🟦  Сітка-100")
        self.nb.add(self.tab_compare, text="⚖️  Порівняння")
        self.nb.add(self.tab_place,   text="🔢  Розряди")
        self.nb.bind("<<NotebookTabChanged>>", self._on_tab_change)

        # Matplotlib figure
        for tab in (self.tab_line, self.tab_grid, self.tab_compare, self.tab_place):
            tab.rowconfigure(0, weight=1)
            tab.columnconfigure(0, weight=1)

        self.fig = plt.figure(figsize=(12, 7), facecolor=BG)
        self.mpl_canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.mpl_canvas.get_tk_widget().configure(bg=BG, highlightthickness=0)
        self.mpl_canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

        # Zoom controls (shown for number line tab)
        self.zoom_frame = tk.Frame(right, bg=BG)
        self.zoom_frame.grid(row=0, column=0, sticky="e", padx=10)
        self.zoom_frame.lift()

        tk.Label(self.zoom_frame, text="Масштаб:", bg=BG,
                 fg=TEXT_DIM, font=self.fn_small).pack(side="left", padx=(0, 6))
        tk.Button(self.zoom_frame, text="−", bg=SURFACE2, fg=TEXT,
                  relief="flat", width=3, font=self.fn_body,
                  command=self._zoom_out, cursor="hand2").pack(side="left")
        self.zoom_lbl = tk.Label(self.zoom_frame, text="×1", bg=BG,
                                 fg=ACCENT, font=self.fn_mono, width=4)
        self.zoom_lbl.pack(side="left")
        tk.Button(self.zoom_frame, text="+", bg=SURFACE2, fg=TEXT,
                  relief="flat", width=3, font=self.fn_body,
                  command=self._zoom_in, cursor="hand2").pack(side="left")
        tk.Button(self.zoom_frame, text="↺", bg=SURFACE2, fg=TEXT_DIM,
                  relief="flat", width=3, font=self.fn_body,
                  command=self._zoom_reset, cursor="hand2").pack(side="left", padx=(4, 0))

    def _make_slider(self, parent, label, var, from_, to, row):
        tk.Label(parent, text=label, bg=SURFACE, fg=TEXT_DIM,
                 font=self.fn_small).grid(row=row*2, column=0, columnspan=3,
                                          sticky="w", pady=(10 if row == 0 else 4, 0))
        sl = ttk.Scale(parent, from_=from_, to=to, variable=var, orient="horizontal",
                       command=lambda v, vr=var: (vr.set(int(float(v))), self._update_all()))
        sl.grid(row=row*2+1, column=0, sticky="ew", pady=(2, 0))
        val_lbl = tk.Label(parent, textvariable=var, bg=SURFACE, fg=ACCENT,
                           font=self.fn_mono, width=3)
        val_lbl.grid(row=row*2+1, column=1, padx=(8, 0))

    # ─── VALUE HELPERS ─────────────────────────────────────────────
    def _get_value(self):
        return self.int_var.get() + self.tenth_var.get() * 0.1 + self.hund_var.get() * 0.01

    # ─── UPDATE ────────────────────────────────────────────────────
    def _update_all(self, *_):
        i = self.int_var.get()
        t = self.tenth_var.get()
        h = self.hund_var.get()

        self.lbl_int.config(text=str(i))
        self.lbl_dec.config(text=f"{t}{h}")
        self.lbl_name.config(text=number_name(i, t, h))

        # Place cards
        vals = [i, t, h]
        colors_active = [TEXT, ACCENT2, ACCENT4]
        for idx, (frame, color) in enumerate(self.pc_frames):
            v = vals[idx]
            is_active = v > 0
            frame.config(highlightbackground=color if is_active else BORDER)
            self.pc_val_labels[idx].config(
                text=str(v),
                fg=colors_active[idx] if is_active else TEXT_DIM
            )

        self._update_fractions()
        self._draw_active_tab()

    def _update_fractions(self):
        for w in self.frac_frame.winfo_children():
            w.destroy()

        val = self._get_value()
        if val == 0:
            tk.Label(self.frac_frame, text="0 = 0/1 = 0/10 = 0/100",
                     bg=SURFACE, fg=TEXT_DIM, font=self.fn_small).pack(anchor="w")
            return

        denominators = [10, 100, 4, 5, 8, 20, 25, 2, 3, 6]
        seen = set()
        fracs = []
        for den in denominators:
            n_raw = round(val * den)
            if n_raw == 0:
                continue
            g = gcd(n_raw, den)
            n, d = n_raw // g, den // g
            key = (n, d)
            if key not in seen and abs(n / d - val) < 0.0001:
                seen.add(key)
                fracs.append((n, d))

        for n, d in fracs[:6]:
            row = tk.Frame(self.frac_frame, bg=SURFACE2,
                           highlightbackground=BORDER, highlightthickness=1)
            row.pack(fill="x", pady=3)
            row.columnconfigure(1, weight=1)

            tk.Label(row, text=f"{n}/{d}", bg=SURFACE2, fg=ACCENT2,
                     font=self.fn_mono, width=8).grid(row=0, column=0, padx=8, pady=6)

            bar_bg = tk.Frame(row, bg=BORDER, height=8)
            bar_bg.grid(row=0, column=1, sticky="ew", padx=(0, 8))
            bar_bg.update_idletasks()

            pct = min(1.0, n / d)

            def draw_bar(event, bg=bar_bg, p=pct):
                w = int(bg.winfo_width() * p)
                for c in bg.winfo_children():
                    c.destroy()
                tk.Frame(bg, bg=ACCENT2, height=8, width=w).place(x=0, y=0)

            bar_bg.bind("<Configure>", draw_bar)
            tk.Label(row, text=f"≈ {n/d:.3f}".rstrip('0').rstrip('.'),
                     bg=SURFACE2, fg=TEXT_DIM, font=self.fn_small, width=7).grid(row=0, column=2, padx=4)

    def _on_tab_change(self, event):
        tab = self.nb.index(self.nb.select())
        self.zoom_frame.grid_remove() if tab != 0 else self.zoom_frame.grid()
        self._draw_active_tab()

    def _draw_active_tab(self):
        tab = self.nb.index(self.nb.select())
        self.fig.clear()
        if tab == 0:
            self._draw_number_line()
        elif tab == 1:
            self._draw_grid()
        elif tab == 2:
            self._draw_compare()
        elif tab == 3:
            self._draw_place()
        self.mpl_canvas.draw()

    # ─── TAB 0: NUMBER LINE ────────────────────────────────────────
    def _draw_number_line(self):
        val = self._get_value()
        zoom = self.zoom_level

        gs = gridspec.GridSpec(2, 1, figure=self.fig,
                               hspace=0.55, top=0.92, bottom=0.08,
                               left=0.06, right=0.97)
        ax1 = self.fig.add_subplot(gs[0])
        ax2 = self.fig.add_subplot(gs[1])

        max_val = max(self.int_var.get() + 1, 2)
        self._draw_line_ax(ax1, val, 0, max_val, zoom=False,
                           title=f"Числова пряма (від 0 до {max_val})")

        r = 1.0 / zoom
        z_start = max(0.0, val - r * 0.55)
        z_end   = z_start + r
        self._draw_line_ax(ax2, val, z_start, z_end, zoom=True,
                           title=f"Збільшено ×{zoom}")

    def _draw_line_ax(self, ax, val, start, end, zoom, title):
        ax.set_facecolor(SURFACE)
        ax.set_xlim(start - (end - start) * 0.03,
                    end   + (end - start) * 0.05)
        ax.set_ylim(-1, 1)
        ax.set_title(title, color=TEXT_DIM, fontsize=11, loc='left', pad=6)
        ax.axis('off')

        # Range bar
        bar_y = 0.0
        ax.annotate("", xy=(end + (end-start)*0.03, bar_y),
                    xytext=(start, bar_y),
                    arrowprops=dict(arrowstyle="->", color=BORDER,
                                   lw=1.5, mutation_scale=14))

        # Ticks
        rng = end - start
        if rng <= 0.05:
            step = 0.001
        elif rng <= 0.2:
            step = 0.01
        elif rng <= 1.0:
            step = 0.1
        elif rng <= 2.0:
            step = 0.2
        else:
            step = 0.5

        t = math.ceil(start / step) * step
        while t <= end + step * 0.01:
            t = round(t, 6)
            if start <= t <= end:
                is_whole  = abs(t - round(t)) < 0.00001
                is_tenth  = abs(t * 10 - round(t * 10)) < 0.0001
                tick_h    = 0.35 if is_whole else (0.22 if is_tenth else 0.12)
                col       = TEXT if is_whole else (BORDER+"ff" if is_tenth else BORDER)
                lw        = 1.5 if is_whole else 0.8
                ax.plot([t, t], [-tick_h, tick_h], color=col, lw=lw, zorder=3)

                if is_whole or (zoom and is_tenth) or (zoom and self.zoom_level >= 5):
                    lbl = str(round(t)) if is_whole else (
                        f"{t:.3f}" if step < 0.01 else (
                        f"{t:.2f}" if step < 0.1 else f"{t:.1f}"))
                    ax.text(t, -tick_h - 0.18, lbl, ha='center', va='top',
                            color=TEXT if is_whole else TEXT_DIM,
                            fontsize=9 if is_whole else 7,
                            fontfamily='monospace')
            t = round(t + step, 6)

        # Highlighted value
        if start <= val <= end:
            # glow
            for r_, a_ in [(0.06, 0.06), (0.03, 0.12), (0.01, 0.20)]:
                ax.axvspan(val - r_ * (end-start), val + r_ * (end-start),
                           ymin=0.3, ymax=0.7, alpha=a_, color=ACCENT, zorder=1)

            ax.plot(val, bar_y, 'o', color=ACCENT, markersize=14, zorder=5,
                    markeredgecolor=BG, markeredgewidth=2)
            ax.text(val, 0.5, f"{val:.2f}", ha='center', va='bottom',
                    color=ACCENT, fontsize=13, fontweight='bold',
                    fontfamily='monospace')

            # Shade from 0
            if start < val:
                ax.axvspan(max(start, 0), val, ymin=0.44, ymax=0.56,
                           alpha=0.18, color=ACCENT, zorder=2)

    # ─── TAB 1: GRID ───────────────────────────────────────────────
    def _draw_grid(self):
        val = self._get_value()
        t   = self.tenth_var.get()
        h   = self.hund_var.get()
        i   = self.int_var.get()
        cents = round((val - i) * 100)  # fractional hundredths

        gs = gridspec.GridSpec(1, 2, figure=self.fig,
                               wspace=0.35, left=0.04, right=0.97,
                               top=0.90, bottom=0.08)

        # ── Left: 10×10 grid ──
        ax1 = self.fig.add_subplot(gs[0])
        ax1.set_facecolor(BG)
        ax1.set_xlim(-0.5, 10.5)
        ax1.set_ylim(-1.5, 10.5)
        ax1.axis('off')
        ax1.set_title(f"1 ціла = 100 кліток · закрашено: {cents}/100",
                      color=TEXT_DIM, fontsize=11, pad=10)

        for idx in range(100):
            row = 9 - idx // 10
            col = idx % 10
            if idx < t * 10:
                color, alpha = ACCENT2, 0.85
            elif idx < cents:
                color, alpha = ACCENT5, 0.85
            else:
                color, alpha = SURFACE2, 1.0
            rect = FancyBboxPatch((col + 0.03, row + 0.03), 0.88, 0.88,
                                  boxstyle="round,pad=0.03",
                                  facecolor=color, edgecolor=BORDER,
                                  linewidth=0.6, alpha=alpha)
            ax1.add_patch(rect)

        # Column header labels
        for c in range(10):
            ax1.text(c + 0.5, -0.4, str(c+1), ha='center', va='top',
                     color=TEXT_DIM, fontsize=7, fontfamily='monospace')

        # Legend
        legend_items = [
            mpatches.Patch(color=ACCENT2, label=f"Десяті ({t}/10 = {t*10} кліток)"),
            mpatches.Patch(color=ACCENT5, label=f"Соті ({h}/100 = {h} кліток)"),
            mpatches.Patch(facecolor=SURFACE2, edgecolor=BORDER, label="Порожньо"),
        ]
        ax1.legend(handles=legend_items, loc='lower center',
                   bbox_to_anchor=(0.5, -0.13), ncol=3,
                   facecolor=SURFACE, edgecolor=BORDER,
                   labelcolor=TEXT, fontsize=8, framealpha=0.9)

        # ── Right: strip of 10 (tenths) ──
        ax2 = self.fig.add_subplot(gs[1])
        ax2.set_facecolor(BG)
        ax2.set_xlim(-0.5, 1.5)
        ax2.set_ylim(-0.5, 10.5)
        ax2.axis('off')
        ax2.set_title(f"Смужка десятих · {t}/10",
                      color=TEXT_DIM, fontsize=11, pad=10)

        for idx in range(10):
            row = 9 - idx
            color = ACCENT2 if idx < t else SURFACE2
            rect = FancyBboxPatch((0.05, row + 0.05), 0.85, 0.85,
                                  boxstyle="round,pad=0.03",
                                  facecolor=color, edgecolor=BORDER,
                                  linewidth=0.7,
                                  alpha=0.9 if idx < t else 1.0)
            ax2.add_patch(rect)
            ax2.text(0.5, row + 0.5, f"0.{idx+1 if idx < 9 else ''}",
                     ha='center', va='center',
                     color=TEXT if idx < t else TEXT_DIM,
                     fontsize=8, fontfamily='monospace')

        # Big value annotation
        self.fig.text(0.5, 0.97, f"{val:.2f}",
                      ha='center', va='top', color=ACCENT,
                      fontsize=28, fontweight='bold', fontfamily='monospace')

    # ─── TAB 2: COMPARE ────────────────────────────────────────────
    FAMOUS = [
        (0.10, "1/10",  "одна десята"),
        (0.20, "1/5",   "одна п'ята"),
        (0.25, "1/4",   "чверть"),
        (0.30, "3/10",  "три десятих"),
        (0.33, "≈1/3",  "третина"),
        (0.40, "2/5",   "дві п'ятих"),
        (0.50, "1/2",   "половина"),
        (0.60, "3/5",   "три п'ятих"),
        (0.67, "≈2/3",  "дві третини"),
        (0.75, "3/4",   "три чверті"),
        (0.80, "4/5",   "чотири п'ятих"),
        (0.90, "9/10",  "дев'ять десятих"),
    ]
    PALETTE = [ACCENT2, ACCENT4, ACCENT, ACCENT3, ACCENT5,
               "#ff8a65", "#80cbc4", "#fff176",
               "#a5d6a7", "#f48fb1", "#81d4fa", "#ffcc80"]

    def _draw_compare(self):
        val = self._get_value()
        rows, cols = 3, 4
        gs = gridspec.GridSpec(rows, cols, figure=self.fig,
                               hspace=0.55, wspace=0.35,
                               left=0.04, right=0.97,
                               top=0.93, bottom=0.06)

        self.fig.text(0.5, 0.975,
                      f"Твоє число: {val:.2f} — порівняй з відомими дробами",
                      ha='center', va='top', color=TEXT_DIM, fontsize=10)

        for idx, (fval, frac_str, fname) in enumerate(self.FAMOUS):
            r, c = divmod(idx, cols)
            ax = self.fig.add_subplot(gs[r, c])
            ax.set_facecolor(SURFACE if abs(fval - val) < 0.005 else SURFACE2)
            ax.axis('off')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)

            color = ACCENT if abs(fval - val) < 0.005 else self.PALETTE[idx]

            # Bar
            ax.add_patch(Rectangle((0.05, 0.12), 0.90, 0.18,
                                   facecolor=BORDER, edgecolor='none'))
            ax.add_patch(Rectangle((0.05, 0.12), 0.90 * fval, 0.18,
                                   facecolor=color, edgecolor='none', alpha=0.85))

            ax.text(0.5, 0.72, f"{fval:.2f}", ha='center', va='center',
                    color=color, fontsize=16, fontweight='bold',
                    fontfamily='monospace',
                    transform=ax.transAxes)
            ax.text(0.5, 0.50, frac_str, ha='center', va='center',
                    color=TEXT_DIM, fontsize=9, transform=ax.transAxes)
            ax.text(0.5, 0.06, fname, ha='center', va='bottom',
                    color=TEXT_DIM, fontsize=7, transform=ax.transAxes)

            if abs(fval - val) < 0.005:
                for spine_pos in ['top','bottom','left','right']:
                    ax.spines[spine_pos].set_visible(True)
                    ax.spines[spine_pos].set_edgecolor(ACCENT)
                    ax.spines[spine_pos].set_linewidth(1.5)
                ax.text(0.5, 0.92, "← твоє число!", ha='center', va='top',
                        color=ACCENT, fontsize=7, transform=ax.transAxes)

    # ─── TAB 3: PLACE VALUE ────────────────────────────────────────
    def _draw_place(self):
        val = self._get_value()
        i   = self.int_var.get()
        t   = self.tenth_var.get()
        h   = self.hund_var.get()

        gs = gridspec.GridSpec(2, 1, figure=self.fig,
                               hspace=0.6, top=0.90, bottom=0.08,
                               left=0.05, right=0.96)

        # ── Top: digit breakdown ──
        ax1 = self.fig.add_subplot(gs[0])
        ax1.set_facecolor(BG)
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 1)
        ax1.axis('off')
        ax1.set_title("Кожна цифра — це окремий розряд",
                      color=TEXT_DIM, fontsize=11, loc='left', pad=8)

        cols_info = [
            (1.0, 2.2, str(i),   "Одиниці",   "× 1",    TEXT,    i > 0),
            (3.8, 5.0, "·",      "",           "",       TEXT_DIM, False),
            (5.3, 6.5, str(t),   "Десяті",     "× 0.1",  ACCENT2, t > 0),
            (7.0, 8.2, str(h),   "Соті",       "× 0.01", ACCENT4, h > 0),
        ]

        for x0, x1, digit, name, mult, color, active in cols_info:
            xc = (x0 + x1) / 2
            if digit == "·":
                ax1.text(xc, 0.5, "·", ha='center', va='center',
                         color=TEXT_DIM, fontsize=40, fontweight='bold')
                continue

            bg_color = color + "18" if active else SURFACE2
            rect = FancyBboxPatch((x0, 0.05), x1 - x0, 0.90,
                                  boxstyle="round,pad=0.03",
                                  facecolor=bg_color,
                                  edgecolor=color if active else BORDER,
                                  linewidth=1.5 if active else 0.8)
            ax1.add_patch(rect)

            ax1.text(xc, 0.82, name, ha='center', va='center',
                     color=color if active else TEXT_DIM, fontsize=9,
                     fontfamily='monospace')
            ax1.text(xc, 0.50, digit, ha='center', va='center',
                     color=color if active else TEXT_DIM,
                     fontsize=32, fontweight='bold', fontfamily='monospace')
            ax1.text(xc, 0.18, mult, ha='center', va='center',
                     color=TEXT_DIM, fontsize=8, fontfamily='monospace')

        # ── Bottom: formula breakdown ──
        ax2 = self.fig.add_subplot(gs[1])
        ax2.set_facecolor(SURFACE)
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 1)
        ax2.axis('off')
        ax2.set_title("Формула розкладу", color=TEXT_DIM, fontsize=11,
                      loc='left', pad=8)

        parts = []
        if i > 0:
            parts.append((f"{i} × 1 = {i}", TEXT))
        if t > 0:
            parts.append((f"{t} × 0.1 = {t*0.1:.1f}", ACCENT2))
        if h > 0:
            parts.append((f"{h} × 0.01 = {h*0.01:.2f}", ACCENT4))
        if not parts:
            parts.append(("0 × 1 = 0", TEXT_DIM))

        n = len(parts)
        gap = 10 / (n + 1)
        for pi, (txt, col) in enumerate(parts):
            xc = gap * (pi + 1)
            ax2.text(xc, 0.62, txt, ha='center', va='center',
                     color=col, fontsize=13, fontfamily='monospace',
                     fontweight='bold')
            if pi < n - 1:
                ax2.text(xc + gap * 0.5, 0.62, "+",
                         ha='center', va='center',
                         color=TEXT_DIM, fontsize=16)

        ax2.text(5, 0.22,
                 f"= {val:.2f}   ({number_name(i, t, h)})",
                 ha='center', va='center', color=ACCENT,
                 fontsize=16, fontweight='bold', fontfamily='monospace')

    # ─── ZOOM ──────────────────────────────────────────────────────
    def _zoom_in(self):
        idx = self.zoom_steps.index(self.zoom_level)
        if idx < len(self.zoom_steps) - 1:
            self.zoom_level = self.zoom_steps[idx + 1]
            self.zoom_lbl.config(text=f"×{self.zoom_level}")
            self._draw_number_line()
            self.mpl_canvas.draw()

    def _zoom_out(self):
        idx = self.zoom_steps.index(self.zoom_level)
        if idx > 0:
            self.zoom_level = self.zoom_steps[idx - 1]
            self.zoom_lbl.config(text=f"×{self.zoom_level}")
            self._draw_number_line()
            self.mpl_canvas.draw()

    def _zoom_reset(self):
        self.zoom_level = 1
        self.zoom_lbl.config(text="×1")
        self._draw_number_line()
        self.mpl_canvas.draw()


# ─── MAIN ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    plt.rcParams.update({
        "figure.facecolor":  BG,
        "axes.facecolor":    SURFACE,
        "text.color":        TEXT,
        "axes.labelcolor":   TEXT,
        "xtick.color":       TEXT_DIM,
        "ytick.color":       TEXT_DIM,
        "axes.edgecolor":    BORDER,
        "axes.titlecolor":   TEXT,
        "grid.color":        BORDER,
        "font.family":       "monospace",
        "axes.spines.top":   False,
        "axes.spines.right": False,
    })
    app = DecimalVisualizerApp()
    app.mainloop()
