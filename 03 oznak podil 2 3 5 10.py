import tkinter as tk
from tkinter import ttk, font
import random


class RulesWindow(tk.Toplevel):
    """Вікно-шпаргалка з правилами подільності"""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Шпаргалка: Ознаки подільності")
        self.geometry("700x550")
        self.configure(bg="#f0f8ff")  # Світло-блакитний фон

        title_font = font.Font(family="Helvetica", size=20, weight="bold")
        rule_font = font.Font(family="Helvetica", size=16)

        tk.Label(self, text="📚 Правила подільності (5 клас)", font=title_font, bg="#f0f8ff", fg="navy").pack(pady=20)

        rules_frame = tk.Frame(self, bg="#f0f8ff")
        rules_frame.pack(fill=tk.BOTH, expand=True, padx=30)

        rules = [
            ("На 2", "Число ділиться на 2, якщо його остання цифра — парна\n(0, 2, 4, 6 або 8).", "#ffe4e1", "darkred"),
            ("На 3",
             "Число ділиться на 3, якщо сума всіх його цифр ділиться на 3.\n(Наприклад: 123 -> 1+2+3=6. 6 ділиться на 3).",
             "#e0ffe0", "darkgreen"),
            ("На 5", "Число ділиться на 5, якщо воно закінчується на 0 або на 5.", "#fffacd", "darkgoldenrod"),
            ("На 10", "Число ділиться на 10, якщо воно закінчується цифрою 0.", "#e6e6fa", "indigo")
        ]

        for title, desc, bg_color, fg_color in rules:
            card = tk.Frame(rules_frame, bg=bg_color, bd=2, relief="groove")
            card.pack(fill=tk.X, pady=10)

            tk.Label(card, text=f"Подільність {title}:", font=font.Font(family="Helvetica", size=18, weight="bold"),
                     bg=bg_color, fg=fg_color).pack(anchor="w", padx=10, pady=(10, 0))
            tk.Label(card, text=desc, font=rule_font, bg=bg_color, justify=tk.LEFT).pack(anchor="w", padx=20,
                                                                                         pady=(5, 10))

        ttk.Button(self, text="Зрозуміло! Закрити", command=self.destroy).pack(pady=20)


class DivisibilityTrainerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Тренажер: Ознаки подільності на 2, 3, 5, 10")
        self.geometry("900x750")
        self.configure(bg="#ffffff")

        # Налаштування шрифтів
        self.font_title = font.Font(family="Helvetica", size=24, weight="bold")
        self.font_number = font.Font(family="Courier", size=60, weight="bold")
        self.font_main = font.Font(family="Helvetica", size=18)
        self.font_feedback = font.Font(family="Helvetica", size=16)

        # Змінні
        self.current_number = 0
        self.score = 0
        self.attempts = 0

        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.BooleanVar()
        self.var_5 = tk.BooleanVar()
        self.var_10 = tk.BooleanVar()

        self._build_ui()
        self.generate_new_task()

    def _build_ui(self):
        # Верхня панель (Заголовок і Рахунок)
        top_frame = tk.Frame(self, bg="#ffffff")
        top_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(top_frame, text="Магічні Ознаки Подільності", font=self.font_title, bg="#ffffff", fg="navy").pack(
            side=tk.LEFT)

        self.score_label = tk.Label(top_frame, text="Рахунок: 0 / 0", font=self.font_main, bg="#ffffff", fg="green")
        self.score_label.pack(side=tk.RIGHT)

        # Панель з числом
        number_frame = tk.Frame(self, bg="#f9f9f9", bd=2, relief="solid")
        number_frame.pack(fill=tk.X, padx=40, pady=20)

        tk.Label(number_frame, text="Досліджуємо число:", font=self.font_main, bg="#f9f9f9", fg="gray").pack(
            pady=(10, 0))
        self.number_label = tk.Label(number_frame, text="0", font=self.font_number, bg="#f9f9f9", fg="#ff4500")
        self.number_label.pack(pady=(0, 10))

        # Запитання і Чекбокси
        question_frame = tk.Frame(self, bg="#ffffff")
        question_frame.pack(fill=tk.X, padx=40, pady=10)

        tk.Label(question_frame, text="Познач галочкою, на що ділиться це число (без остачі):", font=self.font_main,
                 bg="#ffffff").pack()

        self.checkboxes_frame = tk.Frame(question_frame, bg="#ffffff")
        self.checkboxes_frame.pack(pady=15)

        style = ttk.Style()
        style.configure("TCheckbutton", font=font.Font(family="Helvetica", size=20, weight="bold"),
                        background="#ffffff")

        self.cb_2 = ttk.Checkbutton(self.checkboxes_frame, text=" На 2 ", variable=self.var_2, style="TCheckbutton")
        self.cb_3 = ttk.Checkbutton(self.checkboxes_frame, text=" На 3 ", variable=self.var_3, style="TCheckbutton")
        self.cb_5 = ttk.Checkbutton(self.checkboxes_frame, text=" На 5 ", variable=self.var_5, style="TCheckbutton")
        self.cb_10 = ttk.Checkbutton(self.checkboxes_frame, text=" На 10", variable=self.var_10, style="TCheckbutton")

        for cb in [self.cb_2, self.cb_3, self.cb_5, self.cb_10]:
            cb.pack(side=tk.LEFT, padx=20)

        # Кнопки дій
        btn_frame = tk.Frame(self, bg="#ffffff")
        btn_frame.pack(pady=10)

        # Стиль кнопок
        style.configure("Action.TButton", font=self.font_main, padding=10)

        self.btn_check = ttk.Button(btn_frame, text="✔ Перевірити відповідь", command=self.check_answer,
                                    style="Action.TButton")
        self.btn_check.pack(side=tk.LEFT, padx=10)

        self.btn_next = ttk.Button(btn_frame, text="➡ Наступне число", command=self.generate_new_task,
                                   style="Action.TButton")
        self.btn_next.pack(side=tk.LEFT, padx=10)
        self.btn_next.config(state=tk.DISABLED)  # Вимкнено до перевірки

        ttk.Button(btn_frame, text="📖 Правила", command=self.open_rules, style="Action.TButton").pack(side=tk.LEFT,
                                                                                                      padx=10)

        # Область для пояснень (Фідбек)
        self.feedback_frame = tk.LabelFrame(self, text=" Пояснення ", font=self.font_main, bg="#ffffff", fg="navy")
        self.feedback_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        # Створюємо 4 рядки для пояснень кожного правила
        self.feedback_labels = {}
        for div in [2, 3, 5, 10]:
            lbl = tk.Label(self.feedback_frame, text="", font=self.font_feedback, bg="#ffffff", justify=tk.LEFT,
                           anchor="w")
            lbl.pack(fill=tk.X, padx=10, pady=5)
            self.feedback_labels[div] = lbl

        self.main_result_label = tk.Label(self.feedback_frame, text="",
                                          font=font.Font(family="Helvetica", size=18, weight="bold"), bg="#ffffff")
        self.main_result_label.pack(pady=10)

    def open_rules(self):
        RulesWindow(self)

    def generate_new_task(self):
        # Щоб дитині було цікаво, генеруємо числа так, щоб вони часто на щось ділилися
        rand_choice = random.randint(1, 4)
        base = random.randint(11, 999)

        if rand_choice == 1:
            self.current_number = base * 2
        elif rand_choice == 2:
            self.current_number = base * 3
        elif rand_choice == 3:
            self.current_number = base * 5
        else:
            self.current_number = base * 10

        # Іноді даємо зовсім випадкове
        if random.random() > 0.7:
            self.current_number = random.randint(23, 8765)

        self.number_label.config(text=str(self.current_number))

        # Скидання UI
        self.var_2.set(False)
        self.var_3.set(False)
        self.var_5.set(False)
        self.var_10.set(False)

        self.cb_2.state(['!disabled'])
        self.cb_3.state(['!disabled'])
        self.cb_5.state(['!disabled'])
        self.cb_10.state(['!disabled'])

        self.btn_check.config(state=tk.NORMAL)
        self.btn_next.config(state=tk.DISABLED)
        self.main_result_label.config(text="")

        for lbl in self.feedback_labels.values():
            lbl.config(text="")

    def check_answer(self):
        num = self.current_number
        str_num = str(num)
        last_digit = int(str_num[-1])
        sum_digits = sum(int(d) for d in str_num)

        # Справжня ділимість
        is_div_2 = (last_digit in [0, 2, 4, 6, 8])
        is_div_3 = (sum_digits % 3 == 0)
        is_div_5 = (last_digit in [0, 5])
        is_div_10 = (last_digit == 0)

        # Відповіді користувача
        user_2 = self.var_2.get()
        user_3 = self.var_3.get()
        user_5 = self.var_5.get()
        user_10 = self.var_10.get()

        # Перевірка на абсолютну правильність
        all_correct = (is_div_2 == user_2) and (is_div_3 == user_3) and (is_div_5 == user_5) and (is_div_10 == user_10)

        self.attempts += 1
        if all_correct:
            self.score += 1
            self.main_result_label.config(text="🎉 ВІДМІННО! Усі ознаки визначено абсолютно правильно!", fg="green")
        else:
            self.main_result_label.config(text="Ой! Є помилки. Давай розберемося чому 👇", fg="red")

        self.score_label.config(text=f"Рахунок: {self.score} / {self.attempts}")

        # --- Формування детальних наочних пояснень ---

        # Пояснення для 2
        if is_div_2:
            mark = "✅" if user_2 else "❌(ти забув позначити)"
            text = f"{mark} На 2: ОСТАННЯ цифра {last_digit} — парна. Отже, число ДІЛИТЬСЯ на 2."
        else:
            mark = "✅" if not user_2 else "❌(ти позначив зайве)"
            text = f"{mark} На 2: ОСТАННЯ цифра {last_digit} — непарна. Отже, число НЕ ділиться на 2."
        self.feedback_labels[2].config(text=text, fg="darkgreen" if is_div_2 == user_2 else "darkred")

        # Пояснення для 3 (магія з сумою цифр)
        sum_str = " + ".join(list(str_num))
        if is_div_3:
            mark = "✅" if user_3 else "❌(ти забув позначити)"
            text = f"{mark} На 3: Сума цифр ({sum_str} = {sum_digits}). {sum_digits} ділиться на 3. Отже, ДІЛИТЬСЯ на 3."
        else:
            mark = "✅" if not user_3 else "❌(ти позначив зайве)"
            text = f"{mark} На 3: Сума цифр ({sum_str} = {sum_digits}). {sum_digits} не ділиться на 3. Отже, НЕ ділиться на 3."
        self.feedback_labels[3].config(text=text, fg="darkgreen" if is_div_3 == user_3 else "darkred")

        # Пояснення для 5
        if is_div_5:
            mark = "✅" if user_5 else "❌(ти забув позначити)"
            text = f"{mark} На 5: ОСТАННЯ цифра {last_digit}. (0 або 5). Отже, число ДІЛИТЬСЯ на 5."
        else:
            mark = "✅" if not user_5 else "❌(ти позначив зайве)"
            text = f"{mark} На 5: ОСТАННЯ цифра {last_digit} (не 0 і не 5). Отже, число НЕ ділиться на 5."
        self.feedback_labels[5].config(text=text, fg="darkgreen" if is_div_5 == user_5 else "darkred")

        # Пояснення для 10
        if is_div_10:
            mark = "✅" if user_10 else "❌(ти забув позначити)"
            text = f"{mark} На 10: ОСТАННЯ цифра {last_digit}. (Нуль). Отже, число ДІЛИТЬСЯ на 10."
        else:
            mark = "✅" if not user_10 else "❌(ти позначив зайве)"
            text = f"{mark} На 10: ОСТАННЯ цифра {last_digit} (не нуль). Отже, число НЕ ділиться на 10."
        self.feedback_labels[10].config(text=text, fg="darkgreen" if is_div_10 == user_10 else "darkred")

        # Блокуємо чекбокси і кнопку перевірки
        self.cb_2.state(['disabled'])
        self.cb_3.state(['disabled'])
        self.cb_5.state(['disabled'])
        self.cb_10.state(['disabled'])
        self.btn_check.config(state=tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL)


if __name__ == "__main__":
    app = DivisibilityTrainerApp()
    app.mainloop()