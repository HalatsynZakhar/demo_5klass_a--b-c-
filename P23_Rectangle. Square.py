"""
Демонстрація: § 23. Прямокутник. Квадрат.
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
GREEN_BG = "#dcfce7"
RED_BG = "#fee2e2"
INDIGO = "#4f46e5"
SKY = "#0ea5e9"


UNIT_TO_MM = {"мм": 1, "см": 10, "дм": 100, "м": 1000}
UNITS = ["мм", "см", "дм", "м"]


def _to_mm(value, unit):
    return int(value) * UNIT_TO_MM[unit]


def _from_mm(mm, unit):
    return int(mm) // UNIT_TO_MM[unit]

class RectSquareApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Прямокутник. Квадрат (§ 23)")
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

        self._build_ui()
        self.show_rectangle()

    def _draw_right_angle(self, cv, x, y, size, corner):
        # corner: 'bottom_left', 'bottom_right', 'top_right', 'top_left'
        if corner == 'bottom_left':
            cv.create_line(x, y, x + size, y, fill=SKY, width=4)
            cv.create_line(x, y, x, y - size, fill=SKY, width=4)
            cv.create_line(x + size, y - size, x + size, y, fill=SKY, width=4)
            cv.create_line(x + size, y - size, x, y - size, fill=SKY, width=4)
        elif corner == 'bottom_right':
            cv.create_line(x, y, x - size, y, fill=SKY, width=4)
            cv.create_line(x, y, x, y - size, fill=SKY, width=4)
            cv.create_line(x - size, y - size, x - size, y, fill=SKY, width=4)
            cv.create_line(x - size, y - size, x, y - size, fill=SKY, width=4)
        elif corner == 'top_right':
            cv.create_line(x, y, x - size, y, fill=SKY, width=4)
            cv.create_line(x, y, x, y + size, fill=SKY, width=4)
            cv.create_line(x - size, y + size, x - size, y, fill=SKY, width=4)
            cv.create_line(x - size, y + size, x, y + size, fill=SKY, width=4)
        elif corner == 'top_left':
            cv.create_line(x, y, x + size, y, fill=SKY, width=4)
            cv.create_line(x, y, x, y + size, fill=SKY, width=4)
            cv.create_line(x + size, y + size, x + size, y, fill=SKY, width=4)
            cv.create_line(x + size, y + size, x, y + size, fill=SKY, width=4)

    def _build_ui(self):
        hdr = tk.Frame(self, bg=ACCENT, height=60) # Reduced from 80
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(
            hdr,
            text="Прямокутник. Квадрат (§ 23)",
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
        tk.Button(nav, text="1. Прямокутник", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_rectangle).pack(side="left", padx=10)
        tk.Button(nav, text="2. Периметр", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_perimeter).pack(side="left", padx=10)
        tk.Button(nav, text="3. Квадрат", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_square).pack(side="left", padx=10)
        tk.Button(nav, text="4. Тренажер", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_trainer).pack(side="left", padx=10)

        self.main_area = tk.Frame(self, bg=BG)
        self.main_area.pack(fill="both", expand=True)

    def clear_main(self):
        for w in self.main_area.winfo_children():
            w.destroy()

    def _canvas_width(self, cv, fallback):
        w = int(cv.winfo_width())
        if w < 10:
            cv.update_idletasks()
            w = int(cv.winfo_width())
        if w < 10:
            w = int(fallback)
        return w

    def _on_key_press(self, event):
        if self.mode != "trainer":
            return
        if self.answer_mode != "number":
            return
        if event.char.isdigit():
            self._key_press(event.char)

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
            if len(self.user_input) < 8:
                self.user_input += ch
        self.lbl_display.config(text=self.user_input)

    def show_rectangle(self):
        self.clear_main()
        self.mode = "rectangle"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=20) # Reduced from 50/25

        tk.Label(f, text="Прямокутник", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10)) # Reduced from 32
        tk.Label(
            f,
            text=(
                "Прямокутник — це чотирикутник, у якого всі кути прямі.\n\n"
                "Протилежні сторони прямокутника рівні (AB = DC, BC = AD).\n"
                "Суміжні сторони можна називати довжиною і шириною."
            ),
            font=("Segoe UI", 16), # Reduced from 18
            bg=BG,
            fg=MUTED,
            justify="left",
            wraplength=self.SW - 120,
        ).pack(anchor="w")

        cv = tk.Canvas(f, bg=WHITE, height=max(300, int(self.SH * 0.38)), bd=2, relief="ridge") # Reduced height
        cv.pack(fill="x", pady=10, padx=10) # Reduced pady
        self.after(80, lambda: self._draw_rectangle_demo(cv))

    def _draw_rectangle_demo(self, cv):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())
        if h < 50:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 50:
            h = 360

        margin = int(w * 0.25)
        x1 = margin
        y1 = int(h * 0.28)
        x2 = w - margin
        y2 = int(h * 0.78)

        cv.create_rectangle(x1, y1, x2, y2, outline=TEXT, width=6)

        s = 20
        self._draw_right_angle(cv, x1, y2, s, 'bottom_left')
        self._draw_right_angle(cv, x2, y2, s, 'bottom_right')
        self._draw_right_angle(cv, x2, y1, s, 'top_right')
        self._draw_right_angle(cv, x1, y1, s, 'top_left')

        cv.create_text(x1, y2 + 18, text="A", font=("Segoe UI", 14, "bold"), fill=TEXT)
        cv.create_text(x2, y2 + 18, text="B", font=("Segoe UI", 14, "bold"), fill=TEXT)
        cv.create_text(x2, y1 - 18, text="C", font=("Segoe UI", 14, "bold"), fill=TEXT)
        cv.create_text(x1, y1 - 18, text="D", font=("Segoe UI", 14, "bold"), fill=TEXT)

        cv.create_text((x1 + x2) / 2, y2 + 28, text="AB = DC", font=("Segoe UI", 16, "bold"), fill=INDIGO)
        cv.create_text(x2 + 10, (y1 + y2) / 2, text="BC = AD", font=("Segoe UI", 16, "bold"), fill=INDIGO, anchor="w")
        cv.create_rectangle(x1, y1, x2, y2, outline=TEXT, width=2)

    def show_perimeter(self):
        self.clear_main()
        self.mode = "perimeter"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=20)

        tk.Label(f, text="Периметр прямокутника", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10)) # Reduced
        tk.Label(
            f,
            text=(
                "Периметр — це сума довжин усіх сторін фігури.\n"
                "Для прямокутника:\n"
                "P = 2a + 2b  або  P = 2(a + b)\n\n"
                "Якщо відомий периметр P і одна сторона a, то інша сторона:\n"
                "b = P : 2 − a"
            ),
            font=("Segoe UI", 16), # Reduced
            bg=BG,
            fg=MUTED,
            justify="left",
            wraplength=self.SW - 120,
        ).pack(anchor="w")

        cv = tk.Canvas(f, bg=WHITE, height=max(280, int(self.SH * 0.32)), bd=2, relief="ridge") # Reduced height
        cv.pack(fill="x", pady=10, padx=10)
        self.after(80, lambda: self._draw_rectangle_ab(cv, a=8, b=5, unit="см", show_formula=True))

    def show_square(self):
        self.clear_main()
        self.mode = "square"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=30, pady=20)

        tk.Label(f, text="Квадрат", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10)) # Reduced
        tk.Label(
            f,
            text=(
                "Квадрат — це прямокутник, у якого всі сторони рівні.\n\n"
                "Периметр квадрата:\n"
                "P = 4a"
            ),
            font=("Segoe UI", 16), # Reduced
            bg=BG,
            fg=MUTED,
            justify="left",
            wraplength=self.SW - 120,
        ).pack(anchor="w")

        cv = tk.Canvas(f, bg=WHITE, height=max(300, int(self.SH * 0.38)), bd=2, relief="ridge") # Reduced height
        cv.pack(fill="x", pady=10, padx=10)
        self.after(80, lambda: self._draw_square_demo(cv, a=6, unit="см"))

    def _draw_rectangle_ab(self, cv, a, b, unit, show_formula=False, ask_unknown=False):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())
        if h < 50:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 50:
            h = 320

        margin = int(w * 0.25)
        x1 = margin
        y1 = int(h * 0.25)
        x2 = w - margin
        y2 = int(h * 0.78)
        cv.create_rectangle(x1, y1, x2, y2, outline=TEXT, width=6)

        s = 20
        self._draw_right_angle(cv, x1, y2, s, 'bottom_left')
        self._draw_right_angle(cv, x2, y2, s, 'bottom_right')
        self._draw_right_angle(cv, x2, y1, s, 'top_right')
        self._draw_right_angle(cv, x1, y1, s, 'top_left')

        cv.create_text(x1, y2 + 18, text="A", font=("Segoe UI", 14, "bold"), fill=TEXT)
        cv.create_text(x2, y2 + 18, text="B", font=("Segoe UI", 14, "bold"), fill=TEXT)
        cv.create_text(x2, y1 - 18, text="C", font=("Segoe UI", 14, "bold"), fill=TEXT)
        cv.create_text(x1, y1 - 18, text="D", font=("Segoe UI", 14, "bold"), fill=TEXT)

        tx = (x1 + x2) / 2
        ty = y2 + 26
        left = x2 + 12
        midy = (y1 + y2) / 2

        a_txt = "?" if ask_unknown == "a" else f"{a} {unit}"
        b_txt = "?" if ask_unknown == "b" else f"{b} {unit}"
        cv.create_text(tx, ty, text=f"a = {a_txt}", font=("Segoe UI", 16, "bold"), fill=INDIGO) # Reduced
        cv.create_text(left, midy, text=f"b = {b_txt}", font=("Segoe UI", 16, "bold"), fill=INDIGO, anchor="w") # Reduced

        if show_formula:
            cv.create_text(int(w * 0.06), int(h * 0.16), text="P = 2(a + b)", font=("Segoe UI", 18, "bold"), fill=SKY, anchor="w") # Reduced

        cv.create_rectangle(x1, y1, x2, y2, outline=TEXT, width=2)

    def _draw_square_demo(self, cv, a, unit, show_formula=False, ask_unknown=False):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())
        if h < 50:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 50:
            h = 360

        size = min(w, h) * 0.55
        x1 = (w - size) / 2
        y1 = (h - size) / 2 + 10
        x2 = x1 + size
        y2 = y1 + size
        cv.create_rectangle(x1, y1, x2, y2, outline=TEXT, width=6)

        s = 20
        self._draw_right_angle(cv, x1, y2, s, 'bottom_left')
        self._draw_right_angle(cv, x2, y2, s, 'bottom_right')
        self._draw_right_angle(cv, x2, y1, s, 'top_right')
        self._draw_right_angle(cv, x1, y1, s, 'top_left')

        cv.create_text(x1, y2 + 18, text="A", font=("Segoe UI", 14, "bold"), fill=TEXT)
        cv.create_text(x2, y2 + 18, text="B", font=("Segoe UI", 14, "bold"), fill=TEXT)
        cv.create_text(x2, y1 - 18, text="C", font=("Segoe UI", 14, "bold"), fill=TEXT)
        cv.create_text(x1, y1 - 18, text="D", font=("Segoe UI", 14, "bold"), fill=TEXT)

        txt = "?" if ask_unknown else f"{a} {unit}"
        cv.create_text((x1 + x2) / 2, y2 + 28, text=f"a = {txt}", font=("Segoe UI", 18, "bold"), fill=INDIGO) # Reduced
        if show_formula:
            cv.create_text(int(w * 0.06), int(h * 0.14), text="P = 4a", font=("Segoe UI", 18, "bold"), fill=SKY, anchor="w") # Reduced

        cv.create_rectangle(x1, y1, x2, y2, outline=TEXT, width=2)

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
        self.task_text = tk.Label(self.task_box, text="", font=("Segoe UI", 16, "bold"), bg=WHITE, fg=TEXT, justify="center", wraplength=LW - 100) # Reduced from 18
        self.task_text.pack(anchor="center", pady=(5,0))

        self.task_canvas = tk.Canvas(left, bg=WHITE, height=220, bd=2, relief="ridge") # Reduced from 300
        self.task_canvas.pack(pady=10, padx=20, fill="x")

        self.display_frame = tk.Frame(left, bg=WHITE, highlightbackground=ACCENT, highlightthickness=2)
        self.display_frame.pack(pady=5, ipadx=16, ipady=4)
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
                "• Прямокутник: P = 2(a + b)\n"
                "• Якщо відомі P і a: b = P : 2 − a\n"
                "• Квадрат: P = 4a\n"
                "• Якщо відомий P квадрата: a = P : 4"
            ),
            font=("Segoe UI", 11), # Reduced from 12
            bg="#eff6ff",
            justify="left",
        ).pack(anchor="w")

        self.after(80, self.next_task)

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

        t = random.choice(["rect_p", "rect_b", "sq_p", "sq_a"])
        unit = random.choice(UNITS)
        step = UNIT_TO_MM[unit]

        if t == "rect_p":
            a = random.randint(2, 18)
            b = random.randint(2, 18)
            self.task = {"type": "rect_p", "ans": 2 * (a + b), "unit": unit, "a": a, "b": b}
            self.task_text.config(text=f"Знайди периметр прямокутника. a = {a} {unit}, b = {b} {unit}.")
            self._draw_rectangle_ab(self.task_canvas, a, b, unit, show_formula=True)
        elif t == "rect_b":
            a = random.randint(3, 18)
            b = random.randint(2, 18)
            p = 2 * (a + b)
            self.task = {"type": "rect_b", "ans": b, "unit": unit, "a": a, "p": p}
            self.task_text.config(text=f"Периметр P = {p} {unit}. Одна сторона a = {a} {unit}. Знайди іншу сторону b.")
            self._draw_rectangle_ab(self.task_canvas, a, b, unit, show_formula=False, ask_unknown="b")
        elif t == "sq_p":
            a = random.randint(2, 30)
            self.task = {"type": "sq_p", "ans": 4 * a, "unit": unit, "a": a}
            self.task_text.config(text=f"Знайди периметр квадрата. a = {a} {unit}.")
            self._draw_square_demo(self.task_canvas, a, unit, show_formula=True)
        else:
            a = random.randint(2, 30)
            p = 4 * a
            self.task = {"type": "sq_a", "ans": a, "unit": unit, "p": p}
            self.task_text.config(text=f"Периметр квадрата P = {p} {unit}. Знайди сторону a.")
            self._draw_square_demo(self.task_canvas, a, unit, show_formula=False, ask_unknown=True)

        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")

    def check_answer(self):
        if self.mode != "trainer":
            return
        if self.phase != "answer":
            return
        if not self.task:
            return
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
            self.after(850, self.next_task)
        else:
            self.lbl_feedback.config(text=f"❌ Ні. Відповідь: {self.task['ans']}", fg=RED)
            self.lbl_display.config(bg=RED_BG)
            self.btn_ok.pack_forget()
            self.btn_next.pack(side="left", padx=20)
        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")


if __name__ == "__main__":
    app = RectSquareApp()
    app.mainloop()
