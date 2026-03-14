import tkinter as tk
from tkinter import ttk, font
import random
import math
import re


class RulesWindow(tk.Toplevel):
    """Вікно-шпаргалка з визначеннями простих і складених чисел"""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Шпаргалка: Прості та складені числа")
        self.geometry("750x450")
        self.configure(bg="#f0f8ff")

        title_font = font.Font(family="Helvetica", size=20, weight="bold")
        rule_font = font.Font(family="Helvetica", size=16)

        tk.Label(self, text="📚 Які бувають числа? (5 клас)", font=title_font, bg="#f0f8ff", fg="navy").pack(pady=20)

        rules_frame = tk.Frame(self, bg="#f0f8ff")
        rules_frame.pack(fill=tk.BOTH, expand=True, padx=30)

        rules = [
            ("Просте число", "Має рівно ДВА дільники: 1 та саме це число.\n(Наприклад: 2, 3, 5, 7, 11, 13...)",
             "#e0ffe0", "darkgreen"),
            ("Складене число", "Має БІЛЬШЕ ніж два дільники.\n(Наприклад: 4 ділиться на 1, 2, 4. У нього 3 дільники).",
             "#ffe4e1", "darkred"),
            ("Особливе число 1",
             "Одиниця має лише ОДИН дільник (саму себе).\nТому число 1 не є ані простим, ані складеним!", "#e6e6fa",
             "indigo")
        ]

        for title, desc, bg_color, fg_color in rules:
            card = tk.Frame(rules_frame, bg=bg_color, bd=2, relief="groove")
            card.pack(fill=tk.X, pady=10)

            tk.Label(card, text=title, font=font.Font(family="Helvetica", size=18, weight="bold"),
                     bg=bg_color, fg=fg_color).pack(anchor="w", padx=10, pady=(10, 0))
            tk.Label(card, text=desc, font=rule_font, bg=bg_color, justify=tk.LEFT).pack(anchor="w", padx=20,
                                                                                         pady=(5, 10))

        ttk.Button(self, text="Зрозуміло! Закрити", command=self.destroy).pack(pady=10)


class PrimeCompositeTrainerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Тренажер: Прості та складені числа (Для інтерактивної дошки)")
        self.geometry("900x950")  # Збільшено висоту для віртуальної клавіатури
        self.configure(bg="#ffffff")

        # Шрифти
        self.font_title = font.Font(family="Helvetica", size=24, weight="bold")
        self.font_number = font.Font(family="Courier", size=50, weight="bold")
        self.font_main = font.Font(family="Helvetica", size=18)
        self.font_bubbles = font.Font(family="Helvetica", size=16, weight="bold")
        self.font_numpad = font.Font(family="Helvetica", size=22, weight="bold")

        # Змінні
        self.current_number = 0
        self.correct_divisors = set()
        self.user_divisors = set()

        self.score = 0
        self.attempts = 0
        self.choice_var = tk.StringVar(value="")
        self.current_input_var = tk.StringVar(value="")

        self._build_ui()
        self.generate_new_task()

    def _build_ui(self):
        # Верхня панель
        top_frame = tk.Frame(self, bg="#ffffff")
        top_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(top_frame, text="Детектив чисел", font=self.font_title, bg="#ffffff", fg="navy").pack(
            side=tk.LEFT)
        self.score_label = tk.Label(top_frame, text="Рахунок: 0 / 0", font=self.font_main, bg="#ffffff", fg="green")
        self.score_label.pack(side=tk.RIGHT)

        # Панель з поточним числом
        number_frame = tk.Frame(self, bg="#f9f9f9", bd=2, relief="solid")
        number_frame.pack(fill=tk.X, padx=40, pady=10)

        tk.Label(number_frame, text="Знайди всі дільники числа:", font=self.font_main, bg="#f9f9f9", fg="gray").pack(
            pady=(10, 0))
        self.number_label = tk.Label(number_frame, text="0", font=self.font_number, bg="#f9f9f9", fg="#ff4500")
        self.number_label.pack(pady=(0, 10))

        # === ВІРТУАЛЬНА КЛАВІАТУРА (NUMPAD) ===
        numpad_container = tk.Frame(self, bg="#ffffff")
        numpad_container.pack(pady=10)

        # Екранчик для введення
        display_frame = tk.Frame(numpad_container, bg="#ffffff")
        display_frame.pack(pady=(0, 10))

        tk.Label(display_frame, text="Введення:", font=self.font_main, bg="#ffffff").pack(side=tk.LEFT, padx=10)
        self.input_lbl = tk.Label(display_frame, textvariable=self.current_input_var, font=self.font_number,
                                  width=5, bg="#eeeeee", relief="sunken", fg="navy")
        self.input_lbl.pack(side=tk.LEFT, padx=10)

        # Кнопки клавіатури
        numpad_frame = tk.Frame(numpad_container, bg="#ffffff")
        numpad_frame.pack()

        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('C', 3, 0), ('0', 3, 1), ('➕', 3, 2)
        ]

        self.numpad_buttons = []

        for (text, row, col) in buttons:
            if text == 'C':
                btn = tk.Button(numpad_frame, text=text, font=self.font_numpad, bg="#ffcdd2",
                                activebackground="#ef9a9a",
                                width=6, height=1, relief="raised", bd=3, command=self.clear_input)
            elif text == '➕':
                btn = tk.Button(numpad_frame, text=text, font=self.font_numpad, bg="#c8e6c9",
                                activebackground="#a5d6a7",
                                width=6, height=1, relief="raised", bd=3, command=self.add_divisor_from_numpad)
            else:
                btn = tk.Button(numpad_frame, text=text, font=self.font_numpad, bg="#e1f5fe",
                                activebackground="#b3e5fc",
                                width=6, height=1, relief="raised", bd=3, command=lambda t=text: self.press_digit(t))

            btn.grid(row=row, column=col, padx=8, pady=8)
            self.numpad_buttons.append(btn)
        # =======================================

        # Панель відображення бульбашок (знайдених дільників)
        self.bubbles_container = tk.LabelFrame(self, text=" Твої дільники ", font=self.font_main, bg="#f0f8ff",
                                               fg="navy")
        self.bubbles_container.pack(fill=tk.X, padx=40, pady=10, ipady=10)

        self.bubbles_inner_frame = tk.Frame(self.bubbles_container, bg="#f0f8ff")
        self.bubbles_inner_frame.pack(pady=5, padx=10)

        # Блок висновку (класифікація)
        choice_frame = tk.LabelFrame(self, text=" Зроби висновок ", font=self.font_main, bg="#ffffff", fg="navy")
        choice_frame.pack(fill=tk.X, padx=40, pady=5)

        style = ttk.Style()
        style.configure("TRadiobutton", font=self.font_main, background="#ffffff")

        ttk.Radiobutton(choice_frame, text="Це ПРОСТЕ число", variable=self.choice_var, value="prime").pack(
            side=tk.LEFT, padx=20, pady=10)
        ttk.Radiobutton(choice_frame, text="Це СКЛАДЕНЕ число", variable=self.choice_var, value="composite").pack(
            side=tk.LEFT, padx=20, pady=10)
        ttk.Radiobutton(choice_frame, text="Ні те, ні інше (це 1)", variable=self.choice_var, value="one").pack(
            side=tk.LEFT, padx=20, pady=10)

        # Кнопки дій
        btn_frame = tk.Frame(self, bg="#ffffff")
        btn_frame.pack(pady=10)

        style.configure("Action.TButton", font=self.font_main, padding=10)

        self.btn_check = ttk.Button(btn_frame, text="✔ Перевірити все", command=self.check_answer,
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
        self.feedback_label.pack(pady=5)

    def open_rules(self):
        RulesWindow(self)

    def _get_divisors(self, n):
        divisors = set()
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                divisors.add(i)
                divisors.add(n // i)
        return divisors

    def generate_new_task(self):
        r = random.random()
        if r < 0.05:
            self.current_number = 1
        elif r < 0.4:
            primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
            self.current_number = random.choice(primes)
        else:
            composites = [x for x in range(4, 51) if len(self._get_divisors(x)) > 2]
            self.current_number = random.choice(composites)

        self.correct_divisors = self._get_divisors(self.current_number)
        self.user_divisors.clear()

        # Скидання UI
        self.number_label.config(text=str(self.current_number))
        self.current_input_var.set("")
        self.choice_var.set("")
        self.feedback_label.config(text="")

        self.btn_check.config(state=tk.NORMAL)
        self.btn_next.config(state=tk.DISABLED)

        # Увімкнути віртуальну клавіатуру
        for btn in self.numpad_buttons:
            btn.config(state=tk.NORMAL)

        self.update_bubbles_ui()

    # --- Функції для віртуальної клавіатури ---
    def press_digit(self, digit):
        current = self.current_input_var.get()
        # Обмежуємо довжину 3 символами (бо числа до 50)
        if len(current) < 3:
            if current == "0":
                self.current_input_var.set(digit)
            else:
                self.current_input_var.set(current + digit)

    def clear_input(self):
        self.current_input_var.set("")

    def add_divisor_from_numpad(self):
        val_str = self.current_input_var.get()
        if not val_str:
            return

        val = int(val_str)
        if val == 0:
            self.feedback_label.config(text="На нуль ділити не можна!", fg="red")
            self.current_input_var.set("")
            return

        if val not in self.user_divisors:
            self.user_divisors.add(val)
            self.update_bubbles_ui()
            self.feedback_label.config(text=f"Дільник {val} додано. Продовжуй!", fg="gray")
        else:
            self.feedback_label.config(text=f"Число {val} вже додано!", fg="orange")

        self.current_input_var.set("")  # Очищаємо екранчик після додавання

    # ------------------------------------------

    def remove_divisor(self, val):
        if val in self.user_divisors:
            self.user_divisors.remove(val)
            self.update_bubbles_ui()
            self.feedback_label.config(text=f"Число {val} видалено.", fg="gray")

    def update_bubbles_ui(self):
        for widget in self.bubbles_inner_frame.winfo_children():
            widget.destroy()

        if not self.user_divisors:
            tk.Label(self.bubbles_inner_frame, text="Поки що тут порожньо...", font=self.font_main, bg="#f0f8ff",
                     fg="gray").pack()
            return

        sorted_divs = sorted(list(self.user_divisors))

        for val in sorted_divs:
            bubble = tk.Button(self.bubbles_inner_frame, text=str(val), font=self.font_bubbles,
                               bg="deepskyblue", fg="white", activebackground="red", relief="raised", bd=3,
                               command=lambda v=val: self.remove_divisor(v))
            bubble.pack(side=tk.LEFT, padx=5, pady=5)

    def check_answer(self):
        if not self.user_divisors:
            self.feedback_label.config(text="Ти ще не додав жодного дільника!", fg="red")
            return

        if not self.choice_var.get():
            self.feedback_label.config(text="Будь ласка, обери висновок (знизу): яке це число (просте чи складене)?",
                                       fg="red")
            return

        missing = self.correct_divisors - self.user_divisors
        extra = self.user_divisors - self.correct_divisors

        if extra:
            extra_str = ", ".join(map(str, sorted(extra)))
            self.feedback_label.config(
                text=f"❌ Помилка! Числа {extra_str} НЕ ділять {self.current_number} без остачі.\nНатисни на них (бульбашки), щоб видалити.",
                fg="red")
            return

        if missing:
            self.feedback_label.config(
                text=f"🤔 Ти знайшов правильні дільники, але НЕ ВСІ!\nЗалишилося знайти ще {len(missing)} шт. Подумай ще.",
                fg="darkorange")
            return

        num = self.current_number
        is_prime = (len(self.correct_divisors) == 2)
        is_one = (num == 1)

        user_choice = self.choice_var.get()

        correct_choice = ""
        if is_one:
            correct_choice = "one"
        elif is_prime:
            correct_choice = "prime"
        else:
            correct_choice = "composite"

        self.attempts += 1

        if user_choice == correct_choice:
            self.score += 1
            if is_one:
                msg = f"🎉 ВІДМІННО! У числа {num} лише 1 дільник. Воно ані просте, ані складене."
            elif is_prime:
                msg = f"🎉 ВІДМІННО! У числа {num} рівно 2 дільники (1 і {num}). Це ПРОСТЕ число!"
            else:
                msg = f"🎉 ВІДМІННО! У числа {num} аж {len(self.correct_divisors)} дільників (більше двох). Це СКЛАДЕНЕ число!"

            self.feedback_label.config(text=msg, fg="green")

            # Блокуємо UI після успіху
            self.btn_check.config(state=tk.DISABLED)
            self.btn_next.config(state=tk.NORMAL)

            # Вимикаємо клавіатуру
            for btn in self.numpad_buttons:
                btn.config(state=tk.DISABLED)

            # Вимикаємо кнопки-бульбашки
            for widget in self.bubbles_inner_frame.winfo_children():
                widget.config(state=tk.DISABLED)

        else:
            if correct_choice == "prime":
                msg = f"❌ Дільники знайдені ідеально (їх рівно два: 1 та {num}).\nАле за правилом таке число називається ПРОСТИМ!"
            elif correct_choice == "composite":
                msg = f"❌ Дільники знайдені ідеально (їх {len(self.correct_divisors)}, тобто більше двох).\nЗначить число має бути СКЛАДЕНИМ!"
            else:
                msg = f"❌ Дільники знайдені вірно. Але 1 — це виняток, воно не є ні простим, ні складеним!"

            self.feedback_label.config(text=msg, fg="red")

        self.score_label.config(text=f"Рахунок: {self.score} / {self.attempts}")


if __name__ == "__main__":
    app = PrimeCompositeTrainerApp()
    app.mainloop()