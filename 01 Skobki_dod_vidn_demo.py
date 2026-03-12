"""
Демонстрація розкриття дужок — повноекранна, тільки миша, світла тема.
Покрокова анімація зі знаком «+» і «−» перед дужкою.
"""

import tkinter as tk
import math

# ── палітра ───────────────────────────────────────────────────────────────────
BG        = "#faf8f4"
PANEL     = "#ffffff"
ACCENT    = "#1c1917"
BORDER    = "#e7e5e4"
TEXT      = "#1c1917"
MUTED     = "#78716c"
PLUS_COL  = "#0369a1"
MINUS_COL = "#b91c1c"
HL_OUTER  = "#fef08a"
HL_PLUS   = "#e0f2fe"
HL_MINUS  = "#fee2e2"
HL_RESULT = "#d1fae5"
HL_PLUS_T = "#0369a1"
HL_MINUS_T= "#b91c1c"
HL_RES_T  = "#065f46"
NUM_COL   = "#7c3aed"
WHITE     = "#ffffff"

FONT_MATH  = ("Georgia", 34, "bold")
FONT_SMALL = ("Georgia", 18)
FONT_HINT  = ("Georgia", 15, "italic")
FONT_RULE  = ("Georgia", 14)
FONT_BTN   = ("Segoe UI", 13, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_HDR   = ("Segoe UI", 17, "bold")

# ── сценарії ──────────────────────────────────────────────────────────────────
# Кожен крок — список «рядків», кожен рядок — список токенів
# Токен: {"text": str, "style": "normal"|"outer"|"plus"|"minus"|"result"|"muted"|"fade"|"sign_plus"|"sign_minus"}
# eq_text: якщо рядок — роз'яснення між виразами

SCENARIOS = [
    # ── ПЛЮС ──────────────────────────────────────────────────────────────────
    {
        "sign": "plus",
        "title": "+(a + b)",
        "steps": [
            {
                "hint": "Перед дужкою стоїть знак «+». Знайдемо що всередині.",
                "rows": [
                    [{"t":"5","s":"normal"}, {"t":" + ","s":"sign_plus"},
                     {"t":"(","s":"outer"}, {"t":"3a","s":"normal"},
                     {"t":" + ","s":"normal"}, {"t":"2b","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "«+» перед дужкою: всі знаки всередині залишаються незмінними.",
                "rows": [
                    [{"t":"5","s":"normal"}, {"t":" + ","s":"outer"},
                     {"t":"(","s":"outer"}, {"t":"3a","s":"normal"},
                     {"t":" + ","s":"normal"}, {"t":"2b","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "Прибираємо дужку — знаки не змінюємо.",
                "rows": [
                    [{"t":"5","s":"normal"}, {"t":" + ","s":"sign_plus"},
                     {"t":"(","s":"fade"}, {"t":"3a","s":"normal"},
                     {"t":" + ","s":"normal"}, {"t":"2b","s":"normal"},
                     {"t":")","s":"fade"}],
                    [{"t":"знаки не змінюємо","s":"eq"}],
                    [{"t":"5","s":"normal"}, {"t":" + ","s":"plus"},
                     {"t":"3a","s":"plus"}, {"t":" + ","s":"plus"},
                     {"t":"2b","s":"plus"}]
                ]
            },
            {
                "hint": "✓ Готово! Дужка зникла, всі знаки збережено.",
                "rows": [
                    [{"t":"5 + (3a + 2b)","s":"muted"}],
                    [{"t":"=","s":"eq"}],
                    [{"t":"5 + 3a + 2b","s":"result"}]
                ]
            },
        ]
    },
    {
        "sign": "plus",
        "title": "+(a − b)",
        "steps": [
            {
                "hint": "Знак «+» перед дужкою, а всередині є мінус.",
                "rows": [
                    [{"t":"7x","s":"normal"}, {"t":" + ","s":"sign_plus"},
                     {"t":"(","s":"outer"}, {"t":"4y","s":"normal"},
                     {"t":" − ","s":"normal"}, {"t":"3z","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "При «+» — знаки всередині не чіпаємо. Мінус теж залишається.",
                "rows": [
                    [{"t":"7x","s":"normal"}, {"t":" + ","s":"outer"},
                     {"t":"(","s":"outer"}, {"t":"4y","s":"normal"},
                     {"t":" − ","s":"normal"}, {"t":"3z","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "Прибираємо дужку — знак «−» між доданками зберігається.",
                "rows": [
                    [{"t":"7x","s":"normal"}, {"t":" + ","s":"sign_plus"},
                     {"t":"(","s":"fade"}, {"t":"4y","s":"normal"},
                     {"t":" − ","s":"normal"}, {"t":"3z","s":"normal"},
                     {"t":")","s":"fade"}],
                    [{"t":"мінус залишається","s":"eq"}],
                    [{"t":"7x","s":"normal"}, {"t":" + ","s":"plus"},
                     {"t":"4y","s":"plus"}, {"t":" − ","s":"plus"},
                     {"t":"3z","s":"plus"}]
                ]
            },
            {
                "hint": "✓ Знак мінуса між доданками збережено.",
                "rows": [
                    [{"t":"7x + (4y − 3z)","s":"muted"}],
                    [{"t":"=","s":"eq"}],
                    [{"t":"7x + 4y − 3z","s":"result"}]
                ]
            },
        ]
    },
    # ── МІНУС ─────────────────────────────────────────────────────────────────
    {
        "sign": "minus",
        "title": "−(a + b)",
        "steps": [
            {
                "hint": "Перед дужкою стоїть знак «−». Це важливо!",
                "rows": [
                    [{"t":"5","s":"normal"}, {"t":" − ","s":"sign_minus"},
                     {"t":"(","s":"outer"}, {"t":"3a","s":"normal"},
                     {"t":" + ","s":"normal"}, {"t":"2b","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "«−» перед дужкою: знак КОЖНОГО доданка зміниться на протилежний!",
                "rows": [
                    [{"t":"5","s":"normal"}, {"t":" − ","s":"outer"},
                     {"t":"(","s":"outer"}, {"t":"3a","s":"normal"},
                     {"t":" + ","s":"normal"}, {"t":"2b","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "3a мав «+» → стає «−3a».   2b мав «+» → стає «−2b».",
                "rows": [
                    [{"t":"5","s":"normal"}, {"t":" − ","s":"sign_minus"},
                     {"t":"(","s":"fade"}, {"t":"3a","s":"normal"},
                     {"t":" + ","s":"normal"}, {"t":"2b","s":"normal"},
                     {"t":")","s":"fade"}],
                    [{"t":"«+» → «−»,   «+» → «−»","s":"eq"}],
                    [{"t":"5","s":"normal"}, {"t":" − ","s":"minus"},
                     {"t":"3a","s":"minus"}, {"t":" − ","s":"minus"},
                     {"t":"2b","s":"minus"}]
                ]
            },
            {
                "hint": "✓ Обидва знаки змінились з «+» на «−».",
                "rows": [
                    [{"t":"5 − (3a + 2b)","s":"muted"}],
                    [{"t":"=","s":"eq"}],
                    [{"t":"5 − 3a − 2b","s":"result"}]
                ]
            },
        ]
    },
    {
        "sign": "minus",
        "title": "−(a − b)",
        "steps": [
            {
                "hint": "«−» перед дужкою, а всередині є мінус. Увага!",
                "rows": [
                    [{"t":"8","s":"normal"}, {"t":" − ","s":"sign_minus"},
                     {"t":"(","s":"outer"}, {"t":"5x","s":"normal"},
                     {"t":" − ","s":"normal"}, {"t":"3y","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "«−» множить кожен знак всередині — і плюси, і мінуси.",
                "rows": [
                    [{"t":"8","s":"normal"}, {"t":" − ","s":"outer"},
                     {"t":"(","s":"outer"}, {"t":"5x","s":"normal"},
                     {"t":" − ","s":"normal"}, {"t":"3y","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "5x мав «+» → стає «−5x».   3y мав «−» → стає «+3y»!  (мінус × мінус = плюс)",
                "rows": [
                    [{"t":"8","s":"normal"}, {"t":" − ","s":"sign_minus"},
                     {"t":"(","s":"fade"}, {"t":"5x","s":"normal"},
                     {"t":" − ","s":"normal"}, {"t":"3y","s":"normal"},
                     {"t":")","s":"fade"}],
                    [{"t":"«+» → «−»,   «−» → «+»","s":"eq"}],
                    [{"t":"8","s":"normal"}, {"t":" − ","s":"minus"},
                     {"t":"5x","s":"minus"}, {"t":" + ","s":"minus"},
                     {"t":"3y","s":"minus"}]
                ]
            },
            {
                "hint": "✓ Мінус перед мінусом дає плюс! 8 − 5x + 3y",
                "rows": [
                    [{"t":"8 − (5x − 3y)","s":"muted"}],
                    [{"t":"=","s":"eq"}],
                    [{"t":"8 − 5x + 3y","s":"result"}]
                ]
            },
        ]
    },
    # ── ЧИСЛОВИЙ ПРИКЛАД ──────────────────────────────────────────────────────
    {
        "sign": "plus",
        "title": "числа +(4+2)",
        "steps": [
            {
                "hint": "Приклад з числами: 10 + (4 + 2)",
                "rows": [
                    [{"t":"10","s":"normal"}, {"t":" + ","s":"sign_plus"},
                     {"t":"(","s":"outer"}, {"t":"4","s":"normal"},
                     {"t":" + ","s":"normal"}, {"t":"2","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "«+» перед дужкою — знаки не змінюємо.",
                "rows": [
                    [{"t":"10","s":"normal"}, {"t":" + ","s":"outer"},
                     {"t":"(","s":"outer"}, {"t":"4","s":"normal"},
                     {"t":" + ","s":"normal"}, {"t":"2","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "Прибираємо дужки, рахуємо.",
                "rows": [
                    [{"t":"10","s":"normal"}, {"t":" + ","s":"sign_plus"},
                     {"t":"(","s":"fade"}, {"t":"4","s":"normal"},
                     {"t":" + ","s":"normal"}, {"t":"2","s":"normal"},
                     {"t":")","s":"fade"}],
                    [{"t":"=","s":"eq"}],
                    [{"t":"10","s":"normal"}, {"t":" + ","s":"plus"},
                     {"t":"4","s":"plus"}, {"t":" + ","s":"plus"},
                     {"t":"2","s":"plus"}]
                ]
            },
            {
                "hint": "✓ 10 + 4 + 2 = 16",
                "rows": [
                    [{"t":"10 + (4 + 2)","s":"muted"}],
                    [{"t":"=","s":"eq"}],
                    [{"t":"10 + 4 + 2  =  16","s":"result"}]
                ]
            },
        ]
    },
    {
        "sign": "minus",
        "title": "числа −(4+2)",
        "steps": [
            {
                "hint": "Приклад з числами: 10 − (4 + 2)",
                "rows": [
                    [{"t":"10","s":"normal"}, {"t":" − ","s":"sign_minus"},
                     {"t":"(","s":"outer"}, {"t":"4","s":"normal"},
                     {"t":" + ","s":"normal"}, {"t":"2","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "«−» перед дужкою — кожен знак зміниться!",
                "rows": [
                    [{"t":"10","s":"normal"}, {"t":" − ","s":"outer"},
                     {"t":"(","s":"outer"}, {"t":"4","s":"normal"},
                     {"t":" + ","s":"normal"}, {"t":"2","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "4 мав «+» → «−4».   2 мав «+» → «−2».",
                "rows": [
                    [{"t":"10","s":"normal"}, {"t":" − ","s":"sign_minus"},
                     {"t":"(","s":"fade"}, {"t":"4","s":"normal"},
                     {"t":" + ","s":"normal"}, {"t":"2","s":"normal"},
                     {"t":")","s":"fade"}],
                    [{"t":"«+» → «−»,   «+» → «−»","s":"eq"}],
                    [{"t":"10","s":"normal"}, {"t":" − ","s":"minus"},
                     {"t":"4","s":"minus"}, {"t":" − ","s":"minus"},
                     {"t":"2","s":"minus"}]
                ]
            },
            {
                "hint": "✓ 10 − 4 − 2 = 4",
                "rows": [
                    [{"t":"10 − (4 + 2)","s":"muted"}],
                    [{"t":"=","s":"eq"}],
                    [{"t":"10 − 4 − 2  =  4","s":"result"}]
                ]
            },
        ]
    },
    {
        "sign": "minus",
        "title": "числа −(4−2)",
        "steps": [
            {
                "hint": "Каверзний приклад: 10 − (4 − 2)",
                "rows": [
                    [{"t":"10","s":"normal"}, {"t":" − ","s":"sign_minus"},
                     {"t":"(","s":"outer"}, {"t":"4","s":"normal"},
                     {"t":" − ","s":"normal"}, {"t":"2","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "«−» перед дужкою змінює КОЖЕН знак.",
                "rows": [
                    [{"t":"10","s":"normal"}, {"t":" − ","s":"outer"},
                     {"t":"(","s":"outer"}, {"t":"4","s":"normal"},
                     {"t":" − ","s":"normal"}, {"t":"2","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "4 мав «+» → «−4».   2 мав «−» → «+2»!  (− × − = +)",
                "rows": [
                    [{"t":"10","s":"normal"}, {"t":" − ","s":"sign_minus"},
                     {"t":"(","s":"fade"}, {"t":"4","s":"normal"},
                     {"t":" − ","s":"normal"}, {"t":"2","s":"normal"},
                     {"t":")","s":"fade"}],
                    [{"t":"«+» → «−»,   «−» → «+»","s":"eq"}],
                    [{"t":"10","s":"normal"}, {"t":" − ","s":"minus"},
                     {"t":"4","s":"minus"}, {"t":" + ","s":"minus"},
                     {"t":"2","s":"minus"}]
                ]
            },
            {
                "hint": "✓ 10 − 4 + 2 = 8   (а не 4!)",
                "rows": [
                    [{"t":"10 − (4 − 2)","s":"muted"}],
                    [{"t":"=","s":"eq"}],
                    [{"t":"10 − 4 + 2  =  8","s":"result"}]
                ]
            },
        ]
    },
    # ── СКЛАДНІ ПРИКЛАДИ (5 доданків, перший від'ємний) ──────────────────────
    {
        "sign": "plus",
        "title": "+(−a + b − c + d − e)",
        "steps": [
            {
                "hint": "5 доданків, перший з мінусом. «+» перед дужкою.",
                "rows": [
                    [{"t":"10","s":"normal"}, {"t":" + ","s":"sign_plus"},
                     {"t":"(","s":"outer"},
                     {"t":"−3a","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"5b","s":"normal"}, {"t":" − ","s":"normal"},
                     {"t":"2c","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"7d","s":"normal"}, {"t":" − ","s":"normal"},
                     {"t":"4e","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "Знак «+» перед дужкою — всі знаки НЕ ЗМІНЮЮТЬСЯ. Навіть перший «−3a».",
                "rows": [
                    [{"t":"10","s":"normal"}, {"t":" + ","s":"outer"},
                     {"t":"(","s":"outer"},
                     {"t":"−3a","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"5b","s":"normal"}, {"t":" − ","s":"normal"},
                     {"t":"2c","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"7d","s":"normal"}, {"t":" − ","s":"normal"},
                     {"t":"4e","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "Прибираємо дужку. Знак «−» перед 3a залишається як є.",
                "rows": [
                    [{"t":"10","s":"normal"}, {"t":" + ","s":"sign_plus"},
                     {"t":"(","s":"fade"},
                     {"t":"−3a","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"5b","s":"normal"}, {"t":" − ","s":"normal"},
                     {"t":"2c","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"7d","s":"normal"}, {"t":" − ","s":"normal"},
                     {"t":"4e","s":"normal"},
                     {"t":")","s":"fade"}],
                    [{"t":"всі знаки збережено","s":"eq"}],
                    [{"t":"10","s":"normal"},
                     {"t":" − ","s":"plus"}, {"t":"3a","s":"plus"},
                     {"t":" + ","s":"plus"}, {"t":"5b","s":"plus"},
                     {"t":" − ","s":"plus"}, {"t":"2c","s":"plus"},
                     {"t":" + ","s":"plus"}, {"t":"7d","s":"plus"},
                     {"t":" − ","s":"plus"}, {"t":"4e","s":"plus"}]
                ]
            },
            {
                "hint": "✓ Всі 5 знаків збережено. «+(−3a)» = «−3a» — нічого не змінилось.",
                "rows": [
                    [{"t":"10 + (−3a + 5b − 2c + 7d − 4e)","s":"muted"}],
                    [{"t":"=","s":"eq"}],
                    [{"t":"10 − 3a + 5b − 2c + 7d − 4e","s":"result"}]
                ]
            },
        ]
    },
    {
        "sign": "minus",
        "title": "−(−a + b − c + d)",
        "steps": [
            {
                "hint": "«−» перед дужкою, і перший доданок теж з мінусом. Будьте уважні!",
                "rows": [
                    [{"t":"15","s":"normal"}, {"t":" − ","s":"sign_minus"},
                     {"t":"(","s":"outer"},
                     {"t":"−2a","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"3b","s":"normal"}, {"t":" − ","s":"normal"},
                     {"t":"4c","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"6d","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "«−» перед дужкою ЗМІНЮЄ КОЖЕН ЗНАК. Перший «−2a» також зміниться!",
                "rows": [
                    [{"t":"15","s":"normal"}, {"t":" − ","s":"outer"},
                     {"t":"(","s":"outer"},
                     {"t":"−2a","s":"outer"}, {"t":" + ","s":"outer"},
                     {"t":"3b","s":"outer"}, {"t":" − ","s":"outer"},
                     {"t":"4c","s":"outer"}, {"t":" + ","s":"outer"},
                     {"t":"6d","s":"outer"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "«−»×«−»=«+»: −2a → +2a.  «−»×«+»=«−»: 3b→−3b, 6d→−6d.  «−»×«−»=«+»: −4c→+4c.",
                "rows": [
                    [{"t":"15","s":"normal"}, {"t":" − ","s":"sign_minus"},
                     {"t":"(","s":"fade"},
                     {"t":"−2a","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"3b","s":"normal"}, {"t":" − ","s":"normal"},
                     {"t":"4c","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"6d","s":"normal"},
                     {"t":")","s":"fade"}],
                    [{"t":"−×−=+  −×+=−  −×+=−  −×−=+","s":"eq"}],
                    [{"t":"15","s":"normal"},
                     {"t":" + ","s":"minus_flip"}, {"t":"2a","s":"minus_flip"},
                     {"t":" − ","s":"minus"}, {"t":"3b","s":"minus"},
                     {"t":" + ","s":"minus_flip"}, {"t":"4c","s":"minus_flip"},
                     {"t":" − ","s":"minus"}, {"t":"6d","s":"minus"}]
                ]
            },
            {
                "hint": "✓ Перший «−2a» став «+2a». «−4c» став «+4c». Мінус×Мінус = Плюс!",
                "rows": [
                    [{"t":"15 − (−2a + 3b − 4c + 6d)","s":"muted"}],
                    [{"t":"=","s":"eq"}],
                    [{"t":"15 + 2a − 3b + 4c − 6d","s":"result"}]
                ]
            },
        ]
    },
    {
        "sign": "minus",
        "title": "−(−a − b + c − d + e)",
        "steps": [
            {
                "hint": "5 доданків, перший і другий від'ємні. «−» перед дужкою.",
                "rows": [
                    [{"t":"−","s":"sign_minus"},
                     {"t":"(","s":"outer"},
                     {"t":"−x","s":"normal"}, {"t":" − ","s":"normal"},
                     {"t":"2y","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"3z","s":"normal"}, {"t":" − ","s":"normal"},
                     {"t":"4w","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"5k","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "«−» перед дужкою — кожен знак зміниться. Рахуємо по одному.",
                "rows": [
                    [{"t":"−","s":"outer"},
                     {"t":"(","s":"outer"},
                     {"t":"−x","s":"outer"}, {"t":" − ","s":"outer"},
                     {"t":"2y","s":"outer"}, {"t":" + ","s":"outer"},
                     {"t":"3z","s":"outer"}, {"t":" − ","s":"outer"},
                     {"t":"4w","s":"outer"}, {"t":" + ","s":"outer"},
                     {"t":"5k","s":"outer"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "−(−x)=+x  −(−2y)=+2y  −(+3z)=−3z  −(−4w)=+4w  −(+5k)=−5k",
                "rows": [
                    [{"t":"−","s":"sign_minus"},
                     {"t":"(","s":"fade"},
                     {"t":"−x","s":"normal"}, {"t":" − ","s":"normal"},
                     {"t":"2y","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"3z","s":"normal"}, {"t":" − ","s":"normal"},
                     {"t":"4w","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"5k","s":"normal"},
                     {"t":")","s":"fade"}],
                    [{"t":"−×−=+  −×−=+  −×+=−  −×−=+  −×+=−","s":"eq"}],
                    [{"t":"x","s":"minus_flip"}, {"t":" + ","s":"minus_flip"},
                     {"t":"2y","s":"minus_flip"},
                     {"t":" − ","s":"minus"}, {"t":"3z","s":"minus"},
                     {"t":" + ","s":"minus_flip"}, {"t":"4w","s":"minus_flip"},
                     {"t":" − ","s":"minus"}, {"t":"5k","s":"minus"}]
                ]
            },
            {
                "hint": "✓ Два мінуси в дужці стали плюсами. Плюси стали мінусами.",
                "rows": [
                    [{"t":"−(−x − 2y + 3z − 4w + 5k)","s":"muted"}],
                    [{"t":"=","s":"eq"}],
                    [{"t":"x + 2y − 3z + 4w − 5k","s":"result"}]
                ]
            },
        ]
    },
    {
        "sign": "minus",
        "title": "числа −(−3 + 7 − 2 + 5)",
        "steps": [
            {
                "hint": "Числовий каверзний приклад: 20 − (−3 + 7 − 2 + 5). Перший від'ємний!",
                "rows": [
                    [{"t":"20","s":"normal"}, {"t":" − ","s":"sign_minus"},
                     {"t":"(","s":"outer"},
                     {"t":"−3","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"7","s":"normal"}, {"t":" − ","s":"normal"},
                     {"t":"2","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"5","s":"normal"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "«−» перед дужкою змінює всі знаки. −(−3) дасть +3!",
                "rows": [
                    [{"t":"20","s":"normal"}, {"t":" − ","s":"outer"},
                     {"t":"(","s":"outer"},
                     {"t":"−3","s":"outer"}, {"t":" + ","s":"outer"},
                     {"t":"7","s":"outer"}, {"t":" − ","s":"outer"},
                     {"t":"2","s":"outer"}, {"t":" + ","s":"outer"},
                     {"t":"5","s":"outer"},
                     {"t":")","s":"outer"}]
                ]
            },
            {
                "hint": "−(−3)=+3  −(+7)=−7  −(−2)=+2  −(+5)=−5",
                "rows": [
                    [{"t":"20","s":"normal"}, {"t":" − ","s":"sign_minus"},
                     {"t":"(","s":"fade"},
                     {"t":"−3","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"7","s":"normal"}, {"t":" − ","s":"normal"},
                     {"t":"2","s":"normal"}, {"t":" + ","s":"normal"},
                     {"t":"5","s":"normal"},
                     {"t":")","s":"fade"}],
                    [{"t":"−×−=+   −×+=−   −×−=+   −×+=−","s":"eq"}],
                    [{"t":"20","s":"normal"},
                     {"t":" + ","s":"minus_flip"}, {"t":"3","s":"minus_flip"},
                     {"t":" − ","s":"minus"}, {"t":"7","s":"minus"},
                     {"t":" + ","s":"minus_flip"}, {"t":"2","s":"minus_flip"},
                     {"t":" − ","s":"minus"}, {"t":"5","s":"minus"}]
                ]
            },
            {
                "hint": "✓ 20 + 3 − 7 + 2 − 5 = 13.  Перевір: 20 − (−3+7−2+5) = 20 − 7 = 13 ✓",
                "rows": [
                    [{"t":"20 − (−3 + 7 − 2 + 5)","s":"muted"}],
                    [{"t":"=","s":"eq"}],
                    [{"t":"20 + 3 − 7 + 2 − 5  =  13","s":"result"}]
                ]
            },
        ]
    },
]


# ─────────────────────────────────────────────────────────────────────────────
class BracketsDemo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Розкриття дужок")
        self.configure(bg=BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.update_idletasks()
        mx = self.winfo_pointerx()
        my = self.winfo_pointery()
        mon = self._detect_monitor(mx, my)
        self.MON_X, self.MON_Y = mon["x"], mon["y"]
        self.SW, self.SH = mon["w"], mon["h"]
        self.geometry(f"{self.SW}x{self.SH}+{self.MON_X}+{self.MON_Y}")
        self.update_idletasks()
        self.attributes("-fullscreen", True)

        self.HDR = 58
        self.tab    = "plus"    # "plus" | "minus"
        self.sc_idx = 0         # індекс сценарію серед відфільтрованих
        self.step   = 0

        self._build_ui()
        self._refresh()

    # ── монітор ───────────────────────────────────────────────────────────────
    def _detect_monitor(self, px, py):
        try:
            vw = self.winfo_vrootwidth();  vh = self.winfo_vrootheight()
            sw = self.winfo_screenwidth(); sh = self.winfo_screenheight()
            if vw > sw:
                for i in range(round(vw/sw)):
                    m = {"x":i*sw,"y":0,"w":sw,"h":sh}
                    if m["x"] <= px < m["x"]+sw: return m
            elif vh > sh:
                for i in range(round(vh/sh)):
                    m = {"x":0,"y":i*sh,"w":sw,"h":sh}
                    if m["y"] <= py < m["y"]+sh: return m
        except: pass
        return {"x":0,"y":0,"w":self.winfo_screenwidth(),"h":self.winfo_screenheight()}

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        SW, SH, HDR = self.SW, self.SH, self.HDR
        CH = SH - HDR

        # шапка
        hdr = tk.Frame(self, bg="#1c1917", height=HDR)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr, text="( )  Розкриття дужок", bg="#1c1917", fg=WHITE,
                 font=FONT_HDR).place(x=22, rely=.5, anchor="w")
        tk.Label(hdr, text="ESC — вийти", bg="#1c1917", fg=MUTED,
                 font=("Segoe UI", 10)).place(relx=1, x=-18, rely=.5, anchor="e")

        # тіло
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        # ── ліва частина (70%)
        LW = int(SW * 0.68)
        self.LW = LW
        left = tk.Frame(body, bg=BG, width=LW)
        left.pack(side="left", fill="both"); left.pack_propagate(False)

        # табулятор
        tab_f = tk.Frame(left, bg=BG)
        tab_f.place(relx=.5, y=int(CH*.06), anchor="center")

        outer = tk.Frame(tab_f, bg=BORDER, bd=0,
                         highlightbackground=BORDER, highlightthickness=1)
        outer.pack()
        self.btn_plus = tk.Button(outer, text="+(…)  Знак «плюс»",
            bg=HL_PLUS, fg=PLUS_COL, font=("Segoe UI",13,"bold"),
            relief="flat", bd=0, cursor="hand2", padx=28, pady=10,
            command=lambda: self._switch_tab("plus"))
        self.btn_plus.pack(side="left")
        tk.Frame(outer, bg=BORDER, width=1).pack(side="left", fill="y")
        self.btn_minus = tk.Button(outer, text="−(…)  Знак «мінус»",
            bg=WHITE, fg=MUTED, font=("Segoe UI",13,"bold"),
            relief="flat", bd=0, cursor="hand2", padx=28, pady=10,
            command=lambda: self._switch_tab("minus"))
        self.btn_minus.pack(side="left")

        # блок сценарію (назва + крапки)
        self.sc_frame = tk.Frame(left, bg=BG)
        self.sc_frame.place(relx=.5, y=int(CH*.15), anchor="center")

        self.lbl_sc_title = tk.Label(self.sc_frame, text="", bg=BG, fg=MUTED,
                                     font=("Segoe UI",12))
        self.lbl_sc_title.pack(side="left")

        self.dots_frame = tk.Frame(self.sc_frame, bg=BG)
        self.dots_frame.pack(side="left", padx=(16,0))

        # канвас для математики
        self.CW = LW - 40
        self.canvas = tk.Canvas(left, bg=PANEL, highlightthickness=0,
                                width=self.CW, height=int(CH * 0.54))
        self.canvas.place(relx=.5, y=int(CH*.46), anchor="center")

        # підказка
        hint_f = tk.Frame(left, bg="#f5f5f4",
                          highlightbackground=BORDER, highlightthickness=1)
        hint_f.place(relx=.5, y=int(CH*.76), anchor="center", width=LW-60)
        self.lbl_hint = tk.Label(hint_f, text="", bg="#f5f5f4", fg=MUTED,
                                 font=FONT_HINT, wraplength=LW-100,
                                 justify="left", anchor="w")
        self.lbl_hint.pack(fill="x", padx=14, pady=10)

        # кнопки управління
        ctrl = tk.Frame(left, bg=BG)
        ctrl.place(relx=.5, y=int(CH*.90), anchor="center")

        self.btn_prev = tk.Button(ctrl, text="← Назад",
            bg=BORDER, fg=TEXT, font=FONT_BTN,
            relief="flat", bd=0, cursor="hand2", padx=22, pady=10,
            command=self._prev_step)
        self.btn_prev.pack(side="left", padx=6)

        self.btn_next = tk.Button(ctrl, text="Далі →",
            bg=ACCENT, fg=WHITE, font=FONT_BTN,
            relief="flat", bd=0, cursor="hand2", padx=22, pady=10,
            command=self._next_step)
        self.btn_next.pack(side="left", padx=6)

        self.btn_reset = tk.Button(ctrl, text="↺ Спочатку",
            bg=BG, fg=MUTED, font=FONT_BTN,
            relief="flat", bd=0, cursor="hand2", padx=16, pady=10,
            highlightbackground=BORDER, highlightthickness=1,
            command=self._reset)
        self.btn_reset.pack(side="left", padx=6)

        self.btn_sc_prev = tk.Button(ctrl, text="◀ Приклад",
            bg=BG, fg=MUTED, font=FONT_BTN,
            relief="flat", bd=0, cursor="hand2", padx=14, pady=10,
            highlightbackground=BORDER, highlightthickness=1,
            command=self._prev_scenario)
        self.btn_sc_prev.pack(side="left", padx=6)

        self.btn_sc_next = tk.Button(ctrl, text="Приклад ▶",
            bg=BG, fg=MUTED, font=FONT_BTN,
            relief="flat", bd=0, cursor="hand2", padx=14, pady=10,
            highlightbackground=BORDER, highlightthickness=1,
            command=self._next_scenario)
        self.btn_sc_next.pack(side="left", padx=6)

        self.lbl_step_cnt = tk.Label(ctrl, text="", bg=BG, fg=MUTED,
                                     font=("Segoe UI",11))
        self.lbl_step_cnt.pack(side="left", padx=12)

        # ── права панель (правила)
        RW = SW - LW
        self.RW = RW
        right = tk.Frame(body, bg=PANEL, width=RW,
                         highlightbackground=BORDER, highlightthickness=1)
        right.pack(side="right", fill="y"); right.pack_propagate(False)

        rpad = tk.Frame(right, bg=PANEL)
        rpad.place(relx=.5, rely=.04, anchor="n", width=RW-32)

        tk.Label(rpad, text="Правила", bg=PANEL, fg=MUTED,
                 font=("Segoe UI",11,"bold")).pack(anchor="w", pady=(0,10))

        # правило +
        plus_box = tk.Frame(rpad, bg=HL_PLUS,
                            highlightbackground="#bae6fd", highlightthickness=1)
        plus_box.pack(fill="x", ipady=10, ipadx=8, pady=(0,12))
        tk.Label(plus_box, text="+(a + b)", bg=HL_PLUS, fg=PLUS_COL,
                 font=("Georgia",15,"bold")).pack(anchor="w", padx=8)
        tk.Label(plus_box,
                 text="Знак «+» перед дужкою:\nзнаки всіх доданків\nНЕ ЗМІНЮЮТЬСЯ.",
                 bg=HL_PLUS, fg=TEXT, font=FONT_RULE,
                 justify="left").pack(anchor="w", padx=8, pady=(4,0))
        tk.Label(plus_box, text="+(a+b) = a+b\n+(a−b) = a−b",
                 bg=HL_PLUS, fg=PLUS_COL,
                 font=("Courier",12,"bold")).pack(anchor="w", padx=8, pady=(4,0))

        tk.Frame(rpad, bg=BORDER, height=1).pack(fill="x", pady=12)

        # правило −
        minus_box = tk.Frame(rpad, bg=HL_MINUS,
                             highlightbackground="#fca5a5", highlightthickness=1)
        minus_box.pack(fill="x", ipady=10, ipadx=8, pady=(0,12))
        tk.Label(minus_box, text="−(a + b)", bg=HL_MINUS, fg=MINUS_COL,
                 font=("Georgia",15,"bold")).pack(anchor="w", padx=8)
        tk.Label(minus_box,
                 text="Знак «−» перед дужкою:\nзнак КОЖНОГО доданка\nЗМІНЮЄТЬСЯ на протилежний.",
                 bg=HL_MINUS, fg=TEXT, font=FONT_RULE,
                 justify="left").pack(anchor="w", padx=8, pady=(4,0))
        tk.Label(minus_box, text="−(a+b) = −a−b\n−(a−b) = −a+b",
                 bg=HL_MINUS, fg=MINUS_COL,
                 font=("Courier",12,"bold")).pack(anchor="w", padx=8, pady=(4,0))

        tk.Frame(rpad, bg=BORDER, height=1).pack(fill="x", pady=12)

        # таблиця знаків
        tk.Label(rpad, text="Таблиця знаків", bg=PANEL, fg=MUTED,
                 font=("Segoe UI",11,"bold")).pack(anchor="w", pady=(0,8))
        tbl_f = tk.Frame(rpad, bg=PANEL)
        tbl_f.pack(fill="x")

        headers = ["Перед\nдужкою", "Знак\nв дужці", "Знак\nпісля"]
        rows_data = [
            ("+", "+", "+",  HL_PLUS,  PLUS_COL),
            ("+", "−", "−",  HL_PLUS,  PLUS_COL),
            ("−", "+", "−",  HL_MINUS, MINUS_COL),
            ("−", "−", "+",  HL_MINUS, MINUS_COL),
        ]
        for j, h in enumerate(headers):
            tk.Label(tbl_f, text=h, bg=PANEL, fg=MUTED,
                     font=("Segoe UI",10,"bold"),
                     width=9, justify="center").grid(row=0, column=j, padx=2, pady=(0,4))
        for i, (a,b,c,bg,fg) in enumerate(rows_data):
            for j, val in enumerate([a,b,c]):
                tk.Label(tbl_f, text=val, bg=bg, fg=fg,
                         font=("Courier",14,"bold"),
                         width=9, pady=5).grid(row=i+1, column=j, padx=2, pady=2, sticky="ew")

    # ── фільтр сценаріїв за вкладкою ─────────────────────────────────────────
    def _filtered(self):
        return [s for s in SCENARIOS if s["sign"] == self.tab]

    def _scenario(self):
        lst = self._filtered()
        return lst[self.sc_idx % len(lst)]

    # ── перемикачі ────────────────────────────────────────────────────────────
    def _switch_tab(self, tab):
        self.tab = tab; self.sc_idx = 0; self.step = 0
        self._refresh()

    def _prev_step(self):
        if self.step > 0: self.step -= 1; self._draw_step()

    def _next_step(self):
        sc = self._scenario()
        if self.step < len(sc["steps"]) - 1:
            self.step += 1; self._draw_step()
        else:
            self._next_scenario()

    def _reset(self):
        self.step = 0; self._draw_step()

    def _prev_scenario(self):
        lst = self._filtered()
        self.sc_idx = (self.sc_idx - 1) % len(lst)
        self.step = 0; self._refresh()

    def _next_scenario(self):
        lst = self._filtered()
        self.sc_idx = (self.sc_idx + 1) % len(lst)
        self.step = 0; self._refresh()

    def _refresh(self):
        # вкладки
        if self.tab == "plus":
            self.btn_plus.config(bg=HL_PLUS, fg=PLUS_COL)
            self.btn_minus.config(bg=WHITE, fg=MUTED)
        else:
            self.btn_minus.config(bg=HL_MINUS, fg=MINUS_COL)
            self.btn_plus.config(bg=WHITE, fg=MUTED)
        # dots сценаріїв
        for w in self.dots_frame.winfo_children(): w.destroy()
        lst = self._filtered()
        for i in range(len(lst)):
            col = (PLUS_COL if self.tab=="plus" else MINUS_COL) if i==self.sc_idx else BORDER
            tk.Frame(self.dots_frame, bg=col, width=10, height=10,
                     highlightthickness=0).pack(side="left", padx=3)
        self._draw_step()

    # ── малювання кроку ───────────────────────────────────────────────────────
    def _draw_step(self):
        sc   = self._scenario()
        step = sc["steps"][self.step]
        nsteps = len(sc["steps"])

        # заголовок сценарію
        col = PLUS_COL if self.tab=="plus" else MINUS_COL
        self.lbl_sc_title.config(
            text=f"Приклад: {sc['title']}  |  крок {self.step+1} / {nsteps}",
            fg=col)

        # підказка
        self.lbl_hint.config(text=step.get("hint", ""))

        # кнопки
        self.btn_prev.config(state="normal" if self.step>0 else "disabled")
        total_sc = len(self._filtered())
        last = (self.step == nsteps-1)
        self.btn_next.config(
            text=("Наступний приклад ▶" if last else "Далі →"),
            bg=col)
        self.lbl_step_cnt.config(
            text=f"приклад {self.sc_idx+1}/{total_sc}")

        # малюємо математику
        self._draw_math(step["rows"])

    def _draw_math(self, rows):
        c = self.canvas
        c.delete("all")

        CW = self.CW
        CH = int(self.SH * 0.54)

        # розмір шрифту адаптивний
        base_size = max(22, int(self.SH * 0.038))
        font_normal = ("Georgia", base_size, "bold")
        font_eq     = ("Georgia", int(base_size * 0.62), "italic")

        # вертикальний відступ між рядками
        row_h = int(base_size * 2.2)
        total_h = len(rows) * row_h
        start_y = (CH - total_h) // 2 + row_h // 2

        for ri, row in enumerate(rows):
            y = start_y + ri * row_h

            # eq-рядок (роз'яснення)
            if len(row) == 1 and row[0].get("s") == "eq":
                c.create_text(CW//2, y, text=row[0]["t"],
                              fill=MUTED, font=font_eq, anchor="center")
                continue

            # вимірюємо ширину рядка (приблизно)
            total_w = self._measure_row(row, font_normal)
            x = (CW - total_w) // 2

            for tok in row:
                s = tok.get("s", "normal")
                t = tok["t"]

                # колір тексту
                if s == "normal":    fg, bg, border = TEXT,      None,       None
                elif s == "muted":   fg, bg, border = "#c4b9b0", None,       None
                elif s == "fade":    fg, bg, border = "#d6d3d1", None,       None
                elif s == "outer":   fg, bg, border = ACCENT,    HL_OUTER,   "#d97706"
                elif s == "plus":    fg, bg, border = PLUS_COL,  HL_PLUS,    "#7dd3fc"
                elif s == "minus":   fg, bg, border = MINUS_COL, HL_MINUS,   "#fca5a5"
                elif s == "result":     fg, bg, border = HL_RES_T,  HL_RESULT,  "#6ee7b7"
                elif s == "minus_flip": fg, bg, border = "#065f46",  "#bbf7d0",  "#4ade80"  # зелений — знак змінився з − на +
                elif s == "sign_plus":  fg, bg, border = PLUS_COL,  None, None
                elif s == "sign_minus": fg, bg, border = MINUS_COL, None, None
                else:                   fg, bg, border = TEXT,      None,       None

                # ширина токена
                tw = self._token_width(t, font_normal)
                pad = 6 if bg else 0

                if bg:
                    rx1, rx2 = x - pad, x + tw + pad
                    ry1, ry2 = y - int(base_size*0.72), y + int(base_size*0.72)
                    c.create_rectangle(rx1, ry1, rx2, ry2,
                                       fill=bg, outline=border or bg,
                                       width=1.5)

                if s == "fade":
                    c.create_text(x + tw//2, y, text=t, fill=fg,
                                  font=font_normal, anchor="center")
                    # закреслення
                    c.create_line(x, y, x+tw, y, fill="#ef4444", width=2)
                else:
                    c.create_text(x + tw//2, y, text=t, fill=fg,
                                  font=font_normal, anchor="center")

                x += tw + (pad if bg else 0)

    def _token_width(self, text, font):
        """Ширина тексту через tkinter Font."""
        import tkinter.font as tkf
        try:
            f = tkf.Font(family=font[0], size=font[1],
                         weight=font[2] if len(font)>2 else "normal")
            return f.measure(text)
        except Exception:
            return len(text) * (font[1] if len(font)>1 else 20)

    def _measure_row(self, row, font):
        total = 0
        for tok in row:
            s = tok.get("s","normal")
            pad = 6 if s in ("outer","plus","minus","minus_flip","result") else 0
            total += self._token_width(tok["t"], font) + pad
        return total


if __name__ == "__main__":
    # кешуємо ширини при запуску щоб не мигало
    app = BracketsDemo()
    app.mainloop()
