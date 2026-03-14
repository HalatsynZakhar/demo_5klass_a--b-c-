import tkinter as tk
from tkinter import ttk, font
import random

class FactorizationRulesWindow(tk.Toplevel):
    """Шпаргалка: Як розкладати число на прості множники"""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Шпаргалка: Розкладання у стовпчик")
        self.configure(bg="#f0f8ff")
        
        # Make fullscreen or large
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = min(1200, sw), min(900, sh)
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        rule_font = font.Font(family="Helvetica", size=18)
        btn_font = font.Font(family="Helvetica", size=16, weight="bold")

        tk.Label(self, text="📚 Алгоритм розкладання (§ 30)", font=title_font, bg="#f0f8ff", fg="navy").pack(pady=20)

        rules_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="groove")
        rules_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        instructions = (
            "1. Запиши число і проведи вертикальну лінію.\n\n"
            "2. Знайди будь-яке просте число, на яке воно ділиться без остачі (2, 3, 5, 7...).\n\n"
            "3. Запиши цей дільник праворуч від лінії.\n\n"
            "4. Поділи число на дільник, а результат запиши ліворуч під початковим числом.\n\n"
            "5. Повторюй це з новим числом, поки зліва не отримаєш 1.\n\n"
            "6. Запиши відповідь у вигляді добутку."
        )

        tk.Label(rules_frame, text=instructions, font=rule_font, bg="#ffffff", fg="#333333", justify=tk.LEFT,
                 wraplength=w-100).pack(padx=30, pady=30, anchor="w")

        example_frame = tk.Frame(rules_frame, bg="#e0ffe0", bd=1, relief="solid")
        example_frame.pack(pady=20, padx=30, fill=tk.X)
        tk.Label(example_frame, text="Приклад: 60 = 2 × 2 × 3 × 5",
                 font=font.Font(family="Courier", size=24, weight="bold"), bg="#e0ffe0", fg="darkgreen").pack(pady=15)

        ttk.Button(self, text="Зрозуміло! Закрити", command=self.destroy).pack(pady=20, ipadx=20, ipady=10)


class PrimeFactorizationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Тренажер: Розкладання на прості множники (§ 30)")
        self.configure(bg="#ffffff")
        
        # Fullscreen for interactive board
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        # Шрифти (Large for whiteboard)
        self.font_title = font.Font(family="Helvetica", size=28, weight="bold")
        self.font_column = font.Font(family="Courier", size=40, weight="bold")
        self.font_main = font.Font(family="Helvetica", size=20)
        self.font_btn = font.Font(family="Helvetica", size=18, weight="bold")
        self.font_numpad = font.Font(family="Helvetica", size=24, weight="bold")

        # Змінні стану
        self.start_number = 0
        self.current_number = 0
        self.expected_quotient = 0
        self.factors = []
        self.column_rows = []

        self.level_var = tk.IntVar(value=1)
        self.state = "pick_prime"
        self.numpad_input = ""

        self.primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

        self._build_ui()
        self.generate_new_task()

    def _build_ui(self):
        # --- Верхня панель ---
        top_frame = tk.Frame(self, bg="#ffffff")
        top_frame.pack(fill=tk.X, padx=30, pady=20)

        tk.Label(top_frame, text="Майстер Стовпчиків 🧮", font=self.font_title, bg="#ffffff", fg="navy").pack(side=tk.LEFT)
        
        # Exit button for fullscreen
        tk.Button(top_frame, text="❌", font=("Arial", 20), bg="red", fg="white", command=self.destroy).pack(side=tk.RIGHT, padx=10)
        
        ttk.Button(top_frame, text="📖 Правила", command=self.open_rules).pack(side=tk.RIGHT, padx=20)

        level_frame = tk.LabelFrame(top_frame, text=" Рівень ", font=font.Font(family="Helvetica", size=14), bg="#ffffff")
        level_frame.pack(side=tk.RIGHT, padx=30)

        style = ttk.Style()
        style.configure('TRadiobutton', font=('Helvetica', 16))
        
        ttk.Radiobutton(level_frame, text="Авто-ділення", variable=self.level_var, value=1,
                        command=self.generate_new_task).pack(side=tk.LEFT, padx=15, pady=5)
        ttk.Radiobutton(level_frame, text="Вручну", variable=self.level_var, value=2,
                        command=self.generate_new_task).pack(side=tk.LEFT, padx=15, pady=5)


        # --- Основна робоча область ---
        main_workspace = tk.Frame(self, bg="#ffffff")
        main_workspace.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)

        # Ліва частина (Стовпчик)
        self.column_container = tk.LabelFrame(main_workspace, text=" Зошит ", font=self.font_main, bg="#f9f9f9", fg="gray", width=500)
        self.column_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        self.column_container.pack_propagate(False)

        # Права частина (Панель керування)
        self.control_panel = tk.Frame(main_workspace, bg="#ffffff", width=500)
        self.control_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Інструкція
        self.lbl_instruction = tk.Label(self.control_panel, text="Оберіть дільник:", font=self.font_title, bg="#ffffff", fg="#333")
        self.lbl_instruction.pack(pady=(0, 20))

        # Панель з простими числами
        self.primes_frame = tk.Frame(self.control_panel, bg="#ffffff")
        self.primes_frame.pack(fill=tk.BOTH, expand=True)
        
        # Створюємо кнопки простих чисел
        btn_container = tk.Frame(self.primes_frame, bg="#ffffff")
        btn_container.pack(anchor=tk.CENTER)
        
        row, col = 0, 0
        for p in self.primes:
            btn = tk.Button(btn_container, text=str(p), font=self.font_numpad, width=4, height=1,
                            bg="#e0f7fa", activebackground="#b2ebf2",
                            command=lambda x=p: self.on_prime_click(x))
            btn.grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col > 4:
                col = 0
                row += 1

        # Панель для введення частки (спочатку прихована)
        self.quotient_frame = tk.Frame(self.control_panel, bg="#ffffff")
        
        self.lbl_input_prompt = tk.Label(self.quotient_frame, text="Результат ділення:", font=self.font_main, bg="#ffffff")
        self.lbl_input_prompt.pack(pady=10)
        
        self.lbl_input_display = tk.Label(self.quotient_frame, text="?", font=self.font_column, bg="#fff3e0", width=10, relief="sunken")
        self.lbl_input_display.pack(pady=10)
        
        numpad_frame = tk.Frame(self.quotient_frame, bg="#ffffff")
        numpad_frame.pack(pady=10)
        
        keys = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
            ('C', 3, 0), ('0', 3, 1), ('OK', 3, 2)
        ]
        
        for k, r, c in keys:
            color = "#ffccbc" if k == 'C' else "#c8e6c9" if k == 'OK' else "#f0f0f0"
            cmd = lambda x=k: self.on_numpad(x)
            tk.Button(numpad_frame, text=k, font=self.font_numpad, width=4, height=1, bg=color, command=cmd).grid(row=r, column=c, padx=5, pady=5)

        # Кнопка нового завдання
        tk.Button(self.control_panel, text="✨ Нове число", font=self.font_btn, bg="#4caf50", fg="white",
                  command=self.generate_new_task, height=2).pack(side=tk.BOTTOM, fill=tk.X, pady=20, padx=50)

    def open_rules(self):
        FactorizationRulesWindow(self)

    def generate_new_task(self):
        # Очищаємо все
        for w in self.column_container.winfo_children():
            w.destroy()
        self.column_rows = []
        self.factors = []
        
        # Генеруємо число (легке: до 100, складне: до 300)
        candidates = []
        for i in range(10, 200):
            # Перевіримо, щоб не було простим
            temp = i
            f = []
            d = 2
            while d*d <= temp:
                while temp % d == 0:
                    f.append(d)
                    temp //= d
                d += 1
            if temp > 1: f.append(temp)
            if len(f) >= 2 and max(f) < 50: # Хоча б 2 множники і не надто великі
                candidates.append(i)
                
        self.start_number = random.choice(candidates)
        self.current_number = self.start_number
        
        # Додаємо перший рядок
        self.add_row(self.start_number)
        
        self.switch_to_pick_prime()

    def add_row(self, num_val):
        # Рядок: Число | (місце для дільника)
        row_frame = tk.Frame(self.column_container, bg="#f9f9f9")
        row_frame.pack(fill=tk.X, pady=2)
        
        # Ліва частина (Число)
        left = tk.Label(row_frame, text=str(num_val), font=self.font_column, bg="#f9f9f9", width=6, anchor="e")
        left.pack(side=tk.LEFT, padx=(50, 10))
        
        # Розділювач
        sep = tk.Frame(row_frame, bg="black", width=3, height=50)
        sep.pack(side=tk.LEFT, fill=tk.Y)
        
        # Права частина (Дільник) - поки порожньо
        right = tk.Label(row_frame, text="", font=self.font_column, bg="#f9f9f9", width=6, anchor="w", fg="blue")
        right.pack(side=tk.LEFT, padx=(10, 50))
        
        self.column_rows.append({'frame': row_frame, 'left': left, 'right': right, 'val': num_val})

    def switch_to_pick_prime(self):
        self.state = "pick_prime"
        self.quotient_frame.pack_forget()
        self.primes_frame.pack(fill=tk.BOTH, expand=True)
        self.lbl_instruction.config(text=f"На що ділиться {self.current_number}?", fg="black")

    def switch_to_enter_quotient(self, divisor):
        self.state = "enter_quotient"
        self.primes_frame.pack_forget()
        self.quotient_frame.pack(fill=tk.BOTH, expand=True)
        self.numpad_input = ""
        self.lbl_input_display.config(text="?")
        self.expected_quotient = self.current_number // divisor
        self.lbl_instruction.config(text=f"Скільки буде {self.current_number} : {divisor} ?", fg="blue")

    def on_prime_click(self, p):
        if self.current_number == 1: return
        
        if self.current_number % p == 0:
            # Правильний дільник
            # Записуємо дільник у поточний рядок
            last_row = self.column_rows[-1]
            last_row['right'].config(text=str(p))
            self.factors.append(p)
            
            if self.level_var.get() == 1:
                # Автоматичний режим
                self.current_number //= p
                if self.current_number == 1:
                    self.finish_game()
                else:
                    self.add_row(self.current_number)
            else:
                # Ручний режим
                self.switch_to_enter_quotient(p)
        else:
            # Помилка
            self.lbl_instruction.config(text=f"❌ {self.current_number} не ділиться на {p}!", fg="red")

    def on_numpad(self, key):
        if key == 'C':
            self.numpad_input = ""
        elif key == 'OK':
            if self.numpad_input and int(self.numpad_input) == self.expected_quotient:
                # Правильно
                self.current_number = self.expected_quotient
                if self.current_number == 1:
                    self.finish_game()
                else:
                    self.add_row(self.current_number)
                    self.switch_to_pick_prime()
            else:
                self.lbl_instruction.config(text="❌ Неправильно, спробуй ще!", fg="red")
                self.numpad_input = ""
        else:
            self.numpad_input += key
            
        self.lbl_input_display.config(text=self.numpad_input if self.numpad_input else "?")

    def finish_game(self):
        # Додаємо 1 в кінці
        self.add_row(1)
        self.quotient_frame.pack_forget()
        self.primes_frame.pack_forget()
        
        # Формуємо рядок відповіді
        factors_str = " × ".join(map(str, sorted(self.factors)))
        res_text = f"Чудово!\n{self.start_number} = {factors_str}"
        
        self.lbl_instruction.config(text=res_text, fg="green", font=("Helvetica", 32, "bold"))

if __name__ == "__main__":
    app = PrimeFactorizationApp()
    app.mainloop()
