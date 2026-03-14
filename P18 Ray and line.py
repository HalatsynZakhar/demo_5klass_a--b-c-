"""
Демонстрація: Промінь і пряма (§ 17).
Для 5 класу.
Промінь, пряма, доповняльні промені, площина.
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


class RayLineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Промінь і пряма")
        self.configure(bg=BG)

        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.bind("<Key>", self._on_key_press)
        self.bind("<Return>", lambda e: self.check_answer())
        self.bind("<BackSpace>", lambda e: self._key_press("⌫"))
        self.bind("<Delete>", lambda e: self._key_press("C"))

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()

        self.mode = "theory"
        self.task = None
        self.user_input = ""
        self.phase = "answer"
        self.score = 0
        self.total = 0

        self._build_ui()
        self.show_ray()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=ACCENT, height=80)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(
            hdr,
            text="Промінь і пряма (§ 17)",
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
        tk.Button(nav, text="1. Промінь", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_ray).pack(
            side="left", padx=10
        )
        tk.Button(nav, text="2. Пряма", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_line).pack(
            side="left", padx=10
        )
        tk.Button(
            nav,
            text="3. Доповняльні промені",
            font=btn_font,
            bg=WHITE,
            bd=0,
            cursor="hand2",
            command=self.show_complementary,
        ).pack(side="left", padx=10)
        tk.Button(nav, text="4. Площина", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_plane).pack(
            side="left", padx=10
        )
        tk.Button(nav, text="5. Побудови", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_constructions).pack(
            side="left", padx=10
        )
        tk.Button(nav, text="6. Тренажер", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_trainer).pack(
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

    def _draw_point(self, cv, x, y, label, color=ORANGE):
        cv.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color, outline=WHITE, width=2)
        cv.create_text(x, y - 22, text=label, font=("Segoe UI", 12, "bold"), fill=TEXT)

    def show_ray(self):
        self.clear_main()
        self.mode = "ray"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=40, pady=25)

        tk.Label(f, text="Промінь", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        tk.Label(
            f,
            text="Промінь має початок, але не має кінця. Назву пишуть так: спочатку точка-початок.",
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            wraplength=self.SW - 120,
            justify="left",
        ).pack(pady=(0, 10))

        cv = tk.Canvas(f, bg=WHITE, height=340, bd=2, relief="ridge")
        cv.pack(fill="x", pady=15, padx=10)

        w = self._canvas_width(cv, self.SW - 120)
        y = 170
        left = 80
        mid = w // 2
        right = w - 80

        cv.create_text(left, 35, text="Промінь AB (продовжили відрізок AB за B)", font=("Segoe UI", 14, "bold"), fill=TEXT, anchor="w")
        cv.create_line(left, y, right, y, width=4, fill=ACCENT, arrow="last")
        self._draw_point(cv, left, y, "A")
        self._draw_point(cv, mid, y, "B")

        y2 = 280
        cv.create_text(left, 225, text="Промінь BA (продовжили відрізок AB за A)", font=("Segoe UI", 14, "bold"), fill=TEXT, anchor="w")
        cv.create_line(left, y2, right, y2, width=4, fill=INDIGO, arrow="first")
        self._draw_point(cv, mid, y2, "A")
        self._draw_point(cv, right, y2, "B")

    def show_line(self):
        self.clear_main()
        self.mode = "line"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=40, pady=25)

        tk.Label(f, text="Пряма", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        tk.Label(
            f,
            text="Пряма не має ні початку, ні кінця. Через будь-які дві точки можна провести тільки одну пряму.",
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            wraplength=self.SW - 120,
            justify="left",
        ).pack(pady=(0, 10))

        cv = tk.Canvas(f, bg=WHITE, height=340, bd=2, relief="ridge")
        cv.pack(fill="x", pady=15, padx=10)

        w = self._canvas_width(cv, self.SW - 120)
        y = 180
        left = 80
        right = w - 80
        ax = w * 0.35
        bx = w * 0.65

        cv.create_line(left, y, right, y, width=4, fill=ACCENT, arrow="both")
        self._draw_point(cv, ax, y, "A")
        self._draw_point(cv, bx, y, "B")
        cv.create_text(left, 60, text="Цю пряму можна назвати AB або BA, або позначити малою літерою.", font=("Segoe UI", 14), fill=TEXT, anchor="w")
        cv.create_text(left, 95, text="Наприклад: пряма a", font=("Segoe UI", 16, "bold"), fill=ACCENT, anchor="w")
        cv.create_text(left, 130, text="Через A і B — тільки одна пряма.", font=("Segoe UI", 14, "italic"), fill=MUTED, anchor="w")

        cv.create_text(right - 10, y - 25, text="a", font=("Segoe UI", 16, "bold"), fill=ACCENT, anchor="e")

    def show_complementary(self):
        self.clear_main()
        self.mode = "compl"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=40, pady=25)

        tk.Label(f, text="Доповняльні промені", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        tk.Label(
            f,
            text="Точка на прямій ділить її на два промені. Такі промені називають доповняльними: разом вони утворюють пряму.",
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            wraplength=self.SW - 120,
            justify="left",
        ).pack(pady=(0, 10))

        cv = tk.Canvas(f, bg=WHITE, height=340, bd=2, relief="ridge")
        cv.pack(fill="x", pady=15, padx=10)

        w = self._canvas_width(cv, self.SW - 120)
        y = 180
        left = 90
        right = w - 90
        kx = w // 2

        cv.create_line(left, y, right, y, width=4, fill=MUTED, arrow="both")
        self._draw_point(cv, left + 90, y, "M", color=ORANGE)
        self._draw_point(cv, right - 90, y, "L", color=ORANGE)
        self._draw_point(cv, kx, y, "K", color=INDIGO)

        cv.create_line(kx, y, left, y, width=6, fill=ACCENT, arrow="last")
        cv.create_line(kx, y, right, y, width=6, fill=ORANGE, arrow="last")
        cv.create_text(left, 70, text="Промені KM і KL — доповняльні.", font=("Segoe UI", 18, "bold"), fill=TEXT, anchor="w")
        cv.create_text(left, 110, text="Вони мають спільний початок K і лежать на одній прямій у протилежних напрямках.", font=("Segoe UI", 14), fill=MUTED, anchor="w")

    def show_plane(self):
        self.clear_main()
        self.mode = "plane"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=40, pady=25)

        tk.Label(f, text="Площина", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        tk.Label(
            f,
            text="Площина — геометрична фігура, яку можна уявити як поверхню стола або дошки, якщо подумки продовжити її без меж.",
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            wraplength=self.SW - 120,
            justify="left",
        ).pack(pady=(0, 10))

        cv = tk.Canvas(f, bg=WHITE, height=360, bd=2, relief="ridge")
        cv.pack(fill="x", pady=15, padx=10)

        w = self._canvas_width(cv, self.SW - 120)
        x0, y0 = 150, 120
        poly = [x0, y0, x0 + 520, y0 - 40, x0 + 620, y0 + 180, x0 + 100, y0 + 220]
        cv.create_polygon(*poly, fill="#e0f2fe", outline="#93c5fd", width=2)
        cv.create_text(x0 + 20, y0 + 20, text="площина", font=("Segoe UI", 14, "bold"), fill=ACCENT, anchor="w")

        ax, ay = x0 + 160, y0 + 120
        bx, by = x0 + 460, y0 + 90
        cx, cy = x0 + 320, y0 + 170

        cv.create_line(ax, ay, bx, by, width=4, fill=INDIGO)
        cv.create_line(cx, cy, cx + 220, cy - 60, width=4, fill=ORANGE, arrow="last")
        cv.create_line(x0 + 130, y0 + 60, x0 + 560, y0 + 35, width=3, fill=MUTED, arrow="both")

        self._draw_point(cv, ax, ay, "A", color=ORANGE)
        self._draw_point(cv, bx, by, "B", color=ORANGE)
        self._draw_point(cv, cx, cy, "C", color=INDIGO)

        cv.create_text(x0 + 120, y0 + 250, text="На площині можна зобразити точку, відрізок, промінь і пряму.", font=("Segoe UI", 14), fill=TEXT, anchor="w")

    def show_constructions(self):
        self.clear_main()
        self.mode = "build"

        LW = int(self.SW * 0.68)
        RW = self.SW - LW

        left = tk.Frame(self.main_area, bg=BG, width=LW)
        left.pack(side="left", fill="both")
        left.pack_propagate(False)

        top = tk.Frame(left, bg=BG)
        top.pack(fill="x", padx=20, pady=(20, 10))
        tk.Label(top, text="Побудови: побудуй фігуру за умовою", font=("Segoe UI", 26, "bold"), bg=BG, fg=TEXT).pack(
            side="left"
        )

        self.build_task_lbl = tk.Label(left, text="", font=("Segoe UI", 18, "bold"), bg=BG, fg=MUTED, justify="left", wraplength=LW - 60)
        self.build_task_lbl.pack(fill="x", padx=20)

        self.build_canvas = tk.Canvas(left, bg=WHITE, height=420, bd=2, relief="ridge")
        self.build_canvas.pack(fill="both", expand=True, padx=20, pady=15)
        self.build_canvas.bind("<Button-1>", self._build_on_click)

        self.build_feedback = tk.Label(left, text="", font=("Segoe UI", 18, "bold"), bg=BG)
        self.build_feedback.pack(pady=10)

        right = tk.Frame(self.main_area, bg=PANEL, width=RW, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        rpad = tk.Frame(right, bg=PANEL)
        rpad.pack(fill="both", expand=True, padx=25, pady=25)

        tk.Label(rpad, text="Інструмент", font=("Segoe UI", 18, "bold"), bg=PANEL, fg=MUTED).pack(anchor="w")
        tool_box = tk.Frame(rpad, bg=PANEL)
        tool_box.pack(fill="x", pady=10)

        self.build_tool = "ray"
        self.build_tool_lbl = tk.Label(rpad, text="Обрано: Промінь", font=("Segoe UI", 14, "bold"), bg=PANEL, fg=INDIGO)
        self.build_tool_lbl.pack(anchor="w", pady=(0, 10))

        self.btn_tool_seg = tk.Button(tool_box, text="Відрізок", font=("Segoe UI", 14, "bold"), bg=BTN_NUM, bd=0, padx=10, pady=10, command=lambda: self._build_set_tool("segment"))
        self.btn_tool_ray = tk.Button(tool_box, text="Промінь", font=("Segoe UI", 14, "bold"), bg=BTN_NUM, bd=0, padx=10, pady=10, command=lambda: self._build_set_tool("ray"))
        self.btn_tool_line = tk.Button(tool_box, text="Пряма", font=("Segoe UI", 14, "bold"), bg=BTN_NUM, bd=0, padx=10, pady=10, command=lambda: self._build_set_tool("line"))
        self.btn_tool_seg.pack(fill="x", pady=4)
        self.btn_tool_ray.pack(fill="x", pady=4)
        self.btn_tool_line.pack(fill="x", pady=4)

        tk.Label(rpad, text="Дії", font=("Segoe UI", 18, "bold"), bg=PANEL, fg=MUTED).pack(anchor="w", pady=(10, 0))
        btns = tk.Frame(rpad, bg=PANEL)
        btns.pack(fill="x", pady=10)

        tk.Button(btns, text="Очистити", font=("Segoe UI", 14, "bold"), bg=BTN_NUM, bd=0, padx=10, pady=10, command=self._build_clear).pack(fill="x", pady=4)
        tk.Button(btns, text="✓ Перевірити", font=("Segoe UI", 14, "bold"), bg=GREEN, fg=WHITE, bd=0, padx=10, pady=10, command=self._build_check).pack(fill="x", pady=4)
        tk.Button(btns, text="🎲 Наступне", font=("Segoe UI", 14, "bold"), bg=ACCENT, fg=WHITE, bd=0, padx=10, pady=10, command=self._build_new_task).pack(fill="x", pady=4)

        hint_box = tk.Frame(rpad, bg="#eff6ff", highlightbackground="#bfdbfe", highlightthickness=1, padx=12, pady=12)
        hint_box.pack(fill="x", pady=(15, 0))
        self.build_hint_lbl = tk.Label(
            hint_box,
            text="Натисни на дві точки, щоб побудувати фігуру.\nДля променя важливий порядок: перша точка — початок.",
            font=("Segoe UI", 12),
            bg="#eff6ff",
            justify="left",
        )
        self.build_hint_lbl.pack(anchor="w")

        self.build_points = {}
        self.build_selected = []
        self.build_objects = []
        self.build_required = []

        self._build_set_tool("ray")
        self.after(80, self._build_new_task)

    def _build_set_tool(self, tool):
        self.build_tool = tool
        if tool == "segment":
            title = "Відрізок"
        elif tool == "ray":
            title = "Промінь"
        else:
            title = "Пряма"
        self.build_tool_lbl.config(text=f"Обрано: {title}")
        for b, t in ((self.btn_tool_seg, "segment"), (self.btn_tool_ray, "ray"), (self.btn_tool_line, "line")):
            b.config(bg="#dcfce7" if t == tool else BTN_NUM)
        self.build_hint_lbl.config(
            text="Натисни на дві точки, щоб побудувати фігуру.\nДля променя важливий порядок: перша точка — початок.",
        )

    def _build_new_task(self):
        if self.mode != "build":
            return
        self.build_feedback.config(text="", fg=TEXT, bg=BG)
        self.build_selected = []
        self.build_objects = []

        w = self._canvas_width(self.build_canvas, self.SW * 0.68 - 60)
        h = int(self.build_canvas.winfo_height())
        if h < 260:
            self.build_canvas.update_idletasks()
            h = int(self.build_canvas.winfo_height())
        if h < 260:
            h = 420

        cx = w // 2
        cy = h // 2

        tasks = ["ray_ab", "ray_ba", "line_ab", "seg_ab", "compl_k", "two_rays_a"]
        t = random.choice(tasks)

        if t == "ray_ab":
            self.build_task_lbl.config(text="Побудуй промінь AB (початок у точці A, проходить через B).", fg=MUTED)
            self.build_points = {"A": (cx - 220, cy), "B": (cx - 40, cy)}
            self.build_required = [{"tool": "ray", "p1": "A", "p2": "B"}]
        elif t == "ray_ba":
            self.build_task_lbl.config(text="Побудуй промінь BA (початок у точці B, проходить через A).", fg=MUTED)
            self.build_points = {"A": (cx - 80, cy), "B": (cx + 120, cy)}
            self.build_required = [{"tool": "ray", "p1": "B", "p2": "A"}]
        elif t == "line_ab":
            self.build_task_lbl.config(text="Проведи пряму через точки A і B.", fg=MUTED)
            self.build_points = {"A": (cx - 160, cy - 30), "B": (cx + 160, cy + 30)}
            self.build_required = [{"tool": "line", "p1": "A", "p2": "B"}]
        elif t == "seg_ab":
            self.build_task_lbl.config(text="Побудуй відрізок AB.", fg=MUTED)
            self.build_points = {"A": (cx - 160, cy), "B": (cx + 110, cy)}
            self.build_required = [{"tool": "segment", "p1": "A", "p2": "B"}]
        elif t == "compl_k":
            self.build_task_lbl.config(text="Побудуй доповняльні промені KM і KL (від точки K у протилежні напрямки).", fg=MUTED)
            self.build_points = {"M": (cx - 240, cy), "K": (cx, cy), "L": (cx + 240, cy)}
            self.build_required = [{"tool": "ray", "p1": "K", "p2": "M"}, {"tool": "ray", "p1": "K", "p2": "L"}]
        else:
            self.build_task_lbl.config(text="Побудуй два різні промені AM і AN (спільний початок A).", fg=MUTED)
            self.build_points = {"A": (cx - 120, cy + 30), "M": (cx + 120, cy - 70), "N": (cx + 160, cy + 120)}
            self.build_required = [{"tool": "ray", "p1": "A", "p2": "M"}, {"tool": "ray", "p1": "A", "p2": "N"}]

        self._build_redraw()

    def _build_clear(self):
        if self.mode != "build":
            return
        self.build_selected = []
        self.build_objects = []
        self.build_feedback.config(text="", fg=TEXT, bg=BG)
        self._build_redraw()

    def _build_on_click(self, event):
        if self.mode != "build":
            return
        if not self.build_points:
            return

        hit = None
        best = 10**9
        for name, (x, y) in self.build_points.items():
            dx = event.x - x
            dy = event.y - y
            d2 = dx * dx + dy * dy
            if d2 <= 18 * 18 and d2 < best:
                best = d2
                hit = name

        if hit is None:
            return

        self.build_selected.append(hit)
        if len(self.build_selected) > 2:
            self.build_selected = [hit]

        if len(self.build_selected) == 2:
            p1, p2 = self.build_selected
            obj = {"tool": self.build_tool, "p1": p1, "p2": p2}
            self.build_objects.append(obj)
            self.build_selected = []

        self._build_redraw()

    def _build_redraw(self):
        cv = self.build_canvas
        cv.delete("all")

        w = self._canvas_width(cv, self.SW * 0.68 - 60)
        h = int(cv.winfo_height() or 420)

        cv.create_rectangle(0, 0, w, h, fill=WHITE, outline="")

        for obj in self.build_objects:
            tool = obj["tool"]
            p1 = obj["p1"]
            p2 = obj["p2"]
            if p1 not in self.build_points or p2 not in self.build_points:
                continue
            x1, y1 = self.build_points[p1]
            x2, y2 = self.build_points[p2]
            if tool == "segment":
                cv.create_line(x1, y1, x2, y2, width=6, fill=ACCENT)
            elif tool == "line":
                dx = x2 - x1
                dy = y2 - y1
                if dx == 0 and dy == 0:
                    continue
                t1 = -10000
                t2 = 10000
                xa, ya = x1 + dx * t1, y1 + dy * t1
                xb, yb = x1 + dx * t2, y1 + dy * t2
                cv.create_line(xa, ya, xb, yb, width=4, fill=MUTED, arrow="both")
            else:
                dx = x2 - x1
                dy = y2 - y1
                if dx == 0 and dy == 0:
                    continue
                t2 = 2000
                xe = x1 + dx * t2
                ye = y1 + dy * t2
                cv.create_line(x1, y1, xe, ye, width=6, fill=ORANGE, arrow="last")

        for name, (x, y) in self.build_points.items():
            selected = name in self.build_selected
            cv.create_oval(x - 12, y - 12, x + 12, y + 12, fill=INDIGO if selected else ORANGE, outline=WHITE, width=2)
            cv.create_text(x, y - 26, text=name, font=("Segoe UI", 12, "bold"), fill=TEXT)

    def _build_check(self):
        if self.mode != "build":
            return
        if not self.build_required:
            return

        def key(obj):
            tool = obj["tool"]
            a = obj["p1"]
            b = obj["p2"]
            if tool in ("segment", "line"):
                if a > b:
                    a, b = b, a
            return (tool, a, b)

        need = [key(o) for o in self.build_required]
        have = [key(o) for o in self.build_objects]

        ok = True
        for n in need:
            if n in have:
                have.remove(n)
            else:
                ok = False
                break

        if ok:
            self.build_feedback.config(text="✅ Правильно!", fg=GREEN)
        else:
            self.build_feedback.config(text="❌ Не так. Побудуй потрібну фігуру(и) ще раз.", fg=RED)

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

        self.task_canvas = tk.Canvas(left, bg=WHITE, height=240, bd=2, relief="ridge")
        self.task_canvas.pack(pady=10, padx=20, fill="x")

        self.lbl_feedback = tk.Label(left, text="", font=("Segoe UI", 18, "bold"), bg=BG)
        self.lbl_feedback.pack(pady=10)

        self.btns_frame = tk.Frame(left, bg=BG)
        self.btns_frame.pack(pady=10)

        self.btn_ok = tk.Button(
            self.btns_frame,
            text="✓ Перевірити",
            bg=GREEN,
            fg=WHITE,
            font=("Segoe UI", 18, "bold"),
            relief="flat",
            bd=0,
            padx=30,
            pady=12,
            command=self.check_answer,
        )
        self.btn_ok.pack(side="left", padx=15)

        self.btn_next = tk.Button(
            self.btns_frame,
            text="▶ Наступне",
            bg=ACCENT,
            fg=WHITE,
            font=("Segoe UI", 18, "bold"),
            relief="flat",
            bd=0,
            padx=30,
            pady=12,
            command=self.next_task,
        )

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
                "• Відрізок має 2 кінці.\n"
                "• Промінь має початок, але не має кінця.\n"
                "• Пряма не має ні початку, ні кінця.\n"
                "• Через будь-які дві точки — одна пряма.\n"
                "• Доповняльні промені: спільний початок і утворюють пряму."
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

    def _clear_answer_buttons(self):
        for w in self.btns_frame.winfo_children():
            if w not in (self.btn_ok, self.btn_next):
                w.destroy()

    def _set_choice(self, value):
        if self.phase != "answer":
            return
        self.task["chosen"] = value
        self._highlight_choice_buttons()

    def _highlight_choice_buttons(self):
        for w in self.btns_frame.winfo_children():
            if isinstance(w, tk.Button) and getattr(w, "_choice_value", None) is not None:
                if self.task and self.task.get("chosen") == w._choice_value:
                    w.config(bg="#dcfce7")
                else:
                    w.config(bg=BTN_NUM)

    def _add_choice_buttons(self, options):
        self._clear_answer_buttons()
        for opt in options:
            b = tk.Button(
                self.btns_frame,
                text=opt,
                font=("Segoe UI", 18, "bold"),
                bg=BTN_NUM,
                fg=TEXT,
                relief="flat",
                bd=0,
                padx=22,
                pady=12,
                cursor="hand2",
                command=lambda v=opt: self._set_choice(v),
            )
            b._choice_value = opt
            b.pack(side="left", padx=10)
        self._highlight_choice_buttons()

    def next_task(self):
        if self.mode != "trainer":
            return

        self.phase = "answer"
        self.lbl_feedback.config(text="", fg=TEXT, bg=BG)
        self.btn_next.pack_forget()
        self.btn_ok.pack(side="left", padx=15)
        self.task_canvas.delete("all")

        t = random.choice(["figure", "membership", "compl", "count"])

        if t == "figure":
            kind = random.choice(["segment", "ray", "line"])
            if kind == "segment":
                question = "Що зображено на малюнку?"
                correct = "Відрізок"
                hint_title = "Підказка: відрізок"
                hint_text = "Відрізок має ДВА кінці. На малюнку видно дві крайні точки."
            elif kind == "ray":
                question = "Що зображено на малюнку?"
                correct = "Промінь"
                hint_title = "Підказка: промінь"
                hint_text = "Промінь має початок і стрілку в одному напрямку (кінця немає)."
            else:
                question = "Що зображено на малюнку?"
                correct = "Пряма"
                hint_title = "Підказка: пряма"
                hint_text = "Пряма має стрілки з двох боків (немає ні початку, ні кінця)."

            self.task = {"type": "figure", "correct": correct, "chosen": None, "hint_title": hint_title, "hint_text": hint_text}
            self.task_text.config(text=question)
            self._add_choice_buttons(["Відрізок", "Промінь", "Пряма"])
            self._draw_figure_task(kind)

        elif t == "membership":
            kind = random.choice(["line", "ray"])
            belongs = random.choice([True, False])
            self.task = {
                "type": "membership",
                "kind": kind,
                "belongs": belongs,
                "correct": "Так" if belongs else "Ні",
                "chosen": None,
                "hint_title": "Підказка: належність",
                "hint_text": "Точка належить променю/прямій, якщо лежить на намальованій лінії.",
            }
            self.task_text.config(text="Чи належить точка P цій фігурі?")
            self._add_choice_buttons(["Так", "Ні"])
            self._draw_membership_task(kind, belongs)

        elif t == "compl":
            is_compl = random.choice([True, False])
            self.task = {
                "type": "compl",
                "correct": "Так" if is_compl else "Ні",
                "chosen": None,
                "hint_title": "Підказка: доповняльні промені",
                "hint_text": "Доповняльні промені мають спільний початок і лежать на одній прямій у протилежних напрямках.",
            }
            self.task_text.config(text="Чи є ці два промені доповняльними?")
            self._add_choice_buttons(["Так", "Ні"])
            self._draw_compl_task(is_compl)

        else:
            self.task = {
                "type": "count",
                "correct": "1",
                "chosen": None,
                "hint_title": "Підказка: пряма через дві точки",
                "hint_text": "Через будь-які дві різні точки можна провести ТІЛЬКИ ОДНУ пряму.",
            }
            self.task_text.config(text="Скільки прямих можна провести через дві різні точки A і B?")
            self._add_choice_buttons(["0", "1", "2"])
            self._draw_two_points_task()

        self._render_task_hint()
        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")

    def _draw_figure_task(self, kind):
        cv = self.task_canvas
        w = self._canvas_width(cv, self.SW * 0.62 - 60)
        y = 120
        left = 90
        right = w - 90
        mid = (left + right) // 2

        if kind == "segment":
            cv.create_line(left, y, right, y, width=6, fill=ACCENT)
            self._draw_point(cv, left, y, "A")
            self._draw_point(cv, right, y, "B")
        elif kind == "ray":
            cv.create_line(left, y, right, y, width=6, fill=ACCENT, arrow="last")
            self._draw_point(cv, left, y, "A")
            self._draw_point(cv, mid, y, "B")
        else:
            cv.create_line(left, y, right, y, width=6, fill=ACCENT, arrow="both")
            self._draw_point(cv, mid - 60, y, "A")
            self._draw_point(cv, mid + 60, y, "B")

    def _draw_membership_task(self, kind, belongs):
        cv = self.task_canvas
        w = self._canvas_width(cv, self.SW * 0.62 - 60)
        h = 240
        left = 80
        right = w - 80
        y = 120

        if kind == "line":
            cv.create_line(left, y, right, y, width=6, fill=MUTED, arrow="both")
            self._draw_point(cv, left + 120, y, "A", color=ORANGE)
            self._draw_point(cv, right - 120, y, "B", color=ORANGE)
            if belongs:
                px, py = (left + right) // 2, y
            else:
                px, py = (left + right) // 2, y - 55
            self._draw_point(cv, px, py, "P", color=INDIGO)
        else:
            cx, cy = left + 110, y + 30
            cv.create_line(cx, cy, right, cy - 60, width=6, fill=MUTED, arrow="last")
            self._draw_point(cv, cx, cy, "A", color=ORANGE)
            if belongs:
                px, py = cx + 180, cy - 30
            else:
                px, py = cx + 180, cy + 40
            self._draw_point(cv, px, py, "P", color=INDIGO)

    def _draw_compl_task(self, is_compl):
        cv = self.task_canvas
        w = self._canvas_width(cv, self.SW * 0.62 - 60)
        left = 90
        right = w - 90
        y = 120
        kx = w // 2

        self._draw_point(cv, kx, y, "K", color=INDIGO)

        if is_compl:
            cv.create_line(left, y, right, y, width=4, fill=BORDER, arrow="both")
            cv.create_line(kx, y, left, y, width=7, fill=ACCENT, arrow="last")
            cv.create_line(kx, y, right, y, width=7, fill=ORANGE, arrow="last")
            self._draw_point(cv, left + 110, y, "M", color=ORANGE)
            self._draw_point(cv, right - 110, y, "L", color=ORANGE)
        else:
            cv.create_line(kx, y, right, y - 60, width=7, fill=ACCENT, arrow="last")
            cv.create_line(kx, y, right, y + 60, width=7, fill=ORANGE, arrow="last")
            self._draw_point(cv, right - 120, y - 50, "M", color=ORANGE)
            self._draw_point(cv, right - 120, y + 50, "L", color=ORANGE)

    def _draw_two_points_task(self):
        cv = self.task_canvas
        w = self._canvas_width(cv, self.SW * 0.62 - 60)
        y = 120
        left = 110
        right = w - 110
        cv.create_line(left, y, right, y, width=4, fill=MUTED, arrow="both")
        self._draw_point(cv, left + 120, y, "A", color=ORANGE)
        self._draw_point(cv, right - 120, y, "B", color=ORANGE)

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
            if len(self.user_input) < 2:
                self.user_input += ch

    def check_answer(self):
        if self.mode != "trainer":
            return
        if self.phase != "answer":
            return
        if not self.task:
            return

        chosen = self.task.get("chosen")
        if chosen is None:
            return

        self.phase = "feedback"
        self.total += 1
        ok = chosen == self.task["correct"]

        if ok:
            self.score += 1
            self.lbl_feedback.config(text="✅ Правильно!", fg=GREEN)
            self.after(900, self.next_task)
        else:
            self.lbl_feedback.config(text=f"❌ Ні. Правильно: {self.task['correct']}", fg=RED)
            self.btn_ok.pack_forget()
            self.btn_next.pack(side="left", padx=15)

        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")


if __name__ == "__main__":
    app = RayLineApp()
    app.mainloop()
