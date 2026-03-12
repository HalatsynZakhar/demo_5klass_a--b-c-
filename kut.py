"""
Тренажер «Кути» — повноекранний, тільки миша, світла тема.
Два кроки:
  1. Classify — вибрати тип кута
  2. Draw     — побудувати кут на колі; можна тикати скільки завгодно разів
"""

import tkinter as tk
import math
import random

# ── світла палітра ────────────────────────────────────────────────────────────
BG      = "#f5f7fa"
PANEL   = "#ffffff"
ACCENT  = "#4361ee"
BORDER  = "#c8d0e0"
TEXT    = "#1a1a2e"
MUTED   = "#7b8ab8"
GREEN   = "#2d9e5f"
RED     = "#d7263d"
ORANGE  = "#e07b00"
BLUE    = "#1971c2"
PURPLE  = "#7048e8"
GRID    = "#eaecf4"
WHITE   = "#ffffff"

# ── типи кутів ───────────────────────────────────────────────────────────────
ANGLE_TYPES = [
    {"name": "Гострий",     "range": (1,  89),  "color": GREEN,  "icon": "📐"},
    {"name": "Прямий",      "range": (90,  90), "color": BLUE,   "icon": "⊾"},
    {"name": "Тупий",       "range": (91, 179), "color": ORANGE, "icon": "📏"},
    {"name": "Розгорнутий", "range": (180,180), "color": PURPLE, "icon": "↔"},
]

DRAW_TOLERANCE = 0

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

        self.target_deg = 0
        self.score      = 0
        self.total      = 0
        self.streak     = 0
        self.phase      = "classify"

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

        tk.Label(hdr, text="📐  Тренажер «Кути»",
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

        self.lbl_step = tk.Label(pad, text="", bg=BG, fg=MUTED,
                                 font=("Segoe UI", 11))
        self.lbl_step.pack(pady=(0, 2))

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
            lo, hi = t["range"]
            rng = f"{lo}°" if lo == hi else f"{lo}°–{hi}°"
            btn = tk.Button(
                self.btn_frame,
                text=f"{t['icon']}  {t['name']}   ({rng})",
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

        self.btn_next = tk.Button(
            pad, text="▶  Наступне питання",
            bg=ACCENT, fg=WHITE, font=("Segoe UI", 13, "bold"),
            relief="flat", bd=0, cursor="hand2", pady=13,
            command=self._next
        )
        self.btn_next.pack(fill="x", pady=4)
        self.btn_next.pack_forget()

    def _bind_hover(self, btn):
        btn.bind("<Enter>", lambda e: btn.config(bg="#e8edf8") if btn["state"] == "normal" else None)
        btn.bind("<Leave>", lambda e: btn.config(bg=WHITE)     if btn["state"] == "normal" else None)

    # ── нове питання ──────────────────────────────────────────────────────────
    def _new_question(self):
        self.target_deg = rand_angle()
        self.phase      = "classify"
        self.lbl_result.config(text="")
        self.btn_next.pack_forget()

        for btn in self.buttons.values():
            btn.config(bg=WHITE, fg=TEXT, state="normal")
        self.btn_frame.pack(fill="x")

        self.lbl_step.config(text="Крок 1 з 2")
        self.lbl_task.config(text="Який це тип кута?")
        self.lbl_sub.config(text="")
        self._draw_angle(self.target_deg)
        self._update_score()

    # ── класифікація ──────────────────────────────────────────────────────────
    def _on_classify(self, name):
        if self.phase != "classify":
            return

        correct = classify(self.target_deg)
        ok = (name == correct["name"])
        self.total += 1

        if ok:
            self.score  += 1
            self.streak += 1
            s = f"  🔥×{self.streak}" if self.streak > 1 else ""
            self.lbl_result.config(text=f"✅  Правильно!{s}", fg=GREEN)
        else:
            self.streak = 0
            self.lbl_result.config(text=f"❌  Ні. Це «{correct['name']}»", fg=RED)

        for n, btn in self.buttons.items():
            if n == correct["name"]:
                btn.config(bg=GREEN, fg=WHITE, state="disabled")
            elif n == name and not ok:
                btn.config(bg=RED, fg=WHITE, state="disabled")
            else:
                btn.config(state="disabled")

        self._update_score()
        self.phase = "draw"
        self.after(800, self._start_draw_phase)

    def _start_draw_phase(self):
        self.lbl_result.config(text="")
        self.btn_frame.pack_forget()
        self.lbl_step.config(text="Крок 2 з 2")
        self.lbl_task.config(text=f"Побудуй кут {self.target_deg}°")
        self.lbl_sub.config(text="Натисни на дузі — вкажи другий промінь.\nМожна спробувати кілька разів.")
        self._draw_circle_phase()

    # ── клік по канвасу (фаза побудови) ──────────────────────────────────────
    def _on_canvas_click(self, event):
        if self.phase != "draw":
            return

        cx, cy = self.CW // 2, self.CH // 2 + 10
        R = self._R()
        dx, dy = event.x - cx, event.y - cy

        if abs(math.hypot(dx, dy) - R) > 28:
            return

        click_deg = math.degrees(math.atan2(-dy, dx)) % 360
        if click_deg > 180:
            return

        got  = round(click_deg)   # точність до 1 градуса
        diff = abs(got - self.target_deg)

        if diff <= DRAW_TOLERANCE:
            # ── влучив ──────────────────────────────────────────────────────
            self.lbl_result.config(
                text=f"✅  Влучив! Поставив {got}°  (потрібно {self.target_deg}°)",
                fg=GREEN)
            self._draw_circle_phase(user_deg=got, success=True)
            self.phase = "done"
            self.btn_next.pack(fill="x", pady=4)
        else:
            # ── промах — пишемо чітко, даємо спробувати ще ─────────────────
            direction = "більше" if self.target_deg > got else "менше"
            self.lbl_result.config(
                text=f"❌  Поставив {got}° — не влучив.\nПотрібно {direction}. Спробуй ще!",
                fg=RED)
            self._draw_circle_phase(user_deg=got, success=False)
            # phase залишається "draw"

    # ── малювання ─────────────────────────────────────────────────────────────
    def _R(self):
        return int(min(self.CW, self.CH) * 0.34)

    def _draw_angle(self, deg):
        c = self.canvas
        c.delete("all")
        CW, CH = self.CW, self.CH
        cx, cy = CW // 2, CH // 2 + 10
        R = int(min(CW, CH) * 0.30)
        self._grid(CW, CH)

        rad = math.radians(deg)

        c.create_line(cx, cy, cx + R, cy, fill=TEXT, width=3, arrow="last")
        if deg != 0:
            x2 = cx + R * math.cos(rad)
            y2 = cy - R * math.sin(rad)
            c.create_line(cx, cy, x2, y2, fill=ACCENT, width=3, arrow="last")

        ar = int(R * 0.36)
        if 0 < deg < 180:
            c.create_arc(cx-ar, cy-ar, cx+ar, cy+ar,
                         start=0, extent=deg, style="arc", outline=ORANGE, width=2)
        elif deg == 180:
            c.create_line(cx - ar, cy, cx + ar, cy, fill=ORANGE, width=2)

        if deg == 90:
            sq = 20
            c.create_rectangle(cx+2, cy-sq, cx+sq, cy-2, outline=BLUE, width=2)

        lx = cx + (ar+28) * math.cos(math.radians(deg / 2))
        ly = cy - (ar+28) * math.sin(math.radians(deg / 2))
        c.create_text(lx, ly, text=f"{deg}°", fill=ORANGE, font=("Segoe UI", 14, "bold"))

        c.create_oval(cx-6, cy-6, cx+6, cy+6, fill=ACCENT, outline="")

    def _draw_circle_phase(self, user_deg=None, success=None):
        c = self.canvas
        c.delete("all")
        CW, CH = self.CW, self.CH
        cx, cy = CW // 2, CH // 2 + 10
        R = self._R()
        self._grid(CW, CH)

        # верхня дуга (активна зона для кліку)
        c.create_arc(cx-R, cy-R, cx+R, cy+R,
                     start=0, extent=180,
                     style="arc", outline=BORDER, width=3, dash=(8, 5))
        # нижня дуга (неактивна)
        c.create_arc(cx-R, cy-R, cx+R, cy+R,
                     start=180, extent=180,
                     style="arc", outline=GRID, width=1)

        # штрихи кожні 30° — без підписів (щоб не підказувати)
        for a in range(0, 181, 30):
            ra = math.radians(a)
            c.create_line(
                cx + (R-12)*math.cos(ra), cy - (R-12)*math.sin(ra),
                cx + (R+12)*math.cos(ra), cy - (R+12)*math.sin(ra),
                fill=BORDER, width=2)

        # перший промінь (0°)
        c.create_line(cx, cy, cx+R, cy, fill=TEXT, width=3, arrow="last")

        # промінь користувача
        if user_deg is not None:
            col  = GREEN if success else RED
            ux   = cx + R * math.cos(math.radians(user_deg))
            uy   = cy - R * math.sin(math.radians(user_deg))
            dash = () if success else (8, 5)
            c.create_line(cx, cy, ux, uy, fill=col, width=3, dash=dash)
            c.create_oval(ux-9, uy-9, ux+9, uy+9, fill=col, outline="")
            c.create_text(ux, uy-20, text=f"{user_deg}°",
                          fill=col, font=("Segoe UI", 12, "bold"))

            # після успіху показуємо дугу та підтвердження
            if success:
                ar = int(R * 0.30)
                td = self.target_deg
                if 0 < td < 180:
                    c.create_arc(cx-ar, cy-ar, cx+ar, cy+ar,
                                 start=0, extent=td,
                                 style="arc", outline=ORANGE, width=2)
                elif td == 180:
                    c.create_line(cx-ar, cy, cx+ar, cy, fill=ORANGE, width=2)
                if td == 90:
                    sq = 18
                    c.create_rectangle(cx+2, cy-sq, cx+sq, cy-2,
                                       outline=BLUE, width=2)
                lx = cx + (ar+26)*math.cos(math.radians(td/2))
                ly = cy - (ar+26)*math.sin(math.radians(td/2))
                c.create_text(lx, ly, text=f"{td}°",
                              fill=ORANGE, font=("Segoe UI", 13, "bold"))

        # вершина
        c.create_oval(cx-7, cy-7, cx+7, cy+7, fill=ACCENT, outline="")

        # підказка поки не відповів
        if user_deg is None:
            c.create_text(CW//2, CH - 30,
                          text="👆  Натисни на дузі, щоб вказати другий промінь",
                          fill=MUTED, font=("Segoe UI", 12))

    def _grid(self, CW, CH):
        c = self.canvas
        for x in range(0, CW, 40):
            c.create_line(x, 0, x, CH, fill=GRID)
        for y in range(0, CH, 40):
            c.create_line(0, y, CW, y, fill=GRID)

    def _next(self):
        self._new_question()

    def _update_score(self):
        pct = round(self.score / self.total * 100) if self.total else 0
        self.lbl_score.config(text=f"✓ {self.score} / {self.total}   ({pct}%)")


if __name__ == "__main__":
    app = AngleTrainer()
    app.mainloop()
