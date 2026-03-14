"""
Демонстрація: Задачі та вправи на всі дії з натуральними числами (§ 15).
Для 5 класу.
Порядок дій, обчислення виразів з дужками, степенем, множенням/діленням, додаванням/відніманням.
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


def _is_number(tok):
    return isinstance(tok, int)


class AllOperationsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Всі дії з натуральними числами")
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
            8,
            27,
            13,
            144,
            2,
            40,
            72,
            248,
            12,
            91,
            145,
            39,
            338,
            438,
            100,
        }

        self.mode = None
        self.board_tokens = None
        self.board_message = ""
        self.user_input = ""
        self.score = 0
        self.total = 0
        self.phase = "answer"
        self.task = None
        self.task_hint_shown = False

        self._build_ui()
        self.show_rules()

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
            text="Всі дії з натуральними числами (§ 15)",
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
        tk.Button(nav, text="1. Правила", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_rules).pack(
            side="left", padx=10
        )
        tk.Button(
            nav,
            text="2. Властивості для зручних обчислень",
            font=btn_font,
            bg=WHITE,
            bd=0,
            cursor="hand2",
            command=self.show_properties,
        ).pack(side="left", padx=10)
        tk.Button(
            nav,
            text="3. Інтерактивна дошка (порядок дій)",
            font=btn_font,
            bg=WHITE,
            bd=0,
            cursor="hand2",
            command=self.show_board,
        ).pack(side="left", padx=10)
        tk.Button(nav, text="4. Тренажер", font=btn_font, bg=WHITE, bd=0, cursor="hand2", command=self.show_trainer).pack(
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

    def show_rules(self):
        self.clear_main()
        self.mode = "rules"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)

        tk.Label(f, text="Порядок дій у виразах", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 15))

        rule_box = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=25, pady=20)
        rule_box.pack(fill="x", pady=10)

        tk.Label(
            rule_box,
            text=(
                "1) У виразах з дужками спочатку обчислюють значення в дужках.\n"
                "2) У виразах без дужок:\n"
                "   • спочатку степінь (наприклад, x²)\n"
                "   • потім множення і ділення (зліва направо)\n"
                "   • потім додавання і віднімання (зліва направо)"
            ),
            font=("Segoe UI", 18),
            bg=WHITE,
            fg=TEXT,
            justify="left",
        ).pack(anchor="w")

        a = self._pick_not_forbidden(12, 60)
        b = self._pick_not_forbidden(10, 40)
        c = self._pick_not_forbidden(2, 12)
        d = self._pick_not_forbidden(2, 15)

        expr = f"{d} ∙ ({a} + {b}) - {a * d} : {c}"
        val = d * (a + b) - (a * d) // c

        ex = tk.Frame(f, bg=YELLOW_BG, bd=1, relief="solid", padx=20, pady=15)
        ex.pack(fill="x", pady=15)
        tk.Label(ex, text="Приклад (порядок дій):", font=("Segoe UI", 18, "bold"), bg=YELLOW_BG, fg=TEXT).pack(anchor="w")
        tk.Label(ex, text=f"{expr} = {val}", font=("Consolas", 22, "bold"), bg=YELLOW_BG, fg=HL_FG).pack(anchor="w")

        tk.Label(
            f,
            text="Для детального розбору натисни вкладку «Інтерактивна дошка».",
            font=("Segoe UI", 18, "italic"),
            bg=BG,
            fg=MUTED,
        ).pack(pady=10)

    def show_properties(self):
        self.clear_main()
        self.mode = "properties"

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=50, pady=25)

        tk.Label(f, text="Зручні обчислення через властивості", font=("Segoe UI", 32, "bold"), bg=BG, fg=TEXT).pack(
            pady=(0, 15)
        )

        box = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=25, pady=20)
        box.pack(fill="x", pady=10)

        tk.Label(
            box,
            text=(
                "Іноді вираз зручніше обчислити, використовуючи властивості арифметичних дій.\n"
                "Наприклад, розподільну властивість множення:\n"
                "a∙c − b∙c = (a − b)∙c"
            ),
            font=("Segoe UI", 18),
            bg=WHITE,
            fg=TEXT,
            justify="left",
        ).pack(anchor="w")

        c = self._pick_not_forbidden(11, 49)
        a_minus_b = 100
        b = self._pick_not_forbidden(200, 700)
        a = b + a_minus_b

        ex1 = tk.Frame(f, bg="#eff6ff", highlightbackground="#bfdbfe", highlightthickness=1, padx=20, pady=15)
        ex1.pack(fill="x", pady=12)
        tk.Label(ex1, text="Приклад (розподільна властивість):", font=("Segoe UI", 16, "bold"), bg="#eff6ff", fg=TEXT).pack(
            anchor="w"
        )
        tk.Label(ex1, text=f"{a} ∙ {c} − {b} ∙ {c} = ({a} − {b}) ∙ {c} = {a_minus_b} ∙ {c} = {a_minus_b * c}", font=("Consolas", 18, "bold"), bg="#eff6ff", fg=ACCENT).pack(
            anchor="w", pady=(6, 0)
        )

        x = self._pick_not_forbidden(6, 15)
        y = self._pick_not_forbidden(2, 9)
        ex2 = tk.Frame(f, bg="#f0fdf4", highlightbackground="#bbf7d0", highlightthickness=1, padx=20, pady=15)
        ex2.pack(fill="x", pady=12)
        tk.Label(ex2, text="Приклад (дужки + степінь):", font=("Segoe UI", 16, "bold"), bg="#f0fdf4", fg=TEXT).pack(anchor="w")
        tk.Label(ex2, text=f"({x}² − {y} : {y}) ∙ 7 = ({x * x} − 1) ∙ 7 = {(x * x - 1) * 7}", font=("Consolas", 18, "bold"), bg="#f0fdf4", fg=GREEN).pack(
            anchor="w", pady=(6, 0)
        )

    def show_board(self):
        self.clear_main()
        self.mode = "board"
        self.board_tokens = self._generate_board_expression()
        self.board_origin = list(self.board_tokens)
        self.board_message = "Натисни на знак дії, яку треба виконати наступною."

        f = tk.Frame(self.main_area, bg=BG)
        f.pack(expand=True, fill="both", padx=40, pady=20)

        tk.Label(f, text="Інтерактивна дошка: порядок дій", font=("Segoe UI", 30, "bold"), bg=BG, fg=TEXT).pack(pady=(0, 10))
        self.lbl_board_msg = tk.Label(f, text=self.board_message, font=("Segoe UI", 16, "bold"), bg=BG, fg=MUTED)
        self.lbl_board_msg.pack(pady=(0, 10))

        self.board_frame = tk.Frame(f, bg=WHITE, bd=2, relief="solid", padx=20, pady=20)
        self.board_frame.pack(fill="both", expand=True, padx=10, pady=10)

        btns = tk.Frame(f, bg=BG)
        btns.pack(pady=10)
        tk.Button(btns, text="🎲 Новий вираз", font=("Segoe UI", 14, "bold"), bg=ACCENT, fg=WHITE, bd=0, padx=20, pady=10, command=self._board_new).pack(
            side="left", padx=10
        )
        tk.Button(btns, text="↩ Скинути", font=("Segoe UI", 14, "bold"), bg=BTN_NUM, fg=TEXT, bd=0, padx=20, pady=10, command=self._board_reset).pack(
            side="left", padx=10
        )

        self._render_board()

    def _board_new(self):
        self.board_tokens = self._generate_board_expression()
        self.board_origin = list(self.board_tokens)
        self.board_message = "Натисни на знак дії, яку треба виконати наступною."
        self.lbl_board_msg.config(text=self.board_message, fg=MUTED)
        self._render_board()

    def _board_reset(self):
        if getattr(self, "board_origin", None):
            self.board_tokens = list(self.board_origin)
        self.board_message = "Натисни на знак дії, яку треба виконати наступною."
        self.lbl_board_msg.config(text=self.board_message, fg=MUTED)
        self._render_board()

    def _generate_board_expression(self):
        a = self._pick_not_forbidden(11, 49)
        b = self._pick_not_forbidden(11, 39)
        c = self._pick_not_forbidden(2, 9)
        d = self._pick_not_forbidden(2, 12)
        e = self._pick_not_forbidden(2, 10)

        left = ["(", a, "+", b, ")", "^2"]
        right_mul = [d, "*", "(", e, "+", c, ")"]
        right_div = [a * d, "/", d]
        tokens = left + ["-", *right_mul, "+", *right_div]
        tokens = self._simplify_parentheses(tokens)
        return list(tokens)

    def _render_board(self):
        for w in self.board_frame.winfo_children():
            w.destroy()

        tokens = self._simplify_parentheses(list(self.board_tokens or []))
        if not tokens:
            self.board_tokens = self._generate_board_expression()
            self.board_origin = list(self.board_tokens)
            tokens = self._simplify_parentheses(list(self.board_tokens))

        if self._board_is_done(tokens):
            tk.Label(self.board_frame, text=f"Готово! Відповідь: {tokens[0]}", font=("Segoe UI", 36, "bold"), bg=WHITE, fg=GREEN).pack(
                pady=30
            )
            return

        expected = self._next_operation(tokens)
        exp_idx = expected["op_index"]
        if exp_idx < 0 or exp_idx >= len(tokens):
            self.board_tokens = self._generate_board_expression()
            self.board_origin = list(self.board_tokens)
            self.lbl_board_msg.config(text="Спробуй ще раз: створено новий вираз.", fg=MUTED)
            self._render_board()
            return
        exp_tok = tokens[exp_idx]

        row = tk.Frame(self.board_frame, bg=WHITE)
        row.pack(anchor="w", pady=10)

        for i, tok in enumerate(tokens):
            if tok in ("+", "-", "*", "/", "^2"):
                label = "²" if tok == "^2" else tok
                b = tk.Button(
                    row,
                    text=label,
                    font=("Segoe UI", 22, "bold"),
                    bg=BTN_NUM,
                    fg=TEXT,
                    bd=0,
                    padx=14,
                    pady=6,
                    cursor="hand2",
                    command=lambda idx=i: self._board_click(tokens, idx),
                )
                b.pack(side="left", padx=6)
                if i == exp_idx:
                    b.config(bg="#dcfce7")
            else:
                t = str(tok)
                if tok == "(" or tok == ")":
                    t = tok
                tk.Label(row, text=t, font=("Segoe UI", 22, "bold"), bg=WHITE, fg=TEXT).pack(side="left", padx=6)

        info = tk.Frame(self.board_frame, bg=WHITE)
        info.pack(fill="x", pady=(20, 0))

        tk.Label(info, text="Наступна правильна дія:", font=("Segoe UI", 14, "bold"), bg=WHITE, fg=MUTED).pack(anchor="w")
        tk.Label(info, text=("²" if exp_tok == "^2" else exp_tok), font=("Segoe UI", 20, "bold"), bg=YELLOW_BG, fg=HL_FG, padx=10, pady=5).pack(
            anchor="w", pady=(6, 0)
        )

    def _board_click(self, tokens, idx):
        expected = self._next_operation(tokens)
        if idx != expected["op_index"]:
            self.lbl_board_msg.config(text="Неправильно. Спочатку виконай дію з більшим пріоритетом.", fg=RED)
            return

        new_tokens = self._apply_operation(tokens, expected)
        self.lbl_board_msg.config(text="✅ Правильно! Рухайся далі.", fg=GREEN)
        self.board_tokens = list(new_tokens)
        self.after(350, self._render_board)

    def _board_is_done(self, tokens):
        tokens = self._simplify_parentheses(tokens)
        return len(tokens) == 1 and _is_number(tokens[0])

    def _simplify_parentheses(self, tokens):
        out = list(tokens)
        changed = True
        while changed:
            changed = False
            i = 0
            while i < len(out) - 2:
                if out[i] == "(" and _is_number(out[i + 1]) and out[i + 2] == ")":
                    out = out[:i] + [out[i + 1]] + out[i + 3 :]
                    changed = True
                    break
                i += 1
        return out

    def _next_operation(self, tokens):
        tokens = self._simplify_parentheses(tokens)

        stack = []
        best_range = None
        for i, tok in enumerate(tokens):
            if tok == "(":
                stack.append(i)
            elif tok == ")" and stack:
                l = stack.pop()
                best_range = (l, i)
                break

        if best_range is not None:
            start, end = best_range
            inner = tokens[start + 1 : end]
            op = self._next_operation(inner)
            return {"op_index": start + 1 + op["op_index"], "type": op["type"], "span": (start + 1 + op["span"][0], start + 1 + op["span"][1])}

        for i in range(len(tokens)):
            if tokens[i] == "^2":
                if i - 1 >= 0 and _is_number(tokens[i - 1]):
                    return {"op_index": i, "type": "pow", "span": (i - 1, i)}

        for i in range(len(tokens)):
            if tokens[i] in ("*", "/"):
                if i - 1 >= 0 and i + 1 < len(tokens) and _is_number(tokens[i - 1]) and _is_number(tokens[i + 1]):
                    return {"op_index": i, "type": "bin", "span": (i - 1, i + 1)}

        for i in range(len(tokens)):
            if tokens[i] in ("+", "-"):
                if i - 1 >= 0 and i + 1 < len(tokens) and _is_number(tokens[i - 1]) and _is_number(tokens[i + 1]):
                    return {"op_index": i, "type": "bin", "span": (i - 1, i + 1)}

        return {"op_index": 0, "type": "none", "span": (0, 0)}

    def _apply_operation(self, tokens, op):
        tokens = self._simplify_parentheses(tokens)
        a, b = op["span"]
        if op["type"] == "pow":
            base = tokens[a]
            res = base * base
            new = tokens[:a] + [res] + tokens[b + 1 :]
            return self._simplify_parentheses(new)

        if op["type"] == "bin":
            left = tokens[a]
            oper = tokens[op["op_index"]]
            right = tokens[b]
            if oper == "+":
                res = left + right
            elif oper == "-":
                res = left - right
            elif oper == "*":
                res = left * right
            else:
                if right == 0:
                    res = 0
                else:
                    res = left // right
            new = tokens[:a] + [res] + tokens[b + 1 :]
            return self._simplify_parentheses(new)

        return tokens

    def show_trainer(self):
        self.clear_main()
        self.mode = "trainer"

        LW = int(self.SW * 0.60)
        RW = self.SW - LW

        left = tk.Frame(self.main_area, bg=BG, width=LW)
        left.pack(side="left", fill="both")
        left.pack_propagate(False)

        title = tk.Label(left, text="Тренажер: обчисли значення виразу", font=("Segoe UI", 28, "bold"), bg=BG, fg=TEXT)
        title.pack(pady=(25, 10))

        self.task_box = tk.Frame(left, bg=WHITE, bd=3, relief="solid", padx=40, pady=30)
        self.task_box.pack(pady=15)
        self.task_text = tk.Label(self.task_box, text="", font=("Segoe UI", 22, "bold"), bg=WHITE, fg=TEXT, justify="center", wraplength=LW - 120)
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
                tk.Button(
                    r,
                    text=ch,
                    bg=RED_BG if ch in ("⌫", "C") else BTN_NUM,
                    fg=TEXT,
                    font=("Segoe UI", 20, "bold"),
                    width=6,
                    height=1,
                    relief="flat",
                    command=lambda c=ch: self._key_press(c),
                ).pack(side="left", padx=5)

        btn_f = tk.Frame(left, bg=BG)
        btn_f.pack(pady=10)
        self.btn_ok = tk.Button(
            btn_f,
            text="✓ Перевірити",
            bg=GREEN,
            fg=WHITE,
            font=("Segoe UI", 18, "bold"),
            relief="flat",
            padx=40,
            pady=10,
            command=self.check_answer,
        )
        self.btn_ok.pack(side="left", padx=20)
        self.btn_next = tk.Button(
            btn_f,
            text="▶ Наступне",
            bg=ACCENT,
            fg=WHITE,
            font=("Segoe UI", 18, "bold"),
            relief="flat",
            padx=40,
            pady=10,
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
                "Порядок дій:\n"
                "1) Дужки\n"
                "2) Степінь\n"
                "3) Множення/ділення (зліва направо)\n"
                "4) Додавання/віднімання (зліва направо)\n\n"
                "Іноді вигідно винести спільний множник:\n"
                "a∙c − b∙c = (a − b)∙c"
            ),
            font=("Segoe UI", 12),
            bg="#eff6ff",
            justify="left",
        ).pack(anchor="w")

        self.btn_task_hint = tk.Button(
            rpad,
            text="Підказка до задачі (крок)",
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
        self.task_hint_body = tk.Label(self.task_hint_frame, text="", font=("Consolas", 14), bg=WHITE, fg=TEXT, justify="left", wraplength=RW - 80)
        self.task_hint_body.pack(anchor="w", pady=(8, 0))

        self.lbl_score = tk.Label(rpad, text="Рахунок: 0 / 0", font=("Segoe UI", 24, "bold"), bg=PANEL, fg=ACCENT)
        self.lbl_score.pack(side="bottom", pady=20)

        self.next_task()

    def toggle_task_hint(self):
        self.task_hint_shown = not self.task_hint_shown
        if self.task_hint_shown:
            self.task_hint_frame.pack(fill="x", pady=(10, 0))
            self.btn_task_hint.config(text="Сховати підказку")
        else:
            self.task_hint_frame.pack_forget()
            self.btn_task_hint.config(text="Підказка до задачі (крок)")
        self._render_task_hint()

    def _render_task_hint(self):
        if not self.task_hint_shown:
            return
        if not self.task:
            return
        self.task_hint_title.config(text=self.task.get("hint_title", ""))
        self.task_hint_body.config(text=self.task.get("hint_body", ""))

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

        t = random.choice(["mix1", "mix2", "mix3", "dist"])

        if t == "dist":
            c = self._pick_not_forbidden(11, 49)
            a_minus_b = 100
            b = self._pick_not_forbidden(200, 700)
            a = b + a_minus_b
            ans = (a - b) * c
            text = f"Обчисли зручним способом:\n{a} ∙ {c} − {b} ∙ {c}"
            hint_title = "Підказка: розподільна властивість"
            hint_body = f"{a}∙{c} − {b}∙{c} = ({a} − {b})∙{c} = {a_minus_b}∙{c} = {ans}"
        elif t == "mix1":
            a = self._pick_not_forbidden(11, 49)
            b = self._pick_not_forbidden(11, 39)
            d = self._pick_not_forbidden(2, 12)
            k = self._pick_not_forbidden(2, 9)
            expr_tokens = ["(", a, "+", b, ")", "*", d, "-", a * d, "/", k]
            if (a * d) % k != 0:
                k = 1
            ans = (a + b) * d - (a * d) // k
            text = f"Обчисли:\n{d} ∙ ({a} + {b}) − {a * d} : {k}"
            hint_title = "Підказка: порядок дій"
            hint_body = "1) Дужки → 2) Множення/ділення → 3) Віднімання"
        elif t == "mix2":
            x = self._pick_not_forbidden(6, 15)
            y = self._pick_not_forbidden(2, 9)
            m = self._pick_not_forbidden(11, 39)
            ans = (x * x - (y * m) // m) * 7
            text = f"Обчисли:\n({x}² − {y * m} : {m}) ∙ 7"
            hint_title = "Підказка: степінь"
            hint_body = f"{x}² = {x * x}, {y * m}:{m} = {y}"
        else:
            a = self._pick_not_forbidden(200, 900)
            b = self._pick_not_forbidden(20, 99)
            c = self._pick_not_forbidden(2, 12)
            d = self._pick_not_forbidden(2, 10)
            left = a - b
            if left % c != 0:
                left = left - (left % c)
            ans = (left // c) + d * d
            text = f"Обчисли:\n({left} : {c}) + {d}²"
            hint_title = "Підказка: дужки + степінь"
            hint_body = "1) Дужки (ділення) → 2) Степінь → 3) Додавання"

        self.task = {"ans": int(ans), "text": text, "hint_title": hint_title, "hint_body": hint_body}
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
    app = AllOperationsApp()
    app.mainloop()
