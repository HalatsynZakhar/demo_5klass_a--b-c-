"""
Демонстрація: Координатний промінь. Шкала (§ 18).
Для 5 класу.
Координатний промінь, координата точки, порівняння чисел на промені, шкали та ціна поділки.
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
SKY = "#0ea5e9"


class CoordinateAxisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Координатний промінь. Шкала")
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
        self.user_input = ""
        self.score = 0
        self.total = 0
        self.phase = "answer"

        self.task_hint_shown = False

        self._build_ui()
        self.show_ray_intro()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=ACCENT, height=80)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(
            hdr,
            text="Координатний промінь. Шкала (§ 18)",
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
        tk.Button(nav, text="1. Координатний промінь", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_ray_intro).pack(
            side="left", padx=10
        )
        tk.Button(nav, text="2. Координата точки", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_coordinate).pack(
            side="left", padx=10
        )
        tk.Button(nav, text="3. Порівняння чисел", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_compare).pack(
            side="left", padx=10
        )
        tk.Button(nav, text="4. Шкала і ціна поділки", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_scales).pack(
            side="left", padx=10
        )
        tk.Button(nav, text="5. Тренажер", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_trainer).pack(
            side="left", padx=10
        )

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
        if ch == "⌫":
            self.user_input = self.user_input[:-1]
        elif ch == "C":
            self.user_input = ""
        else:
            if len(self.user_input) < 6:
                self.user_input += ch
        self.lbl_display.config(text=self.user_input)

    def show_ray_intro(self):
        self.clear_main()
        self.mode = "ray_intro"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)

        tk.Label(f, text="Координатний промінь", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        tk.Label(
            f,
            text=(
                "Координатний промінь — це промінь OX, на якому:\n"
                "• точка O — початок відліку (0)\n"
                "• позначено одиничний відрізок (довжина 1)\n"
                "• кожному натуральному числу відповідає певна точка"
            ),
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            justify="left",
            wraplength=self.SW - 140,
        ).pack(anchor="w", pady=(0, 10))

        cv = tk.Canvas(f, bg=WHITE, height=320, bd=2, relief="ridge")
        cv.pack(fill="x", pady=15, padx=10)
        w = self._canvas_width(cv, self.SW - 140)
        left = 80
        right = w - 80
        y = 180
        cv.create_line(left, y, right, y, width=4, fill=TEXT, arrow="last")
        cv.create_text(right - 10, y - 25, text="X", font=("Segoe UI", 14, "bold"), fill=TEXT, anchor="e")

        unit = (right - left) / 12
        for i in range(0, 13):
            x = left + i * unit
            cv.create_line(x, y, x, y - (40 if i % 1 == 0 else 25), width=2, fill=TEXT)
            cv.create_text(x, y + 20, text=str(i), font=("Segoe UI", 12, "bold"), fill=MUTED)

        cv.create_oval(left - 10, y - 10, left + 10, y + 10, fill=ORANGE, outline=WHITE, width=2)
        cv.create_text(left, y - 26, text="O", font=("Segoe UI", 12, "bold"), fill=TEXT)
        cv.create_text(left, y + 45, text="0", font=("Segoe UI", 12, "bold"), fill=TEXT)

        x1 = left + unit
        cv.create_oval(x1 - 9, y - 9, x1 + 9, y + 9, fill=INDIGO, outline=WHITE, width=2)
        cv.create_text(x1, y - 26, text="K", font=("Segoe UI", 12, "bold"), fill=TEXT)
        cv.create_text(x1, y + 45, text="1", font=("Segoe UI", 12, "bold"), fill=TEXT)
        cv.create_line(left, y - 75, x1, y - 75, width=5, fill=ACCENT)
        cv.create_text((left + x1) / 2, y - 98, text="одиничний відрізок", font=("Segoe UI", 12, "bold"), fill=ACCENT)

        tk.Label(f, text="Переходь до вкладки «Координата точки» і спробуй поставити точку на потрібному числі.", font=("Segoe UI", 16, "italic"), bg=BG, fg=MUTED).pack(
            pady=10
        )

    def show_coordinate(self):
        self.clear_main()
        self.mode = "coordinate"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=40, pady=20)

        tk.Label(f, text="Координата точки", font=("Segoe UI", 30, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))

        top = tk.Frame(f, bg=BG)
        top.pack(fill="x", pady=(0, 10))

        self.coord_msg = tk.Label(top, text="", font=("Segoe UI", 16, "bold"), bg=BG, fg=MUTED)
        self.coord_msg.pack(side="left")

        tk.Button(top, text="🎲 Нове число", font=("Segoe UI", 14, "bold"), bg=ACCENT, fg=WHITE, bd=0, padx=16, pady=10, command=self._coord_new).pack(
            side="right", padx=10
        )

        self.coord_canvas = tk.Canvas(f, bg=WHITE, height=300, bd=2, relief="ridge")
        self.coord_canvas.pack(fill="x", pady=10, padx=10)
        self.coord_canvas.bind("<Button-1>", self._coord_click)

        self.coord_feedback = tk.Label(f, text="", font=("Segoe UI", 18, "bold"), bg=BG)
        self.coord_feedback.pack(pady=10)

        self.coord_max = 14
        self.coord_target = 7
        self.coord_current = None
        self.after(80, self._coord_new)

    def _coord_new(self):
        self.coord_target = random.randint(2, self.coord_max)
        self.coord_current = None
        self.coord_feedback.config(text="", fg=TEXT)
        self.coord_msg.config(text=f"Постав точку A на числі {self.coord_target}. (Торкнись/клацни по шкалі)", fg=MUTED)
        self._coord_draw()

    def _coord_draw(self):
        cv = self.coord_canvas
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 160)
        left = 80
        right = w - 80
        y = 170
        cv.create_line(left, y, right, y, width=4, fill=TEXT, arrow="last")
        cv.create_text(right - 10, y - 25, text="X", font=("Segoe UI", 14, "bold"), fill=TEXT, anchor="e")

        unit = (right - left) / self.coord_max
        for i in range(0, self.coord_max + 1):
            x = left + i * unit
            cv.create_line(x, y, x, y - 35, width=2, fill=TEXT)
            cv.create_text(x, y + 20, text=str(i), font=("Segoe UI", 12, "bold"), fill=MUTED)
        cv.create_oval(left - 10, y - 10, left + 10, y + 10, fill=ORANGE, outline=WHITE, width=2)
        cv.create_text(left, y - 26, text="O", font=("Segoe UI", 12, "bold"), fill=TEXT)

        if self.coord_current is not None:
            x = left + self.coord_current * unit
            cv.create_line(x, y, x, y - 60, width=3, fill=ACCENT)
            cv.create_oval(x - 12, y - 12, x + 12, y + 12, fill=INDIGO, outline=WHITE, width=2)
            cv.create_text(x, y - 75, text=f"A({self.coord_current})", font=("Segoe UI", 14, "bold"), fill=INDIGO)

    def _coord_click(self, e):
        w = self._canvas_width(self.coord_canvas, self.SW - 160)
        left = 80
        right = w - 80
        unit = (right - left) / self.coord_max
        x = max(left, min(right, e.x))
        n = int(round((x - left) / unit))
        n = max(0, min(self.coord_max, n))
        self.coord_current = n
        self._coord_draw()
        if n == self.coord_target:
            self.coord_feedback.config(text="✅ Правильно!", fg=GREEN)
        else:
            self.coord_feedback.config(text="❌ Не збігається. Спробуй ще.", fg=RED)

    def show_compare(self):
        self.clear_main()
        self.mode = "compare"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=40, pady=20)

        tk.Label(f, text="Порівняння чисел на координатному промені", font=("Segoe UI", 26, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        tk.Label(
            f,
            text="Точка правіше відповідає більшому числу. Точка лівіше — меншому.",
            font=("Segoe UI", 16),
            bg=BG,
            fg=MUTED,
        ).pack(pady=(0, 10))

        self.compare_canvas = tk.Canvas(f, bg=WHITE, height=260, bd=2, relief="ridge")
        self.compare_canvas.pack(fill="x", pady=10, padx=10)

        row = tk.Frame(f, bg=BG)
        row.pack(pady=10)
        self.btn_a = tk.Button(row, text="A", font=("Segoe UI", 20, "bold"), bg=BTN_NUM, bd=0, padx=26, pady=12, command=lambda: self._compare_answer("A"))
        self.btn_b = tk.Button(row, text="B", font=("Segoe UI", 20, "bold"), bg=BTN_NUM, bd=0, padx=26, pady=12, command=lambda: self._compare_answer("B"))
        self.btn_a.pack(side="left", padx=15)
        self.btn_b.pack(side="left", padx=15)

        self.compare_msg = tk.Label(f, text="", font=("Segoe UI", 18, "bold"), bg=BG)
        self.compare_msg.pack(pady=10)

        tk.Button(f, text="🎲 Наступне", font=("Segoe UI", 16, "bold"), bg=ACCENT, fg=WHITE, bd=0, padx=20, pady=10, command=self._compare_new).pack(
            pady=5
        )

        self._compare_new()

    def _compare_new(self):
        self.compare_a = random.randint(2, 18)
        self.compare_b = random.randint(2, 18)
        while self.compare_b == self.compare_a:
            self.compare_b = random.randint(2, 18)
        self.compare_correct = "A" if self.compare_a > self.compare_b else "B"
        self.compare_msg.config(text="Яка точка має більшу координату? (Пам’ятай: правіше — більше)", fg=MUTED)
        self._compare_draw()

    def _compare_draw(self):
        cv = self.compare_canvas
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 160)
        left = 80
        right = w - 80
        y = 160
        cv.create_line(left, y, right, y, width=4, fill=TEXT, arrow="last")

        max_n = 20
        unit = (right - left) / max_n
        for i in range(0, max_n + 1, 2):
            x = left + i * unit
            cv.create_line(x, y, x, y - 25, width=2, fill=TEXT)
            cv.create_text(x, y + 18, text=str(i), font=("Segoe UI", 10, "bold"), fill=MUTED)

        xa = left + self.compare_a * unit
        xb = left + self.compare_b * unit
        cv.create_oval(xa - 12, y - 12, xa + 12, y + 12, fill=INDIGO, outline=WHITE, width=2)
        cv.create_text(xa, y - 24, text="A", font=("Segoe UI", 12, "bold"), fill=TEXT)
        cv.create_oval(xb - 12, y - 12, xb + 12, y + 12, fill=ORANGE, outline=WHITE, width=2)
        cv.create_text(xb, y - 24, text="B", font=("Segoe UI", 12, "bold"), fill=TEXT)

    def _compare_answer(self, pick):
        if pick == self.compare_correct:
            self.compare_msg.config(text=f"✅ Правильно! A({self.compare_a}), B({self.compare_b})", fg=GREEN)
        else:
            self.compare_msg.config(text=f"❌ Ні. Правильна відповідь: {self.compare_correct}. A({self.compare_a}), B({self.compare_b})", fg=RED)

    def show_scales(self):
        self.clear_main()
        self.mode = "scales"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=40, pady=20)

        tk.Label(f, text="Шкала і ціна поділки", font=("Segoe UI", 30, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        tk.Label(
            f,
            text="Шкала — система поділок із числами. Щоб читати показники, треба знати ціну поділки.",
            font=("Segoe UI", 16),
            bg=BG,
            fg=MUTED,
            wraplength=self.SW - 140,
            justify="left",
        ).pack(pady=(0, 10))

        cards = tk.Frame(f, bg=BG)
        cards.pack(fill="both", expand=True)

        c1 = tk.Frame(cards, bg=WHITE, bd=2, relief="solid", padx=20, pady=20)
        c1.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        tk.Label(c1, text="Лінійка", font=("Segoe UI", 18, "bold"), bg=WHITE, fg=ACCENT).pack(anchor="w")
        cv1 = tk.Canvas(c1, bg=WHITE, height=180, highlightthickness=0)
        cv1.pack(fill="x", pady=10)
        self._draw_ruler_scale(cv1)
        tk.Label(c1, text="Велика поділка — 1 см, мала — 1 мм.", font=("Segoe UI", 14), bg=WHITE, fg=MUTED).pack(anchor="w")

        c2 = tk.Frame(cards, bg=WHITE, bd=2, relief="solid", padx=20, pady=20)
        c2.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        tk.Label(c2, text="Термометр", font=("Segoe UI", 18, "bold"), bg=WHITE, fg=ORANGE).pack(anchor="w")
        cv2 = tk.Canvas(c2, bg=WHITE, height=180, highlightthickness=0)
        cv2.pack(fill="x", pady=10)
        self._draw_thermo(cv2, 18)
        tk.Label(c2, text="Ціна малої поділки: 1 °C.", font=("Segoe UI", 14), bg=WHITE, fg=MUTED).pack(anchor="w")

        c3 = tk.Frame(cards, bg=WHITE, bd=2, relief="solid", padx=20, pady=20)
        c3.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        tk.Label(c3, text="Спідометр", font=("Segoe UI", 18, "bold"), bg=WHITE, fg=INDIGO).pack(anchor="w")
        cv3 = tk.Canvas(c3, bg=WHITE, height=180, highlightthickness=0)
        cv3.pack(fill="x", pady=10)
        self._draw_speedo(cv3, 20, 40, 4)
        tk.Label(c3, text="Між 20 і 40 є 4 поділки → ціна: (40−20):4 = 5 км/год.", font=("Segoe UI", 14), bg=WHITE, fg=MUTED, wraplength=320, justify="left").pack(anchor="w")

    def _draw_ruler_scale(self, cv):
        cv.delete("all")
        w = self._canvas_width(cv, 420)
        left = 30
        right = w - 30
        y = 110
        cv.create_line(left, y, right, y, width=4, fill=TEXT)
        length_cm = 10
        unit = (right - left) / length_cm
        for cm in range(0, length_cm + 1):
            x = left + cm * unit
            cv.create_line(x, y, x, y - 50, width=2, fill=TEXT)
            cv.create_text(x, y + 18, text=str(cm), font=("Segoe UI", 10, "bold"), fill=MUTED)
            if cm < length_cm:
                for mm in range(1, 10):
                    xm = x + mm * (unit / 10)
                    h = 30 if mm == 5 else 22
                    cv.create_line(xm, y, xm, y - h, width=1, fill=BORDER)

    def _draw_thermo(self, cv, temp):
        cv.delete("all")
        w = self._canvas_width(cv, 420)
        x = w // 2
        top = 20
        bottom = 160
        cv.create_rectangle(x - 20, top, x + 20, bottom - 25, fill="#f8fafc", outline=BORDER, width=2)
        cv.create_oval(x - 28, bottom - 40, x + 28, bottom + 10, fill=RED, outline=WHITE, width=2)
        cv.create_rectangle(x - 8, bottom - 25 - temp * 4, x + 8, bottom - 25, fill=RED, outline="")
        cv.create_text(x + 60, top + 10, text="°C", font=("Segoe UI", 12, "bold"), fill=MUTED)
        for t in range(0, 31, 5):
            y = bottom - 25 - t * 4
            cv.create_line(x + 20, y, x + 45, y, width=2, fill=TEXT)
            cv.create_text(x + 60, y, text=str(t), font=("Segoe UI", 10, "bold"), fill=MUTED)
            for s in range(1, 5):
                ys = y - s * 4
                cv.create_line(x + 20, ys, x + 35, ys, width=1, fill=BORDER)

    def _draw_speedo(self, cv, a, b, divisions):
        cv.delete("all")
        w = self._canvas_width(cv, 420)
        cx, cy = w // 2, 120
        r = 75
        cv.create_oval(cx - r, cy - r, cx + r, cy + r, outline=BORDER, width=3, fill="#f8fafc")
        cv.create_text(cx, cy + r + 10, text="км/год", font=("Segoe UI", 10, "bold"), fill=MUTED)
        start_ang = 200
        end_ang = -20
        cv.create_arc(cx - r, cy - r, cx + r, cy + r, start=start_ang, extent=end_ang - start_ang, style="arc", width=3, outline=TEXT)
        span = end_ang - start_ang
        for i in range(divisions + 1):
            ang = start_ang + (span * i / divisions)
            x1 = cx + (r - 10) * self._cos_deg(ang)
            y1 = cy - (r - 10) * self._sin_deg(ang)
            x2 = cx + (r - 25) * self._cos_deg(ang)
            y2 = cy - (r - 25) * self._sin_deg(ang)
            cv.create_line(x1, y1, x2, y2, width=3, fill=TEXT)
        cv.create_text(cx - 40, cy - 10, text=str(a), font=("Segoe UI", 12, "bold"), fill=MUTED)
        cv.create_text(cx + 40, cy - 10, text=str(b), font=("Segoe UI", 12, "bold"), fill=MUTED)

    def _cos_deg(self, deg):
        import math
        return math.cos(math.radians(deg))

    def _sin_deg(self, deg):
        import math
        return math.sin(math.radians(deg))

    def show_trainer(self):
        self.clear_main()
        self.mode = "trainer"

        LW = int(self.SW * 0.62)
        RW = self.SW - LW

        left = tk.Frame(self.main_area, bg=BG, width=LW)
        left.pack(side="left", fill="both")
        left.pack_propagate(False)

        tk.Label(left, text="Тренажер", font=("Segoe UI", 30, "bold"), bg=BG, fg=TEXT).pack(pady=(25, 5))
        self.lbl_score = tk.Label(left, text="Рахунок: 0 / 0", font=("Segoe UI", 18, "bold"), bg=BG, fg=ACCENT)
        self.lbl_score.pack(pady=(0, 10))

        self.task_box = tk.Frame(left, bg=WHITE, bd=3, relief="solid", padx=30, pady=20)
        self.task_box.pack(pady=10, padx=20, fill="x")
        self.task_text = tk.Label(self.task_box, text="", font=("Segoe UI", 18, "bold"), bg=WHITE, fg=TEXT, justify="left", wraplength=LW - 120)
        self.task_text.pack(anchor="w")

        self.task_canvas = tk.Canvas(left, bg=WHITE, height=260, bd=2, relief="ridge")
        self.task_canvas.pack(pady=10, padx=20, fill="x")
        self.task_canvas.bind("<Button-1>", self._trainer_click)

        self.display_frame = tk.Frame(left, bg=WHITE, highlightbackground=ACCENT, highlightthickness=2)
        self.display_frame.pack(pady=10, ipadx=24, ipady=10)
        self.lbl_display = tk.Label(self.display_frame, text="", bg=WHITE, fg=TEXT, font=("Segoe UI", 48, "bold"), width=12, anchor="e")
        self.lbl_display.pack()

        self.lbl_feedback = tk.Label(left, text="", font=("Segoe UI", 18, "bold"), bg=BG)
        self.lbl_feedback.pack(pady=10)

        kbd = tk.Frame(left, bg=BG)
        kbd.pack(pady=10)
        rows = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["C", "0", "⌫"]]
        for row in rows:
            r = tk.Frame(kbd, bg=BG)
            r.pack(pady=2)
            for ch in row:
                tk.Button(r, text=ch, bg=RED_BG if ch in ("⌫", "C") else BTN_NUM, font=("Segoe UI", 20, "bold"), width=6, height=1, relief="flat", command=lambda c=ch: self._key_press(c)).pack(
                    side="left", padx=5
                )

        btn_f = tk.Frame(left, bg=BG)
        btn_f.pack(pady=10)
        self.btn_ok = tk.Button(btn_f, text="✓ Перевірити", bg=GREEN, fg=WHITE, font=("Segoe UI", 18, "bold"), relief="flat", padx=40, pady=10, command=self.check_answer)
        self.btn_ok.pack(side="left", padx=20)
        self.btn_next = tk.Button(btn_f, text="▶ Наступне", bg=ACCENT, fg=WHITE, font=("Segoe UI", 18, "bold"), relief="flat", padx=40, pady=10, command=self.next_task)

        right = tk.Frame(self.main_area, bg=PANEL, width=RW, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        rpad = tk.Frame(right, bg=PANEL)
        rpad.pack(fill="both", expand=True, padx=25, pady=25)

        tk.Label(rpad, text="Підказка", font=("Segoe UI", 18, "bold"), bg=PANEL, fg=MUTED).pack(anchor="w")
        hint_box = tk.Frame(rpad, bg="#eff6ff", highlightbackground="#bfdbfe", highlightthickness=1, padx=15, pady=15)
        hint_box.pack(fill="x", pady=10)
        tk.Label(
            hint_box,
            text=(
                "• Координата — число біля точки\n"
                "• Правіше — більше, лівіше — менше\n"
                "• Ціна поділки = (більше − менше) : кількість поділок"
            ),
            font=("Segoe UI", 12),
            bg="#eff6ff",
            justify="left",
        ).pack(anchor="w")

        self.task_hint_shown = False
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
        self.task_hint_text = tk.Label(self.task_hint_frame, text="", font=("Segoe UI", 11), bg=WHITE, fg=MUTED, justify="left", wraplength=RW - 80)
        self.task_hint_text.pack(anchor="w", pady=(8, 0))

        self.after(80, self.next_task)

    def toggle_task_hint(self):
        self.task_hint_shown = not self.task_hint_shown
        if self.task_hint_shown:
            self.task_hint_frame.pack(fill="x", pady=(10, 0))
            self.btn_task_hint.config(text="Сховати підказку")
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
        self.task_hint_text.config(text=self.task.get("hint_text", ""))

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

        t = random.choice(["read_coord", "place_coord", "scale_price", "read_thermo"])

        if t == "read_coord":
            n = random.randint(2, 14)
            self.task = {"type": "read_coord", "ans": n, "chosen": None, "hint_title": "Підказка: координата", "hint_text": "Координата — це число, що відповідає точці на промені."}
            self.task_text.config(text="Яка координата точки A?")
            self._draw_read_coord(n)
        elif t == "place_coord":
            n = random.randint(2, 14)
            self.task = {"type": "place_coord", "ans": n, "chosen": None, "placed": None, "hint_title": "Підказка: постав точку", "hint_text": "Клацни на поділку з потрібним числом."}
            self.task_text.config(text=f"Постав точку A на числі {n}. Потім натисни «Перевірити».")
            self._draw_place_coord(n)
        elif t == "scale_price":
            a = random.choice([20, 30, 40, 50, 60, 80, 100, 200])
            step = random.choice([2, 5, 10, 20])
            b = a + step * random.choice([3, 4, 5])
            divs = (b - a) // step
            ans = step
            self.task = {"type": "scale_price", "ans": ans, "a": a, "b": b, "divs": divs, "hint_title": "Підказка: ціна поділки", "hint_text": "Ціна поділки = (b − a) : кількість поділок між ними."}
            self.task_text.config(text=f"На шкалі між {a} і {b} є {divs} поділок. Знайди ціну поділки.")
            self._draw_scale_price(a, b, divs)
        else:
            temp = random.randint(12, 28)
            self.task = {"type": "read_thermo", "ans": temp, "hint_title": "Підказка: термометр", "hint_text": "Мала поділка — 1 °C. Знайди, на якому числі закінчується стовпчик."}
            self.task_text.config(text="Яку температуру показує термометр?")
            self._draw_thermo_task(temp)

        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")
        self._render_task_hint()

    def _draw_read_coord(self, n):
        cv = self.task_canvas
        w = self._canvas_width(cv, self.SW * 0.62 - 60)
        left = 70
        right = w - 70
        y = 170
        cv.create_line(left, y, right, y, width=4, fill=TEXT, arrow="last")
        max_n = 14
        unit = (right - left) / max_n
        for i in range(0, max_n + 1):
            x = left + i * unit
            cv.create_line(x, y, x, y - 28, width=2, fill=TEXT)
            cv.create_text(x, y + 18, text=str(i), font=("Segoe UI", 10, "bold"), fill=MUTED)
        x = left + n * unit
        cv.create_oval(x - 12, y - 12, x + 12, y + 12, fill=INDIGO, outline=WHITE, width=2)
        cv.create_text(x, y - 24, text="A", font=("Segoe UI", 12, "bold"), fill=TEXT)

    def _draw_place_coord(self, n):
        cv = self.task_canvas
        w = self._canvas_width(cv, self.SW * 0.62 - 60)
        left = 70
        right = w - 70
        y = 170
        cv.create_line(left, y, right, y, width=4, fill=TEXT, arrow="last")
        self.place_left = left
        self.place_right = right
        self.place_max = 14
        unit = (right - left) / self.place_max
        for i in range(0, self.place_max + 1):
            x = left + i * unit
            cv.create_line(x, y, x, y - 28, width=2, fill=TEXT)
            cv.create_text(x, y + 18, text=str(i), font=("Segoe UI", 10, "bold"), fill=MUTED)
        cv.create_text(left, y - 45, text="Клацни на шкалі", font=("Segoe UI", 12, "bold"), fill=MUTED, anchor="w")

    def _trainer_click(self, e):
        if self.mode != "trainer":
            return
        if not self.task or self.task.get("type") != "place_coord":
            return
        left = getattr(self, "place_left", None)
        right = getattr(self, "place_right", None)
        max_n = getattr(self, "place_max", None)
        if left is None or right is None or max_n is None:
            return
        unit = (right - left) / max_n
        x = max(left, min(right, e.x))
        n = int(round((x - left) / unit))
        n = max(0, min(max_n, n))
        self.task["placed"] = n
        self._draw_place_coord(self.task["ans"])
        cv = self.task_canvas
        y = 170
        xp = left + n * unit
        cv.create_oval(xp - 12, y - 12, xp + 12, y + 12, fill=INDIGO, outline=WHITE, width=2)
        cv.create_text(xp, y - 24, text=f"A({n})", font=("Segoe UI", 12, "bold"), fill=TEXT)

    def _draw_scale_price(self, a, b, divs):
        cv = self.task_canvas
        w = self._canvas_width(cv, self.SW * 0.62 - 60)
        left = 90
        right = w - 90
        y = 150
        cv.create_line(left, y, right, y, width=4, fill=TEXT)
        cv.create_text(left, y + 20, text=str(a), font=("Segoe UI", 10, "bold"), fill=MUTED)
        cv.create_text(right, y + 20, text=str(b), font=("Segoe UI", 10, "bold"), fill=MUTED)
        cv.create_line(left, y, left, y - 50, width=3, fill=TEXT)
        cv.create_line(right, y, right, y - 50, width=3, fill=TEXT)
        step_px = (right - left) / divs
        for i in range(1, divs):
            x = left + i * step_px
            cv.create_line(x, y, x, y - 30, width=2, fill=BORDER)
        cv.create_text(left, 40, text="Поділки між двома числами", font=("Segoe UI", 12, "bold"), fill=MUTED, anchor="w")

    def _draw_thermo_task(self, temp):
        cv = self.task_canvas
        w = self._canvas_width(cv, self.SW * 0.62 - 60)
        cv.delete("all")
        x = w // 2
        top = 30
        bottom = 240
        cv.create_rectangle(x - 22, top, x + 22, bottom - 30, fill="#f8fafc", outline=BORDER, width=2)
        cv.create_oval(x - 30, bottom - 45, x + 30, bottom + 10, fill=RED, outline=WHITE, width=2)
        cv.create_rectangle(x - 9, bottom - 30 - temp * 5, x + 9, bottom - 30, fill=RED, outline="")
        for t in range(0, 31, 5):
            y = bottom - 30 - t * 5
            cv.create_line(x + 22, y, x + 48, y, width=2, fill=TEXT)
            cv.create_text(x + 65, y, text=str(t), font=("Segoe UI", 10, "bold"), fill=MUTED)
            for s in range(1, 5):
                ys = y - s * 5
                cv.create_line(x + 22, ys, x + 38, ys, width=1, fill=BORDER)
        cv.create_text(x + 62, top + 8, text="°C", font=("Segoe UI", 12, "bold"), fill=MUTED)

    def check_answer(self):
        if self.mode != "trainer":
            return
        if self.phase != "answer":
            return
        if not self.task:
            return

        t = self.task["type"]
        if t == "place_coord":
            if self.task.get("placed") is None:
                return
            got = self.task["placed"]
        else:
            raw = self.user_input.strip()
            if not raw:
                return
            try:
                got = int(raw)
            except ValueError:
                return

        self.phase = "feedback"
        self.total += 1

        ok = got == self.task["ans"]
        if ok:
            self.score += 1
            self.lbl_feedback.config(text="✅ Правильно!", fg=GREEN)
            self.lbl_display.config(bg=GREEN_BG)
            self.after(900, self.next_task)
        else:
            self.lbl_feedback.config(text=f"❌ Ні. Відповідь: {self.task['ans']}", fg=RED)
            self.lbl_display.config(bg=RED_BG)
            self.btn_ok.pack_forget()
            self.btn_next.pack(side="left", padx=20)

        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")


if __name__ == "__main__":
    app = CoordinateAxisApp()
    app.mainloop()
