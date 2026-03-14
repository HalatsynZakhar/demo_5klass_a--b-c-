"""
Демонстрація: Відрізок. Довжина відрізка (§ 16).
Для 5 класу.
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


class SegmentsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Відрізок. Довжина відрізка")
        self.configure(bg=BG)

        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.bind("<Key>", self._on_key_press)
        self.bind("<Return>", lambda e: self.check_answer())
        self.bind("<BackSpace>", lambda e: self._key_press("⌫"))
        self.bind("<Delete>", lambda e: self._key_press("C"))

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()

        self.forbidden_nums = {
            1,
            2,
            3,
            4,
            7,
            8,
            9,
            10,
            21,
            42,
            43,
            56,
            63,
            75,
        }

        self.mode = None
        self.user_input = ""
        self.phase = "answer"
        self.task = None
        self.score = 0
        self.total = 0

        self.task_hint_shown = False

        self._build_ui()
        self.show_units()

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
            text="Відрізок. Довжина відрізка (§ 16)",
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
        tk.Button(nav, text="1. Одиниці", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_units).pack(
            side="left", padx=10
        )
        tk.Button(nav, text="2. Лінійка", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_ruler).pack(
            side="left", padx=10
        )
        tk.Button(
            nav,
            text="3. Порівняння",
            font=btn_font,
            bg=WHITE,
            bd=0,
            cursor="hand2",
            command=self.show_compare,
        ).pack(side="left", padx=10)
        tk.Button(
            nav,
            text="4. Поділ відрізка",
            font=btn_font,
            bg=WHITE,
            bd=0,
            cursor="hand2",
            command=self.show_split,
        ).pack(side="left", padx=10)
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

    def show_units(self):
        self.clear_main()
        self.mode = "units"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)

        tk.Label(f, text="Одиниці вимірювання довжини", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(
            pady=(0, 15)
        )

        box = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=25, pady=20)
        box.pack(fill="x", pady=10)

        tk.Label(
            box,
            text=(
                "Співвідношення між одиницями:\n\n"
                "1 см = 10 мм\n"
                "1 дм = 10 см\n"
                "1 м = 10 дм = 100 см\n"
                "1 км = 1000 м"
            ),
            font=("Segoe UI", 20),
            bg=WHITE,
            fg=TEXT,
            justify="left",
        ).pack(anchor="w")

        a_cm = self._pick_not_forbidden(2, 9)
        b_mm = self._pick_not_forbidden(1, 9)
        total_mm = a_cm * 10 + b_mm
        ex = tk.Frame(f, bg=YELLOW_BG, bd=1, relief="solid", padx=20, pady=15)
        ex.pack(fill="x", pady=15)
        tk.Label(ex, text="Приклад перетворення:", font=("Segoe UI", 18, "bold"), bg=YELLOW_BG, fg=TEXT).pack(anchor="w")
        tk.Label(ex, text=f"{a_cm} см {b_mm} мм = {total_mm} мм", font=("Consolas", 22, "bold"), bg=YELLOW_BG, fg=HL_FG).pack(
            anchor="w", pady=(6, 0)
        )

        tk.Label(
            f,
            text="Вимірювання відрізків роблять лінійкою: порівнюють довжину відрізка з одиницею довжини.",
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            justify="left",
            wraplength=self.SW - 140,
        ).pack(anchor="w", pady=10)

    def show_ruler(self):
        self.clear_main()
        self.mode = "ruler"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=20)

        top = tk.Frame(f, bg=BG)
        top.pack(fill="x")

        tk.Label(top, text="Лінійка та вимірювання відрізків", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(
            side="left"
        )

        btns = tk.Frame(top, bg=BG)
        btns.pack(side="right")

        tk.Button(
            btns,
            text="🎲 Нове завдання",
            font=("Segoe UI", 14, "bold"),
            bg=ACCENT,
            fg=WHITE,
            bd=0,
            padx=18,
            pady=10,
            command=self._ruler_new_task,
        ).pack(side="left", padx=8)

        tk.Button(
            btns,
            text="✓ Перевірити",
            font=("Segoe UI", 14, "bold"),
            bg=GREEN,
            fg=WHITE,
            bd=0,
            padx=18,
            pady=10,
            command=self._ruler_check_task,
        ).pack(side="left", padx=8)

        self.ruler_msg = tk.Label(f, text="", font=("Segoe UI", 16, "bold"), bg=BG, fg=MUTED)
        self.ruler_msg.pack(pady=(10, 0))

        self.ruler_canvas = tk.Canvas(f, bg=WHITE, height=280, bd=2, relief="ridge")
        self.ruler_canvas.pack(fill="x", pady=15, padx=10)

        self.ruler_len_lbl = tk.Label(f, text="", font=("Segoe UI", 18, "bold"), bg=BG, fg=TEXT)
        self.ruler_len_lbl.pack(pady=(5, 0))

        self.ruler_px_per_mm = 7
        self.ruler_origin_x = 60
        self.ruler_origin_y = 170
        self.ruler_max_cm = 12

        self.ruler_drag = None
        self.ruler_a_mm = 10
        self.ruler_b_mm = 70
        self.ruler_target_mm = None

        self._ruler_new_task()

    def _ruler_draw(self):
        cv = self.ruler_canvas
        cv.delete("all")

        max_mm = self.ruler_max_cm * 10
        x0 = self.ruler_origin_x
        y0 = self.ruler_origin_y
        px = self.ruler_px_per_mm

        cv.create_rectangle(x0 - 20, y0 - 80, x0 + max_mm * px + 20, y0 + 40, fill="#f8fafc", outline="#e2e8f0")
        cv.create_line(x0, y0, x0 + max_mm * px, y0, width=3, fill=TEXT)

        for mm in range(0, max_mm + 1):
            x = x0 + mm * px
            if mm % 10 == 0:
                h = 50
                cv.create_line(x, y0, x, y0 - h, width=2, fill=TEXT)
                cv.create_text(x, y0 + 18, text=str(mm // 10), font=("Segoe UI", 10, "bold"), fill=MUTED)
            elif mm % 5 == 0:
                h = 35
                cv.create_line(x, y0, x, y0 - h, width=2, fill=MUTED)
            else:
                h = 22
                cv.create_line(x, y0, x, y0 - h, width=1, fill=BORDER)

        y_seg = y0 - 110
        ax = x0 + self.ruler_a_mm * px
        bx = x0 + self.ruler_b_mm * px
        cv.create_line(ax, y_seg, bx, y_seg, width=6, fill=ACCENT)

        self.ruler_point_a = cv.create_oval(ax - 12, y_seg - 12, ax + 12, y_seg + 12, fill=ORANGE, outline=WHITE, width=2)
        self.ruler_point_b = cv.create_oval(bx - 12, y_seg - 12, bx + 12, y_seg + 12, fill=ORANGE, outline=WHITE, width=2)
        cv.create_text(ax, y_seg - 26, text="A", font=("Segoe UI", 12, "bold"), fill=TEXT)
        cv.create_text(bx, y_seg - 26, text="B", font=("Segoe UI", 12, "bold"), fill=TEXT)

        self.ruler_canvas.tag_bind(self.ruler_point_a, "<Button-1>", lambda e: self._ruler_start_drag("A", e.x))
        self.ruler_canvas.tag_bind(self.ruler_point_b, "<Button-1>", lambda e: self._ruler_start_drag("B", e.x))
        self.ruler_canvas.bind("<B1-Motion>", self._ruler_drag_move)
        self.ruler_canvas.bind("<ButtonRelease-1>", self._ruler_end_drag)

        self._ruler_update_len()

    def _ruler_start_drag(self, which, x):
        self.ruler_drag = (which, x)

    def _ruler_drag_move(self, e):
        if not self.ruler_drag:
            return

        which, _ = self.ruler_drag
        px = self.ruler_px_per_mm
        max_mm = self.ruler_max_cm * 10
        mm = round((e.x - self.ruler_origin_x) / px)
        mm = max(0, min(max_mm, mm))

        if which == "A":
            self.ruler_a_mm = mm
        else:
            self.ruler_b_mm = mm

        if self.ruler_a_mm > self.ruler_b_mm:
            self.ruler_a_mm, self.ruler_b_mm = self.ruler_b_mm, self.ruler_a_mm
            self.ruler_drag = ("A" if which == "B" else "B", e.x)

        self._ruler_draw()

    def _ruler_end_drag(self, _e):
        self.ruler_drag = None

    def _ruler_update_len(self):
        length_mm = self.ruler_b_mm - self.ruler_a_mm
        cm = length_mm // 10
        mm = length_mm % 10
        self.ruler_len_lbl.config(text=f"AB = {cm} см {mm} мм  (тобто {length_mm} мм)")

    def _ruler_new_task(self):
        target_cm = self._pick_not_forbidden(2, self.ruler_max_cm - 2)
        target_mm = self._pick_not_forbidden(0, 9)
        self.ruler_target_mm = target_cm * 10 + target_mm

        max_mm = self.ruler_max_cm * 10
        left = self._pick_not_forbidden(0, max_mm - self.ruler_target_mm)
        self.ruler_a_mm = left
        self.ruler_b_mm = left + self.ruler_target_mm

        self.ruler_msg.config(text=f"Завдання: встанови довжину AB = {target_cm} см {target_mm} мм", fg=MUTED)
        self._ruler_draw()

    def _ruler_check_task(self):
        length_mm = self.ruler_b_mm - self.ruler_a_mm
        if self.ruler_target_mm is None:
            return
        if length_mm == self.ruler_target_mm:
            self.ruler_msg.config(text="✅ Правильно! Довжина збігається.", fg=GREEN)
        else:
            self.ruler_msg.config(text=f"❌ Не збігається. Зараз AB = {length_mm} мм.", fg=RED)

    def show_compare(self):
        self.clear_main()
        self.mode = "compare"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=20)

        tk.Label(f, text="Порівняння відрізків", font=("Segoe UI", 30, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        self.compare_msg = tk.Label(f, text="", font=("Segoe UI", 16, "bold"), bg=BG, fg=MUTED)
        self.compare_msg.pack()

        self.compare_canvas = tk.Canvas(f, bg=WHITE, height=220, bd=2, relief="ridge")
        self.compare_canvas.pack(fill="x", pady=15, padx=10)

        btn_row = tk.Frame(f, bg=BG)
        btn_row.pack(pady=10)

        self.btn_gt = tk.Button(btn_row, text="AB > CD", font=("Segoe UI", 18, "bold"), bg=BTN_NUM, bd=0, padx=25, pady=12, command=lambda: self._compare_answer(">"))
        self.btn_lt = tk.Button(btn_row, text="AB < CD", font=("Segoe UI", 18, "bold"), bg=BTN_NUM, bd=0, padx=25, pady=12, command=lambda: self._compare_answer("<"))
        self.btn_eq = tk.Button(btn_row, text="AB = CD", font=("Segoe UI", 18, "bold"), bg=BTN_NUM, bd=0, padx=25, pady=12, command=lambda: self._compare_answer("="))
        self.btn_gt.pack(side="left", padx=12)
        self.btn_lt.pack(side="left", padx=12)
        self.btn_eq.pack(side="left", padx=12)

        tk.Button(f, text="🎲 Наступне", font=("Segoe UI", 16, "bold"), bg=ACCENT, fg=WHITE, bd=0, padx=22, pady=10, command=self._compare_new).pack(
            pady=10
        )

        self._compare_new()

    def _compare_new(self):
        self.compare_msg.config(text="Порівняй відрізки AB і CD.", fg=MUTED)
        self.compare_a = self._pick_not_forbidden(20, 115)
        self.compare_c = self._pick_not_forbidden(20, 115)
        if random.random() < 0.25:
            self.compare_c = self.compare_a

        if self.compare_a > self.compare_c:
            self.compare_correct = ">"
        elif self.compare_a < self.compare_c:
            self.compare_correct = "<"
        else:
            self.compare_correct = "="

        self._compare_draw()

    def _compare_draw(self):
        cv = self.compare_canvas
        cv.delete("all")

        w = int(cv.winfo_width() or (self.SW - 120))
        left = 80
        top1 = 70
        top2 = 150
        max_len = max(self.compare_a, self.compare_c, 1)
        scale = (w - 2 * left) / max_len

        a_len = self.compare_a * scale
        c_len = self.compare_c * scale

        cv.create_text(30, top1, text="A", font=("Segoe UI", 12, "bold"), fill=TEXT)
        cv.create_text(30, top2, text="C", font=("Segoe UI", 12, "bold"), fill=TEXT)

        cv.create_line(left, top1, left + a_len, top1, width=6, fill=ACCENT)
        cv.create_oval(left - 10, top1 - 10, left + 10, top1 + 10, fill=ORANGE, outline=WHITE, width=2)
        cv.create_oval(left + a_len - 10, top1 - 10, left + a_len + 10, top1 + 10, fill=ORANGE, outline=WHITE, width=2)
        cv.create_text(left, top1 - 24, text="A", font=("Segoe UI", 12, "bold"), fill=TEXT)
        cv.create_text(left + a_len, top1 - 24, text="B", font=("Segoe UI", 12, "bold"), fill=TEXT)

        cv.create_line(left, top2, left + c_len, top2, width=6, fill=INDIGO)
        cv.create_oval(left - 10, top2 - 10, left + 10, top2 + 10, fill=ORANGE, outline=WHITE, width=2)
        cv.create_oval(left + c_len - 10, top2 - 10, left + c_len + 10, top2 + 10, fill=ORANGE, outline=WHITE, width=2)
        cv.create_text(left, top2 - 24, text="C", font=("Segoe UI", 12, "bold"), fill=TEXT)
        cv.create_text(left + c_len, top2 - 24, text="D", font=("Segoe UI", 12, "bold"), fill=TEXT)

    def _compare_answer(self, sign):
        if sign == self.compare_correct:
            self.compare_msg.config(text="✅ Правильно!", fg=GREEN)
        else:
            self.compare_msg.config(text=f"❌ Ні. Правильна відповідь: AB {self.compare_correct} CD", fg=RED)

    def show_split(self):
        self.clear_main()
        self.mode = "split"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=20)

        tk.Label(f, text="Поділ відрізка на частини", font=("Segoe UI", 30, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))

        top = tk.Frame(f, bg=BG)
        top.pack(fill="x")

        self.split_msg = tk.Label(top, text="", font=("Segoe UI", 16, "bold"), bg=BG, fg=MUTED)
        self.split_msg.pack(side="left")

        tk.Button(top, text="🎲 Нове завдання", font=("Segoe UI", 14, "bold"), bg=ACCENT, fg=WHITE, bd=0, padx=16, pady=10, command=self._split_new).pack(
            side="right", padx=10
        )

        body = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=20, pady=20)
        body.pack(fill="x", pady=15, padx=10)

        self.split_canvas = tk.Canvas(body, bg=WHITE, height=120, highlightthickness=0)
        self.split_canvas.pack(fill="x")

        fields = tk.Frame(body, bg=WHITE)
        fields.pack(pady=10)

        self.split_focus = "AP"
        self.user_ap = ""
        self.user_pb = ""

        self.frame_ap = tk.Frame(fields, bg=WHITE, highlightbackground=ACCENT, highlightthickness=2)
        self.frame_ap.pack(side="left", padx=20, ipadx=12, ipady=8)
        tk.Label(self.frame_ap, text="AP (см)", font=("Segoe UI", 12, "bold"), bg=WHITE, fg=MUTED).pack()
        self.lbl_ap = tk.Label(self.frame_ap, text="", font=("Segoe UI", 32, "bold"), bg=WHITE, fg=TEXT, width=5)
        self.lbl_ap.pack()
        self.lbl_ap.bind("<Button-1>", lambda e: self._split_set_focus("AP"))

        self.frame_pb = tk.Frame(fields, bg=WHITE, highlightbackground=BORDER, highlightthickness=2)
        self.frame_pb.pack(side="left", padx=20, ipadx=12, ipady=8)
        tk.Label(self.frame_pb, text="PB (см)", font=("Segoe UI", 12, "bold"), bg=WHITE, fg=MUTED).pack()
        self.lbl_pb = tk.Label(self.frame_pb, text="", font=("Segoe UI", 32, "bold"), bg=WHITE, fg=TEXT, width=5)
        self.lbl_pb.pack()
        self.lbl_pb.bind("<Button-1>", lambda e: self._split_set_focus("PB"))

        btns = tk.Frame(body, bg=WHITE)
        btns.pack(pady=10)

        tk.Button(btns, text="Перемкнути поле", font=("Segoe UI", 14, "bold"), bg=BTN_NUM, bd=0, padx=16, pady=10, command=self._split_toggle_focus).pack(
            side="left", padx=10
        )
        tk.Button(btns, text="✓ Перевірити", font=("Segoe UI", 14, "bold"), bg=GREEN, fg=WHITE, bd=0, padx=16, pady=10, command=self._split_check).pack(
            side="left", padx=10
        )

        self.split_feedback = tk.Label(f, text="", font=("Segoe UI", 18, "bold"), bg=BG)
        self.split_feedback.pack(pady=10)

        kbd = tk.Frame(f, bg=BG)
        kbd.pack(pady=10)
        rows = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["C", "0", "⌫"]]
        for row in rows:
            r = tk.Frame(kbd, bg=BG)
            r.pack(pady=2)
            for ch in row:
                tk.Button(r, text=ch, bg=RED_BG if ch in ("⌫", "C") else BTN_NUM, font=("Segoe UI", 20, "bold"), width=6, height=1, relief="flat", command=lambda c=ch: self._split_key(c)).pack(
                    side="left", padx=5
                )

        self.after(60, self._split_new)

    def _split_set_focus(self, field):
        if field not in ("AP", "PB"):
            return
        self.split_focus = field
        self._split_update_fields()

    def _split_toggle_focus(self):
        self.split_focus = "PB" if self.split_focus == "AP" else "AP"
        self._split_update_fields()

    def _split_update_fields(self):
        self.lbl_ap.config(text=self.user_ap)
        self.lbl_pb.config(text=self.user_pb)
        self.frame_ap.config(highlightbackground=ACCENT if self.split_focus == "AP" else BORDER)
        self.frame_pb.config(highlightbackground=ACCENT if self.split_focus == "PB" else BORDER)

    def _split_key(self, ch):
        if ch == "⌫":
            if self.split_focus == "AP":
                self.user_ap = self.user_ap[:-1]
            else:
                self.user_pb = self.user_pb[:-1]
        elif ch == "C":
            if self.split_focus == "AP":
                self.user_ap = ""
            else:
                self.user_pb = ""
        else:
            if self.split_focus == "AP":
                if len(self.user_ap) < 4:
                    self.user_ap += ch
            else:
                if len(self.user_pb) < 4:
                    self.user_pb += ch
        self._split_update_fields()

    def _split_new(self):
        self.user_ap = ""
        self.user_pb = ""
        self.split_focus = "AP"
        self.split_feedback.config(text="", fg=TEXT, bg=BG)

        k = random.choice([(2, 1), (3, 2), (4, 1)])
        r1, r2 = k
        part = self._pick_not_forbidden(8, 35)
        self.AB = (r1 + r2) * part
        self.AP = r1 * part
        self.PB = r2 * part

        self.split_msg.config(text=f"AB = {self.AB} см, AP : PB = {r1} : {r2}. Знайди AP і PB.", fg=MUTED)
        self._split_draw()
        self._split_update_fields()

    def _split_draw(self):
        cv = self.split_canvas
        cv.delete("all")
        w = int(cv.winfo_width())
        if w < 300:
            cv.update_idletasks()
            w = int(cv.winfo_width())
        if w < 300:
            w = int(self.SW - 200)
        left = 60
        right = w - 60
        y = 70
        cv.create_line(left, y, right, y, width=6, fill=ACCENT)
        cv.create_oval(left - 10, y - 10, left + 10, y + 10, fill=ORANGE, outline=WHITE, width=2)
        cv.create_oval(right - 10, y - 10, right + 10, y + 10, fill=ORANGE, outline=WHITE, width=2)
        cv.create_text(left, y - 22, text="A", font=("Segoe UI", 12, "bold"), fill=TEXT)
        cv.create_text(right, y - 22, text="B", font=("Segoe UI", 12, "bold"), fill=TEXT)

        p_pos = left + (right - left) * (self.AP / self.AB)
        cv.create_oval(p_pos - 10, y - 10, p_pos + 10, y + 10, fill=INDIGO, outline=WHITE, width=2)
        cv.create_text(p_pos, y + 24, text="P", font=("Segoe UI", 12, "bold"), fill=TEXT)
        cv.create_text((left + p_pos) / 2, y - 26, text="AP", font=("Segoe UI", 12, "bold"), fill=MUTED)
        cv.create_text((p_pos + right) / 2, y - 26, text="PB", font=("Segoe UI", 12, "bold"), fill=MUTED)

    def _split_check(self):
        if not self.user_ap or not self.user_pb:
            return
        try:
            ap = int(self.user_ap)
            pb = int(self.user_pb)
        except ValueError:
            return
        ok = (ap == self.AP) and (pb == self.PB)
        if ok:
            self.split_feedback.config(text="✅ Правильно!", fg=GREEN)
        else:
            self.split_feedback.config(text=f"❌ Ні. Правильно: AP = {self.AP} см, PB = {self.PB} см", fg=RED)

    def show_trainer(self):
        self.clear_main()
        self.mode = "trainer"

        LW = int(self.SW * 0.60)
        RW = self.SW - LW

        left = tk.Frame(self.main_area, bg=BG, width=LW)
        left.pack(side="left", fill="both")
        left.pack_propagate(False)

        tk.Label(left, text="Тренажер: довжина відрізка", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(25, 10))

        self.task_box = tk.Frame(left, bg=WHITE, bd=3, relief="solid", padx=40, pady=30)
        self.task_box.pack(pady=15)
        self.task_text = tk.Label(self.task_box, text="", font=("Segoe UI", 20, "bold"), bg=WHITE, fg=TEXT, justify="left", wraplength=LW - 120)
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
                "• 1 см = 10 мм\n"
                "• AB = AM + MB (якщо M належить AB)\n"
                "• Рівні відрізки мають однакові довжини\n"
                "• Якщо AP : PB = m : n, то AB = (m+n) частин"
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
        w = max(360, int(cv.winfo_width() or 360))
        y = 60
        cv.create_line(20, y, w - 20, y, fill=MUTED, dash=(4, 4))

        kind = self.task.get("kind")
        if kind == "conv":
            cv.create_text(20, 30, text="см ↔ мм", font=("Segoe UI", 12, "bold"), anchor="w", fill=ACCENT)
            cv.create_text(20, 70, text="×10 або :10", font=("Segoe UI", 12, "bold"), anchor="w", fill=HL_FG)
        elif kind == "sum":
            left = 50
            right = w - 50
            p = left + (right - left) * 0.55
            cv.create_line(left, y, right, y, width=6, fill=ACCENT)
            cv.create_oval(left - 8, y - 8, left + 8, y + 8, fill=ORANGE, outline="")
            cv.create_oval(right - 8, y - 8, right + 8, y + 8, fill=ORANGE, outline="")
            cv.create_oval(p - 8, y - 8, p + 8, y + 8, fill=INDIGO, outline="")
            cv.create_text(left, y - 18, text="A", font=("Segoe UI", 10, "bold"), fill=TEXT)
            cv.create_text(p, y + 18, text="M", font=("Segoe UI", 10, "bold"), fill=TEXT)
            cv.create_text(right, y - 18, text="B", font=("Segoe UI", 10, "bold"), fill=TEXT)
        else:
            left = 50
            right = w - 50
            p = left + (right - left) * 0.6
            cv.create_line(left, y, right, y, width=6, fill=ACCENT)
            cv.create_oval(left - 8, y - 8, left + 8, y + 8, fill=ORANGE, outline="")
            cv.create_oval(right - 8, y - 8, right + 8, y + 8, fill=ORANGE, outline="")
            cv.create_oval(p - 8, y - 8, p + 8, y + 8, fill=INDIGO, outline="")
            cv.create_text(left, y - 18, text="A", font=("Segoe UI", 10, "bold"), fill=TEXT)
            cv.create_text(p, y + 18, text="P", font=("Segoe UI", 10, "bold"), fill=TEXT)
            cv.create_text(right, y - 18, text="B", font=("Segoe UI", 10, "bold"), fill=TEXT)

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
            if len(self.user_input) < 12:
                self.user_input += ch
        self.lbl_display.config(text=self.user_input)

    def next_task(self):
        self.user_input = ""
        self.phase = "answer"
        self.lbl_display.config(text="", bg=WHITE)
        self.display_frame.config(highlightbackground=ACCENT)
        self.lbl_feedback.config(text="")
        self.btn_next.pack_forget()
        self.btn_ok.pack(side="left", padx=20)

        t = random.choice(["conv", "sum", "split"])
        if t == "conv":
            cm = self._pick_not_forbidden(2, 18)
            mm = self._pick_not_forbidden(1, 9)
            total = cm * 10 + mm
            if random.choice([True, False]):
                ans = total
                text = f"Перетвори в міліметри:\n{cm} см {mm} мм = ? мм"
            else:
                ans = cm
                total_mm = cm * 10
                text = f"Перетвори в сантиметри:\n{total_mm} мм = ? см"
            hint_title = "Тип: перетворення одиниць"
            hint_formula = "1 см = 10 мм"
            hint_desc = "Щоб перейти з см у мм — множимо на 10. Щоб з мм у см — ділимо на 10."
            kind = "conv"
        elif t == "sum":
            AB = self._pick_not_forbidden(40, 160)
            AM = self._pick_not_forbidden(10, AB - 10)
            MB = AB - AM
            ans = MB
            text = f"Точка M належить відрізку AB.\nAB = {AB} мм, AM = {AM} мм.\nЗнайди MB (мм)."
            hint_title = "Тип: сума відрізків"
            hint_formula = "AB = AM + MB"
            hint_desc = "Якщо точка M на відрізку AB, то AB складається з AM та MB."
            kind = "sum"
        else:
            m, n = random.choice([(2, 1), (3, 2), (4, 1)])
            part = self._pick_not_forbidden(10, 40)
            AB = (m + n) * part
            AP = m * part
            PB = n * part
            if random.choice([True, False]):
                ans = AP
                ask = "AP"
            else:
                ans = PB
                ask = "PB"
            text = f"Точка P належить відрізку AB.\nAB = {AB} см, AP : PB = {m} : {n}.\nЗнайди {ask} (см)."
            hint_title = "Тип: поділ у відношенні"
            hint_formula = "AB = (m+n) частин"
            hint_desc = "Знайди 1 частину: AB : (m+n). Потім AP = m частин, PB = n частин."
            kind = "split"

        self.task = {"ans": int(ans), "text": text, "kind": kind, "hint_title": hint_title, "hint_formula": hint_formula, "hint_desc": hint_desc}
        self.task_text.config(text=text)
        self._render_task_hint()

    def check_answer(self):
        if self.mode != "trainer":
            return
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
            self.lbl_feedback.config(text="✅ Правильно!", fg=GREEN)
            self.lbl_display.config(bg=GREEN_BG)
            self.after(900, self.next_task)
        else:
            self.lbl_feedback.config(text=f"❌ Помилка! Відповідь: {self.task['ans']}", fg=RED)
            self.lbl_display.config(bg=RED_BG)
            self.btn_ok.pack_forget()
            self.btn_next.pack(side="left", padx=20)

        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")


if __name__ == "__main__":
    app = SegmentsApp()
    app.mainloop()
