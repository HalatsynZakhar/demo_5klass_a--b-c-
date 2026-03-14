"""
Інтерактивний урок: Зв'язок між десятковими дробами та кількістю нулів.
Демонстрація правила: "Скільки знаків після коми - стільки нулів у знаменнику".
"""
import tkinter as tk
import random

# ══════════════════════════════════════════════════════════════════
#  КОЛЬОРИ
# ══════════════════════════════════════════════════════════════════
BG_APP    = "#fdf4ff"  # Дуже світлий фіолетовий
BG_HEADER = "#7c3aed"  # Фіолетовий
C_ACCENT  = "#6d28d9"  # Темно-фіолетовий
C_DIGIT   = "#db2777"  # Рожевий (цифри після коми)
C_ZERO    = "#059669"  # Зелений (нулі)
C_BTN     = "#8b5cf6"
C_BTN_ACT = "#7c3aed"

class DecimalLessonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Урок: Знаки після коми")
        self.configure(bg=BG_APP)
        try:
            self.state('zoomed')
        except:
            self.attributes('-fullscreen', True)
            
        self.current_digits = "123"
        self.decimal_places = 1 # 1 .. 6
        
        self.mode = "demo" # "demo" or "task"
        self.task_data = None
        self.score = 0
        self.total = 0

        self._create_ui()
        self._update_demo()

    def _create_ui(self):
        # ─── ЗАГОЛОВОК ──────────────────────────────────────────────
        header = tk.Frame(self, bg=BG_HEADER, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="ЗНАКИ ПІСЛЯ КОМИ ТА НУЛІ", 
                 font=("Segoe UI", 24, "bold"), bg=BG_HEADER, fg="white").pack(side="left", padx=30)
        
        tk.Button(header, text="✕", font=("Arial", 16), bg=BG_HEADER, fg="white", bd=0, 
                  command=self.destroy).pack(side="right", padx=10)

        # ─── МЕНЮ (Tabs) ────────────────────────────────────────────
        menu = tk.Frame(self, bg="white", height=60)
        menu.pack(fill="x", padx=20, pady=10)
        
        self.btn_demo = tk.Button(menu, text="🔍 ПОЯСНЕННЯ", font=("Segoe UI", 14, "bold"),
                                  bg=C_BTN, fg="white", padx=20, bd=0, cursor="hand2",
                                  command=self._to_demo)
        self.btn_demo.pack(side="left", padx=10, pady=5)
        
        self.btn_task = tk.Button(menu, text="📝 ТРЕНУВАННЯ", font=("Segoe UI", 14, "bold"),
                                  bg="#e5e7eb", fg="#374151", padx=20, bd=0, cursor="hand2",
                                  command=self._to_task)
        self.btn_task.pack(side="left", padx=10, pady=5)

        # ─── ГОЛОВНА ЗОНА ───────────────────────────────────────────
        self.main_area = tk.Frame(self, bg=BG_APP)
        self.main_area.pack(expand=True, fill="both", padx=40, pady=10)
        
        # === DEMO FRAME ===
        self.demo_frame = tk.Frame(self.main_area, bg=BG_APP)
        self.demo_frame.pack(fill="both", expand=True)
        
        # Керування кількістю знаків
        ctrl_frame = tk.Frame(self.demo_frame, bg=BG_APP)
        ctrl_frame.pack(pady=20)
        
        tk.Button(ctrl_frame, text="➖ Менше знаків", font=("Segoe UI", 16),
                  command=lambda: self._change_places(-1)).pack(side="left", padx=20)
        
        self.lbl_places_info = tk.Label(ctrl_frame, text="1 знак після коми", 
                                        font=("Segoe UI", 18, "bold"), bg=BG_APP, fg=C_ACCENT)
        self.lbl_places_info.pack(side="left", padx=20)
        
        tk.Button(ctrl_frame, text="➕ Більше знаків", font=("Segoe UI", 16),
                  command=lambda: self._change_places(1)).pack(side="left", padx=20)

        # Візуалізація
        vis_frame = tk.Frame(self.demo_frame, bg="white", bd=2, relief="solid")
        vis_frame.pack(expand=True, fill="both", padx=50, pady=20)
        
        self.lbl_demo_dec = tk.Label(vis_frame, text="", font=("Courier New", 60, "bold"), bg="white")
        self.lbl_demo_dec.place(relx=0.3, rely=0.3, anchor="center")
        
        self.lbl_arrow = tk.Label(vis_frame, text="➡", font=("Arial", 60), bg="white", fg="#9ca3af")
        self.lbl_arrow.place(relx=0.5, rely=0.3, anchor="center")
        
        # Дріб
        self.fr_demo_frac = tk.Frame(vis_frame, bg="white")
        self.fr_demo_frac.place(relx=0.7, rely=0.3, anchor="center")
        
        self.lbl_demo_num = tk.Label(self.fr_demo_frac, text="1", font=("Courier New", 40, "bold"), bg="white", fg=C_DIGIT)
        self.lbl_demo_num.pack()
        tk.Frame(self.fr_demo_frac, bg="black", height=4, width=150).pack(fill="x")
        self.lbl_demo_den = tk.Label(self.fr_demo_frac, text="10", font=("Courier New", 40, "bold"), bg="white", fg=C_ZERO)
        self.lbl_demo_den.pack()
        
        # Пояснення знизу
        self.lbl_explain = tk.Label(vis_frame, text="", font=("Segoe UI", 20), bg="white", justify="center")
        self.lbl_explain.place(relx=0.5, rely=0.75, anchor="center")

        # === TASK FRAME ===
        self.task_frame = tk.Frame(self.main_area, bg=BG_APP)
        # (Прихований спочатку)
        
        self.lbl_score = tk.Label(self.task_frame, text="Рахунок: 0/0", font=("Segoe UI", 16, "bold"), bg=BG_APP, fg=C_ACCENT)
        self.lbl_score.pack(pady=10)
        
        self.task_q_frame = tk.Frame(self.task_frame, bg=BG_APP)
        self.task_q_frame.pack(pady=40)

        # Текстова частина питання (до дробу)
        self.lbl_task_pre = tk.Label(self.task_q_frame, text="", font=("Segoe UI", 28), bg=BG_APP)
        self.lbl_task_pre.pack(side="left")
        
        # Місце для дробу в питанні (якщо є)
        self.q_frac_frame = tk.Frame(self.task_q_frame, bg=BG_APP)
        self.q_frac_frame.pack(side="left", padx=20)
        
        # Текстова частина питання (після дробу)
        self.lbl_task_post = tk.Label(self.task_q_frame, text="", font=("Segoe UI", 28), bg=BG_APP)
        self.lbl_task_post.pack(side="left")

        self.ans_frame = tk.Frame(self.task_frame, bg=BG_APP)
        self.ans_frame.pack(pady=20)
        
        self.lbl_feedback = tk.Label(self.task_frame, text="", font=("Segoe UI", 20, "bold"), bg=BG_APP)
        self.lbl_feedback.pack(pady=20)
        
        tk.Button(self.task_frame, text="Наступне завдання ➡", font=("Segoe UI", 16),
                  command=self._next_task, bg=C_BTN, fg="white").pack(pady=20)

    def _to_demo(self):
        self.mode = "demo"
        self.btn_demo.config(bg=C_BTN, fg="white")
        self.btn_task.config(bg="#e5e7eb", fg="#374151")
        self.task_frame.pack_forget()
        self.demo_frame.pack(fill="both", expand=True)

    def _to_task(self):
        self.mode = "task"
        self.btn_task.config(bg=C_BTN, fg="white")
        self.btn_demo.config(bg="#e5e7eb", fg="#374151")
        self.demo_frame.pack_forget()
        self.task_frame.pack(fill="both", expand=True)
        self._next_task()

    def _change_places(self, delta):
        self.decimal_places = max(1, min(6, self.decimal_places + delta))
        self._update_demo()

    def _update_demo(self):
        # Оновлюємо демо
        # Генеруємо число
        n_str = "0,"
        digits = ""
        for i in range(self.decimal_places):
            d = str(random.randint(1, 9))
            digits += d
        
        n_str += digits
        
        # Відображення десяткового
        # Зменшуємо шрифт для довгих чисел
        f_size = 60 if self.decimal_places <= 4 else 40
        self.lbl_demo_dec.config(text=n_str, fg=C_DIGIT, font=("Courier New", f_size, "bold"))
        
        # Інфо
        suffix = "знак" if self.decimal_places==1 else ("знаки" if 1 < self.decimal_places < 5 else "знаків")
        self.lbl_places_info.config(text=f"{self.decimal_places} {suffix} після коми")
        
        # Дріб
        f_size_frac = 40 if self.decimal_places <= 4 else 28
        self.lbl_demo_num.config(text=digits, font=("Courier New", f_size_frac, "bold"))
        denom = "1" + "0" * self.decimal_places
        self.lbl_demo_den.config(text=denom, font=("Courier New", f_size_frac, "bold"))
        
        # Пояснення
        txt = (f"У числі {n_str} є {self.decimal_places} цифр(и) після коми.\n"
               f"Тому у знаменнику пишемо одиницю та {self.decimal_places} нуль(ів).\n"
               f"Читаємо: {self._get_denom_name(self.decimal_places)}")
        self.lbl_explain.config(text=txt)

    def _get_denom_name(self, p):
        if p == 1: return "Десяті"
        if p == 2: return "Соті"
        if p == 3: return "Тисячні"
        if p == 4: return "Десятитисячні"
        if p == 5: return "Стотисячні"
        if p == 6: return "Мільйонні"
        return ""

    # ─── ЛОГІКА ЗАВДАНЬ ─────────────────────────────────────────────
    def _next_task(self):
        self.lbl_feedback.config(text="")
        # Очистити варіанти
        for w in self.ans_frame.winfo_children(): w.destroy()
        # Очистити питання
        for w in self.q_frac_frame.winfo_children(): w.destroy()
        self.lbl_task_pre.config(text="")
        self.lbl_task_post.config(text="")
        
        types = ["dec_to_frac", "frac_to_dec", "count_zeros"]
        t_type = random.choice(types)
        
        if t_type == "dec_to_frac":
            places = random.randint(1, 6)
            val = random.randint(1, 10**places - 1)
            dec_s = f"0,{str(val).zfill(places)}"
            denom = 10**places
            
            self.lbl_task_pre.config(text=f"Запишіть у вигляді звичайного дробу:\n{dec_s}")
            
            # Варіанти
            correct = (val, denom)
            opts = [correct]
            # Неправильні
            opts.append((val, denom*10))
            opts.append((val, denom//10 if denom>10 else 100))
            opts.append((val*10, denom))
            random.shuffle(opts)
            
            for (n, d) in opts:
                self._make_frac_btn(n, d, (n==val and d==denom))
                
        elif t_type == "frac_to_dec":
            places = random.randint(1, 6)
            denom = 10**places
            val = random.randint(1, denom - 1)
            
            self.lbl_task_pre.config(text="Запишіть десятковим дробом:")
            
            # Вертикальний дріб у питанні
            # Зменшуємо шрифт для довгих чисел
            f_size = 28 if places > 4 else 28
            lbl_n = tk.Label(self.q_frac_frame, text=str(val), font=("Arial", f_size, "bold"), bg=BG_APP)
            lbl_n.pack()
            tk.Frame(self.q_frac_frame, bg="black", height=3, width=60 + (places-4)*10 if places>4 else 60).pack(fill="x")
            lbl_d = tk.Label(self.q_frac_frame, text=str(denom), font=("Arial", f_size, "bold"), bg=BG_APP)
            lbl_d.pack()
            
            correct = f"0,{str(val).zfill(places)}"
            opts = [correct]
            opts.append(f"0,{str(val).zfill(places+1)}")
            opts.append(f"0,{str(val).zfill(places-1)}" if places>1 else f"0,{val}0")
            opts.append(f"{val},0")
            random.shuffle(opts)
            
            for o in opts:
                self._make_btn(o, o==correct)
                
        elif t_type == "count_zeros":
            places = random.randint(1, 6)
            val = random.randint(1, 10**places - 1)
            dec_s = f"0,{str(val).zfill(places)}"
            
            self.lbl_task_pre.config(text=f"Скільки нулів має бути у знаменнику для числа:\n{dec_s} ?")
            
            correct = str(places)
            # Генеруємо варіанти навколо правильного
            start = max(1, places - 2)
            opts = [str(i) for i in range(start, start + 4)]
            # Переконаємось що правильна є
            if correct not in opts: opts[-1] = correct
            opts = sorted(list(set(opts)), key=lambda x: int(x))
            
            for o in opts:
                self._make_btn(f"{o} нуль(ів)", o==correct)

    def _make_frac_btn(self, n, d, is_corr):
        f = tk.Frame(self.ans_frame, bd=1, relief="solid", padx=10, pady=5, bg="white")
        f.pack(side="left", padx=15)
        
        lbl_n = tk.Label(f, text=str(n), font=("Arial", 20, "bold"), bg="white")
        lbl_n.pack()
        tk.Frame(f, bg="black", height=2, width=40).pack(fill="x")
        lbl_d = tk.Label(f, text=str(d), font=("Arial", 20, "bold"), bg="white")
        lbl_d.pack()
        
        # Кнопка прозора поверх фрейму або сам фрейм клікабельний
        # Для простоти - кнопка "Обрати" знизу
        tk.Button(f, text="Обрати", command=lambda: self._check(is_corr)).pack(pady=5)

    def _make_btn(self, text, is_corr):
        tk.Button(self.ans_frame, text=text, font=("Arial", 24), 
                  command=lambda: self._check(is_corr)).pack(side="left", padx=15)

    def _check(self, is_correct):
        self.total += 1
        if is_correct:
            self.score += 1
            self.lbl_feedback.config(text="✅ Правильно! Молодець!", fg=C_ZERO)
        else:
            self.lbl_feedback.config(text="❌ Помилка. Спробуй ще раз!", fg="red")
            
        self.lbl_score.config(text=f"Рахунок: {self.score}/{self.total}")

if __name__ == "__main__":
    app = DecimalLessonApp()
    app.mainloop()
