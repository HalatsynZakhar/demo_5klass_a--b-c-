import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
import random

# --- Palette (from P37_Improper_Fractions.py) ---
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
TEAL_LT   = "#ccfbf1"
TEAL      = "#0f766e"

# --- Fonts (from P37_Improper_Fractions.py) ---
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
F_MIXED  = ("Segoe UI", 40, "bold")


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


class SolutionWindow(tk.Toplevel):
    """Окреме, повністю функціональне вікно для показу рішення"""

    def __init__(self, parent, solution_steps, task_type):
        super().__init__(parent)
        self.title("Рішення завдання")
        self.configure(bg=BG)
        self.geometry("900x650")

        self.task_type = task_type

        hdr = tk.Frame(self, bg=HDR_BG, height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="Рішення завдання",
                 bg=HDR_BG, fg=WHITE, font=("Segoe UI", 18, "bold")).pack(side="left", padx=20)
        mkbtn(hdr, "✕  Закрити", self.destroy, bg=RED,
              font=("Segoe UI", 12, "bold"), w=10, h=1).pack(side="right", padx=16, pady=12)

        # Scroll area
        sc = tk.Canvas(self, bg=BG, highlightthickness=0)
        vsb = tk.Scrollbar(self, orient="vertical", command=sc.yview)
        sc.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        sc.pack(side="left", fill="both", expand=True)
        outer = tk.Frame(sc, bg=BG)
        win = sc.create_window((0, 0), window=outer, anchor="nw")
        outer.bind("<Configure>", lambda e: sc.configure(scrollregion=sc.bbox("all")))
        sc.bind("<Configure>", lambda e: sc.itemconfig(win, width=e.width))

        pad = tk.Frame(outer, bg=BG)
        pad.pack(fill="both", expand=True, padx=30, pady=20)

        for style, text in solution_steps:
            card = tk.Frame(pad, bg=PANEL, padx=16, pady=12,
                            highlightbackground=BORDER, highlightthickness=1)
            card.pack(fill="x", pady=8)

            lines = text.split("\n")
            title_font = F_SUB if style == "bold" else F_BODY
            tk.Label(card, text=lines[0], font=title_font, bg=PANEL,
                     fg=TEXT, anchor="w", justify="left").pack(anchor="w")

            for line in lines[1:]:
                if "->" in line:
                    parts = line.split("->")
                    left, right = parts[0].strip(), parts[1].strip()
                    frac_frame = tk.Frame(card, bg=PANEL)
                    frac_frame.pack(anchor="w", pady=8)
                    if self.task_type == "mixed_to_improper":
                        # left mixed, right improper
                        if " " in left and "/" in left:
                            whole_str, fraction_str = left.split(" ", 1)
                            self.draw_mixed_number(frac_frame, whole_str, fraction_str)
                        else:
                            self.draw_single_fraction(frac_frame, left)
                        tk.Label(frac_frame, text="  →  ", font=F_FRAC_S,
                                 bg=PANEL, fg=TEXT).pack(side="left", padx=8)
                        self.draw_single_fraction(frac_frame, right)
                    else:
                        # left improper, right mixed
                        self.draw_single_fraction(frac_frame, left)
                        tk.Label(frac_frame, text="  →  ", font=F_FRAC_S,
                                 bg=PANEL, fg=TEXT).pack(side="left", padx=8)
                        if " " in right and "/" in right:
                            whole_str, fraction_str = right.split(" ", 1)
                            self.draw_mixed_number(frac_frame, whole_str, fraction_str)
                        else:
                            self.draw_single_fraction(frac_frame, right)
                else:
                    tk.Label(card, text=line, font=F_BODY, bg=PANEL, fg=TEXT,
                             anchor="w", justify="left", wraplength=820).pack(anchor="w", pady=2)

    def draw_single_fraction(self, parent, frac_str):
        try:
            n_str, d_str = map(str.strip, frac_str.replace("(", "").replace(")", "").split("/"))
        except ValueError:
            tk.Label(parent, text=frac_str, font=F_FRAC_S, bg=PANEL, fg=ACCENT).pack(side="left")
            return

        canvas = tk.Canvas(parent, height=60, bg=PANEL, highlightthickness=0)
        canvas.pack(side="left")
        n_w = len(n_str) * 12 + 10
        d_w = len(d_str) * 12 + 10
        max_w = max(n_w, d_w) + 10
        canvas.config(width=max_w)
        canvas.create_text(max_w / 2, 15, text=n_str, font=F_FRAC_S, anchor="center", fill=ACCENT)
        canvas.create_line(2, 30, max_w - 2, 30, width=3, fill=ACCENT)
        canvas.create_text(max_w / 2, 45, text=d_str, font=F_FRAC_S, anchor="center", fill=ACCENT)

    def draw_mixed_number(self, parent, whole_str, frac_str):
        try:
            n_str, d_str = map(str.strip, frac_str.replace("(", "").replace(")", "").split("/"))
        except ValueError:
            tk.Label(parent, text=f"{whole_str} {frac_str}", font=F_FRAC_S,
                     bg=PANEL, fg=TEXT).pack(side="left")
            return

        whole_w = len(whole_str) * 18 + 12
        n_w = len(n_str) * 12 + 10
        d_w = len(d_str) * 12 + 10
        frac_max_w = max(n_w, d_w) + 10

        canvas = tk.Canvas(parent, height=60, width=whole_w + frac_max_w + 8,
                           bg=PANEL, highlightthickness=0)
        canvas.pack(side="left")

        canvas.create_text(whole_w / 2, 30, text=whole_str, font=F_FRAC_S,
                           anchor="center", fill=GREEN)
        frac_x_offset = whole_w + 6
        canvas.create_text(frac_x_offset + frac_max_w / 2, 15, text=n_str,
                           font=F_FRAC_S, anchor="center", fill=ACCENT2)
        canvas.create_line(frac_x_offset, 30, frac_x_offset + frac_max_w, 30,
                           width=3, fill=ACCENT2)
        canvas.create_text(frac_x_offset + frac_max_w / 2, 45, text=d_str,
                           font=F_FRAC_S, anchor="center", fill=ACCENT2)


class FractionConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Тренажер: Перетворення дробів")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.MAX_DENOMINATOR = 10
        self.MAX_WHOLE_PART = 5
        self.MAX_IMPROPER_NUMERATOR = self.MAX_DENOMINATOR * self.MAX_WHOLE_PART + self.MAX_DENOMINATOR - 1

        self.color_filled = 'mediumseagreen'
        self.color_empty = '#E0E0E0'

        # Task state
        self.task_type = None  # "mixed_to_improper" or "improper_to_mixed"
        self.mixed_whole, self.mixed_num, self.mixed_den = 0, 0, 1
        self.improper_num, self.improper_den = 0, 1

        # User inputs
        self.user_whole_var = tk.IntVar(value=0)
        self.user_num_var = tk.IntVar(value=0)
        self.user_den_var = tk.IntVar(value=1)
        self.success_var = tk.StringVar()

        self._build_chrome()
        self._build_main()

        self._generate_new_task()
        self._on_slider_change()

    def _build_chrome(self):
        hdr = tk.Frame(self, bg=HDR_BG, height=70)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="§ 37.  Мішані числа",
                 bg=HDR_BG, fg=WHITE, font=("Segoe UI", 21, "bold")).pack(side="left", padx=30)
        mkbtn(hdr, "✕  Вийти", self.destroy, bg=RED,
              font=("Segoe UI", 13, "bold"), w=9, h=1).pack(side="right", padx=18, pady=16)

        nav = tk.Frame(self, bg=NAV_BG, height=52)
        nav.pack(fill="x")
        nav.pack_propagate(False)
        for label, cmd in [
            ("🎯  Тренажер", self._show_main),
            ("🧾  Рішення", self._open_solution_window),
            ("🆕  Нове завдання", self._generate_new_task),
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

    def _show_main(self):
        if self.main_frame:
            self.main_frame.pack(fill="both", expand=True)

    def _build_main(self):
        self.main_frame = tk.Frame(self.main_area, bg=BG)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=16)

        # left panel (controls)
        left = tk.Frame(self.main_frame, bg=PANEL,
                        highlightbackground=BORDER, highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left, text="📋  Завдання", font=F_SUB, bg=PANEL, fg=MUTED).pack(anchor="w", padx=20, pady=(12, 4))
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x")

        self.task_canvas = tk.Canvas(left, height=90, bg=PANEL, highlightthickness=0)
        self.task_canvas.pack(fill="x", padx=20, pady=10)

        toolbar = tk.Frame(left, bg=PANEL)
        toolbar.pack(fill="x", padx=20, pady=(4, 8))
        self.success_label = tk.Label(toolbar, textvariable=self.success_var, font=F_BODYB, fg=GREEN, bg=PANEL)
        self.success_label.pack(side="left", expand=True, anchor="w")
        mkbtn(toolbar, "🆕  Нове", self._generate_new_task, bg=ORANGE, w=10, h=1, font=("Segoe UI", 12, "bold")).pack(side="right", padx=6)
        mkbtn(toolbar, "🧾  Рішення", self._open_solution_window, bg=ACCENT2, w=11, h=1, font=("Segoe UI", 12, "bold")).pack(side="right", padx=6)

        # controls
        self.user_whole_controls = self._create_slider_unit(left, "Ціла частина:", self.user_whole_var, GREEN)
        self.user_whole_controls["frame"].pack(fill="x", padx=20, pady=6)
        self.user_num_controls = self._create_slider_unit(left, "Чисельник:", self.user_num_var, ACCENT2)
        self.user_num_controls["frame"].pack(fill="x", padx=20, pady=6)
        self.user_den_controls = self._create_slider_unit(left, "Знаменник:", self.user_den_var, ACCENT)
        self.user_den_controls["frame"].pack(fill="x", padx=20, pady=6)

        # right panel (visualization)
        right = tk.Frame(self.main_frame, bg=PANEL,
                         highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        tk.Label(right, text="🧩  Візуалізація", font=F_SUB, bg=PANEL, fg=MUTED).pack(anchor="w", padx=20, pady=(12, 4))
        tk.Frame(right, bg=BORDER, height=1).pack(fill="x")

        plot_frame = tk.Frame(right, bg=PANEL)
        plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.figure = plt.figure(figsize=(12, 6), dpi=90)
        self.canvas = FigureCanvasTkAgg(self.figure, plot_frame)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def _create_slider_unit(self, parent, label_text, var, color):
        frame = tk.Frame(parent, bg=PANEL)
        tk.Label(frame, text=label_text, font=F_BODYB, bg=PANEL, fg=color).grid(row=0, column=0, columnspan=4, sticky="w")

        btn_minus = tk.Button(frame, text="−", font=("Segoe UI", 18, "bold"),
                              width=2, bg=BTN_NUM, fg=TEXT, relief="flat",
                              cursor="hand2", command=lambda v=var: self._adjust_value(v, -1))
        btn_minus.grid(row=1, column=0, padx=(0, 6), pady=4)

        scale = tk.Scale(frame, from_=0, to=self.MAX_IMPROPER_NUMERATOR, variable=var,
                         command=lambda val, v=var: self._on_slider_change(val, v),
                         orient="horizontal", showvalue=0, bg=PANEL, troughcolor=BTN_NUM,
                         highlightthickness=0, length=300)
        scale.grid(row=1, column=1, sticky="ew", pady=4)
        frame.columnconfigure(1, weight=1)

        btn_plus = tk.Button(frame, text="+", font=("Segoe UI", 18, "bold"),
                             width=2, bg=BTN_NUM, fg=TEXT, relief="flat",
                             cursor="hand2", command=lambda v=var: self._adjust_value(v, 1))
        btn_plus.grid(row=1, column=2, padx=6, pady=4)

        val_lbl = tk.Label(frame, textvariable=var, font=F_BODYB, bg=PANEL, fg=color, width=4)
        val_lbl.grid(row=1, column=3, padx=(10, 0), pady=4)

        return {"frame": frame, "scale": scale, "plus": btn_plus, "minus": btn_minus}

    def _adjust_value(self, var, delta):
        var.set(var.get() + delta)
        self._on_slider_change()

    def _on_slider_change(self, value=None, var=None):
        if var is not None and value is not None:
            var.set(int(float(value)))

        if self.user_den_var.get() < 1:
            self.user_den_var.set(1)
        if self.user_whole_var.get() < 0:
            self.user_whole_var.set(0)
        if self.user_num_var.get() < 0:
            self.user_num_var.set(0)

        if self.task_type == "improper_to_mixed":
            if self.user_num_var.get() >= self.user_den_var.get() and self.user_den_var.get() > 0:
                self.user_num_var.set(self.user_den_var.get() - 1 if self.user_den_var.get() > 1 else 0)

        self.user_whole_controls["scale"].config(
            to=self.MAX_WHOLE_PART + self.MAX_IMPROPER_NUMERATOR // (self.user_den_var.get() if self.user_den_var.get() > 0 else 1)
        )
        self.user_den_controls["scale"].config(to=self.MAX_DENOMINATOR)

        if self.task_type == "improper_to_mixed":
            self.user_num_controls["scale"].config(to=self.user_den_var.get() - 1 if self.user_den_var.get() > 1 else 0)
        else:
            self.user_num_controls["scale"].config(to=self.MAX_IMPROPER_NUMERATOR)

        self._check_answer()
        self._visualize_fractions()

    def _update_task_display(self):
        self.task_canvas.delete("all")
        self.task_canvas.bind("<Configure>", self._draw_task_content, add="+")
        self.update_idletasks()
        self._draw_task_content()

    def _draw_task_content(self, event=None):
        self.task_canvas.delete("all")
        canvas_w, canvas_h = self.task_canvas.winfo_width(), self.task_canvas.winfo_height()
        if canvas_w < 50:
            return

        prefix_text = "Завдання: "
        prefix_len = len(prefix_text) * 10 + 8
        self.task_canvas.create_text(10, canvas_h / 2, text=prefix_text, font=F_BODY,
                                     anchor="w", fill=ACCENT)
        x_pos = prefix_len + 10

        if self.task_type == "mixed_to_improper":
            whole_str = str(self.mixed_whole)
            whole_w = len(whole_str) * 18 + 10
            self.task_canvas.create_text(x_pos + whole_w / 2, canvas_h / 2, text=whole_str,
                                         font=F_FRAC_S, anchor="center", fill=GREEN)

            frac_x_offset = x_pos + whole_w + 5
            num_str, den_str = str(self.mixed_num), str(self.mixed_den)
            num_w = len(num_str) * 12 + 10
            den_w = len(den_str) * 12 + 10
            max_frac_w = max(num_w, den_w) + 10

            self.task_canvas.create_text(frac_x_offset + max_frac_w / 2, canvas_h / 2 - 20,
                                         text=num_str, font=F_FRAC_S, anchor="center", fill=ACCENT2)
            self.task_canvas.create_line(frac_x_offset, canvas_h / 2,
                                         frac_x_offset + max_frac_w, canvas_h / 2, width=3, fill=ACCENT2)
            self.task_canvas.create_text(frac_x_offset + max_frac_w / 2, canvas_h / 2 + 20,
                                         text=den_str, font=F_FRAC_S, anchor="center", fill=ACCENT2)
        else:
            num_str, den_str = str(self.improper_num), str(self.improper_den)
            num_w = len(num_str) * 12 + 10
            den_w = len(den_str) * 12 + 10
            max_w = max(num_w, den_w) + 10

            self.task_canvas.create_text(x_pos + max_w / 2, canvas_h / 2 - 20,
                                         text=num_str, font=F_FRAC_S, anchor="center", fill=ACCENT)
            self.task_canvas.create_line(x_pos, canvas_h / 2, x_pos + max_w, canvas_h / 2, width=3, fill=ACCENT)
            self.task_canvas.create_text(x_pos + max_w / 2, canvas_h / 2 + 20,
                                         text=den_str, font=F_FRAC_S, anchor="center", fill=ACCENT)

    def _open_solution_window(self):
        self._build_solution_for_task()
        SolutionWindow(self, self.solution_steps, self.task_type)

    def _set_controls_state(self, state):
        for controls in [self.user_whole_controls, self.user_num_controls, self.user_den_controls]:
            controls["scale"].config(state=state)
            controls["plus"].config(state=state)
            controls["minus"].config(state=state)

    def _generate_new_task(self):
        self._set_controls_state(tk.NORMAL)
        self.success_var.set("")

        self.task_type = random.choice(["mixed_to_improper", "improper_to_mixed"])

        den = random.randint(2, self.MAX_DENOMINATOR)
        num_frac = random.randint(1, den - 1)
        whole = random.randint(1, self.MAX_WHOLE_PART)

        if self.task_type == "mixed_to_improper":
            self.mixed_whole = whole
            self.mixed_num = num_frac
            self.mixed_den = den
            self.improper_num = whole * den + num_frac
            self.improper_den = den
            self.user_whole_var.set(0)
            self.user_num_var.set(0)
            self.user_den_var.set(1)
            self._set_control_visibility(whole_part=False, improper_fraction_input=True)
        else:
            while True:
                improper_num = random.randint(den + 1, den * self.MAX_WHOLE_PART + den - 1)
                if improper_num % den != 0:
                    break
            self.improper_num = improper_num
            self.improper_den = den
            self.mixed_whole = improper_num // den
            self.mixed_num = improper_num % den
            self.mixed_den = den
            self.user_whole_var.set(0)
            self.user_num_var.set(0)
            self.user_den_var.set(1)
            self._set_control_visibility(whole_part=True, improper_fraction_input=False)

        self._update_task_display()
        self._on_slider_change()

    def _set_control_visibility(self, whole_part, improper_fraction_input):
        state_whole_ctrl = tk.NORMAL if whole_part else tk.DISABLED
        self.user_whole_controls["scale"].config(state=state_whole_ctrl)
        self.user_whole_controls["plus"].config(state=state_whole_ctrl)
        self.user_whole_controls["minus"].config(state=state_whole_ctrl)

        state_frac_ctrl = tk.NORMAL
        self.user_num_controls["scale"].config(state=state_frac_ctrl)
        self.user_num_controls["plus"].config(state=state_frac_ctrl)
        self.user_num_controls["minus"].config(state=state_frac_ctrl)
        self.user_den_controls["scale"].config(state=state_frac_ctrl)
        self.user_den_controls["plus"].config(state=state_frac_ctrl)
        self.user_den_controls["minus"].config(state=state_frac_ctrl)

        self.user_den_controls["scale"].config(to=self.MAX_DENOMINATOR)

        if whole_part:
            self.user_num_controls["scale"].config(to=self.user_den_var.get() - 1 if self.user_den_var.get() > 1 else 0)
            self.user_whole_controls["scale"].config(
                to=self.MAX_WHOLE_PART + self.MAX_IMPROPER_NUMERATOR // (self.user_den_var.get() if self.user_den_var.get() > 0 else 1)
            )
        else:
            self.user_num_controls["scale"].config(to=self.MAX_IMPROPER_NUMERATOR)

    def _check_answer(self):
        user_w = self.user_whole_var.get()
        user_n = self.user_num_var.get()
        user_d = self.user_den_var.get()

        if user_d == 0:
            self.success_var.set("")
            return

        is_correct = False

        if self.task_type == "mixed_to_improper":
            if user_w != 0:
                self.success_var.set("")
                return

            gcd_user = math.gcd(user_n, user_d)
            simplified_user_n = user_n // gcd_user
            simplified_user_d = user_d // gcd_user

            gcd_correct = math.gcd(self.improper_num, self.improper_den)
            simplified_correct_n = self.improper_num // gcd_correct
            simplified_correct_d = self.improper_den // gcd_correct

            if simplified_user_n == simplified_correct_n and simplified_user_d == simplified_correct_d:
                is_correct = True

        else:
            if user_n >= user_d and user_d > 0:
                self.success_var.set("")
                return

            if user_w == self.mixed_whole:
                gcd_user_frac = math.gcd(user_n, user_d)
                gcd_correct_frac = math.gcd(self.mixed_num, self.mixed_den)
                if (user_n // gcd_user_frac == self.mixed_num // gcd_correct_frac and
                        user_d // gcd_user_frac == self.mixed_den // gcd_correct_frac):
                    is_correct = True

        if is_correct:
            self.success_var.set("✔ ПРАВИЛЬНО!")
            self._set_controls_state(tk.DISABLED)
        else:
            self.success_var.set("")

    def _build_solution_for_task(self):
        if self.task_type == "mixed_to_improper":
            w, n, d = self.mixed_whole, self.mixed_num, self.mixed_den
            step1_res = w * d
            final_num = step1_res + n

            self.solution_steps = [
                ("bold", f"--- Перетворення мішаного числа {w} {n}/{d} в неправильний дріб ---"),
                ("bold", "--- КРОК 1: Множимо цілу частину на знаменник ---"),
                ("normal", f"Щоб перетворити мішане число, спочатку помножте цілу частину ({w}) на знаменник ({d})."),
                ("normal", f"{w} × {d} = {step1_res}"),
                ("bold", "--- КРОК 2: Додаємо чисельник до результату ---"),
                ("normal", f"Додайте отриманий результат ({step1_res}) до чисельника ({n}) мішаного числа."),
                ("normal", f"{step1_res} + {n} = {final_num}"),
                ("bold", "--- КРОК 3: Формуємо неправильний дріб ---"),
                ("normal", f"Новий чисельник - {final_num}, а знаменник залишається таким же ({d})."),
                ("normal", f"{w} {n}/{d} -> {final_num}/{d}"),
                ("bold", "--- РЕЗУЛЬТАТ ---"),
                ("normal", f"Мішане число {w} {n}/{d} перетворюється в неправильний дріб: {final_num}/{d}")
            ]
        else:
            num_imp, den_imp = self.improper_num, self.improper_den
            whole_res = num_imp // den_imp
            remainder_res = num_imp % den_imp

            simplified_num, simplified_den = remainder_res, den_imp
            if remainder_res != 0:
                gcd_frac = math.gcd(remainder_res, den_imp)
                simplified_num = remainder_res // gcd_frac
                simplified_den = den_imp // gcd_frac

            self.solution_steps = [
                ("bold", f"--- Перетворення неправильного дробу {num_imp}/{den_imp} в мішане число ---"),
                ("bold", "--- КРОК 1: Ділимо чисельник на знаменник ---"),
                ("normal", f"Поділіть чисельник ({num_imp}) на знаменник ({den_imp})."),
                ("normal", f"{num_imp} ÷ {den_imp} = {whole_res} (ціла частина) з залишком {remainder_res}."),
                ("bold", "--- КРОК 2: Формуємо мішане число ---"),
                ("normal", f"Ціла частина дробу стає цілою частиною мішаного числа ({whole_res})."),
                ("normal", f"Залишок {remainder_res} стає чисельником дробової частини."),
                ("normal", f"Знаменник залишається без змін ({den_imp})."),
                ("normal", f"({num_imp}/{den_imp}) -> {whole_res} {remainder_res}/{den_imp}"),
                ("normal", f"Скорочуємо дріб, якщо можливо: {remainder_res}/{den_imp} -> {simplified_num}/{simplified_den}"),
                ("bold", "--- РЕЗУЛЬТАТ ---"),
                ("normal", f"Неправильний дріб {num_imp}/{den_imp} перетворюється в мішане число: {whole_res} {simplified_num}/{simplified_den}")
            ]

    def _visualize_fractions(self):
        self.figure.clear()

        task_num_for_pie = 0
        task_den_for_pie = 1
        task_title_text = ""

        if self.task_type == "mixed_to_improper":
            task_num_for_pie = self.mixed_whole * self.mixed_den + self.mixed_num
            task_den_for_pie = self.mixed_den
            task_title_text = f"Завдання: {self.mixed_whole} $\\frac{{{self.mixed_num}}}{{{self.mixed_den}}}$"
        elif self.task_type == "improper_to_mixed":
            task_num_for_pie = self.improper_num
            task_den_for_pie = self.improper_den
            task_title_text = f"Завдання: $\\frac{{{self.improper_num}}}{{{self.improper_den}}}$"

        user_num_for_pie = 0
        user_den_for_pie = 1
        user_title_text = ""

        if self.user_den_var.get() > 0:
            user_num_for_pie = self.user_whole_var.get() * self.user_den_var.get() + self.user_num_var.get()
            user_den_for_pie = self.user_den_var.get()

        if self.task_type == "improper_to_mixed":
            user_title_text = f"Ваша відповідь: {self.user_whole_var.get()} $\\frac{{{self.user_num_var.get()}}}{{{self.user_den_var.get()}}}$"
        else:
            user_title_text = f"Ваша відповідь: $\\frac{{{self.user_num_var.get()}}}{{{self.user_den_var.get()}}}$"

        ax1 = self.figure.add_subplot(1, 2, 1)
        ax2 = self.figure.add_subplot(1, 2, 2)

        self.draw_fraction_pie(ax1, task_num_for_pie, task_den_for_pie, task_title_text, self.color_filled)
        self.draw_fraction_pie(ax2, user_num_for_pie, user_den_for_pie, user_title_text, 'salmon')

        self.figure.tight_layout(pad=3.0)
        self.canvas.draw()

    def draw_fraction_pie(self, ax, numerator, denominator, title, color):
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
                colors = [color, self.color_empty] if denominator - num > 0 else [color]
            else:
                sizes = [1]
                colors = [self.color_empty]

            ax.pie(sizes, colors=colors, startangle=90, counterclock=False,
                   radius=pie_radius, center=(x_center, y_center),
                   wedgeprops={"edgecolor": "black", "linewidth": 1})

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


if __name__ == "__main__":
    app = FractionConverterApp()
    app.mainloop()
