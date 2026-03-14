"""
Інтерактивна демонстрація: Що таке десяткові дроби?
Великий інтерфейс для інтерактивної дошки.
"""
import tkinter as tk
from tkinter import messagebox
import random

# ══════════════════════════════════════════════════════════════════
#  НАЛАШТУВАННЯ
# ══════════════════════════════════════════════════════════════════
BG_APP    = "#f0f9ff"  # Світло-блакитний фон
BG_HEADER = "#0284c7"  # Синій заголовок
C_ACCENT  = "#0369a1"  # Темно-синій текст
C_HIGHLIGHT = "#bae6fd" # Колір заповнення (світлий)
C_BORDER  = "#0284c7"   # Колір рамок
C_RED     = "#e11d48"   # Колір десяткового числа
C_GREEN   = "#16a34a"   # Колір успіху

class DecimalIntroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Що таке десятковий дріб?")
        self.configure(bg=BG_APP)
        # Спробуємо розгорнути на весь екран
        try:
            self.state('zoomed')
        except:
            self.attributes('-fullscreen', True)

        self.mode = "tenths" # "tenths", "hundredths", "thousandths", "ten_thousandths"
        self.value = 0       # Кількість зафарбованих частин
        
        self.task_mode = False
        self.target_value = 0
        self.task_score = 0
        self.task_total = 0

        self._create_ui()
        self.set_mode("tenths")

    def _create_ui(self):
        # ─── ЗАГОЛОВОК ──────────────────────────────────────────────
        header = tk.Frame(self, bg=BG_HEADER, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        lbl_title = tk.Label(header, text="ДЕСЯТКОВІ ДРОБИ: ЗНАЙОМСТВО", 
                             font=("Segoe UI", 24, "bold"), bg=BG_HEADER, fg="white")
        lbl_title.pack(side="left", padx=30)
        
        # Кнопка виходу (якщо фулскрін)
        btn_exit = tk.Button(header, text="✕", font=("Arial", 16), bg=BG_HEADER, fg="white",
                             bd=0, activebackground="#0ea5e9", activeforeground="white",
                             command=self.destroy)
        btn_exit.pack(side="right", padx=10)

        # ─── ГОЛОВНА ОБЛАСТЬ ────────────────────────────────────────
        main = tk.Frame(self, bg=BG_APP)
        main.pack(expand=True, fill="both", padx=20, pady=20)

        # ЛІВА ПАНЕЛЬ: Кнопки вибору режиму
        left_panel = tk.Frame(main, bg=BG_APP)
        left_panel.pack(side="left", fill="y", padx=(0, 20))

        btn_font = ("Segoe UI", 14, "bold")
        
        self.btn_tenths = tk.Button(left_panel, text="Десяті\n(0,1)", font=btn_font,
                                    width=14, height=2, bd=0, cursor="hand2",
                                    command=lambda: self.set_mode("tenths"))
        self.btn_tenths.pack(pady=10)

        self.btn_hunds = tk.Button(left_panel, text="Соті\n(0,01)", font=btn_font,
                                   width=14, height=2, bd=0, cursor="hand2",
                                   command=lambda: self.set_mode("hundredths"))
        self.btn_hunds.pack(pady=10)

        self.btn_thous = tk.Button(left_panel, text="Тисячні\n(0,001)", font=btn_font,
                                   width=14, height=2, bd=0, cursor="hand2",
                                   command=lambda: self.set_mode("thousandths"))
        self.btn_thous.pack(pady=10)

        self.btn_ten_thous = tk.Button(left_panel, text="Дес-тисячні\n(0,0001)", font=btn_font,
                                       width=14, height=2, bd=0, cursor="hand2",
                                       command=lambda: self.set_mode("ten_thousandths"))
        self.btn_ten_thous.pack(pady=10)
        
        tk.Frame(left_panel, bg=C_BORDER, height=2).pack(fill="x", pady=20)
        
        self.btn_task = tk.Button(left_panel, text="🎓 ЗАВДАННЯ", font=btn_font,
                                  width=14, height=2, bd=0, cursor="hand2", bg="#f59e0b", fg="white",
                                  activebackground="#d97706", activeforeground="white",
                                  command=self._toggle_task_mode)
        self.btn_task.pack(pady=10)
        
        self.lbl_score = tk.Label(left_panel, text="", font=("Segoe UI", 12), bg=BG_APP, fg="#64748b")
        self.lbl_score.pack(pady=5)

        # ЦЕНТР: Полотно для малювання (Квадрат)
        center_panel = tk.Frame(main, bg=BG_APP)
        center_panel.pack(side="left")

        # Розмір полотна підлаштуємо
        self.cv_size = 600
        self.canvas = tk.Canvas(center_panel, width=self.cv_size, height=self.cv_size, 
                                bg="white", highlightthickness=2, highlightbackground=C_BORDER)
        self.canvas.pack()
        
        # Події миші
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)

        # ПРАВА ПАНЕЛЬ: Інформація
        right_panel = tk.Frame(main, bg=BG_APP)
        right_panel.pack(side="left", fill="both", expand=True, padx=20)
        
        # Контейнер для завдання
        self.task_frame = tk.Frame(right_panel, bg=BG_APP)
        self.lbl_task_prompt = tk.Label(self.task_frame, text="", font=("Segoe UI", 20, "bold"), 
                                        bg=BG_APP, fg=C_ACCENT, wraplength=400)
        self.lbl_task_prompt.pack(pady=20)
        
        self.btn_check = tk.Button(self.task_frame, text="Перевірити", font=("Segoe UI", 16, "bold"),
                                   bg=C_GREEN, fg="white", bd=0, padx=20, pady=10, cursor="hand2",
                                   command=self._check_task)
        self.btn_check.pack(pady=20)
        self.lbl_result = tk.Label(self.task_frame, text="", font=("Segoe UI", 16, "bold"), bg=BG_APP)
        self.lbl_result.pack(pady=10)

        # Фрейм для відображення дробів (звичайний режим)
        self.info_container = tk.Frame(right_panel, bg=BG_APP)
        self.info_container.place(relx=0.5, rely=0.4, anchor="center")

        # ─── Вертикальний дріб (Чисельник, риска, Знаменник) ───
        self.frac_frame = tk.Frame(self.info_container, bg=BG_APP)
        self.frac_frame.pack(side="left", padx=10)
        
        self.lbl_num = tk.Label(self.frac_frame, text="0", 
                                font=("Segoe UI", 48, "bold"), bg=BG_APP, fg=C_ACCENT)
        self.lbl_num.pack(side="top")
        
        self.frac_line = tk.Frame(self.frac_frame, bg=C_ACCENT, height=4)
        self.frac_line.pack(side="top", fill="x", pady=5)
        
        self.lbl_den = tk.Label(self.frac_frame, text="10", 
                                font=("Segoe UI", 48, "bold"), bg=BG_APP, fg=C_ACCENT)
        self.lbl_den.pack(side="top")

        # ─── Дорівнює ───
        self.lbl_eq = tk.Label(self.info_container, text="=", 
                               font=("Segoe UI", 48), bg=BG_APP, fg="#64748b")
        self.lbl_eq.pack(side="left", padx=10)

        # ─── Десятковий запис ───
        self.lbl_decimal = tk.Label(self.info_container, text="0,0", 
                                    font=("Segoe UI", 72, "bold"), bg=BG_APP, fg=C_RED)
        self.lbl_decimal.pack(side="left", padx=10)

        self.lbl_text = tk.Label(right_panel, text="Нуль цілих, нуль десятих", 
                                 font=("Segoe UI", 20), bg=BG_APP, fg="#334155", wraplength=400)
        self.lbl_text.place(relx=0.5, rely=0.85, anchor="center")

    def set_mode(self, mode):
        self.mode = mode
        if not self.task_mode:
            self.value = 0
        
        # Стилізація кнопок
        btns = [self.btn_tenths, self.btn_hunds, self.btn_thous, self.btn_ten_thous]
        modes = ["tenths", "hundredths", "thousandths", "ten_thousandths"]
        
        for btn, m in zip(btns, modes):
            if m == mode:
                btn.config(bg=BG_HEADER, fg="white")
            else:
                btn.config(bg="white", fg=BG_HEADER)
            
        self._draw()
        if self.task_mode:
            self._new_task()
        else:
            self._update_text()

    def _get_grid_dims(self):
        if self.mode == "tenths": return 10, 1
        if self.mode == "hundredths": return 10, 10
        if self.mode == "thousandths": return 25, 40 # 1000 клітинок (25x40)
        if self.mode == "ten_thousandths": return 100, 100 # 10000 клітинок
        return 10, 1

    def _draw(self):
        self.canvas.delete("all")
        w = self.cv_size
        h = self.cv_size
        cols, rows = self._get_grid_dims()
        total = cols * rows
        
        cw = w / cols
        ch = h / rows
        
        # Оптимізоване малювання:
        # 1. Малюємо повні зафарбовані рядки одним блоком
        full_rows = self.value // cols
        rem_cols = self.value % cols
        
        if full_rows > 0:
            self.canvas.create_rectangle(0, 0, w, full_rows * ch, fill=C_HIGHLIGHT, outline="")
            
        if rem_cols > 0:
            y = full_rows * ch
            self.canvas.create_rectangle(0, y, rem_cols * cw, y + ch, fill=C_HIGHLIGHT, outline="")
            
        # 2. Малюємо сітку (лінії)
        # Якщо ліній забагато (10000), малюємо рідше або прозоріше?
        # Для 100x100 (10000) це нормально для Canvas
        
        line_color = "#bfdbfe"
        major_line_color = C_BORDER
        
        # Горизонтальні лінії
        step = 1
        if rows > 50: step = 1 # Малюємо всі, але тонкі
        
        for r in range(rows + 1):
            y = r * ch
            width = 1
            color = line_color
            
            # Для 10000 виділяємо кожні 10 ліній
            if self.mode == "ten_thousandths" and r % 10 == 0:
                width = 2
                color = major_line_color
            elif self.mode == "thousandths" and r % 5 == 0:
                 width = 2
                 color = major_line_color
            elif self.mode in ["tenths", "hundredths"]:
                width = 2
                color = major_line_color

            self.canvas.create_line(0, y, w, y, fill=color, width=width)

        # Вертикальні лінії
        for c in range(cols + 1):
            x = c * cw
            width = 1
            color = line_color
            
            if self.mode == "ten_thousandths" and c % 10 == 0:
                width = 2
                color = major_line_color
            elif self.mode == "thousandths" and c % 5 == 0:
                 width = 2
                 color = major_line_color
            elif self.mode in ["tenths", "hundredths"]:
                width = 2
                color = major_line_color
                
            self.canvas.create_line(x, 0, x, h, fill=color, width=width)
            
        # Текстові підписи для малих режимів
        if self.mode == "tenths":
            for i in range(self.value):
                self.canvas.create_text((i+0.5)*cw, h/2, text=str(i+1), font=("Arial", 14, "bold"), fill=C_ACCENT)

    def _on_click(self, event):
        self._process_input(event.x, event.y)

    def _on_drag(self, event):
        self._process_input(event.x, event.y)

    def _process_input(self, x, y):
        w = self.cv_size
        h = self.cv_size
        cols, rows = self._get_grid_dims()
        
        x = max(0, min(x, w - 1))
        y = max(0, min(y, h - 1))
        
        col = int(x // (w / cols))
        row = int(y // (h / rows))
        
        idx = row * cols + col + 1
        if idx != self.value:
            self.value = idx
            self._draw()
            if not self.task_mode:
                self._update_text()
            else:
                # В режимі завдання просто оновлюємо малюнок, але не текст відповіді (поки не натисне Перевірити)
                pass

    def _update_text(self):
        val = self.value
        cols, rows = self._get_grid_dims()
        total = cols * rows
        
        self.lbl_num.config(text=f"{val}")
        self.lbl_den.config(text=f"{total}")
        
        # Десятковий запис
        if total == 10:
            s_val = f"0,{val}" if val < 10 else "1,0"
            suffix = self._get_plural(val, "десята", "десяті", "десятих")
        elif total == 100:
            s_val = f"0,{val:02d}" if val < 100 else "1,00"
            suffix = self._get_plural(val, "сота", "соті", "сотих")
        elif total == 1000:
            s_val = f"0,{val:03d}" if val < 1000 else "1,000"
            suffix = self._get_plural(val, "тисячна", "тисячні", "тисячних")
        else: # 10000
            s_val = f"0,{val:04d}" if val < 10000 else "1,0000"
            suffix = self._get_plural(val, "десятитисячна", "десятитисячні", "десятитисячних")
            
        if val == total:
            s_val = "1"
            txt = "Одна ціла"
        elif val == 0:
            txt = "Нуль"
        else:
            txt = f"Нуль цілих, {self._number_name(val)} {suffix}"
            
        self.lbl_decimal.config(text=s_val)
        self.lbl_text.config(text=txt)

    def _toggle_task_mode(self):
        self.task_mode = not self.task_mode
        if self.task_mode:
            self.btn_task.config(text="❌ ВИЙТИ", bg=C_RED)
            self.info_container.place_forget()
            self.lbl_text.place_forget()
            self.task_frame.place(relx=0.5, rely=0.4, anchor="center")
            self._new_task()
        else:
            self.btn_task.config(text="🎓 ЗАВДАННЯ", bg="#f59e0b")
            self.task_frame.place_forget()
            self.info_container.place(relx=0.5, rely=0.4, anchor="center")
            self.lbl_text.place(relx=0.5, rely=0.85, anchor="center")
            self.value = 0
            self._draw()
            self._update_text()

    def _new_task(self):
        self.value = 0
        self._draw()
        self.lbl_result.config(text="")
        cols, rows = self._get_grid_dims()
        total = cols * rows
        
        # Генеруємо завдання
        self.target_value = random.randint(1, total - 1)
        
        # Формулюємо умову
        if total == 10:
            t_str = f"0,{self.target_value}"
        elif total == 100:
            t_str = f"0,{self.target_value:02d}"
        elif total == 1000:
            t_str = f"0,{self.target_value:03d}"
        else:
            t_str = f"0,{self.target_value:04d}"
            
        self.lbl_task_prompt.config(text=f"Завдання:\nПозначте на схемі число\n{t_str}")

    def _check_task(self):
        if self.value == self.target_value:
            self.lbl_result.config(text="✅ ПРАВИЛЬНО!", fg=C_GREEN)
            self.task_score += 1
            self.task_total += 1
            self.after(1000, self._new_task)
        else:
            self.lbl_result.config(text=f"❌ Помилка. Ви обрали {self.value}, треба {self.target_value}", fg=C_RED)
            self.task_total += 1
            
        self.lbl_score.config(text=f"Рахунок: {self.task_score}/{self.task_total}")

    def _get_plural(self, n, one, two_four, many):
        if n == 0: return many
        if n % 100 in (11, 12, 13, 14): return many
        last = n % 10
        if last == 1: return one
        if last in (2, 3, 4): return two_four
        return many

    def _number_name(self, n):
        # Базова конвертація (для демо можна розширити, але поки до 1000 достатньо цифрами якщо складно)
        # Для великих чисел краще писати цифрами, якщо текст задовгий
        if n > 9999: return str(n)
        return str(n) # Спрощення для великих чисел, щоб не писати гігантський конвертер слів

if __name__ == "__main__":
    app = DecimalIntroApp()
    app.mainloop()
