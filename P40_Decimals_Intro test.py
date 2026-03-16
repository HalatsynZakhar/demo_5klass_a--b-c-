"""
§ 40. Десятковий дріб — повний модуль
ВИПРАВЛЕНО/ДОДАНО:
  - Числова пряма: matplotlib із зумом/панорамуванням, коректні підписи
  - Тренажер Дес→Дріб: повний UI із нумпадом, двокроковий ввід
  - Тренажер Дріб→Дес: не пише ціле за користувача, нумпад
  - Тренажер: Привести до тисячних (нулі знаменника)
  - Тренажер: Запис з тексту (дві цілі, п'ять десятих)
  - Тренажер: Нулі↔знаки (практика)
"""
import tkinter as tk
import random, math
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ── Palette ──────────────────────────────────────────────────────────────────
BG="#f0f4f8"; PANEL="#ffffff"; BORDER="#cbd5e1"; TEXT="#0f172a"; MUTED="#475569"
WHITE="#ffffff"; BTN_NUM="#e2e8f0"; HDR_BG="#1d4ed8"; NAV_BG="#1e3a5f"; NAV_FG="#ffffff"
ACCENT="#1d4ed8"; ACCENT2="#7c3aed"; GREEN="#15803d"; GREEN_LT="#dcfce7"
RED="#b91c1c"; RED_LT="#fee2e2"; ORANGE="#b45309"; ORANGE_LT="#fef3c7"
CARD_B="#dbeafe"; CARD_V="#ede9fe"; CARD_G="#dcfce7"; CARD_Y="#fef9c3"
CARD_R="#fee2e2"; TEAL="#0f766e"; TEAL_LT="#ccfbf1"
C_DIGIT="#db2777"; C_ZERO="#059669"
FILL_10="#3b82f6"; FILL_100="#8b5cf6"; FILL_1000="#16a34a"; C_EMPTY="#e2e8f0"

F_TITLE=("Segoe UI",34,"bold"); F_HEAD=("Segoe UI",26,"bold")
F_SUB=("Segoe UI",20,"bold");   F_BODY=("Segoe UI",17)
F_BODYB=("Segoe UI",17,"bold"); F_BTN=("Segoe UI",19,"bold")
F_NAV=("Segoe UI",13,"bold");   F_SCORE=("Segoe UI",20,"bold")
F_SMALL=("Segoe UI",13);        F_FRAC=("Segoe UI",36,"bold")
F_FRAC_S=("Segoe UI",22,"bold");F_NUM=("Segoe UI",24,"bold")
F_CTRL=("Segoe UI",22,"bold");  F_BIG_DEC=("Courier New",68,"bold")

def _dk(h,a=30):
    return"#{:02x}{:02x}{:02x}".format(
        max(0,int(h[1:3],16)-a),max(0,int(h[3:5],16)-a),max(0,int(h[5:7],16)-a))

def mkbtn(p,text,cmd,bg=ACCENT,fg=WHITE,font=F_BTN,w=12,h=2,px=6,py=6):
    b=tk.Button(p,text=text,command=cmd,bg=bg,fg=fg,font=font,width=w,height=h,
               relief="flat",bd=0,cursor="hand2",activebackground=bg,activeforeground=fg,padx=px,pady=py)
    o=bg; b.bind("<Enter>",lambda e:b.config(bg=_dk(o,25))); b.bind("<Leave>",lambda e:b.config(bg=o))
    return b

def hline(p,color=BORDER): tk.Frame(p,bg=color,height=2).pack(fill="x",pady=(4,12))

def frac_w(p,n,d,bg=PANEL,size="big",color=ACCENT):
    fn=F_FRAC if size=="big" else F_FRAC_S
    bw=max(len(str(n)),len(str(d)))*26+20
    f=tk.Frame(p,bg=bg)
    tk.Label(f,text=str(n),font=fn,bg=bg,fg=color).pack()
    tk.Frame(f,bg=color,height=3,width=bw).pack(pady=2)
    tk.Label(f,text=str(d),font=fn,bg=bg,fg=color).pack()
    return f

def theory_card(p,title,body,bg_c,fg_title=TEXT):
    f=tk.Frame(p,bg=bg_c,padx=22,pady=14,highlightbackground=BORDER,highlightthickness=1)
    f.pack(fill="x",pady=7)
    tk.Label(f,text=title,font=F_SUB,bg=bg_c,fg=fg_title,anchor="w").pack(fill="x")
    tk.Label(f,text=body,font=F_BODY,bg=bg_c,fg=TEXT,justify="left",wraplength=1300,anchor="w").pack(fill="x",pady=(6,0))
    return f

def build_numpad(p,fn,bg=BG):
    np=tk.Frame(p,bg=bg)
    for row in [("7","8","9"),("4","5","6"),("1","2","3"),("C","0","⌫")]:
        rf=tk.Frame(np,bg=bg); rf.pack(pady=3)
        for ch in row:
            bc,fc=(BTN_NUM,TEXT) if ch.isdigit() else ((RED_LT,RED) if ch=="C" else (CARD_V,ACCENT2))
            b=tk.Button(rf,text=ch,font=F_NUM,width=3,height=1,bg=bc,fg=fc,relief="flat",
                       cursor="hand2",command=lambda c=ch:fn(c))
            b.pack(side="left",padx=4)
            o=bc; b.bind("<Enter>",lambda e,x=b,oo=o:x.config(bg=_dk(oo,18))); b.bind("<Leave>",lambda e,x=b,oo=o:x.config(bg=oo))
    return np

# ═══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("§ 40.  Десятковий дріб")
        self.configure(bg=BG)
        self.attributes("-fullscreen",True)
        self.bind("<Escape>",lambda e:self.attributes("-fullscreen",False))
        self.SW=self.winfo_screenwidth(); self.SH=self.winfo_screenheight()
        self.current_frame=None; self.mode=None

        self.gmode="tenths"; self.gval=0; self.gtask=False
        self.gtarget=0; self.glocked=False; self.gscore=0; self.gtotal=0
        self.pv_digits=[0,7,5,3]; self.pv_places=2
        self.zdemo_places=2; self._zdemo_digits=[]

        # trainer states
        self.ta_dec=""; self.ta_n=0; self.ta_d=0
        self.ta_inp_n=""; self.ta_inp_d=""; self.ta_active="n"; self.ta_n_done=False
        self.ta_score=0; self.ta_att=0

        self.tb_n=0; self.tb_d=0; self.tb_whole=0; self.tb_ans=""
        self.tb_inp=""; self.tb_score=0; self.tb_att=0; self.tb_dec_places=1

        self.tc_score=0; self.tc_att=0   # привести до ...
        self.td_score=0; self.td_att=0   # читання числа з тексту
        self.tz_score=0; self.tz_att=0   # нулі-знаки практика

        self.nl_task_mode=False; self.nl_task_target=0.0
        self.nl_task_score=0; self.nl_task_total=0; self.nl_task_locked=False
        self._nl_mpl_fig=None; self._nl_mpl_canvas=None

        self._build_chrome()
        self.show_main_menu()

    # ── chrome ──────────────────────────────────────────────────────────────
    def _build_chrome(self):
        hdr=tk.Frame(self,bg=HDR_BG,height=60); hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr,text="§ 40.   Десятковий дріб",bg=HDR_BG,fg=WHITE,
                 font=("Segoe UI",20,"bold")).pack(side="left",padx=24)
        mkbtn(hdr,"✕  Вийти",self.destroy,bg="#b91c1c",font=("Segoe UI",12,"bold"),w=8,h=1).pack(side="right",padx=14,pady=12)
        nav=tk.Frame(self,bg=NAV_BG,height=48); nav.pack(fill="x"); nav.pack_propagate(False)
        nav_items=[
            ("🏠 Меню",self.show_main_menu),
            ("📖 Теорія А",self.show_theory_a),
            ("📖 Теорія Б",self.show_theory_b),
            ("📖 Нулі в кінці",self.show_theory_c),
            ("🟦 Сітка",self.show_grid),
            ("🔢 Розряди",self.show_place_value),
            ("📏 Пряма",self.show_number_line),
            ("🔗 Нулі↔знаки",self.show_zeros_demo),
            ("🎯 Дес→Дріб",self.show_trainer_a),
            ("🎯 Дріб→Дес",self.show_trainer_b),
            ("🎯 До тисячних",self.show_trainer_c),
            ("🎯 З тексту",self.show_trainer_d),
            ("🎯 Нулі-практика",self.show_trainer_z),
        ]
        for lbl,cmd in nav_items:
            b=tk.Button(nav,text=lbl,command=cmd,bg=NAV_BG,fg=NAV_FG,font=F_NAV,
                       relief="flat",bd=0,cursor="hand2",activebackground=ACCENT,activeforeground=WHITE,padx=8,pady=13)
            b.pack(side="left")
            b.bind("<Enter>",lambda e,x=b:x.config(bg=ACCENT)); b.bind("<Leave>",lambda e,x=b:x.config(bg=NAV_BG))
        self.main_area=tk.Frame(self,bg=BG); self.main_area.pack(fill="both",expand=True)

    def clear_main(self):
        # Close any matplotlib figures before destroying
        if self._nl_mpl_fig is not None:
            try: plt.close(self._nl_mpl_fig)
            except: pass
            self._nl_mpl_fig=None; self._nl_mpl_canvas=None
        if self.current_frame: self.current_frame.destroy()
        self.current_frame=tk.Frame(self.main_area,bg=BG); self.current_frame.pack(expand=True,fill="both")

    def _scroll_page(self):
        sc=tk.Canvas(self.current_frame,bg=BG,highlightthickness=0)
        vsb=tk.Scrollbar(self.current_frame,orient="vertical",command=sc.yview)
        sc.configure(yscrollcommand=vsb.set); vsb.pack(side="right",fill="y"); sc.pack(side="left",fill="both",expand=True)
        outer=tk.Frame(sc,bg=BG); win=sc.create_window((0,0),window=outer,anchor="nw")
        outer.bind("<Configure>",lambda e:sc.configure(scrollregion=sc.bbox("all")))
        sc.bind("<Configure>",lambda e:sc.itemconfig(win,width=e.width))
        p=tk.Frame(outer,bg=BG); p.pack(fill="both",expand=True,padx=50,pady=24)
        return p

    # ══ MAIN MENU ═════════════════════════════════════════════════════════════
    def show_main_menu(self):
        self.clear_main(); c=tk.Frame(self.current_frame,bg=BG); c.place(relx=.5,rely=.5,anchor="center")
        tk.Label(c,text="Десятковий дріб",font=("Segoe UI",44,"bold"),bg=BG,fg=TEXT).pack(pady=(0,4))
        tk.Label(c,text="§ 40   —  знайомство, запис, розряди, перетворення",font=("Segoe UI",20),bg=BG,fg=ACCENT).pack(pady=(0,18))
        cards=[
            ("📖","Теорія А\nЗапис",CARD_B,ACCENT,self.show_theory_a),
            ("📖","Теорія Б\nНулі↔знаки",CARD_V,ACCENT2,self.show_theory_b),
            ("📖","Нулі\nв кінці",TEAL_LT,TEAL,self.show_theory_c),
            ("🟦","Сітка",CARD_G,GREEN,self.show_grid),
            ("🔢","Розряди",CARD_Y,ORANGE,self.show_place_value),
            ("📏","Числова\nпряма",TEAL_LT,TEAL,self.show_number_line),
            ("🔗","Нулі↔знаки\nдемо",CARD_V,ACCENT2,self.show_zeros_demo),
            ("🎯","Дес→Дріб",CARD_G,GREEN,self.show_trainer_a),
            ("🎯","Дріб→Дес",CARD_Y,ORANGE,self.show_trainer_b),
            ("🎯","Точність запису",CARD_B,ACCENT,self.show_trainer_c),
            ("🎯","З тексту",CARD_V,ACCENT2,self.show_trainer_d),
            ("🎯","Нулі-практика",CARD_R,RED,self.show_trainer_z),
        ]
        row1=tk.Frame(c,bg=BG); row1.pack()
        row2=tk.Frame(c,bg=BG); row2.pack(pady=8)
        for i,(icon,title,bg_c,fg_c,cmd) in enumerate(cards):
            row=row1 if i<6 else row2
            card=tk.Frame(row,bg=bg_c,width=160,height=160,highlightbackground=BORDER,highlightthickness=2)
            card.pack(side="left",padx=6); card.pack_propagate(False)
            tk.Label(card,text=icon,font=("Segoe UI",28),bg=bg_c,fg=fg_c).pack(pady=(14,2))
            tk.Label(card,text=title,font=("Segoe UI",11,"bold"),bg=bg_c,fg=fg_c,justify="center").pack()
            for w in [card]+list(card.winfo_children()):
                w.bind("<Button-1>",lambda e,f=cmd:f())
            card.bind("<Enter>",lambda e,x=card,col=bg_c:x.config(bg=_dk(col,12)))
            card.bind("<Leave>",lambda e,x=card,col=bg_c:x.config(bg=col))

    # ══ THEORY A ══════════════════════════════════════════════════════════════
    def show_theory_a(self):
        self.clear_main(); p=self._scroll_page()
        tk.Label(p,text="Десятковий дріб: запис і читання",font=F_TITLE,bg=BG,fg=TEXT).pack(anchor="w")
        hline(p,ACCENT)
        idea_f=tk.Frame(p,bg=CARD_B,padx=22,pady=18,highlightbackground=ACCENT,highlightthickness=2); idea_f.pack(fill="x",pady=8)
        tk.Label(idea_f,text="📌  Що таке десятковий дріб?",font=F_SUB,bg=CARD_B,fg=ACCENT).pack(anchor="w")
        tk.Label(idea_f,text="Дроби зі знаменниками 10, 100, 1 000, … можна записати без знаменника —\nвідділивши цілу частину від дробової КОМОЮ.",
                 font=F_BODY,bg=CARD_B,fg=TEXT,justify="left").pack(anchor="w",pady=(8,6))
        ex_row=tk.Frame(idea_f,bg=CARD_B); ex_row.pack(anchor="w",pady=8)
        for whole,n,d,dec,read in [(7,3,10,"7,3","7 цілих 3 десятих"),(8,17,100,"8,17","8 цілих 17 сотих"),(9,71,1000,"9,071","9 цілих 71 тисячна")]:
            box=tk.Frame(ex_row,bg=PANEL,padx=18,pady=12,highlightbackground=BORDER,highlightthickness=1); box.pack(side="left",padx=10)
            fr=tk.Frame(box,bg=PANEL); fr.pack()
            tk.Label(fr,text=str(whole),font=F_FRAC_S,bg=PANEL,fg=TEXT).pack(side="left")
            frac_w(fr,n,d,PANEL,"small",ACCENT).pack(side="left",padx=6)
            tk.Label(fr,text=" = ",font=F_FRAC_S,bg=PANEL,fg=MUTED).pack(side="left")
            tk.Label(fr,text=dec,font=F_FRAC,bg=PANEL,fg=RED).pack(side="left")
            tk.Label(box,text=read,font=F_SMALL,bg=PANEL,fg=MUTED).pack(pady=(4,0))
        # Алгоритм
        alg_f=tk.Frame(p,bg=CARD_G,padx=22,pady=18,highlightbackground=GREEN,highlightthickness=2); alg_f.pack(fill="x",pady=8)
        tk.Label(alg_f,text="🔑  Алгоритм: звичайний → десятковий",font=F_SUB,bg=CARD_G,fg=GREEN).pack(anchor="w")
        for step,color,txt in [
            ("Крок 1",ACCENT,"Записати цілу частину, поставити кому"),
            ("Крок 2",GREEN,"Після коми записати чисельник із потрібною кількістю цифр"),
            ("⚠️",ORANGE,"Якщо цифр менше ніж нулів — доповнити нулями СПЕРЕДУ")]:
            r=tk.Frame(alg_f,bg=CARD_G); r.pack(anchor="w",pady=4)
            tk.Label(r,text=f"  {step}:  ",font=("Segoe UI",17,"bold"),bg=CARD_G,fg=color,width=12,anchor="w").pack(side="left")
            tk.Label(r,text=txt,font=("Segoe UI",17),bg=CARD_G,fg=TEXT,justify="left",wraplength=1100).pack(side="left")
        # Приклади з нулями
        zp_f=tk.Frame(alg_f,bg=PANEL,padx=16,pady=12,highlightbackground=BORDER,highlightthickness=1); zp_f.pack(fill="x",pady=8)
        tk.Label(zp_f,text="Приклади з нулями-вставками:",font=F_BODYB,bg=PANEL,fg=TEXT).pack(anchor="w")
        for fs,dec,note in [("3/1000","0,003","3 нулі → 2 нулі перед «3»"),("41/1000","0,041","3 нулі → 1 нуль перед «41»"),("29/100","0,29","2 нулі → нічого не треба")]:
            r=tk.Frame(zp_f,bg=PANEL); r.pack(anchor="w",pady=3)
            tk.Label(r,text=f"{fs}  =  ",font=F_BODY,bg=PANEL,fg=MUTED).pack(side="left")
            tk.Label(r,text=dec,font=("Segoe UI",22,"bold"),bg=PANEL,fg=RED).pack(side="left")
            tk.Label(r,text=f"    ({note})",font=F_SMALL,bg=PANEL,fg=MUTED).pack(side="left")
        # Таблиця розрядів
        tf=tk.Frame(p,bg=PANEL,padx=22,pady=18,highlightbackground=BORDER,highlightthickness=1); tf.pack(fill="x",pady=8)
        tk.Label(tf,text="📐  Розряди: число 17,295",font=F_SUB,bg=PANEL,fg=TEXT).pack(anchor="w")
        tbl=tk.Frame(tf,bg=PANEL); tbl.pack(anchor="w",pady=8)
        headers=["Десятки","Одиниці","","Десяті","Соті","Тисячні"]
        hcols=[TEXT,TEXT,MUTED,ACCENT,ACCENT2,GREEN]
        hbgs=[CARD_B,CARD_B,PANEL,CARD_G,CARD_G,CARD_G]
        for j,(h,hc,hb) in enumerate(zip(headers,hcols,hbgs)):
            cell=tk.Frame(tbl,bg=hb,padx=14,pady=8,width=100,height=50,highlightbackground=BORDER,highlightthickness=1)
            cell.grid(row=0,column=j,padx=2,pady=2)
            tk.Label(cell,text=h,font=F_SMALL,bg=hb,fg=hc).pack(expand=True)
        digs=[("1",TEXT,CARD_B),("7",TEXT,CARD_B),(",",MUTED,PANEL),("2",ACCENT,CARD_G),("9",ACCENT2,CARD_G),("5",GREEN,CARD_G)]
        for j,(d,dc,db) in enumerate(digs):
            c=tk.Frame(tbl,bg=db,padx=14,pady=8,width=100,height=70,highlightbackground=BORDER,highlightthickness=1)
            c.grid(row=1,column=j,padx=2,pady=2); c.pack_propagate(False)
            fn=("Segoe UI",36,"bold") if d!="," else ("Segoe UI",48,"bold")
            tk.Label(c,text=d,font=fn,bg=db,fg=dc).pack(expand=True)
        theory_card(p,"💡  Запам'ятай",
            "Скільки нулів у знаменнику → стільки цифр після коми.\n"
            "Якщо цифр менше — доповнюємо нулями зліва.\n"
            "Десяті: 1 цифра.  Соті: 2.  Тисячні: 3.","#f1f5f9",MUTED)

    # ══ THEORY B ══════════════════════════════════════════════════════════════
    def show_theory_b(self):
        self.clear_main(); p=self._scroll_page()
        tk.Label(p,text="Зв'язок: знаки після коми ↔ нулі у знаменнику",font=F_TITLE,bg=BG,fg=TEXT).pack(anchor="w")
        hline(p,ACCENT2)
        rule_f=tk.Frame(p,bg=CARD_V,padx=22,pady=18,highlightbackground=ACCENT2,highlightthickness=2); rule_f.pack(fill="x",pady=8)
        tk.Label(rule_f,text="📌  Головне правило",font=F_SUB,bg=CARD_V,fg=ACCENT2).pack(anchor="w")
        for line,color in [("Скільки цифр після коми → стільки нулів у знаменнику",ACCENT2),("Скільки нулів у знаменнику → стільки цифр після коми",GREEN)]:
            tk.Label(rule_f,text=f"●  {line}",font=F_BODYB,bg=CARD_V,fg=color).pack(anchor="w",pady=3)
        tbl_f=tk.Frame(rule_f,bg=CARD_V); tbl_f.pack(anchor="w",pady=12)
        for j,h in enumerate(["Знаменник","Нулів","Знаків після коми","Назва розряду","Приклад"]):
            tk.Label(tbl_f,text=h,font=("Segoe UI",14,"bold"),bg=ACCENT2,fg=WHITE,padx=16,pady=6,width=20 if j>1 else 12,relief="flat").grid(row=0,column=j,padx=1,pady=1)
        rows_data=[("10","1","1","десяті","0,7"),("100","2","2","соті","0,49"),("1 000","3","3","тисячні","0,041"),("10 000","4","4","десятитисячні","0,0071")]
        row_bgs=[CARD_B,CARD_G,CARD_Y,TEAL_LT]
        for r,(dn,zs,dg,nm,ex) in enumerate(rows_data):
            bg_r=row_bgs[r%4]
            for j,v in enumerate([dn,zs,dg,nm,ex]):
                col=C_ZERO if j==1 else (C_DIGIT if j==2 else TEXT)
                tk.Label(tbl_f,text=v,font=("Segoe UI",16,"bold" if j<3 else "normal"),bg=bg_r,fg=col,padx=16,pady=8,width=20 if j>1 else 12,relief="flat").grid(row=r+1,column=j,padx=1,pady=1)
        # Доповнення нулями
        zp_f=tk.Frame(p,bg=CARD_G,padx=22,pady=18,highlightbackground=GREEN,highlightthickness=2); zp_f.pack(fill="x",pady=8)
        tk.Label(zp_f,text="⚠️  Доповнення нулями",font=F_SUB,bg=CARD_G,fg=GREEN).pack(anchor="w")
        zp_row=tk.Frame(zp_f,bg=CARD_G); zp_row.pack(anchor="w",pady=8)
        for ns,ds,dec,note in [("3","1000","0,003","2 нулі перед «3»"),("41","1000","0,041","1 нуль перед «41»"),("219","1000","0,219","нічого не треба"),("7","100","0,07","1 нуль перед «7»")]:
            box=tk.Frame(zp_row,bg=PANEL,padx=14,pady=12,highlightbackground=BORDER,highlightthickness=1); box.pack(side="left",padx=8)
            fr=tk.Frame(box,bg=PANEL); fr.pack()
            tk.Label(fr,text=ns,font=("Courier New",28,"bold"),bg=PANEL,fg=C_DIGIT).pack()
            tk.Frame(fr,bg=BORDER,height=3,width=80).pack(pady=2,fill="x")
            tk.Label(fr,text=ds,font=("Courier New",28,"bold"),bg=PANEL,fg=C_ZERO).pack()
            tk.Label(box,text="= "+dec,font=("Courier New",28,"bold"),bg=PANEL,fg=RED).pack(pady=4)
            tk.Label(box,text=note,font=F_SMALL,bg=PANEL,fg=MUTED).pack()
        # Десятковий → звичайний
        rev_f=tk.Frame(p,bg=CARD_B,padx=22,pady=18,highlightbackground=ACCENT,highlightthickness=2); rev_f.pack(fill="x",pady=8)
        tk.Label(rev_f,text="🔄  Десятковий → звичайний дріб",font=F_SUB,bg=CARD_B,fg=ACCENT).pack(anchor="w")
        tk.Label(rev_f,text="Рахуємо цифри після коми → стільки нулів у знаменнику.\nЦифри після коми (з нулями) = чисельник.",font=F_BODY,bg=CARD_B,fg=TEXT,justify="left").pack(anchor="w",pady=(6,8))
        rev_row=tk.Frame(rev_f,bg=CARD_B); rev_row.pack(anchor="w",pady=4)
        for dec,n,d in [("0,7","7","10"),("0,49","49","100"),("0,041","41","1000"),("3,007","3007","1000")]:
            box=tk.Frame(rev_row,bg=PANEL,padx=14,pady=10,highlightbackground=BORDER,highlightthickness=1); box.pack(side="left",padx=8)
            tk.Label(box,text=dec,font=("Courier New",28,"bold"),bg=PANEL,fg=RED).pack()
            tk.Label(box,text="=",font=F_HEAD,bg=PANEL,fg=MUTED).pack()
            frac_w(box,n,d,PANEL,"small",ACCENT).pack()
        theory_card(p,"💡  Запам'ятай",
            "Десятковий → звичайний: рахуй цифри після коми → нулі знаменника.\n"
            "Звичайний → десятковий: рахуй нулі → заповни цифри після коми (додай нулі зліва якщо треба).","#f1f5f9",MUTED)

    # ══ THEORY C ══════════════════════════════════════════════════════════════
    def show_theory_c(self):
        self.clear_main(); p=self._scroll_page()
        tk.Label(p,text="Нулі в кінці десяткового дробу",font=F_TITLE,bg=BG,fg=TEXT).pack(anchor="w")
        hline(p,TEAL)
        rule_f=tk.Frame(p,bg=TEAL_LT,padx=22,pady=18,highlightbackground=TEAL,highlightthickness=2); rule_f.pack(fill="x",pady=8)
        tk.Label(rule_f,text="📌  Головне правило",font=F_SUB,bg=TEAL_LT,fg=TEAL).pack(anchor="w")
        tk.Label(rule_f,text="Нулі в кінці дробової частини НЕ змінюють значення числа.\nЇх можна дописувати і прибирати — число залишається тим самим.",
                 font=F_BODY,bg=TEAL_LT,fg=TEXT,justify="left").pack(anchor="w",pady=(8,4))
        # Рівні записи
        eq_f=tk.Frame(p,bg=PANEL,padx=22,pady=18,highlightbackground=BORDER,highlightthickness=1); eq_f.pack(fill="x",pady=8)
        tk.Label(eq_f,text="📊  Всі ці записи рівні між собою:",font=F_SUB,bg=PANEL,fg=TEXT).pack(anchor="w")
        eq_row=tk.Frame(eq_f,bg=PANEL); eq_row.pack(anchor="w",pady=12)
        for group in [["0,5","0,50","0,500"],["1,3","1,30","1,300"],["2,70","2,7","2,700"]]:
            box=tk.Frame(eq_row,bg=CARD_B,padx=16,pady=12,highlightbackground=ACCENT,highlightthickness=1); box.pack(side="left",padx=10)
            for i,s in enumerate(group):
                col=RED if i==0 else (_dk(RED,20) if i==1 else _dk(RED,35))
                tk.Label(box,text=s,font=("Courier New",30,"bold"),bg=CARD_B,fg=col).pack()
                if i<len(group)-1:
                    tk.Label(box,text="=",font=("Segoe UI",18),bg=CARD_B,fg=MUTED).pack()
        # Чому це працює
        frac_f=tk.Frame(p,bg=CARD_G,padx=22,pady=18,highlightbackground=GREEN,highlightthickness=2); frac_f.pack(fill="x",pady=8)
        tk.Label(frac_f,text="🔑  Чому це працює? — Дробовий запис",font=F_SUB,bg=CARD_G,fg=GREEN).pack(anchor="w")
        tk.Label(frac_f,text="Додавання нуля в кінці = множення чисельника і знаменника на 10 → дріб не змінюється:",
                 font=F_BODY,bg=CARD_G,fg=TEXT,justify="left").pack(anchor="w",pady=(6,8))
        frac_row=tk.Frame(frac_f,bg=CARD_G); frac_row.pack(anchor="w")
        for n1,d1,n2,d2 in [("5","10","50","100"),("3","10","30","100"),("7","100","70","1000")]:
            box=tk.Frame(frac_row,bg=PANEL,padx=14,pady=10,highlightbackground=BORDER,highlightthickness=1); box.pack(side="left",padx=10)
            row2=tk.Frame(box,bg=PANEL); row2.pack()
            frac_w(row2,n1,d1,PANEL,"small",ACCENT).pack(side="left")
            tk.Label(row2,text=" = ",font=F_HEAD,bg=PANEL,fg=MUTED).pack(side="left")
            frac_w(row2,n2,d2,PANEL,"small",GREEN).pack(side="left")
            dec1=f"0,{n1.zfill(len(d1)-1)}"; dec2=f"0,{n2.zfill(len(d2)-1)}"
            tk.Label(box,text=f"{dec1} = {dec2}",font=("Courier New",20,"bold"),bg=PANEL,fg=RED).pack(pady=(6,0))
        # Коли прибираємо нулі
        rem_f=tk.Frame(p,bg=CARD_Y,padx=22,pady=18,highlightbackground=ORANGE,highlightthickness=2); rem_f.pack(fill="x",pady=8)
        tk.Label(rem_f,text="✂️  Скорочення: прибираємо зайві нулі",font=F_SUB,bg=CARD_Y,fg=ORANGE).pack(anchor="w")
        tk.Label(rem_f,text="Прибираємо тільки кінцеві нулі дробової частини. Нулі всередині або на початку — НЕ чіпаємо!",
                 font=F_BODY,bg=CARD_Y,fg=TEXT,justify="left").pack(anchor="w",pady=(6,8))
        rem_row=tk.Frame(rem_f,bg=CARD_Y); rem_row.pack(anchor="w")
        for before,after,note in [("0,500","0,5","можна прибрати"),("3,120","3,12","можна прибрати"),("0,041","0,041","НЕ прибирати! (не кінцевий)"),("1,300","1,3","можна прибрати")]:
            box=tk.Frame(rem_row,bg=PANEL,padx=12,pady=10,highlightbackground=BORDER,highlightthickness=1); box.pack(side="left",padx=8)
            tk.Label(box,text=before,font=("Courier New",26,"bold"),bg=PANEL,fg=MUTED).pack()
            tk.Label(box,text="→",font=("Segoe UI",22),bg=PANEL,fg=MUTED).pack()
            col=GREEN if "можна" in note else RED
            tk.Label(box,text=after,font=("Courier New",26,"bold"),bg=PANEL,fg=col).pack()
            tk.Label(box,text=note,font=F_SMALL,bg=PANEL,fg=col).pack(pady=(4,0))
        # Коли дописуємо нулі
        add_f=tk.Frame(p,bg=CARD_V,padx=22,pady=18,highlightbackground=ACCENT2,highlightthickness=2); add_f.pack(fill="x",pady=8)
        tk.Label(add_f,text="✏️  Коли ДОПИСУЄМО нулі — для чого це потрібно",font=F_SUB,bg=CARD_V,fg=ACCENT2).pack(anchor="w")
        for title,ex in [
            ("Порівняння","0,3 та 0,27  →  0,30 та 0,27  →  30>27  →  0,3>0,27"),
            ("Додавання/Віднімання","0,5 + 0,37  →  0,50 + 0,37 = 0,87"),
            ("Однакова кількість знаків","3,1  →  3,100  (щоб була однакова кількість цифр)"),
        ]:
            uf=tk.Frame(add_f,bg=PANEL,padx=14,pady=10,highlightbackground=BORDER,highlightthickness=1); uf.pack(fill="x",pady=4)
            tk.Label(uf,text=f"▶  {title}:",font=F_BODYB,bg=PANEL,fg=ACCENT2).pack(anchor="w")
            tk.Label(uf,text=ex,font=("Courier New",20,"bold"),bg=PANEL,fg=TEXT).pack(anchor="w",pady=(2,0))
        theory_card(p,"💡  Запам'ятай",
            "0,5 = 0,50 = 0,500  — значення не змінюється.\n"
            "Кінцеві нулі після коми можна прибирати і дописувати вільно.\n"
            "Але нулі всередині (0,041) і нулі цілої частини — НЕ чіпаємо!","#f1f5f9",MUTED)

    # ══ GRID ══════════════════════════════════════════════════════════════════
    def show_grid(self):
        self.clear_main(); cf=self.current_frame
        toolbar=tk.Frame(cf,bg=PANEL,highlightbackground=BORDER,highlightthickness=1,height=56)
        toolbar.pack(fill="x"); toolbar.pack_propagate(False)
        self.gmode_btns={}
        for mode,label,color in [("tenths","Десяті (÷10)",FILL_10),("hundredths","Соті (÷100)",FILL_100),("thousandths","Тисячні (÷1000)",FILL_1000)]:
            b=tk.Button(toolbar,text=label,font=("Segoe UI",12,"bold"),bg=BTN_NUM,fg=TEXT,relief="flat",cursor="hand2",padx=14,pady=4,command=lambda m=mode:self._gset(m))
            b.pack(side="left",padx=6,pady=8); self.gmode_btns[mode]=(b,color)
        tk.Frame(toolbar,bg=BORDER,width=2).pack(side="left",fill="y",padx=6,pady=8)
        self.gtask_btn=tk.Button(toolbar,text="🎯  Завдання",font=("Segoe UI",13,"bold"),bg=CARD_Y,fg=ORANGE,relief="flat",cursor="hand2",padx=12,pady=6,command=self._gtoggle)
        self.gtask_btn.pack(side="left",padx=6)
        self.gscore_lbl=tk.Label(toolbar,text="",font=("Segoe UI",14,"bold"),bg=PANEL,fg=GREEN); self.gscore_lbl.pack(side="left",padx=12)
        self._gnext_btn=mkbtn(toolbar,"▶  Наступне",self._gadvance,bg=BTN_NUM,fg=MUTED,font=("Segoe UI",12,"bold"),w=10,h=1)
        self._gnext_btn.pack(side="right",padx=6); self._gnext_btn.config(state="disabled")
        mkbtn(toolbar,"🗑  Очистити",self._gclear,bg=BTN_NUM,fg=TEXT,font=("Segoe UI",12,"bold"),w=10,h=1).pack(side="right",padx=10)
        ws=tk.Frame(cf,bg=BG); ws.pack(fill="both",expand=True,padx=12,pady=10)
        left=tk.Frame(ws,bg=PANEL,highlightbackground=BORDER,highlightthickness=1); left.pack(side="left",fill="both",expand=True,padx=(0,10))
        self.gtask_lbl=tk.Label(left,text="",font=("Segoe UI",17,"bold"),bg=PANEL,fg=ORANGE); self.gtask_lbl.pack(pady=(6,0))
        self.gcanvas=tk.Canvas(left,bg=PANEL,highlightthickness=0)
        self.gcanvas.pack(fill="both",expand=True,padx=8,pady=8)
        self.gcanvas.bind("<Configure>",self._gdraw); self.gcanvas.bind("<Button-1>",self._gclick); self.gcanvas.bind("<B1-Motion>",self._gclick)
        right=tk.Frame(ws,bg=PANEL,highlightbackground=BORDER,highlightthickness=1,width=280); right.pack(side="right",fill="y"); right.pack_propagate(False)
        tk.Label(right,text="Звичайний дріб:",font=("Segoe UI",15),bg=PANEL,fg=MUTED).pack(pady=(18,4))
        self.gfrac_f=tk.Frame(right,bg=PANEL); self.gfrac_f.pack(pady=4)
        tk.Label(right,text="Десятковий дріб:",font=("Segoe UI",15),bg=PANEL,fg=MUTED).pack(pady=(18,4))
        self.gdec_lbl=tk.Label(right,text="0",font=("Courier New",58,"bold"),bg=PANEL,fg=RED); self.gdec_lbl.pack(pady=4)
        self.gfeed_lbl=tk.Label(right,text="",font=("Segoe UI",16,"bold"),bg=PANEL,fg=GREEN,wraplength=270,justify="center"); self.gfeed_lbl.pack(pady=10)
        self._gset("tenths")

    def _gtotal(self): return {"tenths":10,"hundredths":100,"thousandths":1000}[self.gmode]
    def _glayout(self): return {"tenths":(10,1),"hundredths":(10,10),"thousandths":(25,40)}[self.gmode]
    def _gfill(self): return {"tenths":FILL_10,"hundredths":FILL_100,"thousandths":FILL_1000}[self.gmode]

    def _gset(self,mode):
        self.gmode=mode; self.gval=0
        for m,(b,col) in self.gmode_btns.items():
            b.config(bg=col if m==mode else BTN_NUM,fg=WHITE if m==mode else TEXT)
        if self.gtask: self._gnew_task()
        else: self._gdraw(); self._gupdate()

    def _gclear(self):
        self.gval=0; self.gfeed_lbl.config(text="")
        if self.gtask: self.glocked=False
        self._gdraw(); self._gupdate()

    def _gtoggle(self):
        self.gtask=not self.gtask
        if self.gtask:
            self.gtask_btn.config(bg=RED,fg=WHITE,text="⏹  Зупинити"); self.gscore=0; self.gtotal=0; self._gnew_task()
        else:
            self.gtask_btn.config(bg=CARD_Y,fg=ORANGE,text="🎯  Завдання")
            self.gtask_lbl.config(text=""); self.gfeed_lbl.config(text=""); self.gscore_lbl.config(text="")

    def _gnew_task(self):
        self.glocked=False; total=self._gtotal(); self.gtarget=random.randint(1,total)
        val=self.gtarget/total; places={10:1,100:2,1000:3}[total]
        dec_s=f"{val:.{places}f}".replace(".",",")
        prompt=dec_s if random.random()<0.5 else f"{self.gtarget}/{total}"
        self.gtask_lbl.config(text=f"📋  Зафарбуй:  {prompt}",fg=ORANGE)
        if hasattr(self,"_gnext_btn"): self._gnext_btn.config(state="disabled",bg=BTN_NUM,fg=MUTED)
        self._gclear()

    def _gadvance(self):
        self._gnext_btn.config(state="disabled",bg=BTN_NUM,fg=MUTED); self._gnew_task()

    def _gclick(self,event):
        if self.gtask and self.glocked: return
        if not hasattr(self,"_gx0"): return
        x=event.x-self._gx0; y=event.y-self._gy0
        rows,cols=self._glayout()
        if x<0 or y<0 or x>self._gsz or y>self._gsz: return
        c=min(int(x/self._cw),cols-1); r=min(int(y/self._ch),rows-1)
        self.gval=min(r*cols+c+1,self._gtotal())
        self._gdraw(); self._gupdate()
        if self.gtask: self._gcheck()

    def _gdraw(self,event=None):
        cv=self.gcanvas; cv.delete("all")
        W=cv.winfo_width(); H=cv.winfo_height()
        if W<20 or H<20: return
        rows,cols=self._glayout(); pad=12
        sz=min(W-2*pad,H-2*pad); x0=(W-sz)//2; y0=(H-sz)//2
        self._gx0=x0; self._gy0=y0; self._gsz=sz
        self._cw=sz/cols; self._ch=sz/rows
        fill=self._gfill(); filled=self.gval; total=self._gtotal()
        if self.gmode=="thousandths":
            for i in range(total):
                r2=i//cols; c2=i%cols
                x1=x0+c2*self._cw; y1=y0+r2*self._ch; x2=x1+self._cw; y2=y1+self._ch
                cv.create_rectangle(x1,y1,x2,y2,fill=fill if i<filled else C_EMPTY,outline="")
            for r2 in range(rows+1):
                y=y0+r2*self._ch; lw=2 if r2%5==0 else 1
                cv.create_line(x0,y,x0+sz,y,fill=_dk(fill,40) if r2%5==0 else BORDER,width=lw)
            for c2 in range(cols+1):
                x=x0+c2*self._cw; lw=2 if c2%8==0 else 1
                cv.create_line(x,y0,x,y0+sz,fill=_dk(fill,40) if c2%8==0 else BORDER,width=lw)
            cv.create_rectangle(x0,y0,x0+sz,y0+sz,outline=_dk(fill,50),width=3)
        else:
            for i in range(total):
                r2=i//cols; c2=i%cols
                x1=x0+c2*self._cw; y1=y0+r2*self._ch; x2=x1+self._cw; y2=y1+self._ch
                color=fill if i<filled else C_EMPTY
                bc=_dk(fill,25) if i<filled else BORDER
                cv.create_rectangle(x1,y1,x2,y2,fill=color,outline=bc,width=1)
            if self.gmode=="hundredths":
                for r2 in range(rows+1):
                    y=y0+r2*self._ch; lw=3 if r2%10==0 else 1; col2=TEXT if r2%10==0 else BORDER
                    cv.create_line(x0,y,x0+sz,y,fill=col2,width=lw)
                for c2 in range(cols+1):
                    x=x0+c2*self._cw; lw=3 if c2%10==0 else 1; col2=TEXT if c2%10==0 else BORDER
                    cv.create_line(x,y0,x,y0+sz,fill=col2,width=lw)
            else:
                for r2 in range(rows+1):
                    cv.create_line(x0,y0+r2*self._ch,x0+sz,y0+r2*self._ch,fill=MUTED,width=2)
                cv.create_line(x0,y0,x0,y0+sz,fill=MUTED,width=2)
                cv.create_line(x0+sz,y0,x0+sz,y0+sz,fill=MUTED,width=2)

    def _gupdate(self):
        total=self._gtotal(); val=self.gval/total
        for w in self.gfrac_f.winfo_children(): w.destroy()
        frac_w(self.gfrac_f,self.gval,total,PANEL,"big",ACCENT).pack()
        places={10:1,100:2,1000:3}[total]
        self.gdec_lbl.config(text=f"{val:.{places}f}".replace(".",","))

    def _gcheck(self):
        if self.gval==self.gtarget:
            self.glocked=True; self.gscore+=1; self.gtotal+=1
            self.gfeed_lbl.config(text="✅  Правильно!",fg=GREEN)
            self.gscore_lbl.config(text=f"Рахунок: {self.gscore}/{self.gtotal}")
            self._gnext_btn.config(state="normal",bg=ACCENT,fg=WHITE)

    # ══ PLACE VALUE ═══════════════════════════════════════════════════════════
    PVNAMES=["Одиниці","Десяті","Соті","Тисячні"]
    PVCOLORS=[TEXT,ACCENT,ACCENT2,GREEN]

    def show_place_value(self):
        self.clear_main(); cf=self.current_frame
        sbar=tk.Frame(cf,bg=PANEL,height=56,highlightbackground=BORDER,highlightthickness=1)
        sbar.pack(fill="x"); sbar.pack_propagate(False)
        tk.Label(sbar,text="Кількість знаків після коми:",font=("Segoe UI",14),bg=PANEL,fg=MUTED).pack(side="left",padx=18)
        self._pv_prec_btns=[]
        for n in [1,2,3]:
            b=tk.Button(sbar,text=str(n),font=("Segoe UI",15,"bold"),bg=BTN_NUM,fg=TEXT,width=3,height=1,relief="flat",cursor="hand2",command=lambda k=n:self._pvset(k))
            b.pack(side="left",padx=5,pady=10); self._pv_prec_btns.append(b)
        ws=tk.Frame(cf,bg=BG); ws.pack(fill="both",expand=True,padx=14,pady=10)
        left=tk.Frame(ws,bg=PANEL,highlightbackground=BORDER,highlightthickness=1,width=480); left.pack(side="left",fill="y"); left.pack_propagate(False)
        tk.Label(left,text="Зміни розряди:",font=F_SUB,bg=PANEL,fg=MUTED).pack(anchor="w",padx=18,pady=(12,4))
        self._pv_ctrl=tk.Frame(left,bg=PANEL); self._pv_ctrl.pack(fill="x",padx=14)
        right=tk.Frame(ws,bg=PANEL,highlightbackground=BORDER,highlightthickness=1); right.pack(side="right",fill="both",expand=True,padx=(10,0))
        nf=tk.Frame(right,bg=PANEL); nf.pack(expand=True)
        tk.Label(nf,text="Десятковий дріб:",font=("Segoe UI",17),bg=PANEL,fg=MUTED).pack(pady=(0,4))
        self._pv_ncv=tk.Canvas(nf,bg=PANEL,height=110,highlightthickness=0); self._pv_ncv.pack(fill="x",padx=24,pady=4)
        tk.Label(nf,text="Як звичайний дріб:",font=("Segoe UI",17),bg=PANEL,fg=MUTED).pack(pady=(14,4))
        self._pv_frow=tk.Frame(nf,bg=PANEL); self._pv_frow.pack()
        tk.Label(nf,text="Читається:",font=("Segoe UI",17),bg=PANEL,fg=MUTED).pack(pady=(14,4))
        self._pv_rlbl=tk.Label(nf,text="",font=("Segoe UI",19,"bold"),bg=PANEL,fg=ACCENT,wraplength=560,justify="center"); self._pv_rlbl.pack(pady=4)
        self._pvset(self.pv_places)

    def _pvset(self,n):
        self.pv_places=n
        for i,b in enumerate(self._pv_prec_btns):
            b.config(bg=ACCENT if i+1==n else BTN_NUM,fg=WHITE if i+1==n else TEXT)
        self._pvrebuild(); self._pvrefresh()

    def _pvrebuild(self):
        for w in self._pv_ctrl.winfo_children(): w.destroy()
        for i in range(self.pv_places+1):
            color=self.PVCOLORS[i]
            row=tk.Frame(self._pv_ctrl,bg=BTN_NUM,pady=7,padx=10); row.pack(fill="x",pady=4)
            tk.Label(row,text=self.PVNAMES[i],font=("Segoe UI",15,"bold"),bg=BTN_NUM,fg=color,width=12,anchor="w").pack(side="left")
            def dec(idx=i):self._pvchange(idx,-1)
            def inc(idx=i):self._pvchange(idx,1)
            tk.Button(row,text="−",font=F_CTRL,width=3,bg=PANEL,fg=TEXT,relief="flat",cursor="hand2",command=dec).pack(side="left",padx=6)
            tk.Label(row,text=str(self.pv_digits[i]),font=("Courier New",32,"bold"),bg=BTN_NUM,fg=color,width=2).pack(side="left",padx=8)
            tk.Button(row,text="+",font=F_CTRL,width=3,bg=PANEL,fg=TEXT,relief="flat",cursor="hand2",command=inc).pack(side="left",padx=6)

    def _pvchange(self,idx,delta):
        new=self.pv_digits[idx]+delta
        if new>9: self.pv_digits[idx]=0; (self._pvcarry(idx-1,+1) if idx>0 else None)
        elif new<0:
            if idx>0 and self.pv_digits[idx-1]>0: self.pv_digits[idx]=9; self._pvcarry(idx-1,-1)
        else: self.pv_digits[idx]=new
        self._pvrebuild(); self._pvrefresh()

    def _pvcarry(self,idx,delta):
        new=self.pv_digits[idx]+delta
        if new>9: self.pv_digits[idx]=0; (self._pvcarry(idx-1,+1) if idx>0 else None)
        elif new<0:
            if idx>0 and self.pv_digits[idx-1]>0: self.pv_digits[idx]=9; self._pvcarry(idx-1,-1)
            else: self.pv_digits[idx]=0
        else: self.pv_digits[idx]=new

    def _pvrefresh(self):
        val=float(self.pv_digits[0])
        for i in range(1,self.pv_places+1): val+=self.pv_digits[i]*(10**-i)
        val=round(val,self.pv_places)
        cv=self._pv_ncv; cv.delete("all"); cv.update_idletasks()
        W=cv.winfo_width() or 540; H=110
        ws=str(self.pv_digits[0]); ds="".join(str(self.pv_digits[i]) for i in range(1,self.pv_places+1))
        chars=[(ws,self.PVCOLORS[0]),(",",MUTED)]+[(ds[i],self.PVCOLORS[i+1]) for i in range(len(ds))]
        cw=52; total_w=len(chars)*cw; x=(W-total_w)//2
        for ch,col in chars:
            cv.create_text(x+cw//2,H//2,text=ch,font=("Segoe UI",66,"bold"),fill=col,anchor="center"); x+=cw
        for w in self._pv_frow.winfo_children(): w.destroy()
        denom=10**self.pv_places; wp=int(val); fp=round(val-wp,self.pv_places); nm=int(round(fp*denom))
        if wp>0 and nm>0:
            tk.Label(self._pv_frow,text=str(wp),font=F_FRAC,bg=PANEL,fg=TEXT).pack(side="left",padx=(0,8))
            frac_w(self._pv_frow,nm,denom,PANEL,"big",ACCENT).pack(side="left")
        elif wp>0: tk.Label(self._pv_frow,text=str(wp),font=F_FRAC,bg=PANEL,fg=TEXT).pack(side="left")
        else: frac_w(self._pv_frow,nm,denom,PANEL,"big",ACCENT).pack(side="left")
        names={1:"десятих",2:"сотих",3:"тисячних"}; pn=names.get(self.pv_places,"")
        if wp>0 and nm>0: read=f"{wp} {'ціла' if wp==1 else 'цілих'}  {nm} {pn}"
        elif wp>0: read=f"{wp} {'ціла' if wp==1 else 'цілих'}"
        else: read=f"нуль цілих  {nm} {pn}"
        self._pv_rlbl.config(text=read)

    # ══ NUMBER LINE (matplotlib) ═══════════════════════════════════════════════
    def show_number_line(self):
        self.clear_main(); cf=self.current_frame

        # ── toolbar
        tb=tk.Frame(cf,bg=PANEL,height=52,highlightbackground=BORDER,highlightthickness=1)
        tb.pack(fill="x"); tb.pack_propagate(False)
        tk.Label(tb,text="📏  Числова пряма",font=("Segoe UI",16,"bold"),bg=PANEL,fg=TEXT).pack(side="left",padx=18)
        self._nl_task_btn=tk.Button(tb,text="🎯  Завдання",font=("Segoe UI",13,"bold"),
            bg=CARD_Y,fg=ORANGE,relief="flat",cursor="hand2",padx=12,pady=5,command=self._nl_toggle_task)
        self._nl_task_btn.pack(side="left",padx=12)
        self._nl_task_score_lbl=tk.Label(tb,text="",font=("Segoe UI",13,"bold"),bg=PANEL,fg=GREEN)
        self._nl_task_score_lbl.pack(side="left",padx=6)

        # ── task banner (прихований)
        self._nl_task_frame=tk.Frame(cf,bg=CARD_Y,padx=16,pady=8,highlightbackground=ORANGE,highlightthickness=2)
        self._nl_task_target_lbl=tk.Label(self._nl_task_frame,text="",font=("Segoe UI",18,"bold"),bg=CARD_Y,fg=ORANGE)
        self._nl_task_target_lbl.pack(side="left",padx=(0,16))
        self._nl_task_feed_lbl=tk.Label(self._nl_task_frame,text="",font=("Segoe UI",15,"bold"),bg=CARD_Y,fg=GREEN)
        self._nl_task_feed_lbl.pack(side="left")
        self._nl_task_next_btn=tk.Button(self._nl_task_frame,text="▶  Наступне",
            font=("Segoe UI",12,"bold"),bg=ACCENT,fg=WHITE,relief="flat",cursor="hand2",
            padx=10,pady=4,state="disabled",command=self._nl_next_task)
        self._nl_task_next_btn.pack(side="right",padx=6)
        self._nl_task_frame.pack_forget()

        # ── matplotlib figure
        self._nl_fig, self._nl_ax = plt.subplots(figsize=(12,2.6), facecolor="#f0f4f8")
        self._nl_mpl_fig = self._nl_fig
        self._nl_fig.subplots_adjust(left=0.04,right=0.98,top=0.82,bottom=0.25)
        self._nl_mpl_canvas=FigureCanvasTkAgg(self._nl_fig, master=cf)
        self._nl_mpl_canvas.get_tk_widget().pack(fill="x",padx=16,pady=(6,0))

        # ── Лічильники (завжди всі 4: цілі, десяті, соті, тисячні)
        self._nl_ones=0; self._nl_tenths=0; self._nl_hunds=0; self._nl_thous=0

        ctrl_outer=tk.Frame(cf,bg=BG); ctrl_outer.pack(pady=(4,2))

        # Рядок 1: масштаб осі (окремо від лічильників)
        scale_row=tk.Frame(ctrl_outer,bg=BG); scale_row.pack(pady=(0,4))
        tk.Label(scale_row,text="Масштаб осі:",font=("Segoe UI",12,"bold"),bg=BG,fg=MUTED).pack(side="left",padx=(0,8))
        self._nl_scale="tenths"   # ones | tenths | hundredths | thousandths
        self._nl_scale_btns=[]
        for sc,lbl2,stv in [("ones","Цілі","1"),("tenths","Десяті","0,1"),
                             ("hundredths","Соті","0,01"),("thousandths","Тисячні","0,001")]:
            b=tk.Button(scale_row,text=f"{lbl2} ({stv})",font=("Segoe UI",11,"bold"),
                       bg=BTN_NUM,fg=TEXT,relief="flat",cursor="hand2",padx=10,pady=4,
                       command=lambda s=sc:_nlscale(s))
            b.pack(side="left",padx=3)
            self._nl_scale_btns.append((b,sc))

        # Рядок 2: лічильники — завжди всі 4
        cnt_row=tk.Frame(ctrl_outer,bg=BG); cnt_row.pack(pady=2)

        def make_counter(parent, label, attr, color):
            f=tk.Frame(parent,bg=CARD_B,padx=8,pady=5,highlightbackground=BORDER,highlightthickness=1)
            f.pack(side="left",padx=5)
            tk.Label(f,text=label,font=("Segoe UI",11,"bold"),bg=CARD_B,fg=color).pack()
            inner=tk.Frame(f,bg=CARD_B); inner.pack()
            def do_dec():
                v=getattr(self,attr)
                if v>0: setattr(self,attr,v-1)
                # якщо v==0 — нічого не робимо (мінімум 0)
                _nlredraw()
            def do_inc():
                v=getattr(self,attr)
                if v<9: setattr(self,attr,v+1)
                else: setattr(self,attr,0)  # 9→0 overflow (тільки вгору)
                _nlredraw()
            tk.Button(inner,text="−",font=("Segoe UI",18,"bold"),width=2,bg=BTN_NUM,fg=TEXT,
                     relief="flat",cursor="hand2",command=do_dec).pack(side="left",padx=2)
            lbl_w=tk.Label(inner,text="0",font=("Courier New",28,"bold"),bg=CARD_B,fg=color,width=2)
            lbl_w.pack(side="left")
            tk.Button(inner,text="+",font=("Segoe UI",18,"bold"),width=2,bg=BTN_NUM,fg=TEXT,
                     relief="flat",cursor="hand2",command=do_inc).pack(side="left",padx=2)
            return lbl_w

        self._nl_ones_lbl  =make_counter(cnt_row,"Цілі",   "_nl_ones",  TEXT)
        self._nl_tenth_lbl =make_counter(cnt_row,"Десяті",  "_nl_tenths",ACCENT)
        self._nl_hund_lbl  =make_counter(cnt_row,"Соті",    "_nl_hunds", ACCENT2)
        self._nl_thous_lbl =make_counter(cnt_row,"Тисячні", "_nl_thous", GREEN)

        # Рядок 3: відображення числа
        disp=tk.Frame(cf,bg=BG); disp.pack(pady=4)
        self._nl_num_lbl=tk.Label(disp,text="",font=("Courier New",50,"bold"),bg=BG,fg=RED)
        self._nl_num_lbl.pack(side="left",padx=(0,16))
        self._nl_frac_f=tk.Frame(disp,bg=BG); self._nl_frac_f.pack(side="left")

        def _nlscale(sc):
            self._nl_scale=sc
            for b,s in self._nl_scale_btns:
                b.config(bg=ACCENT if s==sc else BTN_NUM,fg=WHITE if s==sc else TEXT)
            _nlredraw()

        def _nlredraw():
            # Оновлюємо лічильники
            self._nl_ones_lbl.config(text=str(self._nl_ones))
            self._nl_tenth_lbl.config(text=str(self._nl_tenths))
            self._nl_hund_lbl.config(text=str(self._nl_hunds))
            self._nl_thous_lbl.config(text=str(self._nl_thous))

            # Значення = сума незалежно від масштабу
            v=round(self._nl_ones + self._nl_tenths*0.1 + self._nl_hunds*0.01 + self._nl_thous*0.001, 3)

            # Крок осі залежить від масштабу
            sc=self._nl_scale
            if sc=="ones":        step=1.0;   places=0
            elif sc=="tenths":    step=0.1;   places=1
            elif sc=="hundredths":step=0.01;  places=2
            else:                 step=0.001; places=3

            s=f"{v:.{places}f}".replace(".",",")
            self._nl_num_lbl.config(text=s)

            # Дріб
            for w in self._nl_frac_f.winfo_children(): w.destroy()
            mul=10**places; nd=int(round(v*mul)); dd=mul
            wp=nd//dd; rp=nd%dd
            tk.Label(self._nl_frac_f,text="=  ",font=F_HEAD,bg=BG,fg=MUTED).pack(side="left")
            if dd==1:
                tk.Label(self._nl_frac_f,text=str(wp),font=F_FRAC,bg=BG,fg=TEXT).pack(side="left")
            elif wp>0 and rp>0:
                tk.Label(self._nl_frac_f,text=str(wp),font=F_FRAC,bg=BG,fg=TEXT).pack(side="left",padx=(0,4))
                frac_w(self._nl_frac_f,rp,dd,BG,"big",ACCENT).pack(side="left")
            elif wp>0:
                tk.Label(self._nl_frac_f,text=str(wp),font=F_FRAC,bg=BG,fg=TEXT).pack(side="left")
            else:
                frac_w(self._nl_frac_f,rp,dd,BG,"big",ACCENT).pack(side="left")

            self._nl_draw_axis(v, step)

            # task check
            if self.nl_task_mode and not self.nl_task_locked:
                tol=step*0.5
                if abs(v-self.nl_task_target)<tol:
                    self.nl_task_locked=True
                    self.nl_task_score+=1; self.nl_task_total+=1
                    self._nl_task_feed_lbl.config(text=f"✅  Правильно! ({s})",fg=GREEN)
                    self._nl_task_score_lbl.config(text=f"Рахунок: {self.nl_task_score}/{self.nl_task_total}")
                    self._nl_task_next_btn.config(state="normal")

        self._nlredraw_fn=_nlredraw
        _nlscale("tenths")

    def _nl_draw_axis(self, point_val, step):
        ax=self._nl_ax; ax.clear()
        # Вікно: показуємо 12 кроків навколо точки, але не менше 0
        span=step*12
        lo=max(0.0, point_val-span/2)
        hi=lo+span
        label_step=step*5

        ax.set_xlim(lo, hi)
        ax.set_ylim(-0.5, 0.7)
        ax.set_yticks([])
        ax.axhline(0, color='#475569', linewidth=2.5, zorder=1)  # ← вісь Y=0
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        # Стрілка вправо
        ax.annotate('', xy=(hi, 0), xytext=(hi-step*0.5, 0),
                    arrowprops=dict(arrowstyle='->', color='#475569', lw=2))

        # Відмітки
        v=lo
        while v<=hi+step*0.01:
            vr=round(v,6)
            is_int=abs(vr-round(vr))<1e-9
            is_label=abs(round(vr/label_step)*label_step - vr)<step*0.01 if label_step>0 else False
            tick_h=0.18 if is_int else (0.12 if is_label else 0.07)
            lw=2.2 if is_int else (1.4 if is_label else 0.7)
            col='#0f172a' if is_int else ('#1d4ed8' if is_label else '#94a3b8')
            ax.plot([vr,vr],[-tick_h,tick_h],color=col,linewidth=lw,solid_capstyle='round',zorder=2)
            if is_int:
                ax.text(vr,-0.30,str(int(round(vr))),ha='center',va='top',
                       fontsize=12,fontweight='bold',color='#0f172a')
            elif is_label:
                places=2 if step<0.05 else 1
                lbl=f"{vr:.{places}f}".replace('.',',')
                ax.text(vr,-0.30,lbl,ha='center',va='top',fontsize=9,color='#1d4ed8')
            v=round(v+step,10)

        # Точка P — на осі (y=0), вертикальна лінія вгору
        places=2 if step<0.05 else 1
        s=f"{point_val:.{places}f}".replace('.',',')
        ax.plot([point_val,point_val],[0,0.42],color='#15803d',linewidth=1.5,linestyle='--',zorder=3)
        ax.plot(point_val, 0, 'o', color='#15803d', markersize=11, zorder=5,
               markeredgecolor='white', markeredgewidth=2)
        ax.text(point_val, 0.46, f"P ({s})", ha='center', va='bottom',
               fontsize=12, fontweight='bold', color='#15803d')

        # Задана точка (режим завдання)
        if self.nl_task_mode and not self.nl_task_locked:
            t=self.nl_task_target
            if lo<=t<=hi:
                ts=f"{t:.{places}f}".replace('.',',')
                ax.plot([t,t],[0,0.42],color='#b91c1c',linewidth=1.5,linestyle=':',zorder=3)
                ax.plot(t, 0, '*', color='#b91c1c', markersize=16, zorder=4,
                       markeredgecolor='white', markeredgewidth=1)
                ax.text(t, 0.46, f"? ({ts})", ha='center', va='bottom',
                       fontsize=11, color='#b91c1c')

        ax.set_facecolor('#f0f4f8')
        self._nl_fig.patch.set_facecolor('#f0f4f8')
        try: self._nl_mpl_canvas.draw()
        except: pass

    def _nl_toggle_task(self):
        self.nl_task_mode=not self.nl_task_mode
        if self.nl_task_mode:
            self._nl_task_btn.config(bg=RED,fg=WHITE,text="⏹  Зупинити")
            self.nl_task_score=0; self.nl_task_total=0
            self._nl_task_frame.pack(fill="x",padx=16,pady=(0,4))
            self._nl_task_score_lbl.config(text="Рахунок: 0/0")
            self._nl_next_task()
        else:
            self._nl_task_btn.config(bg=CARD_Y,fg=ORANGE,text="🎯  Завдання")
            self._nl_task_frame.pack_forget()
            self._nl_task_score_lbl.config(text="")
            self.nl_task_locked=False
            if hasattr(self,"_nlredraw_fn"): self._nlredraw_fn()

    def _nl_next_task(self):
        self.nl_task_locked=False
        sc=self._nl_scale
        if sc=="ones":         target=float(random.randint(1,9))
        elif sc=="tenths":     target=round(random.randint(1,19)/10,1)
        elif sc=="hundredths": target=round(random.randint(1,99)/100,2)
        else:                  target=round(random.randint(1,999)/1000,3)
        self.nl_task_target=target
        places={"ones":0,"tenths":1,"hundredths":2,"thousandths":3}[sc]
        ts=f"{target:.{places}f}".replace(".",",")
        self._nl_task_target_lbl.config(text=f"📋  Постав точку на:  {ts}")
        self._nl_task_feed_lbl.config(text="")
        self._nl_task_next_btn.config(state="disabled")
        if hasattr(self,"_nlredraw_fn"): self._nlredraw_fn()

    # ══ ZEROS DEMO ════════════════════════════════════════════════════════════
    def show_zeros_demo(self):
        self.clear_main(); cf=self.current_frame
        center=tk.Frame(cf,bg=BG); center.pack(expand=True)
        tk.Label(center,text="Зв'язок: знаки після коми ↔ нулі у знаменнику",font=F_TITLE,bg=BG,fg=TEXT).pack(pady=(14,4))
        tk.Label(center,text="Натискай  «+»  і  «−»  щоб змінювати кількість знаків після коми",font=F_BODY,bg=BG,fg=MUTED).pack(pady=(0,12))
        ctrl_row=tk.Frame(center,bg=BG); ctrl_row.pack(pady=8)
        def dec_p():
            if self.zdemo_places>1: self.zdemo_places-=1; _zrefresh()
        def inc_p():
            if self.zdemo_places<5: self.zdemo_places+=1; _zrefresh()
        tk.Button(ctrl_row,text="−  Менше",font=("Segoe UI",17,"bold"),bg=BTN_NUM,fg=TEXT,relief="flat",cursor="hand2",padx=18,pady=7,command=dec_p).pack(side="left",padx=14)
        self._zplbl=tk.Label(ctrl_row,text="",font=("Segoe UI",20,"bold"),bg=BG,fg=ACCENT2,width=18); self._zplbl.pack(side="left")
        tk.Button(ctrl_row,text="+  Більше",font=("Segoe UI",17,"bold"),bg=BTN_NUM,fg=TEXT,relief="flat",cursor="hand2",padx=18,pady=7,command=inc_p).pack(side="left",padx=14)
        vis_f=tk.Frame(center,bg=PANEL,highlightbackground=BORDER,highlightthickness=1,padx=36,pady=24); vis_f.pack(padx=50,pady=12,fill="x")
        self._zdec_f=tk.Frame(vis_f,bg=PANEL); self._zdec_f.pack(pady=(0,6))
        tk.Label(vis_f,text="⟷",font=("Segoe UI",44),bg=PANEL,fg=MUTED).pack()
        self._zfrac_f=tk.Frame(vis_f,bg=PANEL); self._zfrac_f.pack(pady=6)
        self._zexp=tk.Label(vis_f,text="",font=("Segoe UI",17),bg=PANEL,fg=TEXT,justify="center",wraplength=800); self._zexp.pack(pady=6)
        mkbtn(center,"🎲  Нове число",lambda:_zrefresh(True),bg=TEAL,w=13,h=2).pack(pady=6)

        def _zrefresh(new_num=False):
            if new_num or not self._zdemo_digits:
                self._zdemo_digits=[str(random.randint(0,9)) for _ in range(5)]
                if all(d=="0" for d in self._zdemo_digits): self._zdemo_digits[0]=str(random.randint(1,9))
            while len(self._zdemo_digits)<5: self._zdemo_digits.append(str(random.randint(0,9)))
            digits=self._zdemo_digits[:self.zdemo_places]
            dec_str="0,"+"".join(digits)
            suffix={1:"знак",2:"знаки",3:"знаки",4:"знаки"}.get(self.zdemo_places,"знаків")
            self._zplbl.config(text=f"{self.zdemo_places}  {suffix}  після коми")
            for w in self._zdec_f.winfo_children(): w.destroy()
            fn=("Courier New",52,"bold"); ch_w=38; H=84
            all_ch=[(c,TEXT if i<2 else C_DIGIT) for i,c in enumerate("0,"+("".join(digits)))]
            W2=len(all_ch)*ch_w+16
            cv=tk.Canvas(self._zdec_f,bg=PANEL,width=W2,height=H,highlightthickness=0); cv.pack()
            x=8
            for ch,col in all_ch:
                cv.create_text(x+ch_w//2,H//2,text=ch,font=fn,fill=col,anchor="center"); x+=ch_w
            for w in self._zfrac_f.winfo_children(): w.destroy()
            numer=int("".join(digits)); denom=10**self.zdemo_places; denom_str="1"+"0"*self.zdemo_places
            # великий canvas-дріб
            bw=max(len(str(numer)),len(denom_str))*30+24; fH=110
            fcv=tk.Canvas(self._zfrac_f,bg=PANEL,width=bw,height=fH,highlightthickness=0); fcv.pack(side="left")
            fcv.create_text(bw//2,26,text=str(numer),font=("Courier New",36,"bold"),fill=C_DIGIT,anchor="center")
            fcv.create_line(4,52,bw-4,52,fill=ACCENT,width=3)
            fcv.create_text(bw//2,82,text=denom_str,font=("Courier New",36,"bold"),fill=C_ZERO,anchor="center")
            ann=tk.Frame(self._zfrac_f,bg=PANEL); ann.pack(side="left",padx=22)
            s1="цифра" if self.zdemo_places==1 else ("цифри" if self.zdemo_places<5 else "цифр")
            s2="нуль" if self.zdemo_places==1 else ("нулі" if self.zdemo_places<5 else "нулів")
            tk.Label(ann,text=f"← {self.zdemo_places} {s1} після коми",font=("Segoe UI",15,"bold"),bg=PANEL,fg=C_DIGIT).pack(anchor="w")
            tk.Label(ann,text=f"← {self.zdemo_places} {s2} у знаменнику",font=("Segoe UI",15,"bold"),bg=PANEL,fg=C_ZERO).pack(anchor="w")
            pnames={1:"десяті",2:"соті",3:"тисячні",4:"десятитисячні",5:"стотисячні"}
            self._zexp.config(text=f"У числі  {dec_str}  є  {self.zdemo_places} цифр(и) після коми.\nТому у знаменнику «1» та {self.zdemo_places} нул(ів) → {denom_str}.\nЧитаємо: «нуль цілих {numer} {pnames.get(self.zdemo_places,'')}»")
        _zrefresh(True)

    # ══ TRAINER A: decimal → fraction ═════════════════════════════════════════
    def show_trainer_a(self):
        self.clear_main(); cf=self.current_frame
        # Рахунок
        sbar=tk.Frame(cf,bg=PANEL,height=52,highlightbackground=BORDER,highlightthickness=1)
        sbar.pack(fill="x"); sbar.pack_propagate(False)
        self.ta_score_lbl=tk.Label(sbar,text=self._ta_st(),font=F_SCORE,bg=PANEL,fg=GREEN)
        self.ta_score_lbl.pack(side="left",padx=24)
        tk.Label(sbar,text="Десятковий → Звичайний дріб",font=("Segoe UI",14,"bold"),bg=PANEL,fg=MUTED).pack(side="left",padx=8)
        tk.Label(sbar,text="Цифри після коми = чисельник.  Кількість цифр → кількість нулів у знаменнику.",
                 font=("Segoe UI",12),bg=PANEL,fg=ACCENT).pack(side="right",padx=18)

        # Ліво: завдання + введення | Право: нумпад
        body=tk.Frame(cf,bg=BG); body.pack(fill="both",expand=True,padx=20,pady=12)
        left=tk.Frame(body,bg=BG); left.pack(side="left",fill="both",expand=True)
        right=tk.Frame(body,bg=BG,width=230); right.pack(side="right",fill="y",padx=(14,0)); right.pack_propagate(False)

        # ── Завдання
        tf=tk.Frame(left,bg=PANEL,highlightbackground=BORDER,highlightthickness=2,padx=28,pady=18)
        tf.pack(fill="x",pady=(0,10))
        tk.Label(tf,text="Запиши як звичайний дріб:",font=F_SUB,bg=PANEL,fg=TEXT).pack(anchor="w")
        self.ta_task_lbl=tk.Label(tf,text="",font=("Courier New",72,"bold"),bg=PANEL,fg=RED)
        self.ta_task_lbl.pack(pady=6)
        self.ta_hint_lbl=tk.Label(tf,text="",font=("Segoe UI",14),bg=PANEL,fg=MUTED)
        self.ta_hint_lbl.pack()

        # ── Крок 1: чисельник
        step1_f=tk.Frame(left,bg=CARD_B,padx=20,pady=14,highlightbackground=ACCENT,highlightthickness=2)
        step1_f.pack(fill="x",pady=(0,6))
        step1_hdr=tk.Frame(step1_f,bg=CARD_B); step1_hdr.pack(fill="x")
        self.ta_s1_lbl=tk.Label(step1_hdr,text="Крок 1  —  Чисельник",font=("Segoe UI",16,"bold"),bg=CARD_B,fg=ACCENT)
        self.ta_s1_lbl.pack(side="left")
        self.ta_s1_ok=tk.Label(step1_hdr,text="",font=("Segoe UI",14,"bold"),bg=CARD_B,fg=GREEN)
        self.ta_s1_ok.pack(side="left",padx=12)
        s1_inp=tk.Frame(step1_f,bg=CARD_B); s1_inp.pack(anchor="w",pady=(6,0))
        tk.Label(s1_inp,text="=",font=("Courier New",42,"bold"),bg=CARD_B,fg=MUTED).pack(side="left",padx=(0,8))
        self.ta_n_lbl=tk.Label(s1_inp,text="",font=("Courier New",52,"bold"),bg=CARD_B,fg=ACCENT,width=7,anchor="w")
        self.ta_n_lbl.pack(side="left")
        self.ta_n_cur=tk.Label(s1_inp,text="▮",font=("Courier New",52,"bold"),bg=CARD_B,fg=ACCENT2)
        self.ta_n_cur.pack(side="left")
        tk.Label(s1_inp,text="/",font=("Courier New",52,"bold"),bg=CARD_B,fg=MUTED).pack(side="left",padx=6)
        tk.Label(s1_inp,text="?",font=("Courier New",52,"bold"),bg=CARD_B,fg=MUTED).pack(side="left")

        # ── Крок 2: знаменник
        step2_f=tk.Frame(left,bg=BTN_NUM,padx=20,pady=14,highlightbackground=BORDER,highlightthickness=1)
        step2_f.pack(fill="x",pady=(0,6))
        self.ta_step2_f=step2_f
        step2_hdr=tk.Frame(step2_f,bg=BTN_NUM); step2_hdr.pack(fill="x")
        self.ta_s2_lbl=tk.Label(step2_hdr,text="Крок 2  —  Знаменник",font=("Segoe UI",16,"bold"),bg=BTN_NUM,fg=MUTED)
        self.ta_s2_lbl.pack(side="left")
        s2_inp=tk.Frame(step2_f,bg=BTN_NUM); s2_inp.pack(anchor="w",pady=(6,0))
        self.ta_numer_done=tk.Label(s2_inp,text="",font=("Courier New",52,"bold"),bg=BTN_NUM,fg=ACCENT,width=7,anchor="w")
        self.ta_numer_done.pack(side="left")
        tk.Label(s2_inp,text="/",font=("Courier New",52,"bold"),bg=BTN_NUM,fg=MUTED).pack(side="left",padx=6)
        self.ta_d_lbl=tk.Label(s2_inp,text="",font=("Courier New",52,"bold"),bg=BTN_NUM,fg=GREEN,width=7,anchor="w")
        self.ta_d_lbl.pack(side="left")
        self.ta_d_cur=tk.Label(s2_inp,text="",font=("Courier New",52,"bold"),bg=BTN_NUM,fg=ACCENT2)
        self.ta_d_cur.pack(side="left")

        self.ta_feed=tk.Label(left,text="",font=("Segoe UI",15),bg=BG,fg=ORANGE,wraplength=620,justify="center")
        self.ta_feed.pack(pady=4)

        # ── Результат (великий дріб після правильної відповіді)
        self._ta_result_frame=tk.Frame(left,bg=BG); self._ta_result_frame.pack(pady=4)

        # ── Кнопки
        act=tk.Frame(left,bg=BG); act.pack(pady=6)
        self.ta_check=mkbtn(act,"✔  Перевірити",self._ta_check,bg=GREEN,w=13,h=2)
        self.ta_check.pack(side="left",padx=8)
        mkbtn(act,"▶  Наступне",self._ta_new,bg=ACCENT,w=11,h=2).pack(side="left",padx=8)

        # ── Нумпад
        tk.Label(right,text="Клавіатура",font=("Segoe UI",13,"bold"),bg=BG,fg=MUTED).pack(pady=(8,4))
        build_numpad(right,self._ta_key,bg=BG).pack()

        self._ta_new()

    def _ta_st(self): return f"Правильно: {self.ta_score}  /  Завдань: {self.ta_att}"

    def _ta_new(self):
        # Складність від простого до складного залежно від рахунку
        max_places = 1 + min(3, self.ta_score//3)
        places=random.randint(1,max_places)
        denom=10**places; numer=random.randint(1,denom-1)
        val=numer/denom; dec=f"{val:.{places}f}".replace(".",",")
        self.ta_dec=dec; self.ta_n=numer; self.ta_d=denom
        self.ta_inp_n=""; self.ta_inp_d=""; self.ta_active="n"; self.ta_n_done=False; self.ta_att+=1
        after=places

        self.ta_task_lbl.config(text=dec)
        self.ta_hint_lbl.config(text=f"Після коми {after} цифр → знаменник = 1{'0'*after}")
        self.ta_s1_lbl.config(text="Крок 1  —  Чисельник",fg=ACCENT,bg=CARD_B)
        self.ta_s1_ok.config(text="",bg=CARD_B)
        self.ta_n_lbl.config(text="",fg=ACCENT,bg=CARD_B)
        self.ta_n_cur.config(text="▮",bg=CARD_B)
        self.ta_step2_f.config(bg=BTN_NUM,highlightbackground=BORDER,highlightthickness=1)
        self.ta_s2_lbl.config(text="Крок 2  —  Знаменник",fg=MUTED,bg=BTN_NUM)
        self.ta_numer_done.config(text="",bg=BTN_NUM)
        self.ta_d_lbl.config(text="",bg=BTN_NUM)
        self.ta_d_cur.config(text="",bg=BTN_NUM)
        self.ta_feed.config(text="")
        self.ta_check.config(state="normal",bg=GREEN)
        for w in self._ta_result_frame.winfo_children(): w.destroy()
        self.ta_score_lbl.config(text=self._ta_st())

    def _ta_key(self,ch):
        if ch.isdigit():
            if self.ta_active=="n" and len(self.ta_inp_n)<6:
                self.ta_inp_n+=ch; self.ta_n_lbl.config(text=self.ta_inp_n)
            elif self.ta_active=="d" and len(self.ta_inp_d)<8:
                self.ta_inp_d+=ch; self.ta_d_lbl.config(text=self.ta_inp_d)
        elif ch=="⌫":
            if self.ta_active=="n": self.ta_inp_n=self.ta_inp_n[:-1]; self.ta_n_lbl.config(text=self.ta_inp_n)
            else: self.ta_inp_d=self.ta_inp_d[:-1]; self.ta_d_lbl.config(text=self.ta_inp_d)
        elif ch=="C":
            if self.ta_active=="n": self.ta_inp_n=""; self.ta_n_lbl.config(text="")
            else: self.ta_inp_d=""; self.ta_d_lbl.config(text="")

    def _ta_check(self):
        if self.ta_active=="n":
            if not self.ta_inp_n:
                self.ta_feed.config(text="⚠️  Введи чисельник!",fg=ORANGE); return
            val=int(self.ta_inp_n)
            if val==self.ta_n:
                # Крок 1 ✓ → переходимо до кроку 2
                after=len(self.ta_dec.split(",")[1])
                self.ta_n_cur.config(text="")
                self.ta_s1_ok.config(text=f"✓ = {val}",fg=GREEN,bg=CARD_B)
                self.ta_active="d"; self.ta_n_done=True
                # Активуємо крок 2
                self.ta_step2_f.config(bg=CARD_G,highlightbackground=GREEN,highlightthickness=2)
                self.ta_s2_lbl.config(text="Крок 2  —  Знаменник",fg=GREEN,bg=CARD_G)
                self.ta_numer_done.config(text=str(val),bg=CARD_G)
                self.ta_d_lbl.config(bg=CARD_G); self.ta_d_cur.config(text="▮",bg=CARD_G)
                self.ta_feed.config(text=f"✅ Чисельник {val}!  Тепер знаменник: 1 і {after} нулів",fg=GREEN)
            else:
                self.ta_feed.config(text=f"❌  Чисельник ≠ {val}.  Цифри після коми без змін = чисельник.",fg=RED)
        else:
            if not self.ta_inp_d:
                self.ta_feed.config(text="⚠️  Введи знаменник!",fg=ORANGE); return
            val=int(self.ta_inp_d)
            if val==self.ta_d:
                self.ta_score+=1; self.ta_att
                self.ta_d_cur.config(text="")
                self.ta_check.config(state="disabled",bg=BTN_NUM)
                self.ta_feed.config(text="",fg=GREEN)
                self._ta_show_result()
            else:
                places=len(self.ta_dec.split(",")[1])
                self.ta_feed.config(text=f"❌  Знаменник ≠ {val}.  {places} цифр → знаменник = 1{'0'*places}",fg=RED)
        self.ta_score_lbl.config(text=self._ta_st())

    def _ta_show_result(self):
        for w in self._ta_result_frame.winfo_children(): w.destroy()
        outer=tk.Frame(self._ta_result_frame,bg=GREEN_LT,
                       highlightbackground=GREEN,highlightthickness=3,padx=24,pady=14)
        outer.pack()
        tk.Label(outer,text="🎉  Правильно!",font=("Segoe UI",18,"bold"),bg=GREEN_LT,fg=GREEN).pack()
        # Рядок: dec = ціла (якщо є) + дріб
        eq_row=tk.Frame(outer,bg=GREEN_LT); eq_row.pack(pady=8)
        tk.Label(eq_row,text=f"{self.ta_dec}",font=("Courier New",48,"bold"),bg=GREEN_LT,fg=RED).pack(side="left",padx=(0,12))
        tk.Label(eq_row,text="=",font=("Courier New",48,"bold"),bg=GREEN_LT,fg=MUTED).pack(side="left",padx=(0,12))
        whole=self.ta_n//self.ta_d; fn=self.ta_n%self.ta_d
        if whole>0:
            tk.Label(eq_row,text=str(whole),font=("Courier New",56,"bold"),bg=GREEN_LT,fg=TEXT).pack(side="left",padx=(0,8))
        ns=str(fn if whole>0 else self.ta_n); ds=str(self.ta_d)
        bw=max(len(ns),len(ds))*40+24; fH=140
        cv=tk.Canvas(eq_row,bg=GREEN_LT,width=bw,height=fH,highlightthickness=0); cv.pack(side="left")
        cv.create_text(bw//2,30,text=ns,font=("Courier New",50,"bold"),fill=ACCENT,anchor="center")
        cv.create_line(4,62,bw-4,62,fill=ACCENT,width=4)
        cv.create_text(bw//2,100,text=ds,font=("Courier New",50,"bold"),fill=GREEN,anchor="center")

    # ══ TRAINER B: fraction → decimal ═════════════════════════════════════════
    def show_trainer_b(self):
        self.clear_main(); cf=self.current_frame
        sbar=tk.Frame(cf,bg=PANEL,height=52,highlightbackground=BORDER,highlightthickness=1)
        sbar.pack(fill="x"); sbar.pack_propagate(False)
        self.tb_score_lbl=tk.Label(sbar,text=self._tb_st(),font=F_SCORE,bg=PANEL,fg=GREEN)
        self.tb_score_lbl.pack(side="left",padx=24)
        tk.Label(sbar,text="Звичайний → Десятковий дріб",font=("Segoe UI",14,"bold"),bg=PANEL,fg=MUTED).pack(side="left",padx=8)
        tk.Label(sbar,text="Нулів у знаменнику = цифр після коми",font=("Segoe UI",12),bg=PANEL,fg=ACCENT2).pack(side="right",padx=18)

        body=tk.Frame(cf,bg=BG); body.pack(fill="both",expand=True,padx=20,pady=12)
        left=tk.Frame(body,bg=BG); left.pack(side="left",fill="both",expand=True)
        right=tk.Frame(body,bg=BG,width=230); right.pack(side="right",fill="y",padx=(14,0)); right.pack_propagate(False)

        # ── Завдання: великий дріб canvas
        tf=tk.Frame(left,bg=PANEL,highlightbackground=BORDER,highlightthickness=2,padx=28,pady=18)
        tf.pack(fill="x",pady=(0,10))
        tk.Label(tf,text="Запиши як десятковий дріб:",font=F_SUB,bg=PANEL,fg=TEXT).pack(anchor="w")
        task_row=tk.Frame(tf,bg=PANEL); task_row.pack(anchor="w",pady=8)
        self.tb_task_f=tk.Frame(task_row,bg=PANEL); self.tb_task_f.pack(side="left",padx=(0,32))
        self.tb_hint=tk.Label(task_row,text="",font=("Segoe UI",15),bg=PANEL,fg=MUTED,justify="left")
        self.tb_hint.pack(side="left",anchor="center")

        # ── Введення: учень вводить ВСЕ — ціла + кома + дробова
        inp_f=tk.Frame(left,bg=CARD_V,padx=20,pady=14,highlightbackground=ACCENT2,highlightthickness=2)
        inp_f.pack(fill="x",pady=(0,8))
        tk.Label(inp_f,text="Твоя відповідь:",font=("Segoe UI",14,"bold"),bg=CARD_V,fg=ACCENT2).pack(anchor="w",pady=(0,6))
        inp_row=tk.Frame(inp_f,bg=CARD_V); inp_row.pack(anchor="w")
        self.tb_whole_lbl=tk.Label(inp_row,text="",font=("Courier New",56,"bold"),bg=CARD_V,fg=TEXT,width=3,anchor="e")
        self.tb_whole_lbl.pack(side="left")
        self.tb_comma_lbl=tk.Label(inp_row,text="",font=("Courier New",56,"bold"),bg=CARD_V,fg=MUTED)
        self.tb_comma_lbl.pack(side="left")
        self.tb_frac_lbl=tk.Label(inp_row,text="",font=("Courier New",56,"bold"),bg=CARD_V,fg=RED,width=5,anchor="w")
        self.tb_frac_lbl.pack(side="left")
        self.tb_cursor_lbl=tk.Label(inp_row,text="▮",font=("Courier New",56,"bold"),bg=CARD_V,fg=ACCENT2)
        self.tb_cursor_lbl.pack(side="left")
        self.tb_slots_lbl=tk.Label(inp_f,text="",font=("Segoe UI",13),bg=CARD_V,fg=MUTED)
        self.tb_slots_lbl.pack(anchor="w",pady=(4,0))
        self.tb_comma_btn=tk.Button(inp_f,text=",  Поставити кому →",
            font=("Segoe UI",13,"bold"),bg=ACCENT2,fg=WHITE,relief="flat",cursor="hand2",
            padx=14,pady=6,command=self._tb_enter_comma)
        self.tb_comma_btn.pack(anchor="w",pady=(8,0))

        self.tb_feed=tk.Label(left,text="",font=("Segoe UI",15),bg=BG,fg=ORANGE,wraplength=640,justify="center")
        self.tb_feed.pack(pady=4)
        self._tb_result_frame=tk.Frame(left,bg=BG); self._tb_result_frame.pack(pady=4)

        act=tk.Frame(left,bg=BG); act.pack(pady=6)
        self.tb_check=mkbtn(act,"✔  Перевірити",self._tb_check,bg=GREEN,w=13,h=2)
        self.tb_check.pack(side="left",padx=8)
        mkbtn(act,"▶  Наступне",self._tb_new,bg=ACCENT2,w=11,h=2).pack(side="left",padx=8)

        tk.Label(right,text="Клавіатура",font=("Segoe UI",13,"bold"),bg=BG,fg=MUTED).pack(pady=(8,4))
        build_numpad(right,self._tb_key,bg=BG).pack()
        self._tb_new()

    def _tb_st(self): return f"Правильно: {self.tb_score}  /  Завдань: {self.tb_att}"

    def _tb_new(self):
        max_places=1+min(3,self.tb_score//3)
        task_type=random.choices(["pure","mixed","mixed"],[1,3,3])[0]
        if task_type=="pure":
            places=random.randint(1,min(max_places,3)); denom=10**places
            numer=random.randint(1,denom-1); whole=0
        else:
            places=random.randint(1,min(max_places,3)); denom=10**places
            whole=random.randint(1,9); numer=whole*denom+random.randint(1,denom-1)
        val=numer/denom; whole=int(val)
        frac_str=f"{round(val-whole,places):.{places}f}".split(".")[1]
        self.tb_n=numer; self.tb_d=denom; self.tb_whole=whole
        self.tb_ans=frac_str; self.tb_dec_places=places
        self.tb_whole_inp=""; self.tb_frac_inp=""; self._tb_phase="whole"; self.tb_att+=1
        # Дріб canvas
        for w in self.tb_task_f.winfo_children(): w.destroy()
        ns=str(numer); ds=str(denom)
        bw=max(len(ns),len(ds))*38+24; fH=130
        cv=tk.Canvas(self.tb_task_f,bg=PANEL,width=bw,height=fH,highlightthickness=0); cv.pack()
        cv.create_text(bw//2,28,text=ns,font=("Courier New",46,"bold"),fill=C_DIGIT,anchor="center")
        cv.create_line(4,60,bw-4,60,fill=ACCENT2,width=4)
        cv.create_text(bw//2,94,text=ds,font=("Courier New",46,"bold"),fill=C_ZERO,anchor="center")
        z=places; s2="нуль" if z==1 else("нулі" if z<5 else"нулів")
        hint=f"Знаменник {denom}:\n→ {z} {s2} → {z} цифр після коми"
        if whole>0: hint+=f"\n→ Ціла частина: {whole}"
        self.tb_hint.config(text=hint)
        self.tb_whole_lbl.config(text="",fg=TEXT)
        self.tb_comma_lbl.config(text="")
        self.tb_frac_lbl.config(text="",fg=RED)
        self.tb_cursor_lbl.config(text="▮",fg=ACCENT2)
        self.tb_comma_btn.config(state="normal",bg=ACCENT2)
        self.tb_slots_lbl.config(text="Крок 1: введи цілу частину, потім натисни «,»")
        self.tb_feed.config(text="")
        self.tb_check.config(state="normal",bg=GREEN)
        for w in self._tb_result_frame.winfo_children(): w.destroy()
        self.tb_score_lbl.config(text=self._tb_st())

    def _tb_key(self,ch):
        if ch.isdigit():
            if self._tb_phase=="whole":
                if len(self.tb_whole_inp)<2:
                    self.tb_whole_inp+=ch; self.tb_whole_lbl.config(text=self.tb_whole_inp)
            else:
                if len(self.tb_frac_inp)<self.tb_dec_places:
                    self.tb_frac_inp+=ch; self.tb_frac_lbl.config(text=self.tb_frac_inp)
                    if len(self.tb_frac_inp)==self.tb_dec_places:
                        self.tb_cursor_lbl.config(text="")
        elif ch=="⌫":
            if self._tb_phase=="frac" and self.tb_frac_inp:
                self.tb_frac_inp=self.tb_frac_inp[:-1]
                self.tb_frac_lbl.config(text=self.tb_frac_inp)
                self.tb_cursor_lbl.config(text="▮")
            elif self._tb_phase=="frac":
                # повертаємось до цілої
                self._tb_phase="whole"; self.tb_comma_lbl.config(text="")
                self.tb_comma_btn.config(state="normal",bg=ACCENT2)
                self.tb_cursor_lbl.config(text="▮",fg=ACCENT2)
                self.tb_slots_lbl.config(text="Крок 1: введи цілу частину")
            elif self._tb_phase=="whole" and self.tb_whole_inp:
                self.tb_whole_inp=self.tb_whole_inp[:-1]
                self.tb_whole_lbl.config(text=self.tb_whole_inp)
        elif ch=="C":
            self.tb_whole_inp=""; self.tb_frac_inp=""; self._tb_phase="whole"
            self.tb_whole_lbl.config(text=""); self.tb_comma_lbl.config(text="")
            self.tb_frac_lbl.config(text=""); self.tb_cursor_lbl.config(text="▮",fg=ACCENT2)
            self.tb_comma_btn.config(state="normal",bg=ACCENT2)

    def _tb_enter_comma(self):
        if not self.tb_whole_inp:
            self.tb_feed.config(text="⚠️  Спочатку введи цілу частину!",fg=ORANGE); return
        self._tb_phase="frac"; self.tb_comma_lbl.config(text=",")
        self.tb_cursor_lbl.config(text="▮",fg=RED)
        self.tb_comma_btn.config(state="disabled",bg=BTN_NUM)
        self.tb_slots_lbl.config(text=f"Крок 2: введи {self.tb_dec_places} цифр після коми")
        self.tb_feed.config(text="")

    def _tb_confirm_whole(self): pass

    def _tb_check(self):
        if self._tb_phase=="whole":
            self.tb_feed.config(text="⚠️  Спочатку введи цілу частину і натисни «,»",fg=ORANGE); return
        if not self.tb_frac_inp:
            self.tb_feed.config(text="⚠️  Введи цифри після коми!",fg=ORANGE); return
        whole_ok=self.tb_whole_inp==str(self.tb_whole)
        frac_ok=self.tb_frac_inp.zfill(self.tb_dec_places)==self.tb_ans
        if whole_ok and frac_ok:
            self.tb_score+=1; self.tb_check.config(state="disabled",bg=BTN_NUM)
            self.tb_frac_lbl.config(fg=GREEN); self.tb_whole_lbl.config(fg=GREEN)
            self.tb_cursor_lbl.config(text=""); self.tb_feed.config(text="")
            self._tb_show_result()
        elif not whole_ok:
            self.tb_feed.config(text=f"❌  Ціла частина ≠ {self.tb_whole_inp}.  Ціла = {self.tb_whole}",fg=RED)
        else:
            self.tb_feed.config(text=f"❌  Дробова частина не вірна.  Правильно: «{self.tb_whole},{self.tb_ans}»",fg=RED)
        self.tb_score_lbl.config(text=self._tb_st())

    def _tb_show_result(self):
        for w in self._tb_result_frame.winfo_children(): w.destroy()
        outer=tk.Frame(self._tb_result_frame,bg=GREEN_LT,
                       highlightbackground=GREEN,highlightthickness=3,padx=24,pady=14)
        outer.pack()
        tk.Label(outer,text="🎉  Правильно!",font=("Segoe UI",18,"bold"),bg=GREEN_LT,fg=GREEN).pack()
        eq_row=tk.Frame(outer,bg=GREEN_LT); eq_row.pack(pady=8)
        ns=str(self.tb_n); ds=str(self.tb_d)
        bw=max(len(ns),len(ds))*32+20; fH=120
        cv=tk.Canvas(eq_row,bg=GREEN_LT,width=bw,height=fH,highlightthickness=0); cv.pack(side="left",padx=(0,12))
        cv.create_text(bw//2,24,text=ns,font=("Courier New",40,"bold"),fill=C_DIGIT,anchor="center")
        cv.create_line(4,50,bw-4,50,fill=ACCENT2,width=3)
        cv.create_text(bw//2,80,text=ds,font=("Courier New",40,"bold"),fill=C_ZERO,anchor="center")
        tk.Label(eq_row,text="=",font=("Courier New",48,"bold"),bg=GREEN_LT,fg=MUTED).pack(side="left",padx=8)
        tk.Label(eq_row,text=f"{self.tb_whole},{self.tb_ans}",
                 font=("Courier New",56,"bold"),bg=GREEN_LT,fg=RED).pack(side="left")

    # ══ TRAINER C: привести до знаменника ═════════════════════════════════════
    def show_trainer_c(self):
        self.clear_main(); cf=self.current_frame
        sbar=tk.Frame(cf,bg=PANEL,height=52,highlightbackground=BORDER,highlightthickness=1)
        sbar.pack(fill="x"); sbar.pack_propagate(False)
        self.tc_score_lbl=tk.Label(sbar,text=self._tc_st(),font=F_SCORE,bg=PANEL,fg=GREEN)
        self.tc_score_lbl.pack(side="left",padx=24)
        tk.Label(sbar,text="Точність запису десяткового дробу",font=("Segoe UI",14,"bold"),bg=PANEL,fg=MUTED).pack(side="left",padx=8)

        main=tk.Frame(cf,bg=BG); main.pack(fill="both",expand=True,padx=16,pady=12)
        left=tk.Frame(main,bg=BG); left.pack(side="left",fill="both",expand=True)
        right=tk.Frame(main,bg=BG,width=260); right.pack(side="right",fill="y",padx=(12,0)); right.pack_propagate(False)

        # ── правило-підказка
        rule_f=tk.Frame(left,bg=CARD_B,padx=16,pady=10,highlightbackground=ACCENT,highlightthickness=1)
        rule_f.pack(fill="x",pady=(0,8))
        tk.Label(rule_f,text="📌  Запиши число, додаючи нулі в кінці, щоб отримати потрібну кількість знаків після коми.\nПриклад: 3,7 → до тисячних (3 знаки) → 3,700",
                 font=("Segoe UI",13,"bold"),bg=CARD_B,fg=ACCENT,justify="left",wraplength=700).pack(anchor="w")

        # ── завдання
        task_f=tk.Frame(left,bg=PANEL,highlightbackground=BORDER,highlightthickness=1,padx=24,pady=16)
        task_f.pack(fill="x",pady=(0,8))
        tk.Label(task_f,text="Запиши число з точністю до:",font=F_SUB,bg=PANEL,fg=TEXT).pack(anchor="w")
        task_row=tk.Frame(task_f,bg=PANEL); task_row.pack(anchor="w",pady=8)
        self.tc_num_lbl=tk.Label(task_row,text="",font=("Courier New",60,"bold"),bg=PANEL,fg=RED,width=8)
        self.tc_num_lbl.pack(side="left",padx=(0,24))
        tc_target_f=tk.Frame(task_row,bg=PANEL); tc_target_f.pack(side="left")
        tk.Label(tc_target_f,text="Знаменник:",font=("Segoe UI",16),bg=PANEL,fg=MUTED).pack(anchor="w")
        self.tc_target_lbl=tk.Label(tc_target_f,text="",font=("Courier New",52,"bold"),bg=PANEL,fg=C_ZERO)
        self.tc_target_lbl.pack(anchor="w")
        self.tc_name_lbl=tk.Label(tc_target_f,text="",font=("Segoe UI",14),bg=PANEL,fg=MUTED)
        self.tc_name_lbl.pack(anchor="w")

        # ── введення: учень вводить ВСЕ — ціла + кома + дробова
        inp_f=tk.Frame(left,bg=CARD_G,padx=16,pady=10,highlightbackground=GREEN,highlightthickness=2)
        inp_f.pack(fill="x",pady=(0,6))
        tk.Label(inp_f,text="Результат (десятковий дріб):",font=("Segoe UI",14,"bold"),bg=CARD_G,fg=GREEN).pack(anchor="w",pady=(0,6))
        inp_row=tk.Frame(inp_f,bg=CARD_G); inp_row.pack(anchor="w")
        self.tc_whole_lbl=tk.Label(inp_row,text="",font=("Courier New",48,"bold"),bg=CARD_G,fg=TEXT,width=3,anchor="e")
        self.tc_whole_lbl.pack(side="left")
        self.tc_comma_lbl=tk.Label(inp_row,text="",font=("Courier New",48,"bold"),bg=CARD_G,fg=MUTED)
        self.tc_comma_lbl.pack(side="left")
        self.tc_inp_lbl=tk.Label(inp_row,text="",font=("Courier New",48,"bold"),bg=CARD_G,fg=RED,width=6,anchor="w")
        self.tc_inp_lbl.pack(side="left")
        self.tc_cursor_lbl=tk.Label(inp_row,text="▮",font=("Courier New",48,"bold"),bg=CARD_G,fg=GREEN)
        self.tc_cursor_lbl.pack(side="left")
        self.tc_comma_btn=tk.Button(inp_f,text=",  Поставити кому →",
            font=("Segoe UI",13,"bold"),bg=GREEN,fg=WHITE,relief="flat",cursor="hand2",
            padx=14,pady=6,command=self._tc_enter_comma)
        self.tc_comma_btn.pack(anchor="w",pady=(8,0))
        self.tc_slots_lbl=tk.Label(inp_f,text="",font=("Segoe UI",13),bg=CARD_G,fg=MUTED)
        self.tc_slots_lbl.pack(anchor="w",pady=(4,0))

        self.tc_feed=tk.Label(left,text="",font=("Segoe UI",15),bg=BG,fg=ORANGE,wraplength=620,justify="center")
        self.tc_feed.pack(pady=4)

        act=tk.Frame(left,bg=BG); act.pack(pady=6)
        self.tc_check_btn=mkbtn(act,"✔  Перевірити",self._tc_check,bg=GREEN,w=13,h=2)
        self.tc_check_btn.pack(side="left",padx=8)
        mkbtn(act,"▶  Наступне",self._tc_new,bg=ACCENT,w=11,h=2).pack(side="left",padx=8)

        tk.Label(right,text="Клавіатура",font=("Segoe UI",14,"bold"),bg=BG,fg=MUTED).pack(pady=(8,4))
        build_numpad(right,self._tc_key,bg=BG).pack()

        self._tc_inp=""; self._tc_new()

    def _tc_st(self): return f"Правильно: {self.tc_score}  /  Завдань: {self.tc_att}"

    def _tc_new(self):
        max_places=1+min(3,self.tc_score//3)
        src_places=random.choice([1]*(3-min(2,self.tc_score//5)) + [2,3])
        src_places=min(src_places,max_places)
        extra=random.choice([0,1,2,3]); target_places=src_places+extra
        denom_target=10**target_places
        src_denom=10**src_places; numer=random.randint(1,src_denom-1)
        whole=random.randint(0,5)
        val=whole+numer/src_denom
        self._tc_val=round(val,src_places)
        self._tc_target_places=target_places
        self._tc_whole=whole
        ans_str=f"{val:.{target_places}f}".split(".")[1]
        self._tc_ans=ans_str
        self._tc_inp=""; self._tc_whole_inp=""; self._tc_phase="whole"; self.tc_att+=1
        src_str=f"{val:.{src_places}f}".replace(".",",")
        names={10:"десяті",100:"соті",1000:"тисячні",10000:"десятитисячні"}
        pname=names.get(denom_target,f"{target_places} знаків")
        if self.tc_num_lbl: self.tc_num_lbl.config(text=src_str)
        if self.tc_target_lbl: self.tc_target_lbl.config(text=str(denom_target))
        if self.tc_name_lbl: self.tc_name_lbl.config(text=f"({pname}, {target_places} знаків після коми)")
        if self.tc_whole_lbl: self.tc_whole_lbl.config(text="",fg=TEXT)
        if self.tc_comma_lbl: self.tc_comma_lbl.config(text="")
        if self.tc_inp_lbl: self.tc_inp_lbl.config(text="",fg=RED)
        if self.tc_cursor_lbl: self.tc_cursor_lbl.config(text="▮",fg=GREEN)
        if self.tc_comma_btn: self.tc_comma_btn.config(state="normal",bg=GREEN)
        if self.tc_slots_lbl: self.tc_slots_lbl.config(text="Крок 1: введи цілу частину, потім натисни «,»")
        if self.tc_feed: self.tc_feed.config(text="")
        if self.tc_check_btn: self.tc_check_btn.config(state="normal",bg=GREEN)
        if self.tc_score_lbl: self.tc_score_lbl.config(text=self._tc_st())

    def _tc_enter_comma(self):
        if not self._tc_whole_inp:
            if self.tc_feed: self.tc_feed.config(text="⚠️  Введи цілу частину!",fg=ORANGE); return
        self._tc_phase="frac"
        if self.tc_comma_lbl: self.tc_comma_lbl.config(text=",")
        if self.tc_cursor_lbl: self.tc_cursor_lbl.config(text="▮",fg=RED)
        if self.tc_comma_btn: self.tc_comma_btn.config(state="disabled",bg=BTN_NUM)
        if self.tc_slots_lbl: self.tc_slots_lbl.config(text=f"Крок 2: введи {self._tc_target_places} цифр після коми")
        if self.tc_feed: self.tc_feed.config(text="")

    def _tc_key(self,ch):
        p=self._tc_target_places
        if ch.isdigit():
            if self._tc_phase=="whole":
                if len(self._tc_whole_inp)<2:
                    self._tc_whole_inp+=ch
                    if self.tc_whole_lbl: self.tc_whole_lbl.config(text=self._tc_whole_inp)
            else:
                if len(self._tc_inp)<p:
                    self._tc_inp+=ch
                    if self.tc_inp_lbl: self.tc_inp_lbl.config(text=self._tc_inp)
                    if len(self._tc_inp)==p:
                        if self.tc_cursor_lbl: self.tc_cursor_lbl.config(text="")
        elif ch=="⌫":
            if self._tc_phase=="frac" and self._tc_inp:
                self._tc_inp=self._tc_inp[:-1]
                if self.tc_inp_lbl: self.tc_inp_lbl.config(text=self._tc_inp)
                if self.tc_cursor_lbl: self.tc_cursor_lbl.config(text="▮")
            elif self._tc_phase=="frac":
                self._tc_phase="whole"
                if self.tc_comma_lbl: self.tc_comma_lbl.config(text="")
                if self.tc_comma_btn: self.tc_comma_btn.config(state="normal",bg=GREEN)
                if self.tc_cursor_lbl: self.tc_cursor_lbl.config(text="▮",fg=GREEN)
            elif self._tc_whole_inp:
                self._tc_whole_inp=self._tc_whole_inp[:-1]
                if self.tc_whole_lbl: self.tc_whole_lbl.config(text=self._tc_whole_inp)
        elif ch=="C":
            self._tc_inp=""; self._tc_whole_inp=""; self._tc_phase="whole"
            if self.tc_whole_lbl: self.tc_whole_lbl.config(text="")
            if self.tc_comma_lbl: self.tc_comma_lbl.config(text="")
            if self.tc_inp_lbl: self.tc_inp_lbl.config(text="")
            if self.tc_cursor_lbl: self.tc_cursor_lbl.config(text="▮",fg=GREEN)
            if self.tc_comma_btn: self.tc_comma_btn.config(state="normal",bg=GREEN)

    def _tc_check(self):
        if self._tc_phase=="whole":
            if self.tc_feed: self.tc_feed.config(text="⚠️  Введи цілу частину і натисни «,»",fg=ORANGE); return
        if not self._tc_inp:
            if self.tc_feed: self.tc_feed.config(text="⚠️  Введіть відповідь!",fg=ORANGE); return
        padded=self._tc_inp.zfill(self._tc_target_places)
        whole_ok=self._tc_whole_inp==str(self._tc_whole)
        frac_ok=padded==self._tc_ans
        if whole_ok and frac_ok:
            self.tc_score+=1
            if self.tc_check_btn: self.tc_check_btn.config(state="disabled",bg=BTN_NUM)
            if self.tc_inp_lbl: self.tc_inp_lbl.config(fg=GREEN)
            if self.tc_whole_lbl: self.tc_whole_lbl.config(fg=GREEN)
            if self.tc_cursor_lbl: self.tc_cursor_lbl.config(text="")
            res=f"{self._tc_whole},{self._tc_ans}"
            if self.tc_feed: self.tc_feed.config(text=f"🎉  Правильно!  {res}  (дописали нулі в кінці)",fg=GREEN)
        elif not whole_ok:
            if self.tc_feed: self.tc_feed.config(text=f"❌  Ціла частина ≠ {self._tc_whole_inp}.  Ціла = {self._tc_whole}",fg=RED)
        else:
            if self.tc_feed: self.tc_feed.config(text=f"❌  Не вірно.  Правильно: «{self._tc_whole},{self._tc_ans}»",fg=RED)
        if self.tc_score_lbl: self.tc_score_lbl.config(text=self._tc_st())



    # ══ TRAINER D: читання числа з тексту ═════════════════════════════════════
    # Словники для розбору
    _ONES_W={"нуль":0,"один":1,"одна":1,"два":2,"дві":2,"три":3,"чотири":4,"п'ять":5,"шість":6,"сім":7,"вісім":8,"дев'ять":9}
    _TEEN_W={"десять":10,"одинадцять":11,"дванадцять":12,"тринадцять":13,"чотирнадцять":14,"п'ятнадцять":15,"шістнадцять":16,"сімнадцять":17,"вісімнадцять":18,"дев'ятнадцять":19}
    _TENS_W={"двадцять":20,"тридцять":30,"сорок":40,"п'ятдесят":50,"шістдесят":60,"сімдесят":70,"вісімдесят":80,"дев'яносто":90}
    _HUNDREDS_W={"сто":100,"двісті":200,"триста":300,"чотириста":400,"п'ятсот":500,"шістсот":600,"сімсот":700,"вісімсот":800,"дев'ятсот":900}
    _FRAC_NAMES={
        "десят":1,"десятих":1,"десята":1,"десяте":1,"десятих":1,
        "сот":2,"сотих":2,"сота":2,"соте":2,"сотих":2,
        "тисячн":3,"тисячних":3,"тисячна":3,"тисячне":3,
        "десятитисячн":4,"десятитисячних":4,
    }
    _FRAC_MAP={"десят":1,"сот":2,"тисячн":3,"десятитисячн":4}

    def _parse_number_text(self,text):
        """Парсить текстовий опис числа. Повертає (value, places) або None."""
        text=text.lower().strip()
        # Розбиваємо на частини: "X цілих Y [назва]" або "X [назва]"
        # Шукаємо 'цілих'/'ціла'/'ціле'
        whole=0; frac_num=0; places=0
        parts=text.replace("'","'").split()
        i=0; n=len(parts)
        # ціла частина
        whole_words=[]; frac_start=0
        found_whole_marker=False
        for j,w in enumerate(parts):
            if w in ("ціла","цілих","ціле","цілі"):
                # все до j — ціла
                whole_words=parts[:j]; frac_start=j+1; found_whole_marker=True; break
        if not found_whole_marker: frac_start=0; whole_words=[]
        # парсимо ціле
        whole=self._parse_int_words(whole_words) if whole_words else 0
        if whole is None: whole=0
        # парсимо дробову частину
        frac_parts=parts[frac_start:]
        # остання частина — назва розряду
        frac_name_places=0
        name_idx=-1
        for j in range(len(frac_parts)-1,-1,-1):
            w=frac_parts[j]
            for key,pl in self._FRAC_MAP.items():
                if w.startswith(key): frac_name_places=pl; name_idx=j; break
            if frac_name_places: break
        frac_num_words=frac_parts[:name_idx] if name_idx>0 else frac_parts[:name_idx] if name_idx==0 else frac_parts
        if name_idx>=0: frac_num_words=frac_parts[:name_idx]
        frac_num=self._parse_int_words(frac_num_words)
        if frac_num is None: return None
        places=frac_name_places
        if places==0: return None
        val=whole+frac_num/10**places
        return round(val,places), places

    def _parse_int_words(self,words):
        if not words: return 0
        total=0; cur=0
        for w in words:
            w=w.strip(".,")
            if w in self._HUNDREDS_W: cur+=self._HUNDREDS_W[w]
            elif w in self._TENS_W: cur+=self._TENS_W[w]
            elif w in self._TEEN_W: cur+=self._TEEN_W[w]
            elif w in self._ONES_W: cur+=self._ONES_W[w]
            else: return None  # невідоме слово
        total+=cur
        return total

    # Набір завдань з тексту — ПЕРЕВІРЕНО вручну
    _WORD_TASKS=[
        ("нуль цілих сім десятих",         "0,7",   1),
        ("нуль цілих п'ять десятих",        "0,5",   1),
        ("нуль цілих три десятих",          "0,3",   1),
        ("нуль цілих одна десята",          "0,1",   1),
        ("нуль цілих дев'ять десятих",      "0,9",   1),
        ("нуль цілих сорок дев'ять сотих",  "0,49",  2),
        ("нуль цілих сім сотих",            "0,07",  2),
        ("нуль цілих двадцять п'ять сотих", "0,25",  2),
        ("нуль цілих одна сота",            "0,01",  2),
        ("нуль цілих дев'яносто дев'ять сотих","0,99",2),
        ("одна ціла три десятих",           "1,3",   1),
        ("дві цілих п'ять десятих",         "2,5",   1),
        ("три цілих сімнадцять сотих",      "3,17",  2),
        ("п'ять цілих сім десятих",         "5,7",   1),
        ("дев'ять цілих дев'яносто дев'ять сотих","9,99",2),
        ("нуль цілих сорок одна тисячна",   "0,041", 3),
        ("нуль цілих двісті дев'ятнадцять тисячних","0,219",3),
        ("нуль цілих сімсот тисячних",      "0,700", 3),  # 700/1000
        ("нуль цілих сім тисячних",         "0,007", 3),  # 7/1000
        ("нуль цілих сто тисячних",         "0,100", 3),  # 100/1000
        ("нуль цілих п'ятсот тисячних",     "0,500", 3),
        ("нуль цілих одна тисячна",         "0,001", 3),
        ("два цілих сто двадцять п'ять тисячних","2,125",3),
        ("одна ціла двісті тисячних",       "1,200", 3),
    ]

    def show_trainer_d(self):
        self.clear_main(); cf=self.current_frame
        sbar=tk.Frame(cf,bg=PANEL,height=52,highlightbackground=BORDER,highlightthickness=1)
        sbar.pack(fill="x"); sbar.pack_propagate(False)
        self.td_score_lbl=tk.Label(sbar,text=self._td_st(),font=F_SCORE,bg=PANEL,fg=GREEN)
        self.td_score_lbl.pack(side="left",padx=24)
        tk.Label(sbar,text="Запиши десятковий дріб за словесним описом",font=("Segoe UI",14,"bold"),bg=PANEL,fg=MUTED).pack(side="left",padx=8)

        main=tk.Frame(cf,bg=BG); main.pack(fill="both",expand=True,padx=16,pady=12)
        left=tk.Frame(main,bg=BG); left.pack(side="left",fill="both",expand=True)
        right=tk.Frame(main,bg=BG,width=260); right.pack(side="right",fill="y",padx=(12,0)); right.pack_propagate(False)

        # ── правило
        rule_f=tk.Frame(left,bg=CARD_V,padx=16,pady=10,highlightbackground=ACCENT2,highlightthickness=1)
        rule_f.pack(fill="x",pady=(0,8))
        tk.Label(rule_f,text="📌  Як читати: «дві цілих п'ять десятих» → ціла частина = 2, дробова = 5, знаменник = 10 → 2,5",
                 font=("Segoe UI",13,"bold"),bg=CARD_V,fg=ACCENT2,justify="left",wraplength=700).pack(anchor="w")

        # ── завдання
        task_f=tk.Frame(left,bg=PANEL,highlightbackground=BORDER,highlightthickness=1,padx=24,pady=18)
        task_f.pack(fill="x",pady=(0,8))
        tk.Label(task_f,text="Запиши цифрами:",font=F_SUB,bg=PANEL,fg=TEXT).pack(anchor="w")
        self.td_task_lbl=tk.Label(task_f,text="",font=("Segoe UI",30,"bold"),bg=PANEL,fg=ACCENT2,wraplength=700,justify="left")
        self.td_task_lbl.pack(anchor="w",pady=10)

        # ── введення
        inp_f=tk.Frame(left,bg=CARD_Y,padx=16,pady=12,highlightbackground=ORANGE,highlightthickness=2)
        inp_f.pack(fill="x",pady=(0,6))
        tk.Label(inp_f,text="Відповідь:",font=("Segoe UI",14,"bold"),bg=CARD_Y,fg=ORANGE).pack(anchor="w",pady=(0,6))
        inp_row=tk.Frame(inp_f,bg=CARD_Y); inp_row.pack(anchor="w")
        self.td_inp_lbl=tk.Label(inp_row,text="",font=("Courier New",52,"bold"),bg=CARD_Y,fg=TEXT,width=12,anchor="w")
        self.td_inp_lbl.pack(side="left")
        self.td_cursor_lbl=tk.Label(inp_row,text="▮",font=("Courier New",52,"bold"),bg=CARD_Y,fg=ORANGE)
        self.td_cursor_lbl.pack(side="left")
        self.td_slots_lbl=tk.Label(inp_f,text="Вводь цифри та кому (,)",font=("Segoe UI",12),bg=CARD_Y,fg=MUTED)
        self.td_slots_lbl.pack(anchor="w",pady=(4,0))

        self.td_feed=tk.Label(left,text="",font=("Segoe UI",15),bg=BG,fg=ORANGE,wraplength=640,justify="center")
        self.td_feed.pack(pady=4)

        act=tk.Frame(left,bg=BG); act.pack(pady=6)
        self.td_check_btn=mkbtn(act,"✔  Перевірити",self._td_check,bg=GREEN,w=13,h=2)
        self.td_check_btn.pack(side="left",padx=8)
        mkbtn(act,"▶  Наступне",self._td_new,bg=ACCENT2,w=11,h=2).pack(side="left",padx=8)

        # нумпад + кнопка коми
        np_f=tk.Frame(right,bg=BG); np_f.pack(pady=(8,0))
        tk.Label(np_f,text="Клавіатура",font=("Segoe UI",14,"bold"),bg=BG,fg=MUTED).pack(pady=(0,4))
        def _td_key(ch):
            if ch=="," :
                if "," not in self._td_inp and len(self._td_inp)>0:
                    self._td_inp+=","; self._upd_td()
            elif ch.isdigit():
                self._td_inp+=ch; self._upd_td()
            elif ch=="⌫":
                self._td_inp=self._td_inp[:-1]; self._upd_td()
            elif ch=="C":
                self._td_inp=""; self._upd_td()
        build_numpad(np_f,_td_key,bg=BG).pack()
        # кнопка коми
        tk.Button(np_f,text="  ,  кома",font=("Segoe UI",16,"bold"),bg=CARD_Y,fg=ORANGE,
                  relief="flat",cursor="hand2",width=12,command=lambda:_td_key(",")).pack(pady=6)

        self._td_inp=""; self._td_ans=""; self._td_new()

    def _td_st(self): return f"Правильно: {self.td_score}  /  Завдань: {self.td_att}"

    def _td_new(self):
        task=random.choice(self._WORD_TASKS)
        self._td_text, self._td_ans, self._td_places=task
        self._td_inp=""; self.td_att+=1
        if self.td_task_lbl: self.td_task_lbl.config(text=f"«  {self._td_text}  »")
        self._upd_td()
        if self.td_feed: self.td_feed.config(text="")
        if self.td_check_btn: self.td_check_btn.config(state="normal",bg=GREEN)
        if self.td_score_lbl: self.td_score_lbl.config(text=self._td_st())

    def _upd_td(self):
        if self.td_inp_lbl: self.td_inp_lbl.config(text=self._td_inp)
        if self.td_cursor_lbl: self.td_cursor_lbl.config(text="▮" if len(self._td_inp)<12 else "")

    def _td_check(self):
        inp=self._td_inp.strip()
        if not inp:
            if self.td_feed: self.td_feed.config(text="⚠️  Введіть відповідь!",fg=ORANGE); return
        if inp==self._td_ans:
            self.td_score+=1
            if self.td_check_btn: self.td_check_btn.config(state="disabled",bg=BTN_NUM)
            if self.td_cursor_lbl: self.td_cursor_lbl.config(text="")
            if self.td_inp_lbl: self.td_inp_lbl.config(fg=GREEN)
            if self.td_feed: self.td_feed.config(text=f"🎉  Правильно!  {self._td_text}  =  {self._td_ans}",fg=GREEN)
        else:
            if self.td_feed: self.td_feed.config(text=f"❌  Не вірно.  Правильно: «{self._td_ans}»",fg=RED)
        if self.td_score_lbl: self.td_score_lbl.config(text=self._td_st())

    # ══ TRAINER Z: нулі-знаки практика ════════════════════════════════════════
    def show_trainer_z(self):
        self.clear_main(); cf=self.current_frame
        sbar=tk.Frame(cf,bg=PANEL,height=52,highlightbackground=BORDER,highlightthickness=1)
        sbar.pack(fill="x"); sbar.pack_propagate(False)
        self.tz_score_lbl=tk.Label(sbar,text=self._tz_st(),font=F_SCORE,bg=PANEL,fg=GREEN)
        self.tz_score_lbl.pack(side="left",padx=24)
        tk.Label(sbar,text="Нулі↔знаки: практика",font=("Segoe UI",14,"bold"),bg=PANEL,fg=MUTED).pack(side="left",padx=8)

        main=tk.Frame(cf,bg=BG); main.pack(fill="both",expand=True,padx=16,pady=12)
        left=tk.Frame(main,bg=BG); left.pack(side="left",fill="both",expand=True)
        right=tk.Frame(main,bg=BG,width=260); right.pack(side="right",fill="y",padx=(12,0)); right.pack_propagate(False)

        # ── правило
        rule_f=tk.Frame(left,bg=CARD_V,padx=16,pady=10,highlightbackground=ACCENT2,highlightthickness=1)
        rule_f.pack(fill="x",pady=(0,8))
        tk.Label(rule_f,text="📌  Скільки цифр після коми ↔ скільки нулів у знаменнику",
                 font=("Segoe UI",13,"bold"),bg=CARD_V,fg=ACCENT2).pack(anchor="w")

        # ── тип завдань (режим)
        mode_f=tk.Frame(left,bg=BG); mode_f.pack(fill="x",pady=(0,8))
        tk.Label(mode_f,text="Тип:",font=F_BODYB,bg=BG,fg=MUTED).pack(side="left",padx=(0,8))
        self._tz_mode="zeros"  # zeros | digits | both
        self._tz_mode_btns=[]
        for m,lbl in [("zeros","Знайди кількість нулів"),("digits","Знайди кількість цифр"),("both","Змішаний")]:
            b=tk.Button(mode_f,text=lbl,font=("Segoe UI",12,"bold"),bg=BTN_NUM,fg=TEXT,
                       relief="flat",cursor="hand2",padx=12,pady=5,command=lambda x=m:self._tz_set_mode(x))
            b.pack(side="left",padx=4)
            self._tz_mode_btns.append((b,m))
        self._tz_set_mode("zeros")

        # ── завдання
        task_f=tk.Frame(left,bg=PANEL,highlightbackground=BORDER,highlightthickness=1,padx=24,pady=18)
        task_f.pack(fill="x",pady=(0,8))
        self.tz_question_lbl=tk.Label(task_f,text="",font=("Segoe UI",22,"bold"),bg=PANEL,fg=TEXT,wraplength=680,justify="left")
        self.tz_question_lbl.pack(anchor="w",pady=6)
        self.tz_object_lbl=tk.Label(task_f,text="",font=("Courier New",58,"bold"),bg=PANEL,fg=RED)
        self.tz_object_lbl.pack(anchor="w",pady=8)
        self.tz_question2_lbl=tk.Label(task_f,text="",font=("Segoe UI",20),bg=PANEL,fg=MUTED)
        self.tz_question2_lbl.pack(anchor="w")

        # ── варіанти відповіді (4 кнопки)
        self.tz_ans_frame=tk.Frame(left,bg=BG); self.tz_ans_frame.pack(fill="x",pady=8)
        self.tz_feed=tk.Label(left,text="",font=("Segoe UI",16,"bold"),bg=BG,fg=ORANGE,wraplength=640)
        self.tz_feed.pack(pady=4)

        act=tk.Frame(left,bg=BG); act.pack(pady=6)
        mkbtn(act,"▶  Наступне",self._tz_new,bg=ACCENT2,w=11,h=2).pack(side="left",padx=8)

        # Пояснення справа
        tk.Label(right,text="Пам'ятка",font=("Segoe UI",14,"bold"),bg=BG,fg=MUTED).pack(pady=(8,6))
        memo_f=tk.Frame(right,bg=CARD_V,padx=12,pady=12,highlightbackground=ACCENT2,highlightthickness=1)
        memo_f.pack(fill="x")
        for row in [("0,7","1 знак","1 нуль (10)"),("0,49","2 знаки","2 нулі (100)"),("0,041","3 знаки","3 нулі (1000)"),("0,0071","4 знаки","4 нулі (10000)")]:
            f=tk.Frame(memo_f,bg=CARD_V); f.pack(fill="x",pady=3)
            tk.Label(f,text=row[0],font=("Courier New",16,"bold"),bg=CARD_V,fg=RED,width=8,anchor="w").pack(side="left")
            tk.Label(f,text=row[1],font=("Segoe UI",13),bg=CARD_V,fg=C_DIGIT,width=8).pack(side="left")
            tk.Label(f,text=row[2],font=("Segoe UI",13),bg=CARD_V,fg=C_ZERO).pack(side="left")

        # Встановлюємо режим і генеруємо перше завдання ПІСЛЯ створення всіх widgets
        self._tz_mode="zeros"
        self._tz_set_mode("zeros")

    def _tz_st(self): return f"Правильно: {self.tz_score}  /  Завдань: {self.tz_att}"

    def _tz_set_mode(self,m):
        self._tz_mode=m
        if hasattr(self,'_tz_mode_btns'):
            for b,bm in self._tz_mode_btns:
                b.config(bg=ACCENT2 if bm==m else BTN_NUM,fg=WHITE if bm==m else TEXT)
        if hasattr(self,'tz_ans_frame') and self.tz_ans_frame.winfo_exists():
            self._tz_new()

    def _tz_new(self):
        if not hasattr(self,'tz_ans_frame') or not self.tz_ans_frame.winfo_exists(): return
        for w in self.tz_ans_frame.winfo_children(): w.destroy()
        if hasattr(self,'tz_feed') and self.tz_feed.winfo_exists():
            self.tz_feed.config(text="")
        self.tz_att+=1
        mode=self._tz_mode
        if mode=="both": mode=random.choice(["zeros","digits"])

        places=random.choice([1,2,3,4])
        denom=10**places

        if mode=="zeros":
            val=random.randint(1,denom-1)/denom
            dec_str=f"{val:.{places}f}".replace(".",",")
            self.tz_question_lbl.config(text="Скільки нулів у знаменнику цього числа?")
            self.tz_object_lbl.config(text=dec_str)
            self.tz_question2_lbl.config(text="(яким буде знаменник?)")
        else:
            self.tz_question_lbl.config(text="Скільки цифр після коми у дробі з таким знаменником?")
            self.tz_object_lbl.config(text=str(denom))
            self.tz_question2_lbl.config(text=f"Знаменник: {denom}")

        correct=places
        # Неправильні варіанти — 3 різних від правильного
        wrong_pool=[x for x in [1,2,3,4,5] if x!=correct]
        wrong_vals=random.sample(wrong_pool, min(3,len(wrong_pool)))
        options=[correct]+wrong_vals
        random.shuffle(options)

        self._tz_correct=correct

        for opt in options:
            if mode=="zeros":
                label=f"{opt}  →  знаменник 1{'0'*opt}"
            else:
                label=f"{opt} цифр{'а' if opt==1 else 'и' if opt<5 else ''} після коми"
            btn=tk.Button(self.tz_ans_frame,text=label,
                font=("Segoe UI",16,"bold"),bg=BTN_NUM,fg=TEXT,
                relief="flat",cursor="hand2",padx=16,pady=10,
                command=lambda o=opt:self._tz_answer(o))
            btn.pack(fill="x",pady=3,padx=4)
            o_bg=BTN_NUM
            btn.bind("<Enter>",lambda e,x=btn,ob=o_bg:x.config(bg=_dk(ob,18)))
            btn.bind("<Leave>",lambda e,x=btn,ob=o_bg:x.config(bg=ob))

        if self.tz_score_lbl: self.tz_score_lbl.config(text=self._tz_st())

    def _tz_answer(self,chosen):
        correct=self._tz_correct
        # Блокуємо всі кнопки і підсвічуємо
        for w in self.tz_ans_frame.winfo_children():
            w.config(state="disabled")
            try:
                # Витягуємо число з тексту кнопки (перший токен)
                first=w.cget("text").strip().split()[0]
                opt=int(first)
                if opt==correct:
                    w.config(bg=GREEN_LT,fg=GREEN)
                elif opt==chosen:
                    w.config(bg=RED_LT,fg=RED)
            except: pass
        if chosen==correct:
            self.tz_score+=1
            self.tz_feed.config(text=f"✅  Правильно!  {correct} знак(и) ↔ {correct} нуль(і) ↔ знаменник 1{'0'*correct}",fg=GREEN)
        else:
            self.tz_feed.config(text=f"❌  Правильно: {correct}.  {correct} цифр ↔ {correct} нулів ↔ знаменник 1{'0'*correct}",fg=RED)
        if self.tz_score_lbl: self.tz_score_lbl.config(text=self._tz_st())

if __name__=="__main__":
    App().mainloop()
