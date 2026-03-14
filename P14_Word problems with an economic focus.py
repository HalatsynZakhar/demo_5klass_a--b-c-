"""
Демонстрація: Текстові задачі економічного змісту (§ 14).
Для 5 класу.
Вартість товару та задачі на роботу (продуктивність).
"""

import tkinter as tk
import random

BG = "#f5f7fa"
PANEL = "#ffffff"
ACCENT = "#2563eb"
BORDER = "#dbeafe"
TEXT = "#1e293b"
MUTED = "#64748b"
GREEN = "#16a34a"
RED = "#dc2626"
ORANGE = "#d97706"
YELLOW_BG = "#fef9c3"
HL_FG = "#92400e"
GREEN_BG = "#dcfce7"
RED_BG = "#fee2e2"
WHITE = "#ffffff"
BTN_NUM = "#e2e8f0"
INDIGO = "#4f46e5"


class EconomicProblemsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Текстові задачі економічного змісту")
        self.configure(bg=BG)

        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.bind("<Key>", self._on_key_press)
        self.bind("<Return>", lambda e: self.check_answer())
        self.bind("<BackSpace>", lambda e: self._key_press("⌫"))
        self.bind("<Delete>", lambda e: self._key_press("C"))

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()

        self.task = None
        self.user_input = ""
        self.score = 0
        self.total = 0
        self.phase = "answer"
        self.task_hint_shown = False
        self.forbidden_nums = {3, 4, 5, 8, 10, 12, 15, 24, 30, 60, 72, 75, 200}

        self._build_ui()
        self.show_intro_cost()

    def _pick_not_forbidden(self, lo, hi):
        while True:
            x = random.randint(lo, hi)
            if x not in self.forbidden_nums:
                return x

    def _build_ui(self):
        hdr = tk.Frame(self, bg=ACCENT, height=80)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(
            hdr,
            text="Текстові задачі економічного змісту (§ 14)",
            bg=ACCENT,
            fg=WHITE,
            font=("Segoe UI", 24, "bold"),
        ).pack(side="left", padx=30)
        tk.Button(
            hdr,
            text="❌ Вихід",
            font=("Arial", 16, "bold"),
            bg=RED,
            fg=WHITE,
            bd=0,
            command=self.destroy,
        ).pack(side="right", padx=20)

        nav = tk.Frame(self, bg=WHITE, height=60)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        btn_font = ("Segoe UI", 12, "bold")
        tk.Button(
            nav,
            text="1. Вартість товару",
            font=btn_font,
            bg=WHITE,
            bd=0,
            cursor="hand2",
            command=self.show_intro_cost,
        ).pack(side="left", padx=10)
        tk.Button(
            nav,
            text="2. Задачі на роботу",
            font=btn_font,
            bg=WHITE,
            bd=0,
            cursor="hand2",
            command=self.show_intro_work,
        ).pack(side="left", padx=10)
        tk.Button(
            nav,
            text="3. Приклади",
            font=btn_font,
            bg=WHITE,
            bd=0,
            cursor="hand2",
            command=self.show_examples,
        ).pack(side="left", padx=10)
        tk.Button(
            nav,
            text="4. Тренажер",
            font=btn_font,
            bg=WHITE,
            bd=0,
            cursor="hand2",
            command=self.show_trainer,
        ).pack(side="left", padx=10)

        self.main_area = tk.Frame(self, bg=BG)
        self.main_area.pack(fill="both", expand=True)

    def clear_main(self):
        for w in self.main_area.winfo_children():
            w.destroy()

    def _on_key_press(self, event):
        if event.char.isdigit():
            self._key_press(event.char)

    def show_intro_cost(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=30)

        tk.Label(f, text="Задачі про вартість товару", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(
            pady=(0, 20)
        )

        box = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=30, pady=25)
        box.pack(fill="x", pady=10)

        left = tk.Frame(box, bg=WHITE)
        left.pack(side="left", padx=10)
        tk.Label(left, text="C — вартість\nа — ціна\nn — кількість", font=("Segoe UI", 20), bg=WHITE, fg=TEXT, justify="left").pack(
            anchor="w"
        )

        right = tk.Frame(box, bg=WHITE)
        right.pack(side="left", padx=40)
        tk.Label(right, text="Формули вартості", font=("Segoe UI", 18, "bold"), bg=WHITE, fg=MUTED).pack(anchor="w")
        tk.Label(right, text="C = a ∙ n", font=("Consolas", 36, "bold"), bg=YELLOW_BG, fg=HL_FG, padx=15, pady=8).pack(
            anchor="w", pady=(10, 8)
        )
        tk.Label(right, text="a = C : n\nn = C : a", font=("Consolas", 22, "bold"), bg=WHITE, fg=TEXT).pack(anchor="w")

        cv = tk.Canvas(f, bg=WHITE, height=170, bd=1, relief="ridge")
        cv.pack(fill="x", pady=25, padx=20)
        self._draw_cost_diagram(cv)

        a_ex = self._pick_not_forbidden(12, 65)
        n_ex = self._pick_not_forbidden(2, 9)
        C_ex = a_ex * n_ex

        ex = tk.Frame(f, bg="#eff6ff", highlightbackground="#bfdbfe", highlightthickness=1, padx=20, pady=15)
        ex.pack(fill="x", pady=10)
        tk.Label(ex, text=f"Приклад: 1 кг товару — {a_ex} грн. Скільки коштують {n_ex} кг?", font=("Segoe UI", 16, "bold"), bg="#eff6ff", fg=TEXT).pack(
            anchor="w"
        )
        tk.Label(ex, text=f"C = a ∙ n = {a_ex} ∙ {n_ex} = {C_ex} (грн)", font=("Consolas", 18, "bold"), bg="#eff6ff", fg=ACCENT).pack(
            anchor="w", pady=(5, 0)
        )

    def _draw_cost_diagram(self, cv):
        w = int(cv.winfo_width() or (self.SW - 160))
        cv.delete("all")
        cv.create_text(20, 20, text="Вартість = Ціна × Кількість", font=("Segoe UI", 14, "bold"), anchor="w", fill=TEXT)

        x0 = 60
        y0 = 75
        bw = 160
        bh = 60
        gap = 60

        cv.create_rectangle(x0, y0, x0 + bw, y0 + bh, fill="#eff6ff", outline="#bfdbfe", width=2)
        cv.create_text(x0 + bw / 2, y0 + bh / 2, text="a\n(ціна)", font=("Segoe UI", 14, "bold"), fill=ACCENT)

        cv.create_text(x0 + bw + gap / 2, y0 + bh / 2, text="×", font=("Segoe UI", 28, "bold"), fill=MUTED)

        x1 = x0 + bw + gap
        cv.create_rectangle(x1, y0, x1 + bw, y0 + bh, fill="#fef9c3", outline="#fde68a", width=2)
        cv.create_text(x1 + bw / 2, y0 + bh / 2, text="n\n(кількість)", font=("Segoe UI", 14, "bold"), fill=HL_FG)

        cv.create_text(x1 + bw + gap / 2, y0 + bh / 2, text="=", font=("Segoe UI", 28, "bold"), fill=MUTED)

        x2 = x1 + bw + gap
        cv.create_rectangle(x2, y0, x2 + bw, y0 + bh, fill="#dcfce7", outline="#bbf7d0", width=2)
        cv.create_text(x2 + bw / 2, y0 + bh / 2, text="C\n(вартість)", font=("Segoe UI", 14, "bold"), fill=GREEN)

    def show_intro_work(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=30)

        tk.Label(f, text="Задачі на роботу", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 20))

        box = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=30, pady=25)
        box.pack(fill="x", pady=10)

        left = tk.Frame(box, bg=WHITE)
        left.pack(side="left", padx=10)
        tk.Label(left, text="A — обсяг роботи\nN — продуктивність\nt — час", font=("Segoe UI", 20), bg=WHITE, fg=TEXT, justify="left").pack(
            anchor="w"
        )

        right = tk.Frame(box, bg=WHITE)
        right.pack(side="left", padx=40)
        tk.Label(right, text="Формули роботи", font=("Segoe UI", 18, "bold"), bg=WHITE, fg=MUTED).pack(anchor="w")
        tk.Label(right, text="A = N ∙ t", font=("Consolas", 36, "bold"), bg=YELLOW_BG, fg=HL_FG, padx=15, pady=8).pack(
            anchor="w", pady=(10, 8)
        )
        tk.Label(right, text="N = A : t\nt = A : N", font=("Consolas", 22, "bold"), bg=WHITE, fg=TEXT).pack(anchor="w")

        cv = tk.Canvas(f, bg=WHITE, height=170, bd=1, relief="ridge")
        cv.pack(fill="x", pady=25, padx=20)
        self._draw_work_diagram(cv)

        N_ex = self._pick_not_forbidden(2, 14)
        t_ex = self._pick_not_forbidden(2, 9)
        A_ex = N_ex * t_ex

        ex = tk.Frame(f, bg="#f0fdf4", highlightbackground="#bbf7d0", highlightthickness=1, padx=20, pady=15)
        ex.pack(fill="x", pady=10)
        tk.Label(ex, text=f"Приклад: Працівник виконує {N_ex} операцій за 1 хв. Скільки за {t_ex} хв?", font=("Segoe UI", 16, "bold"), bg="#f0fdf4", fg=TEXT).pack(
            anchor="w"
        )
        tk.Label(ex, text=f"A = N ∙ t = {N_ex} ∙ {t_ex} = {A_ex} (операцій)", font=("Consolas", 18, "bold"), bg="#f0fdf4", fg=GREEN).pack(
            anchor="w", pady=(5, 0)
        )

    def _draw_work_diagram(self, cv):
        w = int(cv.winfo_width() or (self.SW - 160))
        cv.delete("all")
        cv.create_text(20, 20, text="Обсяг роботи = Продуктивність × Час", font=("Segoe UI", 14, "bold"), anchor="w", fill=TEXT)

        x0 = 60
        y0 = 75
        bw = 160
        bh = 60
        gap = 60

        cv.create_rectangle(x0, y0, x0 + bw, y0 + bh, fill="#eff6ff", outline="#bfdbfe", width=2)
        cv.create_text(x0 + bw / 2, y0 + bh / 2, text="N\n(прод.)", font=("Segoe UI", 14, "bold"), fill=ACCENT)

        cv.create_text(x0 + bw + gap / 2, y0 + bh / 2, text="×", font=("Segoe UI", 28, "bold"), fill=MUTED)

        x1 = x0 + bw + gap
        cv.create_rectangle(x1, y0, x1 + bw, y0 + bh, fill="#fef9c3", outline="#fde68a", width=2)
        cv.create_text(x1 + bw / 2, y0 + bh / 2, text="t\n(час)", font=("Segoe UI", 14, "bold"), fill=HL_FG)

        cv.create_text(x1 + bw + gap / 2, y0 + bh / 2, text="=", font=("Segoe UI", 28, "bold"), fill=MUTED)

        x2 = x1 + bw + gap
        cv.create_rectangle(x2, y0, x2 + bw, y0 + bh, fill="#dcfce7", outline="#bbf7d0", width=2)
        cv.create_text(x2 + bw / 2, y0 + bh / 2, text="A\n(робота)", font=("Segoe UI", 14, "bold"), fill=GREEN)

    def show_examples(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)

        tk.Label(f, text="Приклади завдань", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 15))

        a1 = self._pick_not_forbidden(9, 49)
        n1 = self._pick_not_forbidden(2, 14)
        C1 = a1 * n1

        n2 = self._pick_not_forbidden(2, 12)
        a2 = self._pick_not_forbidden(9, 49)
        C2 = a2 * n2

        A3 = self._pick_not_forbidden(40, 140)
        t3 = self._pick_not_forbidden(2, 14)
        if A3 % t3 != 0:
            A3 = A3 - (A3 % t3)
            if A3 == 0:
                A3 = t3 * 2
        N3 = A3 // t3
        if N3 in self.forbidden_nums:
            N3 += 1
            A3 = N3 * t3

        N4 = self._pick_not_forbidden(6, 17)
        t4 = self._pick_not_forbidden(2, 15)
        A4 = N4 * t4

        N5 = self._pick_not_forbidden(7, 19)
        t5 = self._pick_not_forbidden(2, 12)
        A5 = N5 * t5

        price_nb = random.choice([17, 19, 23, 29, 31])
        price_p = random.choice([5, 9, 11, 13])
        pay = random.choice([150, 250, 350, 450])
        total = 2 * price_nb + 3 * price_p

        examples = [
            (f"1) Ціна товару {a1} грн за одиницю. Купили {n1} одиниць.", f"C = {a1} ∙ {n1} = {C1}"),
            (f"2) За {n2} однакових товарів заплатили {C2} грн. Знайди ціну одного.", f"a = {C2} : {n2} = {a2}"),
            (f"3) За {t3} хв виконали {A3} операцій. Знайди продуктивність.", f"N = {A3} : {t3} = {N3}"),
            (f"4) Пристрій обробляє {N4} деталей за хвилину. Скільки деталей за {t4} хв?", f"A = {N4} ∙ {t4} = {A4}"),
            (f"5) Майстер виготовляє {N5} деталей за годину. За скільки годин {A5} деталей?", f"t = {A5} : {N5} = {t5}"),
            (f"6) Є {pay} грн. Вартість покупки: 2∙{price_nb} + 3∙{price_p}. Знайди решту.", f"{pay} - (2∙{price_nb} + 3∙{price_p}) = {pay - total}"),
        ]

        for q, s in examples:
            row = tk.Frame(f, bg=WHITE, bd=1, relief="solid", padx=18, pady=10)
            row.pack(fill="x", pady=6)
            tk.Label(row, text=q, font=("Segoe UI", 16), bg=WHITE, fg=TEXT, justify="left").pack(anchor="w")
            tk.Label(row, text=s, font=("Consolas", 16, "bold"), bg=YELLOW_BG, fg=HL_FG, padx=10, pady=5).pack(
                anchor="w", pady=(8, 0)
            )

    def show_trainer(self):
        self.clear_main()

        LW = int(self.SW * 0.60)
        RW = self.SW - LW

        left = tk.Frame(self.main_area, bg=BG, width=LW)
        left.pack(side="left", fill="both")
        left.pack_propagate(False)

        self.task_box = tk.Frame(left, bg=WHITE, bd=3, relief="solid", padx=40, pady=35)
        self.task_box.pack(pady=25)
        self.task_text = tk.Label(self.task_box, text="", font=("Segoe UI", 20), bg=WHITE, fg=TEXT, justify="left", wraplength=LW - 100)
        self.task_text.pack()

        self.display_frame = tk.Frame(left, bg=WHITE, highlightbackground=ACCENT, highlightthickness=2)
        self.display_frame.pack(pady=10, ipadx=24, ipady=10)
        self.lbl_display = tk.Label(self.display_frame, text="", bg=WHITE, fg=TEXT, font=("Segoe UI", 48, "bold"), width=12, anchor="e")
        self.lbl_display.pack()

        self.lbl_feedback = tk.Label(left, text="", bg=BG, font=("Segoe UI", 20, "bold"), justify="center")
        self.lbl_feedback.pack(pady=10)

        kbd = tk.Frame(left, bg=BG)
        kbd.pack(pady=10)
        rows = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["C", "0", "⌫"]]
        for row in rows:
            r = tk.Frame(kbd, bg=BG)
            r.pack(pady=2)
            for ch in row:
                tk.Button(
                    r,
                    text=ch,
                    bg=RED_BG if ch in ("⌫", "C") else BTN_NUM,
                    fg=TEXT,
                    font=("Segoe UI", 20, "bold"),
                    width=6,
                    height=1,
                    relief="flat",
                    command=lambda c=ch: self._key_press(c),
                ).pack(side="left", padx=5)

        btn_f = tk.Frame(left, bg=BG)
        btn_f.pack(pady=10)
        self.btn_ok = tk.Button(
            btn_f,
            text="✓ Перевірити",
            bg=GREEN,
            fg=WHITE,
            font=("Segoe UI", 18, "bold"),
            relief="flat",
            padx=40,
            pady=10,
            command=self.check_answer,
        )
        self.btn_ok.pack(side="left", padx=20)
        self.btn_next = tk.Button(
            btn_f,
            text="▶ Наступне",
            bg=ACCENT,
            fg=WHITE,
            font=("Segoe UI", 18, "bold"),
            relief="flat",
            padx=40,
            pady=10,
            command=self.next_task,
        )

        right = tk.Frame(self.main_area, bg=PANEL, width=RW, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        rpad = tk.Frame(right, bg=PANEL)
        rpad.pack(fill="both", expand=True, padx=30, pady=30)

        tk.Label(rpad, text="Формули", font=("Segoe UI", 18, "bold"), bg=PANEL, fg=MUTED).pack(anchor="w")
        hint_box = tk.Frame(rpad, bg="#eff6ff", highlightbackground="#bfdbfe", highlightthickness=1, padx=15, pady=15)
        hint_box.pack(fill="x", pady=10)
        tk.Label(
            hint_box,
            text=(
                "Вартість товару:\n"
                "• C = a ∙ n\n"
                "• a = C : n\n"
                "• n = C : a\n\n"
                "Робота:\n"
                "• A = N ∙ t\n"
                "• N = A : t\n"
                "• t = A : N"
            ),
            font=("Segoe UI", 12),
            bg="#eff6ff",
            justify="left",
        ).pack(anchor="w")

        self.btn_task_hint = tk.Button(
            rpad,
            text="Підказка до задачі (схема)",
            font=("Segoe UI", 14, "bold"),
            bg=BTN_NUM,
            fg=TEXT,
            relief="flat",
            padx=15,
            pady=8,
            command=self.toggle_task_hint,
        )
        self.btn_task_hint.pack(fill="x", pady=(10, 0))

        self.task_hint_frame = tk.Frame(rpad, bg=WHITE, bd=1, relief="solid", padx=12, pady=12)
        self.task_hint_title = tk.Label(self.task_hint_frame, text="", font=("Segoe UI", 14, "bold"), bg=WHITE, fg=INDIGO)
        self.task_hint_title.pack(anchor="w")
        self.task_hint_formula = tk.Label(self.task_hint_frame, text="", font=("Consolas", 14, "bold"), bg=YELLOW_BG, fg=HL_FG, padx=10, pady=5)
        self.task_hint_formula.pack(anchor="w", pady=(8, 8))
        self.task_hint_canvas = tk.Canvas(self.task_hint_frame, bg=WHITE, height=110, highlightthickness=0)
        self.task_hint_canvas.pack(fill="x")
        self.task_hint_desc = tk.Label(self.task_hint_frame, text="", font=("Segoe UI", 11), bg=WHITE, fg=MUTED, justify="left", wraplength=RW - 80)
        self.task_hint_desc.pack(anchor="w", pady=(8, 0))

        self.lbl_score = tk.Label(rpad, text="Рахунок: 0 / 0", font=("Segoe UI", 24, "bold"), bg=PANEL, fg=ACCENT)
        self.lbl_score.pack(side="bottom", pady=20)

        self.next_task()

    def toggle_task_hint(self):
        self.task_hint_shown = not self.task_hint_shown
        if self.task_hint_shown:
            self.task_hint_frame.pack(fill="x", pady=(10, 0))
            self.btn_task_hint.config(text="Сховати підказку (схема)")
        else:
            self.task_hint_frame.pack_forget()
            self.btn_task_hint.config(text="Підказка до задачі (схема)")
        self._render_task_hint()

    def _render_task_hint(self):
        if not self.task_hint_shown:
            return
        if not self.task:
            return

        self.task_hint_title.config(text=self.task.get("hint_title", ""))
        self.task_hint_formula.config(text=self.task.get("hint_formula", ""))
        self.task_hint_desc.config(text=self.task.get("hint_desc", ""))

        cv = self.task_hint_canvas
        cv.delete("all")
        w = max(340, int(cv.winfo_width() or 340))
        y = 60

        def box(x, label, fill, outline, fg):
            cv.create_rectangle(x, y - 22, x + 110, y + 22, fill=fill, outline=outline, width=2)
            cv.create_text(x + 55, y, text=label, font=("Segoe UI", 10, "bold"), fill=fg)

        kind = self.task.get("kind")

        if kind.startswith("cost_"):
            box(20, "a", "#eff6ff", "#bfdbfe", ACCENT)
            cv.create_text(140, y, text="×", font=("Segoe UI", 16, "bold"), fill=MUTED)
            box(160, "n", "#fef9c3", "#fde68a", HL_FG)
            cv.create_text(280, y, text="=", font=("Segoe UI", 16, "bold"), fill=MUTED)
            box(300, "C", "#dcfce7", "#bbf7d0", GREEN)
        elif kind.startswith("work_"):
            box(20, "N", "#eff6ff", "#bfdbfe", ACCENT)
            cv.create_text(140, y, text="×", font=("Segoe UI", 16, "bold"), fill=MUTED)
            box(160, "t", "#fef9c3", "#fde68a", HL_FG)
            cv.create_text(280, y, text="=", font=("Segoe UI", 16, "bold"), fill=MUTED)
            box(300, "A", "#dcfce7", "#bbf7d0", GREEN)
        elif kind == "purchase_change":
            cv.create_text(20, 30, text="Гроші", font=("Segoe UI", 12, "bold"), anchor="w", fill=TEXT)
            cv.create_text(20, 60, text="мінус", font=("Segoe UI", 12), anchor="w", fill=MUTED)
            cv.create_text(20, 90, text="вартість покупки", font=("Segoe UI", 12, "bold"), anchor="w", fill=TEXT)
        elif kind == "bouquet":
            cv.create_text(20, 30, text="Гроші ÷ ціна = максимум квітів", font=("Segoe UI", 11, "bold"), anchor="w", fill=TEXT)
            cv.create_text(20, 60, text="Потім беремо найбільше НЕПАРНЕ", font=("Segoe UI", 11, "bold"), anchor="w", fill=ORANGE)

    def _key_press(self, ch):
        if self.phase != "answer":
            return
        if ch == "⌫":
            self.user_input = self.user_input[:-1]
        elif ch == "C":
            self.user_input = ""
        else:
            if len(self.user_input) < 10:
                self.user_input += ch
        if hasattr(self, "lbl_display"):
            self.lbl_display.config(text=self.user_input)

    def next_task(self):
        self.user_input = ""
        self.phase = "answer"
        if hasattr(self, "lbl_display"):
            self.lbl_display.config(text="", bg=WHITE)
        if hasattr(self, "display_frame"):
            self.display_frame.config(highlightbackground=ACCENT)
        if hasattr(self, "lbl_feedback"):
            self.lbl_feedback.config(text="")
        if hasattr(self, "btn_next"):
            self.btn_next.pack_forget()
        if hasattr(self, "btn_ok"):
            self.btn_ok.pack(side="left", padx=20)

        pool = [
            "cost_C",
            "cost_a",
            "cost_n",
            "work_A",
            "work_N",
            "work_t",
            "purchase_change",
            "bouquet",
        ]
        t = random.choice(pool)

        if t == "cost_C":
            a = self._pick_not_forbidden(8, 55)
            n = self._pick_not_forbidden(2, 14)
            ans = a * n
            text = f"Ціна товару {a} грн за одиницю. Купили {n} одиниць.\nЗнайди вартість покупки C (грн)."
            kind = "cost_C"
            hint_title = "Тип: знайти вартість"
            hint_formula = "C = a ∙ n"
            hint_desc = "Помнож ціну на кількість."
        elif t == "cost_a":
            n = self._pick_not_forbidden(2, 14)
            a = self._pick_not_forbidden(8, 55)
            C = a * n
            ans = a
            text = f"За {n} однакових товарів заплатили {C} грн.\nЗнайди ціну одного товару a (грн)."
            kind = "cost_a"
            hint_title = "Тип: знайти ціну"
            hint_formula = "a = C : n"
            hint_desc = "Поділи вартість на кількість."
        elif t == "cost_n":
            a = self._pick_not_forbidden(8, 55)
            n = self._pick_not_forbidden(2, 14)
            C = a * n
            ans = n
            text = f"Ціна товару {a} грн за одиницю. Заплатили {C} грн.\nСкільки одиниць купили (n)?"
            kind = "cost_n"
            hint_title = "Тип: знайти кількість"
            hint_formula = "n = C : a"
            hint_desc = "Поділи вартість на ціну."
        elif t == "work_A":
            N = self._pick_not_forbidden(2, 18)
            tt = self._pick_not_forbidden(2, 14)
            A = N * tt
            ans = A
            text = f"Продуктивність {N} деталей за годину. Працював {tt} год.\nСкільки деталей виготовив (A)?"
            kind = "work_A"
            hint_title = "Тип: знайти обсяг роботи"
            hint_formula = "A = N ∙ t"
            hint_desc = "Помнож продуктивність на час."
        elif t == "work_N":
            N = self._pick_not_forbidden(2, 18)
            tt = self._pick_not_forbidden(2, 14)
            A = N * tt
            ans = N
            text = f"За {tt} год виготовили {A} деталей.\nЗнайди продуктивність N (деталей/год)."
            kind = "work_N"
            hint_title = "Тип: знайти продуктивність"
            hint_formula = "N = A : t"
            hint_desc = "Поділи обсяг роботи на час."
        elif t == "work_t":
            N = self._pick_not_forbidden(2, 18)
            tt = self._pick_not_forbidden(2, 14)
            A = N * tt
            ans = tt
            text = f"Продуктивність {N} сторінок за хвилину. Надрукували {A} сторінок.\nЗнайди час t (хв)."
            kind = "work_t"
            hint_title = "Тип: знайти час"
            hint_formula = "t = A : N"
            hint_desc = "Поділи обсяг роботи на продуктивність."
        elif t == "purchase_change":
            price_nb = random.choice([17, 19, 23, 29, 31])
            price_p = random.choice([5, 9, 11, 13])
            pay = random.choice([150, 250, 350, 450])
            total = 2 * price_nb + 3 * price_p
            ans = pay - total
            text = f"Покупець купив 2 зошити по {price_nb} грн і 3 олівці по {price_p} грн.\nЯку решту отримає з {pay} грн?"
            kind = "purchase_change"
            hint_title = "Тип: покупка + решта"
            hint_formula = "решта = гроші - вартість"
            hint_desc = "Спочатку знайди вартість кожної покупки, потім відніми від суми грошей."
        else:
            price = random.choice([19, 23, 27, 31])
            money = random.choice([155, 215, 275, 335, 395])
            max_n = money // price
            if max_n % 2 == 0:
                max_n -= 1
            if max_n < 1:
                max_n = 1
            ans = max_n
            text = f"Потрібно купити букет з НЕПАРНОЮ кількістю квітів.\nЦіна квітки {price} грн. Є {money} грн.\nЯку найбільшу непарну кількість квітів можна купити?"
            kind = "bouquet"
            hint_title = "Тип: найбільше можливе"
            hint_formula = "n = гроші : ціна"
            hint_desc = "Знайди максимум квітів за гроші, а потім зроби кількість непарною."

        self.task = {"ans": int(ans), "text": text, "kind": kind, "hint_title": hint_title, "hint_formula": hint_formula, "hint_desc": hint_desc}
        if hasattr(self, "task_text"):
            self.task_text.config(text=text)
        self._render_task_hint()

    def check_answer(self):
        if self.phase != "answer":
            return
        raw = self.user_input.strip()
        if not raw:
            return

        self.phase = "feedback"
        self.total += 1
        try:
            got = int(raw)
        except ValueError:
            got = None

        ok = got == self.task["ans"]
        if ok:
            self.score += 1
            if hasattr(self, "lbl_feedback"):
                self.lbl_feedback.config(text="✅ Правильно!", fg=GREEN)
            if hasattr(self, "lbl_display"):
                self.lbl_display.config(bg=GREEN_BG)
            self.after(1000, self.next_task)
        else:
            if hasattr(self, "lbl_feedback"):
                self.lbl_feedback.config(text=f"❌ Помилка! Відповідь: {self.task['ans']}", fg=RED)
            if hasattr(self, "lbl_display"):
                self.lbl_display.config(bg=RED_BG)
            if hasattr(self, "btn_ok"):
                self.btn_ok.pack_forget()
            if hasattr(self, "btn_next"):
                self.btn_next.pack(side="left", padx=20)

        if hasattr(self, "lbl_score"):
            self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")


if __name__ == "__main__":
    app = EconomicProblemsApp()
    app.mainloop()
