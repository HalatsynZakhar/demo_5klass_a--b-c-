"""
Демонстрація: § 20–21. Кути.
Кут, види кутів, градусна міра, транспортир, вимірювання та побудова.
Є вкладка з практикою (тренажер побудови та визначення виду кута).
"""

import tkinter as tk
import math
import random

BG = "#f5f7fa"
PANEL = "#ffffff"
ACCENT = "#4361ee"
SELECTION = "#dbe4ff"
BORDER = "#c8d0e0"
TEXT = "#1a1a2e"
MUTED = "#7b8ab8"
GREEN = "#2d9e5f"
RED = "#d7263d"
ORANGE = "#e07b00"
BLUE = "#1971c2"
PURPLE = "#7048e8"
GRID = "#eaecf4"
WHITE = "#ffffff"
BTN_NUM = "#e2e8f0"

ANGLE_TYPES = [
    {"name": "Гострий", "range": (1, 89), "color": GREEN, "icon": "📐"},
    {"name": "Прямий", "range": (90, 90), "color": BLUE, "icon": "⊾"},
    {"name": "Тупий", "range": (91, 179), "color": ORANGE, "icon": "📏"},
    {"name": "Розгорнутий", "range": (180, 180), "color": PURPLE, "icon": "↔"},
]

DRAW_TOLERANCE = 0


def classify(deg):
    for t in ANGLE_TYPES:
        lo, hi = t["range"]
        if lo <= deg <= hi:
            return t
    return None


def rand_angle():
    weighted_types = ["Гострий", "Гострий", "Тупий", "Тупий", "Прямий", "Розгорнутий"]
    chosen_type_name = random.choice(weighted_types)
    t = next(item for item in ANGLE_TYPES if item["name"] == chosen_type_name)
    lo, hi = t["range"]
    return random.randint(lo, hi)


class AngleTrainerFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)

        self.target_deg = 0
        self.score = 0
        self.total = 0
        self.streak = 0
        self.phase = "build"
        self.user_chosen_type = None

        self._build_ui()
        self.after(120, self._new_question)

    def _build_ui(self):
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        right_w = max(360, int(self.winfo_toplevel().winfo_screenwidth() * 0.33))

        canvas_wrap = tk.Frame(body, bg=BG)
        canvas_wrap.pack(side="left", fill="both", expand=True)
        self.canvas = tk.Canvas(canvas_wrap, bg=PANEL, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=16, pady=16)
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        right = tk.Frame(body, bg=BG, width=right_w)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        pad = tk.Frame(right, bg=BG)
        pad.place(relx=0.5, rely=0.5, anchor="center", width=right_w - 44)

        self.lbl_score = tk.Label(pad, text="", bg=BG, fg=ACCENT, font=("Segoe UI", 14, "bold"))
        self.lbl_score.pack(pady=(0, 10))

        self.lbl_task = tk.Label(pad, text="", bg=BG, fg=TEXT, font=("Segoe UI", 17, "bold"), wraplength=right_w - 60, justify="center")
        self.lbl_task.pack(pady=(0, 6))

        self.lbl_sub = tk.Label(pad, text="", bg=BG, fg=MUTED, font=("Segoe UI", 12), wraplength=right_w - 60, justify="center")
        self.lbl_sub.pack(pady=(0, 20))

        self.btn_frame = tk.Frame(pad, bg=BG)
        self.btn_frame.pack(fill="x")

        self.buttons = {}
        for t in ANGLE_TYPES:
            btn = tk.Button(
                self.btn_frame,
                text=f"{t['icon']}  {t['name']}",
                bg=WHITE,
                fg=TEXT,
                font=("Segoe UI", 13, "bold"),
                relief="flat",
                bd=0,
                cursor="hand2",
                pady=13,
                highlightbackground=BORDER,
                highlightthickness=1,
                command=lambda n=t["name"]: self._on_classify(n),
            )
            btn.pack(fill="x", pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#e8edf8") if b["bg"] == WHITE else None)
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=WHITE) if b["bg"] == "#e8edf8" else None)
            self.buttons[t["name"]] = btn

        self.lbl_result = tk.Label(pad, text="", bg=BG, font=("Segoe UI", 13, "bold"), wraplength=right_w - 60, justify="center")
        self.lbl_result.pack(pady=(20, 6))

        self.btn_action = tk.Button(pad, text="", bg=ACCENT, fg=WHITE, font=("Segoe UI", 13, "bold"), relief="flat", bd=0, cursor="hand2", pady=13, command=self._on_action_button_click)
        self.btn_action.pack(fill="x", pady=4)

    def _new_question(self):
        self.target_deg = rand_angle()
        self.phase = "build"
        self.user_chosen_type = None

        self.lbl_result.config(text="")
        self.btn_action.pack_forget()

        for btn in self.buttons.values():
            btn.config(bg=WHITE, fg=TEXT, state="normal")

        self.lbl_task.config(text=f"Побудуй кут {self.target_deg}°")
        self.lbl_sub.config(text="Торкнись/клацни по дузі, щоб поставити промінь.\nМожна пробувати багато разів!")
        self._draw_circle_phase()
        self._update_score()

    def _on_canvas_click(self, event):
        if self.phase != "build":
            return

        cw = int(self.canvas.winfo_width())
        ch = int(self.canvas.winfo_height())
        if cw < 300 or ch < 300:
            self.canvas.update_idletasks()
            cw = int(self.canvas.winfo_width())
            ch = int(self.canvas.winfo_height())

        cx, cy = cw // 2, ch // 2 + 10
        r = self._R(cw, ch)
        dx, dy = event.x - cx, event.y - cy

        if abs(math.hypot(dx, dy) - r) > 28:
            return

        click_deg = math.degrees(math.atan2(-dy, dx)) % 360
        if click_deg > 180:
            return

        got = round(click_deg)
        build_ok = abs(got - self.target_deg) <= DRAW_TOLERANCE

        self._draw_circle_phase(user_deg=got, success=build_ok)

        if build_ok:
            self.phase = "classify"
            self.lbl_result.config(text="✅ Влучив! Чудова робота!", fg=GREEN)
            self.lbl_task.config(text=f"Кут {self.target_deg}° побудовано!")
            self.lbl_sub.config(text="Тепер вибери правильний тип кута\nі натисни кнопку, щоб перевірити.")
            self.btn_action.config(text="Перевірити тип кута")
            self.btn_action.pack(fill="x", pady=4)
        else:
            direction = "більше" if self.target_deg > got else "менше"
            self.lbl_result.config(text=f"❌ Спробуй ще! Потрібно {direction}.", fg=RED)

    def _on_classify(self, name):
        if self.phase == "done":
            return
        self.user_chosen_type = name
        for n, btn in self.buttons.items():
            btn.config(bg=SELECTION if (n == name) else WHITE, fg=TEXT)

    def _on_action_button_click(self):
        if self.phase == "classify":
            if self.user_chosen_type is None:
                self.lbl_result.config(text="Будь ласка, вибери тип кута", fg=ORANGE)
                return

            self.total += 1
            correct_type = classify(self.target_deg)["name"]
            classify_ok = self.user_chosen_type == correct_type

            if classify_ok:
                self.score += 1
                self.streak += 1
                s = f"  ×{self.streak}" if self.streak > 1 else ""
                self.lbl_result.config(text=f"✅ Тип визначено правильно!{s}", fg=GREEN)
            else:
                self.streak = 0
                self.lbl_result.config(text=f"❌ Ні. Правильний тип: «{correct_type}»", fg=RED)

            for n, btn in self.buttons.items():
                btn.config(state="disabled")
                if n == correct_type:
                    btn.config(bg=GREEN, fg=WHITE)
                elif n == self.user_chosen_type and not classify_ok:
                    btn.config(bg=RED, fg=WHITE)

            self.phase = "done"
            self.btn_action.config(text="▶  Наступне завдання")
            self._update_score()
        elif self.phase == "done":
            self._new_question()

    def _R(self, cw, ch):
        return int(min(cw, ch) * 0.34)

    def _draw_circle_phase(self, user_deg=None, success=None):
        c = self.canvas
        c.delete("all")

        cw = int(c.winfo_width())
        ch = int(c.winfo_height())
        if cw < 300 or ch < 300:
            c.update_idletasks()
            cw = int(c.winfo_width())
            ch = int(c.winfo_height())

        cx, cy = cw // 2, ch // 2 + 10
        r = self._R(cw, ch)
        self._grid(cw, ch)

        c.create_arc(cx - r, cy - r, cx + r, cy + r, start=0, extent=180, style="arc", outline=BORDER, width=3, dash=(8, 5))
        c.create_arc(cx - r, cy - r, cx + r, cy + r, start=180, extent=180, style="arc", outline=GRID, width=1)
        for a in range(0, 181, 30):
            ra = math.radians(a)
            c.create_line(cx + (r - 12) * math.cos(ra), cy - (r - 12) * math.sin(ra), cx + (r + 12) * math.cos(ra), cy - (r + 12) * math.sin(ra), fill=BORDER, width=2)
        c.create_line(cx, cy, cx + r, cy, fill=TEXT, width=3, arrow="last")

        if user_deg is not None:
            col = GREEN if success else RED
            ux = cx + r * math.cos(math.radians(user_deg))
            uy = cy - r * math.sin(math.radians(user_deg))
            dash = () if success else (8, 5)
            c.create_line(cx, cy, ux, uy, fill=col, width=3, dash=dash)
            c.create_oval(ux - 9, uy - 9, ux + 9, uy + 9, fill=col, outline="")
            c.create_text(ux, uy - 22, text=f"{user_deg}°", fill=col, font=("Segoe UI", 12, "bold"))

        if success:
            ar = int(r * 0.30)
            td = self.target_deg
            if 0 < td <= 180:
                c.create_arc(cx - ar, cy - ar, cx + ar, cy + ar, start=0, extent=td, style="arc", outline=ORANGE, width=2)
            if td == 90:
                sq = 18
                c.create_rectangle(cx + 2, cy - sq, cx + sq, cy - 2, outline=BLUE, width=2)

        c.create_oval(cx - 7, cy - 7, cx + 7, cy + 7, fill=ACCENT, outline="")

    def _grid(self, cw, ch):
        c = self.canvas
        for x in range(0, cw, 40):
            c.create_line(x, 0, x, ch, fill=GRID)
        for y in range(0, ch, 40):
            c.create_line(0, y, cw, y, fill=GRID)

    def _update_score(self):
        pct = round(self.score / self.total * 100) if self.total else 0
        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}   ({pct}%)")


class Practice2Frame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)

        self.mode = "name"
        self.phase = "answer"
        self.score = 0
        self.total = 0

        self.canvas_points = {}
        self.selected = set()
        self.expect = set()
        self.task = None

        self._build_ui()
        self.after(120, self.new_task)

    def _build_ui(self):
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        right_w = max(380, int(self.winfo_toplevel().winfo_screenwidth() * 0.34))

        left = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(left, bg=PANEL, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=16, pady=16)
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        right = tk.Frame(body, bg=BG, width=right_w)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        pad = tk.Frame(right, bg=BG)
        pad.place(relx=0.5, rely=0.5, anchor="center", width=right_w - 44)

        tk.Label(pad, text="Практика 2", bg=BG, fg=TEXT, font=("Segoe UI", 18, "bold")).pack(pady=(0, 10))

        tab = tk.Frame(pad, bg=BG)
        tab.pack(fill="x", pady=(0, 12))

        self.btn_tab_name = tk.Button(tab, text="1) Найменування", bg=BTN_NUM, fg=TEXT, font=("Segoe UI", 12, "bold"), bd=0, padx=10, pady=10, command=lambda: self.set_mode("name"))
        self.btn_tab_build = tk.Button(tab, text="2) Побудова", bg=BTN_NUM, fg=TEXT, font=("Segoe UI", 12, "bold"), bd=0, padx=10, pady=10, command=lambda: self.set_mode("build"))
        self.btn_tab_points = tk.Button(tab, text="3) Точки", bg=BTN_NUM, fg=TEXT, font=("Segoe UI", 12, "bold"), bd=0, padx=10, pady=10, command=lambda: self.set_mode("points"))
        self.btn_tab_name.pack(fill="x", pady=4)
        self.btn_tab_build.pack(fill="x", pady=4)
        self.btn_tab_points.pack(fill="x", pady=4)

        self.lbl_score = tk.Label(pad, text="", bg=BG, fg=ACCENT, font=("Segoe UI", 14, "bold"))
        self.lbl_score.pack(pady=(6, 10))

        self.lbl_task = tk.Label(pad, text="", bg=BG, fg=TEXT, font=("Segoe UI", 16, "bold"), wraplength=right_w - 60, justify="center")
        self.lbl_task.pack(pady=(0, 6))
        self.lbl_sub = tk.Label(pad, text="", bg=BG, fg=MUTED, font=("Segoe UI", 12), wraplength=right_w - 60, justify="center")
        self.lbl_sub.pack(pady=(0, 14))

        self.answers = tk.Frame(pad, bg=BG)
        self.answers.pack(fill="x")

        self.lbl_result = tk.Label(pad, text="", bg=BG, fg=TEXT, font=("Segoe UI", 13, "bold"), wraplength=right_w - 60, justify="center")
        self.lbl_result.pack(pady=(16, 6))

        self.btn_action = tk.Button(pad, text="▶ Наступне", bg=ACCENT, fg=WHITE, font=("Segoe UI", 13, "bold"), relief="flat", bd=0, cursor="hand2", pady=12, command=self.new_task)
        self.btn_action.pack(fill="x", pady=4)

        self.btn_check = tk.Button(pad, text="✓ Перевірити", bg=GREEN, fg=WHITE, font=("Segoe UI", 13, "bold"), relief="flat", bd=0, cursor="hand2", pady=12, command=self.check_points_task)
        self.btn_check.pack(fill="x", pady=4)

        self._update_score()
        self._update_tabs()

    def _update_tabs(self):
        sel = SELECTION
        self.btn_tab_name.config(bg=sel if self.mode == "name" else BTN_NUM)
        self.btn_tab_build.config(bg=sel if self.mode == "build" else BTN_NUM)
        self.btn_tab_points.config(bg=sel if self.mode == "points" else BTN_NUM)

    def _update_score(self):
        pct = round(self.score / self.total * 100) if self.total else 0
        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}   ({pct}%)")

    def set_mode(self, mode):
        self.mode = mode
        self._update_tabs()
        self.new_task()

    def _clear_answers(self):
        for w in self.answers.winfo_children():
            w.destroy()

    def _polar(self, ox, oy, r, ang_deg):
        return ox + r * math.cos(math.radians(ang_deg)), oy - r * math.sin(math.radians(ang_deg))

    def _rand_letters(self, n):
        letters = list("ABCDEFGHKLMNPQRSTUVXYZ")
        random.shuffle(letters)
        return letters[:n]

    def _nearest_point(self, x, y, radius=18):
        best = None
        best_d = None
        for name, (px, py) in self.canvas_points.items():
            d = (px - x) ** 2 + (py - y) ** 2
            if d <= radius * radius and (best_d is None or d < best_d):
                best = name
                best_d = d
        return best

    def new_task(self):
        self.phase = "answer"
        self.task = None
        self.selected = set()
        self.expect = set()
        self.canvas_points = {}
        self.lbl_result.config(text="", fg=TEXT)
        self._clear_answers()

        self.btn_action.config(state="normal")
        self.btn_check.pack_forget()

        if self.mode == "name":
            self._task_name()
        elif self.mode == "build":
            self._task_build()
        else:
            self._task_points()

        self._update_score()

    def _task_name(self):
        a, o, b = self._rand_letters(3)
        prompt_kind = random.choice(["three", "vertex"])
        if prompt_kind == "three":
            ok1 = f"∠{a}{o}{b}"
            ok2 = f"∠{b}{o}{a}"
            accept = {ok1, ok2}
            canonical = ok1
            self.lbl_task.config(text="Вибери правильну назву кута (3 літери):")
            self.lbl_sub.config(text=f"Вершина кута — {o} (вона має бути посередині).")
        else:
            canonical = f"∠{o}"
            accept = {canonical}
            self.lbl_task.config(text="Вибери правильну назву кута (за вершиною):")
            self.lbl_sub.config(text=f"Вершина кута — {o}.")

        options = {canonical}
        options.update(accept)
        options.add(f"∠{a}{b}{o}")
        options.add(f"∠{a}")
        options.add(f"∠{b}")
        options = list(options)
        random.shuffle(options)
        options = options[:4]
        if canonical not in options:
            options[random.randrange(len(options))] = canonical
            random.shuffle(options)

        self.task = {"type": "name", "accept": set(accept), "canonical": canonical, "letters": (a, o, b)}
        for opt in options:
            tk.Button(self.answers, text=opt, bg=BTN_NUM, fg=TEXT, font=("Segoe UI", 16, "bold"), bd=0, padx=18, pady=12, command=lambda v=opt: self._pick_name(v)).pack(fill="x", pady=6)

        self._draw_named_angle(a, o, b)

    def _draw_named_angle(self, a, o, b):
        cv = self.canvas
        cv.delete("all")
        w = int(cv.winfo_width())
        h = int(cv.winfo_height())
        if w < 300 or h < 300:
            cv.update_idletasks()
            w = int(cv.winfo_width())
            h = int(cv.winfo_height())
        margin = 70
        ox, oy = int(w * 0.50), int(h * 0.70)
        r = min(w - 2 * margin, h - 2 * margin) * 0.50
        a1 = random.randint(10, 40)
        a2 = random.randint(a1 + 60, min(160, a1 + 120))

        ax, ay = self._polar(ox, oy, r, a1)
        bx, by = self._polar(ox, oy, r, a2)
        cv.create_line(ox, oy, ax, ay, width=6, fill=ACCENT, arrow="last")
        cv.create_line(ox, oy, bx, by, width=6, fill=ACCENT, arrow="last")
        cv.create_oval(ox - 7, oy - 7, ox + 7, oy + 7, fill=ORANGE, outline="")
        cv.create_text(ox, oy + 20, text=o, font=("Segoe UI", 16, "bold"), fill=TEXT)
        cv.create_text(ax + 18, ay, text=a, font=("Segoe UI", 16, "bold"), fill=TEXT)
        cv.create_text(bx - 18, by, text=b, font=("Segoe UI", 16, "bold"), fill=TEXT)
        ar = r * 0.45
        cv.create_arc(ox - ar, oy - ar, ox + ar, oy + ar, start=a1, extent=a2 - a1, style="arc", outline=ORANGE, width=5)

    def _pick_name(self, picked):
        if self.task is None or self.task.get("type") != "name":
            return
        if self.phase != "answer":
            return
        self.phase = "feedback"
        self.total += 1
        accept = set(self.task.get("accept", set()))
        if picked in accept:
            self.score += 1
            self.lbl_result.config(text="✅ Правильно!", fg=GREEN)
            self.after(650, self.new_task)
        else:
            shown = " або ".join(sorted(accept)) if accept else self.task.get("canonical", "")
            self.lbl_result.config(text=f"❌ Ні. Правильно: {shown}", fg=RED)
        self._update_score()

    def _task_build(self):
        a, o, b = self._rand_letters(3)
        self.task = {"type": "build", "a": a, "o": o, "b": b, "need": {a, b}, "picked": []}
        self.lbl_task.config(text=f"Побудуй кут {a}{o}{b}")
        self.lbl_sub.config(text=f"Побудуй 2 промені з вершини {o}: до точок {a} і {b}. Потім натисни «Перевірити».")
        self._clear_answers()
        self.btn_action.config(state="disabled")
        self.btn_check.pack(fill="x", pady=4)
        self.btn_check.config(state="disabled")
        self._generate_build_scene()
        self._draw_build_scene()

    def _generate_build_scene(self):
        cv = self.canvas
        w = int(cv.winfo_width())
        h = int(cv.winfo_height())
        if w < 300 or h < 300:
            cv.update_idletasks()
            w = int(cv.winfo_width())
            h = int(cv.winfo_height())

        margin = 80
        ox, oy = int(w * 0.50), int(h * 0.72)
        r = min(w - 2 * margin, h - 2 * margin) * 0.55
        a = self.task["a"]
        o = self.task["o"]
        b = self.task["b"]

        decoys = [x for x in self._rand_letters(6) if x not in {a, o, b}]
        decoys = decoys[:4]
        endpoints = [a, b] + decoys
        random.shuffle(endpoints)

        angles_pool = [15, 35, 55, 75, 95, 115, 135, 155, 165]
        angs = random.sample(angles_pool, k=len(endpoints))
        points = {o: (ox, oy)}
        for name, ang in zip(endpoints, angs):
            px, py = self._polar(ox, oy, r, ang)
            points[name] = (px, py)

        self.task["geom"] = {"ox": ox, "oy": oy, "r": r}
        self.task["points"] = points

    def _draw_build_scene(self):
        cv = self.canvas
        cv.delete("all")
        w = int(cv.winfo_width())
        h = int(cv.winfo_height())
        if w < 300 or h < 300:
            cv.update_idletasks()
            w = int(cv.winfo_width())
            h = int(cv.winfo_height())

        a = self.task["a"]
        o = self.task["o"]
        b = self.task["b"]
        pts = self.task.get("points") or {}
        if not pts:
            self._generate_build_scene()
            pts = self.task.get("points") or {}

        ox, oy = pts[o]
        self.canvas_points = dict(pts)

        cv.create_oval(ox - 8, oy - 8, ox + 8, oy + 8, fill=ORANGE, outline="")
        cv.create_text(ox, oy + 22, text=o, font=("Segoe UI", 16, "bold"), fill=TEXT)

        for name, (px, py) in pts.items():
            if name == o:
                continue
            cv.create_oval(px - 10, py - 10, px + 10, py + 10, fill=ACCENT, outline="")
            cv.create_text(px, py - 22, text=name, font=("Segoe UI", 16, "bold"), fill=TEXT)

        picked = list(self.task.get("picked", []))
        for end_name in picked:
            ex, ey = self.canvas_points[end_name]
            cv.create_line(ox, oy, ex, ey, width=6, fill=GREEN, arrow="last")

        self.btn_check.config(state="normal" if len(picked) == 2 else "disabled")
        self.lbl_sub.config(text=f"Побудуй 2 промені з вершини {o}: до точок {a} і {b}. Потім натисни «Перевірити».")

    def _on_canvas_click(self, e):
        if self.task is None:
            return
        t = self.task.get("type")
        if t == "build":
            self._build_click(e.x, e.y)
        elif t == "points":
            self._points_click(e.x, e.y)

    def _build_click(self, x, y):
        hit = self._nearest_point(x, y)
        if hit is None:
            return
        if hit == self.task["o"]:
            return
        pts = self.task.get("points") or {}
        if hit not in pts:
            return
        picked = self.task["picked"]
        if hit in picked:
            picked.remove(hit)
        else:
            if len(picked) >= 2:
                picked.pop(0)
            picked.append(hit)
        self.lbl_result.config(text=f"Вибрано: {', '.join(picked) or '—'}", fg=MUTED)
        self._draw_build_scene()

    def check_build_task(self):
        if self.task is None or self.task.get("type") != "build":
            return
        if self.phase != "answer":
            return
        need = set(self.task.get("need", set()))
        picked_list = list(self.task.get("picked", []))
        picked = set(picked_list)
        if len(picked_list) != 2 or len(picked) != 2:
            return
        self.phase = "feedback"
        self.total += 1
        if picked == need:
            self.score += 1
            self.lbl_result.config(text="✅ Правильно! Кут побудовано.", fg=GREEN)
            self.after(650, self.new_task)
        else:
            self.lbl_result.config(text=f"❌ Ні. Потрібно: {', '.join(sorted(need))}", fg=RED)
            self.btn_action.config(state="normal")
        self._update_score()

    def _task_points(self):
        a, o, b = self._rand_letters(3)
        group = random.choice(["inside", "on", "outside"])
        prompt = {"inside": "внутрішній області", "on": "сторонах", "outside": "поза кутом"}[group]
        self.task = {"type": "points", "a": a, "o": o, "b": b, "group": group}
        self.lbl_task.config(text=f"Обери всі точки, що лежать y / на {prompt}")
        self.lbl_sub.config(text=f"Торкнись точок на малюнку, потім натисни «Перевірити». Кут: {a}{o}{b}")
        self.btn_check.pack(fill="x", pady=4)
        self.btn_check.config(state="normal")
        self.btn_action.config(state="disabled")
        self._generate_points_scene()
        self._draw_points_scene()

    def _generate_points_scene(self):
        cv = self.canvas
        w = int(cv.winfo_width())
        h = int(cv.winfo_height())
        if w < 300 or h < 300:
            cv.update_idletasks()
            w = int(cv.winfo_width())
            h = int(cv.winfo_height())

        margin = 80
        ox, oy = int(w * 0.48), int(h * 0.76)
        r = min(w - 2 * margin, h - 2 * margin) * 0.56
        a1 = random.randint(10, 35)
        a2 = random.randint(a1 + 70, min(165, a1 + 125))

        letters = self._rand_letters(6)
        pts = []

        for _ in range(2):
            ang = random.uniform(a1 + 12, a2 - 12)
            rr = random.uniform(r * 0.30, r * 0.85)
            pts.append(("inside", self._polar(ox, oy, rr, ang)))
        for _ in range(2):
            side = random.choice([a1, a2])
            rr = random.uniform(r * 0.35, r * 0.85)
            pts.append(("on", self._polar(ox, oy, rr, side)))
        for _ in range(2):
            if random.random() < 0.5:
                ang = random.uniform(max(0, a1 - 60), max(1, a1 - 18))
            else:
                ang = random.uniform(min(179, a2 + 18), min(180, a2 + 60))
            rr = random.uniform(r * 0.35, r * 0.85)
            pts.append(("outside", self._polar(ox, oy, rr, ang)))

        random.shuffle(pts)
        point_pos = {}
        point_group = {}
        expect = set()
        for name, (g, (px, py)) in zip(letters, pts):
            point_pos[name] = (px, py)
            point_group[name] = g
            if g == self.task["group"]:
                expect.add(name)

        self.task["angle"] = {"ox": ox, "oy": oy, "a1": a1, "a2": a2, "r": r}
        self.task["point_pos"] = point_pos
        self.task["point_group"] = point_group
        self.expect = set(expect)
        self.canvas_points = dict(point_pos)

    def _draw_points_scene(self):
        cv = self.canvas
        cv.delete("all")
        w = int(cv.winfo_width())
        h = int(cv.winfo_height())
        if w < 300 or h < 300:
            cv.update_idletasks()
            w = int(cv.winfo_width())
            h = int(cv.winfo_height())

        if not self.task.get("angle") or not self.task.get("point_pos"):
            self._generate_points_scene()

        ang = self.task["angle"]
        ox, oy, r, a1, a2 = ang["ox"], ang["oy"], ang["r"], ang["a1"], ang["a2"]
        ax, ay = self._polar(ox, oy, r, a1)
        bx, by = self._polar(ox, oy, r, a2)

        cv.create_line(ox, oy, ax, ay, width=6, fill=ACCENT, arrow="last")
        cv.create_line(ox, oy, bx, by, width=6, fill=ACCENT, arrow="last")
        cv.create_oval(ox - 8, oy - 8, ox + 8, oy + 8, fill=ORANGE, outline="")
        cv.create_text(ox, oy + 22, text=self.task["o"], font=("Segoe UI", 16, "bold"), fill=TEXT)
        cv.create_text(ax + 18, ay, text=self.task["a"], font=("Segoe UI", 16, "bold"), fill=TEXT)
        cv.create_text(bx - 18, by, text=self.task["b"], font=("Segoe UI", 16, "bold"), fill=TEXT)
        ar = r * 0.45
        cv.create_arc(ox - ar, oy - ar, ox + ar, oy + ar, start=a1, extent=a2 - a1, style="arc", outline=ORANGE, width=5)
        self.canvas_points = dict(self.task["point_pos"])

        self._render_points_markers()

    def _render_points_markers(self):
        cv = self.canvas
        for name, (px, py) in self.canvas_points.items():
            r = 12
            fill = GREEN if name in self.selected else BLUE
            cv.create_oval(px - r, py - r, px + r, py + r, fill=fill, outline="")
            cv.create_text(px, py - 22, text=name, font=("Segoe UI", 14, "bold"), fill=TEXT)

    def _points_click(self, x, y):
        hit = self._nearest_point(x, y, radius=22)
        if hit is None:
            return
        if hit in self.selected:
            self.selected.remove(hit)
        else:
            self.selected.add(hit)
        self._draw_points_scene()

    def _draw_points_scene_static(self):
        self._draw_points_scene()

    def check_points_task(self):
        if self.task is None:
            return
        if self.task.get("type") == "build":
            self.check_build_task()
            return
        if self.task.get("type") != "points":
            return
        if self.phase != "answer":
            return
        self.phase = "feedback"
        self.total += 1
        if set(self.selected) == set(self.expect):
            self.score += 1
            self.lbl_result.config(text="✅ Правильно!", fg=GREEN)
            self.btn_action.config(state="normal")
            self.after(650, self.new_task)
        else:
            exp = " ".join(sorted(self.expect))
            self.lbl_result.config(text=f"❌ Ні. Правильно: {exp}", fg=RED)
            self.btn_action.config(state="normal")
        self._update_score()


class AnglesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("§ 20–21. Кути")
        self.configure(bg=BG)

        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()

        self._build_ui()
        self.show_s20_angle()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=ACCENT, height=80)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="Кути (§ 20–21)", bg=ACCENT, fg=WHITE, font=("Segoe UI", 24, "bold")).pack(side="left", padx=30)
        tk.Button(hdr, text="❌ Вихід", font=("Arial", 16, "bold"), bg=RED, fg=WHITE, bd=0, command=self.destroy).pack(side="right", padx=20)

        nav = tk.Frame(self, bg=WHITE, height=60)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        btn_font = ("Segoe UI", 12, "bold")
        tk.Button(nav, text="§20: Кут", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_s20_angle).pack(side="left", padx=10)
        tk.Button(nav, text="§20: Види", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_s20_types).pack(side="left", padx=10)
        tk.Button(nav, text="§20: Точки/Поділ", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_s20_points_split).pack(side="left", padx=10)
        tk.Button(nav, text="§21: Градуси/Транспортир", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_s21_protractor).pack(side="left", padx=10)
        tk.Button(nav, text="Практика", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_practice).pack(side="left", padx=10)
        tk.Button(nav, text="Практика 2", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_practice2).pack(side="left", padx=10)

        self.main_area = tk.Frame(self, bg=BG)
        self.main_area.pack(fill="both", expand=True)

        self.practice_frame = None
        self.practice2_frame = None
        self.protractor_angle = 50

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

    def show_s20_angle(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)

        tk.Label(f, text="§ 20. Кут", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        tk.Label(
            f,
            text=(
                "Кут — це геометрична фігура, що складається з двох променів,\n"
                "які виходять з однієї точки.\n\n"
                "• точка спільного початку — вершина кута\n"
                "• промені — сторони кута\n"
                "• кут називають за трьома літерами: ∠AOB (вершина завжди посередині)\n"
                "  або за вершиною: ∠O"
            ),
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            justify="left",
            wraplength=self.SW - 160,
        ).pack(anchor="w", pady=(0, 10))

        cv_h = max(360, int(self.SH * 0.42))
        cv = tk.Canvas(f, bg=WHITE, height=cv_h, bd=2, relief="ridge")
        cv.pack(fill="x", pady=15, padx=10)
        self.after(80, lambda: self._draw_basic_angle(cv))

    def _draw_basic_angle(self, cv):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())
        if h < 220:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 220:
            h = 320

        margin = 60
        cx, cy = w // 2, int(h * 0.64)
        r = min(w - 2 * margin, h - 2 * margin) * 0.48
        a1 = 20
        a2 = 110
        x1 = cx + r * math.cos(math.radians(a1))
        y1 = cy - r * math.sin(math.radians(a1))
        x2 = cx + r * math.cos(math.radians(a2))
        y2 = cy - r * math.sin(math.radians(a2))
        cv.create_line(cx, cy, x1, y1, width=5, fill=ACCENT, arrow="last")
        cv.create_line(cx, cy, x2, y2, width=5, fill=ACCENT, arrow="last")
        cv.create_oval(cx - 7, cy - 7, cx + 7, cy + 7, fill=ORANGE, outline="")
        cv.create_text(cx, cy + 18, text="O", font=("Segoe UI", 14, "bold"), fill=TEXT)
        cv.create_text(x1 + 16, y1, text="A", font=("Segoe UI", 14, "bold"), fill=TEXT)
        cv.create_text(x2 - 16, y2, text="B", font=("Segoe UI", 14, "bold"), fill=TEXT)
        ar = r * 0.45
        cv.create_arc(cx - ar, cy - ar, cx + ar, cy + ar, start=a1, extent=a2 - a1, style="arc", outline=ORANGE, width=4)
        cv.create_text(cx, int(h * 0.16), text="∠AOB", font=("Segoe UI", 22, "bold"), fill=TEXT)

    def show_s20_types(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)

        tk.Label(f, text="§ 20. Види кутів", font=("Segoe UI", 30, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        tk.Label(
            f,
            text=(
                "• гострий — менший за прямий (менше 90°)\n"
                "• прямий — дорівнює 90°\n"
                "• тупий — більший за 90°, але менший за 180°\n"
                "• розгорнутий — дорівнює 180° (сторони — доповняльні промені)"
            ),
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            justify="left",
        ).pack(anchor="w", pady=(0, 10))

        cv_h = max(420, int(self.SH * 0.50))
        cv = tk.Canvas(f, bg=WHITE, height=cv_h, bd=2, relief="ridge")
        cv.pack(fill="x", pady=15, padx=10)
        self.after(80, lambda: self._draw_angle_types(cv))

    def _draw_angle_types(self, cv):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())
        if h < 260:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 260:
            h = 360

        items = [
            ("Гострий", 40, GREEN),
            ("Прямий", 90, BLUE),
            ("Тупий", 130, ORANGE),
            ("Розгорнутий", 180, PURPLE),
        ]

        cols = 2
        rows = 2
        cell_w = w / cols
        cell_h = h / rows

        for idx, (name, deg, col) in enumerate(items):
            r = idx // cols
            c = idx % cols
            cx = int(c * cell_w + cell_w * 0.5)
            cy = int(r * cell_h + cell_h * 0.70)
            margin = 42
            rr = min(cell_w - 2 * margin, cell_h - 2 * margin) * 0.50

            cv.create_text(cx, int(r * cell_h + 32), text=f"{name}: {deg}°", font=("Segoe UI", 18, "bold"), fill=TEXT)
            cv.create_line(cx, cy, cx + rr, cy, width=5, fill=TEXT, arrow="last")
            ang = deg
            x2 = cx + rr * math.cos(math.radians(ang))
            y2 = cy - rr * math.sin(math.radians(ang))
            cv.create_line(cx, cy, x2, y2, width=5, fill=col, arrow="last")
            ar = rr * 0.52
            cv.create_arc(cx - ar, cy - ar, cx + ar, cy + ar, start=0, extent=ang, style="arc", outline=col, width=4)
            if deg == 90:
                sq = 24
                cv.create_rectangle(cx + 4, cy - sq, cx + sq, cy - 4, outline=BLUE, width=3)
            cv.create_oval(cx - 6, cy - 6, cx + 6, cy + 6, fill=ACCENT, outline="")

    def show_s20_points_split(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)

        tk.Label(f, text="§ 20. Розміщення точок. Поділ кута", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        tk.Label(
            f,
            text=(
                "Точки можуть бути:\n"
                "• у внутрішній області кута\n"
                "• на сторонах кута\n"
                "• поза кутом\n\n"
                "Якщо з вершини кута провести промінь, він поділить кут на два кути."
            ),
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            justify="left",
        ).pack(anchor="w", pady=(0, 10))

        cards = tk.Frame(f, bg=BG)
        cards.pack(fill="both", expand=True, pady=10)

        c1 = tk.Frame(cards, bg=WHITE, bd=2, relief="ridge")
        c1.pack(side="left", expand=True, fill="both", padx=(10, 6), pady=10)
        tk.Label(c1, text="Точки відносно кута", font=("Segoe UI", 16, "bold"), bg=WHITE, fg=TEXT).pack(anchor="w", padx=14, pady=(12, 6))
        tk.Label(c1, text="Зелений — всередині, синій — на стороні, червоний — поза кутом", font=("Segoe UI", 12), bg=WHITE, fg=MUTED).pack(anchor="w", padx=14)
        cv1 = tk.Canvas(c1, bg=WHITE, height=max(320, int(self.SH * 0.42)), highlightthickness=0)
        cv1.pack(fill="both", expand=True, padx=10, pady=10)

        c2 = tk.Frame(cards, bg=WHITE, bd=2, relief="ridge")
        c2.pack(side="left", expand=True, fill="both", padx=(6, 10), pady=10)
        tk.Label(c2, text="Поділ кута променем", font=("Segoe UI", 16, "bold"), bg=WHITE, fg=TEXT).pack(anchor="w", padx=14, pady=(12, 6))
        tk.Label(c2, text="Промінь з вершини ділить кут на два кути", font=("Segoe UI", 12), bg=WHITE, fg=MUTED).pack(anchor="w", padx=14)
        cv2 = tk.Canvas(c2, bg=WHITE, height=max(320, int(self.SH * 0.42)), highlightthickness=0)
        cv2.pack(fill="both", expand=True, padx=10, pady=10)

        self.after(80, lambda: self._draw_points_in_angle(cv1))
        self.after(80, lambda: self._draw_angle_split(cv2))

    def _draw_points_in_angle(self, cv):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())
        if h < 260:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 260:
            h = 360

        margin = 60
        cx, cy = int(w * 0.46), int(h * 0.74)
        r = min(w - 2 * margin, h - 2 * margin) * 0.52
        a1 = 20
        a2 = 120
        x1 = cx + r * math.cos(math.radians(a1))
        y1 = cy - r * math.sin(math.radians(a1))
        x2 = cx + r * math.cos(math.radians(a2))
        y2 = cy - r * math.sin(math.radians(a2))
        cv.create_line(cx, cy, x1, y1, width=5, fill=ACCENT, arrow="last")
        cv.create_line(cx, cy, x2, y2, width=5, fill=ACCENT, arrow="last")
        cv.create_oval(cx - 7, cy - 7, cx + 7, cy + 7, fill=ORANGE, outline="")
        cv.create_text(cx, cy + 18, text="O", font=("Segoe UI", 12, "bold"), fill=TEXT)

        pts_inside = [("C", cx + r * 0.28, cy - r * 0.28), ("D", cx + r * 0.18, cy - r * 0.18)]
        pts_on = [
            ("L", cx + r * math.cos(math.radians(a1)) * 0.58, cy - r * math.sin(math.radians(a1)) * 0.58),
            ("P", cx + r * math.cos(math.radians(a2)) * 0.58, cy - r * math.sin(math.radians(a2)) * 0.58),
        ]
        pts_out = [("M", cx - r * 0.30, cy - r * 0.40), ("N", cx + r * 0.58, cy + r * 0.10)]

        for name, x, y in pts_inside:
            cv.create_oval(x - 6, y - 6, x + 6, y + 6, fill=GREEN, outline="")
            cv.create_text(x, y - 14, text=name, font=("Segoe UI", 12, "bold"), fill=TEXT)
        for name, x, y in pts_on:
            cv.create_oval(x - 6, y - 6, x + 6, y + 6, fill=BLUE, outline="")
            cv.create_text(x, y - 14, text=name, font=("Segoe UI", 12, "bold"), fill=TEXT)
        for name, x, y in pts_out:
            cv.create_oval(x - 6, y - 6, x + 6, y + 6, fill=RED, outline="")
            cv.create_text(x, y - 14, text=name, font=("Segoe UI", 12, "bold"), fill=TEXT)

    def _draw_angle_split(self, cv):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())
        if h < 260:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 260:
            h = 360

        margin = 60
        cx, cy = w // 2, int(h * 0.78)
        r2 = min(w - 2 * margin, h - 2 * margin) * 0.52
        b1 = 10
        b2 = 140
        split = 70
        cv.create_line(cx, cy, cx + r2 * math.cos(math.radians(b1)), cy - r2 * math.sin(math.radians(b1)), width=5, fill=ACCENT, arrow="last")
        cv.create_line(cx, cy, cx + r2 * math.cos(math.radians(b2)), cy - r2 * math.sin(math.radians(b2)), width=5, fill=ACCENT, arrow="last")
        cv.create_line(cx, cy, cx + r2 * math.cos(math.radians(split)), cy - r2 * math.sin(math.radians(split)), width=4, fill=ORANGE, dash=(8, 4), arrow="last")
        ar = r2 * 0.52
        cv.create_arc(cx - ar, cy - ar, cx + ar, cy + ar, start=0, extent=split, style="arc", outline=ORANGE, width=4)
        cv.create_arc(cx - ar, cy - ar, cx + ar, cy + ar, start=split, extent=b2 - split, style="arc", outline=BLUE, width=4)
        cv.create_oval(cx - 7, cy - 7, cx + 7, cy + 7, fill=ORANGE, outline="")

    def show_s21_protractor(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)

        tk.Label(f, text="§ 21. Величина кута. Транспортир", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        tk.Label(
            f,
            text=(
                "Градус (1°) — це 1/90 частина прямого кута.\n"
                "Прямий кут = 90°, розгорнутий кут = 180°.\n\n"
                "Транспортир — прилад для вимірювання та побудови кутів.\n"
                "Його шкала має 180 поділок (1 поділка = 1°) і зазвичай дві нумерації: зліва і справа."
            ),
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            justify="left",
            wraplength=self.SW - 160,
        ).pack(anchor="w", pady=(0, 10))

        top = tk.Frame(f, bg=BG)
        top.pack(fill="x", pady=(0, 10))
        self.lbl_protractor = tk.Label(top, text="", font=("Segoe UI", 16, "bold"), bg=BG, fg=MUTED)
        self.lbl_protractor.pack(side="left")
        tk.Button(top, text="🎲 Приклад", font=("Segoe UI", 14, "bold"), bg=ACCENT, fg=WHITE, bd=0, padx=16, pady=10, command=self._new_protractor_example).pack(side="right", padx=10)

        tk.Label(
            f,
            text="Як виміряти: центр = вершина; одна сторона через 0°; друга сторона показує градуси.",
            font=("Segoe UI", 13, "bold"),
            bg=BG,
            fg=MUTED,
        ).pack(anchor="w", pady=(0, 8))

        self.protractor_canvas = tk.Canvas(f, bg=WHITE, height=max(420, int(self.SH * 0.52)), bd=2, relief="ridge")
        self.protractor_canvas.pack(fill="x", pady=10, padx=10)

        self.after(80, self._new_protractor_example)

    def _new_protractor_example(self):
        self.protractor_angle = random.choice([30, 40, 50, 60, 75, 90, 110, 120, 135, 150, 165])
        self.lbl_protractor.config(text=f"Приклад: вимірювання кута. Друга сторона проходить через штрих {self.protractor_angle}°.")
        self._draw_protractor(self.protractor_canvas, self.protractor_angle)

    def _draw_protractor(self, cv, angle):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())
        if h < 260:
            cv.update_idletasks()
            h = int(cv.winfo_height())
        if h < 260:
            h = 360

        margin = 60
        cx, cy = w // 2, int(h * 0.80)
        r = min(w - 2 * margin, h - 2 * margin) * 0.60
        cv.create_arc(cx - r, cy - r, cx + r, cy + r, start=0, extent=180, style="arc", outline=TEXT, width=3)
        cv.create_line(cx - r, cy, cx + r, cy, width=3, fill=TEXT)
        cv.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill=ORANGE, outline="")

        for a in range(0, 181, 10):
            ra = math.radians(a)
            x1 = cx + (r - 10) * math.cos(ra)
            y1 = cy - (r - 10) * math.sin(ra)
            x2 = cx + (r + (10 if a % 30 == 0 else 4)) * math.cos(ra)
            y2 = cy - (r + (10 if a % 30 == 0 else 4)) * math.sin(ra)
            cv.create_line(x1, y1, x2, y2, width=2 if a % 30 == 0 else 1, fill=BORDER if a % 30 != 0 else TEXT)

        for a in range(0, 181, 30):
            ra = math.radians(a)
            xt = cx + (r - 22) * math.cos(ra)
            yt = cy - (r - 22) * math.sin(ra)
            cv.create_text(xt, yt, text=str(a), font=("Segoe UI", 10, "bold"), fill=MUTED)

        cv.create_text(cx - r + 10, cy + 18, text="0°", font=("Segoe UI", 10, "bold"), fill=MUTED, anchor="w")
        cv.create_text(cx + r - 10, cy + 18, text="180°", font=("Segoe UI", 10, "bold"), fill=MUTED, anchor="e")

        cv.create_line(cx, cy, cx + r * 0.95, cy, width=4, fill=ACCENT, arrow="last")
        x2 = cx + r * 0.95 * math.cos(math.radians(angle))
        y2 = cy - r * 0.95 * math.sin(math.radians(angle))
        cv.create_line(cx, cy, x2, y2, width=4, fill=ORANGE, arrow="last")
        ar = r * 0.35
        cv.create_arc(cx - ar, cy - ar, cx + ar, cy + ar, start=0, extent=angle, style="arc", outline=ORANGE, width=4)
        cv.create_text(cx, cy - ar - 18, text=f"{angle}°", font=("Segoe UI", 16, "bold"), fill=ORANGE)

    def show_practice(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both")

        tk.Label(f, text="Практика: побудуй кут і визнач його вид", font=("Segoe UI", 22, "bold"), bg=BG, fg=TEXT).pack(pady=(16, 0))
        tk.Label(f, text="Порада: гострий < 90°, прямий = 90°, тупий між 90° і 180°, розгорнутий = 180°.", font=("Segoe UI", 14), bg=BG, fg=MUTED).pack(pady=(4, 10))

        wrap = tk.Frame(f, bg=BG)
        wrap.pack(fill="both", expand=True)

        self.practice_frame = AngleTrainerFrame(wrap)
        self.practice_frame.pack(fill="both", expand=True)

    def show_practice2(self):
        self.clear_main()
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both")

        tk.Label(f, text="Практика 2: назви, побудова, точки", font=("Segoe UI", 22, "bold"), bg=BG, fg=TEXT).pack(pady=(16, 0))
        tk.Label(f, text="Тут є 3 режими: найменування кута, побудова кута за точками, вибір точок (всередині/на стороні/поза).", font=("Segoe UI", 14), bg=BG, fg=MUTED).pack(
            pady=(4, 10)
        )

        wrap = tk.Frame(f, bg=BG)
        wrap.pack(fill="both", expand=True)

        self.practice2_frame = Practice2Frame(wrap)
        self.practice2_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = AnglesApp()
    app.mainloop()
