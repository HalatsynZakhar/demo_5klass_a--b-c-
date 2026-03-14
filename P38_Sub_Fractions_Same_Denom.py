import tkinter as tk
from tkinter import ttk, font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.gridspec as gridspec
import numpy as np
import random
import re


class SolutionWindow(tk.Toplevel):
    """Окреме, повністю функціональне вікно для показу рішення"""

    def __init__(self, parent, solution_steps):
        super().__init__(parent)
        self.title("Рішення завдання (5 клас)")
        self.geometry("800x600")

        self.font_explanation = font.Font(family="Helvetica", size=18)
        self.font_title = font.Font(family="Helvetica", size=20, weight="bold")
        self.font_frac = font.Font(family="Helvetica", size=22, weight="bold")

        main_canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)

        scrollable_frame.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        row_counter = 0
        for style, text in solution_steps:
            frame = ttk.LabelFrame(scrollable_frame, padding=15)
            frame.grid(row=row_counter, column=0, sticky="ew", pady=10, padx=10)
            scrollable_frame.columnconfigure(0, weight=1)
            row_counter += 1

            lines = text.split('\n')

            title_label = ttk.Label(frame, text=lines[0],
                                    font=self.font_title if style == "bold" else self.font_explanation)
            title_label.pack(anchor="w")

            for line in lines[1:]:
                if "->" in line:
                    parts = line.split("->")
                    frac_frame = ttk.Frame(frame)
                    frac_frame.pack(anchor="w", pady=10)

                    for i, part in enumerate(parts):
                        if i > 0:
                            ttk.Label(frac_frame, text="  =  ", font=self.font_frac).pack(side=tk.LEFT, padx=10)
                        self.draw_fraction_expression(frac_frame, part.strip())
                else:
                    line_label = ttk.Label(frame, text=line, font=self.font_explanation, wraplength=700)
                    line_label.pack(anchor="w", pady=2)
                    frame.bind("<Configure>", lambda e, lbl=line_label: lbl.config(wraplength=e.width - 40))

    def draw_fraction_expression(self, parent, expression):
        tokens = re.split(r'(\s[+-]\s|=)', expression)
        for token in tokens:
            token = token.strip()
            if not token: continue
            if "/" in token:
                try:
                    if ' ' in token:
                        whole_part, frac_part = token.split(' ')
                        n_str, d_str = frac_part.split('/')
                        whole_label = ttk.Label(parent, text=f"{whole_part}", font=self.font_frac)
                        whole_label.pack(side=tk.LEFT, padx=(0, 5))
                    else:
                        n_str, d_str = token.replace('(', '').replace(')', '').split('/')
                except ValueError:
                    ttk.Label(parent, text=token, font=self.font_frac).pack(side=tk.LEFT)
                    continue
                canvas = tk.Canvas(parent, height=60, bg=self.cget('bg'), highlightthickness=0)
                canvas.pack(side=tk.LEFT)
                n_w, d_w = self.font_frac.measure(n_str), self.font_frac.measure(str(d_str))
                max_w = max(n_w, d_w) + 10
                canvas.config(width=max_w)
                canvas.create_text(max_w / 2, 15, text=n_str, font=self.font_frac, anchor="center")
                canvas.create_line(2, 30, max_w - 2, 30, width=3)
                canvas.create_text(max_w / 2, 45, text=d_str, font=self.font_frac, anchor="center")
            else:
                ttk.Label(parent, text=f" {token} ", font=self.font_frac).pack(side=tk.LEFT)


class FractionVisualizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Тренажер (5 клас): Віднімання дробів з однаковими знаменниками")
        try:
            self.state('zoomed')
        except tk.TclError:
            self.attributes('-zoomed', True)

        self.MAX_CIRCLES = 6
        self.MAX_SLIDER_VAL = 50
        self.color1, self.color2, self.empty_color = 'deepskyblue', 'salmon', '#E0E0E0'

        self.task_n1, self.task_n2, self.task_d = 0, 0, 1
        self.correct_n, self.correct_d = 0, 1

        self.font_body = font.Font(family="Helvetica", size=16)
        self.font_title = font.Font(family="Helvetica", size=18, weight="bold")
        self.font_slider_value = font.Font(family="Helvetica", size=17, weight="bold")
        self.font_success = font.Font(family="Helvetica", size=18, weight="bold")

        self.style = ttk.Style(self)
        self.style.configure("TLabel", font=self.font_body)
        self.style.configure("TButton", font=self.font_body, padding=10)
        self.style.configure("TScale", length=300)
        self.style.configure("Title.TLabel", font=self.font_title)
        self.style.configure("Success.TLabel", font=self.font_success, foreground="green")
        self.style.configure("Error.TLabel", font=self.font_success, foreground="red")

        self.ans_w_var = tk.IntVar()
        self.ans_n_var = tk.IntVar()
        self.ans_d_var = tk.IntVar()
        self.result_status_var = tk.StringVar()

        main_pane = ttk.PanedWindow(self, orient=tk.VERTICAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        top_pane_frame = ttk.Frame(main_pane)
        top_pane_frame.columnconfigure(0, weight=1)
        top_pane_frame.rowconfigure(1, weight=1)
        main_pane.add(top_pane_frame, weight=3)

        task_frame = ttk.Frame(top_pane_frame)
        task_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.task_canvas = tk.Canvas(task_frame, height=70)
        self.task_canvas.pack(side=tk.LEFT, fill=tk.X, expand=True)

        toolbar_frame = ttk.Frame(task_frame)
        toolbar_frame.pack(side=tk.LEFT, padx=20)
        self.result_status_label = ttk.Label(toolbar_frame, textvariable=self.result_status_var, style="Success.TLabel")
        self.result_status_label.pack(side=tk.LEFT, padx=20)
        ttk.Button(toolbar_frame, text="Нове завдання", command=self._generate_new_task).pack(side=tk.LEFT, padx=10)
        ttk.Button(toolbar_frame, text="Як це розв'язати?", command=self._open_solution_window).pack(side=tk.LEFT,
                                                                                                     padx=10)

        controls_frame = ttk.Frame(top_pane_frame)
        controls_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        controls_frame.columnconfigure(0, weight=1)

        self.ans_controls = self._create_fraction_controls(controls_frame, "Ваша відповідь:", self.ans_w_var,
                                                           self.ans_n_var, self.ans_d_var, 0)

        plot_frame = ttk.Frame(main_pane)
        main_pane.add(plot_frame, weight=7)

        self.figure = plt.figure(figsize=(14, 6), dpi=90)
        self.canvas = FigureCanvasTkAgg(self.figure, plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._generate_new_task()

    def _create_fraction_controls(self, parent, title, whole_var, num_var, den_var, col):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=col, padx=20, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        ttk.Label(frame, text=title, style="Title.TLabel", foreground="navy").pack(pady=(0, 10))

        whole_widgets = self._create_slider_unit(frame, "Ціла частина:", whole_var)
        whole_widgets['frame'].pack(pady=5, fill="x")
        ttk.Separator(frame, orient="horizontal").pack(pady=5, fill="x")

        num_widgets = self._create_slider_unit(frame, "Чисельник:", num_var)
        num_widgets['frame'].pack(pady=5, fill="x")
        ttk.Separator(frame, orient="horizontal").pack(pady=5, fill="x")

        den_widgets = self._create_slider_unit(frame, "Знаменник:", den_var)
        den_widgets['frame'].pack(pady=5, fill="x")

        return {'frame': frame, 'whole': whole_widgets, 'num': num_widgets, 'den': den_widgets}

    def _create_slider_unit(self, parent, label_text, var):
        frame = ttk.Frame(parent)
        frame.columnconfigure(1, weight=1)
        ttk.Label(frame, text=label_text).grid(row=0, column=0, columnspan=4, sticky="w")

        scale = ttk.Scale(frame, from_=0, to=self.MAX_SLIDER_VAL, variable=var,
                          command=lambda val, v=var: self._on_slider_change(val, v), orient="horizontal")
        scale.grid(row=1, column=1, sticky="ew")

        btn_minus = ttk.Button(frame, text="-", command=lambda v=var: self._adjust_value(v, -1))
        btn_minus.grid(row=1, column=0, padx=(0, 5))
        btn_plus = ttk.Button(frame, text="+", command=lambda v=var: self._adjust_value(v, 1))
        btn_plus.grid(row=1, column=2, padx=5)

        ttk.Label(frame, textvariable=var, font=self.font_slider_value, width=4).grid(row=1, column=3, padx=(10, 0))
        return {'frame': frame, 'scale': scale, 'plus': btn_plus, 'minus': btn_minus}

    def _adjust_value(self, var, delta):
        new_val = var.get() + delta
        if var == self.ans_d_var and new_val < 1: new_val = 1
        if var != self.ans_d_var and new_val < 0: new_val = 0
        var.set(new_val)
        self._on_slider_change()

    def _on_slider_change(self, value=None, var=None):
        if var is not None and value is not None: var.set(int(float(value)))

        if self.ans_d_var.get() < 1: self.ans_d_var.set(1)
        if self.ans_n_var.get() < 0: self.ans_n_var.set(0)
        if self.ans_w_var.get() < 0: self.ans_w_var.set(0)

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

        # Обчислюємо правильний результат
        self.correct_n = n1 - n2
        self.correct_d = d

        # Скидаємо повзунки відповіді
        self.ans_w_var.set(0)
        self.ans_n_var.set(0)
        self.ans_d_var.set(d)

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
        if canvas_w < 50: return

        task_font = font.Font(family="Helvetica", size=24, weight="bold")
        prefix_text = "Завдання: "
        prefix_len = font.Font(font=self.font_body).measure(prefix_text)
        self.task_canvas.create_text(10, canvas_h / 2, text=prefix_text, font=self.font_body, anchor="w", fill="navy")
        x_pos = prefix_len + 15

        def draw_frac(n, d, x):
            n_w, d_w = task_font.measure(str(n)), task_font.measure(str(d))
            max_w = max(n_w, d_w) + 10
            self.task_canvas.create_text(x + max_w / 2, canvas_h / 2 - 16, text=str(n), font=task_font, anchor="center")
            self.task_canvas.create_line(x, canvas_h / 2, x + max_w, canvas_h / 2, width=3)
            self.task_canvas.create_text(x + max_w / 2, canvas_h / 2 + 16, text=str(d), font=task_font, anchor="center")
            return x + max_w + 20

        x_pos = draw_frac(self.task_n1, self.task_d, x_pos)
        self.task_canvas.create_text(x_pos, canvas_h / 2, text="-", font=task_font, anchor="center")
        x_pos += 40
        draw_frac(self.task_n2, self.task_d, x_pos)

    def _set_controls_state(self, state):
        for key in ['whole', 'num', 'den']:
            self.ans_controls[key]['scale'].config(state=state)
            self.ans_controls[key]['plus'].config(state=state)
            self.ans_controls[key]['minus'].config(state=state)

    def visualize(self):
        self.figure.clear()

        gs_main = gridspec.GridSpec(2, 3, figure=self.figure, height_ratios=[1, 9], hspace=0.1)
        ax_title1, ax_title2, ax_title3 = (self.figure.add_subplot(gs_main[0, i], facecolor='none') for i in range(3))
        for ax in [ax_title1, ax_title2, ax_title3]: ax.axis('off')

        ax_title1.set_title(self.format_user_input_title("Зменшуване", 0, self.task_n1, self.task_d), fontsize=18)
        ax_title2.set_title(self.format_user_input_title("Від'ємник", 0, self.task_n2, self.task_d), fontsize=18)

        user_w, user_n, user_d = self.ans_w_var.get(), self.ans_n_var.get(), self.ans_d_var.get()
        ax_title3.set_title(self.format_user_input_title("Ваша відповідь", user_w, user_n, user_d), fontsize=18,
                            color="green")

        ax1, ax2, ax3 = (self.figure.add_subplot(gs_main[1, i]) for i in range(3))

        self._draw_overlapping_circles(ax1, self.task_n1, self.task_d, self.color1)
        self._draw_overlapping_circles(ax2, self.task_n2, self.task_d, self.color2)

        user_improper_n = user_w * user_d + user_n
        if user_w == 0 and user_n == 0 and self.correct_n != 0:
            self.draw_placeholder(ax3, "Введіть\nрезультат")
        else:
            self._draw_overlapping_circles(ax3, user_improper_n, user_d, 'mediumseagreen')

        self.figure.tight_layout(pad=2.0)
        self.canvas.draw()

    def _check_user_answer(self):
        user_w = self.ans_w_var.get()
        user_n = self.ans_n_var.get()
        user_d = self.ans_d_var.get()

        if user_d == 0:
            self.result_status_var.set("Знаменник не може бути нулем!")
            self.result_status_label.config(style="Error.TLabel")
            return

        # Якщо правильна відповідь 0
        if self.correct_n == 0:
            if user_w == 0 and user_n == 0:
                self.result_status_var.set("✔ ВІДМІННО! Дроби однакові, тому їх різниця дорівнює нулю.")
                self.result_status_label.config(style="Success.TLabel")
                self._set_controls_state(tk.DISABLED)
            else:
                self.result_status_var.set("")
            return

        if user_w == 0 and user_n == 0:
            self.result_status_var.set("")
            return

        # ПЕРЕВІРКА: Учень не повинен змінювати знаменник
        if user_d != self.correct_d:
            self.result_status_var.set("Пам'ятайте: при відніманні знаменник залишається тим самим!")
            self.result_status_label.config(style="Error.TLabel")
            return

        # Перевірка точного збігу без скорочень (чисельник та знаменник)
        if user_w == 0 and user_n == self.correct_n and user_d == self.correct_d:
            self.result_status_var.set("✔ ВІДМІННО! Абсолютно правильна відповідь.")
            self.result_status_label.config(style="Success.TLabel")
            self._set_controls_state(tk.DISABLED)
        else:
            self.result_status_var.set("Поки що неправильно. Спробуйте ще!")
            self.result_status_label.config(style="Error.TLabel")

    def format_user_input_title(self, base_title, w, n, d):
        if d == 0: return base_title

        whole_str = f"${w}$" if w > 0 else ""
        frac_str = f"$\\frac{{{n}}}{{{d}}}$" if n > 0 or (w == 0 and n == 0 and d != 0) else ""

        if w == 0 and n == 0 and d != 0:
            return f"{base_title}\n$0$"
        elif w == 0 and n > 0 and d != 0:
            return f"{base_title}\n{frac_str}"
        elif w > 0 and n == 0 and d != 0:
            return f"{base_title}\n{whole_str}"

        return f"{base_title}\n{whole_str}{frac_str}"

    def _draw_overlapping_circles(self, ax, n, d, color):
        ax.axis('off')
        ax.set_aspect('equal', adjustable='box')
        if d == 0: return
        whole, frac_n = divmod(n, d)
        total_circles = whole + (1 if frac_n > 0 else 0)
        if total_circles == 0 and n == 0: self.draw_fraction_pie(ax, [0], [color], d, center=(0, 0)); return

        radius = 1.0
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
                                    "При відніманні дробів з однаковими знаменниками:\nвід чисельника зменшуваного віднімають чисельник від'ємника,\nа знаменник залишають тим самим."))

        diff_n = n1 - n2

        if diff_n == 0:
            self.solution_steps.extend([
                ("bold", "--- КРОК 1: ВІДНІМАЄМО ЧИСЕЛЬНИКИ ---"),
                ("normal", f"Чисельники однакові: {n1} - {n2} = 0."),
                ("normal", f"Якщо чисельник дорівнює нулю, то весь дріб дорівнює нулю."),
                ("bold", "Кінцева відповідь: 0")
            ])
            return

        self.solution_steps.extend([
            ("bold", "--- КРОК 1: ВІДНІМАЄМО ЧИСЕЛЬНИКИ ---"),
            ("normal", f"({n1}/{d}) - ({n2}/{d}) -> ({(n1 - n2)}/{d})")
        ])

        self.solution_steps.append(("bold", f"Кінцева відповідь: {diff_n}/{d}"))

    def draw_fraction_pie(self, ax, numerators, colors, denominator, center=(0, 0), radius=1.0):
        sizes, final_colors = [], []
        total_num = sum(numerators)
        if total_num > 0:
            sizes.extend([n for n in numerators if n > 0])
            final_colors.extend(colors[:len(sizes)])
        if denominator - total_num > 0:
            sizes.append(denominator - total_num)
            final_colors.append(self.empty_color)
        if not sizes: sizes, final_colors = [1], [self.empty_color]

        ax.pie(sizes, radius=radius * 2.2, center=center, colors=final_colors, startangle=90, counterclock=False,
               wedgeprops={'edgecolor': 'black', 'linewidth': 0.8})

    def draw_placeholder(self, ax, text):
        ax.axis('off')
        ax.text(0.5, 0.5, text, ha='center', va='center', fontsize=20, color='grey', transform=ax.transAxes, wrap=True)

    def _open_solution_window(self):
        self._build_solution_for_task()
        SolutionWindow(self, self.solution_steps)


if __name__ == "__main__":
    app = FractionVisualizerApp()
    app.mainloop()