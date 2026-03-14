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
        self.configure(bg="#f0f8ff")
        
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = min(1200, sw), min(900, sh)
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        rule_font = font.Font(family="Helvetica", size=18)

        tk.Label(self, text="📚 Як знайти НСД та НСК? (§ 31-32)", font=title_font, bg="#f0f8ff", fg="navy").pack(pady=20)

        rules_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="groove")
        rules_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        instructions_gcd = (
            "🔵 НСД (Найбільший спільний дільник)\n"
            "Щоб знайти НСД, вибираємо ТІЛЬКИ СПІЛЬНІ прості множники "
            "з розкладу обох чисел. Беремо їх парами.\n"
            "Приклад: A = 2 × 2 × 3,  B = 2 × 3 × 5\n"
            "Спільні: 2 і 3. Отже, НСД = 2 × 3 = 6."
        )

        tk.Label(rules_frame, text=instructions_gcd, font=rule_font, bg="#e0ffe0", fg="darkgreen", justify=tk.LEFT,
                 wraplength=w-100, bd=2, relief="solid").pack(padx=30, pady=20, anchor="w", fill=tk.X, ipady=15)

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
                 wraplength=w-100, bd=2, relief="solid").pack(padx=30, pady=20, anchor="w", fill=tk.X, ipady=15)

        ttk.Button(self, text="Зрозуміло! Закрити", command=self.destroy).pack(pady=20, ipadx=20, ipady=10)


class GCDLCMTrainerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Конструктор НСД та НСК (§ 31-32)")
        self.configure(bg="#ffffff")
        
        # Fullscreen
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        # Шрифти
        self.font_title = font.Font(family="Helvetica", size=28, weight="bold")
        self.font_numbers = font.Font(family="Courier", size=36, weight="bold")
        self.font_main = font.Font(family="Helvetica", size=22)
        self.font_btn = font.Font(family="Helvetica", size=20, weight="bold")

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
        top_frame.pack(fill=tk.X, padx=30, pady=20)

        tk.Label(top_frame, text="🧩 Збирач НСД та НСК", font=self.font_title, bg="#ffffff", fg="navy").pack(side=tk.LEFT)
        
        tk.Button(top_frame, text="❌", font=("Arial", 20), bg="red", fg="white", command=self.destroy).pack(side=tk.RIGHT, padx=10)
        ttk.Button(top_frame, text="📖 Як шукати?", command=self.open_rules).pack(side=tk.RIGHT, padx=20)

        # --- Панель умови (дано числа) ---
        task_container = tk.LabelFrame(self, text=" Розкладені числа ", font=self.font_main, bg="#f9f9f9", fg="gray")
        task_container.pack(fill=tk.X, padx=50, pady=20, ipady=20)

        self.lbl_numA = tk.Label(task_container, text="A = ?", font=self.font_numbers, bg="#f9f9f9", fg="black")
        self.lbl_numA.pack(pady=10)

        self.lbl_numB = tk.Label(task_container, text="B = ?", font=self.font_numbers, bg="#f9f9f9", fg="black")
        self.lbl_numB.pack(pady=10)

        # --- Панель конструювання виразу ---
        self.construct_frame = tk.LabelFrame(self, text=" Твоя відповідь ", font=self.font_main, bg="#e3f2fd", fg="navy")
        self.construct_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)

        self.lbl_question = tk.Label(self.construct_frame, text="Знайди НСД (спільні множники):", font=self.font_main, bg="#e3f2fd", fg="navy")
        self.lbl_question.pack(pady=15)

        # Поле, де збираються множники
        self.lbl_user_expr = tk.Label(self.construct_frame, text="?", font=self.font_numbers, bg="white", relief="sunken", width=30)
        self.lbl_user_expr.pack(pady=10, ipady=10)

        # Кнопки з множниками (будуть оновлюватись)
        self.factors_btn_frame = tk.Frame(self.construct_frame, bg="#e3f2fd")
        self.factors_btn_frame.pack(pady=20)

        # Панель керування
        ctrl_frame = tk.Frame(self.construct_frame, bg="#e3f2fd")
        ctrl_frame.pack(pady=20)

        tk.Button(ctrl_frame, text="⬅ Стерти", font=self.font_btn, bg="#ffccbc", command=self.undo_factor).pack(side=tk.LEFT, padx=20)
        tk.Button(ctrl_frame, text="✅ Перевірити", font=self.font_btn, bg="#c8e6c9", command=self.check_answer).pack(side=tk.LEFT, padx=20)
        tk.Button(ctrl_frame, text="➡ Далі", font=self.font_btn, bg="#bbdefb", command=self.next_phase).pack(side=tk.LEFT, padx=20)

    def open_rules(self):
        GCDLCMRulesWindow(self)

    def generate_task(self):
        # Генеруємо два числа через множники
        # Обмежуємо множники, щоб не було занадто складно
        fA = sorted([random.choice([2, 2, 2, 3, 3, 5]) for _ in range(random.randint(2, 4))])
        fB = sorted([random.choice([2, 2, 3, 3, 5, 5, 7]) for _ in range(random.randint(2, 4))])

        self.a_factors = fA
        self.b_factors = fB
        self.a_val = math.prod(fA)
        self.b_val = math.prod(fB)

        # Рахуємо правильні відповіді
        cA = Counter(fA)
        cB = Counter(fB)
        
        # НСД
        common = cA & cB
        self.gcd_factors = sorted(list(common.elements()))
        
        # НСК
        union = cA | cB
        self.lcm_factors = sorted(list(union.elements()))

        # Оновлюємо UI
        self.lbl_numA.config(text=f"A = {self.format_factors(fA)} = {self.a_val}")
        self.lbl_numB.config(text=f"B = {self.format_factors(fB)} = {self.b_val}")

        # Починаємо з НСД
        self.phase = 1
        self.setup_phase()

    def setup_phase(self):
        self.user_factors = []
        self.update_user_expr()
        
        # Очистити кнопки
        for w in self.factors_btn_frame.winfo_children():
            w.destroy()

        # Збираємо унікальні множники з обох чисел для кнопок
        available = sorted(list(set(self.a_factors + self.b_factors)))
        
        for p in available:
            tk.Button(self.factors_btn_frame, text=str(p), font=self.font_btn, width=4,
                      command=lambda x=p: self.add_factor(x)).pack(side=tk.LEFT, padx=10)

        if self.phase == 1:
            self.lbl_question.config(text="Етап 1: Знайди НСД (тільки спільні пари)", fg="navy")
            self.construct_frame.config(text=" Збираємо НСД ")
        else:
            self.lbl_question.config(text="Етап 2: Знайди НСК (всі з більшого + чого не вистачає)", fg="darkred")
            self.construct_frame.config(text=" Збираємо НСК ")

    def add_factor(self, p):
        self.user_factors.append(p)
        self.update_user_expr()

    def undo_factor(self):
        if self.user_factors:
            self.user_factors.pop()
            self.update_user_expr()

    def update_user_expr(self):
        if not self.user_factors:
            self.lbl_user_expr.config(text="?")
            return
        
        s = " × ".join(map(str, self.user_factors))
        val = math.prod(self.user_factors)
        self.lbl_user_expr.config(text=f"{s} = {val}")

    def format_factors(self, factors):
        return " × ".join(map(str, factors))

    def check_answer(self):
        user_sorted = sorted(self.user_factors)
        
        if self.phase == 1:
            target = self.gcd_factors
            name = "НСД"
        else:
            target = self.lcm_factors
            name = "НСК"
            
        if user_sorted == target:
            self.lbl_question.config(text=f"✅ Правильно! {name} знайдено.", fg="green")
        else:
            self.lbl_question.config(text=f"❌ Помилка. Спробуй ще.", fg="red")

    def next_phase(self):
        if self.phase == 1:
            self.phase = 2
            self.setup_phase()
        else:
            # Генеруємо нове
            self.generate_task()

if __name__ == "__main__":
    app = GCDLCMTrainerApp()
    app.mainloop()
