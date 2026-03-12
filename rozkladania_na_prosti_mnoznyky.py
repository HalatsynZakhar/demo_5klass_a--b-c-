import tkinter as tk
from tkinter import ttk, font
import random


class FactorizationRulesWindow(tk.Toplevel):
    """Шпаргалка: Як розкладати число на прості множники"""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Шпаргалка: Розкладання у стовпчик")
        self.geometry("750x550")
        self.configure(bg="#f0f8ff")

        title_font = font.Font(family="Helvetica", size=20, weight="bold")
        rule_font = font.Font(family="Helvetica", size=16)

        tk.Label(self, text="📚 Алгоритм розкладання (6 клас)", font=title_font, bg="#f0f8ff", fg="navy").pack(pady=20)

        rules_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="groove")
        rules_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        instructions = (
            "1. Запиши число і проведи вертикальну лінію.\n\n"
            "2. Знайди будь-яке просте число, на яке воно ділиться без остачі (найкраще починати з найменшого: 2, 3, 5).\n\n"
            "3. Запиши цей дільник праворуч від лінії.\n\n"
            "4. Поділи число на дільник, а результат запиши ліворуч під початковим числом.\n\n"
            "5. Повторюй це з новим числом, поки зліва не отримаєш 1.\n\n"
            "6. Запиши відповідь у вигляді добутку (бажано від меншого до більшого)."
        )

        tk.Label(rules_frame, text=instructions, font=rule_font, bg="#ffffff", fg="#333333", justify=tk.LEFT,
                 wraplength=650).pack(padx=20, pady=20, anchor="w")

        example_frame = tk.Frame(rules_frame, bg="#e0ffe0", bd=1, relief="solid")
        example_frame.pack(pady=10, padx=20, fill=tk.X)
        tk.Label(example_frame, text="Приклад: 60 = 2 × 2 × 3 × 5",
                 font=font.Font(family="Courier", size=18, weight="bold"), bg="#e0ffe0", fg="darkgreen").pack(pady=10)

        ttk.Button(self, text="Зрозуміло! Закрити", command=self.destroy).pack(pady=10)


class PrimeFactorizationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Тренажер: Розкладання на прості множники (2 рівні)")
        self.geometry("1000x900")
        self.configure(bg="#ffffff")

        # Шрифти
        self.font_title = font.Font(family="Helvetica", size=22, weight="bold")
        self.font_column = font.Font(family="Courier", size=28, weight="bold")
        self.font_main = font.Font(family="Helvetica", size=16)
        self.font_btn = font.Font(family="Helvetica", size=16, weight="bold")
        self.font_numpad = font.Font(family="Helvetica", size=18, weight="bold")

        # Змінні стану
        self.start_number = 0
        self.current_number = 0
        self.expected_quotient = 0
        self.factors = []
        self.column_rows = []  # Зберігаємо віджети рядків

        self.level_var = tk.IntVar(value=1)  # 1 - Авто, 2 - Вручну
        self.state = "pick_prime"  # "pick_prime" або "enter_quotient"
        self.numpad_input = ""

        self.primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

        self._build_ui()
        self.generate_new_task()

    def _build_ui(self):
        # --- Верхня панель (Налаштування та заголовок) ---
        top_frame = tk.Frame(self, bg="#ffffff")
        top_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(top_frame, text="Майстер Стовпчиків 🧮", font=self.font_title, bg="#ffffff", fg="navy").pack(
            side=tk.LEFT)

        level_frame = tk.LabelFrame(top_frame, text=" Рівень складності ", font=font.Font(family="Helvetica", size=12),
                                    bg="#ffffff")
        level_frame.pack(side=tk.LEFT, padx=30)

        ttk.Radiobutton(level_frame, text="1. Ділить комп'ютер", variable=self.level_var, value=1,
                        command=self.generate_new_task).pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Radiobutton(level_frame, text="2. Ділю самостійно", variable=self.level_var, value=2,
                        command=self.generate_new_task).pack(side=tk.LEFT, padx=10, pady=5)

        ttk.Button(top_frame, text="📖 Правила", command=self.open_rules).pack(side=tk.RIGHT, padx=10)

        # --- Основна робоча область ---
        main_workspace = tk.Frame(self, bg="#ffffff")
        main_workspace.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        # Ліва частина (Стовпчик)
        self.column_container = tk.LabelFrame(main_workspace, text=" Твій зошит ", font=self.font_main, bg="#f9f9f9",
                                              fg="gray", width=350)
        self.column_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.column_container.pack_propagate(False)

        self.column_frame = tk.Frame(self.column_container, bg="#f9f9f9")
        self.column_frame.pack(pady=20)

        # Права частина (Клавіатури)
        controls_container = tk.Frame(main_workspace, bg="#ffffff", width=450)
        controls_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- 1. Клавіатура простих чисел ---
        self.lbl_prime_hint = tk.Label(controls_container, text="1. Обери простий дільник:", font=self.font_main,
                                       bg="#ffffff", fg="navy")
        self.lbl_prime_hint.pack(pady=(10, 5))

        self.keyboard_frame = tk.Frame(controls_container, bg="#ffffff")
        self.keyboard_frame.pack()

        self.prime_buttons = []
        for i, prime in enumerate(self.primes):
            row = i // 5
            col = i % 5
            btn = tk.Button(self.keyboard_frame, text=str(prime), font=self.font_btn, width=4, height=1,
                            bg="#e1f5fe", activebackground="#b3e5fc", relief="raised", bd=3,
                            command=lambda p=prime: self.process_divisor(p))
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.prime_buttons.append(btn)

        # --- 2. Цифрова клавіатура (Numpad) для введення частки ---
        self.numpad_container = tk.Frame(controls_container, bg="#ffffff")
        self.numpad_container.pack(pady=(20, 0))

        self.lbl_numpad_hint = tk.Label(self.numpad_container, text="2. Введи результат ділення:", font=self.font_main,
                                        bg="#ffffff", fg="gray")
        self.lbl_numpad_hint.pack(pady=(0, 5))

        numpad_frame = tk.Frame(self.numpad_container, bg="#ffffff")
        numpad_frame.pack()

        numpad_layout = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
            ('C', 3, 0), ('0', 3, 1), ('OK', 3, 2)
        ]

        self.numpad_buttons = []
        for (text, row, col) in numpad_layout:
            if text == 'C':
                btn = tk.Button(numpad_frame, text=text, font=self.font_numpad, bg="#ffcdd2",
                                activebackground="#ef9a9a",
                                width=5, height=1, relief="raised", bd=3, command=self.numpad_clear)
            elif text == 'OK':
                btn = tk.Button(numpad_frame, text="✔", font=self.font_numpad, bg="#c8e6c9", activebackground="#a5d6a7",
                                width=5, height=1, relief="raised", bd=3, command=self.numpad_ok)
            else:
                btn = tk.Button(numpad_frame, text=text, font=self.font_numpad, bg="#f5f5f5",
                                activebackground="#e0e0e0",
                                width=5, height=1, relief="raised", bd=3, command=lambda t=text: self.numpad_press(t))
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.numpad_buttons.append(btn)

        # --- Панель результатів та підказок ---
        bottom_frame = tk.Frame(self, bg="#ffffff")
        bottom_frame.pack(fill=tk.X, padx=20, pady=10)

        self.feedback_label = tk.Label(bottom_frame, text="",
                                       font=font.Font(family="Helvetica", size=16, weight="bold"), bg="#ffffff",
                                       wraplength=800)
        self.feedback_label.pack(pady=5)

        self.result_label = tk.Label(bottom_frame, text="", font=font.Font(family="Courier", size=22, weight="bold"),
                                     bg="#ffffff", fg="darkgreen")
        self.result_label.pack(pady=5)

        self.btn_next = ttk.Button(bottom_frame, text="➡ Наступне число", command=self.generate_new_task)
        self.btn_next.pack(pady=10)

    def open_rules(self):
        FactorizationRulesWindow(self)

    def generate_new_task(self):
        # Генерація числа (від 3 до 5 множників)
        num = 1
        num_factors = random.randint(3, 5)
        available_primes = [2, 2, 2, 3, 3, 5, 5, 7, 11]
        for _ in range(num_factors):
            num *= random.choice(available_primes)

        if num < 12: num *= random.choice([2, 3])
        if num > 999: num = random.randint(40, 200)

        self.start_number = num
        self.current_number = num
        self.factors.clear()
        self.column_rows.clear()
        self.numpad_input = ""

        # Очищення UI
        for widget in self.column_frame.winfo_children():
            widget.destroy()

        self.result_label.config(text="")
        self.btn_next.config(state=tk.DISABLED)

        # Малюємо перший рядок (Число | ?)
        self.add_row(self.current_number, "?", is_active=True)

        self.set_state_pick_prime()
        self.feedback_label.config(text=f"Починаємо! Знайди будь-який простий дільник для {self.start_number}.",
                                   fg="navy")

    def add_row(self, left_val, right_val, is_active=False):
        """Додає новий рядок у візуальний стовпчик і зберігає посилання на нього"""
        row_idx = len(self.column_rows)
        fg_left = "#ff4500" if is_active else "black"
        fg_right = "blue" if right_val not in ("?", "") else "gray"

        lbl_left = tk.Label(self.column_frame, text=str(left_val), font=self.font_column, bg="#f9f9f9", fg=fg_left,
                            width=5, anchor="e")
        lbl_left.grid(row=row_idx, column=0, padx=(10, 5), pady=2)

        line = tk.Frame(self.column_frame, bg="black", width=3, height=40)
        line.grid(row=row_idx, column=1, sticky="ns", pady=0)

        lbl_right = tk.Label(self.column_frame, text=str(right_val), font=self.font_column, bg="#f9f9f9", fg=fg_right,
                             width=4, anchor="w")
        lbl_right.grid(row=row_idx, column=2, padx=(5, 10), pady=2)

        self.column_rows.append({'left': lbl_left, 'right': lbl_right})

    # === КЕРУВАННЯ СТАНАМИ ===
    def set_state_pick_prime(self):
        self.state = "pick_prime"
        # Вмикаємо прості числа
        self.lbl_prime_hint.config(fg="navy")
        for btn in self.prime_buttons:
            btn.config(state=tk.NORMAL)
        # Вимикаємо Numpad
        self.lbl_numpad_hint.config(fg="gray")
        for btn in self.numpad_buttons:
            btn.config(state=tk.DISABLED)

    def set_state_enter_quotient(self):
        self.state = "enter_quotient"
        self.numpad_input = ""
        # Вимикаємо прості числа
        self.lbl_prime_hint.config(fg="gray")
        for btn in self.prime_buttons:
            btn.config(state=tk.DISABLED)
        # Вмикаємо Numpad
        self.lbl_numpad_hint.config(fg="navy")
        for btn in self.numpad_buttons:
            btn.config(state=tk.NORMAL)

    def disable_all_inputs(self):
        self.state = "done"
        for btn in self.prime_buttons + self.numpad_buttons:
            btn.config(state=tk.DISABLED)

    # === ЛОГІКА ДІЛЕННЯ ===
    def process_divisor(self, selected_prime):
        if self.state != "pick_prime": return

        # Перевірка: чи ділиться?
        if self.current_number % selected_prime != 0:
            self.feedback_label.config(
                text=f"❌ Помилка! Число {self.current_number} не ділиться на {selected_prime} без остачі.", fg="red")
            return

        # Дільник підходить (навіть якщо не найменший!)
        self.factors.append(selected_prime)

        # Оновлюємо поточний рядок: міняємо "?" на вибраний дільник
        self.column_rows[-1]['right'].config(text=str(selected_prime), fg="blue")
        self.column_rows[-1]['left'].config(fg="black")  # Знімаємо активний колір

        if self.level_var.get() == 1:
            # РІВЕНЬ 1: АВТОМАТИЧНО
            self.current_number //= selected_prime

            if self.current_number == 1:
                self.add_row(1, "", is_active=False)
                self.win_state()
            else:
                self.add_row(self.current_number, "?", is_active=True)
                self.feedback_label.config(text=f"✅ Добре! Ділимо далі число {self.current_number}.", fg="green")
        else:
            # РІВЕНЬ 2: ВРУЧНУ
            self.expected_quotient = self.current_number // selected_prime
            self.add_row("?", "", is_active=True)  # Новий порожній рядок для введення
            self.set_state_enter_quotient()
            self.feedback_label.config(
                text=f"✅ Дільник {selected_prime} підходить. Тепер поділи і введи результат праворуч знизу.",
                fg="darkorange")

    # === ЛОГІКА NUMPAD (Рівень 2) ===
    def numpad_press(self, digit):
        if self.state != "enter_quotient": return
        if len(self.numpad_input) < 4:
            self.numpad_input += digit
            self.column_rows[-1]['left'].config(text=self.numpad_input)

    def numpad_clear(self):
        if self.state != "enter_quotient": return
        self.numpad_input = ""
        self.column_rows[-1]['left'].config(text="?")

    def numpad_ok(self):
        if self.state != "enter_quotient": return
        if not self.numpad_input: return

        user_val = int(self.numpad_input)

        if user_val == self.expected_quotient:
            self.current_number = user_val

            if self.current_number == 1:
                self.column_rows[-1]['left'].config(text="1", fg="black")
                self.win_state()
            else:
                self.column_rows[-1]['left'].config(text=str(self.current_number))
                self.column_rows[-1]['right'].config(text="?", fg="gray")
                self.set_state_pick_prime()
                self.feedback_label.config(text=f"✅ Правильно поділив! Тепер шукай дільник для {self.current_number}.",
                                           fg="green")
        else:
            self.feedback_label.config(text=f"❌ Неправильно! Спробуй поділити ще раз.", fg="red")
            self.numpad_clear()

    # === ПЕРЕМОГА ===
    def win_state(self):
        # Оскільки учні могли шукати множники в довільному порядку,
        # у фінальній відповіді розставляємо їх від меншого до більшого (канонічний вигляд)
        sorted_factors = sorted(self.factors)
        factors_str = " × ".join(map(str, sorted_factors))

        msg = "🎉 ВІДМІННО! Ти повністю розклав число!"
        if self.factors != sorted_factors:
            msg += "\n(Записуємо множники у порядку зростання 📊)"

        self.feedback_label.config(text=msg, fg="green")
        self.result_label.config(text=f"{self.start_number} = {factors_str}")

        self.disable_all_inputs()
        self.btn_next.config(state=tk.NORMAL)


if __name__ == "__main__":
    app = PrimeFactorizationApp()
    app.mainloop()