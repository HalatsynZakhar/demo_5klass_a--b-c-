import tkinter as tk
import random
import math

# ── Palette (unified with series) ────────────────────────────────────────────
BG = "#f0f4f8"
PANEL = "#ffffff"
BORDER = "#cbd5e1"
TEXT = "#0f172a"
MUTED = "#475569"
WHITE = "#ffffff"
BTN_NUM = "#e2e8f0"
HDR_BG = "#1d4ed8"
NAV_BG = "#1e3a5f"
NAV_FG = "#ffffff"
ACCENT = "#1d4ed8"
ACCENT2 = "#7c3aed"
GREEN = "#15803d"
GREEN_LT = "#dcfce7"
RED = "#b91c1c"
RED_LT = "#fee2e2"
ORANGE = "#b45309"
ORANGE_LT = "#fef3c7"
CARD_B = "#dbeafe"
CARD_V = "#ede9fe"
CARD_G = "#dcfce7"
CARD_Y = "#fef9c3"
TEAL = "#0f766e"
TEAL_LT = "#ccfbf1"

# ── Fonts (Optimized for 1080p Vertical Space) ───────────────────────────────
F_TITLE = ("Segoe UI", 22, "bold")
F_HEAD = ("Segoe UI", 18, "bold")
F_SUB = ("Segoe UI", 15, "bold")
F_BODY = ("Segoe UI", 13)
F_BODYB = ("Segoe UI", 13, "bold")
F_BIG = ("Segoe UI", 32, "bold") # Reduced from 40
F_BTN = ("Segoe UI", 13, "bold")
F_NAV = ("Segoe UI", 11, "bold")
F_SCORE = ("Segoe UI", 13, "bold")
F_FEED = ("Segoe UI", 12)
F_NUM = ("Segoe UI", 16, "bold") # Reduced from 18
F_SMALL = ("Segoe UI", 10)
F_FRAC = ("Segoe UI", 24, "bold") # Reduced from 26
F_FRAC_S = ("Segoe UI", 15, "bold")
F_FRAC_T = ("Segoe UI", 12, "bold")


# ── Helpers ───────────────────────────────────────────────────────────────────
def _darken(h, a=30):
    r = max(0, int(h[1:3], 16) - a)
    g = max(0, int(h[3:5], 16) - a)
    b = max(0, int(h[5:7], 16) - a)
    return f"#{r:02x}{g:02x}{b:02x}"


def mkbtn(parent, text, cmd, bg=ACCENT, fg=WHITE, font=F_BTN,
          w=12, h=1, px=6, py=4): # Reduced height and padding
    b = tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg,
                  font=font, width=w, height=h,
                  relief="flat", bd=0, cursor="hand2",
                  activebackground=bg, activeforeground=fg,
                  padx=px, pady=py)
    orig = bg
    b.bind("<Enter>", lambda e: b.config(bg=_darken(orig, 25)))
    b.bind("<Leave>", lambda e: b.config(bg=orig))
    return b


def hline(parent, color=BORDER):
    tk.Frame(parent, bg=color, height=2).pack(fill="x", pady=(4, 8))


def theory_card(parent, title, body, bg_c, fg_title=TEXT):
    f = tk.Frame(parent, bg=bg_c, padx=16, pady=10, # Reduced pady
                 highlightbackground=BORDER, highlightthickness=1)
    f.pack(fill="x", pady=5) # Reduced pady
    tk.Label(f, text=title, font=F_SUB, bg=bg_c, fg=fg_title,
             anchor="w").pack(fill="x")
    tk.Label(f, text=body, font=F_BODY, bg=bg_c, fg=TEXT,
             justify="left", wraplength=800, anchor="w").pack(
        fill="x", pady=(4, 0))
    return f


def frac(parent, n, d, bg=PANEL, size="big", color=ACCENT):
    """Visual fraction widget: n over d with horizontal bar."""
    sizes = {"big": F_FRAC, "small": F_FRAC_S, "tiny": F_FRAC_T}
    widths = {"big": 36, "small": 28, "tiny": 20}
    fn = sizes.get(size, F_FRAC_S)
    w = widths.get(size, 28)
    f = tk.Frame(parent, bg=bg)
    tk.Label(f, text=str(n), font=fn, bg=bg, fg=color).pack()
    tk.Frame(f, bg=color, height=2, width=w).pack(pady=1)
    tk.Label(f, text=str(d), font=fn, bg=bg, fg=color).pack()
    return f


def inline_row(parent, bg, *items):
    row = tk.Frame(parent, bg=bg)
    for item in items:
        if item[0] == "text":
            tk.Label(row, text=item[1], font=F_BODY, bg=bg, fg=TEXT).pack(side="left")
        elif item[0] == "text_b":
            tk.Label(row, text=item[1], font=F_BODYB, bg=bg, fg=TEXT).pack(side="left")
        elif item[0] == "text_c":
            tk.Label(row, text=item[1], font=F_BODY, bg=bg, fg=item[2]).pack(side="left")
        elif item[0] == "frac":
            frac(row, item[1], item[2], bg, "small").pack(side="left", padx=5)
        elif item[0] == "frac_big":
            frac(row, item[1], item[2], bg, "big").pack(side="left", padx=6)
        elif item[0] == "frac_tiny":
            frac(row, item[1], item[2], bg, "tiny").pack(side="left", padx=3)
    return row


# ── Numpad (More compact) ─────────────────────────────────────────────────────
def build_numpad(parent, key_fn, bg=BG):
    np = tk.Frame(parent, bg=bg)
    for row_chars in [("7", "8", "9"), ("4", "5", "6"), ("1", "2", "3"), ("C", "0", "⌫")]:
        rf = tk.Frame(np, bg=bg)
        rf.pack(pady=2) # Reduced from 4
        for ch in row_chars:
            if ch.isdigit():
                bc, fc = BTN_NUM, TEXT
            elif ch == "C":
                bc, fc = RED_LT, RED
            else:
                bc, fc = CARD_V, ACCENT2
            b = tk.Button(rf, text=ch, font=F_NUM, width=3, height=1,
                          bg=bc, fg=fc, relief="flat", cursor="hand2",
                          command=lambda c=ch: key_fn(c))
            b.pack(side="left", padx=4) # Reduced from 5
            orig = bc
            b.bind("<Enter>", lambda e, x=b, o=orig: x.config(bg=_darken(o, 18)))
            b.bind("<Leave>", lambda e, x=b, o=orig: x.config(bg=o))
    return np


# ══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("§ 34. Дріб як частка двох натуральних чисел")
        self.configure(bg=BG)
        self.geometry("1024x768")
        self.minsize(800, 600)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.current_frame = None
        self.mode = None

        self.t1_a = self.t1_b = 0
        self.t1_input = ""
        self.t1_which = "num"
        self.t1_entered_num = ""
        self.t1_score = self.t1_attempts = 0

        self.t2_a = self.t2_b = 0
        self.t2_input = ""
        self.t2_score = self.t2_attempts = 0

        self.t3_n = self.t3_b = self.t3_ans = 0
        self.t3_input = ""
        self.t3_score = self.t3_attempts = 0

        self._build_chrome()
        self.show_main_menu()

    # ── Chrome ────────────────────────────────────────────────────────────────
    def _build_chrome(self):
        hdr = tk.Frame(self, bg=HDR_BG, height=45) # Reduced from 50
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="§ 34. Дріб як частка двох натуральних чисел",
                 bg=HDR_BG, fg=WHITE,
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=20)
        mkbtn(hdr, "✕  Вийти", self.destroy, bg="#b91c1c",
              font=("Segoe UI", 11, "bold"), w=8, h=1).pack(
            side="right", padx=14, pady=6)

        nav = tk.Frame(self, bg=NAV_BG, height=40) # Reduced from 45
        nav.pack(fill="x")
        nav.pack_propagate(False)

        for label, cmd in [
            ("🏠  Меню", self.show_main_menu),
            ("📖  Теорія", self.show_theory),
            ("🎯  Ділення → дріб", self.show_trainer_1),
            ("🎯  Дріб → значення", self.show_trainer_2),
            ("🎯  Число → дріб", self.show_trainer_3),
        ]:
            b = tk.Button(nav, text=label, command=cmd,
                          bg=NAV_BG, fg=NAV_FG, font=F_NAV,
                          relief="flat", bd=0, cursor="hand2",
                          activebackground=ACCENT, activeforeground=WHITE,
                          padx=10, pady=5)
            b.pack(side="left")
            b.bind("<Enter>", lambda e, x=b: x.config(bg=ACCENT))
            b.bind("<Leave>", lambda e, x=b: x.config(bg=NAV_BG))

        self.main_area = tk.Frame(self, bg=BG)
        self.main_area.pack(fill="both", expand=True)

    def clear_main(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.unbind_all("<MouseWheel>")
        self.unbind_all("<Button-4>")
        self.unbind_all("<Button-5>")
        self.current_frame = tk.Frame(self.main_area, bg=BG)
        self.current_frame.pack(expand=True, fill="both")

    def _scroll_page(self):
        sc = tk.Canvas(self.current_frame, bg=BG, highlightthickness=0)
        vsb = tk.Scrollbar(self.current_frame, orient="vertical", command=sc.yview)
        sc.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        sc.pack(side="left", fill="both", expand=True)
        outer = tk.Frame(sc, bg=BG)
        win = sc.create_window((0, 0), window=outer, anchor="nw")

        outer.bind("<Configure>", lambda e: sc.configure(scrollregion=sc.bbox("all")))
        sc.bind("<Configure>", lambda e: sc.itemconfig(win, width=e.width))

        def _on_mousewheel(event):
            try:
                if event.num == 4 or event.delta > 0:
                    sc.yview_scroll(-1, "units")
                elif event.num == 5 or event.delta < 0:
                    sc.yview_scroll(1, "units")
            except Exception:
                pass

        self.bind_all("<MouseWheel>", _on_mousewheel)
        self.bind_all("<Button-4>", _on_mousewheel)
        self.bind_all("<Button-5>", _on_mousewheel)

        p = tk.Frame(outer, bg=BG)
        p.pack(fill="both", expand=True, padx=20, pady=10) # Reduced pady from 20 to 10
        return p

    # ══════════════════════════════════════════════════════════════════════════
    # MAIN MENU
    # ══════════════════════════════════════════════════════════════════════════
    def show_main_menu(self):
        self.clear_main()
        self.mode = "menu"
        p = self._scroll_page()

        center = tk.Frame(p, bg=BG)
        center.pack(expand=True, pady=(10, 0)) # Reduced pady

        tk.Label(center, text="Дріб як частка",
                 font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 2))
        tk.Label(center, text="двох натуральних чисел   §34",
                 font=("Segoe UI", 16), bg=BG, fg=ACCENT).pack(pady=(0, 20))

        cards = [
            ("📖", "Теорія", CARD_B, ACCENT, self.show_theory),
            ("🎯", "Ділення\n→ дріб", CARD_G, GREEN, self.show_trainer_1),
            ("🎯", "Дріб\n→ значення", CARD_V, ACCENT2, self.show_trainer_2),
            ("🎯", "Число\n→ дріб", CARD_Y, ORANGE, self.show_trainer_3),
        ]

        row1 = tk.Frame(center, bg=BG)
        row1.pack(pady=4)
        row2 = tk.Frame(center, bg=BG)
        row2.pack(pady=4)

        for i, (icon, title, bg_c, fg_c, cmd) in enumerate(cards):
            r = row1 if i < 2 else row2
            c = tk.Frame(r, bg=bg_c, width=180, height=140, # Reduced width/height
                         highlightbackground=BORDER, highlightthickness=2)
            c.pack(side="left", padx=10)
            c.pack_propagate(False)
            tk.Label(c, text=icon, font=("Segoe UI", 28),
                     bg=bg_c, fg=fg_c).pack(pady=(12, 2))
            tk.Label(c, text=title, font=("Segoe UI", 12, "bold"),
                     bg=bg_c, fg=fg_c, justify="center").pack()
            orig = bg_c
            for w in [c] + list(c.winfo_children()):
                w.bind("<Button-1>", lambda e, f=cmd: f())
            c.bind("<Enter>", lambda e, x=c, col=orig: x.config(bg=_darken(col, 12)))
            c.bind("<Leave>", lambda e, x=c, col=orig: x.config(bg=col))

        tk.Label(center, text="Натисніть на картку або скористайтесь меню зверху",
                 font=F_SMALL, bg=BG, fg=MUTED).pack(pady=15)

    # ══════════════════════════════════════════════════════════════════════════
    # THEORY (General adjustments)
    # ══════════════════════════════════════════════════════════════════════════
    def show_theory(self):
        self.clear_main()
        self.mode = "theory"
        p = self._scroll_page()

        tk.Label(p, text="Дріб як частка двох натуральних чисел",
                 font=F_TITLE, bg=BG, fg=TEXT).pack(anchor="w")
        hline(p, ACCENT)

        core_f = tk.Frame(p, bg=CARD_B, padx=22, pady=12,
                          highlightbackground=ACCENT, highlightthickness=2)
        core_f.pack(fill="x", pady=6)
        tk.Label(core_f, text="📌  Головна ідея",
                 font=F_SUB, bg=CARD_B, fg=ACCENT).pack(anchor="w")

        r1 = inline_row(core_f, CARD_B,
                        ("text", "Дріб — це результат ділення двох натуральних чисел:   "))
        r1.pack(anchor="w", pady=(6, 2))

        r2 = inline_row(core_f, CARD_B,
                        ("frac_big", "a", "b"),
                        ("text_c", "  =  a  :  b", ACCENT))
        r2.pack(anchor="w", pady=2)

        r3 = inline_row(core_f, CARD_B,
                        ("text", "І навпаки,   a  :  b  =  "),
                        ("frac_big", "a", "b"))
        r3.pack(anchor="w", pady=(2, 6))

        tk.Label(core_f,
                 text="Значення дробу дорівнює частці від ділення чисельника на знаменник.",
                 font=F_BODYB, bg=CARD_B, fg=TEXT).pack(anchor="w")

        # ... (rest of theory frames adjusted for tighter padding)
        story_f = tk.Frame(p, bg=PANEL, padx=22, pady=12,
                           highlightbackground=BORDER, highlightthickness=1)
        story_f.pack(fill="x", pady=6)
        tk.Label(story_f, text="🍎  Задача-казка: 3 яблука ÷ 4 дітей",
                 font=F_BODYB, bg=PANEL, fg=TEXT).pack(anchor="w", pady=(0, 6))
        tk.Label(story_f,
                 text="Число 3 не ділиться націло на 4. Поділимо кожне яблуко на 4 рівні частини → 12 четвертин.\n"
                      "Дамо кожній дитині 3 таких частини.",
                 font=F_BODY, bg=PANEL, fg=TEXT, justify="left", wraplength=800).pack(anchor="w")

        res_row = inline_row(story_f, PANEL,
                             ("text", "Кожна дитина отримала  "),
                             ("frac_big", 3, 4),
                             ("text", "  яблука   →   3  :  4  =  "),
                             ("frac_big", 3, 4))
        res_row.pack(anchor="w", pady=6)

        theory_card(p, "💡  Запам'ятай",
                    "a : b  =  дріб a/b       (ділення можна записати дробом)\n"
                    "дріб a/b  =  a : b       (дріб — це ділення чисельника на знаменник)\n\n"
                    "Якщо ділиться без остачі → натуральне число. Якщо ні → залишається дробом.",
                    "#f1f5f9", MUTED)

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER 1 (Vertical layout optimization)
    # ══════════════════════════════════════════════════════════════════════════
    def show_trainer_1(self):
        self.clear_main()
        self.mode = "trainer1"

        cf = self.current_frame
        sbar = tk.Frame(cf, bg=PANEL, height=45,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.t1_score_lbl = tk.Label(sbar,
                                     text=self._t1_score_text(), font=F_SCORE, bg=PANEL, fg=GREEN)
        self.t1_score_lbl.pack(side="left", padx=20)
        
        frm_f = tk.Frame(sbar, bg=PANEL)
        frm_f.pack(side="right", padx=15)
        inline_row(frm_f, PANEL,
                   ("text_c", "a : b = ", MUTED),
                   ("frac", "a", "b")).pack(side="left")

        p = self._scroll_page()
        center = tk.Frame(p, bg=BG)
        center.pack(expand=True, pady=0) # No pady here

        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=20, pady=10) # Heavily reduced pady
        task_f.pack(pady=(5, 5))
        
        self.t1_task_lbl = tk.Label(task_f, text="",
                                    font=F_BIG, bg=PANEL, fg=ACCENT)
        self.t1_task_lbl.pack()

        ans_f = tk.Frame(center, bg=PANEL, padx=15, pady=8,
                         highlightbackground=BORDER, highlightthickness=1)
        ans_f.pack(pady=4)

        frac_build = tk.Frame(ans_f, bg=PANEL)
        frac_build.pack()

        self.t1_num_box = tk.Frame(frac_build, bg=BTN_NUM,
                                   highlightbackground=ACCENT,
                                   highlightthickness=2,
                                   width=60, height=40)
        self.t1_num_box.pack()
        self.t1_num_box.pack_propagate(False)
        self.t1_num_display = tk.Label(self.t1_num_box, text="?",
                                       font=F_FRAC, bg=BTN_NUM, fg=ACCENT)
        self.t1_num_display.pack(expand=True)

        tk.Frame(frac_build, bg=ACCENT, height=2, width=60).pack(pady=2)

        self.t1_den_box = tk.Frame(frac_build, bg=BTN_NUM,
                                   highlightbackground=BORDER,
                                   highlightthickness=1,
                                   width=60, height=40)
        self.t1_den_box.pack()
        self.t1_den_box.pack_propagate(False)
        self.t1_den_display = tk.Label(self.t1_den_box, text="?",
                                       font=F_FRAC, bg=BTN_NUM, fg=MUTED)
        self.t1_den_display.pack(expand=True)

        self.t1_field_lbl = tk.Label(center, text="",
                                     font=F_BODYB, bg=BG, fg=ACCENT)
        self.t1_field_lbl.pack(pady=2)

        self.t1_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                    bg=BG, fg=ORANGE,
                                    wraplength=600, justify="center")
        self.t1_feed_lbl.pack(pady=2)

        build_numpad(center, self._t1_key).pack(pady=4)

        act = tk.Frame(center, bg=BG)
        act.pack(pady=4)
        self.t1_check_btn = mkbtn(act, "✔ Перевірити", self._t1_check,
                                  bg=GREEN, w=14, h=1)
        self.t1_check_btn.pack(side="left", padx=10)
        mkbtn(act, "▶ Наступне", self._t1_new,
              bg=ACCENT, w=12, h=1).pack(side="left", padx=10)

        self._t1_new()

    def _t1_score_text(self):
        return f"Правильно: {self.t1_score} / {self.t1_attempts}"

    def _t1_new(self):
        self.t1_a = random.randint(1, 20)
        self.t1_b = random.randint(2, 15)
        while self.t1_a == self.t1_b:
            self.t1_a = random.randint(1, 20)
        self.t1_which = "num"
        self.t1_input = ""
        self.t1_entered_num = ""
        self.t1_attempts += 1

        if self.t1_task_lbl:
            self.t1_task_lbl.config(text=f"{self.t1_a}  :  {self.t1_b}")
        if self.t1_num_display:
            self.t1_num_display.config(text="?", fg=ACCENT)
        if self.t1_den_display:
            self.t1_den_display.config(text="?", fg=MUTED)
        if self.t1_num_box:
            self.t1_num_box.config(highlightbackground=ACCENT, highlightthickness=3, bg=BTN_NUM)
            self.t1_num_display.config(bg=BTN_NUM)
        if self.t1_den_box:
            self.t1_den_box.config(highlightbackground=BORDER, highlightthickness=1, bg=BTN_NUM)
            self.t1_den_display.config(bg=BTN_NUM)
        if self.t1_field_lbl:
            self.t1_field_lbl.config(text="▲ Вводиш ЧИСЕЛЬНИК", fg=ACCENT)
        if self.t1_feed_lbl:
            self.t1_feed_lbl.config(text="")
        if self.t1_check_btn:
            self.t1_check_btn.config(state="normal", bg=GREEN)
        if self.t1_score_lbl:
            self.t1_score_lbl.config(text=self._t1_score_text())

    def _t1_key(self, ch):
        if ch.isdigit():
            if len(self.t1_input) < 4:
                self.t1_input += ch
        elif ch == "⌫":
            self.t1_input = self.t1_input[:-1]
        elif ch == "C":
            self.t1_input = ""
        disp = self.t1_num_display if self.t1_which == "num" else self.t1_den_display
        if disp:
            disp.config(text=self.t1_input if self.t1_input else "?")

    def _t1_check(self):
        if not self.t1_input.strip():
            if self.t1_feed_lbl:
                self.t1_feed_lbl.config(text="⚠️ Введіть число!", fg=ORANGE)
            return
        val = int(self.t1_input)

        if self.t1_which == "num":
            if val == self.t1_a:
                self.t1_entered_num = str(val)
                self.t1_which = "den"
                self.t1_input = ""
                if self.t1_num_display:
                    self.t1_num_display.config(text=str(val), fg=GREEN)
                if self.t1_num_box:
                    self.t1_num_box.config(highlightbackground=GREEN, bg=GREEN_LT)
                    self.t1_num_display.config(bg=GREEN_LT)
                if self.t1_den_box:
                    self.t1_den_box.config(highlightbackground=ACCENT2, highlightthickness=3, bg=BTN_NUM)
                    self.t1_den_display.config(bg=BTN_NUM, fg=ACCENT2)
                if self.t1_field_lbl:
                    self.t1_field_lbl.config(
                        text=f"✅ Вірно! Тепер ЗНАМЕННИК ▼", fg=GREEN)
                if self.t1_feed_lbl:
                    self.t1_feed_lbl.config(text="")
            else:
                if self.t1_feed_lbl:
                    self.t1_feed_lbl.config(
                        text=f"❌ Чисельник = ліве число", fg=RED)
        else:
            if val == self.t1_b:
                self.t1_score += 1
                if self.t1_den_display:
                    self.t1_den_display.config(text=str(val), fg=GREEN)
                if self.t1_den_box:
                    self.t1_den_box.config(highlightbackground=GREEN, bg=GREEN_LT)
                    self.t1_den_display.config(bg=GREEN_LT)
                if self.t1_field_lbl:
                    self.t1_field_lbl.config(text="", fg=TEXT)
                if self.t1_feed_lbl:
                    g = math.gcd(self.t1_a, self.t1_b)
                    simp = f" (спрощено: {self.t1_a // g}/{self.t1_b // g})" if g > 1 else ""
                    self.t1_feed_lbl.config(
                        text=f"🎉 Чудово! {self.t1_a} : {self.t1_b} = {self.t1_a}/{self.t1_b}{simp}", fg=GREEN)
                if self.t1_check_btn:
                    self.t1_check_btn.config(state="disabled", bg=BTN_NUM)
            else:
                if self.t1_feed_lbl:
                    self.t1_feed_lbl.config(
                        text=f"❌ Знаменник = праве число", fg=RED)

        self.t1_input = ""
        disp = self.t1_num_display if self.t1_which == "num" else self.t1_den_display
        if disp and not disp.cget("text").replace("?", "").strip():
            disp.config(text="?")
        if self.t1_score_lbl:
            self.t1_score_lbl.config(text=self._t1_score_text())

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER 2 (Optimized)
    # ══════════════════════════════════════════════════════════════════════════
    def show_trainer_2(self):
        self.clear_main()
        self.mode = "trainer2"

        cf = self.current_frame
        sbar = tk.Frame(cf, bg=PANEL, height=45,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.t2_score_lbl = tk.Label(sbar,
                                     text=self._t2_score_text(), font=F_SCORE, bg=PANEL, fg=GREEN)
        self.t2_score_lbl.pack(side="left", padx=20)

        p = self._scroll_page()
        center = tk.Frame(p, bg=BG)
        center.pack(expand=True, pady=0)

        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=20, pady=8)
        task_f.pack(pady=4)

        self.t2_frac_frame = tk.Frame(task_f, bg=PANEL)
        self.t2_frac_frame.pack()

        self.t2_type_lbl = tk.Label(task_f, text="", font=F_SMALL,
                                    bg=PANEL, fg=MUTED)
        self.t2_type_lbl.pack()

        inp_f = tk.Frame(center, bg=BTN_NUM,
                         highlightbackground=ACCENT, highlightthickness=2,
                         padx=10, pady=4)
        inp_f.pack(pady=4)
        tk.Label(inp_f, text="Відповідь:", font=F_BODYB,
                 bg=BTN_NUM, fg=MUTED).pack(side="left")
        self.t2_inp_lbl = tk.Label(inp_f, text="",
                                   font=("Segoe UI", 28, "bold"),
                                   bg=BTN_NUM, fg=ACCENT, width=5)
        self.t2_inp_lbl.pack(side="left", padx=10)

        self.t2_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                    bg=BG, fg=ORANGE,
                                    wraplength=600, justify="center")
        self.t2_feed_lbl.pack(pady=2)

        build_numpad(center, self._t2_key).pack(pady=4)

        act = tk.Frame(center, bg=BG)
        act.pack(pady=4)
        self.t2_check_btn = mkbtn(act, "✔ Перевірити", self._t2_check,
                                  bg=GREEN, w=14, h=1)
        self.t2_check_btn.pack(side="left", padx=10)
        mkbtn(act, "▶ Наступне", self._t2_new,
              bg=ACCENT, w=12, h=1).pack(side="left", padx=10)

        self._t2_new()

    def _t2_score_text(self):
        return f"Правильно: {self.t2_score} / {self.t2_attempts}"

    def _t2_new(self):
        if random.random() < 0.6:
            self.t2_b = random.choice([2, 3, 4, 5, 6, 8, 10])
            self.t2_a = self.t2_b * random.randint(1, 12)
        else:
            self.t2_b = random.choice([3, 5, 7, 8, 9])
            self.t2_a = random.randint(1, self.t2_b * 3)
            while self.t2_a % self.t2_b == 0:
                self.t2_a = random.randint(1, self.t2_b * 3)

        self.t2_input = ""
        self.t2_attempts += 1

        for w in self.t2_frac_frame.winfo_children():
            w.destroy()
        frac(self.t2_frac_frame, self.t2_a, self.t2_b, PANEL, "big").pack()

        whole = (self.t2_a % self.t2_b == 0)
        if self.t2_type_lbl:
            if whole:
                self.t2_type_lbl.config(text=f"({self.t2_a} ÷ {self.t2_b} — натуральне)", fg=GREEN)
            else:
                self.t2_type_lbl.config(text=f"({self.t2_a} ÷ {self.t2_b} — дріб)", fg=ORANGE)

        if self.t2_inp_lbl:   self.t2_inp_lbl.config(text="", fg=ACCENT)
        if self.t2_feed_lbl:  self.t2_feed_lbl.config(text="")
        if self.t2_check_btn: self.t2_check_btn.config(state="normal", bg=GREEN)
        if self.t2_score_lbl: self.t2_score_lbl.config(text=self._t2_score_text())

    def _t2_key(self, ch):
        if ch.isdigit():
            if len(self.t2_input) < 5: self.t2_input += ch
        elif ch == "⌫":
            self.t2_input = self.t2_input[:-1]
        elif ch == "C":
            self.t2_input = ""
        if self.t2_inp_lbl: self.t2_inp_lbl.config(text=self.t2_input)

    def _t2_check(self):
        if not self.t2_input.strip():
            if self.t2_feed_lbl:
                self.t2_feed_lbl.config(text="⚠️ Введіть відповідь!", fg=ORANGE)
            return
        val = int(self.t2_input)
        self.t2_input = ""
        if self.t2_inp_lbl: self.t2_inp_lbl.config(text="")

        a, b = self.t2_a, self.t2_b
        whole = (a % b == 0)
        g = math.gcd(a, b)

        if whole:
            correct = a // b
            if val == correct:
                self.t2_score += 1
                if self.t2_feed_lbl:
                    self.t2_feed_lbl.config(text=f"🎉 Вірно! {a} ÷ {b} = {correct}", fg=GREEN)
                if self.t2_inp_lbl: self.t2_inp_lbl.config(fg=GREEN)
                if self.t2_check_btn: self.t2_check_btn.config(state="disabled", bg=BTN_NUM)
            else:
                if self.t2_feed_lbl:
                    self.t2_feed_lbl.config(text=f"❌ Не вірно. {a} ÷ {b} = ?", fg=RED)
        else:
            sn = a // g
            if val in (a, sn):
                self.t2_score += 1
                note = f" = {sn}/{b // g}" if g > 1 else ""
                if self.t2_feed_lbl:
                    self.t2_feed_lbl.config(text=f"🎉 Вірно! Лишається {a}/{b}{note}", fg=GREEN)
                if self.t2_inp_lbl: self.t2_inp_lbl.config(fg=GREEN)
                if self.t2_check_btn: self.t2_check_btn.config(state="disabled", bg=BTN_NUM)
            else:
                if self.t2_feed_lbl:
                    self.t2_feed_lbl.config(text=f"❌ Не вірно. Це не ділиться націло.", fg=RED)

        if self.t2_score_lbl:
            self.t2_score_lbl.config(text=self._t2_score_text())

    # ══════════════════════════════════════════════════════════════════════════
    # TRAINER 3 (Optimized)
    # ══════════════════════════════════════════════════════════════════════════
    def show_trainer_3(self):
        self.clear_main()
        self.mode = "trainer3"

        cf = self.current_frame
        sbar = tk.Frame(cf, bg=PANEL, height=45,
                        highlightbackground=BORDER, highlightthickness=1)
        sbar.pack(fill="x")
        sbar.pack_propagate(False)
        self.t3_score_lbl = tk.Label(sbar,
                                     text=self._t3_score_text(), font=F_SCORE, bg=PANEL, fg=GREEN)
        self.t3_score_lbl.pack(side="left", padx=20)

        p = self._scroll_page()
        center = tk.Frame(p, bg=BG)
        center.pack(expand=True, pady=0)

        task_f = tk.Frame(center, bg=PANEL,
                          highlightbackground=BORDER, highlightthickness=1,
                          padx=20, pady=8)
        task_f.pack(pady=4)

        self.t3_task_row = tk.Frame(task_f, bg=PANEL)
        self.t3_task_row.pack()

        ans_f = tk.Frame(center, bg=PANEL, padx=15, pady=8,
                         highlightbackground=BORDER, highlightthickness=1)
        ans_f.pack(pady=4)

        self.t3_frac_display = tk.Frame(ans_f, bg=PANEL)
        self.t3_frac_display.pack()

        inp_f = tk.Frame(center, bg=BTN_NUM,
                         highlightbackground=ORANGE, highlightthickness=2,
                         padx=10, pady=4)
        inp_f.pack(pady=4)
        tk.Label(inp_f, text="a =", font=F_BODYB, bg=BTN_NUM, fg=MUTED).pack(side="left")
        self.t3_inp_lbl = tk.Label(inp_f, text="",
                                   font=("Segoe UI", 28, "bold"),
                                   bg=BTN_NUM, fg=ORANGE, width=4)
        self.t3_inp_lbl.pack(side="left", padx=10)

        self.t3_feed_lbl = tk.Label(center, text="", font=F_FEED,
                                    bg=BG, fg=ORANGE,
                                    wraplength=600, justify="center")
        self.t3_feed_lbl.pack(pady=2)

        build_numpad(center, self._t3_key).pack(pady=4)

        act = tk.Frame(center, bg=BG)
        act.pack(pady=4)
        self.t3_check_btn = mkbtn(act, "✔ Перевірити", self._t3_check,
                                  bg=GREEN, w=14, h=1)
        self.t3_check_btn.pack(side="left", padx=10)
        mkbtn(act, "▶ Наступне", self._t3_new,
              bg=ORANGE, w=12, h=1).pack(side="left", padx=10)

        self._t3_new()

    def _t3_score_text(self):
        return f"Правильно: {self.t3_score} / {self.t3_attempts}"

    def _t3_new(self):
        self.t3_n = random.randint(2, 12)
        self.t3_b = random.choice([2, 3, 4, 5, 6, 8, 10])
        self.t3_ans = self.t3_n * self.t3_b
        self.t3_input = ""
        self.t3_attempts += 1

        for w in self.t3_task_row.winfo_children():
            w.destroy()
        tk.Label(self.t3_task_row,
                 text=f"Запиши  {self.t3_n}  як дріб зі знаменником {self.t3_b}:",
                 font=F_SUB, bg=PANEL, fg=TEXT).pack()

        for w in self.t3_frac_display.winfo_children():
            w.destroy()
        tk.Label(self.t3_frac_display, text="?",
                 font=F_FRAC, bg=PANEL, fg=ORANGE).pack()
        tk.Frame(self.t3_frac_display, bg=ORANGE, height=2, width=50).pack(pady=2)
        tk.Label(self.t3_frac_display, text=str(self.t3_b),
                 font=F_FRAC, bg=PANEL, fg=ACCENT).pack()

        if self.t3_inp_lbl:   self.t3_inp_lbl.config(text="", fg=ORANGE)
        if self.t3_feed_lbl:  self.t3_feed_lbl.config(text="")
        if self.t3_check_btn: self.t3_check_btn.config(state="normal", bg=GREEN)
        if self.t3_score_lbl: self.t3_score_lbl.config(text=self._t3_score_text())

    def _t3_key(self, ch):
        if ch.isdigit():
            if len(self.t3_input) < 5: self.t3_input += ch
        elif ch == "⌫":
            self.t3_input = self.t3_input[:-1]
        elif ch == "C":
            self.t3_input = ""
        if self.t3_inp_lbl: self.t3_inp_lbl.config(text=self.t3_input)
        if self.t3_frac_display:
            kids = self.t3_frac_display.winfo_children()
            if kids: kids[0].config(text=self.t3_input if self.t3_input else "?")

    def _t3_check(self):
        if not self.t3_input.strip():
            if self.t3_feed_lbl:
                self.t3_feed_lbl.config(text="⚠️ Введіть чисельник!", fg=ORANGE)
            return
        val = int(self.t3_input)
        self.t3_input = ""
        if self.t3_inp_lbl: self.t3_inp_lbl.config(text="")

        if val == self.t3_ans:
            self.t3_score += 1
            if self.t3_frac_display:
                kids = self.t3_frac_display.winfo_children()
                if kids:
                    kids[0].config(text=str(val), fg=GREEN)
                    if len(kids) > 1: kids[1].config(bg=GREEN)
            if self.t3_feed_lbl:
                self.t3_feed_lbl.config(text=f"🎉 Вірно! {self.t3_n} = {self.t3_ans}/{self.t3_b}", fg=GREEN)
            if self.t3_check_btn: self.t3_check_btn.config(state="disabled", bg=BTN_NUM)
        else:
            if self.t3_feed_lbl:
                self.t3_feed_lbl.config(text=f"❌ Не вірно. a = {self.t3_n} × {self.t3_b}", fg=RED)

        if self.t3_score_lbl:
            self.t3_score_lbl.config(text=self._t3_score_text())


if __name__ == "__main__":
    app = App()
    app.mainloop()
