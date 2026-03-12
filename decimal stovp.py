import tkinter as tk
from decimal import Decimal
import random

# ── ПАЛІТРА (Світла тема) ───────────────────────────────────────────────────
COLOR_BG = "#ffffff"  # Білий фон
COLOR_GRID = "#e1f5fe"  # Світло-блакитна клітинка
COLOR_LINE = "#03a9f4"  # Синя лінія зошита
COLOR_TEXT = "#2c3e50"  # Темний текст
COLOR_INPUT = "#f8f9fa"  # Фон клітинки для введення
COLOR_CORRECT = "#2ecc71"  # Зелений
COLOR_WRONG = "#e74c3c"  # Червоний
COLOR_ACCENT = "#3498db"  # Акцентний синій


class ColumnTrainer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Математика в клітинку")
        self.attributes("-fullscreen", True)
        self.configure(bg=COLOR_BG)

        self.score = 0
        self.total = 0
        self.cells = []  # Список об'єктів Entry
        self.target_digits = []  # Правильні цифри для перевірки

        self._setup_ui()
        self._generate_problem()

    def _setup_ui(self):
        # Шапка
        header = tk.Frame(self, bg=COLOR_ACCENT, height=60)
        header.pack(fill="x")

        tk.Label(header, text="📓 Десяткові дроби: Крок за кроком", font=("Segoe UI", 18, "bold"),
                 bg=COLOR_ACCENT, fg="white").pack(side="left", padx=20, pady=10)

        self.lbl_score = tk.Label(header, text="Рахунок: 0/0", font=("Segoe UI", 14),
                                  bg=COLOR_ACCENT, fg="white")
        self.lbl_score.pack(side="right", padx=20)

        # Контейнер для зошита
        self.main_frame = tk.Frame(self, bg=COLOR_BG)
        self.main_frame.pack(expand=True, fill="both")

        # Канвас для малювання клітинок (фон)
        self.canvas = tk.Canvas(self.main_frame, bg=COLOR_BG, highlightthickness=0)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._draw_notebook_grid()

        # Кнопки знизу
        btn_frame = tk.Frame(self, bg=COLOR_BG)
        btn_frame.pack(side="bottom", pady=40)

        tk.Button(btn_frame, text="ПЕРЕВІРИТИ", font=("Segoe UI", 14, "bold"),
                  bg=COLOR_CORRECT, fg="white", relief="flat", padx=30, pady=10,
                  command=self._check_all).pack(side="left", padx=10)

        tk.Button(btn_frame, text="НОВИЙ ПРИКЛАД", font=("Segoe UI", 14),
                  bg=COLOR_ACCENT, fg="white", relief="flat", padx=30, pady=10,
                  command=self._generate_problem).pack(side="left", padx=10)

        tk.Label(self, text="ESC - вихід", bg=COLOR_BG, fg="grey").pack(side="bottom")
        self.bind("<Escape>", lambda e: self.destroy())

    def _draw_notebook_grid(self):
        # Малюємо сітку як у зошиті
        self.update()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        step = 50  # Розмір клітинки
        for x in range(0, w, step):
            self.canvas.create_line(x, 0, x, h, fill=COLOR_GRID)
        for y in range(0, h, step):
            self.canvas.create_line(0, y, w, y, fill=COLOR_GRID)

    def _generate_problem(self):
        # Очищення
        for cell in self.cells:
            cell.destroy()
        self.cells = []
        self.canvas.delete("problem_ui")

        # Генерація чисел
        op = random.choice(["+", "-"])
        n1 = round(random.uniform(10.0, 99.9), random.randint(1, 2))
        n2 = round(random.uniform(1.0, 9.9), random.randint(1, 2))
        if op == "-" and n1 < n2: n1, n2 = n2, n1

        res = n1 + n2 if op == "+" else n1 - n2

        # Перетворення в рядки з вирівнюванням по комі
        s1, s2 = str(n1), str(n2)
        sres = f"{res:.2f}".rstrip('0').rstrip('.')

        # Знаходимо позицію коми
        p1 = s1.find('.')
        p2 = s2.find('.')
        max_before = max(p1, p2)

        # Координати центру
        start_x = self.winfo_screenwidth() // 2
        start_y = 200
        step = 50

        # Малюємо перше число
        self._draw_row(s1, max_before - p1, start_x, start_y)
        # Малюємо друге число
        self._draw_row(s2, max_before - p2, start_x, start_y + step)
        # Знак операції
        self.canvas.create_text(start_x - (max_before + 2) * step, start_y + step / 2,
                                text=op, font=("Consolas", 30, "bold"), fill=COLOR_TEXT, tags="problem_ui")
        # Лінія підкреслення
        self.canvas.create_line(start_x - (max_before + 2) * step, start_y + 1.6 * step,
                                start_x + 2 * step, start_y + 1.6 * step, fill=COLOR_LINE, width=3, tags="problem_ui")

        # Створюємо клітинки для відповіді
        res_str = f"{float(res):.2f}".rstrip('0').rstrip('.')
        pres = res_str.find('.')
        offset_res = max_before - pres

        self.target_digits = list(res_str)
        for i, char in enumerate(res_str):
            x = start_x + (i + offset_res - pres) * step - step / 2
            y = start_y + 2 * step

            if char == '.':
                self.canvas.create_text(x + step / 2, y + step / 2, text=",",
                                        font=("Consolas", 30, "bold"), fill=COLOR_TEXT, tags="problem_ui")
            else:
                entry = tk.Entry(self.main_frame, width=1, font=("Consolas", 26, "bold"),
                                 justify="center", bd=1, relief="flat", bg=COLOR_INPUT)
                entry.place(x=x + 5, y=y + 5, width=40, height=40)
                entry.bind("<KeyRelease>", lambda e, idx=i: self._auto_move(e, idx))
                self.cells.append({'entry': entry, 'correct': char, 'idx': i})

        # Фокус на останню клітинку (рахуємо з кінця)
        if self.cells:
            self.cells[-1]['entry'].focus_set()

    def _draw_row(self, text, offset, sx, sy):
        step = 50
        p = text.find('.')
        for i, char in enumerate(text):
            x = sx + (i + offset - p) * step
            self.canvas.create_text(x, sy + step / 2, text=char if char != '.' else ',',
                                    font=("Consolas", 30, "bold"), fill=COLOR_TEXT, tags="problem_ui")

    def _auto_move(self, event, idx):
        # Якщо введено цифру, рухаємось вліво (тому що рахуємо з кінця)
        if event.char.isdigit():
            # Пошук поточної позиції в списку cells
            current_cell_idx = -1
            for i, c in enumerate(self.cells):
                if c['idx'] == idx:
                    current_cell_idx = i
                    break

            if current_cell_idx > 0:
                self.cells[current_cell_idx - 1]['entry'].focus_set()

    def _check_all(self):
        all_correct = True
        for cell_data in self.cells:
            val = cell_data['entry'].get()
            if val == cell_data['correct']:
                cell_data['entry'].config(bg=COLOR_CORRECT, fg="white")
            else:
                cell_data['entry'].config(bg=COLOR_WRONG, fg="white")
                all_correct = False

        if all_correct:
            self.score += 1
        self.total += 1
        self._update_score_text()

    def _update_score_text(self):
        self.lbl_score.config(text=f"Рахунок: {self.score}/{self.total}")


if __name__ == "__main__":
    app = ColumnTrainer()
    app.mainloop()