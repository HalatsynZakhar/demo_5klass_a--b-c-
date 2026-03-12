import tkinter as tk
from tkinter import ttk, font
import random
from collections import Counter
import math


class GCDLCMRulesWindow(tk.Toplevel):
    """Шпаргалка: Як знаходити НСД і НСК"""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Шпаргалка: НСД та НСК")
        self.geometry("750x550")
        self.configure(bg="#f0f8ff")

        title_font = font.Font(family="Helvetica", size=20, weight="bold")
        rule_font = font.Font(family="Helvetica", size=15)

        tk.Label(self, text="📚 Як знайти НСД та НСК? (6 клас)", font=title_font, bg="#f0f8ff", fg="navy").pack(pady=20)

        rules_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="groove")
        rules_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        instructions_gcd = (
            "🔵 НСД (Найбільший спільний дільник)\n"
            "Щоб знайти НСД, вибираємо ТІЛЬКИ СПІЛЬНІ прості множники "
            "з розкладу обох чисел. Беремо їх парами.\n"
            "Приклад: A = 2 × 2 × 3,  B = 2 × 3 × 5\n"
            "Спільні: 2 і 3. Отже, НСД = 2 × 3 = 6."
        )

        tk.Label(rules_frame, text=instructions_gcd, font=rule_font, bg="#e0ffe0", fg="darkgreen", justify=tk.LEFT,
                 wraplength=650, bd=2, relief="solid").pack(padx=20, pady=10, anchor="w", fill=tk.X, ipady=10)

        instructions_lcm = (
            "🔴 НСК (Найменше спільне кратне)\n"
            "Щоб знайти НСК, виписуємо ВСІ множники одного (краще більшого) числа "
            "і ДОДАЄМО ті множники іншого числа, яких не вистачає.\n"
            "Приклад: A = 2 × 2 × 3 (це 12),  B = 2 × 3 × 5 (це 30)\n"
            "Виписуємо всі з B: 2 × 3 × 5.\n"
            "Дивимось на A: тут дві двійки, а ми виписали одну. Треба додати ще одну '2'.\n"
            "Отже, НСК = 2 × 3 × 5 × 2 = 60."
        )

        tk.Label(rules_frame, text=instructions_lcm, font=rule_font, bg="#ffe4e1", fg="darkred", justify=tk.LEFT,
                 wraplength=650, bd=2, relief="solid").pack(padx=20, pady=10, anchor="w", fill=tk.X, ipady=10)

        ttk.Button(self, text="Зрозуміло! Закрити", command=self.destroy).pack(pady=10)


class GCDLCMTrainerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Конструктор НСД та НСК")
        self.geometry("900x850")
        self.configure(bg="#ffffff")

        # Шрифти
        self.font_title = font.Font(family="Helvetica", size=22, weight="bold")
        self.font_numbers = font.Font(family="Courier", size=24, weight="bold")
        self.font_main = font.Font(family="Helvetica", size=18)
        self.font_btn = font.Font(family="Helvetica", size=18, weight="bold")

        # Змінні
        self.a_val = 0
        self.b_val = 0
        self.a_factors = []
        self.b_factors = []

        self.gcd_factors = []
        self.lcm_factors = []
        self.user_factors = []

        self.phase = 1  # 1 = НСД, 2 = НСК
        self.primes = [2, 3, 5, 7, 11, 13, 17, 19]

        self._build_ui()
        self.generate_task()

    def _build_ui(self):
        # --- Верхня панель ---
        top_frame = tk.Frame(self, bg="#ffffff")
        top_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(top_frame, text="🧩 Збирач НСД та НСК", font=self.font_title, bg="#ffffff", fg="navy").pack(
            side=tk.LEFT)
        ttk.Button(top_frame, text="📖 Як шукати?", command=self.open_rules).pack(side=tk.RIGHT)

        # --- Панель умови (дано числа) ---
        task_container = tk.LabelFrame(self, text=" Розкладені числа ", font=self.font_main, bg="#f9f9f9", fg="gray")
        task_container.pack(fill=tk.X, padx=40, pady=10, ipady=10)

        self.lbl_numA = tk.Label(task_container, text="A = ?", font=self.font_numbers, bg="#f9f9f9", fg="black")
        self.lbl_numA.pack(pady=5)

        self.lbl_numB = tk.Label(task_container, text="B = ?", font=self.font_numbers, bg="#f9f9f9", fg="black")
        self.lbl_numB.pack(pady=5)

        # --- Панель конструювання виразу ---
        self.work_container = tk.LabelFrame(self, text=" Твоя відповідь ", font=self.font_main, bg="#ffffff", fg="navy")
        self.work_container.pack(fill=tk.X, padx=40, pady=10, ipady=10)

        self.lbl_task_prompt = tk.Label(self.work_container, text="КРОК 1: Склади НСД (Найбільший спільний дільник)",
                                        font=font.Font(family="Helvetica", size=16, weight="bold"), bg="#ffffff",
                                        fg="darkgreen")
        self.lbl_task_prompt.pack(pady=10)

        self.lbl_user_expr = tk.Label(self.work_container, text="НСД = ...", font=self.font_numbers, bg="#e1f5fe",
                                      fg="blue", width=30, relief="sunken", bd=2)
        self.lbl_user_expr.pack(pady=10)

        # --- Клавіатура простих множників ---
        kb_frame = tk.Frame(self, bg="#ffffff")
        kb_frame.pack(pady=10)

        for p in self.primes:
            btn = tk.Button(kb_frame, text=str(p), font=self.font_btn, width=4, bg="#fff9c4",
                            activebackground="#fff59d", relief="raised", bd=3,
                            command=lambda prime=p: self.add_factor(prime))
            btn.pack(side=tk.LEFT, padx=5)

        btn_del = tk.Button(kb_frame, text="⌫ Стерти", font=self.font_btn, bg="#ffcdd2", activebackground="#ef9a9a",
                            relief="raised", bd=3, command=self.remove_factor)
        btn_del.pack(side=tk.LEFT, padx=15)

        # --- Керування та зворотний зв'язок ---
        controls_frame = tk.Frame(self, bg="#ffffff")
        controls_frame.pack(pady=10)

        style = ttk.Style()
        style.configure("Action.TButton", font=self.font_main, padding=10)

        self.btn_check = ttk.Button(controls_frame, text="✔ Перевірити", style="Action.TButton",
                                    command=self.check_answer)
        self.btn_check.pack(side=tk.LEFT, padx=10)

        self.btn_next = ttk.Button(controls_frame, text="➡ Наступна пара", style="Action.TButton",
                                   command=self.generate_task)
        self.btn_next.pack(side=tk.LEFT, padx=10)

        self.lbl_feedback = tk.Label(self, text="Вибирай множники з панелі вище.",
                                     font=font.Font(family="Helvetica", size=16, weight="bold"), bg="#ffffff",
                                     wraplength=700)
        self.lbl_feedback.pack(pady=20)

    def open_rules(self):
        GCDLCMRulesWindow(self)

    def _calc_target_factors(self):
        """Алгоритмічно точно рахує списки множників для НСД та НСК"""
        count_a = Counter(self.a_factors)
        count_b = Counter(self.b_factors)

        # НСД: перетин множин (мінімальні степені)
        gcd_counts = count_a & count_b
        self.gcd_factors = sorted(list(gcd_counts.elements()))

        # НСК: об'єднання множин (максимальні степені)
        lcm_counts = count_a | count_b
        self.lcm_factors = sorted(list(lcm_counts.elements()))

    def generate_task(self):
        # Генеруємо базу (щоб точно був спільний дільник)
        base = random.choices([2, 3, 5], k=random.randint(1, 2))

        # Додаємо унікальні множники для А та Б
        extra_a = random.choices([2, 3, 5, 7], k=random.randint(1, 2))
        extra_b = random.choices([2, 3, 5, 7, 11], k=random.randint(1, 2))

        # Запобігаємо повному співпадінню
        if sorted(extra_a) == sorted(extra_b):
            extra_b.append(11)

        self.a_factors = sorted(base + extra_a)
        self.b_factors = sorted(base + extra_b)

        self.a_val = math.prod(self.a_factors)
        self.b_val = math.prod(self.b_factors)

        self._calc_target_factors()

        # Оновлення інтерфейсу
        a_str = " × ".join(map(str, self.a_factors))
        b_str = " × ".join(map(str, self.b_factors))

        self.lbl_numA.config(text=f"{self.a_val} = {a_str}")
        self.lbl_numB.config(text=f"{self.b_val} = {b_str}")

        self.phase = 1
        self.user_factors.clear()

        self.lbl_task_prompt.config(text=f"КРОК 1: Склади НСД для чисел {self.a_val} та {self.b_val}", fg="darkgreen")
        self.update_user_expr_display()
        self.lbl_feedback.config(text="Уважно подивись на обидва числа і вибери тільки СПІЛЬНІ множники.", fg="gray")

        self.btn_check.config(state=tk.NORMAL)
        self.btn_next.config(state=tk.DISABLED)

    def update_user_expr_display(self):
        prefix = "НСД =" if self.phase == 1 else "НСК ="

        if not self.user_factors:
            self.lbl_user_expr.config(text=f"{prefix} ...")
        else:
            factors_str = " × ".join(map(str, self.user_factors))
            self.lbl_user_expr.config(text=f"{prefix} {factors_str}")

    def add_factor(self, prime):
        self.user_factors.append(prime)
        # Автоматично сортуємо для зручності перевірки та красивого вигляду
        self.user_factors.sort()
        self.update_user_expr_display()
        self.lbl_feedback.config(text="")

    def remove_factor(self):
        if self.user_factors:
            self.user_factors.pop()  # Видаляємо найбільший (оскільки відсортовано)
            self.update_user_expr_display()

    def check_answer(self):
        if not self.user_factors:
            self.lbl_feedback.config(text="Ти ще не вибрав жодного множника!", fg="red")
            return

        user_counts = Counter(self.user_factors)

        if self.phase == 1:
            # ПЕРЕВІРКА НСД
            target_counts = Counter(self.gcd_factors)

            if self.user_factors == self.gcd_factors:
                gcd_val = math.prod(self.gcd_factors)
                self.lbl_user_expr.config(text=f"НСД = {' × '.join(map(str, self.user_factors))} = {gcd_val}")
                self.lbl_feedback.config(text="🎉 ВІДМІННО! НСД знайдено абсолютно правильно.\nПереходимо до НСК!",
                                         fg="green")

                # Перехід до Фази 2 (НСК)
                self.phase = 2
                self.user_factors.clear()
                self.lbl_task_prompt.config(text=f"КРОК 2: Склади НСК для чисел {self.a_val} та {self.b_val}",
                                            fg="darkred")
                # Робимо невеличку затримку для оновлення виразу, щоб учень побачив повідомлення
                self.after(2500, self.update_user_expr_display)

            else:
                # Аналіз помилок НСД
                extra = user_counts - target_counts
                missing = target_counts - user_counts

                if extra:
                    self.lbl_feedback.config(
                        text="❌ Помилка! Ти додав множник, якого немає в обох числах,\nабо взяв його забагато разів.",
                        fg="red")
                elif missing:
                    self.lbl_feedback.config(text="🤔 Майже! Але ти вибрав ще НЕ ВСІ спільні множники.", fg="darkorange")

        else:
            # ПЕРЕВІРКА НСК
            target_counts = Counter(self.lcm_factors)

            if self.user_factors == self.lcm_factors:
                lcm_val = math.prod(self.lcm_factors)
                self.lbl_user_expr.config(text=f"НСК = {' × '.join(map(str, self.user_factors))} = {lcm_val}")
                self.lbl_feedback.config(text="🎉 БРАВО! Ти ідеально склав НСК!\nЗавдання виконано повністю.",
                                         fg="green")

                self.btn_check.config(state=tk.DISABLED)
                self.btn_next.config(state=tk.NORMAL)
            else:
                # Аналіз помилок НСК
                extra = user_counts - target_counts
                missing = target_counts - user_counts

                if extra:
                    self.lbl_feedback.config(
                        text="❌ Помилка! Ти вибрав зайві множники.\nДля НСК беремо всі множники більшого числа і тільки ті, яких НЕ вистачає з меншого.",
                        fg="red")
                elif missing:
                    self.lbl_feedback.config(
                        text="🤔 Малувато! Ти забув додати унікальні 'хвостики' з іншого числа.\nПеревір, чи всі множники обох чисел покриті.",
                        fg="darkorange")


if __name__ == "__main__":
    app = GCDLCMTrainerApp()
    app.mainloop()