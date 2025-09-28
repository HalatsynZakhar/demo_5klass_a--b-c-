import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random
import math
from tkinter import font as tkfont  # Імпортуємо модуль для роботи зі шрифтами


class InteractiveBoardDemo:
    def __init__(self, master):
        self.master = master
        master.title("Інтерактивна дошка: Правило Віднімання Суми")
        master.state('zoomed')

        self.style = ttk.Style(theme='flatly')
        self.master.configure(bg=self.style.colors.bg)

        # Змінні стану
        self.current_question = {}
        self.animation_step = 0
        self.animation_running = False
        self.animation_job = None

        self.create_widgets()
        self.generate_new_example()

        master.bind('<Configure>', self.on_window_resize)

    def create_widgets(self):
        """Створює всі елементи інтерфейсу, повністю українською мовою."""

        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # === ВЕРХНЯ ПАНЕЛЬ ===
        top_panel = ttk.Frame(self.master, style='primary.TFrame', padding=20)
        top_panel.grid(row=0, column=0, sticky='ew')
        top_panel.grid_columnconfigure(0, weight=1)

        ttk.Label(
            top_panel, text="ПРАВИЛО ВІДНІМАННЯ СУМИ ВІД ЧИСЛА",
            font=("Segoe UI Black", 32), style='primary.Inverse.TLabel'
        ).grid(row=0, column=0, pady=(0, 10))

        ttk.Label(
            top_panel, text="a - (b + c) = a - b - c",
            font=("Segoe UI", 26, "bold"), style='warning.Inverse.TLabel'
        ).grid(row=1, column=0)

        # === ПАНЕЛЬ ПРИКЛАДУ ===
        example_panel = ttk.Frame(self.master, style='secondary.TFrame', padding=15)
        example_panel.grid(row=1, column=0, sticky='ew', pady=5)
        example_panel.grid_columnconfigure(0, weight=1)

        self.example_label = ttk.Label(
            example_panel, text="",
            font=("Segoe UI Semibold", 30), style='secondary.Inverse.TLabel'
        )
        self.example_label.pack()

        # === ОСНОВНА ОБЛАСТЬ ВІЗУАЛІЗАЦІЇ ===
        main_frame = ttk.Frame(self.master, style='light.TFrame', padding=10)
        main_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=5)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        self.left_example_title = ttk.Label(main_frame, text="", font=("Segoe UI", 22, "bold"), style='info.TLabel')
        self.left_example_title.grid(row=0, column=0, pady=5)

        self.right_example_title = ttk.Label(main_frame, text="", font=("Segoe UI", 22, "bold"), style='info.TLabel')
        self.right_example_title.grid(row=0, column=1, pady=5)

        ttk.Label(main_frame, text="Спосіб 1: Віднімаємо суму", font=("Segoe UI", 18)).grid(row=1, column=0)
        ttk.Label(main_frame, text="Спосіб 2: Віднімаємо по черзі", font=("Segoe UI", 18)).grid(row=1, column=1)

        self.left_canvas = tk.Canvas(main_frame, bg=self.style.colors.light, highlightthickness=0)
        self.left_canvas.grid(row=2, column=0, sticky='nsew', padx=(0, 5))

        self.right_canvas = tk.Canvas(main_frame, bg=self.style.colors.light, highlightthickness=0)
        self.right_canvas.grid(row=2, column=1, sticky='nsew', padx=(5, 0))

        # === ПАНЕЛЬ КЕРУВАННЯ ===
        control_panel = ttk.Frame(self.master, style='secondary.TFrame', padding=15)
        control_panel.grid(row=3, column=0, sticky='ew')
        control_panel.grid_columnconfigure([0, 1, 2, 3], weight=1)

        self.step_button = ttk.Button(control_panel, text="▶ Наступний крок", command=self.next_step,
                                      style='success.TButton', width=20)
        self.step_button.grid(row=0, column=0, padx=5, ipady=10)

        self.reset_button = ttk.Button(control_panel, text="↺ Спочатку", command=self.reset_animation,
                                       style='warning.TButton', width=20)
        self.reset_button.grid(row=0, column=1, padx=5, ipady=10)

        self.auto_button = ttk.Button(control_panel, text="🎬 Автоматично", command=self.auto_animate,
                                      style='info.TButton', width=20)
        self.auto_button.grid(row=0, column=2, padx=5, ipady=10)

        self.new_button = ttk.Button(control_panel, text="★ Новий приклад", command=self.generate_new_example,
                                     style='primary.TButton', width=20)
        self.new_button.grid(row=0, column=3, padx=5, ipady=10)

    def generate_new_example(self):
        if self.animation_job: self.master.after_cancel(self.animation_job)
        self.animation_job = None
        self.animation_step = 0
        self.animation_running = False

        a = random.randint(20, 30)
        b = random.randint(4, a // 3)
        c = random.randint(3, (a - b) // 2)

        self.current_question = {'a': a, 'b': b, 'c': c}
        self.example_label.config(text=f"Приклад: {a} - ({b} + {c}) = ?")

        self.left_example_title.config(text=f"{a} - ({b} + {c})")
        self.right_example_title.config(text=f"{a} - {b} - {c}")

        self.draw_visualization()

    def calculate_block_size(self, canvas, total_blocks):
        canvas_width, canvas_height = canvas.winfo_width(), canvas.winfo_height()
        if canvas_width < 100 or canvas_height < 150: return 20

        available_width = canvas_width - 40
        available_height = canvas_height - 200  # Залишаємо ще трохи місця

        blocks_per_row = min(10, total_blocks)
        rows_needed = math.ceil(total_blocks / blocks_per_row)
        if rows_needed == 0: return 20

        size_by_width = available_width / (blocks_per_row * 1.2)
        size_by_height = available_height / (rows_needed * 1.2)

        return int(max(20, min(size_by_width, size_by_height, 60)))

    def draw_visualization(self):
        self.draw_method(self.left_canvas, 'sum')
        self.draw_method(self.right_canvas, 'sequential')

    def draw_method(self, canvas, method):
        canvas.delete("all")
        width, height = canvas.winfo_width(), canvas.winfo_height()
        if width < 100: return

        q = self.current_question
        block_size = self.calculate_block_size(canvas, q['a'])
        font_size = max(12, int(block_size * 0.4))

        y_text = 40
        step_text, step_color = self.get_step_info(method)
        canvas.create_text(width / 2, y_text, text=step_text, font=("Segoe UI", font_size, "bold"), fill=step_color)

        self.draw_blocks_grid(canvas, q['a'], q['b'], q['c'], width / 2, y_text + 40, block_size, method)

        # --- НАДІЙНЕ ВІДОБРАЖЕННЯ ІСТОРІЇ ДІЙ ---
        calc_history = self.get_calc_history(method)
        if not calc_history:
            return

        # 1. Створюємо об'єкт шрифта, щоб отримати його точні розміри
        history_font = tkfont.Font(family="Segoe UI", size=font_size + 2, weight="bold")

        # 2. Отримуємо точну висоту рядка і додаємо відступ для читабельності
        line_height = history_font.metrics('linespace') + 10

        # 3. Розраховуємо початкову позицію Y для першого рядка
        total_text_height = (len(calc_history) - 1) * line_height
        y_start = height - 40 - total_text_height

        # 4. Малюємо кожен рядок з розрахованим інтервалом
        current_y = y_start
        for line in calc_history:
            canvas.create_text(
                width / 2, current_y,
                text=line,
                font=history_font,
                fill=self.style.colors.primary,
                anchor='center'  # Центруємо текст по вертикалі і горизонталі
            )
            current_y += line_height  # Переходимо до наступного рядка

    def get_step_info(self, method):
        q = self.current_question
        a, b, c, answer = q['a'], q['b'], q['c'], q['a'] - q['b'] - q['c']

        steps = {
            'sum': [
                (f"Спочатку маємо {a} блоків", self.style.colors.dark),
                (f"Знайдемо суму в дужках: {b} + {c} = {b + c}", self.style.colors.info),
                (f"Тепер віднімемо всю суму ({b + c})", self.style.colors.danger),
                (f"Залишилось {answer} блоків. Результат: {answer}", self.style.colors.success)
            ],
            'sequential': [
                (f"Спочатку маємо {a} блоків", self.style.colors.dark),
                (f"Спочатку віднімемо перше число: {b}", self.style.colors.info),
                (f"Потім віднімемо друге число: {c}", self.style.colors.danger),
                (f"Залишилось {answer} блоків. Результат: {answer}", self.style.colors.success)
            ]
        }
        return steps[method][self.animation_step]

    def get_calc_history(self, method):
        q = self.current_question
        a, b, c, answer = q['a'], q['b'], q['c'], q['a'] - q['b'] - q['c']
        history = []

        if method == 'sum':
            if self.animation_step >= 1: history.append(f"1) {b} + {c} = {b + c}")
            if self.animation_step == 2: history.append(f"2) {a} - {b + c} = ?")
            if self.animation_step >= 3: history.append(f"2) {a} - {b + c} = {answer}")
        else:
            if self.animation_step >= 1: history.append(f"1) {a} - {b} = {a - b}")
            if self.animation_step == 2: history.append(f"2) {a - b} - {c} = ?")
            if self.animation_step >= 3: history.append(f"2) {a - b} - {c} = {answer}")
        return history

    def draw_blocks_grid(self, canvas, a, b, c, center_x, start_y, block_size, method):
        blocks_per_row = min(10, a)
        total_width = blocks_per_row * (block_size + 5) - 5
        start_x = center_x - total_width / 2

        if method == 'sum' and self.animation_step == 1:
            group_start_index = a - (b + c)
            start_row = group_start_index // blocks_per_row
            start_col = group_start_index % blocks_per_row
            x1 = start_x + start_col * (block_size + 5) - 5
            y1 = start_y + start_row * (block_size + 5) - 5
            x2 = start_x + (blocks_per_row - 1) * (block_size + 5) + block_size + 5
            y2 = start_y + (math.ceil(a / blocks_per_row) - 1) * (block_size + 5) + block_size + 5
            canvas.create_rectangle(x1, y1, x2, y2, fill=self.style.colors.light, stipple="gray25", outline="")

        x, y = start_x, start_y
        for i in range(a):
            info = {'color': self.style.colors.success, 'alpha': 1.0, 'visible': True}

            if method == 'sum':
                if self.animation_step == 1:
                    if i >= a - c:
                        info['color'] = self.style.colors.warning
                    elif i >= a - b - c:
                        info['color'] = self.style.colors.info
                elif self.animation_step == 2 and i >= a - (b + c):
                    info['color'] = self.style.colors.danger
                    info['alpha'] = 0.5
                elif self.animation_step >= 3 and i >= a - (b + c):
                    info['visible'] = False
            else:
                if self.animation_step == 1 and i >= a - b:
                    info['color'] = self.style.colors.info
                    info['alpha'] = 0.5
                elif self.animation_step >= 2:
                    if i >= a - b:
                        info['visible'] = False
                    elif i >= a - b - c:
                        if self.animation_step == 2:
                            info['color'] = self.style.colors.danger
                            info['alpha'] = 0.5
                        else:
                            info['visible'] = False

            if info['visible']:
                self.draw_single_block(canvas, x, y, block_size, info['color'], info['alpha'])

            x += block_size + 5
            if (i + 1) % blocks_per_row == 0 and i < a - 1:
                x = start_x
                y += block_size + 5

    def draw_single_block(self, canvas, x, y, size, color, alpha):
        shadow_color = self.style.colors.secondary
        canvas.create_oval(x + 3, y + 3, x + size + 3, y + size + 3, fill=shadow_color, outline="")
        canvas.create_oval(x, y, x + size, y + size, fill=color, outline=color)

        if alpha < 1.0:
            cross_color = "#FFFFFF"
            cr = int(size * 0.2)
            canvas.create_line(x + cr, y + cr, x + size - cr, y + size - cr, fill=cross_color, width=4)
            canvas.create_line(x + size - cr, y + cr, x + cr, y + size - cr, fill=cross_color, width=4)

    def next_step(self):
        if self.animation_step < 3:
            self.animation_step += 1
            self.draw_visualization()
        else:
            self.reset_animation()

    def reset_animation(self):
        if self.animation_job: self.master.after_cancel(self.animation_job)
        self.animation_running = False
        self.animation_step = 0
        self.draw_visualization()

    def auto_animate(self):
        if not self.animation_running:
            self.animation_running = True
            self.animation_step = 0
            self.run_auto_animation()

    def run_auto_animation(self):
        if self.animation_running and self.animation_step <= 3:
            self.draw_visualization()
            self.animation_step += 1
            if self.animation_step <= 3:
                self.animation_job = self.master.after(1800, self.run_auto_animation)
            else:
                self.animation_running = False
        else:
            self.animation_running = False

    def on_window_resize(self, event=None):
        if hasattr(self, 'resize_job'): self.master.after_cancel(self.resize_job)
        self.resize_job = self.master.after(50, self.draw_visualization)


if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    app = InteractiveBoardDemo(root)
    root.mainloop()