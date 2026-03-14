"""
Тренажер обчислень у стовпчик (4 клас) — Цілі числа.
Операції: Додавання, Віднімання, Множення, Ділення.
Всі числа цілі, без ком.
"""

import tkinter as tk
import tkinter.font as tkf
import random

# ══════════════════════════════════════════════════════════════════
#  ПАЛІТРА
# ══════════════════════════════════════════════════════════════════
BG        = "#faf8f4"
WHITE     = "#ffffff"
BORDER    = "#e2e0dc"
BORDER2   = "#c9c6c0"
TEXT      = "#1c1917"
MUTED     = "#78716c"
ACC       = "#2563eb"
ACC_BG    = "#dbeafe"
GREEN     = "#16a34a"
GREEN_BG  = "#dcfce7"
RED       = "#dc2626"
RED_BG    = "#fee2e2"
ORANGE    = "#ea580c"
YELLOW    = "#ca8a04"
YELLOW_BG = "#fef9c3"
CARRY_C   = "#7c3aed"
CARRY_BG  = "#ede9fe"
GIVEN_BG  = "#f0ede8"
HDR_BG    = "#1c1917"
OK_BG     = GREEN_BG
OK_FG     = GREEN
ERR_BG    = RED_BG
ERR_FG    = RED
HINT_BG   = YELLOW_BG
HINT_FG   = YELLOW

OP_COLORS = {'+': ('#14532d','#dcfce7'),
             '−': ('#7f1d1d','#fee2e2'),
             '×': ('#3b0764','#f3e8ff'),
             '÷': ('#1e3a8a','#dbeafe'),
             '÷R':('#0e7490','#cffafe')}

CELL_W  = 52
CELL_H  = 52
CARRY_H = 20
GAP     = 2

FONT_TASK   = ("Segoe UI",    48, "bold")   # велике завдання
FONT_MONO   = ("Courier New", 26, "bold")   # цифри в матриці
FONT_MONO_S = ("Courier New", 16, "bold")
FONT_MONO_XS= ("Courier New", 12, "bold")
FONT_HDR    = ("Segoe UI",    16, "bold")
FONT_UI_B   = ("Segoe UI",    12, "bold")
FONT_UI     = ("Segoe UI",    12)
FONT_SMALL  = ("Segoe UI",    10)
FONT_HINT_T = ("Segoe UI",    11, "italic")
FONT_PAD    = ("Segoe UI",    22, "bold")   # цифри на клавіатурі

# ══════════════════════════════════════════════════════════════════
#  МАТЕМАТИКА (ЦІЛІ ЧИСЛА)
# ══════════════════════════════════════════════════════════════════

def rnd(a, b):
    return random.randint(a, b)

# ── Ділення (цілочисельне) ───────────────────────────────────────
def build_division(a, b):
    """
    Ділення цілого a на ціле b.
    Генерує кроки для стовпчика.
    """
    a_str = str(a)
    b_str = str(b)
    n_dig = len(a_str)
    
    div_steps = []
    
    current_val = 0
    # Позиція поточної цифри в a_str, яку ми зносимо
    current_idx = 0
    
    # Шукаємо перше неповне ділене
    first_part = True
    
    while current_idx < n_dig:
        # Зносимо цифру
        digit = int(a_str[current_idx])
        current_val = current_val * 10 + digit
        
        # Якщо це початок і число менше дільника, беремо наступну цифру
        if first_part and current_val < b:
            current_idx += 1
            continue
            
        first_part = False
        
        # Ділимо
        q_digit = current_val // b
        prod    = q_digit * b
        rem     = current_val - prod
        
        # Записуємо крок
        # dig_col - це колонка, де закінчується число (вирівнювання вправо)
        # У нашій матриці це відповідає індексу цифри в a_str
        div_steps.append({
            'k': current_idx,
            'dig_col': current_idx, 
            'val': current_val, # те, що ділимо (зноска)
            'digit': q_digit,   # цифра частки
            'prod': prod,       # що віднімаємо
            'rem': rem          # залишок
        })
        
        current_val = rem
        current_idx += 1

    return {
        'a': a, 'b': b,
        'a_str': a_str, 'b_str': b_str,
        'div_steps': div_steps,
        'q_str': str(a // b)
    }

def build_matrix_division(info):
    div_steps = info['div_steps']
    a_str     = info['a_str']
    b_str     = info['b_str']
    q_str     = info['q_str']
    n_steps   = len(div_steps)
    b         = info['b']

    # ── Розміри ───────────────────────────────────────────────────
    # Лівий блок: ділене + обчислення
    # Ширина визначається довжиною a_str (плюс можливі відступи, але для цілих зазвичай вистачає)
    left_w = len(a_str) + 1 
    
    # Правий блок: дільник і частка
    right_w = max(len(b_str), len(q_str)) + 1
    SEP = left_w
    total_cols = SEP + 1 + right_w

    # ── Рядки ─────────────────────────────────────────────────────
    # r0: a | b
    # r1: - | = (лінії)
    # r2:   | q
    
    # Визначаємо структуру рядків
    # Для першого кроку: prod (віднімаємо) і line
    # Але prod має бути ВІДРАЗУ під a (r0), тобто r1
    # А лінія під ним.
    # Але у нас r1 зайнято лінією під дільником.
    
    # Класичний вигляд:
    #   126 | 3
    #   12  |---
    #   --  | 42
    #    06
    #     6
    #    --
    #     0
    
    # Отже:
    # r0: 126 | 3
    # r1: 12  |--- (тут prod_0 і лінія розділювача)
    # r2: --  | 42 (лінія під prod_0 і частка)
    
    # Перебудуємо логіку рядків
    
    # r0: a | op | b
    # r1: prod_0 (під a) | = | line_under_b
    # r2: line_under_prod_0 | q
    
    # Далі кроки k>0:
    # r_next: val_k (зноска)
    # r_next+1: prod_k
    # r_next+2: line
    
    n_rows = 3 # r0, r1, r2
    for k in range(1, n_steps):
        n_rows += 3 # val, prod, line
    
    # Останній залишок
    n_rows += 1

    matrix = _make_matrix(n_rows, total_cols)
    input_order = []

    # ── r0: a, op, b ──────────────────────────────────────────────
    for i, ch in enumerate(a_str):
        matrix[0][i] = Cell(GIVEN, ch)
    matrix[0][SEP] = Cell(OP_SYM, '÷')
    for i, ch in enumerate(b_str):
        matrix[0][SEP + 1 + i] = Cell(GIVEN, ch)

    # ── r1: prod_0 (частково) і лінія під b ───────────────────────
    # Спочатку заповнимо праву частину (лінія під b)
    matrix[1][SEP] = Cell(OP_SYM, '=') # або вертикальна риска
    for c in range(SEP + 1, total_cols):
        matrix[1][c] = Cell(LINE, '') # Горизонтальна під дільником

    # ── r2: q (частка) ────────────────────────────────────────────
    # Спочатку заповнимо q (щоб було праворуч)
    c_start = SEP + 1
    for i, ch in enumerate(q_str):
        col = c_start + i
        # Прибираємо явні підказки
        matrix[2][col] = Cell(INPUT, ch, hint="")
        # НЕ додаємо в input_order відразу! Порядок важливий.

    # Тепер формуємо input_order ПОКРОКОВО
    # Крок 0:
    # 1. Вгадати першу цифру частки (q[0])
    # 2. Ввести prod_0 (те що віднімаємо)
    
    # Змінна для поточного рядка лівої частини
    left_row = 1 
    
    for k, s in enumerate(div_steps):
        # Додаємо цифру частки в порядок вводу
        q_col = c_start + k
        
        right_col = s['dig_col']
        val_str   = str(s['val'])
        prod_str  = str(s['prod'])
        rem_str   = str(s['rem'])
        
        # Якщо це Крок 0:
        if k == 0:
            # Спочатку цифра частки
            input_order.append((2, q_col))
            
            # prod_0 пишеться в r1 (left_row)
            w = len(prod_str)
            for i, ch in enumerate(prod_str):
                col = right_col - w + 1 + i
                matrix[left_row][col] = Cell(INPUT, ch, hint="")
                input_order.append((left_row, col))
            left_row += 1
            
            # Лінія під prod_0 (r2)
            # В r2 справа вже є частка, але зліва вільно
            line_w = len(prod_str)
            for c in range(right_col - line_w + 1, right_col + 1):
                matrix[left_row][c] = Cell(LINE, '')
            left_row += 1
            
        else:
            # Крок k > 0
            # 1. Зноска (val)
            w = len(val_str)
            for i, ch in enumerate(val_str):
                col = right_col - w + 1 + i
                matrix[left_row][col] = Cell(INPUT, ch, hint="")
                input_order.append((left_row, col))
            left_row += 1

            # 2. Цифра частки (ТЕПЕР ТУТ)
            input_order.append((2, q_col))
            
            # 3. Добуток (prod)
            w = len(prod_str)
            for i, ch in enumerate(prod_str):
                col = right_col - w + 1 + i
                matrix[left_row][col] = Cell(INPUT, ch, hint="")
                input_order.append((left_row, col))
            left_row += 1
            
            # 4. Лінія
            line_w = len(prod_str)
            for c in range(right_col - line_w + 1, right_col + 1):
                matrix[left_row][c] = Cell(LINE, '')
            left_row += 1
            
        # Якщо останній крок - залишок
        if k == n_steps - 1:
            w = len(rem_str)
            for i, ch in enumerate(rem_str):
                col = right_col - w + 1 + i
                matrix[left_row][col] = Cell(INPUT, ch, hint="")
                input_order.append((left_row, col))
            left_row += 1

    _fix_coords(matrix)
    return matrix, input_order

# ── Множення ─────────────────────────────────────────────────────
def build_multiplication(a, b):
    # a, b - integers
    res = a * b
    b_str = str(b)
    partials = []
    
    # Часткові добутки
    # b_str йде зліва направо, але множимо ми з розряду одиниць (справа наліво)
    for i, digit_char in enumerate(reversed(b_str)):
        digit = int(digit_char)
        val = a * digit
        # shift = i (0 для одиниць, 1 для десятків...)
        partials.append({'val': val, 'shift': i, 'dgt': digit})
        
    return {
        'a': a, 'b': b, 'res': res,
        'partials': partials,
        'a_str': str(a), 'b_str': str(b), 'r_str': str(res)
    }

def build_matrix_multiplication(info):
    a_str = info['a_str']
    b_str = info['b_str']
    r_str = info['r_str']
    partials = info['partials']
    
    # Ширина матриці
    # Макс ширина = макс(a, b, shift+partial, res)
    max_w = max(len(a_str), len(b_str))
    for p in partials:
        max_w = max(max_w, len(str(p['val'])) + p['shift'])
    max_w = max(max_w, len(r_str))
    
    tc = max_w + 2 # + запас зліва
    
    n_rows = 3 + len(partials) + 2 # a, b, line, partials..., line, res
    matrix = _make_matrix(n_rows, tc)
    input_order = []
    
    # r0: a
    for i, ch in enumerate(a_str):
        col = tc - len(a_str) + i
        matrix[0][col] = Cell(GIVEN, ch)
        
    # r1: x b
    matrix[1][0] = Cell(OP_SYM, '×')
    for i, ch in enumerate(b_str):
        col = tc - len(b_str) + i
        matrix[1][col] = Cell(GIVEN, ch)
        
    # r2: line
    for c in range(tc): matrix[2][c] = Cell(LINE, '')
    
    # Partials
    cur_row = 3
    # Сортуємо partials від одиниць (shift=0) до старших
    # Вони вже в такому порядку в info['partials']
    
    for p in partials:
        p_str = str(p['val'])
        shift = p['shift']
        
        # Ввід справа наліво
        cells_in_row = []
        for i, ch in enumerate(p_str):
            col = tc - shift - len(p_str) + i
            cell = Cell(INPUT, ch, hint=f"{info['a']} × {p['dgt']} = {p['val']}")
            matrix[cur_row][col] = cell
            cells_in_row.append((cur_row, col))
        
        # Додаємо в input_order у зворотному порядку (справа наліво)
        input_order.extend(reversed(cells_in_row))
        cur_row += 1
        
    # Line
    for c in range(tc): matrix[cur_row][c] = Cell(LINE, '')
    cur_row += 1
    
    # Result (якщо більше 1 часткового добутку)
    if len(partials) > 1:
        cells_res = []
        for i, ch in enumerate(r_str):
            col = tc - len(r_str) + i
            cell = Cell(INPUT, ch, hint=f"Сума = {r_str}")
            matrix[cur_row][col] = cell
            cells_res.append((cur_row, col))
        input_order.extend(reversed(cells_res))
    else:
        # Якщо множили на одну цифру, результат вже в partials, рядка суми немає
        pass

    _fix_coords(matrix)
    return matrix, input_order

# ── Додавання / Віднімання ───────────────────────────────────────
def build_add_sub(a, b, op):
    res = a + b if op == '+' else a - b
    
    a_str = str(a)
    b_str = str(b)
    r_str = str(res)
    
    max_len = max(len(a_str), len(b_str), len(r_str))
    
    # Переноси (carries)
    # Для візуалізації обчислюємо їх
    a_fill = a_str.zfill(max_len)
    b_fill = b_str.zfill(max_len)
    carries = []
    
    carry = 0
    # Йдемо справа наліво
    for i in range(max_len - 1, -1, -1):
        da = int(a_fill[i])
        db = int(b_fill[i])
        
        if op == '+':
            s = da + db + carry
            new_carry = s // 10
        else:
            s = da - db + carry
            if s < 0:
                new_carry = -1
            else:
                new_carry = 0
        
        carries.insert(0, carry) # зберігаємо carry, який ПРИЙШОВ у цей розряд
        carry = new_carry
        
    return {
        'a': a, 'b': b, 'op': op, 'res': res,
        'a_str': a_str, 'b_str': b_str, 'r_str': r_str,
        'carries': carries, 'max_len': max_len
    }

def build_matrix_add_sub(info):
    a_str = info['a_str']
    b_str = info['b_str']
    r_str = info['r_str']
    max_len = info['max_len']
    carries = info['carries']
    op = info['op']
    
    tc = max_len + 1 # +1 for sign
    n_rows = 5 # carries, a, b, line, res
    
    matrix = _make_matrix(n_rows, tc)
    input_order = []
    
    # r0: Carries (відображаємо тільки ненульові, які впливають на розряд)
    # carries[i] - це перенос, який прийшов у розряд i
    # Але зазвичай пишуть перенос НАД тим розрядом, куди він прийшов.
    # for i, c_val in enumerate(carries):
    #     if c_val != 0:
    #         col = tc - max_len + i
    #         matrix[0][col] = Cell(CARRY, str(abs(c_val)))
            
    # r1: a
    for i, ch in enumerate(a_str):
        col = tc - len(a_str) + i
        matrix[1][col] = Cell(GIVEN, ch)
        
    # r2: op b
    matrix[2][0] = Cell(OP_SYM, op)
    for i, ch in enumerate(b_str):
        col = tc - len(b_str) + i
        matrix[2][col] = Cell(GIVEN, ch)
        
    # r3: line
    for c in range(tc): matrix[3][c] = Cell(LINE, '')
    
    # r4: res
    cells_res = []
    for i, ch in enumerate(r_str):
        col = tc - len(r_str) + i
        # Підказка
        hint = "Результат"
        matrix[4][col] = Cell(INPUT, ch, hint=hint)
        cells_res.append((4, col))
        
    input_order.extend(reversed(cells_res))
    
    _fix_coords(matrix)
    return matrix, input_order


# ══════════════════════════════════════════════════════════════════
#  ТИПИ КЛІТИНОК
# ══════════════════════════════════════════════════════════════════
EMPTY  = 'empty'
GIVEN  = 'given'
INPUT  = 'input'
OP_SYM = 'op'
LINE   = 'line'
CARRY  = 'carry'
LABEL  = 'label'

class Cell:
    def __init__(self, ctype=EMPTY, value='', row=0, col=0, hint=''):
        self.ctype    = ctype
        self.value    = value
        self.row      = row
        self.col      = col
        self.hint     = hint
        self.state    = 'idle'   # idle|active|ok|error|hint_shown
        self.user_val = ''

def _make_matrix(nrows, ncols):
    return [[Cell(EMPTY, row=r, col=c) for c in range(ncols)]
            for r in range(nrows)]

def _fix_coords(matrix):
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            cell.row = r; cell.col = c

# ══════════════════════════════════════════════════════════════════
#  ГЕНЕРАТОР (ЦІЛІ)
# ══════════════════════════════════════════════════════════════════
def gen_numbers(op, diff):
    # easy: 2-digit / 1-digit, or similar
    # med: 3-digit / 1-2 digit
    # hard: 4-5 digit
    
    if op == '÷':
        if diff == 'easy':
            b = rnd(2, 9)
            q = rnd(10, 99)
        elif diff == 'med':
            b = rnd(3, 19)
            q = rnd(20, 200)
        else:
            b = rnd(12, 99)
            q = rnd(100, 999)
        a = q * b
        return a, b
        
    elif op == '÷R':
        if diff == 'easy':
            b = rnd(2, 9)
            q = rnd(10, 99)
        elif diff == 'med':
            b = rnd(3, 19)
            q = rnd(20, 200)
        else:
            b = rnd(12, 99)
            q = rnd(100, 999)
        
        # Завжди з залишком
        rem = rnd(1, b-1)
        a = q * b + rem
        return a, b
        
    elif op == '×':
        if diff == 'easy':
            a = rnd(10, 99)
            b = rnd(2, 9)
        elif diff == 'med':
            a = rnd(100, 999)
            b = rnd(2, 19)
        else:
            a = rnd(100, 9999)
            b = rnd(12, 99)
        return a, b
        
    else: # + -
        if diff == 'easy':
            a = rnd(10, 99)
            b = rnd(10, 99)
        elif diff == 'med':
            a = rnd(100, 9999)
            b = rnd(100, 9999)
        else:
            a = rnd(10000, 999999)
            b = rnd(10000, 999999)
            
    if op == '−' and b > a:
        a, b = b, a
    return a, b


# ══════════════════════════════════════════════════════════════════
#  ГОЛОВНИЙ КЛАС
# ══════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Тренажер — Стовпчик (4 клас)")
        self.configure(bg=BG)
        self.resizable(True, True)
        
        # Спробуємо на весь екран
        try:    self.state("zoomed")
        except: self.attributes("-fullscreen", True)

        self.op        = '÷'
        self.diff      = 'med'
        self.score_ok  = 0
        self.score_all = 0
        self.streak    = 0
        self.matrix    = []
        self.order     = []
        self.step_idx  = 0
        self.hint_used = False
        self.task_done = False
        self._pending_digit = ''
        self._timer_id = None

        self._build_ui()
        self._new_task()
        self.bind('<Escape>', lambda e: self.attributes('-fullscreen', False))
        self.bind('<Key>', self._block_keyboard)

    def _block_keyboard(self, event):
        return 'break'

    def _build_ui(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = min(1400, sw), min(900, sh)
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.minsize(960, 640)

        # Header
        hdr = tk.Frame(self, bg=HDR_BG, height=60)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)
        tk.Label(hdr, text="Повторення 4 клас: Стовпчик",
                 bg=HDR_BG, fg=WHITE, font=FONT_HDR).place(x=20, rely=.5, anchor='w')
        self._lbl_score = tk.Label(hdr, text="Вірно: 0 / 0",
                                   bg=HDR_BG, fg='#a1a1aa', font=FONT_UI)
        self._lbl_score.place(relx=1, x=-20, rely=.5, anchor='e')

        body = tk.Frame(self, bg=BG)
        body.pack(fill='both', expand=True)

        # Left
        left = tk.Frame(body, bg=WHITE, width=220,
                        highlightbackground=BORDER, highlightthickness=1)
        left.pack(side='left', fill='y')
        left.pack_propagate(False)
        self._build_left(left)

        # Right
        right = tk.Frame(body, bg=WHITE, width=240,
                         highlightbackground=BORDER, highlightthickness=1)
        right.pack(side='right', fill='y')
        right.pack_propagate(False)
        self._build_right(right)

        # Center
        center = tk.Frame(body, bg=BG)
        center.pack(side='left', fill='both', expand=True)
        self._build_center(center)

    def _build_left(self, parent):
        p = tk.Frame(parent, bg=WHITE)
        p.pack(fill='both', expand=True, padx=12, pady=16)

        tk.Label(p, text="ОПЕРАЦІЯ", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 10, "bold")).pack(anchor='w', pady=(0,6))

        self._op_btns = {}
        for op, label in [('÷','Ділення'), ('÷R', 'З остачею'),
                           ('×','Множення'), ('+','Додавання'),('−','Віднімання')]:
            fg_c, bg_c = OP_COLORS[op]
            op_sym = op
            if '÷' in op_sym: op_sym = '÷'
            btn = tk.Button(p, text=f"  {op_sym}  {label}",
                            bg=WHITE, fg=MUTED, font=FONT_UI_B,
                            relief='flat', bd=0, cursor='hand2', anchor='w',
                            padx=8, pady=7,
                            highlightbackground=BORDER, highlightthickness=1,
                            command=lambda o=op: self._set_op(o))
            btn.pack(fill='x', pady=3)
            self._op_btns[op] = (btn, fg_c, bg_c)

        tk.Frame(p, bg=BORDER, height=1).pack(fill='x', pady=15)

        tk.Label(p, text="РІВЕНЬ", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 10, "bold")).pack(anchor='w', pady=(0,6))

        self._diff_btns = {}
        for d, label, col in [('easy','🟢 Легкий', GREEN),
                               ('med', '🟡 Середній', YELLOW),
                               ('hard','🔴 Складний', RED)]:
            btn = tk.Button(p, text=label, bg=WHITE, fg=MUTED,
                            font=FONT_UI_B, relief='flat', bd=0,
                            cursor='hand2', anchor='w', padx=8, pady=7,
                            highlightbackground=BORDER, highlightthickness=1,
                            command=lambda x=d: self._set_diff(x))
            btn.pack(fill='x', pady=3)
            self._diff_btns[d] = (btn, col)

        tk.Frame(p, bg=BORDER, height=1).pack(fill='x', pady=15)

        tk.Button(p, text="↺  Нове завдання",
                  bg=BG, fg=TEXT, font=FONT_UI_B,
                  relief='flat', bd=0, cursor='hand2', padx=8, pady=10,
                  highlightbackground=BORDER2, highlightthickness=1,
                  command=self._new_task).pack(fill='x')

        self._update_left_buttons()

    def _build_center(self, parent):
        # Task display
        task_frame = tk.Frame(parent, bg=WHITE,
                              highlightbackground=BORDER2, highlightthickness=1)
        task_frame.pack(fill='x', padx=20, pady=(20, 10))

        inner_task = tk.Frame(task_frame, bg=WHITE)
        inner_task.pack(pady=15)

        self._lbl_task = tk.Label(inner_task, text="",
                                  bg=WHITE, fg=TEXT,
                                  font=FONT_TASK)
        self._lbl_task.pack(side='left')

        self._lbl_step = tk.Label(inner_task, text="",
                                  bg=WHITE, fg=MUTED,
                                  font=("Segoe UI", 14))
        self._lbl_step.pack(side='left', padx=(30, 0))

        # Canvas
        canvas_frame = tk.Frame(parent, bg=BG)
        canvas_frame.pack(fill='both', expand=True, padx=20, pady=5)

        self._canvas = tk.Canvas(canvas_frame, bg=WHITE,
                                 highlightbackground=BORDER2, highlightthickness=1)
        self._canvas.pack(fill='both', expand=True)
        self._canvas.bind('<Configure>', lambda e: self._redraw())

        # Hint text
        self._lbl_prompt = tk.Label(parent, text="",
                                    bg=BG, fg=MUTED, font=FONT_HINT_T,
                                    wraplength=600, justify='center')
        self._lbl_prompt.pack(pady=(5, 0))

        # Numpad area
        bottom = tk.Frame(parent, bg=BG)
        bottom.pack(pady=(5, 20))

        self._lbl_msg = tk.Label(bottom, text="",
                                 bg=BG, fg=RED, font=FONT_UI_B)
        self._lbl_msg.pack(pady=(0, 10))

        numpad = tk.Frame(bottom, bg=BG)
        numpad.pack()
        self._build_numpad(numpad)

    def _build_numpad(self, parent):
        PAD = 6
        layout = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['⌫', '0', '✓'],
        ]
        for ri, row in enumerate(layout):
            for ci, label in enumerate(row):
                if label == '⌫':
                    bg_c, fg_c = '#fef2f2', RED
                elif label == '✓':
                    bg_c, fg_c = '#f0fdf4', GREEN
                else:
                    bg_c, fg_c = WHITE, TEXT

                btn = tk.Button(
                    parent,
                    text=label,
                    bg=bg_c, fg=fg_c,
                    font=FONT_PAD,
                    relief='solid', bd=1,
                    cursor='hand2',
                    width=4, height=1,
                    highlightbackground=BORDER2, highlightthickness=1,
                    command=lambda l=label: self._numpad_press(l)
                )
                btn.grid(row=ri, column=ci,
                         padx=PAD, pady=PAD,
                         ipadx=10, ipady=10)

    def _numpad_press(self, label):
        if label == '⌫':
            self._pending_digit = self._pending_digit[:-1]
        elif label == '✓':
            self._submit()
        elif label.isdigit():
            self._pending_digit = label
            self._submit()
        self._redraw()

    def _build_right(self, parent):
        p = tk.Frame(parent, bg=WHITE)
        p.pack(fill='both', expand=True, padx=12, pady=16)

        tk.Label(p, text="АЛГОРИТМ", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 10, "bold")).pack(anchor='w', pady=(0,6))

        self._rule_frames = {}
        rules = {
            '÷': ("Ділення (куточок)",
                  "1. Виділи неповне ділене.\n"
                  "2. Підбери цифру частки.\n"
                  "3. Помнож і відніми.\n"
                  "4. Знеси наступну цифру.\n"
                  "5. Повторюй до кінця.",
                  "126 ÷ 3 = 42"),
            '÷R': ("Ділення з остачею",
                   "Все так само, як у звичайному діленні.\n"
                   "Але в кінці залишається число,\n"
                   "менше за дільник (остача).",
                   "14 ÷ 3 = 4 (ост. 2)"),
            '×': ("Множення",
                  "1. Множимо на одиниці.\n"
                  "2. Множимо на десятки (зсув).\n"
                  "3. Додаємо результати.\n"
                  "Не забувай про переноси!",
                  "23 × 14 = 322"),
            '+': ("Додавання",
                  "1. Пиши розряд під розрядом.\n"
                  "2. Додавай справа наліво.\n"
                  "3. Якщо ≥ 10, перенос у наступний розряд.",
                  "370 + 145 = 515"),
            '−': ("Віднімання",
                  "1. Пиши розряд під розрядом.\n"
                  "2. Віднімай справа наліво.\n"
                  "3. Якщо менше, позичай десяток.",
                  "530 − 274 = 256"),
        }
        for op, (title, text, example) in rules.items():
            f = tk.Frame(p, bg=WHITE)
            tk.Label(f, text=title, bg=WHITE, fg=TEXT,
                     font=("Segoe UI", 11, "bold")).pack(anchor='w')
            tk.Label(f, text=text, bg=WHITE, fg=TEXT,
                     font=("Segoe UI", 10), justify='left',
                     wraplength=210).pack(anchor='w', pady=(4,0))
            ex_f = tk.Frame(f, bg='#f5f3ef',
                            highlightbackground=BORDER, highlightthickness=1)
            ex_f.pack(fill='x', pady=(8,0))
            tk.Label(ex_f, text=example, bg='#f5f3ef', fg=YELLOW,
                     font=("Courier New", 11, "bold"),
                     justify='left').pack(anchor='w', padx=8, pady=6)
            self._rule_frames[op] = f

        tk.Frame(p, bg=BORDER, height=1).pack(fill='x', pady=15)

        tk.Label(p, text="ПРОГРЕС", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 10, "bold")).pack(anchor='w', pady=(0,4))
        self._prog_lbl = tk.Label(p, text="0%", bg=WHITE, fg=MUTED,
                                  font=FONT_SMALL)
        self._prog_lbl.pack(anchor='e')
        prog_outer = tk.Frame(p, bg=BORDER, height=10)
        prog_outer.pack(fill='x')
        self._prog_inner = tk.Frame(prog_outer, bg=ACC, height=10)
        self._prog_inner.place(x=0, y=0, relheight=1, relwidth=0)

        tk.Frame(p, bg=BORDER, height=1).pack(fill='x', pady=15)

        tk.Button(p, text="💡 Підказка",
                  bg=WHITE, fg=MUTED, font=FONT_UI_B,
                  relief='flat', bd=0, cursor='hand2',
                  padx=12, pady=10,
                  highlightbackground=BORDER2, highlightthickness=1,
                  command=self._give_hint).pack(fill='x')

        self._show_rule('÷')

    def _set_op(self, op):
        self.op = op
        self._update_left_buttons()
        self._show_rule(op)
        self._new_task()

    def _set_diff(self, d):
        self.diff = d
        self._update_left_buttons()
        self._new_task()

    def _update_left_buttons(self):
        for op, (btn, fg_c, bg_c) in self._op_btns.items():
            if op == self.op:
                btn.config(bg=bg_c, fg=fg_c, highlightbackground=fg_c)
            else:
                btn.config(bg=WHITE, fg=MUTED, highlightbackground=BORDER)
        for d, (btn, col) in self._diff_btns.items():
            if d == self.diff:
                btn.config(fg=col, highlightbackground=col)
            else:
                btn.config(fg=MUTED, highlightbackground=BORDER)

    def _show_rule(self, op):
        for f in self._rule_frames.values():
            f.pack_forget()
        if op in self._rule_frames:
            self._rule_frames[op].pack(fill='x', pady=(0,4))

    def _new_task(self):
        self.hint_used = False
        self.task_done = False
        self.step_idx = 0
        self._pending_digit = ''
        self._timer_id = None

        a, b = gen_numbers(self.op, self.diff)

        op_sym = self.op
        if '÷' in op_sym: op_sym = '÷'

        self._lbl_task.config(
            text=f"{a}  {op_sym}  {b}  =  ?",
            fg=TEXT)

        if self.op in ('÷', '÷R'):
            info = build_division(a, b)
            self.matrix, self.order = build_matrix_division(info)
        elif self.op == '×':
            info = build_multiplication(a, b)
            self.matrix, self.order = build_matrix_multiplication(info)
        else:
            info = build_add_sub(a, b, self.op)
            self.matrix, self.order = build_matrix_add_sub(info)

        self._lbl_msg.config(text='')
        self._update_progress()
        self._redraw()
        self._highlight_current()

    def _redraw(self):
        c = self._canvas
        c.delete('all')
        if not self.matrix: return

        n_rows = len(self.matrix)
        n_cols = max(len(row) for row in self.matrix)

        row_h = []
        for r, row in enumerate(self.matrix):
            if any(cell.ctype == CARRY for cell in row):
                row_h.append(CARRY_H)
            elif all(cell.ctype in (LINE, EMPTY) for cell in row):
                row_h.append(10)
            else:
                row_h.append(CELL_H)

        total_h = sum(row_h) + (n_rows - 1) * GAP
        total_w = n_cols * (CELL_W + GAP)

        cw = c.winfo_width()  or 600
        ch = c.winfo_height() or 400
        ox = max(20, (cw - total_w) // 2)
        oy = max(20, (ch - total_h) // 2)

        y = oy
        for r, row in enumerate(self.matrix):
            rh = row_h[r]
            x  = ox
            for cell in row:
                self._draw_cell(c, cell, x, y, CELL_W, rh)
                x += CELL_W + GAP
            y += rh + GAP

        # Pending digit
        if self._pending_digit and self.step_idx < len(self.order):
            pr, pc_idx = self.order[self.step_idx]
            px = ox + pc_idx * (CELL_W + GAP) + CELL_W // 2
            py = oy + sum(row_h[i] + GAP for i in range(pr)) + row_h[pr] // 2
            c.create_text(px, py, text=self._pending_digit,
                          fill=ACC, font=FONT_MONO, anchor='center')

    def _draw_cell(self, c, cell, x, y, w, h):
        t = cell.ctype
        if t == EMPTY: return
        if t == LINE:
            c.create_line(x, y + h//2, x + w, y + h//2, fill=BORDER2, width=3)
            return

        st = cell.state
        
        bg_c, br_c, fg_c = WHITE, BORDER, TEXT
        
        if t in (GIVEN, OP_SYM):
            if t == OP_SYM:
                bg_c = BG
                br_c = BG
                fg_c = OP_COLORS.get(cell.value, (MUTED, WHITE))[0]
            else:
                bg_c = GIVEN_BG
        elif t == CARRY:
            bg_c = CARRY_BG
            br_c = CARRY_C
            fg_c = CARRY_C
        elif t == INPUT:
            if   st == 'idle':       bg_c, br_c, fg_c = WHITE,    BORDER,  WHITE
            elif st == 'active':     bg_c, br_c, fg_c = ACC_BG,   ACC,     ACC
            elif st == 'ok':         bg_c, br_c, fg_c = OK_BG,    GREEN,   OK_FG
            elif st == 'error':      bg_c, br_c, fg_c = ERR_BG,   RED,     ERR_FG
            elif st == 'hint_shown': bg_c, br_c, fg_c = HINT_BG,  YELLOW,  HINT_FG
            else:                    bg_c, br_c, fg_c = WHITE,    BORDER,  TEXT

        # Draw rect
        if t != OP_SYM:
            r_c = 8 if t == INPUT else 4
            self._rrect(c, x, y, x+w, y+h, r_c, bg_c, br_c)

        # Draw text
        tv = ''
        if t in (GIVEN, OP_SYM, CARRY):
            tv = cell.value
        elif t == INPUT:
            if st == 'ok':
                tv = cell.user_val or cell.value
            elif st == 'error':
                tv = cell.user_val or '?' # Show what user typed or ?
            elif st == 'hint_shown':
                tv = cell.value
            elif st == 'active':
                tv = '?'
        
        if tv:
            font = (FONT_MONO_XS if t == CARRY else FONT_MONO_S if t == OP_SYM else FONT_MONO)
            c.create_text(x + w//2, y + h//2, text=tv, fill=fg_c, font=font, anchor='center')

    def _rrect(self, c, x1, y1, x2, y2, r, fill, outline, width=1):
        c.create_polygon(
            x1+r,y1, x2-r,y1, x2,y1,
            x2,y1+r, x2,y2-r, x2,y2,
            x2-r,y2, x1+r,y2, x1,y2,
            x1,y2-r, x1,y1+r, x1,y1,
            smooth=True, fill=fill, outline=outline, width=width)

    def _highlight_current(self):
        for row in self.matrix:
            for cell in row:
                if cell.state == 'active': cell.state = 'idle'

        if self.step_idx < len(self.order):
            r, col = self.order[self.step_idx]
            cell = self.matrix[r][col]
            cell.state = 'active'
            self._lbl_prompt.config(text=cell.hint or "Введіть цифру")
        else:
            self._lbl_prompt.config(text="Завдання виконано!")

        total = len(self.order)
        done  = self.step_idx
        self._lbl_step.config(text=(f"Крок {done+1}/{total}" if done < total else f"✓ {total}"))
        self._update_progress()
        self._redraw()

    def _submit(self):
        if self.task_done or self.step_idx >= len(self.order): return
        
        # Cancel any pending reset
        if self._timer_id:
            self.after_cancel(self._timer_id)
            self._timer_id = None
            
        val = self._pending_digit.strip()
        if not val: return
        self._pending_digit = ''

        r, col = self.order[self.step_idx]
        cell = self.matrix[r][col]
        expected = cell.value

        if val == expected:
            cell.state = 'ok'
            cell.user_val = val
            self.step_idx += 1
            self._lbl_msg.config(text='')
            if self.step_idx >= len(self.order):
                self._finish(True)
            else:
                self._highlight_current()
        else:
            cell.state = 'error'
            cell.user_val = val # Keep the wrong answer visible
            self._lbl_msg.config(text="✗ Помилка", fg=RED)
            self._redraw()
            self._timer_id = self.after(700, lambda: self._reset_active(r, col))

    def _reset_active(self, r, col):
        self._timer_id = None
        # Don't reset if user already corrected it
        if r < len(self.matrix) and col < len(self.matrix[r]):
            if self.matrix[r][col].state == 'ok':
                return
            self.matrix[r][col].state = 'active'
        self._lbl_msg.config(text='')
        self._redraw()

    def _give_hint(self):
        if self.task_done or self.step_idx >= len(self.order): return
        r, col = self.order[self.step_idx]
        cell = self.matrix[r][col]
        cell.state = 'hint_shown'
        cell.user_val = cell.value
        self.hint_used = True
        self._lbl_msg.config(text=f"💡 Відповідь: {cell.value}", fg=YELLOW)
        self._redraw()
        self.after(1200, self._accept_hint)

    def _accept_hint(self):
        if self.step_idx >= len(self.order): return
        r, col = self.order[self.step_idx]
        self.matrix[r][col].state = 'ok'
        self.step_idx += 1
        self._pending_digit = ''
        if self.step_idx >= len(self.order):
            self._finish(False)
        else:
            self._highlight_current()
            self._lbl_msg.config(text='')

    def _finish(self, perfect):
        self.task_done = True
        self.score_all += 1
        if perfect and not self.hint_used:
            self.score_ok += 1
            self.streak += 1
        else:
            self.streak = 0

        streak_txt = f"  🔥×{self.streak}" if self.streak >= 3 else ""
        self._lbl_score.config(text=f"Вірно: {self.score_ok} / {self.score_all}{streak_txt}")
        self._update_progress()
        self._highlight_current()

        if perfect and not self.hint_used:
            msg, col = f"🎉 Чудово!", GREEN
        elif perfect:
            msg, col = "✓ Правильно! (з підказкою)", YELLOW
        else:
            msg, col = "✓ Виконано!", ORANGE

        self._lbl_msg.config(text=msg, fg=col)
        self._lbl_step.config(text="✓")
        self._lbl_prompt.config(text="Натисніть ↺ Нове завдання")

    def _update_progress(self):
        total = len(self.order)
        done  = self.step_idx
        pct   = done / total if total > 0 else 0
        self._prog_inner.place(relwidth=pct)
        self._prog_lbl.config(text=f"{int(pct*100)}%")


if __name__ == '__main__':
    App().mainloop()
