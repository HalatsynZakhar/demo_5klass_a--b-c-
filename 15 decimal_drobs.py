"""
Інтерактивний тренажер: Десяткові дроби (Покращена версія)
Спеціально для інтерактивної дошки: Великий шрифт, зручне керування дотиком.
"""
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Wedge
import numpy as np
import math

# ══════════════════════════════════════════════════════════════════
#  НАЛАШТУВАННЯ СТИЛЮ
# ══════════════════════════════════════════════════════════════════
BG       = "#F8FAFC"       # Світлий фон
SURFACE  = "#FFFFFF"       # Білий фон карток
SRF2     = "#F1F5F9"       # Світло-сірий фон елементів
BORDER   = "#CBD5E1"       # Колір рамок
C_BLUE   = "#2563EB"       # Основний акцент (синій)
C_CYAN   = "#0891B2"       # Додатковий (бірюзовий)
C_RED    = "#DC2626"       # Акцент (червоний)
C_GREEN  = "#16A34A"       # Акцент (зелений)
C_PURP   = "#7C3AED"       # Акцент (фіолетовий)
C_ORANGE = "#EA580C"       # Акцент (помаранчевий)
TEXT     = "#0F172A"       # Основний текст
TEXT2    = "#334155"       # Другорядний текст
TEXT3    = "#64748B"       # Третій рівень тексту

PLACE_COLORS = [TEXT, C_BLUE, C_CYAN, C_GREEN, C_PURP, C_ORANGE]
PLACE_NAMES  = ["Одиниці", "Десяті", "Соті", "Тисячні", "Дес-тис.", "Сто-тис."]
PLACE_MULTS  = ["x1", "x0,1", "x0,01", "x0,001", "x0,0001", "x0,00001"]

# Шрифти адаптовані для великого екрану
FONT_UI      = ("Segoe UI", 16)
FONT_UI_BOLD = ("Segoe UI", 16, "bold")
FONT_NUM     = ("Courier New", 32, "bold")
FONT_BIG     = ("Courier New", 72, "bold")
FONT_TITLE   = ("Segoe UI", 20, "bold")
FONT_SMALL   = ("Segoe UI", 14)

PLT = {
    "figure.facecolor": SURFACE,
    "axes.facecolor":   BG,
    "text.color":       TEXT,
    "axes.labelcolor":  TEXT2,
    "xtick.color":      TEXT2,
    "ytick.color":      TEXT2,
    "axes.edgecolor":   BORDER,
    "axes.titlecolor":  TEXT,
    "grid.color":       "#E2E8F0",
    "font.family":      "sans-serif",
    "font.size":        14,
    "axes.titlesize":   18,
    "axes.labelsize":   14,
    "xtick.labelsize":  12,
    "ytick.labelsize":  12,
}

# ══════════════════════════════════════════════════════════════════
#  УТИЛІТИ
# ══════════════════════════════════════════════════════════════════
def get_frac_parts(val, places):
    # Повертаємо дріб без спрощення, що відповідає кількості знаків
    d = 10 ** places
    n = int(round(val * d))
    
    int_part = n // d
    frac_n   = n % d
    
    return int_part, frac_n, d

def num_name(digits, places):
    int_p = digits[0]
    limit = min(places + 1, len(digits))
    
    # Збираємо дробову частину як рядок
    dec_digits = digits[1:limit]
    if not dec_digits:
        dec_s = ""
    else:
        dec_s = "".join(map(str, dec_digits))
    
    parts = []
    
    # Ціла частина
    if int_p == 0:
        parts.append("нуль цілих")
    else:
        parts.append(f"{int_p} {'ціла' if int_p==1 else 'цілих'}")

    # Дробова частина
    if dec_s and int(dec_s) > 0:
        n = int(dec_s)
        pos = len(dec_s)
        pn = {1:"десятих", 2:"сотих", 3:"тисячних", 4:"десятитисячних", 5:"стотисячних"}.get(pos, "")
        parts.append(f"{n} {pn}")
    
    return " ".join(parts)

def fmt(val, places):
    """Форматує число з комою."""
    return f"{val:.{places}f}".replace(".", ",")

def digits_to_val(digits):
    v = float(digits[0])
    for i in range(1, 6):
        if i < len(digits):
            v += digits[i] * (10**-i)
    return round(v, 5)

# ══════════════════════════════════════════════════════════════════
#  ГОЛОВНИЙ КЛАС
# ══════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Десяткові дроби — Інтерактивна дошка")
        self.configure(bg=BG)
        # Спробувати відкрити на весь екран
        try:    self.state("zoomed")
        except: self.attributes("-fullscreen", True) # Альтернатива для Linux/Mac

        plt.rcParams.update(PLT)

        # Стан
        self.digits = [0, 7, 5, 0, 0, 0] # [int, d1, d2, d3, d4, d5]
        self.places = 2

        # Стан візуалізації
        self.zoom_range  = 1.0
        self.zoom_center = 0.75
        self._drag_x0    = None
        self._drag_c0    = None
        
        # Лічильник
        self.ctr_val  = 0.0
        self.ctr_hist = [0.0]
        self._ctr_step_var = tk.StringVar(value="0.1")

        # Порівняння
        self.cmp_mode = False
        self.cmp_digits_b = [0, 5, 0, 0, 0, 0]

        self._setup_styles()
        self._build_ui()
        
        # Ініціалізація елементів керування
        self._digit_labels = []
        self._set_places(self.places)
        
        # Запуск першого оновлення
        self.after(100, self._full_refresh)

    def _setup_styles(self):
        st = ttk.Style(self)
        st.theme_use("clam")
        st.configure("TFrame", background=BG)
        st.configure("TLabel", background=BG, foreground=TEXT, font=FONT_UI)
        st.configure("Big.TButton", font=("Segoe UI", 14, "bold"), padding=10)

    # ══ UI БУДІВНИЦТВО ════════════════════════════════════════════
    def _build_ui(self):
        self.columnconfigure(0, minsize=500, weight=0) # Ліва панель ширша
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._build_left()
        self._build_right()

    def _build_left(self):
        self._left = tk.Frame(self, bg=SURFACE, highlightbackground=BORDER, highlightthickness=1)
        self._left.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Scrollable container setup
        canvas = tk.Canvas(self._left, bg=SURFACE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self._left, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=SURFACE)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Вміст лівої панелі ---
        pad_opts = {'padx': 25, 'pady': 10}
        
        # 1. Заголовок і число
        tk.Label(self.scrollable_frame, text="ЧИСЛО", bg=SURFACE, fg=TEXT3, font=FONT_SMALL).pack(anchor="w", **pad_opts)
        
        disp_frame = tk.Frame(self.scrollable_frame, bg=SRF2, padx=15, pady=15)
        disp_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Велике число
        num_c = tk.Frame(disp_frame, bg=SRF2)
        num_c.pack()
        self.lbl_int = tk.Label(num_c, text="0", bg=SRF2, fg=TEXT, font=FONT_BIG)
        self.lbl_int.pack(side="left")
        self.lbl_dot = tk.Label(num_c, text=",", bg=SRF2, fg=TEXT3, font=FONT_BIG)
        self.lbl_dot.pack(side="left")
        self.lbl_dec = tk.Label(num_c, text="00", bg=SRF2, fg=C_BLUE, font=FONT_BIG)
        self.lbl_dec.pack(side="left")

        # Текстова назва
        self.lbl_name = tk.Label(disp_frame, text="", bg=SRF2, fg=TEXT2, 
                                 font=("Segoe UI", 16, "italic"), wraplength=450, justify="center")
        self.lbl_name.pack(pady=(10,0))

        # 2. Вибір точності
        tk.Label(self.scrollable_frame, text="КІЛЬКІСТЬ ЗНАКІВ (ТОЧНІСТЬ)", bg=SURFACE, fg=TEXT3, font=FONT_SMALL).pack(anchor="w", padx=25)
        
        prec_frame = tk.Frame(self.scrollable_frame, bg=SURFACE)
        prec_frame.pack(fill="x", padx=20, pady=(5, 20))
        
        self._place_btns = []
        labels = ["1", "2", "3", "4", "5"]
        for i, txt in enumerate(labels):
            btn = tk.Button(prec_frame, text=txt, font=("Segoe UI", 14, "bold"),
                            bg=SRF2, fg=TEXT, relief="flat", bd=0, cursor="hand2",
                            activebackground=C_BLUE, activeforeground="white",
                            width=3, height=1,
                            command=lambda n=i+1: self._set_places(n))
            btn.pack(side="left", padx=4, fill="x", expand=True)
            self._place_btns.append(btn)

        # 3. Керування розрядами
        tk.Label(self.scrollable_frame, text="ЗМІНА РОЗРЯДІВ", bg=SURFACE, fg=TEXT3, font=FONT_SMALL).pack(anchor="w", padx=25)
        
        self._controls_frame = tk.Frame(self.scrollable_frame, bg=SURFACE)
        self._controls_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # 4. Звичайний дріб (Шкільний формат)
        tk.Label(self.scrollable_frame, text="ЯК ЗВИЧАЙНИЙ ДРІБ", bg=SURFACE, fg=TEXT3, font=FONT_SMALL).pack(anchor="w", padx=25, pady=(20, 5))
        
        self._frac_frame = tk.Frame(self.scrollable_frame, bg=SRF2, padx=20, pady=15)
        self._frac_frame.pack(fill="x", padx=20, pady=5)
        
        # Контейнер для центрування
        container = tk.Frame(self._frac_frame, bg=SRF2)
        container.pack()

        # Ціла частина
        self.lbl_frac_int = tk.Label(container, text="", bg=SRF2, fg=C_CYAN, font=("Courier New", 48, "bold"))
        self.lbl_frac_int.pack(side="left", padx=(0, 20))
        
        # Дробова частина (вертикальний стос)
        self.frac_stack = tk.Frame(container, bg=SRF2)
        self.frac_stack.pack(side="left")

        self.lbl_frac_n = tk.Label(self.frac_stack, text="0", bg=SRF2, fg=C_CYAN, font=("Courier New", 28, "bold"))
        self.lbl_frac_n.pack()
        
        self.lbl_frac_line = tk.Frame(self.frac_stack, bg=C_CYAN, height=4, width=80)
        self.lbl_frac_line.pack(pady=4, fill="x")
        
        self.lbl_frac_d = tk.Label(self.frac_stack, text="1", bg=SRF2, fg=C_CYAN, font=("Courier New", 28, "bold"))
        self.lbl_frac_d.pack()

    def _build_right(self):
        right = tk.Frame(self, bg=BG)
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Верхня панель режимів (Custom Tabs)
        self._tab_frame = tk.Frame(right, bg=BG)
        self._tab_frame.pack(fill="x", side="top", pady=(0, 15))
        
        self._current_tab_idx = 0
        self._tab_btns = []
        # Назви режимів українською
        tab_names = ["📏 Пряма", "🟦 Сітка", "🥧 Торт", "🔢 Розряди", "⚖ Порівняння"]
        
        for i, txt in enumerate(tab_names):
            btn = tk.Button(self._tab_frame, text=txt, font=("Segoe UI", 12, "bold"),
                            bg=SRF2, fg=TEXT2, relief="flat", padx=20, pady=10, cursor="hand2",
                            activebackground=C_BLUE, activeforeground="white",
                            command=lambda idx=i: self._switch_tab(idx))
            btn.pack(side="left", padx=5, fill="x", expand=True)
            self._tab_btns.append(btn)
            
        # Панель інструментів (для порівняння)
        self._toolbar = tk.Frame(right, bg=SRF2, height=0)
        self._toolbar.pack(fill="x", side="top", pady=0)
        
        # Область графіку Matplotlib
        self.fig = plt.figure(figsize=(10, 8), facecolor=SURFACE)
        self.mpl = FigureCanvasTkAgg(self.fig, master=right)
        self.mpl_widget = self.mpl.get_tk_widget()
        self.mpl_widget.configure(bg=SURFACE, highlightthickness=0)
        self.mpl_widget.pack(fill="both", expand=True, side="top")
        
        # Прив'язка подій для інтерактивності (зум, перетягування)
        self.mpl_widget.bind("<MouseWheel>",      self._wheel)
        self.mpl_widget.bind("<Button-4>",        self._wheel) # Linux scroll up
        self.mpl_widget.bind("<Button-5>",        self._wheel) # Linux scroll down
        self.mpl_widget.bind("<ButtonPress-1>",   self._drag_start)
        self.mpl_widget.bind("<B1-Motion>",       self._drag_move)
        self.mpl_widget.bind("<ButtonRelease-1>", self._drag_end)

        self._switch_tab(0)

    # ══ ЛОГІКА ІНТЕРФЕЙСУ ═════════════════════════════════════════
    def _switch_tab(self, idx):
        self._current_tab_idx = idx
        # Оновлення стилю кнопок
        for i, btn in enumerate(self._tab_btns):
            if i == idx:
                btn.config(bg=C_BLUE, fg="white", relief="sunken")
            else:
                btn.config(bg=SRF2, fg=TEXT2, relief="flat")
        
        # Керування тулбаром
        for w in self._toolbar.winfo_children(): w.destroy()
        
        if idx == 4: # Порівняння
            self.cmp_mode = True
            self._build_cmp_toolbar()
            self._toolbar.pack(fill="x", pady=(0, 15))
        else:
            self.cmp_mode = False
            self._toolbar.pack_forget()
            
        self._redraw()

    def _set_places(self, n):
        # Обрізаємо або додаємо нулі
        for i in range(n + 1, 6):
            self.digits[i] = 0
        self.places = n
        
        # Оновлення кнопок точності
        for i, btn in enumerate(self._place_btns):
            if i == n - 1:
                btn.config(bg=C_BLUE, fg="white")
            else:
                btn.config(bg=SRF2, fg=TEXT)
                
        self._rebuild_controls()
        self._full_refresh()

    def _rebuild_controls(self):
        # Очищаємо старі контроли
        for w in self._controls_frame.winfo_children(): w.destroy()
        
        self._digit_labels = []
        
        # Створюємо рядки для кожного активного розряду
        for i in range(self.places + 1):
            color = PLACE_COLORS[i]
            
            # Контейнер рядка
            row = tk.Frame(self._controls_frame, bg=SRF2, pady=8, padx=10)
            row.pack(fill="x", pady=4)
            
            # Назва розряду (зліва)
            lbl_name = tk.Label(row, text=PLACE_NAMES[i], width=12, anchor="w",
                                bg=SRF2, fg=TEXT2, font=("Segoe UI", 14))
            lbl_name.pack(side="left")
            
            # Кнопка "-"
            btn_minus = tk.Button(row, text="−", font=("Arial", 20, "bold"), 
                                  bg=SURFACE, fg=TEXT, width=3, bd=0, cursor="hand2",
                                  activebackground="#fee2e2",
                                  command=lambda idx=i: self._change_digit(idx, -1))
            btn_minus.pack(side="left", padx=10)
            
            # Цифра
            lbl_digit = tk.Label(row, text=str(self.digits[i]), font=("Courier New", 32, "bold"),
                                 width=2, bg=SRF2, fg=color)
            lbl_digit.pack(side="left", padx=10)
            self._digit_labels.append(lbl_digit)
            
            # Кнопка "+"
            btn_plus = tk.Button(row, text="+", font=("Arial", 20, "bold"), 
                                 bg=SURFACE, fg=TEXT, width=3, bd=0, cursor="hand2",
                                 activebackground="#dcfce7",
                                 command=lambda idx=i: self._change_digit(idx, 1))
            btn_plus.pack(side="left", padx=10)
            
            # Множник (справа)
            tk.Label(row, text=PLACE_MULTS[i], bg=SRF2, fg=TEXT3, font=("Segoe UI", 12)).pack(side="right", padx=10)

    def _change_digit(self, idx, delta):
        # Перетворення в ціле число на основі максимальної точності (5 знаків)
        # precision factor = 100,000
        factor = 100000
        
        current_val = self.digits[0] * factor
        for i in range(1, 6):
            w = 10**(5-i)
            current_val += self.digits[i] * w
        
        # Визначаємо вагу зміни
        if idx == 0:
            change = delta * factor
        else:
            change = delta * (10**(5-idx))
            
        new_val = current_val + change
        
        if new_val < 0: return # Не дозволяємо від'ємні числа
        if new_val > 4 * factor: return # Обмеження до 4.0
        
        # Конвертуємо назад у цифри
        new_int = new_val // factor
        rem = new_val % factor
        
        self.digits[0] = new_int
        
        for i in range(1, 6):
            w = 10**(5-i)
            d = rem // w
            self.digits[i] = d
            rem %= w
            
        self._full_refresh()

    def _full_refresh(self):
        # 1. Оновлення дисплею числа
        val = digits_to_val(self.digits)
        int_p = self.digits[0]
        dec_p = "".join(str(self.digits[i]) for i in range(1, self.places+1))
        
        self.lbl_int.config(text=str(int_p))
        self.lbl_dec.config(text=dec_p)
        self.lbl_name.config(text=num_name(self.digits, self.places))
        
        # 2. Оновлення звичайного дробу
        int_v, n, d = get_frac_parts(val, self.places)
        
        if int_v > 0:
            self.lbl_frac_int.config(text=str(int_v))
            self.lbl_frac_int.pack(side="left", before=self.frac_stack, padx=(0, 20)) # Ensure visible
        else:
            self.lbl_frac_int.config(text="")
            self.lbl_frac_int.pack_forget()
            
        self.lbl_frac_n.config(text=str(n))
        self.lbl_frac_d.config(text=str(d))
        
        # 3. Оновлення цифр в контролах
        for i, lbl in enumerate(self._digit_labels):
            if i < len(self.digits):
                lbl.config(text=str(self.digits[i]))
        
        # 4. Перемальовування графіку
        self._redraw()

    # ══ ІНСТРУМЕНТИ ПОРІВНЯННЯ ════════════════════════════════════
    def _build_cmp_toolbar(self):
        f = self._toolbar
        
        # Панель для числа B
        tk.Label(f, text="ЧИСЛО B:", fg=C_GREEN, bg=SRF2, font=FONT_UI_BOLD).pack(side="left", padx=20)
        
        # Кнопки зміни числа B
        # Для простоти зробимо +/- для кожного розряду? Ні, це занадто багато кнопок.
        # Зробимо кнопку "Копіювати з А" і прості +/- 0.1, 0.01
        
        tk.Button(f, text="Копіювати А", font=FONT_UI, bg=SURFACE, command=self._copy_a_to_b).pack(side="left", padx=10)
        
        tk.Button(f, text="-0,1", font=FONT_UI, command=lambda: self._change_b(1, -1)).pack(side="left", padx=2)
        tk.Button(f, text="+0,1", font=FONT_UI, command=lambda: self._change_b(1, 1)).pack(side="left", padx=2)
        tk.Label(f, text=" | ", bg=SRF2).pack(side="left")
        tk.Button(f, text="-0,01", font=FONT_UI, command=lambda: self._change_b(2, -1)).pack(side="left", padx=2)
        tk.Button(f, text="+0,01", font=FONT_UI, command=lambda: self._change_b(2, 1)).pack(side="left", padx=2)

    def _copy_a_to_b(self):
        for i in range(len(self.digits)):
            self.cmp_digits_b[i] = self.digits[i]
        self._redraw()

    def _change_b(self, idx, delta):
        # Аналогічно, перетворення B в ціле число
        factor = 100000
        current_val = self.cmp_digits_b[0] * factor
        for i in range(1, 6):
            w = 10**(5-i)
            current_val += self.cmp_digits_b[i] * w
            
        if idx == 0:
            change = delta * factor
        else:
            change = delta * (10**(5-idx))
            
        new_val = current_val + change
        if new_val < 0: return
        if new_val > 4 * factor: return

        # Конвертуємо назад
        new_int = new_val // factor
        rem = new_val % factor
        self.cmp_digits_b[0] = new_int
        
        for i in range(1, 6):
            w = 10**(5-i)
            d = rem // w
            self.cmp_digits_b[i] = d
            rem %= w
            
        self._redraw()

    # ══ ВІЗУАЛІЗАЦІЯ ══════════════════════════════════════════════
    def _redraw(self):
        self.fig.clear()
        idx = self._current_tab_idx
        
        methods = [self._draw_line, self._draw_grid, self._draw_pie,
                   self._draw_place, self._draw_cmp]
        
        if 0 <= idx < len(methods):
            methods[idx]()
            
        self.mpl.draw_idle()

    # ── 1. ЧИСЛОВА ПРЯМА ──────────────────────────────────────────
    def _draw_line(self):
        val = digits_to_val(self.digits)
        if self._drag_x0 is None: self.zoom_center = val

        half  = self.zoom_range / 2
        start = max(0.0, self.zoom_center - half)
        end   = start + self.zoom_range
        
        # Автоматичний крок
        step = 1.0
        if self.zoom_range < 0.0005: step = 0.00001
        elif self.zoom_range < 0.005: step = 0.0001
        elif self.zoom_range < 0.05: step = 0.001
        elif self.zoom_range < 0.5: step = 0.01
        elif self.zoom_range < 5: step = 0.1
        
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(BG)
        ax.set_xlim(start - self.zoom_range*0.05, end + self.zoom_range*0.05)
        ax.set_ylim(-1, 1)
        ax.axis("off") # Вимикаємо стандартні осі

        # Малюємо поділки
        # Знаходимо першу поділку
        t = math.floor(start / step) * step
        while t <= end + step:
            # Округлення для уникнення float помилок
            t_r = round(t, 6)
            
            if start <= t_r <= end:
                # Визначаємо тип поділки (ціла, десята, сота...)
                is_int = abs(t_r - round(t_r)) < 1e-9
                
                # Висота і стиль
                if is_int:
                    hh, col, lw = 0.4, TEXT, 3
                    fsize = 16
                else:
                    hh, col, lw = 0.2, TEXT2, 1.5
                    fsize = 12
                
                ax.plot([t_r, t_r], [-hh, hh], color=col, lw=lw)
                
                # Підпис
                # Показуємо підпис, якщо це "красиве" число або зум дозволяє
                should_label = is_int or (self.zoom_range < step * 15)
                if should_label:
                    lbl = fmt(t_r, 5).rstrip("0").rstrip(",") if not is_int else str(int(t_r))
                    ax.text(t_r, -hh - 0.1, lbl, ha="center", va="top", color=col, fontsize=fsize)
            
            t += step

        # Головна лінія
        ax.axhline(0, color=TEXT2, lw=2)
        
        # Поточне значення (Точка)
        ax.plot(val, 0, "o", color=C_BLUE, markersize=20, zorder=10,
                markeredgecolor="white", markeredgewidth=3)
        
        # Підпис над точкою
        ax.text(val, 0.5, fmt(val, self.places), ha="center", va="bottom",
                color=C_BLUE, fontsize=24, fontweight="bold", 
                bbox=dict(facecolor="white", edgecolor=C_BLUE, boxstyle="round,pad=0.5"))

    # ── 2. СІТКА (Квадрати 10х10) ─────────────────────────────────
    def _draw_grid(self):
        val = digits_to_val(self.digits)
        int_part = int(val)
        frac_part = val - int_part
        
        # Скільки квадратів малювати?
        # Якщо число 2.35 -> Малюємо 2 повних + 1 частковий
        total_grids = int_part + 1 if frac_part > 0 or int_part == 0 else int_part
        if total_grids == 0: total_grids = 1
        
        gs = gridspec.GridSpec(1, total_grids, figure=self.fig)
        
        for i in range(total_grids):
            ax = self.fig.add_subplot(gs[i])
            ax.set_aspect("equal")
            ax.axis("off")
            
            # Визначаємо заповнення
            if i < int_part:
                fill_count = 100
                title = f"Ціла #{i+1}"
                color = C_BLUE
            elif i == int_part:
                fill_count = int(round(frac_part * 100))
                # Використовуємо LaTeX для вертикального дробу
                title = f"Дробова: $\\frac{{{fill_count}}}{{100}}$"
                color = C_CYAN
            else:
                fill_count = 0
                title = ""
                color = SRF2
                
            ax.set_title(title, fontsize=16, color=TEXT2)
            
            # Малюємо сітку 10х10
            for cell in range(100):
                r = 9 - (cell // 10)
                c = cell % 10
                is_filled = cell < fill_count
                
                fc = color if is_filled else "white"
                rect = Rectangle((c, r), 1, 1, facecolor=fc, edgecolor=BORDER)
                ax.add_patch(rect)
            
            ax.set_xlim(-0.5, 10.5)
            ax.set_ylim(-0.5, 10.5)

    # ── 3. ТОРТ (Кругова діаграма) ────────────────────────────────
    def _draw_pie(self):
        val = digits_to_val(self.digits)
        int_part = int(val)
        frac = val - int_part
        
        # Визначаємо скільки "тортів" нам потрібно
        # Якщо є дробова частина, то int_part + 1, інакше int_part
        total_pies = int_part + 1 if frac > 0 or int_part == 0 else int_part
        if total_pies == 0: total_pies = 1 # Мінімум один для 0
        
        gs = gridspec.GridSpec(1, total_pies, figure=self.fig)
        
        for i in range(total_pies):
            ax = self.fig.add_subplot(gs[i])
            ax.set_aspect("equal")
            ax.axis("off")
            
            radius = 1.0
            
            # Фон (білий круг з рамкою)
            ax.add_patch(Circle((0,0), radius, facecolor="white", edgecolor=BORDER, lw=2))
            
            # Логіка заповнення
            if i < int_part:
                # Повний торт
                ax.add_patch(Circle((0,0), radius, facecolor=C_BLUE, edgecolor="white"))
                ax.text(0, -1.3, "1 ціла", ha="center", fontsize=20, color=TEXT2)
            else:
                # Дробова частина
                if frac > 0:
                    angle = 360 * frac
                    w = Wedge((0,0), radius, 90 - angle, 90, facecolor=C_CYAN, edgecolor="white")
                    ax.add_patch(w)
                    ax.text(0, -1.3, f"{fmt(frac, self.places)}", ha="center", fontsize=24, fontweight="bold", color=C_CYAN)
                    
                    # Підказка про дріб
                    self._draw_fraction_hint(ax, frac)
                else:
                    ax.text(0, 0, "0", ha="center", va="center", fontsize=40, color=TEXT3)

            ax.set_xlim(-1.2, 1.2)
            ax.set_ylim(-1.5, 1.2)

    def _draw_fraction_hint(self, ax, frac):
        common_fractions = {
            0.5: (1, 2), 0.25: (1, 4), 0.75: (3, 4), 
            0.2: (1, 5), 0.4: (2, 5), 0.6: (3, 5), 0.8: (4, 5),
            0.1: (1, 10)
        }
        
        closest = None
        min_diff = 0.001
        for v, (n, d) in common_fractions.items():
            if abs(v - frac) < min_diff:
                closest = (n, d)
                break
        
        if closest:
            n, d = closest
            # LaTeX для вертикального дробу
            ax.text(0, 0, f"$\\frac{{{n}}}{{{d}}}$", ha="center", va="center", fontsize=36, color="white", fontweight="bold")

    # ── 4. РОЗРЯДИ (Таблиця) ──────────────────────────────────────
    def _draw_place(self):
        n = self.places + 1 # 0 (int) + decimals
        
        gs = gridspec.GridSpec(1, n, figure=self.fig, wspace=0.05)
        
        for i in range(n):
            ax = self.fig.add_subplot(gs[i])
            ax.axis("off")
            ax.set_ylim(0, 1)
            
            val = self.digits[i]
            col = PLACE_COLORS[i]
            bg_col = SRF2
            
            # Рамка картки
            rect = FancyBboxPatch((0.05, 0.1), 0.9, 0.8, boxstyle="round,pad=0.02", 
                                  facecolor=bg_col, edgecolor=BORDER)
            ax.add_patch(rect)
            
            # Назва
            ax.text(0.5, 0.8, PLACE_NAMES[i], ha="center", color=TEXT3, fontsize=14, fontweight="bold")
            
            # Цифра
            ax.text(0.5, 0.5, str(val), ha="center", va="center", 
                    color=col, fontsize=60, fontweight="bold")
            
            # Значення (x0.1)
            ax.text(0.5, 0.2, PLACE_MULTS[i], ha="center", color=TEXT2, fontsize=14, zorder=10)
            
            # Кома після цілих
            if i == 0:
                ax.text(1.1, 0.3, ",", ha="center", fontsize=80, fontweight="bold", transform=ax.transAxes, zorder=20)

    # ── 5. ПОРІВНЯННЯ ─────────────────────────────────────────────
    def _draw_cmp(self):
        val_a = digits_to_val(self.digits)
        val_b = digits_to_val(self.cmp_digits_b)
        
        # Розбиваємо область на 2 частини: текст і лінія
        gs = gridspec.GridSpec(2, 1, figure=self.fig, height_ratios=[1, 1], hspace=0.3)
        
        # --- Частина 1: Текст ---
        ax1 = self.fig.add_subplot(gs[0])
        ax1.axis("off")
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 10)
        
        # Число А
        ax1.text(2.5, 6, "Число A", ha="center", color=TEXT3, fontsize=18)
        ax1.text(2.5, 5, fmt(val_a, self.places), ha="center", fontsize=50, color=C_BLUE, fontweight="bold")
        
        # Число B
        ax1.text(7.5, 6, "Число B", ha="center", color=TEXT3, fontsize=18)
        ax1.text(7.5, 5, fmt(val_b, self.places), ha="center", fontsize=50, color=C_GREEN, fontweight="bold")
        
        # Знак порівняння
        if val_a > val_b:
            sym, col = ">", C_RED
        elif val_a < val_b:
            sym, col = "<", C_RED
        else:
            sym, col = "=", TEXT
            
        ax1.text(5, 5, sym, ha="center", va="center", fontsize=100, color=col)
        
        # Візуалізація різниці
        if val_a != val_b:
            diff = abs(val_a - val_b)
            ax1.text(5, 2, f"Різниця: {fmt(diff, 5).rstrip('0').rstrip(',')}", 
                    ha="center", fontsize=24, color=TEXT2)

        # --- Частина 2: Числова пряма ---
        ax2 = self.fig.add_subplot(gs[1])
        ax2.set_facecolor(BG)
        ax2.axis("off")
        
        # Визначаємо межі графіка
        vmin = min(val_a, val_b)
        vmax = max(val_a, val_b)
        
        # Якщо числа рівні або дуже близькі
        if vmax - vmin < 1e-9:
            span = 1.0 # Дефолтний діапазон
        else:
            span = (vmax - vmin) * 2.0 # Додаємо відступи
            
        center = (vmin + vmax) / 2
        start = center - span/2
        end = center + span/2
        
        ax2.set_xlim(start, end)
        ax2.set_ylim(-1, 1)
        
        # Крок сітки
        step = 1.0
        if span < 0.005: step = 0.0001
        elif span < 0.05: step = 0.001
        elif span < 0.5: step = 0.01
        elif span < 5: step = 0.1
        
        # Малюємо поділки
        t = math.floor(start / step) * step
        while t <= end + step:
            t_r = round(t, 6)
            if start <= t_r <= end:
                is_int = abs(t_r - round(t_r)) < 1e-9
                hh = 0.3 if is_int else 0.15
                col = TEXT if is_int else TEXT2
                lw = 2 if is_int else 1
                
                ax2.plot([t_r, t_r], [-hh, hh], color=col, lw=lw)
                
                # Підписи тільки якщо не надто густо
                if span / step < 20 or is_int:
                    lbl = fmt(t_r, 5).rstrip("0").rstrip(",") if not is_int else str(int(t_r))
                    ax2.text(t_r, -hh - 0.2, lbl, ha="center", va="top", color=col, fontsize=12)
            t += step

        # Головна лінія
        ax2.axhline(0, color=TEXT2, lw=2)
        
        # Точка A
        ax2.plot(val_a, 0, "o", color=C_BLUE, markersize=15, zorder=10, label="A")
        ax2.text(val_a, 0.4, "A", ha="center", va="bottom", color=C_BLUE, fontsize=20, fontweight="bold")
        
        # Точка B
        ax2.plot(val_b, 0, "o", color=C_GREEN, markersize=15, zorder=10, label="B")
        ax2.text(val_b, -0.4, "B", ha="center", va="top", color=C_GREEN, fontsize=20, fontweight="bold")

    # ══ ПОДІЇ МИШІ ════════════════════════════════════════════════
    def _wheel(self, event):
        if self._current_tab_idx != 0: return # Тільки для прямої
        
        factor = 1.2
        if event.num == 4 or (hasattr(event,"delta") and event.delta > 0):
            # Zoom in
            self.zoom_range = max(0.0001, self.zoom_range / factor)
        else:
            # Zoom out
            self.zoom_range = min(100.0, self.zoom_range * factor)
        self._redraw()

    def _drag_start(self, event):
        if self._current_tab_idx != 0: return
        self._drag_x0 = event.x
        self._drag_c0 = self.zoom_center

    def _drag_move(self, event):
        if self._drag_x0 is None or self._current_tab_idx != 0: return
        
        # Скільки пікселів екран?
        cw = self.mpl_widget.winfo_width()
        
        # Зміщення в пікселях
        dx = event.x - self._drag_x0
        
        # Зміщення в одиницях графіка
        # zoom_range відповідає всій ширині екрану
        shift = -(dx / cw) * self.zoom_range
        
        self.zoom_center = self._drag_c0 + shift
        self._redraw()

    def _drag_end(self, event):
        self._drag_x0 = None


if __name__ == "__main__":
    app = App()
    app.mainloop()
