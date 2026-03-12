import tkinter as tk
from tkinter import ttk, font
import random


class RulesWindow(tk.Toplevel):
    """Вікно-шпаргалка з визначеннями дільників та кратних"""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Шпаргалка: Кратні та Дільники")
        self.geometry("750x450")
        self.configure(bg="#f0f8ff")

        title_font = font.Font(family="Helvetica", size=20, weight="bold")
        rule_font = font.Font(family="Helvetica", size=16)

        tk.Label(self, text="📚 Дільники чи Кратні? (5 клас)", font=title_font, bg="#f0f8ff", fg="navy").pack(pady=20)

        rules_frame = tk.Frame(self, bg="#f0f8ff")
        rules_frame.pack(fill=tk.BOTH, expand=True, padx=30)

        rules = [
            ("ДІЛЬНИК (менший або рівний)",
             "Число, НА ЯКЕ ділиться задане число без остачі.\n(Наприклад: дільники числа 12 — це 1, 2, 3, 4, 6, 12).",
             "#ffe4e1", "darkred"),
            ("КРАТНЕ (більше або рівне)",
             "Число, ЯКЕ ділиться на задане число без остачі.\n(Наприклад: кратні числу 12 — це 12, 24, 36, 48, 120... їх безліч!).",
             "#e0ffe0", "darkgreen"),
            ("Підказка 💡",
             "Саме число є і своїм дільником, і своїм кратним!\nДля великих чисел використовуй ознаки подільності або діли в стовпчик.",
             "#fffacd", "olive")
        ]

        for title, desc, bg_color, fg_color in rules:
            card = tk.Frame(rules_frame, bg=bg_color, bd=2, relief="groove")
            card.pack(fill=tk.X, pady=10)

            tk.Label(card, text=title, font=font.Font(family="Helvetica", size=18, weight="bold"),
                     bg=bg_color, fg=fg_color).pack(anchor="w", padx=10, pady=(10, 0))
            tk.Label(card, text=desc, font=rule_font, bg=bg_color, justify=tk.LEFT).pack(anchor="w", padx=20,
                                                                                         pady=(5, 10))

        ttk.Button(self, text="Зрозуміло! Закрити", command=self.destroy).pack(pady=10)


class MultiplesTrainerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Тренажер: Знаходження Кратних (Вибір варіантів)")
        self.geometry("900x800")
        self.configure(bg="#ffffff")

        # Шрифти
        self.font_title = font.Font(family="Helvetica", size=24, weight="bold")
        self.font_number = font.Font(family="Courier", size=60, weight="bold")
        self.font_main = font.Font(family="Helvetica", size=18)
        self.font_btn = font.Font(family="Helvetica", size=20, weight="bold")

        # Змінні
        self.current_number = 0
        self.options = []  # Усі згенеровані варіанти на екрані
        self.correct_multiples = set()  # Ті з них, що реально є кратними
        self.selected_options = set()  # Ті, що вибрав користувач

        self.score = 0
        self.attempts = 0

        self.option_buttons = {}  # Словник для зберігання кнопок (щоб міняти їх колір)

        self._build_ui()
        self.generate_new_task()

    def _build_ui(self):
        # Верхня панель
        top_frame = tk.Frame(self, bg="#ffffff")
        top_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(top_frame, text="Мисливець за Кратними 🎯", font=self.font_title, bg="#ffffff", fg="navy").pack(
            side=tk.LEFT)
        self.score_label = tk.Label(top_frame, text="Рахунок: 0 / 0", font=self.font_main, bg="#ffffff", fg="green")
        self.score_label.pack(side=tk.RIGHT)

        # Панель з поточним числом
        number_frame = tk.Frame(self, bg="#f9f9f9", bd=2, relief="solid")
        number_frame.pack(fill=tk.X, padx=40, pady=10)

        tk.Label(number_frame, text="Вибери ВСІ числа, які є КРАТНИМИ числу:", font=self.font_main, bg="#f9f9f9",
                 fg="gray").pack(
            pady=(10, 0))
        self.number_label = tk.Label(number_frame, text="0", font=self.font_number, bg="#f9f9f9", fg="#ff4500")
        self.number_label.pack(pady=(0, 10))

        # === ПАНЕЛЬ З ВАРІАНТАМИ (СІТКА КНОПОК) ===
        self.options_container = tk.Frame(self, bg="#ffffff")
        self.options_container.pack(pady=20)

        # Кнопки дій
        btn_frame = tk.Frame(self, bg="#ffffff")
        btn_frame.pack(pady=20)

        style = ttk.Style()
        style.configure("Action.TButton", font=self.font_main, padding=10)

        self.btn_check = ttk.Button(btn_frame, text="✔ Перевірити", command=self.check_answer,
                                    style="Action.TButton")
        self.btn_check.pack(side=tk.LEFT, padx=10)

        self.btn_next = ttk.Button(btn_frame, text="➡ Наступне число", command=self.generate_new_task,
                                   style="Action.TButton")
        self.btn_next.pack(side=tk.LEFT, padx=10)
        self.btn_next.config(state=tk.DISABLED)

        ttk.Button(btn_frame, text="📖 Правила", command=self.open_rules, style="Action.TButton").pack(side=tk.LEFT,
                                                                                                      padx=10)

        # Зворотний зв'язок
        self.feedback_label = tk.Label(self, text="", font=font.Font(family="Helvetica", size=16, weight="bold"),
                                       bg="#ffffff", wraplength=800, justify=tk.CENTER)
        self.feedback_label.pack(pady=10)

    def open_rules(self):
        RulesWindow(self)

    def generate_options(self, n):
        """Розумна генерація варіантів (пастки + правильні відповіді)"""
        opts = set()

        # 1. Саме число (завжди є кратним)
        opts.add(n)

        # 2. Декілька дрібних правильних кратних
        opts.add(n * random.randint(2, 5))
        opts.add(n * random.randint(6, 9))

        # 3. Одне ДУЖЕ велике правильне кратне (для перевірки в стовпчик / ознак)
        opts.add(n * random.randint(20, 100))

        # 4. Пастки: Дільники числа (якщо є)
        divisors = [i for i in range(1, n) if n % i == 0]
        if divisors:
            opts.add(random.choice(divisors))
            if len(divisors) > 1:
                opts.add(random.choice(divisors))

        # 5. Пастка: Дуже велике число, яке НЕ ділиться (залишок)
        large_trap = n * random.randint(20, 100) + random.randint(1, n - 1)
        opts.add(large_trap)

        # 6. Заповнюємо решту випадковими числами (не кратними), щоб було рівно 12 варіантів
        while len(opts) < 12:
            rand_val = random.randint(2, n * 15)
            if rand_val % n != 0 and rand_val not in opts:
                opts.add(rand_val)

        return list(opts)

    def generate_new_task(self):
        # Очищення попереднього стану
        self.selected_options.clear()
        self.correct_multiples.clear()
        self.feedback_label.config(text="")

        for widget in self.options_container.winfo_children():
            widget.destroy()
        self.option_buttons.clear()

        # Генеруємо нове число (від 3 до 25)
        self.current_number = random.randint(3, 25)
        self.number_label.config(text=str(self.current_number))

        # Генеруємо варіанти і перемішуємо їх
        self.options = self.generate_options(self.current_number)
        random.shuffle(self.options)

        # Визначаємо, які з них реально є кратними
        self.correct_multiples = {x for x in self.options if x % self.current_number == 0}

        # Малюємо сітку кнопок (3 рядки по 4 кнопки)
        for i, val in enumerate(self.options):
            row = i // 4
            col = i % 4

            btn = tk.Button(self.options_container, text=str(val), font=self.font_btn,
                            width=6, height=2, bg="#e1f5fe", activebackground="#b3e5fc",
                            relief="raised", bd=4, command=lambda v=val: self.toggle_option(v))
            btn.grid(row=row, column=col, padx=15, pady=15)
            self.option_buttons[val] = btn

        # Управління кнопками
        self.btn_check.config(state=tk.NORMAL)
        self.btn_next.config(state=tk.DISABLED)

    def toggle_option(self, val):
        """Вибір або скасування вибору варіанта"""
        if val in self.selected_options:
            self.selected_options.remove(val)
            self.option_buttons[val].config(bg="#e1f5fe", relief="raised")  # Повертаємо стандартний колір
        else:
            self.selected_options.add(val)
            self.option_buttons[val].config(bg="#ffd54f", relief="sunken")  # Золотий колір для обраного

    def check_answer(self):
        if not self.selected_options:
            self.feedback_label.config(
                text="Ти не вибрав жодного числа! Натисни на ті, що діляться на " + str(self.current_number), fg="red")
            return

        missing = self.correct_multiples - self.selected_options
        extra = self.selected_options - self.correct_multiples

        # Аналіз помилок (якщо обрали зайві)
        if extra:
            # Перевіряємо, чи не обрали випадково дільник
            divisors_chosen = [x for x in extra if self.current_number % x == 0 and x != self.current_number]
            if divisors_chosen:
                divs_str = ", ".join(map(str, divisors_chosen))
                self.feedback_label.config(
                    text=f"❌ ОБЕРЕЖНО! Числа {divs_str} — це ДІЛЬНИКИ, а не кратні!\nКратне має бути більшим або рівним {self.current_number}. Зніми з них виділення.",
                    fg="red")
                return

            # Звичайна помилка
            extra_str = ", ".join(map(str, extra))
            self.feedback_label.config(
                text=f"❌ Помилка! Числа {extra_str} НЕ діляться на {self.current_number} без остачі.\nПеревір їх ще раз (можливо, діленням у стовпчик).",
                fg="red")
            return

        # Аналіз помилок (якщо не обрали всі правильні)
        if missing:
            has_large_missing = any(x > self.current_number * 10 for x in missing)
            if self.current_number in missing:
                self.feedback_label.config(
                    text=f"🤔 Ти забув найпростіше кратне! Саме число {self.current_number} ділиться на себе.",
                    fg="darkorange")
            elif has_large_missing:
                self.feedback_label.config(
                    text=f"🤔 Майже правильно, але ти пропустив великі числа!\nВикористай ознаки подільності або поділи у стовпчик.",
                    fg="darkorange")
            else:
                self.feedback_label.config(
                    text=f"🤔 Ти знайшов не всі кратні! Залишилося ще {len(missing)} шт. Шукай уважніше.",
                    fg="darkorange")
            return

        # Якщо все правильно
        self.attempts += 1
        self.score += 1

        self.feedback_label.config(
            text=f"🎉 ВІДМІННО! Ти знайшов усі {len(self.correct_multiples)} кратних числу {self.current_number} серед запропонованих!",
            fg="green")

        # Підсвічуємо правильні відповіді зеленим
        for val in self.correct_multiples:
            self.option_buttons[val].config(bg="#81c784", fg="white")

        # Блокуємо UI після успіху
        self.btn_check.config(state=tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL)

        for btn in self.option_buttons.values():
            btn.config(state=tk.DISABLED)

        self.score_label.config(text=f"Рахунок: {self.score} / {self.attempts}")


if __name__ == "__main__":
    app = MultiplesTrainerApp()
    app.mainloop()