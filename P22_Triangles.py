"""
Демонстрація: § 22. Трикутник і його периметр. Види трикутників.
Для 5 класу.
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
BLUE = "#1971c2"
WHITE = "#ffffff"
BTN_NUM = "#e2e8f0"
INDIGO = "#4f46e5"
SKY = "#0ea5e9"
GREEN_BG = "#dcfce7"
RED_BG = "#fee2e2"


def _triangle_exists(a, b, c):
    a, b, c = sorted([a, b, c])
    return a + b > c


def _classify_sides(a, b, c):
    if a == b == c:
        return "Рівносторонній"
    if a == b or b == c or a == c:
        return "Рівнобедрений"
    return "Різносторонній"


def _classify_angles(A, B, C):
    mx = max(A, B, C)
    if mx == 90:
        return "Прямокутний"
    if mx > 90:
        return "Тупокутний"
    return "Гострокутний"


class TrianglesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Трикутники (§ 22)")
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

        self._build_ui()
        self.show_triangle()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=ACCENT, height=80)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="Трикутник і його периметр. Види трикутників (§ 22)", bg=ACCENT, fg=WHITE, font=("Segoe UI", 22, "bold")).pack(side="left", padx=30)
        tk.Button(hdr, text="❌ Вихід", font=("Arial", 16, "bold"), bg=RED, fg=WHITE, bd=0, command=self.destroy).pack(side="right", padx=20)

        nav = tk.Frame(self, bg=WHITE, height=60)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        btn_font = ("Segoe UI", 12, "bold")
        tk.Button(nav, text="1. Трикутник", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_triangle).pack(side="left", padx=10)
        tk.Button(nav, text="2. Периметр", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_perimeter).pack(side="left", padx=10)
        tk.Button(nav, text="3. Види за сторонами", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_types_sides).pack(side="left", padx=10)
        tk.Button(nav, text="4. Види за кутами", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_types_angles).pack(side="left", padx=10)
        tk.Button(nav, text="5. Тренажер", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_trainer).pack(side="left", padx=10)

        self.main_area = tk.Frame(self, bg=BG)
        self.main_area.pack(fill="both", expand=True)

    def clear_main(self):
        for w in self.main_area.winfo_children():
            w.destroy()

    def _canvas_width(self, cv, fallback):
        w = int(cv.winfo_width())
        if w < 300:
            cv.update_idletasks()
            w = int(cv.winfo_width())
        if w < 300:
            w = int(fallback)
        return w

    def _label_on_segment(self, cv, p1, p2, text, offset=18, fill=INDIGO):
        x1, y1 = p1
        x2, y2 = p2
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        if ln < 1e-6:
            return
        nx, ny = -dy / ln, dx / ln
        tx, ty = mx + nx * offset, my + ny * offset
        tid = cv.create_text(tx, ty, text=str(text), font=("Segoe UI", 14, "bold"), fill=fill)
        bb = cv.bbox(tid)
        if bb:
            rid = cv.create_rectangle(bb[0] - 6, bb[1] - 2, bb[2] + 6, bb[3] + 2, fill=WHITE, outline="")
            cv.tag_lower(rid, tid)

    def _triangle_points_from_angles(self, A_deg, B_deg, C_deg, w, h):
        A = (0.0, 0.0)
        B = (1.0, 0.0)
        a = math.radians(A_deg)
        b = math.radians(B_deg)
        d1 = (math.cos(a), math.sin(a))
        d2 = (math.cos(math.pi - b), math.sin(math.pi - b))
        cross = d1[0] * d2[1] - d1[1] * d2[0]
        if abs(cross) < 1e-6:
            return None
        t = d2[1] / cross
        if t <= 0:
            return None
        C = (A[0] + t * d1[0], A[1] + t * d1[1])

        xs = [A[0], B[0], C[0]]
        ys = [A[1], B[1], C[1]]
        minx, maxx = min(xs), max(xs)
        miny, maxy = min(ys), max(ys)
        if maxx - minx < 1e-6 or maxy - miny < 1e-6:
            return None

        margin = 60
        sx = (w - 2 * margin) / (maxx - minx)
        sy = (h - 2 * margin) / (maxy - miny)
        scale = max(1e-6, min(sx, sy))

        def m(p):
            x, y = p
            xx = margin + (x - minx) * scale
            yy = margin + (maxy - y) * scale
            return (xx, yy)

        return m(A), m(B), m(C)

    def _triangle_points_from_angles_box(self, A_deg, B_deg, C_deg, x0, y0, w, h, margin):
        A = (0.0, 0.0)
        B = (1.0, 0.0)
        a = math.radians(A_deg)
        b = math.radians(B_deg)
        d1 = (math.cos(a), math.sin(a))
        d2 = (math.cos(math.pi - b), math.sin(math.pi - b))
        cross = d1[0] * d2[1] - d1[1] * d2[0]
        if abs(cross) < 1e-6:
            return None
        t = d2[1] / cross
        if t <= 0:
            return None
        C = (A[0] + t * d1[0], A[1] + t * d1[1])

        xs = [A[0], B[0], C[0]]
        ys = [A[1], B[1], C[1]]
        minx, maxx = min(xs), max(xs)
        miny, maxy = min(ys), max(ys)
        if maxx - minx < 1e-6 or maxy - miny < 1e-6:
            return None

        sx = (w - 2 * margin) / (maxx - minx)
        sy = (h - 2 * margin) / (maxy - miny)
        scale = max(1e-6, min(sx, sy))

        def m(p):
            x, y = p
            xx = x0 + margin + (x - minx) * scale
            yy = y0 + margin + (maxy - y) * scale
            return (xx, yy)

        return m(A), m(B), m(C)

    def _triangle_points_from_sides_box(self, AB, BC, CA, x0, y0, w, h, margin):
        AB = float(AB)
        BC = float(BC)
        CA = float(CA)
        if AB <= 0 or BC <= 0 or CA <= 0:
            return None
        if CA + AB <= BC or AB + BC <= CA or CA + BC <= AB:
            return None

        A = (0.0, 0.0)
        B = (AB, 0.0)
        x = (CA * CA + AB * AB - BC * BC) / (2 * AB)
        y2 = CA * CA - x * x
        if y2 <= 1e-9:
            return None
        y = math.sqrt(y2)
        C = (x, y)

        xs = [A[0], B[0], C[0]]
        ys = [A[1], B[1], C[1]]
        minx, maxx = min(xs), max(xs)
        miny, maxy = min(ys), max(ys)
        if maxx - minx < 1e-6 or maxy - miny < 1e-6:
            return None

        sx = (w - 2 * margin) / (maxx - minx)
        sy = (h - 2 * margin) / (maxy - miny)
        scale = max(1e-6, min(sx, sy))

        def m(p):
            x, y = p
            xx = x0 + margin + (x - minx) * scale
            yy = y0 + margin + (maxy - y) * scale
            return (xx, yy)

        A2, B2, C2 = m(A), m(B), m(C)
        xs2 = [A2[0], B2[0], C2[0]]
        ys2 = [A2[1], B2[1], C2[1]]
        cx = x0 + w / 2
        cy = y0 + h / 2
        ccx = (min(xs2) + max(xs2)) / 2
        ccy = (min(ys2) + max(ys2)) / 2
        dx = cx - ccx
        dy = cy - ccy
        return (A2[0] + dx, A2[1] + dy), (B2[0] + dx, B2[1] + dy), (C2[0] + dx, C2[1] + dy)

    def _draw_right_mark(self, cv, P, Q, R, color=BLUE):
        ux, uy = Q[0] - P[0], Q[1] - P[1]
        vx, vy = R[0] - P[0], R[1] - P[1]
        ulen = math.hypot(ux, uy)
        vlen = math.hypot(vx, vy)
        if ulen < 1e-6 or vlen < 1e-6:
            return
        ux, uy = ux / ulen, uy / ulen
        vx, vy = vx / vlen, vy / vlen
        s = 16
        p1 = (P[0] + ux * s, P[1] + uy * s)
        p3 = (P[0] + vx * s, P[1] + vy * s)
        p2 = (p1[0] + vx * s, p1[1] + vy * s)
        cv.create_line(p1[0], p1[1], p2[0], p2[1], width=3, fill=color)
        cv.create_line(p2[0], p2[1], p3[0], p3[1], width=3, fill=color)

    def _on_key_press(self, event):
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

    def show_triangle(self):
        self.clear_main()
        self.mode = "triangle"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)

        tk.Label(f, text="Трикутник", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        tk.Label(
            f,
            text=(
                "Якщо три точки, які не лежать на одній прямій, сполучити відрізками — отримаємо трикутник.\n\n"
                "• вершини: A, B, C\n"
                "• сторони: AB, BC, AC\n"
                "• кути трикутника: ∠ABC, ∠BCA, ∠CAB\n\n"
                "Трикутник позначають знаком △, наприклад △ABC."
            ),
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            justify="left",
            wraplength=self.SW - 160,
        ).pack(anchor="w")

        cv = tk.Canvas(f, bg=WHITE, height=max(360, int(self.SH * 0.42)), bd=2, relief="ridge")
        cv.pack(fill="x", pady=15, padx=10)
        self.after(80, lambda: self._draw_basic_triangle(cv))

    def _draw_basic_triangle(self, cv):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())
        if h < 260:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 260:
            h = 360

        margin = 80
        A = (int(w * 0.30), int(h * 0.72))
        B = (int(w * 0.70), int(h * 0.72))
        C = (int(w * 0.52), int(h * 0.25))

        cv.create_polygon(A[0], A[1], B[0], B[1], C[0], C[1], outline=TEXT, fill="", width=5)
        for name, (x, y) in (("A", A), ("B", B), ("C", C)):
            cv.create_oval(x - 8, y - 8, x + 8, y + 8, fill=ORANGE, outline="")
            cv.create_text(x, y - 22, text=name, font=("Segoe UI", 16, "bold"), fill=TEXT)

        cv.create_text(int(w * 0.06), int(h * 0.12), text="△ABC", font=("Segoe UI", 24, "bold"), fill=INDIGO, anchor="w")
        cv.create_text(int(w * 0.06), int(h * 0.22), text="Вершини — точки A, B, C", font=("Segoe UI", 14, "bold"), fill=MUTED, anchor="w")
        cv.create_text(int(w * 0.06), int(h * 0.30), text="Сторони — відрізки AB, BC, AC", font=("Segoe UI", 14, "bold"), fill=MUTED, anchor="w")

    def show_perimeter(self):
        self.clear_main()
        self.mode = "perimeter"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)

        tk.Label(f, text="Периметр трикутника", font=("Segoe UI", 30, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        tk.Label(
            f,
            text=(
                "Периметр трикутника — це сума довжин усіх його сторін.\n"
                "Формула: P = AB + BC + AC"
            ),
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            justify="left",
        ).pack(anchor="w")

        cards = tk.Frame(f, bg=BG)
        cards.pack(fill="both", expand=True, pady=10)

        c1 = tk.Frame(cards, bg=WHITE, bd=2, relief="ridge", padx=18, pady=18)
        c1.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        tk.Label(c1, text="Приклад (арифметично)", font=("Segoe UI", 16, "bold"), bg=WHITE, fg=TEXT).pack(anchor="w")
        tk.Label(
            c1,
            text="Нехай AB = 6 см, BC = 8 см, AC = 5 см.\nТоді P = 6 + 8 + 5 = 19 см.",
            font=("Segoe UI", 14),
            bg=WHITE,
            fg=MUTED,
            justify="left",
        ).pack(anchor="w", pady=(10, 0))

        c2 = tk.Frame(cards, bg=WHITE, bd=2, relief="ridge", padx=18, pady=18)
        c2.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        tk.Label(c2, text="Як знайти невідому сторону", font=("Segoe UI", 16, "bold"), bg=WHITE, fg=TEXT).pack(anchor="w")
        tk.Label(
            c2,
            text="Якщо P відомий, а дві сторони відомі:\nAC = P − AB − BC",
            font=("Segoe UI", 14),
            bg=WHITE,
            fg=MUTED,
            justify="left",
        ).pack(anchor="w", pady=(10, 0))

        cv = tk.Canvas(f, bg=WHITE, height=max(300, int(self.SH * 0.32)), bd=2, relief="ridge")
        cv.pack(fill="x", pady=10, padx=10)
        self.after(80, lambda: self._draw_perimeter_triangle(cv))

    def _draw_perimeter_triangle(self, cv):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())
        if h < 220:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 220:
            h = 300

        A = (int(w * 0.28), int(h * 0.78))
        B = (int(w * 0.72), int(h * 0.78))
        C = (int(w * 0.55), int(h * 0.22))
        cv.create_polygon(A[0], A[1], B[0], B[1], C[0], C[1], outline=TEXT, fill="", width=5)
        for name, (x, y) in (("A", A), ("B", B), ("C", C)):
            cv.create_oval(x - 8, y - 8, x + 8, y + 8, fill=ORANGE, outline="")
            cv.create_text(x, y - 22, text=name, font=("Segoe UI", 14, "bold"), fill=TEXT)
        cv.create_text(int(w * 0.50), int(h * 0.90), text="P = AB + BC + AC", font=("Segoe UI", 18, "bold"), fill=INDIGO, anchor="center")

    def show_types_sides(self):
        self.clear_main()
        self.mode = "types_sides"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)

        tk.Label(f, text="Види трикутників за сторонами", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        tk.Label(
            f,
            text=(
                "• рівносторонній — усі сторони рівні\n"
                "• рівнобедрений — дві сторони рівні\n"
                "• різносторонній — усі сторони різні"
            ),
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            justify="left",
        ).pack(anchor="w")

        cv = tk.Canvas(f, bg=WHITE, height=max(420, int(self.SH * 0.50)), bd=2, relief="ridge")
        cv.pack(fill="x", pady=15, padx=10)
        self.after(80, lambda: self._draw_side_types(cv))

    def _draw_side_types(self, cv):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())
        if h < 320:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 320:
            h = 420

        cells = [
            ("Рівносторонній", [9, 9, 9], INDIGO),
            ("Рівнобедрений", [5, 12, 12], SKY),
            ("Різносторонній", [17, 5, 13], ORANGE),
        ]

        cw = w / 3
        margin = 30
        for i, (name, sides, col) in enumerate(cells):
            x0 = int(i * cw)
            cx = int(x0 + cw * 0.5)
            cv.create_text(cx, int(h * 0.12), text=name, font=("Segoe UI", 16, "bold"), fill=TEXT)
            cv.create_text(cx, int(h * 0.20), text=f"AB={sides[0]}, BC={sides[1]}, CA={sides[2]}", font=("Segoe UI", 12, "bold"), fill=MUTED)

            box_w = int(cw)
            box_h = int(h * 0.66)
            box_x0 = x0
            box_y0 = int(h * 0.26)
            pts = self._triangle_points_from_sides_box(sides[0], sides[1], sides[2], box_x0, box_y0, box_w, box_h, margin=34)
            if pts is None:
                cy = int(h * 0.62)
                r = min(cw, h) * 0.30
                A = (cx - int(r * 0.95), cy + int(r * 0.60))
                B = (cx + int(r * 0.95), cy + int(r * 0.60))
                C = (cx, cy - int(r * 0.95))
            else:
                A, B, C = pts

            cv.create_polygon(A[0], A[1], B[0], B[1], C[0], C[1], outline=col, fill="#f8fafc", width=5)
            for p in (A, B, C):
                cv.create_oval(p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6, fill=WHITE, outline=col, width=2)

            self._label_on_segment(cv, A, B, sides[0], offset=22, fill=INDIGO)
            self._label_on_segment(cv, B, C, sides[1], offset=22, fill=INDIGO)
            self._label_on_segment(cv, C, A, sides[2], offset=22, fill=INDIGO)
            if i < 2:
                cv.create_line(int((i + 1) * cw), margin, int((i + 1) * cw), h - margin, fill=BORDER, width=2)

    def show_types_angles(self):
        self.clear_main()
        self.mode = "types_angles"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)

        tk.Label(f, text="Види трикутників за кутами", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        card = tk.Frame(f, bg=WHITE, bd=2, relief="ridge", padx=18, pady=14)
        card.pack(fill="x", padx=10, pady=(0, 12))
        tk.Label(card, text="Головні правила", font=("Segoe UI", 16, "bold"), bg=WHITE, fg=TEXT).pack(anchor="w")
        tk.Label(
            card,
            text=(
                "1) Сума кутів будь‑якого трикутника дорівнює 180°.\n"
                "2) Гострокутний: усі кути < 90°.\n"
                "3) Прямокутний: один кут = 90° (і більше прямого бути не може).\n"
                "4) Тупокутний: один кут > 90° (і більше тупого бути не може)."
            ),
            font=("Segoe UI", 14),
            bg=WHITE,
            fg=MUTED,
            justify="left",
        ).pack(anchor="w", pady=(8, 0))

        cv = tk.Canvas(f, bg=WHITE, height=max(420, int(self.SH * 0.52)), bd=2, relief="ridge")
        cv.pack(fill="both", expand=True, pady=15, padx=10)
        self.after(80, lambda: self._draw_angle_types(cv))

    def _draw_angle_types(self, cv):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())
        if h < 320:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 320:
            h = 420

        items = [
            ("Гострокутний", (10, 85, 85), GREEN),
            ("Прямокутний", (90, 30, 60), BLUE),
            ("Тупокутний", (130, 30, 20), ORANGE),
        ]

        cw = w / 3
        margin = 30
        for i, (name, angs, col) in enumerate(items):
            x0 = int(i * cw)
            cx = int(x0 + cw * 0.5)
            cv.create_text(cx, int(h * 0.12), text=name, font=("Segoe UI", 16, "bold"), fill=TEXT)
            cv.create_text(cx, int(h * 0.20), text=f"Кути: {angs[0]}°, {angs[1]}°, {angs[2]}°", font=("Segoe UI", 12, "bold"), fill=MUTED)

            box_w = int(cw)
            box_h = int(h * 0.60)
            box_x0 = x0
            box_y0 = int(h * 0.26)
            pts = self._triangle_points_from_angles_box(angs[0], angs[1], angs[2], box_x0, box_y0, box_w, box_h, margin=28)
            if pts is None:
                cy = int(h * 0.62)
                r = min(cw, h) * 0.30
                A = (cx - int(r * 0.95), cy + int(r * 0.60))
                B = (cx + int(r * 0.95), cy + int(r * 0.60))
                C = (cx, cy - int(r * 0.95))
            else:
                A, B, C = pts

            cv.create_polygon(A[0], A[1], B[0], B[1], C[0], C[1], outline=col, fill="#f8fafc", width=5)
            for px, py in (A, B, C):
                cv.create_oval(px - 6, py - 6, px + 6, py + 6, fill=WHITE, outline=col, width=2)

            if angs[0] == 90:
                self._draw_right_mark(cv, A, B, C, color=BLUE)
            if angs[1] == 90:
                self._draw_right_mark(cv, B, A, C, color=BLUE)
            if angs[2] == 90:
                self._draw_right_mark(cv, C, A, B, color=BLUE)
            if i < 2:
                cv.create_line(int((i + 1) * cw), margin, int((i + 1) * cw), h - margin, fill=BORDER, width=2)
        cv.create_text(int(w * 0.06), int(h * 0.90), text="Сума кутів: A + B + C = 180°", font=("Segoe UI", 16, "bold"), fill=INDIGO, anchor="w")

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

        self.task_canvas = tk.Canvas(left, bg=WHITE, height=300, bd=2, relief="ridge")
        self.task_canvas.pack(pady=10, padx=20, fill="x")

        self.choice_frame = tk.Frame(left, bg=BG)
        self.choice_msg = tk.Label(self.choice_frame, text="", font=("Segoe UI", 18, "bold"), bg=BG, fg=MUTED)
        self.choice_msg.pack()
        self.choice_btns = tk.Frame(self.choice_frame, bg=BG)
        self.choice_btns.pack(pady=10)

        self.display_frame = tk.Frame(left, bg=WHITE, highlightbackground=ACCENT, highlightthickness=2)
        self.display_frame.pack(pady=10, ipadx=24, ipady=10)
        self.lbl_display = tk.Label(self.display_frame, text="", bg=WHITE, fg=TEXT, font=("Segoe UI", 48, "bold"), width=12, anchor="e")
        self.lbl_display.pack()

        self.lbl_feedback = tk.Label(left, text="", font=("Segoe UI", 18, "bold"), bg=BG)
        self.lbl_feedback.pack(pady=10)

        self.kbd = tk.Frame(left, bg=BG)
        self.kbd.pack(pady=10)
        rows = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["C", "0", "⌫"]]
        for row in rows:
            r = tk.Frame(self.kbd, bg=BG)
            r.pack(pady=2)
            for ch in row:
                tk.Button(
                    r,
                    text=ch,
                    bg=RED_BG if ch in ("⌫", "C") else BTN_NUM,
                    font=("Segoe UI", 20, "bold"),
                    width=6,
                    height=1,
                    relief="flat",
                    command=lambda c=ch: self._key_press(c),
                ).pack(side="left", padx=5)

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
        tk.Label(rpad, text="Підказки", font=("Segoe UI", 18, "bold"), bg=PANEL, fg=MUTED).pack(anchor="w")

        hint_box = tk.Frame(rpad, bg="#eff6ff", highlightbackground="#bfdbfe", highlightthickness=1, padx=15, pady=15)
        hint_box.pack(fill="x", pady=10)
        tk.Label(
            hint_box,
            text=(
                "• P = сума сторін\n"
                "• Рівносторонній: 3 рівні сторони\n"
                "• Рівнобедрений: 2 рівні сторони\n"
                "• Сума кутів трикутника = 180°\n"
                "• Трикутник існує, якщо сума двох сторін більша за третю"
            ),
            font=("Segoe UI", 12),
            bg="#eff6ff",
            justify="left",
        ).pack(anchor="w")

        self.after(80, self.next_task)

    def _trainer_set_mode(self, mode):
        self.answer_mode = mode
        self.choice_value = None
        for w in self.choice_btns.winfo_children():
            w.destroy()
        self.choice_msg.config(text="")

        if mode == "number":
            self.choice_frame.pack_forget()
            self.display_frame.pack(pady=10, ipadx=24, ipady=10)
            self.kbd.pack(pady=10)
            self.btn_ok.config(state="normal")
        else:
            self.kbd.pack_forget()
            self.display_frame.pack_forget()
            self.choice_frame.pack(pady=10)
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

        t = random.choice(["perimeter", "missing_side", "sum_angles", "type_sides", "type_angles", "exists"])

        if t == "perimeter":
            a, b, c = self._pick_triangle_sides()
            self.task = {"type": "perimeter", "ans": a + b + c, "sides": (a, b, c)}
            self._trainer_set_mode("number")
            self.task_text.config(text=f"Знайди периметр, якщо сторони: {a} см, {b} см, {c} см.")
            self._draw_triangle_sides(self.task_canvas, a, b, c)
        elif t == "missing_side":
            a, b, c = self._pick_triangle_sides()
            p = a + b + c
            known = random.sample([a, b, c], 2)
            ans = p - known[0] - known[1]
            self.task = {"type": "missing_side", "ans": ans, "p": p, "known": tuple(known)}
            self._trainer_set_mode("number")
            self.task_text.config(text=f"Периметр P = {p} см. Дві сторони: {known[0]} см і {known[1]} см. Знайди третю сторону.")
            self._draw_triangle_missing(self.task_canvas, p, known[0], known[1])
        elif t == "sum_angles":
            A = random.randint(25, 95)
            B = random.randint(25, 95)
            while A + B >= 179:
                A = random.randint(25, 95)
                B = random.randint(25, 95)
            C = 180 - A - B
            self.task = {"type": "sum_angles", "ans": C, "A": A, "B": B}
            self._trainer_set_mode("number")
            self.task_text.config(text=f"У трикутнику ∠A = {A}°, ∠B = {B}°. Знайди ∠C.")
            self._draw_triangle_angles(self.task_canvas, A, B, None)
        elif t == "type_sides":
            a, b, c = self._pick_triangle_sides(allow_equilateral=True)
            typ = _classify_sides(a, b, c)
            self.task = {"type": "type_sides", "ans": typ, "sides": (a, b, c)}
            self._trainer_set_mode("choice")
            self.task_text.config(text=f"Який це трикутник за сторонами? Сторони: {a}, {b}, {c}.")
            self._draw_triangle_sides(self.task_canvas, a, b, c)
            self.choice_msg.config(text="Обери відповідь:")
            for opt in ["Рівносторонній", "Рівнобедрений", "Різносторонній"]:
                tk.Button(self.choice_btns, text=opt, font=("Segoe UI", 18, "bold"), bg=BTN_NUM, bd=0, padx=18, pady=10, command=lambda o=opt: self._pick_choice(o)).pack(
                    side="left", padx=10
                )
        elif t == "type_angles":
            kind = random.choice(["acute", "right", "obtuse"])
            if kind == "right":
                A = 90
                B = random.choice([15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70])
                C = 90 - B
            elif kind == "obtuse":
                A = random.choice([100, 110, 120, 130, 140])
                B = random.randint(15, 60)
                C = 180 - A - B
                if C <= 0:
                    B = 20
                    C = 180 - A - B
            else:
                A = random.randint(40, 80)
                B = random.randint(40, 80)
                while A + B >= 140:
                    A = random.randint(35, 70)
                    B = random.randint(35, 70)
                C = 180 - A - B
                if max(A, B, C) >= 90:
                    A, B, C = 50, 60, 70
            typ = _classify_angles(A, B, C)
            self.task = {"type": "type_angles", "ans": typ, "angles": (A, B, C)}
            self._trainer_set_mode("choice")
            self.task_text.config(text=f"Який це трикутник за кутами? Кути: {A}°, {B}°, {C}°.")
            self._draw_triangle_angles(self.task_canvas, A, B, C)
            self.choice_msg.config(text="Обери відповідь:")
            for opt in ["Гострокутний", "Прямокутний", "Тупокутний"]:
                tk.Button(self.choice_btns, text=opt, font=("Segoe UI", 18, "bold"), bg=BTN_NUM, bd=0, padx=18, pady=10, command=lambda o=opt: self._pick_choice(o)).pack(
                    side="left", padx=10
                )
        else:
            a = random.randint(2, 18)
            b = random.randint(2, 18)
            c = random.randint(2, 18)
            ans = "Так" if _triangle_exists(a, b, c) else "Ні"
            self.task = {"type": "exists", "ans": ans, "sides": (a, b, c)}
            self._trainer_set_mode("choice")
            self.task_text.config(text=f"Чи існує трикутник зі сторонами {a}, {b}, {c}?")
            self._draw_triangle_sides(self.task_canvas, a, b, c)
            self.choice_msg.config(text="Обери відповідь:")
            for opt in ["Так", "Ні"]:
                tk.Button(self.choice_btns, text=opt, font=("Segoe UI", 18, "bold"), bg=BTN_NUM, bd=0, padx=26, pady=10, command=lambda o=opt: self._pick_choice(o)).pack(
                    side="left", padx=12
                )

        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")

    def _pick_choice(self, value):
        if self.mode != "trainer":
            return
        if self.phase != "answer":
            return
        if self.answer_mode != "choice":
            return
        self.choice_value = value
        self._finish_answer(got=value)

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

    def _finish_answer(self, got):
        if self.mode != "trainer":
            return
        if self.phase != "answer":
            return
        if not self.task:
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

    def _pick_triangle_sides(self, allow_equilateral=False):
        pool = []
        for a in range(3, 19):
            for b in range(3, 19):
                for c in range(3, 19):
                    if not _triangle_exists(a, b, c):
                        continue
                    if not allow_equilateral and a == b == c:
                        continue
                    pool.append((a, b, c))
        return random.choice(pool)

    def _draw_triangle_sides(self, cv, a, b, c):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW * 0.62 - 60)
        h = int(cv.winfo_height())
        if h < 240:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 240:
            h = 300

        A = (int(w * 0.22), int(h * 0.78))
        B = (int(w * 0.78), int(h * 0.78))
        C = (int(w * 0.55), int(h * 0.25))
        cv.create_polygon(A[0], A[1], B[0], B[1], C[0], C[1], outline=TEXT, fill="", width=5)
        for name, (x, y) in (("A", A), ("B", B), ("C", C)):
            cv.create_oval(x - 7, y - 7, x + 7, y + 7, fill=ORANGE, outline="")
            cv.create_text(x, y - 20, text=name, font=("Segoe UI", 12, "bold"), fill=TEXT)

        self._label_on_segment(cv, A, B, a, offset=22)
        self._label_on_segment(cv, B, C, b, offset=22)
        self._label_on_segment(cv, C, A, c, offset=22)

    def _draw_triangle_missing(self, cv, p, x, y):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW * 0.62 - 60)
        h = int(cv.winfo_height())
        if h < 240:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 240:
            h = 300

        A = (int(w * 0.22), int(h * 0.78))
        B = (int(w * 0.78), int(h * 0.78))
        C = (int(w * 0.55), int(h * 0.25))
        cv.create_polygon(A[0], A[1], B[0], B[1], C[0], C[1], outline=TEXT, fill="", width=5)
        cv.create_text(int(w * 0.06), int(h * 0.12), text=f"P = {p}", font=("Segoe UI", 16, "bold"), fill=INDIGO, anchor="w")
        self._label_on_segment(cv, A, B, x, offset=22)
        self._label_on_segment(cv, B, C, y, offset=22)
        self._label_on_segment(cv, C, A, "?", offset=22, fill=ORANGE)

    def _draw_triangle_angles(self, cv, Aang, Bang, Cang):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW * 0.62 - 60)
        h = int(cv.winfo_height())
        if h < 240:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 240:
            h = 300
        if Cang is None:
            Cfull = 180 - Aang - Bang
        else:
            Cfull = Cang

        pts = self._triangle_points_from_angles(Aang, Bang, Cfull, w, h)
        if pts is None:
            A = (int(w * 0.25), int(h * 0.78))
            B = (int(w * 0.78), int(h * 0.78))
            C = (int(w * 0.55), int(h * 0.22))
        else:
            A, B, C = pts

        cv.create_polygon(A[0], A[1], B[0], B[1], C[0], C[1], outline=TEXT, fill="", width=5)
        for name, (x, y) in (("A", A), ("B", B), ("C", C)):
            cv.create_oval(x - 7, y - 7, x + 7, y + 7, fill=ORANGE, outline="")
            cv.create_text(x, y - 20, text=name, font=("Segoe UI", 12, "bold"), fill=TEXT)

        gx = (A[0] + B[0] + C[0]) / 3
        gy = (A[1] + B[1] + C[1]) / 3

        def angle_label(P, value, unknown=False):
            vx = P[0] - gx
            vy = P[1] - gy
            ln = math.hypot(vx, vy)
            if ln < 1e-6:
                lx, ly = P[0] + 30, P[1] - 30
            else:
                lx = P[0] + vx / ln * 30
                ly = P[1] + vy / ln * 30
            txt = "?" if unknown else f"{value}°"
            tid = cv.create_text(lx, ly, text=txt, font=("Segoe UI", 14, "bold"), fill=ORANGE if unknown else INDIGO)
            bb = cv.bbox(tid)
            if bb:
                rid = cv.create_rectangle(bb[0] - 6, bb[1] - 2, bb[2] + 6, bb[3] + 2, fill=WHITE, outline="")
                cv.tag_lower(rid, tid)

        angle_label(A, Aang)
        angle_label(B, Bang)
        angle_label(C, Cfull, unknown=(Cang is None))

        def right_mark(P, Q, R):
            ux, uy = Q[0] - P[0], Q[1] - P[1]
            vx, vy = R[0] - P[0], R[1] - P[1]
            ulen = math.hypot(ux, uy)
            vlen = math.hypot(vx, vy)
            if ulen < 1e-6 or vlen < 1e-6:
                return
            ux, uy = ux / ulen, uy / ulen
            vx, vy = vx / vlen, vy / vlen
            s = 18
            p1 = (P[0] + ux * s, P[1] + uy * s)
            p3 = (P[0] + vx * s, P[1] + vy * s)
            p2 = (p1[0] + vx * s, p1[1] + vy * s)
            cv.create_line(p1[0], p1[1], p2[0], p2[1], width=3, fill=BLUE)
            cv.create_line(p2[0], p2[1], p3[0], p3[1], width=3, fill=BLUE)

        if Aang == 90:
            right_mark(A, B, C)
        if Bang == 90:
            right_mark(B, A, C)
        if Cfull == 90:
            right_mark(C, A, B)


if __name__ == "__main__":
    app = TrianglesApp()
    app.mainloop()
