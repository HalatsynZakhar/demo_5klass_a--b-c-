"""
Тренажер «Кути» — весела гра на вгадування.
Крок 1: Побудуй кут на око, отримуй миттєвий відгук.
Крок 2: Визнач тип побудованого кута та перевір себе.
"""

import tkinter as tk
import math
import random

# ── світла палітра ────────────────────────────────────────────────────────────
BG         = "#f5f7fa"
PANEL      = "#ffffff"
ACCENT     = "#4361ee"
SELECTION  = "#dbe4ff" # ВИПРАВЛЕНО: Колір для виділення кнопки
BORDER     = "#c8d0e0"
TEXT       = "#1a1a2e"
MUTED      = "#7b8ab8"
GREEN      = "#2d9e5f"
RED        = "#d7263d"
ORANGE     = "#e07b00"
BLUE       = "#1971c2"
PURPLE     = "#7048e8"
GRID       = "#eaecf4"
WHITE      = "#ffffff"

# ── типи кутів ───────────────────────────────────────────────────────────────
ANGLE_TYPES = [
    {"name": "Гострий",     "range": (1,  89),  "color": GREEN,  "icon": "📐"},
    {"name": "Прямий",      "range": (90,  90), "color": BLUE,   "icon": "⊾"},
    {"name": "Тупий",       "range": (91, 179), "color": ORANGE, "icon": "📏"},
    {"name": "Розгорнутий", "range": (180,180), "color": PURPLE, "icon": "↔"},
]

DRAW_TOLERANCE = 0 # точність влучання в 0 градусів

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

# ─────────────────────────────────────────────────────────────────────────────
class AngleTrainer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Тренажер: Вгадай Кут")
        self.attributes("-fullscreen", True)
        self.configure(bg=BG)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.target_deg = 0
        self.score = 0
        self.total = 0
        self.streak = 0
        self.phase = "build"  # 'build', 'classify', 'done'

        self.user_chosen_type = None

        self.update_idletasks()
        self.SW = self.winfo_screenwidth()
        self.SH = self.winfo_screenheight()

        self._build_ui()
        self._new_question()

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        SW, SH = self.SW, self.SH

        hdr = tk.Frame(self, bg=ACCENT, height=58)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="🎯  Вгадай Кут",
                 bg=ACCENT, fg=WHITE, font=("Segoe UI", 18, "bold")
                 ).place(x=24, rely=0.5, anchor="w")

        self.lbl_score = tk.Label(hdr, text="", bg=ACCENT, fg="#b8d0ff",
                                  font=("Segoe UI", 14, "bold"))
        self.lbl_score.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(hdr, text="ESC — вийти з повного екрана",
                 bg=ACCENT, fg="#8eaaff", font=("Segoe UI", 10)
                 ).place(relx=1.0, x=-18, rely=0.5, anchor="e")

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        self.CW = int(SW * 0.63)
        self.CH = SH - 58
        self.canvas = tk.Canvas(body, width=self.CW, height=self.CH,
                                bg=PANEL, highlightthickness=0)
        self.canvas.pack(side="left", fill="both")
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        self.RW = SW - self.CW
        right = tk.Frame(body, bg=BG, width=self.RW)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        pad = tk.Frame(right, bg=BG)
        pad.place(relx=0.5, rely=0.5, anchor="center", width=self.RW - 44)

        self.lbl_task = tk.Label(pad, text="", bg=BG, fg=TEXT,
                                 font=("Segoe UI", 17, "bold"),
                                 wraplength=self.RW - 60, justify="center")
        self.lbl_task.pack(pady=(0, 6))

        self.lbl_sub = tk.Label(pad, text="", bg=BG, fg=MUTED,
                                font=("Segoe UI", 12),
                                wraplength=self.RW - 60, justify="center")
        self.lbl_sub.pack(pady=(0, 20))

        self.btn_frame = tk.Frame(pad, bg=BG)
        self.btn_frame.pack(fill="x")

        self.buttons = {}
        for t in ANGLE_TYPES:
            btn = tk.Button(
                self.btn_frame,
                text=f"{t['icon']}  {t['name']}",
                bg=WHITE, fg=TEXT,
                font=("Segoe UI", 13, "bold"),
                relief="flat", bd=0, cursor="hand2", pady=13,
                highlightbackground=BORDER, highlightthickness=1,
                command=lambda n=t["name"]: self._on_classify(n)
            )
            btn.pack(fill="x", pady=5)
            self._bind_hover(btn)
            self.buttons[t["name"]] = btn

        self.lbl_result = tk.Label(pad, text="", bg=BG,
                                   font=("Segoe UI", 13, "bold"),
                                   wraplength=self.RW - 60, justify="center")
        self.lbl_result.pack(pady=(20, 6))

        self.btn_action = tk.Button(
            pad, text="",
            bg=ACCENT, fg=WHITE, font=("Segoe UI", 13, "bold"),
            relief="flat", bd=0, cursor="hand2", pady=13,
            command=self._on_action_button_click
        )
        self.btn_action.pack(fill="x", pady=4)

    def _bind_hover(self, btn):
        btn.bind("<Enter>", lambda e: btn.config(bg="#e8edf8") if btn["bg"] == WHITE else None)
        btn.bind("<Leave>", lambda e: btn.config(bg=WHITE) if btn["bg"] == "#e8edf8" else None)

    # ── новий ігровий цикл ────────────────────────────────────────────────────
    def _new_question(self):
        self.target_deg = rand_angle()
        self.phase = "build"
        self.user_chosen_type = None

        self.lbl_result.config(text="")
        self.btn_action.pack_forget()

        for btn in self.buttons.values():
            btn.config(bg=WHITE, fg=TEXT, state="normal")

        self.lbl_task.config(text=f"Побудуй кут {self.target_deg}°")
        self.lbl_sub.config(text="Натисни на дузі, щоб поставити промінь.\nМожна пробувати багато разів!")
        self._draw_circle_phase()
        self._update_score()

    # ── клік по канвасу (фаза побудови) ──────────────────────────────────────
    def _on_canvas_click(self, event):
        if self.phase != "build":
            return

        cx, cy = self.CW // 2, self.CH // 2 + 10
        R = self._R()
        dx, dy = event.x - cx, event.y - cy

        if abs(math.hypot(dx, dy) - R) > 28:
            return

        click_deg = math.degrees(math.atan2(-dy, dx)) % 360
        if click_deg > 180: return

        got = round(click_deg)
        build_ok = abs(got - self.target_deg) <= DRAW_TOLERANCE

        self._draw_circle_phase(user_deg=got, success=build_ok)

        if build_ok:
            self.phase = "classify"
            self.lbl_result.config(text=f"✅ Влучив! Чудова робота!", fg=GREEN)
            self.lbl_task.config(text=f"Кут {self.target_deg}° побудовано!")
            self.lbl_sub.config(text="Тепер вибери правильний тип кута\nі натисни кнопку, щоб перевірити.")
            self.btn_action.config(text="Перевірити тип кута")
            self.btn_action.pack(fill="x", pady=4)
        else:
            direction = "більше" if self.target_deg > got else "менше"
            self.lbl_result.config(text=f"❌ Спробуй ще! Потрібно {direction}.", fg=RED)

    # ── вибір типу кута (фаза класифікації) ───────────────────────────────────
    def _on_classify(self, name):
        if self.phase == "done":
            return
        self.user_chosen_type = name
        for n, btn in self.buttons.items():
            is_selected = (n == name)
            # ВИПРАВЛЕНО: Використовуємо новий колір для виділення
            btn.config(bg=SELECTION if is_selected else WHITE, fg=TEXT)

    # ── головна кнопка дії ──────────────────────────────────────────────────
    def _on_action_button_click(self):
        if self.phase == "classify":
            if self.user_chosen_type is None:
                self.lbl_result.config(text="Будь ласка, вибери тип кута", fg=ORANGE)
                return

            self.total += 1
            correct_type = classify(self.target_deg)["name"]
            classify_ok = (self.user_chosen_type == correct_type)

            if classify_ok:
                self.score += 1
                self.streak += 1
                s = f"  🔥×{self.streak}" if self.streak > 1 else ""
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

    # ── малювання ─────────────────────────────────────────────────────────────
    def _R(self):
        return int(min(self.CW, self.CH) * 0.34)

    def _draw_circle_phase(self, user_deg=None, success=None):
        c = self.canvas
        c.delete("all")
        CW, CH = self.CW, self.CH
        cx, cy = CW // 2, CH // 2 + 10
        R = self._R()
        self._grid(CW, CH)

        c.create_arc(cx-R, cy-R, cx+R, cy+R, start=0, extent=180, style="arc", outline=BORDER, width=3, dash=(8, 5))
        c.create_arc(cx-R, cy-R, cx+R, cy+R, start=180, extent=180, style="arc", outline=GRID, width=1)
        for a in range(0, 181, 30):
            ra = math.radians(a)
            c.create_line(cx+(R-12)*math.cos(ra), cy-(R-12)*math.sin(ra), cx+(R+12)*math.cos(ra), cy-(R+12)*math.sin(ra), fill=BORDER, width=2)
        c.create_line(cx, cy, cx+R, cy, fill=TEXT, width=3, arrow="last")

        if user_deg is not None:
            col = GREEN if success else RED
            ux = cx + R * math.cos(math.radians(user_deg))
            uy = cy - R * math.sin(math.radians(user_deg))
            dash = () if success else (8, 5)
            c.create_line(cx, cy, ux, uy, fill=col, width=3, dash=dash)
            c.create_oval(ux-9, uy-9, ux+9, uy+9, fill=col, outline="")

            # ВИПРАВЛЕНО: Додано підпис кута, який побудував учень
            c.create_text(ux, uy - 22, text=f"{user_deg}°",
                          fill=col, font=("Segoe UI", 12, "bold"))

        if success:
            ar = int(R * 0.30)
            td = self.target_deg
            if 0 < td <= 180:
                c.create_arc(cx-ar, cy-ar, cx+ar, cy+ar, start=0, extent=td, style="arc", outline=ORANGE, width=2)
            if td == 90:
                sq = 18
                c.create_rectangle(cx+2, cy-sq, cx+sq, cy-2, outline=BLUE, width=2)

        c.create_oval(cx-7, cy-7, cx+7, cy+7, fill=ACCENT, outline="")

    def _grid(self, CW, CH):
        c = self.canvas
        for x in range(0, CW, 40): c.create_line(x, 0, x, CH, fill=GRID)
        for y in range(0, CH, 40): c.create_line(0, y, CW, y, fill=GRID)

    def _update_score(self):
        pct = round(self.score / self.total * 100) if self.total else 0
        self.lbl_score.config(text=f"✓ {self.score} / {self.total}   ({pct}%)")

if __name__ == "__main__":
    app = AngleTrainer()
    app.mainloop()