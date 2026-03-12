"""
Тренажер «Кути» — повноекранний, тільки миша.
Два етапи на кожне питання:
  1. Classify — вибрати тип кута з кнопок
  2. Draw     — побудувати кут, натиснувши на кружечок по колу
"""

import tkinter as tk
import math
import random

# ── палітра ───────────────────────────────────────────────────────────────────
BG        = "#0d1117"
PANEL     = "#161b22"
ACCENT    = "#21262d"
BORDER    = "#30363d"
TEXT      = "#e6edf3"
MUTED     = "#6e7681"
GREEN     = "#3fb950"
RED       = "#f85149"
YELLOW    = "#d29922"
BLUE      = "#58a6ff"
PURPLE    = "#bc8cff"
WHITE     = "#ffffff"
GRID      = "#161b22"

# ── типи кутів (без нульового та опуклого) ─────────────────────────────────────
ANGLE_TYPES = [
    {"name": "Гострий",      "range": (1,  89),  "color": GREEN,   "icon": "📐"},
    {"name": "Прямий",       "range": (90,  90), "color": BLUE,    "icon": "⊾"},
    {"name": "Тупий",        "range": (91, 179), "color": YELLOW,  "icon": "📏"},
    {"name": "Розгорнутий",  "range": (180,180), "color": PURPLE,  "icon": "↔"},
    {"name": "Повний",       "range": (360,360), "color": WHITE,   "icon": "○"},
]

DRAW_TOLERANCE = 12   # допуск у градусах для фази побудови

def classify(deg):
    for t in ANGLE_TYPES:
        lo, hi = t["range"]
        if lo <= deg <= hi:
            return t
    return None

def rand_angle():
    t = random.choice(ANGLE_TYPES)
    lo, hi = t["range"]
    return random.randint(lo, hi)

# ─────────────────────────────────────────────────────────────────────────────
class AngleTrainer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Тренажер: Кути")
        self.attributes("-fullscreen", True)
        self.configure(bg=BG)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        # стан
        self.target_deg  = 0
        self.score       = 0
        self.total       = 0
        self.streak      = 0
        self.phase       = "classify"   # "classify" | "draw" | "feedback"
        self.draw_dot    = None         # (x, y) — куди тикнув користувач

        self.update_idletasks()
        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()

        self._build_ui()
        self._new_question()

    # ── побудова UI ───────────────────────────────────────────────────────────
    def _build_ui(self):
        SW, SH = self.SW, self.SH

        # ── шапка
        self.hdr = tk.Frame(self, bg=ACCENT, height=56)
        self.hdr.pack(fill="x")
        self.hdr.pack_propagate(False)

        tk.Label(self.hdr, text="📐  Тренажер «Кути»",
                 bg=ACCENT, fg=WHITE, font=("Segoe UI", 17, "bold")
                 ).place(x=24, rely=0.5, anchor="w")

        self.lbl_score = tk.Label(self.hdr, text="",
                                  bg=ACCENT, fg=GREEN, font=("Segoe UI", 14, "bold"))
        self.lbl_score.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.hdr, text="ESC — вийти з повного екрана",
                 bg=ACCENT, fg=MUTED, font=("Segoe UI", 10)
                 ).place(relx=1.0, x=-16, rely=0.5, anchor="e")

        # ── тіло
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        # ліва частина — канвас
        self.CW = int(SW * 0.62)
        self.CH = SH - 56
        self.canvas = tk.Canvas(body, width=self.CW, height=self.CH,
                                bg=PANEL, highlightthickness=0)
        self.canvas.pack(side="left", fill="both")
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        # права частина — панель
        self.RW = SW - self.CW
        right = tk.Frame(body, bg=BG, width=self.RW)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        pad = tk.Frame(right, bg=BG)
        pad.place(relx=0.5, rely=0.5, anchor="center", width=self.RW - 40)

        self.lbl_task = tk.Label(pad, text="", bg=BG, fg=TEXT,
                                 font=("Segoe UI", 16, "bold"),
                                 wraplength=self.RW - 60, justify="center")
        self.lbl_task.pack(pady=(0, 8))

        self.lbl_sub = tk.Label(pad, text="", bg=BG, fg=MUTED,
                                font=("Segoe UI", 12),
                                wraplength=self.RW - 60, justify="center")
        self.lbl_sub.pack(pady=(0, 18))

        # кнопки типів
        self.btn_frame = tk.Frame(pad, bg=BG)
        self.btn_frame.pack(fill="x")

        self.buttons = {}
        for t in ANGLE_TYPES:
            lo, hi = t["range"]
            range_str = f"{lo}°" if lo == hi else f"{lo}°–{hi}°"
            btn = tk.Button(
                self.btn_frame,
                text=f"{t['icon']}  {t['name']}  ({range_str})",
                bg=ACCENT, fg=TEXT, activebackground=t["color"],
                activeforeground=BG if t["color"] == WHITE else WHITE,
                font=("Segoe UI", 13, "bold"),
                relief="flat", bd=0, cursor="hand2", pady=12,
                command=lambda name=t["name"]: self._on_classify(name)
            )
            btn.pack(fill="x", pady=5)
            self._hover(btn, ACCENT, BORDER)
            self.buttons[t["name"]] = btn

        # повідомлення результату
        self.lbl_result = tk.Label(pad, text="", bg=BG,
                                   font=("Segoe UI", 14, "bold"), wraplength=self.RW - 60)
        self.lbl_result.pack(pady=(18, 8))

        # кнопка «далі»
        self.btn_next = tk.Button(
            pad, text="▶  Наступне питання",
            bg=BLUE, fg=BG, font=("Segoe UI", 13, "bold"),
            relief="flat", bd=0, cursor="hand2", pady=12,
            command=self._next
        )
        self.btn_next.pack(fill="x", pady=4)
        self.btn_next.pack_forget()

        self._right_pad = pad   # зберігаємо для перемальовування

    def _hover(self, btn, normal_bg, hover_bg):
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=normal_bg if btn["state"] == "normal" else btn["bg"]))

    # ── нове питання ──────────────────────────────────────────────────────────
    def _new_question(self):
        self.target_deg = rand_angle()
        self.phase      = "classify"
        self.draw_dot   = None
        self.lbl_result.config(text="")
        self.btn_next.pack_forget()

        for btn in self.buttons.values():
            btn.config(bg=ACCENT, fg=TEXT, state="normal")

        self._show_classify_task()
        self._draw_angle(self.target_deg, show_type=False)
        self._update_score()

    def _show_classify_task(self):
        self.lbl_task.config(text="Крок 1 / 2")
        self.lbl_sub.config(text="Який це тип кута?")
        for btn in self.buttons.values():
            btn.pack(fill="x", pady=5)

    def _show_draw_task(self):
        self.lbl_task.config(text="Крок 2 / 2")
        self.lbl_sub.config(
            text=f"Побудуй кут {self.target_deg}°:\nнатисни точку на колі, щоб\nвказати другий промінь"
        )
        for btn in self.buttons.values():
            btn.pack_forget()   # ховаємо кнопки на час побудови

    # ── відповідь: класифікація ───────────────────────────────────────────────
    def _on_classify(self, name):
        if self.phase != "classify":
            return

        correct_type = classify(self.target_deg)
        is_correct   = (name == correct_type["name"])
        self.total  += 1

        if is_correct:
            self.score  += 1
            self.streak += 1
            streak_str = f"  🔥 ×{self.streak}" if self.streak > 1 else ""
            self.lbl_result.config(text=f"✅  Правильно!{streak_str}", fg=GREEN)
        else:
            self.streak = 0
            self.lbl_result.config(
                text=f"❌  Неправильно!\nЦе «{correct_type['name']}»", fg=RED)

        # підсвічування
        for n, btn in self.buttons.items():
            if n == correct_type["name"]:
                btn.config(bg=GREEN, fg=BG, state="disabled")
            elif n == name and not is_correct:
                btn.config(bg=RED, fg=WHITE, state="disabled")
            else:
                btn.config(state="disabled")

        self._update_score()

        # переходимо до фази побудови
        self.phase = "draw"
        self.after(900, self._start_draw_phase)

    def _start_draw_phase(self):
        self.lbl_result.config(text="")
        self._show_draw_task()
        self._draw_angle_with_circle(self.target_deg)

    # ── клік по канвасу (фаза побудови) ──────────────────────────────────────
    def _on_canvas_click(self, event):
        if self.phase != "draw":
            return

        cx = self.CW // 2
        cy = self.CH // 2 + 20
        R  = self._circle_radius()

        dx = event.x - cx
        dy = event.y - cy
        dist = math.hypot(dx, dy)

        # приймаємо клік тільки поблизу кола (±22 px)
        if abs(dist - R) > 22:
            return

        # кут кліку (від правого горизонталь, проти год. стрілки)
        click_deg = math.degrees(math.atan2(-dy, dx)) % 360
        diff = abs(click_deg - self.target_deg)
        diff = min(diff, 360 - diff)

        self.draw_dot = (event.x, event.y, click_deg)

        if diff <= DRAW_TOLERANCE:
            self.lbl_result.config(text=f"✅  Чудово! Ти побудував {self.target_deg}°!", fg=GREEN)
            self._draw_angle_with_circle(self.target_deg, user_deg=click_deg, success=True)
        else:
            self.lbl_result.config(
                text=f"❌  Майже! Ти поставив ~{click_deg:.0f}°,\nпотрібно {self.target_deg}°", fg=RED)
            self._draw_angle_with_circle(self.target_deg, user_deg=click_deg, success=False)

        self.phase = "feedback"
        self.btn_next.pack(fill="x", pady=4)

    # ── малювання ─────────────────────────────────────────────────────────────
    def _circle_radius(self):
        return int(min(self.CW, self.CH) * 0.34)

    def _draw_angle(self, deg, show_type=True):
        """Просто кут без кола для побудови."""
        c = self.canvas
        c.delete("all")
        CW, CH = self.CW, self.CH
        cx, cy = CW // 2, CH // 2 + 20
        R = int(min(CW, CH) * 0.30)

        self._draw_grid(CW, CH)

        # промені
        x1 = cx + R
        rad = math.radians(deg)
        x2 = cx + R * math.cos(rad)
        y2 = cy - R * math.sin(rad)

        # промінь 1
        c.create_line(cx, cy, x1, cy, fill=WHITE, width=3, arrow="last")
        # промінь 2
        if deg != 0:
            c.create_line(cx, cy, x2, y2, fill=RED, width=3, arrow="last")

        # дуга
        arc_r = int(R * 0.38)
        if 0 < deg < 360:
            c.create_arc(cx - arc_r, cy - arc_r, cx + arc_r, cy + arc_r,
                         start=0, extent=deg, style="arc", outline=YELLOW, width=2)
        elif deg == 360:
            c.create_oval(cx - arc_r, cy - arc_r, cx + arc_r, cy + arc_r,
                          outline=YELLOW, width=2)

        # прямий кут — квадратик
        if deg == 90:
            sq = 20
            c.create_rectangle(cx + 2, cy - sq, cx + sq, cy - 2,
                                outline=BLUE, width=2)

        # підпис градусів
        lx = cx + (arc_r + 28) * math.cos(math.radians(deg / 2))
        ly = cy - (arc_r + 28) * math.sin(math.radians(deg / 2))
        c.create_text(lx, ly, text=f"{deg}°", fill=YELLOW,
                      font=("Segoe UI", 14, "bold"))

        # вершина
        c.create_oval(cx - 6, cy - 6, cx + 6, cy + 6, fill=RED, outline="")

        # тип кута (якщо треба)
        if show_type:
            t = classify(deg)
            if t:
                c.create_text(CW // 2, 36, text=f"{t['icon']}  {t['name']}",
                              fill=t["color"], font=("Segoe UI", 16, "bold"))

    def _draw_angle_with_circle(self, deg, user_deg=None, success=None):
        """Кут + коло для побудови + точка користувача."""
        c = self.canvas
        c.delete("all")
        CW, CH = self.CW, self.CH
        cx, cy = CW // 2, CH // 2 + 20
        R = self._circle_radius()

        self._draw_grid(CW, CH)

        # ── коло-направляч
        c.create_oval(cx - R, cy - R, cx + R, cy + R,
                      outline=BORDER, width=2, dash=(6, 4))

        # ── позначки кожні 30°
        for a in range(0, 360, 30):
            rad_a = math.radians(a)
            ox = cx + R * math.cos(rad_a)
            oy = cy - R * math.sin(rad_a)
            r2 = 5
            c.create_oval(ox - r2, oy - r2, ox + r2, oy + r2,
                          fill=BORDER, outline="")
            # підпис
            lx = cx + (R + 22) * math.cos(rad_a)
            ly = cy - (R + 22) * math.sin(rad_a)
            c.create_text(lx, ly, text=f"{a}°", fill=MUTED,
                          font=("Segoe UI", 9))

        # ── промінь 1 (завжди → 0°)
        c.create_line(cx, cy, cx + R, cy, fill=WHITE, width=3, arrow="last")

        # ── якщо вже є відповідь користувача
        if user_deg is not None:
            color_user = GREEN if success else RED
            ux = cx + R * math.cos(math.radians(user_deg))
            uy = cy - R * math.sin(math.radians(user_deg))
            c.create_line(cx, cy, ux, uy, fill=color_user, width=3,
                          dash=(8, 4) if not success else ())
            c.create_oval(ux - 9, uy - 9, ux + 9, uy + 9,
                          fill=color_user, outline="")
            c.create_text(ux, uy - 18, text=f"{user_deg:.0f}°",
                          fill=color_user, font=("Segoe UI", 11, "bold"))

            if not success:
                # показати правильне положення пунктиром
                tx = cx + R * math.cos(math.radians(deg))
                ty = cy - R * math.sin(math.radians(deg))
                c.create_line(cx, cy, tx, ty, fill=GREEN, width=2, dash=(6, 4))
                c.create_oval(tx - 8, ty - 8, tx + 8, ty + 8,
                              fill=GREEN, outline="")
                c.create_text(tx, ty - 18, text=f"{deg}°",
                              fill=GREEN, font=("Segoe UI", 11, "bold"))

        # ── дуга
        arc_r = int(R * 0.32)
        if 0 < deg < 360:
            c.create_arc(cx - arc_r, cy - arc_r, cx + arc_r, cy + arc_r,
                         start=0, extent=deg, style="arc", outline=YELLOW, width=2)
        elif deg == 360:
            c.create_oval(cx - arc_r, cy - arc_r, cx + arc_r, cy + arc_r,
                          outline=YELLOW, width=2)

        # прямий кут — квадратик
        if deg == 90:
            sq = 18
            c.create_rectangle(cx + 2, cy - sq, cx + sq, cy - 2,
                                outline=BLUE, width=2)

        # підпис потрібного кута
        lx = cx + (arc_r + 26) * math.cos(math.radians(deg / 2))
        ly = cy - (arc_r + 26) * math.sin(math.radians(deg / 2))
        c.create_text(lx, ly, text=f"{deg}°", fill=YELLOW,
                      font=("Segoe UI", 13, "bold"))

        # ── вершина
        c.create_oval(cx - 7, cy - 7, cx + 7, cy + 7, fill=RED, outline="")

        # ── підказка (якщо ще не відповів)
        if user_deg is None:
            c.create_text(CW // 2, CH - 28,
                          text="👆  Натисни на колі, щоб вказати другий промінь",
                          fill=MUTED, font=("Segoe UI", 12))

    def _draw_grid(self, CW, CH):
        c = self.canvas
        step = 40
        for x in range(0, CW, step):
            c.create_line(x, 0, x, CH, fill=GRID)
        for y in range(0, CH, step):
            c.create_line(0, y, CW, y, fill=GRID)

    # ── допоміжні ─────────────────────────────────────────────────────────────
    def _next(self):
        self._new_question()

    def _update_score(self):
        pct = round(self.score / self.total * 100) if self.total else 0
        self.lbl_score.config(text=f"✓ {self.score} / {self.total}   ({pct}%)")


# ── запуск ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = AngleTrainer()
    app.mainloop()