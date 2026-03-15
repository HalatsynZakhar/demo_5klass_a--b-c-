"""
Демонстрація: § 25. Площа прямокутника і квадрата
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

UNIT_TO_MM = {"мм": 1, "см": 10, "дм": 100, "м": 1000, "км": 1000000}
AREA_UNIT_TO_MM2 = {"мм²": 1, "см²": 100, "дм²": 10000, "м²": 1000000, "ар": 100000000, "га": 10000000000, "км²": 1000000000000}
UNITS = ["мм", "см", "дм", "м", "км"]
AREA_UNITS = ["мм²", "см²", "дм²", "м²", "ар", "га", "км²"]


class AreaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Площа прямокутника і квадрата (§ 25)")
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
        self.show_concept_of_area()

    def _draw_right_angle(self, cv, x, y, size, corner):
        # corner: 'bottom_left', 'bottom_right', 'top_right', 'top_left'
        if corner == 'bottom_left':
            cv.create_line(x, y, x + size, y, fill=SKY, width=4)
            cv.create_line(x, y, x, y - size, fill=SKY, width=4)
        elif corner == 'bottom_right':
            cv.create_line(x, y, x - size, y, fill=SKY, width=4)
            cv.create_line(x, y, x, y - size, fill=SKY, width=4)
        elif corner == 'top_right':
            cv.create_line(x, y, x - size, y, fill=SKY, width=4)
            cv.create_line(x, y, x, y + size, fill=SKY, width=4)
        elif corner == 'top_left':
            cv.create_line(x, y, x + size, y, fill=SKY, width=4)
            cv.create_line(x, y, x, y + size, fill=SKY, width=4)

    def _build_ui(self):
        hdr = tk.Frame(self, bg=ACCENT, height=80)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(
            hdr,
            text="Площа прямокутника і квадрата (§ 25)",
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
        tk.Button(nav, text="1. Поняття про площу", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_concept_of_area).pack(side="left", padx=10)
        tk.Button(nav, text="2. Площа прямокутника", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_rectangle_area).pack(side="left", padx=10)
        tk.Button(nav, text="3. Площа квадрата", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_square_area).pack(side="left", padx=10)
        tk.Button(nav, text="4. Властивості площі", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_properties_of_area).pack(side="left", padx=10)
        tk.Button(nav, text="5. Одиниці вимірювання", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_unit_conversion).pack(side="left", padx=10)
        tk.Button(nav, text="6. Тренажер", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_trainer).pack(side="left", padx=10)

        self.main_area = tk.Frame(self, bg=BG)
        self.main_area.pack(fill="both", expand=True)

    def clear_main(self):
        for w in self.main_area.winfo_children():
            w.destroy()

    def _canvas_width(self, cv, fallback):
        cv.update_idletasks()
        w = cv.winfo_width()
        if w < 300:
            w = fallback
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

    def show_concept_of_area(self):
        self.clear_main()
        self.mode = "concept_of_area"
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)
        tk.Label(f, text="Поняття про площу фігури", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        text_content = """Одиницею вимірювання площі вважають площу одиничного квадрата (квадрата, сторона якого дорівнює \
одиниці довжини). Наприклад, якщо сторона квадрата дорівнює 1 см, то його площа 1 см².\n
Знайти площу фігури — означає дізнатися, скільки одиничних квадратів уміщується в цій фігурі. Якщо, \
наприклад, деяку фігуру можна розбити на m квадратів зі стороною 1 см, то її площа дорівнює m см²."""
        tk.Label(
            f,
            text=text_content,
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            justify="left",
            wraplength=self.SW - 200,
        ).pack(anchor="w", pady=(0, 25))
        cv = tk.Canvas(f, bg=WHITE, height=max(480, int(self.SH * 0.55)), bd=2, relief="ridge")
        cv.pack(fill="x", pady=25, padx=10)
        self.after(80, lambda: self._draw_area_concept_demo(cv))

    def _draw_area_concept_demo(self, cv):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())
        
        # Draw a larger square
        side = min(w, h) * 0.5
        x0, y0 = (w / 2) - (side * 1.2), (h - side) / 2
        
        cv.create_rectangle(x0, y0, x0 + side, y0 + side, outline=TEXT, width=3)
        cv.create_text(x0 + side/2, y0 - 20, text="1 см", font=("Segoe UI", 18), fill=TEXT)
        cv.create_text(x0 - 25, y0 + side/2, text="1 см", font=("Segoe UI", 18), fill=TEXT, angle=90)
        cv.create_text(x0 + side/2, y0 + side/2, text="1 см²", font=("Segoe UI", 28, "bold"), fill=INDIGO)

        # Draw a grid of smaller squares
        num_cols = 5
        num_rows = 4
        square_size = 50
        start_x = (w / 2) + (side * 0.2)
        start_y = (h - num_rows * square_size) / 2

        for row in range(num_rows):
            for col in range(num_cols):
                x1 = start_x + col * square_size
                y1 = start_y + row * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size
                cv.create_rectangle(x1, y1, x2, y2, outline=MUTED, width=1)
        
        cv.create_text(start_x + num_cols * square_size / 2, start_y - 20, text=f"Площа = {num_cols * num_rows} см²", font=("Segoe UI", 18, "bold"), fill=TEXT)


    def show_rectangle_area(self):
        self.clear_main()
        self.mode = "rectangle_area"
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)
        tk.Label(f, text="Формула площі прямокутника", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        text_content = """S — площа прямокутника, а і b — його довжина і ширина.\n\nЩоб знайти площу прямокутника, треба його довжину помножити на ширину.\nS = a • b\n\nЯкщо сторони прямокутника задано в метрах, то площу S отримаємо у квадратних метрах, якщо в сантиметрах, то \nплощу отримаємо у квадратних сантиметрах і т. д.\n\nЗадача 1. Знайти площу прямокутника зі сторонами завдовжки 1 дм і 8 см.\nРозв’язання. 1 дм = 10 см, тоді S = а • b = 10 • 8 = 80 (см²).\nВідповідь: 80 см²."""
        tk.Label(
            f,
            text=text_content,
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            justify="left",
            wraplength=self.SW - 240,
        ).pack(anchor="w", pady=(0, 25))
        cv = tk.Canvas(f, bg=WHITE, height=max(480, int(self.SH * 0.55)), bd=2, relief="ridge")
        cv.pack(fill="x", pady=25, padx=10)
        self.after(80, lambda: self._draw_rectangle_area_demo(cv, a=10, b=8, unit_a="см", unit_b="см"))


    def _draw_rectangle_area_demo(self, cv, a, b, unit_a, unit_b, is_trainer=False):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200 if not is_trainer else cv.winfo_width())
        h = int(cv.winfo_height())

        if is_trainer:
            rect_width = min(w * 0.8, 200) 
            rect_height = min(h * 0.6, 160) 
            font_size_sides = 14
            offset_sides_y = 15
            offset_sides_x = 15
            offset_y0 = 0
            angle_size = 15
        else: 
            rect_width = 300
            rect_height = 240
            font_size_sides = 18
            offset_sides_y = 25
            offset_sides_x = 30
            offset_y0 = 30
            angle_size = 25

        x0 = (w - rect_width) / 2
        y0 = (h - rect_height) / 2 - offset_y0

        cv.create_rectangle(x0, y0, x0 + rect_width, y0 + rect_height, outline=TEXT, width=3)
        self._draw_right_angle(cv, x0, y0 + rect_height, angle_size, 'bottom_left')
        self._draw_right_angle(cv, x0 + rect_width, y0 + rect_height, angle_size, 'bottom_right')
        self._draw_right_angle(cv, x0 + rect_width, y0, angle_size, 'top_right')
        self._draw_right_angle(cv, x0, y0, angle_size, 'top_left')

        cv.create_text(x0 + rect_width / 2, y0 + rect_height + offset_sides_y, text=f"a = {a} {unit_a}", font=("Segoe UI", font_size_sides, "bold"), fill=INDIGO)
        cv.create_text(x0 - offset_sides_x, y0 + rect_height / 2, text=f"b = {b} {unit_b}", font=("Segoe UI", font_size_sides, "bold"), fill=INDIGO, angle=90)
        
        if not is_trainer:
            cv.create_text(w / 2, y0 + rect_height / 2, text=f"S = a × b", font=("Segoe UI", 30, "bold"), fill=SKY, anchor="center")
            cv.create_text(w / 2, y0 + rect_height + 70, text=f"S = {a} × {b} = {a*b} {unit_a}²", font=("Segoe UI", 22, "bold"), fill=TEXT, anchor="center")


    def show_square_area(self):
        self.clear_main()
        self.mode = "square_area"
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)
        tk.Label(f, text="Формула площі квадрата", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        text_content = """Щоб знайти площу квадрата, треба довжину його сторони піднести до другого степеня, тобто піднести до квадрата.\nS = a²\n\nСаме тому, що площу квадрата знаходять за формулою S = a², число в другому степені називають квадратом.\n\nЗадача 2. Знайти площу квадрата зі стороною 2 см 5 мм.\nРозв’язання. 2 см 5 мм = 25 мм. Тоді S = a² = 25² = 25 • 25 = 625 (мм²).\nВідповідь: 625 мм²."""
        tk.Label(
            f,
            text=text_content,
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            justify="left",
            wraplength=self.SW - 240,
        ).pack(anchor="w", pady=(0, 40))
        cv = tk.Canvas(f, bg=WHITE, height=max(400, int(self.SH * 0.45)), bd=2, relief="ridge")
        cv.pack(fill="x", pady=30, padx=10)
        self.after(80, lambda: self._draw_square_area_demo(cv, a=25, unit="мм"))


    def _draw_square_area_demo(self, cv, a, unit, is_trainer=False):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())

        if is_trainer:
            side_len = min(w * 0.7, h * 0.7, 120) 
            font_size_sides = 14
            offset_sides_y = 15
            offset_sides_x = 15
            offset_y0 = 0
            angle_size = 15
        else:
            side_len = 250
            font_size_sides = 18
            offset_sides_y = 25
            offset_sides_x = 30
            offset_y0 = 30
            angle_size = 25

        x0 = (w - side_len) / 2
        y0 = (h - side_len) / 2 - offset_y0

        cv.create_rectangle(x0, y0, x0 + side_len, y0 + side_len, outline=TEXT, width=3)
        self._draw_right_angle(cv, x0, y0 + side_len, angle_size, 'bottom_left')
        self._draw_right_angle(cv, x0 + side_len, y0 + side_len, angle_size, 'bottom_right')
        self._draw_right_angle(cv, x0 + side_len, y0, angle_size, 'top_right')
        self._draw_right_angle(cv, x0, y0, angle_size, 'top_left')

        cv.create_text(x0 + side_len / 2, y0 + side_len + offset_sides_y, text=f"a = {a} {unit}", font=("Segoe UI", font_size_sides, "bold"), fill=INDIGO)
        cv.create_text(x0 - offset_sides_x, y0 + side_len / 2, text=f"a = {a} {unit}", font=("Segoe UI", font_size_sides, "bold"), fill=INDIGO, angle=90)
        if not is_trainer:
            cv.create_text(w / 2, y0 + side_len / 2, text=f"S = a²", font=("Segoe UI", 30, "bold"), fill=SKY, anchor="center")
            cv.create_text(w / 2, y0 + side_len + 70, text=f"S = {a}² = {a*a} {unit}²", font=("Segoe UI", 22, "bold"), fill=TEXT, anchor="center")


    def show_properties_of_area(self):
        self.clear_main()
        self.mode = "properties_of_area"
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)
        tk.Label(f, text="Властивості площі", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        text_content = """Нехай маємо прямокутник ABCD розміром 4 x 5 клітинок. Тоді його площа дорівнює 4 • 5 = 20 (клітинок).\nЛамана KLMN розбиває прямокутник ABCD на дві частини. Площа однієї з них — 12 клітинок, а іншої — 8 клітинок. Але 12 + 8 = 20, \
а це те саме значення, що й площа прямокутника ABCD.\n\nОтже, площа прямокутника дорівнює сумі площ його частин.\nПлоща фігури дорівнює сумі площ її частин."""
        tk.Label(
            f,
            text=text_content,
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            justify="left",
            wraplength=self.SW - 200,
        ).pack(anchor="w", pady=(0, 25))
        cv = tk.Canvas(f, bg=WHITE, height=max(480, int(self.SH * 0.55)), bd=2, relief="ridge")
        cv.pack(fill="x", pady=25, padx=10)
        self.after(80, lambda: self._draw_area_properties_demo(cv))

    def _draw_area_properties_demo(self, cv):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())

        # Dimensions for the overall rectangle
        total_width_units = 10
        total_height_units = 6
        unit_size = 40 # Pixels per unit

        total_rect_width = total_width_units * unit_size
        total_rect_height = total_height_units * unit_size

        start_x = (w - total_rect_width) / 2
        start_y = (h - total_rect_height) / 2

        # Draw the overall grid
        for r in range(total_height_units):
            for c in range(total_width_units):
                x1 = start_x + c * unit_size
                y1 = start_y + r * unit_size
                cv.create_rectangle(x1, y1, x1 + unit_size, y1 + unit_size, outline=MUTED, width=1)

        # Define split point (e.g., horizontally)
        split_height_units = 3 # Split into two parts, 3 units high and 3 units high

        # Part 1: Top rectangle
        part1_height = split_height_units * unit_size
        cv.create_rectangle(start_x, start_y, start_x + total_rect_width, start_y + part1_height, fill="#fee2e2")
        cv.create_rectangle(start_x, start_y, start_x + total_rect_width, start_y + part1_height, outline=RED, width=3)
        area1 = total_width_units * split_height_units
        cv.create_text(start_x + total_rect_width / 2, start_y + part1_height / 2, text=f"S1 = {total_width_units} × {split_height_units} = {area1}", font=("Segoe UI", 18, "bold"), fill=RED)
        cv.create_text(start_x + total_rect_width / 2, start_y + part1_height + 15, text=f"{total_width_units} од.", font=("Segoe UI", 14), fill=TEXT)
        cv.create_text(start_x - 15, start_y + part1_height / 2, text=f"{split_height_units} од.", font=("Segoe UI", 14), fill=TEXT, angle=90)


        # Part 2: Bottom rectangle
        part2_start_y = start_y + part1_height
        part2_height = (total_height_units - split_height_units) * unit_size
        cv.create_rectangle(start_x, part2_start_y, start_x + total_rect_width, part2_start_y + part2_height, fill="#e0f2fe")
        cv.create_rectangle(start_x, part2_start_y, start_x + total_rect_width, part2_start_y + part2_height, outline=INDIGO, width=3)
        area2 = total_width_units * (total_height_units - split_height_units)
        cv.create_text(start_x + total_rect_width / 2, part2_start_y + part2_height / 2, text=f"S2 = {total_width_units} × {total_height_units - split_height_units} = {area2}", font=("Segoe UI", 18, "bold"), fill=INDIGO)
        cv.create_text(start_x - 15, part2_start_y + part2_height / 2, text=f"{total_height_units - split_height_units} од.", font=("Segoe UI", 14), fill=TEXT, angle=90)


        # Total area
        total_area = area1 + area2
        cv.create_text(w / 2, start_y + total_rect_height + 40, text=f"S = S1 + S2 = {area1} + {area2} = {total_area} од².", font=("Segoe UI", 22, "bold"), fill=TEXT)



    def show_unit_conversion(self):
        self.clear_main()
        self.mode = "unit_conversion"
        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)
        tk.Label(f, text="Співвідношення між одиницями вимірювання площі", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        text_content = """Установимо співвідношення між одиницями вимірювання площі.\n1 дм² = 1 дм • 1 дм = 10 см • 10 см = 100 см².\nМіркуючи аналогічно, можна показати, що:\n1 м² = 100 дм² = 10 000 см².\n1 км² = 1 000 000 м².\nАр — це площа квадрата зі стороною 10 м: 1 а = 100 м².\nГектар — це площа квадрата зі стороною 100 м: 1 га = 10 000 м² = 100 а.\nОтже, 1 км² = 100 га."""
        tk.Label(
            f,
            text=text_content,
            font=("Segoe UI", 18),
            bg=BG,
            fg=MUTED,
            justify="left",
            wraplength=self.SW - 200,
        ).pack(anchor="w", pady=(0, 25))

        cv = tk.Canvas(f, bg=WHITE, height=max(480, int(self.SH * 0.55)), bd=2, relief="ridge")
        cv.pack(fill="x", pady=25, padx=10)
        self.after(80, lambda: self._draw_unit_conversion_demo(cv))

    def _draw_unit_conversion_demo(self, cv):
        cv.delete("all")
        w = self._canvas_width(cv, self.SW - 200)
        h = int(cv.winfo_height())

        # Draw 1 dm2 = 100 cm2 example
        dm_side = 200 # pixels for 1 dm
        cm_side = 20 # pixels for 1 cm
        
        x0 = (w - dm_side) / 2
        y0 = (h - dm_side) / 2 - 30

        cv.create_rectangle(x0, y0, x0 + dm_side, y0 + dm_side, outline=TEXT, width=3)
        cv.create_text(x0 + dm_side / 2, y0 - 25, text="1 дм", font=("Segoe UI", 18), fill=TEXT)
        cv.create_text(x0 - 30, y0 + dm_side / 2, text="1 дм", font=("Segoe UI", 18), fill=TEXT, angle=90)
        
        # Draw cm grid inside
        for i in range(1, 10):
            cv.create_line(x0 + i * cm_side, y0, x0 + i * cm_side, y0 + dm_side, fill=MUTED, dash=(2,2))
            cv.create_line(x0, y0 + i * cm_side, x0 + dm_side, y0 + i * cm_side, fill=MUTED, dash=(2,2))
        
        cv.create_text(w / 2, y0 + dm_side / 2, text="100 см²", font=("Segoe UI", 30, "bold"), fill=SKY, anchor="center")
        cv.create_text(w / 2, y0 + dm_side + 30, text="1 дм² = 100 см²", font=("Segoe UI", 22, "bold"), fill=TEXT, anchor="center")



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
        self.task_text = tk.Label(self.task_box, text="", font=("Segoe UI", 16, "bold"), bg=WHITE, fg=TEXT, justify="center", wraplength=LW - 200)
        self.task_text.pack(anchor="center", pady=(10,0))

        self.task_canvas = tk.Canvas(left, bg=WHITE, height=300, bd=2, relief="ridge")
        self.task_canvas.pack(pady=10, padx=20, fill="x")

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
                "• Площа прямокутника: S = a • b\n"
                "• Площа квадрата: S = a²\n\n"
                "--- Одиниці вимірювання ---\n"
                "• 1 см = 10 мм\n"
                "• 1 дм = 10 см = 100 мм\n"
                "• 1 м = 10 дм = 100 см = 1000 мм\n"
                "• 1 км = 1000 м\n\n"
                "--- Одиниці площі ---\n"
                "• 1 см² = 100 мм² (10мм * 10мм)\n"
                "• 1 дм² = 100 см² (10см * 10см)\n"
                "• 1 м² = 100 дм² (10дм * 10дм)\n"
                "• 1 ар (сотка) = 100 м² (10м * 10м)\n"
                "• 1 га = 100 ар = 10 000 м² (100м * 100м)\n"
                "• 1 км² = 100 га = 1 000 000 м² (1000м * 1000м)"
            ),
            font=("Segoe UI", 12),
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

        # Define task types: calculate area of rectangle, square, find side, unit conversion
        task_type = random.choice(["rect_area", "sq_area", "rect_side", "unit_convert"])
        
        if task_type == "rect_area":
            a = random.randint(5, 30)
            b = random.randint(5, 30)
            unit = random.choice(["см", "дм", "м"])
            area = a * b
            self.task = {"type": "rect_area", "ans": area, "unit": unit, "a": a, "b": b}
            self.task_text.config(text=f"Знайди площу прямокутника зі сторонами {a} {unit} і {b} {unit}.")
            self._draw_rectangle_area_demo(self.task_canvas, a, b, unit, unit, is_trainer=True)

        elif task_type == "sq_area":
            a = random.randint(5, 30)
            unit = random.choice(["см", "дм", "м"])
            area = a * a
            self.task = {"type": "sq_area", "ans": area, "unit": unit, "a": a}
            self.task_text.config(text=f"Знайди площу квадрата зі стороною {a} {unit}.")
            self._draw_square_area_demo(self.task_canvas, a, unit, is_trainer=True)
        
        elif task_type == "rect_side":
            side_a = random.randint(5, 25)
            side_b = random.randint(5, 25)
            area_val = side_a * side_b
            unit = random.choice(["см", "дм", "м"])
            self.task = {"type": "rect_side", "ans": side_b, "unit": unit, "S": area_val, "a": side_a}
            self.task_text.config(text=f"Площа прямокутника {area_val} {unit}². Одна сторона {side_a} {unit}. Знайди іншу сторону.")
            self._draw_rectangle_area_demo(self.task_canvas, side_a, "?", unit, unit, is_trainer=True)

        elif task_type == "unit_convert":
            while True:
                from_unit, to_unit = random.sample(AREA_UNITS, 2)
                value = random.randint(1, 100)
                
                val_in_mm2 = value * AREA_UNIT_TO_MM2[from_unit]
                
                if AREA_UNIT_TO_MM2[to_unit] == 0: continue
                if val_in_mm2 % AREA_UNIT_TO_MM2[to_unit] != 0: continue
                
                converted_value = val_in_mm2 // AREA_UNIT_TO_MM2[to_unit]
                if converted_value == 0: continue

                self.task = {"type": "unit_convert", "ans": converted_value, "from_val": value, "from_unit": from_unit, "to_unit": to_unit}
                self.task_text.config(text=f"Переведи: {value} {from_unit} = ? {to_unit}")
                break

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
            self.lbl_feedback.config(text=f"❌ Ні. Правильна відповідь: {self.task['ans']}", fg=RED)
            self.lbl_display.config(bg=RED_BG)
            self.btn_ok.pack_forget()
            self.btn_next.pack(side="left", padx=20)
        self.lbl_score.config(text=f"Рахунок: {self.score} / {self.total}")


if __name__ == "__main__":
    app = AreaApp()
    app.mainloop()
