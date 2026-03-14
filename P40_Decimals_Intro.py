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
        self.title("Що таке десятковий дріб? (§ 40)")
        self.configure(bg=BG_APP)
        # Fullscreen
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

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
        header = tk.Frame(self, bg=BG_HEADER, height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        lbl_title = tk.Label(header, text="ДЕСЯТКОВІ ДРОБИ: ЗНАЙОМСТВО (§ 40)", 
                             font=("Segoe UI", 32, "bold"), bg=BG_HEADER, fg="white")
        lbl_title.pack(side="left", padx=30)
        
        # Кнопка виходу
        btn_exit = tk.Button(header, text="❌ ВИХІД", font=("Arial", 20, "bold"), bg="red", fg="white",
                             bd=0, activebackground="#ff4444", activeforeground="white",
                             command=self.destroy)
        btn_exit.pack(side="right", padx=20)

        # ─── ГОЛОВНА ОБЛАСТЬ ────────────────────────────────────────
        main = tk.Frame(self, bg=BG_APP)
        main.pack(expand=True, fill="both", padx=30, pady=30)

        # ЛІВА ПАНЕЛЬ: Кнопки вибору режиму
        left_panel = tk.Frame(main, bg=BG_APP)
        left_panel.pack(side="left", fill="y", padx=(0, 40))

        btn_font = ("Segoe UI", 20, "bold")
        
        self.btn_tenths = tk.Button(left_panel, text="Десяті\n(0,1)", font=btn_font,
                                    width=16, height=2, bd=0, cursor="hand2",
                                    command=lambda: self.set_mode("tenths"))
        self.btn_tenths.pack(pady=15)

        self.btn_hunds = tk.Button(left_panel, text="Соті\n(0,01)", font=btn_font,
                                   width=16, height=2, bd=0, cursor="hand2",
                                   command=lambda: self.set_mode("hundredths"))
        self.btn_hunds.pack(pady=15)

        self.btn_thous = tk.Button(left_panel, text="Тисячні\n(0,001)", font=btn_font,
                                   width=16, height=2, bd=0, cursor="hand2",
                                   command=lambda: self.set_mode("thousandths"))
        self.btn_thous.pack(pady=15)

        self.btn_ten_thous = tk.Button(left_panel, text="Дес-тисячні\n(0,0001)", font=btn_font,
                                       width=16, height=2, bd=0, cursor="hand2",
                                       command=lambda: self.set_mode("ten_thousandths"))
        self.btn_ten_thous.pack(pady=15)
        
        tk.Frame(left_panel, bg=C_BORDER, height=4).pack(fill="x", pady=30)
        
        self.btn_task = tk.Button(left_panel, text="🎓 ЗАВДАННЯ", font=btn_font,
                                  width=16, height=2, bd=0, cursor="hand2", bg="#f59e0b", fg="white",
                                  activebackground="#d97706", activeforeground="white",
                                  command=self._toggle_task_mode)
        self.btn_task.pack(pady=15)
        
        self.lbl_score = tk.Label(left_panel, text="", font=("Segoe UI", 18), bg=BG_APP, fg="#64748b")
        self.lbl_score.pack(pady=10)

        # ЦЕНТР: Полотно для малювання (Квадрат)
        center_panel = tk.Frame(main, bg=BG_APP)
        center_panel.pack(side="left", fill="both", expand=True)
        
        self.canvas = tk.Canvas(center_panel, bg="white", highlightthickness=2, highlightbackground=C_BORDER)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._draw_grid)
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_click) # Малювання протягуванням

        # ПРАВА ПАНЕЛЬ: Відображення числа
        right_panel = tk.Frame(main, bg=BG_APP, width=300)
        right_panel.pack(side="right", fill="y", padx=(40, 0))
        right_panel.pack_propagate(False)

        tk.Label(right_panel, text="Звичайний дріб:", font=("Segoe UI", 18), bg=BG_APP, fg=C_ACCENT).pack(pady=(0, 10))
        self.lbl_fraction = tk.Label(right_panel, text="0 / 10", font=("Courier New", 40, "bold"), bg="white", fg=C_ACCENT, width=10, relief="solid")
        self.lbl_fraction.pack(pady=(0, 40))

        tk.Label(right_panel, text="Десятковий дріб:", font=("Segoe UI", 18), bg=BG_APP, fg=C_RED).pack(pady=(0, 10))
        self.lbl_decimal = tk.Label(right_panel, text="0.0", font=("Courier New", 50, "bold"), bg="white", fg=C_RED, width=8, relief="solid")
        self.lbl_decimal.pack(pady=(0, 40))
        
        self.lbl_message = tk.Label(right_panel, text="", font=("Segoe UI", 16, "bold"), bg=BG_APP, wraplength=280)
        self.lbl_message.pack(pady=20)
        
        # Кнопка очищення
        tk.Button(right_panel, text="🗑 Очистити", font=("Segoe UI", 16), bg="#e2e8f0", 
                  command=self._clear).pack(side="bottom", fill="x", pady=20)

    def set_mode(self, mode):
        self.mode = mode
        
        # Стилі кнопок
        def reset_btns():
            for b in [self.btn_tenths, self.btn_hunds, self.btn_thous, self.btn_ten_thous]:
                b.configure(bg="#e0f2fe", fg=C_ACCENT)
                
        reset_btns()
        if mode == "tenths": self.btn_tenths.configure(bg=C_ACCENT, fg="white")
        elif mode == "hundredths": self.btn_hunds.configure(bg=C_ACCENT, fg="white")
        elif mode == "thousandths": self.btn_thous.configure(bg=C_ACCENT, fg="white")
        elif mode == "ten_thousandths": self.btn_ten_thous.configure(bg=C_ACCENT, fg="white")
            
        self._clear()
        
    def _clear(self):
        self.value = 0
        self._update_display()
        self._draw_grid()
        
    def _toggle_task_mode(self):
        self.task_mode = not self.task_mode
        if self.task_mode:
            self.btn_task.configure(text="❌ Зупинити", bg=C_RED)
            self.task_score = 0
            self.task_total = 0
            self._new_task()
        else:
            self.btn_task.configure(text="🎓 ЗАВДАННЯ", bg="#f59e0b")
            self.lbl_message.configure(text="")
            self.lbl_score.configure(text="")
            
    def _new_task(self):
        total_cells = self._get_total_cells()
        self.target_value = random.randint(1, total_cells)
        
        # Формуємо текст завдання
        denom = total_cells
        dec_val = self.target_value / denom
        
        # 50% шанс запитати десятковим або звичайним
        if random.random() < 0.5:
            txt = f"Зафарбуй: {self._fmt_dec(dec_val)}"
        else:
            txt = f"Зафарбуй: {self.target_value}/{denom}"
            
        self.lbl_message.configure(text=txt, fg="#f59e0b")
        self._clear()

    def _get_total_cells(self):
        if self.mode == "tenths": return 10
        if self.mode == "hundredths": return 100
        if self.mode == "thousandths": return 1000
        if self.mode == "ten_thousandths": return 10000
        return 10

    def _draw_grid(self, event=None):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        # Відступи
        pad = 20
        avail_w = w - 2*pad
        avail_h = h - 2*pad
        
        # Розмір сітки (квадратна)
        size = min(avail_w, avail_h)
        x0 = (w - size) // 2
        y0 = (h - size) // 2
        
        self.grid_x0 = x0
        self.grid_y0 = y0
        self.grid_size = size
        
        rows, cols = 1, 1
        if self.mode == "tenths": rows, cols = 10, 1
        elif self.mode == "hundredths": rows, cols = 10, 10
        elif self.mode == "thousandths": rows, cols = 20, 50 # 1000 = 20x50
        elif self.mode == "ten_thousandths": rows, cols = 100, 100
        
        self.rows = rows
        self.cols = cols
        
        self.cell_w = size / cols
        self.cell_h = size / rows
        
        # Малюємо зафарбовані
        filled = self.value
        for i in range(filled):
            r = i // cols
            c = i % cols
            # Для тисячних заповнюємо інакше для краси? Ні, просто послідовно
            
            x1 = x0 + c * self.cell_w
            y1 = y0 + r * self.cell_h
            x2 = x1 + self.cell_w
            y2 = y1 + self.cell_h
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=C_HIGHLIGHT, outline="")
            
        # Малюємо сітку
        # Якщо занадто дрібна (ten_thousandths), не малюємо всі лінії, тільки рамку
        if self.mode == "ten_thousandths":
             self.canvas.create_rectangle(x0, y0, x0+size, y0+size, outline=C_BORDER, width=2)
        else:
            for r in range(rows + 1):
                y = y0 + r * self.cell_h
                self.canvas.create_line(x0, y, x0+size, y, fill=C_BORDER)
            for c in range(cols + 1):
                x = x0 + c * self.cell_w
                self.canvas.create_line(x, y0, x, y0+size, fill=C_BORDER)

    def _on_click(self, event):
        # Визначаємо клітинку
        if not hasattr(self, 'grid_size'): return
        
        x = event.x - self.grid_x0
        y = event.y - self.grid_y0
        
        if x < 0 or y < 0 or x > self.grid_size or y > self.grid_size:
            return
            
        c = int(x / self.cell_w)
        r = int(y / self.cell_h)
        
        idx = r * self.cols + c + 1
        
        # Обмежуємо
        total = self.rows * self.cols
        if idx > total: idx = total
        
        self.value = idx
        self._update_display()
        self._draw_grid()
        
        if self.task_mode:
            self._check_task()

    def _update_display(self):
        total = self.rows * self.cols
        
        # Дріб
        self.lbl_fraction.configure(text=f"{self.value}\n---\n{total}")
        
        # Десятковий
        val = self.value / total
        self.lbl_decimal.configure(text=self._fmt_dec(val))

    def _fmt_dec(self, val):
        s = f"{val:.10f}".rstrip('0').rstrip('.')
        if s == "0": s = "0.0"
        return s

    def _check_task(self):
        if self.value == self.target_value:
            self.task_score += 1
            self.task_total += 1
            self.lbl_message.configure(text="✅ Правильно!", fg=C_GREEN)
            self.lbl_score.configure(text=f"Рахунок: {self.task_score} / {self.task_total}")
            self.after(1000, self._new_task)

if __name__ == "__main__":
    app = DecimalIntroApp()
    app.mainloop()
