"""
Тренажер обчислень у стовпчик — десяткові дроби.
"""

import tkinter as tk
import tkinter.font as tkf
import random

# ══════════════════════════════════════════════════════════════════
#  ПАЛИТРА
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
             '÷': ('#1e3a8a','#dbeafe')}

CELL_W  = 52
CELL_H  = 52
CARRY_H = 20
GAP     = 6

FONT_TASK   = ("Segoe UI",    48, "bold")
FONT_MONO   = ("Courier New", 26, "bold")
FONT_MONO_S = ("Courier New", 16, "bold")
FONT_MONO_XS= ("Courier New", 12, "bold")
FONT_HDR    = ("Segoe UI",    16, "bold")
FONT_UI_B   = ("Segoe UI",    12, "bold")
FONT_UI     = ("Segoe UI",    12)
FONT_SMALL  = ("Segoe UI",    10)
FONT_HINT_T = ("Segoe UI",    11, "italic")
FONT_PAD    = ("Segoe UI",    22, "bold")

# ══════════════════════════════════════════════════════════════════
#  МАТЕМАТИКА
# ══════════════════════════════════════════════════════════════════
def fmt(n):
    if n == int(n): return str(int(n))
    return str(round(n, 10)).rstrip('0').rstrip('.')

def dec_len(n):
    s = fmt(n)
    d = s.find('.')
    return 0 if d == -1 else len(s) - d - 1

def aligned(n, dp):
    s = fmt(n)
    if dp == 0: return s
    if '.' not in s: s += '.'
    cur = len(s) - s.index('.') - 1
    return s + '0' * (dp - cur)

def rnd(a, b):
    return random.randint(a, b)

def gen_numbers(op, diff):
    if op == '÷':
        if diff == 'easy':
            divs =[2, 4, 5]
            b_int = random.choice(divs)
            dp = 1
            q = rnd(2, 9)
            shift = 0
        elif diff == 'med':
            divs =[3, 4, 5, 6, 8, 12, 15]
            b_int = random.choice(divs)
            dp = rnd(1, 2)
            q = rnd(11, 99)
            shift = random.choice([0, 1])
        else:
            divs =[7, 8, 9, 14, 16, 25, 35, 45, 125]
            b_int = random.choice(divs)
            dp = rnd(1, 3)
            q = rnd(101, 999)
            shift = random.choice([1, 2])

        a_int = q * b_int
        a = a_int / 10**dp
        b = b_int
        if shift > 0:
            a_orig = round(a / 10**shift, dp + shift)
            b_orig = round(b / 10**shift, shift)
        else:
            a_orig, b_orig = a, b
        return a_orig, b_orig

    if op == '×':
        dp1 = 1 if diff=='easy' else rnd(1,2)
        dp2 = 1 if diff=='easy' else rnd(1,2)
        ma  = 9 if diff=='easy' else (45 if diff=='med' else 99)
        mb  = 9 if diff=='easy' else (25 if diff=='med' else 45)
        a = round(rnd(2, ma * 10**dp1) / 10**dp1, dp1)
        b = round(rnd(2, mb * 10**dp2) / 10**dp2, dp2)
        return a, b

    # Сложение / Вычитание
    dp1 = 1 if diff=='easy' else rnd(1,3)
    dp2 = 1 if diff=='easy' else rnd(1,3)
    # З більшою ймовірністю генеруємо різну кількість знаків після коми
    if diff != 'easy' and random.random() < 0.7:
        while dp1 == dp2: dp2 = rnd(1,3)

    mv  = 9 if diff=='easy' else (50 if diff=='med' else 300)
    a = round(rnd(1, mv * 10**dp1) / 10**dp1, dp1)
    b = round(rnd(1, mv * 10**dp2) / 10**dp2, dp2)
    if op == '−' and b > a:
        a, b = b, a
    return a, b

# ── Деление ──────────────────────────────────────────────────────
def build_division(a, b):
    b_str = fmt(b)
    shift = len(b_str) - b_str.index('.') - 1 if '.' in b_str else 0
    a_shift = round(a * 10**shift, 10)
    b_shift = int(round(b * 10**shift, 10))

    a_str     = fmt(a_shift)
    a_dot     = a_str.find('.')
    a_dig_str = a_str.replace('.', '')
    n_dig     = len(a_dig_str)
    dot_pos   = n_dig if a_dot == -1 else a_dot

    div_steps =[]
    rem = 0
    started = False
    for i, ch in enumerate(a_dig_str):
        rem = rem * 10 + int(ch)
        if not started and rem < b_shift and i < dot_pos - 1:
            continue
        started = True
        digit   = rem // b_shift
        prod    = digit * b_shift
        new_rem = rem - prod
        div_steps.append({'k': i, 'dig_col': i, 'rem': rem, 'digit': digit, 'prod': prod, 'new_rem': new_rem})
        rem = new_rem

    extra = 0
    while rem != 0 and extra < 8:
        rem = rem * 10
        k = n_dig + extra
        digit   = rem // b_shift
        prod    = digit * b_shift
        new_rem = rem - prod
        div_steps.append({'k': k, 'dig_col': k, 'rem': rem, 'digit': digit, 'prod': prod, 'new_rem': new_rem})
        rem = new_rem
        extra += 1

    return {
        'a_orig': a, 'b_orig': b,
        'a_shift': a_shift, 'b_shift': b_shift,
        'a_shift_str': a_str, 'b_shift_str': fmt(b_shift),
        'a_dig_str': a_dig_str,
        'div_steps': div_steps,
        'q_str': fmt(a_shift / b_shift),
    }

# ── Умножение ──────────────────────────────────────────────────────
def build_multiplication(a, b):
    dp1, dp2 = dec_len(a), dec_len(b)
    dpR = dp1 + dp2
    aI  = round(a * 10**dp1)
    bI  = round(b * 10**dp2)
    rI  = aI * bI
    partials =[]
    for i, d in enumerate(reversed(str(bI))):
        partials.append({'val': aI * int(d), 'shift': i, 'dgt': int(d)})
    return {
        'a': a, 'b': b, 'aI': aI, 'bI': bI, 'rI': rI,
        'dp1': dp1, 'dp2': dp2, 'dpR': dpR,
        'partials': partials,
        'result': rI / 10**dpR,
        'a_str': fmt(a), 'b_str': fmt(b), 'r_str': fmt(rI / 10**dpR),
    }

# ── Сложение / Вычитание ─────────────────────────────────────────
def build_add_sub(a, b, op):
    result = round(a + b, 10) if op == '+' else round(a - b, 10)
    dp   = max(dec_len(a), dec_len(b))
    mul  = 10**dp
    aI   = round(a * mul)
    bI   = round(b * mul)
    rI   = round(result * mul)
    a_al = aligned(a, dp)
    b_al = aligned(b, dp)
    r_al = aligned(result, dp)
    ml   = max(len(a_al), len(b_al), len(r_al))

    return {
        'a': a, 'b': b, 'result': result, 'op': op,
        'a_al': a_al, 'b_al': b_al, 'r_al': r_al,
        'dp': dp, 'max_len': ml,
        'a_str': fmt(a), 'b_str': fmt(b), 'r_str': fmt(result)
    }

# ══════════════════════════════════════════════════════════════════
#  ТИПЫ КЛЕТОК
# ══════════════════════════════════════════════════════════════════
EMPTY  = 'empty'
GIVEN  = 'given'
INPUT  = 'input'
OP_SYM = 'op'
LINE   = 'line'
VLINE  = 'vline'

class Cell:
    def __init__(self, ctype=EMPTY, value='', row=0, col=0, hint='', phase=1):
        self.ctype    = ctype
        self.value    = value
        self.row      = row
        self.col      = col
        self.hint     = hint
        self.state    = 'idle'
        self.user_val = ''
        self.has_dot  = False
        self.phase    = phase  # Для поэтапного отображения

def _make_matrix(nrows, ncols):
    return [[Cell(EMPTY, row=r, col=c) for c in range(ncols)] for r in range(nrows)]

def _fix_coords(matrix):
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            cell.row = r; cell.col = c

# ── Деление ───────────────────────────────────────────────
def build_matrix_division(info):
    div_steps = info['div_steps']
    b         = info['b_shift']
    n_steps   = len(div_steps)

    q_chars = list(info['q_str'])
    if '.' in q_chars:
        di = q_chars.index('.')
        ip, fp = q_chars[:di], q_chars[di:]
        while len(ip) > 1 and ip[0] == '0': ip = ip[1:]
        q_chars = ip + fp
        q_clean = [ch for ch in q_chars if ch != '.']
    else:
        while len(q_chars) > 1 and q_chars[0] == '0':
            q_chars = q_chars[1:]
        q_clean = list(q_chars)

    q_dot_idx = q_chars.index('.') if '.' in q_chars else -1

    max_used = max([s['dig_col'] + 1 for s in div_steps] + [0])
    left_w = max(len(info['a_dig_str']), max_used) + 1
    right_w = max(len(info['b_shift_str']), len(q_clean)) + 1
    SEP = left_w
    total_cols = SEP + 1 + right_w

    has_shift = (info['b_orig'] != info['b_shift'])
    shift_offset = 3 if has_shift else 0
    n_rows = shift_offset + 3 + (n_steps - 1) * 3 + 1

    matrix = _make_matrix(n_rows, max(total_cols, 16))
    input_order =[]

    if has_shift:
        a_o_s = fmt(info['a_orig']).replace('.', ',')
        b_o_s = fmt(info['b_orig']).replace('.', ',')
        a_s_s = fmt(info['a_shift']).replace('.', ',')
        b_s_s = fmt(info['b_shift']).replace('.', ',')

        c = 0
        for ch in a_o_s: matrix[0][c] = Cell(GIVEN, ch); c+=1
        matrix[0][c] = Cell(EMPTY); c+=1
        matrix[0][c] = Cell(OP_SYM, '÷'); c+=1
        matrix[0][c] = Cell(EMPTY); c+=1
        for ch in b_o_s: matrix[0][c] = Cell(GIVEN, ch); c+=1
        matrix[0][c] = Cell(EMPTY); c+=1
        matrix[0][c] = Cell(OP_SYM, '='); c+=1

        c = 0
        for ch in a_s_s:
            matrix[1][c] = Cell(INPUT, ch, hint="Перенесіть кому в діленому (введіть цифру або кому)")
            input_order.append((1, c))
            c+=1
        matrix[1][c] = Cell(EMPTY); c+=1
        matrix[1][c] = Cell(OP_SYM, '÷'); c+=1
        matrix[1][c] = Cell(EMPTY); c+=1
        for ch in b_s_s:
            matrix[1][c] = Cell(INPUT, ch, hint="Перенесіть кому в дільнику (щоб він став цілим)")
            input_order.append((1, c))
            c+=1

    R = shift_offset
    matrix[R][SEP] = Cell(VLINE)
    matrix[R + 1][SEP] = Cell(VLINE)
    matrix[R + 2][SEP] = Cell(VLINE)

    a_dot_idx = info['a_shift_str'].find('.')
    for i, ch in enumerate(info['a_dig_str']):
        cell = Cell(GIVEN, ch)
        if a_dot_idx != -1 and i == a_dot_idx - 1: cell.has_dot = True
        matrix[R][i] = cell

    for i, ch in enumerate(info['b_shift_str']):
        matrix[R][SEP + 1 + i] = Cell(GIVEN, ch)

    for c in range(SEP + 1, total_cols):
        matrix[R + 1][c] = Cell(LINE, '')

    q_cell_map = {}
    for i, ch in enumerate(q_clean):
        cell = Cell(INPUT, ch, hint="Цифра частки")
        if q_dot_idx != -1 and i == q_dot_idx - 1: cell.has_dot = True
        matrix[R + 2][SEP + 1 + i] = cell
        q_cell_map[i] = (R + 2, SEP + 1 + i)

    def place_number_input(row, num_str, right_col, hint_text):
        w = len(num_str)
        left_col = max(0, right_col - w + 1)
        for i, ch in enumerate(num_str):
            col = left_col + i
            if 0 <= col < SEP:
                matrix[row][col] = Cell(INPUT, ch, hint=hint_text)

    s0 = div_steps[0]
    prod_row0 = R + 1
    place_number_input(prod_row0, str(s0['prod']), s0['dig_col'], f"Множимо {s0['digit']} на {b}")
    line_row0 = R + 2
    w_line0 = max(len(str(s0['prod'])), len(str(s0['rem'])))
    for c in range(max(0, s0['dig_col'] - w_line0 + 1), s0['dig_col'] + 1):
        matrix[line_row0][c] = Cell(LINE, '')

    step_row_info =[{'k': 0, 'prod_row': prod_row0, 'snoska_row': None}]
    cur_row = R + 3

    for k in range(1, n_steps):
        s = div_steps[k]
        right = s['dig_col']

        snoska_row = cur_row
        place_number_input(snoska_row, str(s['rem']), right, "Остача + зносимо цифру")
        cur_row += 1

        prod_row = cur_row
        place_number_input(prod_row, str(s['prod']), right, f"Множимо {s['digit']} на {b}")
        cur_row += 1

        line_row = cur_row
        w_line = max(len(str(s['prod'])), len(str(s['rem'])))
        for c in range(max(0, right - w_line + 1), right + 1):
            matrix[line_row][c] = Cell(LINE, '')
        cur_row += 1
        step_row_info.append({'k': k, 'prod_row': prod_row, 'snoska_row': snoska_row})

    final_rem = str(div_steps[-1]['new_rem'])
    right_f = div_steps[-1]['dig_col']
    place_number_input(cur_row, final_rem, right_f, "Кінцева нульова остача")
    f_rem_c = max(0, right_f - len(final_rem) + 1)
    final_rem_cells =[(cur_row, f_rem_c + i) for i in range(len(final_rem))]

    input_order.append(q_cell_map[0])
    for c in range(SEP):
        if matrix[step_row_info[0]['prod_row']][c].ctype == INPUT:
            input_order.append((step_row_info[0]['prod_row'], c))

    for k in range(1, n_steps):
        for c in range(SEP):
            if matrix[step_row_info[k]['snoska_row']][c].ctype == INPUT:
                input_order.append((step_row_info[k]['snoska_row'], c))
        if k in q_cell_map: input_order.append(q_cell_map[k])
        for c in range(SEP):
            if matrix[step_row_info[k]['prod_row']][c].ctype == INPUT:
                input_order.append((step_row_info[k]['prod_row'], c))

    input_order.extend(final_rem_cells)

    # Скриваємо стовпчик до завершення перетворення (переходу в фазу 2)
    if has_shift:
        for r in range(R, n_rows):
            for c in range(len(matrix[r])):
                if matrix[r][c]:
                    matrix[r][c].phase = 2

    _fix_coords(matrix)
    return matrix, input_order

# ── Сложение / Вычитание ─────────────────────────────────────────
def build_matrix_add_sub(info):
    a_clean = info['a_al'].replace('.', '')
    b_clean = info['b_al'].replace('.', '')
    r_clean = info['r_al'].replace('.', '')
    op = info['op']
    dp = info['dp']
    ml = max(len(a_clean), len(b_clean), len(r_clean))

    pad_a = dp - dec_len(info['a'])
    pad_b = dp - dec_len(info['b'])

    SIGN = 0; DS = 1; tc = DS + ml
    matrix = _make_matrix(5, tc)
    a_p = a_clean.rjust(ml); b_p = b_clean.rjust(ml); r_p = r_clean.rjust(ml)

    def place_row(ri, s_clean, is_input=False, sign_ch='', pad_count=0):
        if sign_ch: matrix[ri][SIGN] = Cell(OP_SYM, sign_ch)
        cells = []
        pad_cells =[]
        n = len(s_clean)
        for i, ch in enumerate(s_clean):
            c = DS + i
            if ch == ' ': continue

            is_pad = (pad_count > 0 and i >= n - pad_count)

            if is_input:
                ctype = INPUT
                hint_txt = "Додаємо розряд" if op == '+' else "Віднімаємо розряд"
            elif is_pad:
                ctype = INPUT
                hint_txt = "Зрівняйте кількість знаків (додайте 0)"
            else:
                ctype = GIVEN
                hint_txt = ""

            cell = Cell(ctype, ch, hint=hint_txt)
            if dp > 0 and i == ml - 1 - dp: cell.has_dot = True
            matrix[ri][c] = cell

            if is_input: cells.append((ri, c))
            elif is_pad: pad_cells.append((ri, c))
        return cells, pad_cells

    _, pad_cells_a = place_row(1, a_p, pad_count=pad_a)
    _, pad_cells_b = place_row(2, b_p, sign_ch=op, pad_count=pad_b)
    for c in range(tc): matrix[3][c] = Cell(LINE, '')
    res_cells, _ = place_row(4, r_p, is_input=True)

    input_order =[]
    input_order.extend(pad_cells_a)
    input_order.extend(pad_cells_b)
    input_order.extend(list(reversed(res_cells)))

    _fix_coords(matrix)
    return matrix, input_order

# ── Умножение ─────────────────────────────────────────────────────
def build_matrix_multiplication(info):
    a_str = info['a_str']; b_str = info['b_str']
    a_clean = a_str.replace('.', ''); b_clean = b_str.replace('.', '')
    partials = info['partials']; dpR = info['dpR']

    def format_mult_result(rI, dp_r):
        if dp_r == 0: return str(abs(rI))
        s = str(abs(rI)).zfill(dp_r + 1)
        return s[:-dp_r] + '.' + s[-dp_r:]

    r_str_matrix = format_mult_result(info['rI'], dpR)
    r_clean = r_str_matrix.replace('.', '')
    np_ = len(partials)
    mw = max(len(a_clean), len(b_clean), max(len(str(p['val'])) + p['shift'] for p in partials), len(r_clean)) + 2
    tc = mw + 1

    def place_with_dot_str(ri, s, right_col, sign_ch='', is_input=False, hint_text=""):
        if sign_ch: matrix[ri][0] = Cell(OP_SYM, sign_ch)
        dot_idx = s.find('.')
        clean_s = s.replace('.', '')
        chars_after_dot = len(s) - dot_idx - 1 if dot_idx != -1 else 0
        cells =[]
        for i, ch in enumerate(reversed(clean_s)):
            col = right_col - i
            if 0 <= col < tc:
                ctype = INPUT if is_input else GIVEN
                cell = Cell(ctype, ch, hint=hint_text if is_input else "")
                if dot_idx != -1 and i == chars_after_dot: cell.has_dot = True
                matrix[ri][col] = cell
                if is_input: cells.append((ri, col))
        return cells

    if np_ == 1:
        n_rows = 4
        matrix = _make_matrix(n_rows, tc)
        place_with_dot_str(0, a_str, tc - 1)
        place_with_dot_str(1, b_str, tc - 1, '×')
        for c in range(tc): matrix[2][c] = Cell(LINE, '')
        tot_cells = place_with_dot_str(3, r_str_matrix, tc - 1, is_input=True, hint_text="Обчислюємо добуток")
        input_order = tot_cells
    else:
        n_rows = 3 + np_ + 2
        matrix = _make_matrix(n_rows, tc)
        place_with_dot_str(0, a_str, tc - 1)
        place_with_dot_str(1, b_str, tc - 1, '×')
        for c in range(tc): matrix[2][c] = Cell(LINE, '')

        part_cells =[]
        for k, p in enumerate(partials):
            ri = 3 + k
            p_str = str(p['val'])
            for i, ch in enumerate(reversed(p_str)):
                col = tc - 1 - p['shift'] - i
                if 0 <= col < tc:
                    cell = Cell(INPUT, ch, hint="Обчислюємо добуток")
                    matrix[ri][col] = cell
                    part_cells.append((ri, col))

        line_row = 3 + np_
        for c in range(tc): matrix[line_row][c] = Cell(LINE, '')
        tot_cells = place_with_dot_str(line_row + 1, r_str_matrix, tc - 1, is_input=True, hint_text="Додаємо стовпчик")

        input_order =[]
        rg = {}
        for (r, c) in part_cells: rg.setdefault(r,[]).append((r, c))
        for r in sorted(rg): input_order.extend(rg[r])
        input_order.extend(tot_cells)

    _fix_coords(matrix)
    return matrix, input_order


# ══════════════════════════════════════════════════════════════════
#  ГЛАВНОЕ ПРИЛОЖЕНИЕ
# ══════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Тренажер — Стовпчик")
        self.configure(bg=BG)
        self.resizable(True, True)

        self.op        = '÷'
        self.diff      = 'med'
        self.score_ok  = 0
        self.score_all = 0
        self.streak    = 0
        self.matrix    = []
        self.order     =[]
        self.step_idx  = 0
        self.hint_used = False
        self.task_done = False
        self._pending_digit = ''
        self.expected_answer_str = ''
        self.current_phase = 1

        self._build_ui()
        self._new_task()
        self.bind('<Escape>', lambda e: self.attributes('-fullscreen', False))
        self.bind('<Key>', self._block_keyboard)

    def _block_keyboard(self, event): return 'break'

    def _build_ui(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = min(1400, sw), min(900, sh)
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.minsize(960, 640)

        hdr = tk.Frame(self, bg=HDR_BG, height=50)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)
        tk.Label(hdr, text="÷  Тренажер — Стовпчик", bg=HDR_BG, fg=WHITE, font=FONT_HDR).place(x=18, rely=.5, anchor='w')
        self._lbl_score = tk.Label(hdr, text="Вірно: 0 / 0", bg=HDR_BG, fg='#a1a1aa', font=FONT_UI)
        self._lbl_score.place(relx=1, x=-18, rely=.5, anchor='e')

        body = tk.Frame(self, bg=BG)
        body.pack(fill='both', expand=True)

        left = tk.Frame(body, bg=WHITE, width=190, highlightbackground=BORDER, highlightthickness=1)
        left.pack(side='left', fill='y')
        left.pack_propagate(False)
        self._build_left(left)

        right = tk.Frame(body, bg=WHITE, width=210, highlightbackground=BORDER, highlightthickness=1)
        right.pack(side='right', fill='y')
        right.pack_propagate(False)
        self._build_right(right)

        center = tk.Frame(body, bg=BG)
        center.pack(side='left', fill='both', expand=True)
        self._build_center(center)

    def _build_left(self, parent):
        p = tk.Frame(parent, bg=WHITE)
        p.pack(fill='both', expand=True, padx=12, pady=16)

        tk.Label(p, text="ОПЕРАЦІЯ", bg=WHITE, fg=MUTED, font=("Segoe UI", 10, "bold")).pack(anchor='w', pady=(0,6))
        self._op_btns = {}
        for op, label in[('÷','Ділення'),('×','Множення'), ('+','Додавання'),('−','Віднімання')]:
            fg_c, bg_c = OP_COLORS[op]
            btn = tk.Button(p, text=f"  {op}  {label}", bg=WHITE, fg=MUTED, font=FONT_UI_B,
                            relief='flat', bd=0, cursor='hand2', anchor='w', padx=8, pady=7,
                            highlightbackground=BORDER, highlightthickness=1, command=lambda o=op: self._set_op(o))
            btn.pack(fill='x', pady=2)
            self._op_btns[op] = (btn, fg_c, bg_c)

        tk.Frame(p, bg=BORDER, height=1).pack(fill='x', pady=10)

        tk.Label(p, text="РІВЕНЬ", bg=WHITE, fg=MUTED, font=("Segoe UI", 10, "bold")).pack(anchor='w', pady=(0,6))
        self._diff_btns = {}
        for d, label, col in[('easy','🟢 Легкий', GREEN), ('med', '🟡 Середній', YELLOW), ('hard','🔴 Складний', RED)]:
            btn = tk.Button(p, text=label, bg=WHITE, fg=MUTED, font=FONT_UI_B, relief='flat', bd=0,
                            cursor='hand2', anchor='w', padx=8, pady=7, highlightbackground=BORDER, highlightthickness=1,
                            command=lambda x=d: self._set_diff(x))
            btn.pack(fill='x', pady=2)
            self._diff_btns[d] = (btn, col)

        tk.Frame(p, bg=BORDER, height=1).pack(fill='x', pady=10)
        tk.Button(p, text="↺  Нове завдання", bg=BG, fg=TEXT, font=FONT_UI_B, relief='flat', bd=0, cursor='hand2',
                  padx=8, pady=8, highlightbackground=BORDER2, highlightthickness=1, command=self._new_task).pack(fill='x')

    def _build_center(self, parent):
        task_frame = tk.Frame(parent, bg=WHITE, highlightbackground=BORDER2, highlightthickness=1)
        task_frame.pack(fill='x', padx=16, pady=(14, 6))

        inner_task = tk.Frame(task_frame, bg=WHITE)
        inner_task.pack(pady=14)

        self._lbl_task = tk.Label(inner_task, text="", bg=WHITE, fg=TEXT, font=FONT_TASK)
        self._lbl_task.pack(side='left')

        self._lbl_step = tk.Label(inner_task, text="", bg=WHITE, fg=MUTED, font=("Segoe UI", 13))
        self._lbl_step.pack(side='left', padx=(24, 0))

        canvas_frame = tk.Frame(parent, bg=BG)
        canvas_frame.pack(fill='both', expand=True, padx=16, pady=4)

        self._canvas = tk.Canvas(canvas_frame, bg=WHITE, highlightbackground=BORDER2, highlightthickness=1)
        self._canvas.pack(fill='both', expand=True)
        self._canvas.bind('<Configure>', lambda e: self._redraw())

        self._lbl_prompt = tk.Label(parent, text="", bg=BG, fg=MUTED, font=FONT_HINT_T, wraplength=560, justify='center')
        self._lbl_prompt.pack(pady=(2, 0))

        bottom = tk.Frame(parent, bg=BG)
        bottom.pack(pady=(4, 12))

        self._lbl_msg = tk.Label(bottom, text="", bg=BG, fg=RED, font=FONT_UI_B)
        self._lbl_msg.pack(pady=(0, 6))

        numpad = tk.Frame(bottom, bg=BG)
        numpad.pack()
        self._build_numpad(numpad)

    def _build_numpad(self, parent):
        layout = [['7', '8', '9'],
                  ['4', '5', '6'],['1', '2', '3'],
                  ['⌫', '0', ',']]
        for ri, row in enumerate(layout):
            for ci, label in enumerate(row):
                if label == '⌫': bg_c, fg_c = '#fef2f2', RED
                else: bg_c, fg_c = WHITE, TEXT

                btn = tk.Button(parent, text=label, bg=bg_c, fg=fg_c, font=FONT_PAD, relief='solid', bd=1,
                                cursor='hand2', width=3, highlightbackground=BORDER2, highlightthickness=1,
                                command=lambda l=label: self._numpad_press(l))
                btn.grid(row=ri, column=ci, padx=4, pady=4, ipadx=4, ipady=6)

    def _numpad_press(self, label):
        if label == '⌫':
            self._pending_digit = ''
        elif label.isdigit() or label == ',':
            self._pending_digit = label
            self._submit()
        self._redraw()

    def _build_right(self, parent):
        p = tk.Frame(parent, bg=WHITE)
        p.pack(fill='both', expand=True, padx=10, pady=14)
        tk.Label(p, text="АЛГОРИТМ", bg=WHITE, fg=MUTED, font=("Segoe UI", 10, "bold")).pack(anchor='w', pady=(0,6))
        self._rule_frames = {}
        rules = {
            '÷': ("Ділення у стовпчик", "1. Зробіть дільник цілим.\n2. Беремо цифри зліва.\n3. Скільки разів ділиться?\n4. Кома після цілої частини діленого.", "12,6 ÷ 4 = 3,15"),
            '×': ("Множення у стовпчик", "1. Рахуємо як цілі.\n2. Зсув на 1 вліво кожен рядок.\n3. Складаємо рядки.\n4. Кома = сума знаків.", "2,3×1,4 = 23×14 = 322 → 3,22"),
            '+': ("Додавання у стовпчик", "1. Зрівняйте знаки (додайте 0).\n2. Складаємо справа наліво.\n3. Перенос якщо ≥ 10.", "3,70+1,45 = 5,15"),
            '−': ("Віднімання у стовпчик", "1. Зрівняйте знаки (додайте 0).\n2. Віднімаємо справа наліво.\n3. Позика якщо розряд < 0.", "5,30−2,74 = 2,56"),
        }
        for op, (title, text, example) in rules.items():
            f = tk.Frame(p, bg=WHITE)
            tk.Label(f, text=title, bg=WHITE, fg=TEXT, font=("Segoe UI", 11, "bold")).pack(anchor='w')
            tk.Label(f, text=text, bg=WHITE, fg=TEXT, font=("Segoe UI", 10), justify='left', wraplength=185).pack(anchor='w', pady=(4,0))
            self._rule_frames[op] = f

        tk.Frame(p, bg=BORDER, height=1).pack(fill='x', pady=10)
        tk.Label(p, text="ПРОГРЕС", bg=WHITE, fg=MUTED, font=("Segoe UI", 10, "bold")).pack(anchor='w', pady=(0,4))
        self._prog_lbl = tk.Label(p, text="0%", bg=WHITE, fg=MUTED, font=FONT_SMALL)
        self._prog_lbl.pack(anchor='e')
        prog_outer = tk.Frame(p, bg=BORDER, height=8)
        prog_outer.pack(fill='x')
        self._prog_inner = tk.Frame(prog_outer, bg=ACC, height=8)
        self._prog_inner.place(x=0, y=0, relheight=1, relwidth=0)

        tk.Frame(p, bg=BORDER, height=1).pack(fill='x', pady=10)
        tk.Button(p, text="💡 Підказка", bg=WHITE, fg=MUTED, font=FONT_UI_B, relief='flat', bd=0, cursor='hand2',
                  padx=12, pady=8, highlightbackground=BORDER2, highlightthickness=1, command=self._give_hint).pack(fill='x')

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
            if op == self.op: btn.config(bg=bg_c, fg=fg_c, highlightbackground=fg_c)
            else: btn.config(bg=WHITE, fg=MUTED, highlightbackground=BORDER)
        for d, (btn, col) in self._diff_btns.items():
            if d == self.diff: btn.config(fg=col, highlightbackground=col)
            else: btn.config(fg=MUTED, highlightbackground=BORDER)

    def _show_rule(self, op):
        for f in self._rule_frames.values(): f.pack_forget()
        if op in self._rule_frames: self._rule_frames[op].pack(fill='x', pady=(0,4))

    def _new_task(self):
        self.hint_used = False
        self.task_done = False
        self.step_idx = 0
        self._pending_digit = ''

        a, b = gen_numbers(self.op, self.diff)
        a_disp = fmt(a).replace('.', ',')
        b_disp = fmt(b).replace('.', ',')
        self._lbl_task.config(text=f"{a_disp}  {self.op}  {b_disp}  =  ?", fg=TEXT)

        if self.op == '÷':
            info = build_division(a, b)
            self.expected_answer_str = info['q_str']
            self.matrix, self.order = build_matrix_division(info)
        elif self.op == '×':
            info = build_multiplication(a, b)
            self.expected_answer_str = info['r_str']
            self.matrix, self.order = build_matrix_multiplication(info)
        else:
            info = build_add_sub(a, b, self.op)
            self.expected_answer_str = info['r_str']
            self.matrix, self.order = build_matrix_add_sub(info)

        if self.order:
            first_r, first_c = self.order[0]
            self.current_phase = self.matrix[first_r][first_c].phase
        else:
            self.current_phase = 1

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

        row_h =[10 if all(cell.ctype in (LINE, EMPTY) for cell in row) else CELL_H for row in self.matrix]
        total_h = sum(row_h) + (n_rows - 1) * GAP
        total_w = n_cols * (CELL_W + GAP)

        cw, ch = c.winfo_width() or 600, c.winfo_height() or 400
        ox, oy = max(16, (cw - total_w) // 2), max(16, (ch - total_h) // 2)

        y = oy
        for r, row in enumerate(self.matrix):
            rh = row_h[r]
            x = ox
            for cell in row:
                if cell.phase <= self.current_phase:
                    self._draw_cell(c, cell, x, y, CELL_W, rh)
                x += CELL_W + GAP
            y += rh + GAP

        if self._pending_digit and self.step_idx < len(self.order):
            pr, pc_idx = self.order[self.step_idx]
            px = ox + pc_idx * (CELL_W + GAP) + CELL_W // 2
            py = oy + sum(row_h[i] + GAP for i in range(pr)) + row_h[pr] // 2
            c.create_text(px, py, text=self._pending_digit, fill=ACC, font=FONT_MONO, anchor='center')

    def _draw_cell(self, c, cell, x, y, w, h):
        t = cell.ctype
        if t == EMPTY: return
        if t == LINE:
            c.create_line(x, y + h//2, x + w, y + h//2, fill=BORDER2, width=2)
            return
        if t == VLINE:
            c.create_line(x + w//2, y - GAP, x + w//2, y + h + GAP, fill=BORDER2, width=2)
            return

        st = cell.state
        if t in (GIVEN, OP_SYM):
            if t == OP_SYM: bg_c, br_c, fg_c = BG, BG, OP_COLORS[cell.value][0] if cell.value in OP_COLORS else MUTED
            else: bg_c, br_c, fg_c = GIVEN_BG, BORDER, TEXT
        elif t == INPUT:
            if   st == 'idle':       bg_c, br_c, fg_c = WHITE,    BORDER,  WHITE
            elif st == 'active':     bg_c, br_c, fg_c = ACC_BG,   ACC,     ACC
            elif st == 'ok':         bg_c, br_c, fg_c = OK_BG,    GREEN,   OK_FG
            elif st == 'error':      bg_c, br_c, fg_c = ERR_BG,   RED,     ERR_FG
            elif st == 'hint_shown': bg_c, br_c, fg_c = HINT_BG,  YELLOW,  HINT_FG
            else:                    bg_c, br_c, fg_c = WHITE,    BORDER,  TEXT
        else:
            bg_c, br_c, fg_c = WHITE, BORDER, TEXT

        if t != OP_SYM:
            r_c = 5 if t == INPUT else 3
            c.create_polygon(x+r_c,y, x+w-r_c,y, x+w,y, x+w,y+r_c, x+w,y+h-r_c, x+w,y+h, x+w-r_c,y+h, x+r_c,y+h, x,y+h, x,y+h-r_c, x,y+r_c, x,y, smooth=True, fill=bg_c, outline=br_c, width=1)

        tv = ''
        if t in (GIVEN, OP_SYM): tv = cell.value
        elif t == INPUT:
            if st in ('ok', 'error', 'hint_shown'): tv = cell.user_val or cell.value
            elif st == 'active': tv = '?'

        if tv:
            c.create_text(x + w//2, y + h//2, text=tv, fill=fg_c, font=FONT_MONO_S if t == OP_SYM else FONT_MONO, anchor='center')

        if cell.has_dot:
            c.create_text(x + w + GAP//2, y + h - 10, text=',', fill=ORANGE, font=FONT_MONO, anchor='center')

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
        self._lbl_step.config(text=(f"крок {self.step_idx+1}/{total}" if self.step_idx < total else f"✓ {total} кроків"))
        self._update_progress()
        self._redraw()

    def _submit(self):
        if self.task_done or self.step_idx >= len(self.order): return
        val = self._pending_digit.strip()
        if not val: return
        self._pending_digit = ''

        r, col = self.order[self.step_idx]
        cell = self.matrix[r][col]

        cell.user_val = val
        if val == cell.value:
            cell.state = 'ok'
            self.step_idx += 1
            self._lbl_msg.config(text='')
            if self.step_idx >= len(self.order):
                self._finish(True)
            else:
                next_r, next_c = self.order[self.step_idx]
                if self.matrix[next_r][next_c].phase > self.current_phase:
                    self.current_phase = self.matrix[next_r][next_c].phase
                self._highlight_current()
        else:
            cell.state = 'error'
            self._lbl_msg.config(text="✗ Неправильно", fg=RED)
            self._redraw()
            self.after(700, lambda: self._reset_active(r, col))

    def _reset_active(self, r, col):
        if r < len(self.matrix) and col < len(self.matrix[r]):
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
        self._lbl_msg.config(text=f"💡 Підказка: правильна цифра — {cell.value}", fg=YELLOW)
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
            next_r, next_c = self.order[self.step_idx]
            if self.matrix[next_r][next_c].phase > self.current_phase:
                self.current_phase = self.matrix[next_r][next_c].phase
            self._highlight_current()
            self._lbl_msg.config(text='')

    def _finish(self, perfect):
        self.task_done = True
        self.score_all += 1
        if perfect and not self.hint_used:
            self.score_ok += 1
            self.streak += 1
        else: self.streak = 0

        self._lbl_score.config(text=f"Вірно: {self.score_ok} / {self.score_all}" + (f"  🔥×{self.streak}" if self.streak >= 3 else ""))
        self._update_progress()
        self._highlight_current()

        ans_disp = self.expected_answer_str.replace('.', ',')
        task_text = self._lbl_task.cget("text").replace("?", ans_disp)
        self._lbl_task.config(text=task_text, fg=GREEN)

        if perfect and not self.hint_used: msg, col = f"🎉 Чудово! Всі {len(self.order)} кроків правильно!", GREEN
        elif perfect: msg, col = "✓ Правильно! (з підказками)", YELLOW
        else: msg, col = "✓ Завдання виконано!", ORANGE

        self._lbl_msg.config(text=msg, fg=col)
        self._lbl_step.config(text="✓ Виконано!")
        self._lbl_prompt.config(text="Натисніть ↺ Нове завдання або виберіть операцію ліворуч")

    def _update_progress(self):
        pct = self.step_idx / len(self.order) if len(self.order) > 0 else 0
        self._prog_inner.place(relwidth=pct)
        self._prog_lbl.config(text=f"{int(pct*100)}%")


if __name__ == '__main__':
    App().mainloop()
