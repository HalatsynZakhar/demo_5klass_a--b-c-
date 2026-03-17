"""
Демонстрація: Лінійні та стовпчасті діаграми (§ 19).
Для 5 класу.
Діаграма, лінійна діаграма, стовпчаста діаграма, читання даних за шкалою.
"""

import tkinter as tk
import random
import math

BG = "#f5f7fa"
PANEL = "#ffffff"
ACCENT = "#2563eb"
BORDER = "#dbeafe"
TEXT = "#1e293b"
MUTED = "#64748b"
GREEN = "#16a34a"
RED = "#dc2626"
ORANGE = "#d97706"
WHITE = "#ffffff"
BTN_NUM = "#e2e8f0"
INDIGO = "#4f46e5"
SKY = "#0ea5e9"
GREEN_BG = "#dcfce7"
RED_BG = "#fee2e2"


class ChartsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Лінійні та стовпчасті діаграми")
        self.configure(bg=BG)

        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        self.bind("<Key>", self._on_key_press)
        self.bind("<Return>", lambda e: self.check_answer())
        self.bind("<BackSpace>", lambda e: self._key_press("⌫"))
        self.bind("<Delete>", lambda e: self._key_press("C"))

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()

        self.mode = None
        self.task = None
        self.phase = "answer"
        self.user_input = ""
        self.score = 0
        self.total = 0

        self.answer_mode = "number"
        self.choice_value = None
        self.trainer_show_value_labels = True

        self._build_ui()
        self.show_intro()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=ACCENT, height=60) # Reduced from 80
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(
            hdr,
            text="Лінійні та стовпчасті діаграми (§ 19)",
            bg=ACCENT,
            fg=WHITE,
            font=("Segoe UI", 20, "bold"), # Reduced from 24
        ).pack(side="left", padx=30)
        tk.Button(
            hdr,
            text="❌ Вихід",
            font=("Arial", 14, "bold"), # Reduced from 16
            bg=RED,
            fg=WHITE,
            bd=0,
            command=self.destroy,
        ).pack(side="right", padx=20)

        nav = tk.Frame(self, bg=WHITE, height=50) # Reduced from 60
        nav.pack(fill="x")
        nav.pack_propagate(False)

        btn_font = ("Segoe UI", 11, "bold") # Reduced from 12
        tk.Button(nav, text="1. Діаграми", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_intro).pack(side="left", padx=10)
        tk.Button(nav, text="2. Лінійна", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_line).pack(side="left", padx=10)
        tk.Button(nav, text="3. Стовпчаста", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_bar).pack(side="left", padx=10)
        tk.Button(nav, text="4. Читання", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_reading).pack(side="left", padx=10)
        tk.Button(nav, text="5. Тренажер", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_trainer).pack(side="left", padx=10)

        self.main_area = tk.Frame(self, bg=BG)
        self.main_area.pack(fill="both", expand=True)

    def clear_main(self):
        for w in self.main_area.winfo_children():
            w.destroy()

    def _on_key_press(self, event):
        if event.char.isdigit():
            self._key_press(event.char)

    def _canvas_width(self, cv, fallback):
        w = int(cv.winfo_width())
        if w < 300:
            cv.update_idletasks()
            w = int(cv.winfo_width())
        if w < 300:
            w = int(fallback)
        return w

    def _key_press(self, ch):
        if self.mode != "trainer":
            return
        if self.phase != "answer":
            return
        if self.answer_mode != "number":
            return
        if ch == "⌫":
            self.user_input = self.user_input[:-1]
        elif ch == "C":
            self.user_input = ""
        else:
            if len(self.user_input) < 7:
                self.user_input += ch
        self.lbl_display.config(text=self.user_input)

    def show_intro(self):
        self.clear_main()
        self.mode = "intro"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=20) # Reduced from 50/25

        tk.Label(f, text="Діаграми", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10)) # Reduced from 32
        tk.Label(
            f,
            text=(
                "Діаграма — це наочний спосіб показати співвідношення між величинами.\n"
                "Найчастіше в 5 класі використовують:\n"
                "• лінійну діаграму (значення показують відрізками)\n"
                "• стовпчасту діаграму (значення показують стовпчиками)\n\n"
                "Щоб правильно прочитати діаграму, треба знати масштаб (наприклад: 1 поділка = 2 одиниці)."
            ),
            font=("Segoe UI", 16), # Reduced from 18
            bg=BG,
            fg=MUTED,
            justify="left",
            wraplength=self.SW - 100,
        ).pack(anchor="w", pady=(0, 10))

        cv = tk.Canvas(f, bg=WHITE, height=260, bd=2, relief="ridge") # Reduced from 320
        cv.pack(fill="x", pady=10, padx=10) # Reduced pady

        demo = [("A", 8), ("B", 12), ("C", 5), ("D", 10)]
        self._draw_line_diagram(cv, demo, unit_name="ум. од.", title="Приклад лінійної діаграми")

        tk.Label(
            f,
            text="Перейди на вкладки «Лінійна» та «Стовпчаста», а потім спробуй тренажер.",
            font=("Segoe UI", 14, "italic"), # Reduced from 16
            bg=BG,
            fg=MUTED,
        ).pack(pady=10)

    def show_line(self):
        self.clear_main()
        self.mode = "line"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=20)

        tk.Label(f, text="Лінійна діаграма", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10)) # Reduced from 30
        tk.Label(
            f,
            text=(
                "Лінійна діаграма показує значення за допомогою відрізків.\n"
                "Потрібно обрати масштаб (наприклад: 1 кг = 1 мм) і відкласти довжини відрізків."
            ),
            font=("Segoe UI", 16),
            bg=BG,
            fg=MUTED,
            justify="left",
            wraplength=self.SW - 100,
        ).pack(anchor="w")

        top = tk.Frame(f, bg=BG)
        top.pack(fill="x", pady=10)
        self.line_msg = tk.Label(top, text="", font=("Segoe UI", 14, "bold"), bg=BG, fg=MUTED) # Reduced from 16
        self.line_msg.pack(side="left")
        tk.Button(top, text="🎲 Нові дані", font=("Segoe UI", 12, "bold"), bg=ACCENT, fg=WHITE, bd=0, padx=14, pady=8, command=self._line_new).pack(
            side="right", padx=10
        ) # Reduced sizes

        self.line_canvas = tk.Canvas(f, bg=WHITE, height=300, bd=2, relief="ridge") # Reduced from 360
        self.line_canvas.pack(fill="x", pady=10, padx=10)

        self._line_new()

    def _line_new(self):
        names = random.sample(["Марко", "Софія", "Юрко", "Олена", "Данило", "Аня", "Ілля", "Назар"], 4)
        values = [random.randint(22, 38) for _ in range(4)]
        self.line_data = list(zip(names, values))
        axis_step = self._draw_line_diagram(self.line_canvas, self.line_data, unit_name="кг", title="Маса дітей")
        self.line_msg.config(text=f"Приклад: маса дітей (кг). Масштаб осі: 1 поділка = {axis_step} кг.", fg=MUTED)

    def show_bar(self):
        self.clear_main()
        self.mode = "bar"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=20)

        tk.Label(f, text="Стовпчаста діаграма", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        tk.Label(
            f,
            text=(
                "Стовпчаста діаграма показує значення за допомогою стовпчиків.\n"
                "Ширина стовпчиків однакова, а висота залежить від значення.\n"
                "Потрібно знати масштаб (наприклад: 10 кг = 1 мм)."
            ),
            font=("Segoe UI", 16),
            bg=BG,
            fg=MUTED,
            justify="left",
            wraplength=self.SW - 100,
        ).pack(anchor="w")

        top = tk.Frame(f, bg=BG)
        top.pack(fill="x", pady=10)
        self.bar_msg = tk.Label(top, text="", font=("Segoe UI", 14, "bold"), bg=BG, fg=MUTED) # Reduced
        self.bar_msg.pack(side="left")
        tk.Button(top, text="🎲 Нові дані", font=("Segoe UI", 12, "bold"), bg=ACCENT, fg=WHITE, bd=0, padx=14, pady=8, command=self._bar_new).pack(
            side="right", padx=10
        ) # Reduced

        self.bar_canvas = tk.Canvas(f, bg=WHITE, height=300, bd=2, relief="ridge") # Reduced from 360
        self.bar_canvas.pack(fill="x", pady=10, padx=10)

        self._bar_new()

    def _bar_new(self):
        names = random.sample(["Лама", "Олень", "Тигр", "Лев", "Кінь", "Ведмідь"], 3)
        self.bar_scale_step = random.choice([5, 10, 20])
        lo_k = (90 + self.bar_scale_step - 1) // self.bar_scale_step
        hi_k = 340 // self.bar_scale_step
        values = [random.randint(lo_k, hi_k) * self.bar_scale_step for _ in range(3)]
        self.bar_data = list(zip(names, values))
        self.bar_msg.config(text=f"Приклад: маса тварин (кг). Масштаб: {self.bar_scale_step} кг = 1 поділка.", fg=MUTED)
        self._draw_bar_diagram(self.bar_canvas, self.bar_data, unit_name="кг", step=self.bar_scale_step, title="Маса тварин")

    def show_reading(self):
        self.clear_main()
        self.mode = "reading"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=20)

        tk.Label(f, text="Читання діаграм", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10)) # Reduced from 30
        tk.Label(
            f,
            text="Спробуй відповісти на запитання за діаграмою. Натисни варіант відповіді.",
            font=("Segoe UI", 16),
            bg=BG,
            fg=MUTED,
        ).pack()

        top = tk.Frame(f, bg=BG)
        top.pack(fill="x", pady=10)
        tk.Button(top, text="🔁 Інша діаграма", font=("Segoe UI", 12, "bold"), bg=ACCENT, fg=WHITE, bd=0, padx=14, pady=8, command=self._reading_toggle).pack(side="right", padx=10) # Reduced
        self.reading_title = tk.Label(top, text="", font=("Segoe UI", 14, "bold"), bg=BG, fg=MUTED) # Reduced
        self.reading_title.pack(side="left")

        self.reading_canvas = tk.Canvas(f, bg=WHITE, height=260, bd=2, relief="ridge") # Reduced from 320
        self.reading_canvas.pack(fill="x", pady=10, padx=10)

        self.quiz_box = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=20, pady=10) # Reduced pad
        self.quiz_box.pack(fill="x", padx=10, pady=10)
        self.quiz_q = tk.Label(self.quiz_box, text="", font=("Segoe UI", 14, "bold"), bg=WHITE, fg=TEXT, wraplength=self.SW - 100, justify="left") # Reduced
        self.quiz_q.pack(anchor="w")
        self.quiz_btns = tk.Frame(self.quiz_box, bg=WHITE)
        self.quiz_btns.pack(pady=8)
        self.quiz_msg = tk.Label(self.quiz_box, text="", font=("Segoe UI", 14, "bold"), bg=WHITE)
        self.quiz_msg.pack(anchor="w")

        self.reading_variant = 0
        self.reading_idx = 0
        self._reading_load()

    def _reading_toggle(self):
        self.reading_variant = 1 - self.reading_variant
        self.reading_idx = 0
        self._reading_load()

    def _reading_load(self):
        for w in self.quiz_btns.winfo_children():
            w.destroy()
        self.quiz_msg.config(text="", fg=TEXT)

        if self.reading_variant == 0:
            data = [("Клавіатури", 18), ("Монітори", 12), ("Геймпади", 18), ("Ноутбуки", 6), ("Смартфони", 20)]
            self.reading_title.config(text="Лінійна діаграма: продаж товарів за день", fg=MUTED)
            self._draw_line_diagram(self.reading_canvas, data, unit_name="шт", title="")
            questions = [
                ("Скільки продали ноутбуків?", ["6", "12", "18"], 0),
                ("Чого продали більше: смартфонів чи моніторів?", ["Смартфонів", "Моніторів", "Порівну"], 0),
                ("Яких товарів продали порівну?", ["Клавіатури і геймпади", "Монітори і ноутбуки", "Смартфони і клавіатури"], 0),
            ]
        else:
            data = [("5-А", 9), ("5-Б", 11), ("5-В", 12), ("5-Г", 9)]
            self.reading_title.config(text="Стовпчаста діаграма: учасники олімпіади", fg=MUTED)
            self._draw_bar_diagram(self.reading_canvas, data, unit_name="дітей", step=1, title="")
            questions = [
                ("Скільки дітей з 5-Б класу взяло участь?", ["9", "11", "12"], 1),
                ("Де було більше учасників: 5-А чи 5-В?", ["5-А", "5-В", "Порівну"], 1),
                ("Від яких класів була однакова кількість учасників?", ["5-А і 5-Г", "5-А і 5-Б", "5-Б і 5-В"], 0),
            ]

        q_text, options, correct_idx = questions[self.reading_idx]
        self.reading_current = {"correct": correct_idx, "options": options}
        self.quiz_q.config(text=f"Питання {self.reading_idx + 1}/3: {q_text}")

        for i, opt in enumerate(options):
            tk.Button(
                self.quiz_btns,
                text=opt,
                font=("Segoe UI", 14, "bold"), # Reduced from 16
                bg=BTN_NUM,
                bd=0,
                padx=16,
                pady=8,
                command=lambda k=i: self._reading_pick(k),
            ).pack(side="left", padx=10, pady=5)

    def _reading_pick(self, idx):
        if idx == self.reading_current["correct"]:
            self.quiz_msg.config(text="✅ Правильно!", fg=GREEN)
            self.after(650, self._reading_next)
        else:
            self.quiz_msg.config(text="❌ Ні. Спробуй ще.", fg=RED)

    def _reading_next(self):
        self.reading_idx += 1
        if self.reading_idx >= 3:
            self.reading_idx = 0
            self.reading_variant = 1 - self.reading_variant
        self._reading_load()

    def show_trainer(self):
        self.clear_main()
        self.mode = "trainer"

        LW = int(self.SW * 0.62)
        RW = self.SW - LW

        left = tk.Frame(self.main_area, bg=BG, width=LW)
        left.pack(side="left", fill="both")
        left.pack_propagate(False)

        tk.Label(left, text="Тренажер", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(15, 5)) # Reduced
        self.lbl_score = tk.Label(left, text="Рахунок: 0 / 0", font=("Segoe UI", 16, "bold"), bg=BG, fg=ACCENT)
        self.lbl_score.pack(pady=(0, 5))

        self.task_box = tk.Frame(left, bg=WHITE, bd=3, relief="solid", padx=20, pady=15) # Reduced pad
        self.task_box.pack(pady=10, padx=20, fill="x")
        self.task_text = tk.Label(self.task_box, text="", font=("Segoe UI", 16, "bold"), bg=WHITE, fg=TEXT, justify="left", wraplength=LW - 100) # Reduced from 18
        self.task_text.pack(anchor="w")

        self.task_canvas = tk.Canvas(left, bg=WHITE, height=220, bd=2, relief="ridge") # Reduced from 280
        self.task_canvas.pack(pady=10, padx=20, fill="x")

        self.btn_labels = tk.Button(
            left,
            text="Підписи значень: +",
            bg=BTN_NUM,
            fg=TEXT,
            font=("Segoe UI", 12, "bold"),
            bd=0,
            padx=14,
            pady=8,
            command=self.toggle_value_labels,
        ) # Reduced sizes
        self.btn_labels.pack(pady=(0, 5))

        self.choice_frame = tk.Frame(left, bg=BG)
        self.choice_msg = tk.Label(self.choice_frame, text="", font=("Segoe UI", 16, "bold"), bg=BG, fg=MUTED) # Reduced from 18
        self.choice_msg.pack()
        self.choice_btns = tk.Frame(self.choice_frame, bg=BG)
        self.choice_btns.pack(pady=5)

        self.display_frame = tk.Frame(left, bg=WHITE, highlightbackground=ACCENT, highlightthickness=2)
        self.display_frame.pack(pady=5, ipadx=16, ipady=4) # Reduced pad
        self.lbl_display = tk.Label(self.display_frame, text="", bg=WHITE, fg=TEXT, font=("Segoe UI", 32, "bold"), width=12, anchor="e") # Reduced from 48
        self.lbl_display.pack()

        self.lbl_feedback = tk.Label(left, text="", font=("Segoe UI", 16, "bold"), bg=BG)
        self.lbl_feedback.pack(pady=5)

        self.kbd = tk.Frame(left, bg=BG)
        self.kbd.pack(pady=5)
        rows = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["C", "0", "⌫"]]
        for row in rows:
            r = tk.Frame(self.kbd, bg=BG)
            r.pack(pady=2)
            for ch in row:
                tk.Button(
                    r,
                    text=ch,
                    bg=RED_BG if ch in ("⌫", "C") else BTN_NUM,
                    font=("Segoe UI", 16, "bold"),
                    width=6,
                    height=1,
                    relief="flat",
                    command=lambda c=ch: self._key_press(c),
                ).pack(side="left", padx=4) # Reduced size

        btn_f = tk.Frame(left, bg=BG)
        btn_f.pack(pady=5)
        self.btn_ok = tk.Button(btn_f, text="✓ Перевірити", bg=GREEN, fg=WHITE, font=("Segoe UI", 14, "bold"), relief="flat", padx=30, pady=8, command=self.check_answer)
        self.btn_ok.pack(side="left", padx=15)
        self.btn_next = tk.Button(btn_f, text="▶ Наступне", bg=ACCENT, fg=WHITE, font=("Segoe UI", 14, "bold"), relief="flat", padx=30, pady=8, command=self.next_task)

        right = tk.Frame(self.main_area, bg=PANEL, width=RW, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        rpad = tk.Frame(right, bg=PANEL)
        rpad.pack(fill="both", expand=True, padx=20, pady=20)
        tk.Label(rpad, text="Підказки", font=("Segoe UI", 16, "bold"), bg=PANEL, fg=MUTED).pack(anchor="w")

        hint_box = tk.Frame(rpad, bg="#eff6ff", highlightbackground="#bfdbfe", highlightthickness=1, padx=10, pady=10)
        hint_box.pack(fill="x", pady=10)
        tk.Label(
            hint_box,
            text=(
                "• Спочатку подивись на масштаб (скільки одиниць у 1 поділці)\n"
                "• Для лінійної діаграми: довший відрізок — більше значення\n"
                "• Для стовпчастої: вищий стовпчик — більше значення\n"
                "• Переведення: якщо k одиниць = 1 мм, то висота = значення : k"
            ),
            font=("Segoe UI", 11), # Reduced from 12
            bg="#eff6ff",
            justify="left",
        ).pack(anchor="w")

        self.after(80, self.next_task)

    def toggle_value_labels(self):
        if self.mode != "trainer":
            return
        self.trainer_show_value_labels = not self.trainer_show_value_labels
        self.btn_labels.config(text=f"Підписи значень: {'+' if self.trainer_show_value_labels else '-'}")
        if self.task and self.phase == "answer":
            t = self.task.get("type")
            if t == "read_bar":
                self._draw_bar_diagram(self.task_canvas, self.task["data"], unit_name="од.", step=self.task["step"], title="", show_value_labels=self.trainer_show_value_labels)
            elif t == "read_line":
                self._draw_line_diagram(self.task_canvas, self.task["data"], unit_name="од.", title="", show_value_labels=self.trainer_show_value_labels)
            elif t == "compare":
                self._draw_line_diagram(self.task_canvas, self.task["data"], unit_name="од.", title="", show_value_labels=self.trainer_show_value_labels)
            elif t == "scale_mm":
                self._draw_scale_formula(self.task_canvas, self.task["unit"], self.task["value"])

    def _trainer_set_mode(self, mode):
        self.answer_mode = mode
        self.choice_value = None
        for w in self.choice_btns.winfo_children():
            w.destroy()
        self.choice_msg.config(text="")

        if mode == "number":
            self.choice_frame.pack_forget()
            self.display_frame.pack(pady=5, ipadx=16, ipady=4) # Adjusted
            self.kbd.pack(pady=5)
            self.btn_ok.config(state="normal")
        else:
            self.kbd.pack_forget()
            self.display_frame.pack_forget()
            self.choice_frame.pack(pady=5)
            self.btn_ok.config(state="disabled")

    def next_task(self):
        if self.mode != "trainer":
            return

        self.phase = "answer"
        self.user_input = ""
        self.lbl_display.config(text="", bg=WHITE)
        self.lbl_feedback.config(text="", fg=TEXT, bg=BG)
        self.btn_next.pack_forget()
        self.btn_ok.pack(side="left", padx=20)

        self.task_canvas.delete("all")

        t = random.choice(["read_line", "read_bar", "compare", "scale_mm"])

        if t == "read_line":
            data = self._make_line_dataset()
            name, value = random.choice(data)
            self.task = {"type": "read_line", "ans": value, "data": data, "name": name}
            self._trainer_set_mode("number")
            axis_step = self._draw_line_diagram(self.task_canvas, data, unit_name="од.", title="", show_value_labels=self.trainer_show_value_labels)
            self.task_text.config(text=f"Лінійна діаграма. Скільки у {name}? (1 поділка = {axis_step} од.)")
        elif t == "read_bar":
            data, step = self._make_bar_dataset()
            name, value = random.choice(data)
            self.task = {"type": "read_bar", "ans": value, "data": data, "name": name, "step": step}
            self._trainer_set_mode("number")
            self.task_text.config(text=f"Стовпчаста діаграма. Яке значення у «{name}»? (1 поділка = {step} од.)")
            self._draw_bar_diagram(self.task_canvas, data, unit_name="од.", step=step, title="", show_value_labels=self.trainer_show_value_labels)
        elif t == "compare":
            data = self._make_line_dataset()
            n1 = n2 = None
            v1 = v2 = None
            for k in range(40):
                (n1, v1), (n2, v2) = random.sample(data, 2)
                if v1 != v2:
                    break
                if k in (9, 19, 29):
                    data = self._make_line_dataset()
            if v1 == v2:
                correct = "Порівну"
            else:
                correct = n1 if v1 > v2 else n2
            self.task = {"type": "compare", "ans": correct, "n1": n1, "n2": n2, "data": data}
            self._trainer_set_mode("choice")
            self.task_text.config(text="Порівняй за діаграмою. Хто має більше?")
            self._draw_line_diagram(self.task_canvas, data, unit_name="од.", title="", show_value_labels=self.trainer_show_value_labels)
            self.choice_msg.config(text="Обери правильний варіант:")
            if v1 == v2:
                self.task_text.config(text="Порівняй за діаграмою. У кого більше, чи порівну?")
                options = [n1, "Порівну", n2]
            else:
                options = [n1, n2]
            for opt in options:
                tk.Button(
                    self.choice_btns,
                    text=opt,
                    font=("Segoe UI", 14, "bold"), # Reduced from 18
                    bg=BTN_NUM,
                    bd=0,
                    padx=14,
                    pady=8,
                    command=lambda o=opt: self._pick_choice(o),
                ).pack(side="left", padx=10)
        else:
            unit_in_mm = random.choice([2, 5, 10, 20])
            value = random.choice([80, 90, 110, 120, 150, 200, 230, 320, 360, 450])
            ans = value // unit_in_mm
            self.task = {"type": "scale_mm", "ans": ans, "unit": unit_in_mm, "value": value}
            self._trainer_set_mode("number")
            self.task_text.config(text=f"Масштаб: {unit_in_mm} одиниць = 1 мм. Яка висота (в мм) для значення {value}?")
            self._draw_scale_formula(self.task_canvas, unit_in_mm, value)

        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")

    def _pick_choice(self, value):
        if self.mode != "trainer":
            return
        if self.phase != "answer":
            return
        if self.answer_mode != "choice":
            return
        self.choice_value = value
        self._finish_answer()

    def check_answer(self):
        if self.mode != "trainer":
            return
        if self.phase != "answer":
            return
        if not self.task:
            return
        if self.answer_mode != "number":
            return
        raw = self.user_input.strip()
        if not raw:
            return
        try:
            got = int(raw)
        except ValueError:
            return
        self._finish_answer(got=got)

    def _finish_answer(self, got=None):
        if self.mode != "trainer":
            return
        if self.phase != "answer":
            return
        if not self.task:
            return

        if self.answer_mode == "choice":
            got_value = self.choice_value
            if got_value is None:
                return
        else:
            got_value = got

        self.phase = "feedback"
        self.total += 1

        ok = got_value == self.task["ans"]
        if ok:
            self.score += 1
            self.lbl_feedback.config(text="✅ Правильно!", fg=GREEN)
            self.lbl_display.config(bg=GREEN_BG)
            self.after(850, self.next_task)
        else:
            self.lbl_feedback.config(text=f"❌ Ні. Відповідь: {self.task['ans']}", fg=RED)
            self.lbl_display.config(bg=RED_BG)
            self.btn_ok.pack_forget()
            self.btn_next.pack(side="left", padx=20)

        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")

    def _make_line_dataset(self):
        names = random.sample(["Клас A", "Клас B", "Клас C", "Клас D", "Клас E"], 4)
        values = [random.randint(5, 20) for _ in range(4)]
        return list(zip(names, values))

    def _make_bar_dataset(self):
        names = random.sample(["Груша", "Яблуко", "Слива", "Вишня", "Абрикос"], 4)
        step = random.choice([1, 2, 5])
        values = [random.randint(8, 30) * step for _ in range(4)]
        return list(zip(names, values)), step

    def _draw_scale_formula(self, cv, unit, value):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW * 0.62 - 60)
        cx = w // 2
        cv.create_text(cx, 50, text=f"{unit} одиниць = 1 мм", font=("Segoe UI", 16, "bold"), fill=MUTED) # Reduced Y
        cv.create_text(cx, 100, text=f"значення {value} : {unit} = ?", font=("Segoe UI", 20, "bold"), fill=TEXT) # Reduced Y
        cv.create_line(cx - 200, 130, cx + 200, 130, width=2, fill=BORDER)
        h = 140
        cv.create_rectangle(cx - 30, h, cx + 30, h + 70, fill=SKY, outline=WHITE, width=2)
        cv.create_text(cx, h + 35, text="мм", font=("Segoe UI", 14, "bold"), fill=WHITE)

    def _draw_line_diagram(self, cv, data, unit_name, title, show_value_labels=True):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        left = 140 # Reduced from 180
        right = w - 40
        h = int(cv.winfo_height())
        if h < 220:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 220:
            h = 320
        top = 40 # Reduced from 60
        n = max(1, len(data))
        avail = max(140, h - top - 40)
        row_h = max(36, min(60, int(avail / n)))

        max_val = max(v for _, v in data) if data else 1
        scale = (right - left) / max(1, max_val)

        if title:
            cv.create_text(30, 20, text=title, font=("Segoe UI", 14, "bold"), fill=TEXT, anchor="w")
        cv.create_text(w - 30, 20, text=unit_name, font=("Segoe UI", 12, "bold"), fill=MUTED, anchor="e")

        axis_step = 1
        ticks = min(10, max_val)
        if ticks > 0:
            axis_step = max(1, int(math.ceil(max_val / ticks)))
            for t in range(0, max_val + 1, axis_step):
                x = left + t * scale
                cv.create_line(x, top - 15, x, top - 5, width=2, fill=BORDER)
                cv.create_text(x, top - 25, text=str(t), font=("Segoe UI", 10, "bold"), fill=MUTED)

        for i, (name, val) in enumerate(data):
            y = top + i * row_h + 30
            cv.create_text(30, y, text=name, font=("Segoe UI", 12, "bold"), fill=TEXT, anchor="w") # Reduced font
            x2 = left + val * scale
            cv.create_line(left, y, x2, y, width=8, fill=INDIGO) # Reduced width
            cv.create_oval(x2 - 6, y - 6, x2 + 6, y + 6, fill=ORANGE, outline=WHITE, width=2)
            if show_value_labels:
                cv.create_text(x2 + 10, y, text=str(val), font=("Segoe UI", 11, "bold"), fill=MUTED, anchor="w")
        return axis_step

    def _draw_bar_diagram(self, cv, data, unit_name, step, title, show_value_labels=True):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())
        if h < 220:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 220:
            h = 320
        left = 60 # Reduced
        right = w - 30
        bottom = h - 40 # Reduced
        top = 40
        axis_h = bottom - top

        max_val = max(v for _, v in data) if data else 1
        max_tick = int(math.ceil(max_val / step) * step)
        if max_tick == 0:
            max_tick = step
        scale = axis_h / max_tick

        if title:
            cv.create_text(30, 20, text=title, font=("Segoe UI", 14, "bold"), fill=TEXT, anchor="w")
        cv.create_text(w - 30, 20, text=unit_name, font=("Segoe UI", 12, "bold"), fill=MUTED, anchor="e")

        cv.create_line(left, top, left, bottom, width=3, fill=TEXT)
        cv.create_line(left, bottom, right, bottom, width=3, fill=TEXT)

        label_step = step * (2 if max_tick / step > 15 else 1)
        for t in range(0, max_tick + 1, step):
            y = bottom - t * scale
            major = (t % label_step == 0)
            cv.create_line(left - (8 if major else 5), y, left, y, width=2 if major else 1, fill=TEXT if major else BORDER)
            cv.create_line(left, y, right, y, width=1, fill=BORDER)
            if major:
                cv.create_text(left - 10, y, text=str(t), font=("Segoe UI", 9, "bold"), fill=MUTED, anchor="e") # Reduced

        n = len(data) if data else 1
        bar_area = right - left - 20
        bar_w = max(20, min(70, int(bar_area / n) - 15))
        gap = (bar_area - n * bar_w) / max(1, n + 1)
        x = left + 10 + gap

        for name, val in data:
            h = val * scale
            cv.create_rectangle(x, bottom - h, x + bar_w, bottom, fill=SKY, outline=WHITE, width=2)
            cv.create_text(x + bar_w / 2, bottom + 10, text=name, font=("Segoe UI", 10, "bold"), fill=TEXT, anchor="n", width=bar_w + 10) # Reduced
            if show_value_labels:
                cv.create_text(x + bar_w / 2, bottom - h - 8, text=str(val), font=("Segoe UI", 10, "bold"), fill=MUTED, anchor="s") # Reduced
            x += bar_w + gap


if __name__ == "__main__":
    app = ChartsApp()
    app.mainloop()
