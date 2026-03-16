"""
§ 40. Десятковий дріб — повний модуль (А + Б об'єднані)
Теорія, сітка-візуалізатор, розряди, числова пряма,
зв'язок нулів, тренажери перетворень.
ВИПРАВЛЕНО:
  - Сітка тисячних: правильна 25×40 сітка
  - Числова пряма: завдання + overflow (лічильник)
  - Нулі-знаки: центральний дріб оновлюється правильно
  - Дріб→дес: наочний дріб, поле введення, кнопки
  - Дріб→дес: цілі числа
  - Нова теорія: нулі в кінці десяткового дробу
"""
import tkinter as tk
import random, math

# ── Palette ───────────────────────────────────────────────────────────────────
BG="#f0f4f8"; PANEL="#ffffff"; BORDER="#cbd5e1"; TEXT="#0f172a"; MUTED="#475569"
WHITE="#ffffff"; BTN_NUM="#e2e8f0"; HDR_BG="#1d4ed8"; NAV_BG="#1e3a5f"; NAV_FG="#ffffff"
ACCENT="#1d4ed8"; ACCENT2="#7c3aed"; GREEN="#15803d"; GREEN_LT="#dcfce7"
RED="#b91c1c"; RED_LT="#fee2e2"; ORANGE="#b45309"; ORANGE_LT="#fef3c7"
CARD_B="#dbeafe"; CARD_V="#ede9fe"; CARD_G="#dcfce7"; CARD_Y="#fef9c3"
CARD_R="#fee2e2"; TEAL="#0f766e"; TEAL_LT="#ccfbf1"
C_DIGIT="#db2777"; C_ZERO="#059669"
FILL_10="#3b82f6"; FILL_100="#8b5cf6"; FILL_1000="#16a34a"; C_EMPTY="#e2e8f0"

# ── Fonts ─────────────────────────────────────────────────────────────────────
F_TITLE=("Segoe UI",34,"bold"); F_HEAD=("Segoe UI",26,"bold")
F_SUB=("Segoe UI",20,"bold");   F_BODY=("Segoe UI",17)
F_BODYB=("Segoe UI",17,"bold"); F_BTN=("Segoe UI",19,"bold")
F_NAV=("Segoe UI",14,"bold");   F_SCORE=("Segoe UI",20,"bold")
F_SMALL=("Segoe UI",13);        F_FRAC=("Segoe UI",38,"bold")
F_FRAC_S=("Segoe UI",22,"bold");F_NUM=("Segoe UI",26,"bold")
F_CTRL=("Segoe UI",22,"bold");  F_BIG_DEC=("Courier New",68,"bold")

# ── Helpers ───────────────────────────────────────────────────────────────────
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
    fn=F_FRAC if size=="big" else F_FRAC_S; bw=66 if size=="big" else 44
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
        rf=tk.Frame(np,bg=bg); rf.pack(pady=4)
        for ch in row:
            bc,fc=(BTN_NUM,TEXT) if ch.isdigit() else ((RED_LT,RED) if ch=="C" else (CARD_V,ACCENT2))
            b=tk.Button(rf,text=ch,font=F_NUM,width=4,height=1,bg=bc,fg=fc,relief="flat",
                       cursor="hand2",command=lambda c=ch:fn(c))
            b.pack(side="left",padx=5)
            o=bc; b.bind("<Enter>",lambda e,x=b,oo=o:x.config(bg=_dk(oo,18))); b.bind("<Leave>",lambda e,x=b,oo=o:x.config(bg=oo))
    return np

def draw_frac_canvas(p,ns,ds,bg=PANEL,nc=ACCENT,dc=ACCENT,lc=ACCENT):
    fn=("Courier New",34,"bold")
    bw=max(len(ns)*22+20,len(ds)*22+20)+8; H=100
    cv=tk.Canvas(p,bg=bg,width=bw,height=H,highlightthickness=0)
    cv.create_text(bw//2,20,text=ns,font=fn,fill=nc,anchor="center")
    cv.create_line(4,50,bw-4,50,fill=lc,width=3)
    cv.create_text(bw//2,78,text=ds,font=fn,fill=dc,anchor="center")
    return cv

def draw_number_line(p,marks,lo=0.0,hi=2.0,step=0.1,width=800,bg=PANEL):
    H=110; cv=tk.Canvas(p,bg=bg,width=width,height=H,highlightthickness=0)
    L,R=60,width-40; ly=60; span=R-L
    def px(v): return L+(v-lo)/(hi-lo)*span
    cv.create_line(L,ly,R,ly,fill=MUTED,width=3)
    cv.create_line(R-14,ly-7,R,ly,fill=MUTED,width=3)
    cv.create_line(R-14,ly+7,R,ly,fill=MUTED,width=3)
    v=lo
    while v<=hi+1e-9:
        vr=round(v,6); x=px(vr); iw=abs(vr-round(vr))<1e-9
        th=14 if iw else 7; lw=3 if iw else 1; col=TEXT if iw else MUTED
        cv.create_line(x,ly-th,x,ly+th,fill=col,width=lw)
        if iw: cv.create_text(x,ly+26,text=str(int(round(vr))),font=("Segoe UI",14,"bold"),fill=TEXT)
        else:
            s=f"{vr:.10f}".rstrip("0").rstrip(".")
            cv.create_text(x,ly+22,text=s,font=("Segoe UI",10),fill=MUTED)
        v=round(v+step,10)
    for val,color,label in marks:
        if lo<=val<=hi:
            x=px(val)
            cv.create_oval(x-9,ly-9,x+9,ly+9,fill=color,outline=WHITE,width=2)
            cv.create_text(x,ly-24,text=label,font=("Segoe UI",13,"bold"),fill=color)
    return cv

# ══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("§ 40.  Десятковий дріб")
        self.configure(bg=BG)
        self.attributes("-fullscreen",True)
        self.bind("<Escape>",lambda e:self.attributes("-fullscreen",False))
        self.SW=self.winfo_screenwidth(); self.SH=self.winfo_screenheight()
        self.current_frame=None; self.mode=None

        # Grid state
        self.gmode="tenths"; self.gval=0; self.gtask=False
        self.gtarget=0; self.glocked=False; self.gscore=0; self.gtotal=0

        # Place-value state
        self.pv_digits=[0,7,5,3]; self.pv_places=2

        # Zeros-demo state
        self.zdemo_places=2; self._zdemo_digits=[]

        # Trainer A: decimal→fraction
        self.ta_dec=""; self.ta_n=0; self.ta_d=0
        self.ta_inp_n=""; self.ta_inp_d=""; self.ta_active="n"; self.ta_n_done=False
        self.ta_score=0; self.ta_att=0
        self.ta_score_lbl=None; self.ta_task_lbl=None
        self.ta_feed=None; self.ta_check=None; self.ta_step1=None
        self.ta_step_lbl=None; self.ta_inp_lbl=None; self.ta_steps=[]

        # Trainer B: fraction→decimal
        self.tb_n=0; self.tb_d=0; self.tb_whole=0; self.tb_ans=""
        self.tb_inp=""; self.tb_score=0; self.tb_att=0
        self.tb_score_lbl=None; self.tb_task_f=None
        self.tb_inp_lbl=None; self.tb_feed=None; self.tb_check=None; self.tb_hint=None
        self.tb_frac_cv=None  # canvas for live fraction display

        # Number line task state
        self.nl_task_mode=False
        self.nl_task_target=0.0
        self.nl_task_prec="tenths"
        self.nl_task_score=0
        self.nl_task_total=0
        self.nl_task_locked=False

        self._build_chrome()
        self.show_main_menu()

    def _build_chrome(self):
        hdr=tk.Frame(self,bg=HDR_BG,height=70); hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr,text="§ 40.   Десятковий дріб",bg=HDR_BG,fg=WHITE,
                 font=("Segoe UI",21,"bold")).pack(side="left",padx=30)
        mkbtn(hdr,"✕  Вийти",self.destroy,bg="#b91c1c",font=("Segoe UI",13,"bold"),w=9,h=1).pack(side="right",padx=18,pady=16)
        nav=tk.Frame(self,bg=NAV_BG,height=52); nav.pack(fill="x"); nav.pack_propagate(False)
        for lbl,cmd in [
            ("🏠 Меню",self.show_main_menu),
            ("📖 Теорія А",self.show_theory_a),
            ("📖 Теорія Б",self.show_theory_b),
            ("📖 Нулі в кінці",self.show_theory_c),
            ("🟦 Сітка",self.show_grid),
            ("🔢 Розряди",self.show_place_value),
            ("📏 Пряма",self.show_number_line),
            ("🔗 Нулі↔знаки",self.show_zeros_demo),
            ("🎯 Дес→дріб",self.show_trainer_a),
            ("🎯 Дріб→дес",self.show_trainer_b),
        ]:
            b=tk.Button(nav,text=lbl,command=cmd,bg=NAV_BG,fg=NAV_FG,font=F_NAV,
                       relief="flat",bd=0,cursor="hand2",activebackground=ACCENT,activeforeground=WHITE,padx=10,pady=14)
            b.pack(side="left")
            b.bind("<Enter>",lambda e,x=b:x.config(bg=ACCENT)); b.bind("<Leave>",lambda e,x=b:x.config(bg=NAV_BG))
        self.main_area=tk.Frame(self,bg=BG); self.main_area.pack(fill="both",expand=True)

    def clear_main(self):
        if self.current_frame: self.current_frame.destroy()
        self.current_frame=tk.Frame(self.main_area,bg=BG); self.current_frame.pack(expand=True,fill="both")

    def _scroll_page(self):
        sc=tk.Canvas(self.current_frame,bg=BG,highlightthickness=0)
        vsb=tk.Scrollbar(self.current_frame,orient="vertical",command=sc.yview)
        sc.configure(yscrollcommand=vsb.set); vsb.pack(side="right",fill="y"); sc.pack(side="left",fill="both",expand=True)
        outer=tk.Frame(sc,bg=BG); win=sc.create_window((0,0),window=outer,anchor="nw")
        outer.bind("<Configure>",lambda e:sc.configure(scrollregion=sc.bbox("all")))
        sc.bind("<Configure>",lambda e:sc.itemconfig(win,width=e.width))
        p=tk.Frame(outer,bg=BG); p.pack(fill="both",expand=True,padx=60,pady=28)
        return p

    # ══ MAIN MENU ═════════════════════════════════════════════════════════════
    def show_main_menu(self):
        self.clear_main(); c=tk.Frame(self.current_frame,bg=BG); c.place(relx=.5,rely=.5,anchor="center")
        tk.Label(c,text="Десятковий дріб",font=("Segoe UI",50,"bold"),bg=BG,fg=TEXT).pack(pady=(0,4))
        tk.Label(c,text="§ 40   —  знайомство, запис, розряди, перетворення",font=("Segoe UI",22),bg=BG,fg=ACCENT).pack(pady=(0,24))
        cards=[
            ("📖","Теорія\nЗапис",CARD_B,ACCENT,self.show_theory_a),
            ("📖","Теорія\nНулі↔знаки",CARD_V,ACCENT2,self.show_theory_b),
            ("📖","Теорія\nНулі в кінці",TEAL_LT,TEAL,self.show_theory_c),
            ("🟦","Сітка-\nвізуалізатор",CARD_G,GREEN,self.show_grid),
            ("🔢","Розряди",CARD_Y,ORANGE,self.show_place_value),
            ("📏","Числова\nпряма",TEAL_LT,TEAL,self.show_number_line),
            ("🔗","Нулі↔знаки\nдемо",CARD_V,ACCENT2,self.show_zeros_demo),
            ("🎯","Дес→дріб",CARD_G,GREEN,self.show_trainer_a),
            ("🎯","Дріб→дес",CARD_Y,ORANGE,self.show_trainer_b),
        ]
        row=tk.Frame(c,bg=BG); row.pack()
        for icon,title,bg_c,fg_c,cmd in cards:
            card=tk.Frame(row,bg=bg_c,width=175,height=180,highlightbackground=BORDER,highlightthickness=2)
            card.pack(side="left",padx=8); card.pack_propagate(False)
            tk.Label(card,text=icon,font=("Segoe UI",32),bg=bg_c,fg=fg_c).pack(pady=(16,2))
            tk.Label(card,text=title,font=("Segoe UI",12,"bold"),bg=bg_c,fg=fg_c,justify="center").pack()
            for w in [card]+list(card.winfo_children()):
                w.bind("<Button-1>",lambda e,f=cmd:f())
            card.bind("<Enter>",lambda e,x=card,col=bg_c:x.config(bg=_dk(col,12)))
            card.bind("<Leave>",lambda e,x=card,col=bg_c:x.config(bg=col))
        tk.Label(c,text="Натисніть на картку або меню",font=F_SMALL,bg=BG,fg=MUTED).pack(pady=14)

    # ══ THEORY A ══════════════════════════════════════════════════════════════
    def show_theory_a(self):
        self.clear_main(); p=self._scroll_page()
        tk.Label(p,text="Десятковий дріб: запис і читання",font=F_TITLE,bg=BG,fg=TEXT).pack(anchor="w")
        hline(p,ACCENT)
        idea_f=tk.Frame(p,bg=CARD_B,padx=22,pady=18,highlightbackground=ACCENT,highlightthickness=2)
        idea_f.pack(fill="x",pady=8)
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
        alg_f=tk.Frame(p,bg=CARD_G,padx=22,pady=18,highlightbackground=GREEN,highlightthickness=2); alg_f.pack(fill="x",pady=8)
        tk.Label(alg_f,text="🔑  Алгоритм: звичайний → десятковий",font=F_SUB,bg=CARD_G,fg=GREEN).pack(anchor="w")
        for step,color,txt in [("Крок 1",ACCENT,"Записати цілу частину, поставити кому"),("Крок 2",GREEN,"Після коми записати чисельник із потрібною кількістю цифр"),("⚠️",ORANGE,"Якщо цифр менше ніж нулів — доповнити нулями СПЕРЕДУ")]:
            r=tk.Frame(alg_f,bg=CARD_G); r.pack(anchor="w",pady=4)
            tk.Label(r,text=f"  {step}:  ",font=("Segoe UI",18,"bold"),bg=CARD_G,fg=color,width=12,anchor="w").pack(side="left")
            tk.Label(r,text=txt,font=("Segoe UI",18),bg=CARD_G,fg=TEXT,justify="left",wraplength=1100).pack(side="left")
        zp_f=tk.Frame(alg_f,bg=PANEL,padx=16,pady=12,highlightbackground=BORDER,highlightthickness=1); zp_f.pack(fill="x",pady=8)
        tk.Label(zp_f,text="Приклади з нулями-вставками:",font=F_BODYB,bg=PANEL,fg=TEXT).pack(anchor="w")
        for fs,dec,note in [("3/1000","0,003","3 нулі → 2 нулі перед «3»"),("41/1000","0,041","3 нулі → 1 нуль перед «41»"),("29/100","0,29","2 нулі → нічого не треба")]:
            r=tk.Frame(zp_f,bg=PANEL); r.pack(anchor="w",pady=3)
            tk.Label(r,text=f"{fs}  =  ",font=F_BODY,bg=PANEL,fg=MUTED).pack(side="left")
            tk.Label(r,text=dec,font=("Segoe UI",22,"bold"),bg=PANEL,fg=RED).pack(side="left")
            tk.Label(r,text=f"    ({note})",font=F_SMALL,bg=PANEL,fg=MUTED).pack(side="left")
        tf=tk.Frame(p,bg=PANEL,padx=22,pady=18,highlightbackground=BORDER,highlightthickness=1); tf.pack(fill="x",pady=8)
        tk.Label(tf,text="📐  Розряди: число 17,295",font=F_SUB,bg=PANEL,fg=TEXT).pack(anchor="w")
        tbl=tk.Frame(tf,bg=PANEL); tbl.pack(anchor="w",pady=8)
        headers=["Десятки","Одиниці","","Десяті","Соті","Тисячні"]
        hcols=[TEXT,TEXT,MUTED,ACCENT,ACCENT2,GREEN]
        hbgs=[CARD_B,CARD_B,PANEL,CARD_G,CARD_G,CARD_G]
        for j,(h,hc,hb) in enumerate(zip(headers,hcols,hbgs)):
            tk.Frame(tbl,bg=hb,padx=14,pady=8,width=100,height=50,highlightbackground=BORDER,highlightthickness=1).grid(row=0,column=j,padx=2,pady=2)
            tk.Label(tbl.grid_slaves(row=0,column=j)[0],text=h,font=F_SMALL,bg=hb,fg=hc).pack(expand=True)
        digs=[("1",TEXT,CARD_B),("7",TEXT,CARD_B),(",",MUTED,PANEL),("2",ACCENT,CARD_G),("9",ACCENT2,CARD_G),("5",GREEN,CARD_G)]
        for j,(d,dc,db) in enumerate(digs):
            c=tk.Frame(tbl,bg=db,padx=14,pady=8,width=100,height=70,highlightbackground=BORDER,highlightthickness=1)
            c.grid(row=1,column=j,padx=2,pady=2); c.pack_propagate(False)
            fn=("Segoe UI",36,"bold") if d!="," else ("Segoe UI",48,"bold")
            tk.Label(c,text=d,font=fn,bg=db,fg=dc).pack(expand=True)
        theory_card(p,"💡  Запам'ятай","Скільки нулів у знаменнику → стільки цифр після коми.\nЯкщо цифр менше — доповнюємо нулями зліва.\nДесяті: 1 цифра.  Соті: 2.  Тисячні: 3.","#f1f5f9",MUTED)

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
        rev_f=tk.Frame(p,bg=CARD_B,padx=22,pady=18,highlightbackground=ACCENT,highlightthickness=2); rev_f.pack(fill="x",pady=8)
        tk.Label(rev_f,text="🔄  Десятковий → звичайний дріб",font=F_SUB,bg=CARD_B,fg=ACCENT).pack(anchor="w")
        tk.Label(rev_f,text="Рахуємо цифри після коми → стільки нулів у знаменнику.\nЦифри після коми (з нулями) = чисельник.",font=F_BODY,bg=CARD_B,fg=TEXT,justify="left").pack(anchor="w",pady=(6,8))
        rev_row=tk.Frame(rev_f,bg=CARD_B); rev_row.pack(anchor="w",pady=4)
        for dec,n,d in [("0,7","7","10"),("0,49","49","100"),("0,041","41","1000"),("3,007","3007","1000")]:
            box=tk.Frame(rev_row,bg=PANEL,padx=14,pady=10,highlightbackground=BORDER,highlightthickness=1); box.pack(side="left",padx=8)
            tk.Label(box,text=dec,font=("Courier New",28,"bold"),bg=PANEL,fg=RED).pack()
            tk.Label(box,text="=",font=F_HEAD,bg=PANEL,fg=MUTED).pack()
            frac_w(box,n,d,PANEL,"small",ACCENT).pack()
        theory_card(p,"💡  Запам'ятай","Десятковий → звичайний: рахуй цифри після коми → нулі знаменника.\nЗвичайний → десятковий: рахуй нулі → заповни цифри після коми (додай нулі зліва якщо треба).","#f1f5f9",MUTED)

    # ══ THEORY C: нулі в кінці десяткового дробу ═════════════════════════════
    def show_theory_c(self):
        self.clear_main(); p=self._scroll_page()
        tk.Label(p,text="Нулі в кінці десяткового дробу",font=F_TITLE,bg=BG,fg=TEXT).pack(anchor="w")
        hline(p,TEAL)

        rule_f=tk.Frame(p,bg=TEAL_LT,padx=22,pady=18,highlightbackground=TEAL,highlightthickness=2)
        rule_f.pack(fill="x",pady=8)
        tk.Label(rule_f,text="📌  Головне правило",font=F_SUB,bg=TEAL_LT,fg=TEAL).pack(anchor="w")
        tk.Label(rule_f,
            text="Нулі в кінці дробової частини НЕ змінюють значення числа.\n"
                 "Їх можна дописувати і прибирати — число залишається тим самим.",
            font=F_BODY,bg=TEAL_LT,fg=TEXT,justify="left").pack(anchor="w",pady=(8,4))

        # Візуальні приклади рівності
        eq_f=tk.Frame(p,bg=PANEL,padx=22,pady=18,highlightbackground=BORDER,highlightthickness=1)
        eq_f.pack(fill="x",pady=8)
        tk.Label(eq_f,text="📊  Всі ці записи рівні між собою:",font=F_SUB,bg=PANEL,fg=TEXT).pack(anchor="w")
        eq_row=tk.Frame(eq_f,bg=PANEL); eq_row.pack(anchor="w",pady=12)
        for group in [["0,5","0,50","0,500"],["1,3","1,30","1,300"],["2,70","2,7","2,700"]]:
            box=tk.Frame(eq_row,bg=CARD_B,padx=16,pady=12,highlightbackground=ACCENT,highlightthickness=1)
            box.pack(side="left",padx=10)
            for i,s in enumerate(group):
                col=RED if i==0 else (_dk(RED,20) if i==1 else _dk(RED,35))
                tk.Label(box,text=s,font=("Courier New",30,"bold"),bg=CARD_B,fg=col).pack()
                if i<len(group)-1:
                    tk.Label(box,text="=",font=("Segoe UI",18),bg=CARD_B,fg=MUTED).pack()

        # Дроби — рівність
        frac_f=tk.Frame(p,bg=CARD_G,padx=22,pady=18,highlightbackground=GREEN,highlightthickness=2)
        frac_f.pack(fill="x",pady=8)
        tk.Label(frac_f,text="🔑  Чому це працює? — Дробовий запис",font=F_SUB,bg=CARD_G,fg=GREEN).pack(anchor="w")
        tk.Label(frac_f,text="Додавання нуля в кінці = множення чисельника і знаменника на 10 → дріб не змінюється:",
                 font=F_BODY,bg=CARD_G,fg=TEXT,justify="left").pack(anchor="w",pady=(6,8))
        frac_row=tk.Frame(frac_f,bg=CARD_G); frac_row.pack(anchor="w")
        for pairs in [("5","10","50","100"),("3","10","30","100"),("7","100","70","1000")]:
            n1,d1,n2,d2=pairs
            box=tk.Frame(frac_row,bg=PANEL,padx=14,pady=10,highlightbackground=BORDER,highlightthickness=1)
            box.pack(side="left",padx=10)
            row2=tk.Frame(box,bg=PANEL); row2.pack()
            frac_w(row2,n1,d1,PANEL,"small",ACCENT).pack(side="left")
            tk.Label(row2,text=" = ",font=F_HEAD,bg=PANEL,fg=MUTED).pack(side="left")
            frac_w(row2,n2,d2,PANEL,"small",GREEN).pack(side="left")
            tk.Label(box,text=f"0,{n1.zfill(len(d1)-1)} = 0,{n2.zfill(len(d2)-1)}",
                     font=("Courier New",20,"bold"),bg=PANEL,fg=RED).pack(pady=(6,0))

        # Коли ПРИБИРАЄМО нулі
        rem_f=tk.Frame(p,bg=CARD_Y,padx=22,pady=18,highlightbackground=ORANGE,highlightthickness=2)
        rem_f.pack(fill="x",pady=8)
        tk.Label(rem_f,text="✂️  Скорочення: прибираємо зайві нулі",font=F_SUB,bg=CARD_Y,fg=ORANGE).pack(anchor="w")
        tk.Label(rem_f,text="Прибираємо тільки кінцеві нулі дробової частини. Нулі всередині або на початку — НЕ чіпаємо!",
                 font=F_BODY,bg=CARD_Y,fg=TEXT,justify="left").pack(anchor="w",pady=(6,8))
        rem_row=tk.Frame(rem_f,bg=CARD_Y); rem_row.pack(anchor="w")
        for before,after,note in [("0,500","0,5","можна прибрати"),("3,120","3,12","можна прибрати"),("0,041","0,041","НЕ прибирати! (не кінцевий)"),("1,300","1,3","можна прибрати")]:
            box=tk.Frame(rem_row,bg=PANEL,padx=12,pady=10,highlightbackground=BORDER,highlightthickness=1)
            box.pack(side="left",padx=8)
            tk.Label(box,text=before,font=("Courier New",26,"bold"),bg=PANEL,fg=MUTED).pack()
            tk.Label(box,text="→",font=("Segoe UI",22),bg=PANEL,fg=MUTED).pack()
            col=GREEN if "можна" in note else RED
            tk.Label(box,text=after,font=("Courier New",26,"bold"),bg=PANEL,fg=col).pack()
            tk.Label(box,text=note,font=F_SMALL,bg=PANEL,fg=col).pack(pady=(4,0))

        # Коли ДОПИСУЄМО нулі
        add_f=tk.Frame(p,bg=CARD_V,padx=22,pady=18,highlightbackground=ACCENT2,highlightthickness=2)
        add_f.pack(fill="x",pady=8)
        tk.Label(add_f,text="✏️  Коли ДОПИСУЄМО нулі — для чого це потрібно",font=F_SUB,bg=CARD_V,fg=ACCENT2).pack(anchor="w")
        usecases=[
            ("Порівняння","0,3 та 0,27  →  0,30 та 0,27  →  30>27  →  0,3>0,27"),
            ("Додавання/Віднімання","0,5 + 0,37  →  0,50 + 0,37 = 0,87"),
            ("Однакова кількість знаків","3,1  →  3,100  (щоб була однакова кількість цифр)"),
        ]
        for title,ex in usecases:
            uf=tk.Frame(add_f,bg=PANEL,padx=14,pady=10,highlightbackground=BORDER,highlightthickness=1)
            uf.pack(fill="x",pady=4)
            tk.Label(uf,text=f"▶  {title}:",font=F_BODYB,bg=PANEL,fg=ACCENT2).pack(anchor="w")
            tk.Label(uf,text=ex,font=("Courier New",20,"bold"),bg=PANEL,fg=TEXT).pack(anchor="w",pady=(2,0))

        theory_card(p,"💡  Запам'ятай",
            "0,5 = 0,50 = 0,500  — значення не змінюється.\n"
            "Кінцеві нулі після коми можна прибирати і дописувати вільно.\n"
            "Але нулі всередині (0,041) і нулі цілої частини — НЕ чіпаємо!",
            "#f1f5f9",MUTED)

    # ══ GRID VISUALIZER ═══════════════════════════════════════════════════════
    def show_grid(self):
        self.clear_main(); cf=self.current_frame
        toolbar=tk.Frame(cf,bg=PANEL,highlightbackground=BORDER,highlightthickness=1,height=60)
        toolbar.pack(fill="x"); toolbar.pack_propagate(False)
        self.gmode_btns={}
        for mode,label,color in [("tenths","Десяті\n(÷10)",FILL_10),("hundredths","Соті\n(÷100)",FILL_100),("thousandths","Тисячні\n(÷1000)",FILL_1000)]:
            b=tk.Button(toolbar,text=label,font=("Segoe UI",13,"bold"),bg=BTN_NUM,fg=TEXT,relief="flat",cursor="hand2",padx=16,pady=4,justify="center",command=lambda m=mode:self._gset(m))
            b.pack(side="left",padx=8,pady=8); self.gmode_btns[mode]=(b,color)
        tk.Frame(toolbar,bg=BORDER,width=2).pack(side="left",fill="y",padx=8,pady=8)
        self.gtask_btn=tk.Button(toolbar,text="🎯  Завдання",font=("Segoe UI",14,"bold"),bg=CARD_Y,fg=ORANGE,relief="flat",cursor="hand2",padx=14,pady=6,command=self._gtoggle)
        self.gtask_btn.pack(side="left",padx=8)
        self.gscore_lbl=tk.Label(toolbar,text="",font=("Segoe UI",15,"bold"),bg=PANEL,fg=GREEN); self.gscore_lbl.pack(side="left",padx=14)
        self._gnext_btn=mkbtn(toolbar,"▶  Наступне",self._gadvance,bg=BTN_NUM,fg=MUTED,font=("Segoe UI",13,"bold"),w=10,h=1)
        self._gnext_btn.pack(side="right",padx=6); self._gnext_btn.config(state="disabled")
        mkbtn(toolbar,"🗑  Очистити",self._gclear,bg=BTN_NUM,fg=TEXT,font=("Segoe UI",13,"bold"),w=10,h=1).pack(side="right",padx=14)
        ws=tk.Frame(cf,bg=BG); ws.pack(fill="both",expand=True,padx=16,pady=12)
        left=tk.Frame(ws,bg=PANEL,highlightbackground=BORDER,highlightthickness=1)
        left.pack(side="left",fill="both",expand=True,padx=(0,12))
        self.gtask_lbl=tk.Label(left,text="",font=("Segoe UI",18,"bold"),bg=PANEL,fg=ORANGE); self.gtask_lbl.pack(pady=(8,0))
        self.gcanvas=tk.Canvas(left,bg=PANEL,highlightthickness=0)
        self.gcanvas.pack(fill="both",expand=True,padx=10,pady=10)
        self.gcanvas.bind("<Configure>",self._gdraw); self.gcanvas.bind("<Button-1>",self._gclick); self.gcanvas.bind("<B1-Motion>",self._gclick)
        right=tk.Frame(ws,bg=PANEL,highlightbackground=BORDER,highlightthickness=1,width=300)
        right.pack(side="right",fill="y"); right.pack_propagate(False)
        tk.Label(right,text="Звичайний дріб:",font=("Segoe UI",16),bg=PANEL,fg=MUTED).pack(pady=(20,4))
        self.gfrac_f=tk.Frame(right,bg=PANEL); self.gfrac_f.pack(pady=4)
        tk.Label(right,text="Десятковий дріб:",font=("Segoe UI",16),bg=PANEL,fg=MUTED).pack(pady=(20,4))
        self.gdec_lbl=tk.Label(right,text="0",font=("Courier New",64,"bold"),bg=PANEL,fg=RED); self.gdec_lbl.pack(pady=4)
        self.gfeed_lbl=tk.Label(right,text="",font=("Segoe UI",18,"bold"),bg=PANEL,fg=GREEN,wraplength=290,justify="center"); self.gfeed_lbl.pack(pady=12)
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
        if hasattr(self,"_gnext_btn"): self._gnext_btn.config(state="disabled",bg=BTN_NUM,fg=MUTED)
        self._gnew_task()

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
        sz=min(W-2*pad,H-2*pad)
        x0=(W-sz)//2; y0=(H-sz)//2
        self._gx0=x0; self._gy0=y0; self._gsz=sz
        self._cw=sz/cols; self._ch=sz/rows
        fill=self._gfill(); filled=self.gval; total=self._gtotal()

        if self.gmode=="thousandths":
            # ── ВИПРАВЛЕНО: малюємо справжню сітку 25×40 по одній клітинці ──
            cw=self._cw; ch=self._ch
            # Спочатку фон для всіх клітинок
            for i in range(total):
                r=i//cols; c2=i%cols
                x1=x0+c2*cw; y1=y0+r*ch; x2=x1+cw; y2=y1+ch
                color=fill if i<filled else C_EMPTY
                cv.create_rectangle(x1,y1,x2,y2,fill=color,outline="")
            # Тонкі лінії між кожною клітинкою
            for r in range(rows+1):
                y=y0+r*ch
                lw=2 if r%5==0 else 1
                col2=_dk(fill,40) if r%5==0 else BORDER
                cv.create_line(x0,y,x0+sz,y,fill=col2,width=lw)
            for c2 in range(cols+1):
                x=x0+c2*cw
                lw=2 if c2%8==0 else 1
                col2=_dk(fill,40) if c2%8==0 else BORDER
                cv.create_line(x,y0,x,y0+sz,fill=col2,width=lw)
            # Зовнішня рамка
            cv.create_rectangle(x0,y0,x0+sz,y0+sz,outline=_dk(fill,50),width=3)
        elif self.gmode=="tenths":
            for i in range(total):
                r=i//cols; c2=i%cols
                x1=x0+c2*self._cw; y1=y0+r*self._ch
                x2=x1+self._cw;   y2=y1+self._ch
                color=fill if i<filled else C_EMPTY
                border_col=_dk(fill,25) if i<filled else BORDER
                cv.create_rectangle(x1,y1,x2,y2,fill=color,outline=border_col,width=1)
            for r in range(rows+1):
                y=y0+r*self._ch
                cv.create_line(x0,y,x0+sz,y,fill=MUTED,width=2)
            cv.create_line(x0,y0,x0,y0+sz,fill=MUTED,width=2)
            cv.create_line(x0+sz,y0,x0+sz,y0+sz,fill=MUTED,width=2)
        else:  # hundredths
            for i in range(total):
                r=i//cols; c2=i%cols
                x1=x0+c2*self._cw; y1=y0+r*self._ch
                x2=x1+self._cw;   y2=y1+self._ch
                color=fill if i<filled else C_EMPTY
                border_col=_dk(fill,25) if i<filled else BORDER
                cv.create_rectangle(x1,y1,x2,y2,fill=color,outline=border_col,width=1)
            for r in range(rows+1):
                y=y0+r*self._ch; lw=3 if r%10==0 else 1; col2=TEXT if r%10==0 else BORDER
                cv.create_line(x0,y,x0+sz,y,fill=col2,width=lw)
            for c2 in range(cols+1):
                x=x0+c2*self._cw; lw=3 if c2%10==0 else 1; col2=TEXT if c2%10==0 else BORDER
                cv.create_line(x,y0,x,y0+sz,fill=col2,width=lw)

    def _gupdate(self):
        total=self._gtotal(); val=self.gval/total
        for w in self.gfrac_f.winfo_children(): w.destroy()
        frac_w(self.gfrac_f,self.gval,total,PANEL,"big",ACCENT).pack()
        places={10:1,100:2,1000:3}[total]
        self.gdec_lbl.config(text=f"{val:.{places}f}".replace(".",","),fg=RED)

    def _gcheck(self):
        if self.gval==self.gtarget:
            self.glocked=True; self.gscore+=1; self.gtotal+=1
            self.gfeed_lbl.config(text="✅  Правильно!  Натисни «Наступне» →",fg=GREEN)
            self.gscore_lbl.config(text=f"Рахунок: {self.gscore}/{self.gtotal}",fg=GREEN)
            if hasattr(self,"_gnext_btn"): self._gnext_btn.config(state="normal",bg=ACCENT,fg=WHITE)

    # ══ PLACE VALUE ═══════════════════════════════════════════════════════════
    PVNAMES=["Одиниці","Десяті","Соті","Тисячні"]
    PVCOLORS=[TEXT,ACCENT,ACCENT2,GREEN]

    def show_place_value(self):
        self.clear_main(); cf=self.current_frame
        sbar=tk.Frame(cf,bg=PANEL,height=60,highlightbackground=BORDER,highlightthickness=1)
        sbar.pack(fill="x"); sbar.pack_propagate(False)
        tk.Label(sbar,text="Кількість знаків після коми:",font=("Segoe UI",15),bg=PANEL,fg=MUTED).pack(side="left",padx=20)
        self._pv_prec_btns=[]
        for n in [1,2,3]:
            b=tk.Button(sbar,text=str(n),font=("Segoe UI",16,"bold"),bg=BTN_NUM,fg=TEXT,width=3,height=1,relief="flat",cursor="hand2",command=lambda k=n:self._pvset(k))
            b.pack(side="left",padx=6,pady=10); self._pv_prec_btns.append(b)
        ws=tk.Frame(cf,bg=BG); ws.pack(fill="both",expand=True,padx=16,pady=12)
        left=tk.Frame(ws,bg=PANEL,highlightbackground=BORDER,highlightthickness=1,width=500)
        left.pack(side="left",fill="y"); left.pack_propagate(False)
        tk.Label(left,text="Зміни розряди:",font=F_SUB,bg=PANEL,fg=MUTED).pack(anchor="w",padx=20,pady=(14,6))
        self._pv_ctrl=tk.Frame(left,bg=PANEL); self._pv_ctrl.pack(fill="x",padx=16)
        right=tk.Frame(ws,bg=PANEL,highlightbackground=BORDER,highlightthickness=1)
        right.pack(side="right",fill="both",expand=True,padx=(12,0))
        nf=tk.Frame(right,bg=PANEL); nf.pack(expand=True)
        tk.Label(nf,text="Десятковий дріб:",font=("Segoe UI",18),bg=PANEL,fg=MUTED).pack(pady=(0,6))
        self._pv_ncv=tk.Canvas(nf,bg=PANEL,height=120,highlightthickness=0)
        self._pv_ncv.pack(fill="x",padx=30,pady=4)
        tk.Label(nf,text="Як звичайний дріб:",font=("Segoe UI",18),bg=PANEL,fg=MUTED).pack(pady=(16,4))
        self._pv_frow=tk.Frame(nf,bg=PANEL); self._pv_frow.pack()
        tk.Label(nf,text="Читається:",font=("Segoe UI",18),bg=PANEL,fg=MUTED).pack(pady=(16,4))
        self._pv_rlbl=tk.Label(nf,text="",font=("Segoe UI",20,"bold"),bg=PANEL,fg=ACCENT,wraplength=600,justify="center")
        self._pv_rlbl.pack(pady=4)
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
            row=tk.Frame(self._pv_ctrl,bg=BTN_NUM,pady=8,padx=12); row.pack(fill="x",pady=5)
            tk.Label(row,text=self.PVNAMES[i],font=("Segoe UI",16,"bold"),bg=BTN_NUM,fg=color,width=12,anchor="w").pack(side="left")
            def dec(idx=i):self._pvchange(idx,-1)
            def inc(idx=i):self._pvchange(idx,1)
            tk.Button(row,text="−",font=F_CTRL,width=3,bg=PANEL,fg=TEXT,relief="flat",cursor="hand2",command=dec).pack(side="left",padx=8)
            tk.Label(row,text=str(self.pv_digits[i]),font=("Courier New",36,"bold"),bg=BTN_NUM,fg=color,width=2).pack(side="left",padx=10)
            tk.Button(row,text="+",font=F_CTRL,width=3,bg=PANEL,fg=TEXT,relief="flat",cursor="hand2",command=inc).pack(side="left",padx=8)

    def _pvchange(self,idx,delta):
        new=self.pv_digits[idx]+delta
        if new>9: self.pv_digits[idx]=0; (self._pvcarry(idx-1,+1) if idx>0 else None)
        elif new<0:
            if idx>0 and self.pv_digits[idx-1]>0: self.pv_digits[idx]=9; self._pvcarry(idx-1,-1)
            else: pass
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
        W=cv.winfo_width() or 600; H=120
        whole_s=str(self.pv_digits[0]); dec_s="".join(str(self.pv_digits[i]) for i in range(1,self.pv_places+1))
        chars=[(whole_s,self.PVCOLORS[0]),(",",MUTED)]+[(dec_s[i],self.PVCOLORS[i+1]) for i in range(len(dec_s))]
        FONT_D=("Segoe UI",72,"bold"); cw=56; total_w=len(chars)*cw; x=(W-total_w)//2
        for ch,col in chars:
            cv.create_text(x+cw//2,H//2,text=ch,font=FONT_D,fill=col,anchor="center"); x+=cw
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

    # ══ NUMBER LINE ═══════════════════════════════════════════════════════════
    def show_number_line(self):
        self.clear_main(); cf=self.current_frame
        sbar=tk.Frame(cf,bg=PANEL,height=60,highlightbackground=BORDER,highlightthickness=1)
        sbar.pack(fill="x"); sbar.pack_propagate(False)
        tk.Label(sbar,text="📏  Числова пряма",font=("Segoe UI",18,"bold"),bg=PANEL,fg=TEXT).pack(side="left",padx=20)
        # Завдання кнопка
        self._nl_task_btn=tk.Button(sbar,text="🎯  Завдання",font=("Segoe UI",14,"bold"),
            bg=CARD_Y,fg=ORANGE,relief="flat",cursor="hand2",padx=14,pady=6,
            command=self._nl_toggle_task)
        self._nl_task_btn.pack(side="left",padx=16)
        self._nl_task_score_lbl=tk.Label(sbar,text="",font=("Segoe UI",14,"bold"),bg=PANEL,fg=GREEN)
        self._nl_task_score_lbl.pack(side="left",padx=8)

        center=tk.Frame(cf,bg=BG); center.pack(fill="both",expand=True,padx=40,pady=12)

        # Блок завдання
        self._nl_task_frame=tk.Frame(center,bg=CARD_Y,padx=20,pady=10,
            highlightbackground=ORANGE,highlightthickness=2)
        self._nl_task_target_lbl=tk.Label(self._nl_task_frame,text="",
            font=("Segoe UI",20,"bold"),bg=CARD_Y,fg=ORANGE)
        self._nl_task_target_lbl.pack(side="left",padx=(0,20))
        self._nl_task_feed_lbl=tk.Label(self._nl_task_frame,text="",
            font=("Segoe UI",16,"bold"),bg=CARD_Y,fg=GREEN)
        self._nl_task_feed_lbl.pack(side="left")
        self._nl_task_next_btn=tk.Button(self._nl_task_frame,text="▶  Наступне",
            font=("Segoe UI",13,"bold"),bg=ACCENT,fg=WHITE,relief="flat",cursor="hand2",
            padx=12,pady=4,state="disabled",command=self._nl_next_task)
        self._nl_task_next_btn.pack(side="right",padx=8)
        # спочатку сховано
        self._nl_task_frame.pack_forget()

        # Демо-рядок
        tk.Label(center,text="Приклад: A(0,6) і B(1,3)",font=F_SUB,bg=BG,fg=TEXT).pack(anchor="w",pady=(0,6))
        draw_number_line(center,[(0.6,ACCENT,"A (0,6)"),(1.3,RED,"B (1,3)")],lo=0.0,hi=2.0,step=0.1,width=self.SW-120,bg=BG).pack(fill="x")
        tk.Label(center,text="Від 0 відкладаємо 6 десятих → A(0,6).  Від 1 відкладаємо 3 десятих → B(1,3).",font=F_BODY,bg=BG,fg=MUTED).pack(anchor="w",pady=(4,8))
        hline(center,BORDER)
        tk.Label(center,text="🎯  Постав свою точку",font=F_SUB,bg=BG,fg=TEXT).pack(anchor="w",pady=(8,8))

        # ── Точність з переповненням ──────────────────────────────────────────
        self._nl_ones=0; self._nl_tenths=0; self._nl_hunds=0
        self._nl_prec="tenths"
        prec_row=tk.Frame(center,bg=BG); prec_row.pack(anchor="w",pady=(0,6))
        tk.Label(prec_row,text="Точність:",font=F_BODYB,bg=BG,fg=MUTED).pack(side="left",padx=(0,10))
        self._nl_pbtns=[]
        for val2,label2 in [("tenths","Десяті (0,1)"),("hundredths","Соті (0,01)")]:
            b=tk.Button(prec_row,text=label2,font=("Segoe UI",14,"bold"),bg=BTN_NUM,fg=TEXT,relief="flat",cursor="hand2",padx=16,pady=4,command=lambda v=val2:_nlprec(v))
            b.pack(side="left",padx=6); self._nl_pbtns.append((b,val2))

        ctrl_row=tk.Frame(center,bg=BG); ctrl_row.pack(anchor="w",pady=6)

        def _nl_make_ctrl(parent,label,get_fn,set_fn,overflow_fn,underflow_fn,color):
            f=tk.Frame(parent,bg=CARD_B,padx=12,pady=8,highlightbackground=BORDER,highlightthickness=1)
            f.pack(side="left",padx=10)
            tk.Label(f,text=label,font=("Segoe UI",14,"bold"),bg=CARD_B,fg=color).pack(anchor="center")
            inner=tk.Frame(f,bg=CARD_B); inner.pack()
            def dec():
                v=get_fn()
                if v>0: set_fn(v-1)
                else: underflow_fn(); set_fn(9)  # ← лічильник: 0→9
                _nlredraw()
            def inc():
                v=get_fn()
                if v<9: set_fn(v+1)
                else: overflow_fn(); set_fn(0)  # ← лічильник: 9→0
                _nlredraw()
            tk.Button(inner,text="−",font=F_CTRL,width=3,bg=BTN_NUM,fg=TEXT,relief="flat",cursor="hand2",command=dec).pack(side="left",padx=4)
            lbl=tk.Label(inner,text=str(get_fn()),font=("Courier New",36,"bold"),bg=CARD_B,fg=color,width=3); lbl.pack(side="left")
            tk.Button(inner,text="+",font=F_CTRL,width=3,bg=BTN_NUM,fg=TEXT,relief="flat",cursor="hand2",command=inc).pack(side="left",padx=4)
            return lbl

        def _ones_inc(): pass  # переповнення одиниць → нічого (обмежуємо до 9)
        def _ones_dec(): pass
        def _tenth_inc(): # переповнення десятих → +1 до одиниць
            self._nl_ones=min(9,self._nl_ones+1)
        def _tenth_dec(): # недобір десятих → -1 від одиниць
            if self._nl_ones>0: self._nl_ones=self._nl_ones-1
        def _hund_inc():  # переповнення сотих → +1 до десятих
            v=self._nl_tenths+1
            if v>9: self._nl_tenths=0; _tenth_inc()
            else: self._nl_tenths=v
        def _hund_dec():
            if self._nl_tenths>0: self._nl_tenths=self._nl_tenths-1
            else:
                if self._nl_ones>0: self._nl_tenths=9; self._nl_ones-=1

        self._nl_ones_lbl=_nl_make_ctrl(ctrl_row,"Цілі",
            lambda:self._nl_ones, lambda v:setattr(self,"_nl_ones",v),
            _ones_inc, _ones_dec, TEXT)
        self._nl_tenth_lbl=_nl_make_ctrl(ctrl_row,"Десяті",
            lambda:self._nl_tenths, lambda v:setattr(self,"_nl_tenths",v),
            _tenth_inc, _tenth_dec, ACCENT)
        self._nl_hund_frame=tk.Frame(ctrl_row,bg=BG); self._nl_hund_frame.pack(side="left")
        self._nl_hund_lbl=_nl_make_ctrl(self._nl_hund_frame,"Соті",
            lambda:self._nl_hunds, lambda v:setattr(self,"_nl_hunds",v),
            _hund_inc, _hund_dec, ACCENT2)

        disp_row=tk.Frame(center,bg=BG); disp_row.pack(anchor="w",pady=8)
        self._nl_num_lbl=tk.Label(disp_row,text="",font=("Courier New",56,"bold"),bg=BG,fg=RED)
        self._nl_num_lbl.pack(side="left",padx=(0,20))
        self._nl_frac_f=tk.Frame(disp_row,bg=BG); self._nl_frac_f.pack(side="left")
        self._nl_cv_f=tk.Frame(center,bg=BG); self._nl_cv_f.pack(fill="x")

        def _nlredraw():
            prec=self._nl_prec
            ones=max(0,min(9,self._nl_ones))
            tenths=max(0,min(9,self._nl_tenths))
            hunds=max(0,min(9,self._nl_hunds)) if prec=="hundredths" else 0
            self._nl_ones=ones; self._nl_tenths=tenths
            self._nl_ones_lbl.config(text=str(ones))
            self._nl_tenth_lbl.config(text=str(tenths))
            self._nl_hund_lbl.config(text=str(hunds))
            if prec=="hundredths":
                v=round(ones+tenths*0.1+hunds*0.01,2); s=f"{v:.2f}".replace(".",","); step=0.01; nd=int(round(v*100)); dd=100
            else:
                v=round(ones+tenths*0.1,1); s=f"{v:.1f}".replace(".",","); step=0.1; nd=int(round(v*10)); dd=10
            hi=max(10.0,v+1.0); lo=max(0.0,v-1.0) if v>2 else 0.0
            self._nl_num_lbl.config(text=s)
            for w in self._nl_frac_f.winfo_children(): w.destroy()
            wp2=nd//dd; rp=nd%dd
            tk.Label(self._nl_frac_f,text="=  ",font=F_HEAD,bg=BG,fg=MUTED).pack(side="left")
            if wp2>0 and rp>0:
                tk.Label(self._nl_frac_f,text=str(wp2),font=F_FRAC,bg=BG,fg=TEXT).pack(side="left",padx=(0,6))
                frac_w(self._nl_frac_f,rp,dd,BG,"big",ACCENT).pack(side="left")
            elif wp2>0: tk.Label(self._nl_frac_f,text=str(wp2),font=F_FRAC,bg=BG,fg=TEXT).pack(side="left")
            else: frac_w(self._nl_frac_f,rp,dd,BG,"big",ACCENT).pack(side="left")
            for w in self._nl_cv_f.winfo_children(): w.destroy()
            marks=[(v,GREEN,f"P ({s})")]
            # Якщо режим завдання — додаємо мітку цілі
            if self.nl_task_mode and not self.nl_task_locked:
                pass
            draw_number_line(self._nl_cv_f,marks,lo=lo,hi=hi,step=step,width=self.SW-120,bg=BG).pack(fill="x")
            # Перевірка завдання
            if self.nl_task_mode and not self.nl_task_locked:
                target=self.nl_task_target
                if abs(v-target)<(0.005 if prec=="hundredths" else 0.05):
                    self.nl_task_locked=True
                    self.nl_task_score+=1; self.nl_task_total+=1
                    self._nl_task_feed_lbl.config(text=f"✅  Правильно!  {s} = {str(target).replace('.',',')}",fg=GREEN)
                    self._nl_task_score_lbl.config(text=f"Рахунок: {self.nl_task_score}/{self.nl_task_total}")
                    self._nl_task_next_btn.config(state="normal")

        def _nlprec(val2):
            self._nl_prec=val2
            for b,v in self._nl_pbtns:
                b.config(bg=ACCENT if v==val2 else BTN_NUM,fg=WHITE if v==val2 else TEXT)
            if val2=="hundredths": self._nl_hund_frame.pack(side="left")
            else: self._nl_hund_frame.pack_forget(); self._nl_hunds=0
            _nlredraw()

        self._nlredraw_fn=_nlredraw
        _nlprec("tenths")

    def _nl_toggle_task(self):
        self.nl_task_mode=not self.nl_task_mode
        if self.nl_task_mode:
            self._nl_task_btn.config(bg=RED,fg=WHITE,text="⏹  Зупинити")
            self.nl_task_score=0; self.nl_task_total=0
            self._nl_task_frame.pack(fill="x",pady=(0,8))
            self._nl_task_score_lbl.config(text="Рахунок: 0/0")
            self._nl_next_task()
        else:
            self._nl_task_btn.config(bg=CARD_Y,fg=ORANGE,text="🎯  Завдання")
            self._nl_task_frame.pack_forget()
            self._nl_task_score_lbl.config(text="")
            self.nl_task_locked=False

    def _nl_next_task(self):
        self.nl_task_locked=False
        prec=self._nl_prec
        if prec=="hundredths":
            target=round(random.randint(1,99)/100,2)
        else:
            target=round(random.randint(1,19)/10,1)
        self.nl_task_target=target
        ts=f"{target:.2f}".replace(".",",") if prec=="hundredths" else f"{target:.1f}".replace(".",",")
        self._nl_task_target_lbl.config(text=f"📋  Постав точку:  {ts}")
        self._nl_task_feed_lbl.config(text="")
        self._nl_task_next_btn.config(state="disabled")
        if self.nl_task_total>0:
            self.nl_task_total  # вже збільшено при правильній відповіді
        if hasattr(self,"_nlredraw_fn"): self._nlredraw_fn()

    # ══ ZEROS DEMO ════════════════════════════════════════════════════════════
    def show_zeros_demo(self):
        self.clear_main(); cf=self.current_frame
        center=tk.Frame(cf,bg=BG); center.pack(expand=True)
        tk.Label(center,text="Зв'язок: знаки після коми ↔ нулі у знаменнику",font=F_TITLE,bg=BG,fg=TEXT).pack(pady=(16,4))
        tk.Label(center,text="Натискай  «+»  і  «−»  щоб змінювати кількість знаків після коми",font=F_BODY,bg=BG,fg=MUTED).pack(pady=(0,16))
        ctrl_row=tk.Frame(center,bg=BG); ctrl_row.pack(pady=10)
        def dec_p():
            if self.zdemo_places>1: self.zdemo_places-=1; _zrefresh()
        def inc_p():
            if self.zdemo_places<5: self.zdemo_places+=1; _zrefresh()
        tk.Button(ctrl_row,text="−  Менше знаків",font=("Segoe UI",18,"bold"),bg=BTN_NUM,fg=TEXT,relief="flat",cursor="hand2",padx=20,pady=8,command=dec_p).pack(side="left",padx=16)
        self._zplbl=tk.Label(ctrl_row,text="",font=("Segoe UI",22,"bold"),bg=BG,fg=ACCENT2,width=20); self._zplbl.pack(side="left")
        tk.Button(ctrl_row,text="+  Більше знаків",font=("Segoe UI",18,"bold"),bg=BTN_NUM,fg=TEXT,relief="flat",cursor="hand2",padx=20,pady=8,command=inc_p).pack(side="left",padx=16)
        vis_f=tk.Frame(center,bg=PANEL,highlightbackground=BORDER,highlightthickness=1,padx=40,pady=28)
        vis_f.pack(padx=60,pady=16,fill="x")
        self._zdec_f=tk.Frame(vis_f,bg=PANEL); self._zdec_f.pack(pady=(0,8))
        tk.Label(vis_f,text="⟷",font=("Segoe UI",48),bg=PANEL,fg=MUTED).pack()
        self._zfrac_f=tk.Frame(vis_f,bg=PANEL); self._zfrac_f.pack(pady=8)
        self._zexp=tk.Label(vis_f,text="",font=("Segoe UI",18),bg=PANEL,fg=TEXT,justify="center",wraplength=900); self._zexp.pack(pady=8)
        mkbtn(center,"🎲  Нове число",lambda:_zrefresh(True),bg=TEAL,w=14,h=2).pack(pady=8)

        def _zrefresh(new_num=False):
            # ── ВИПРАВЛЕНО: завжди оновлюємо digits до поточної кількості знаків
            if new_num or not self._zdemo_digits:
                self._zdemo_digits=[str(random.randint(0,9)) for _ in range(5)]
                if all(d=="0" for d in self._zdemo_digits):
                    self._zdemo_digits[0]=str(random.randint(1,9))
            # Обрізаємо або доповнюємо digits до поточної довжини
            while len(self._zdemo_digits)<5:
                self._zdemo_digits.append(str(random.randint(0,9)))
            digits=self._zdemo_digits[:self.zdemo_places]
            dec_str="0,"+"".join(digits)
            suffix={1:"знак",2:"знаки",3:"знаки",4:"знаки"}.get(self.zdemo_places,"знаків")
            self._zplbl.config(text=f"{self.zdemo_places}  {suffix}  після коми")
            for w in self._zdec_f.winfo_children(): w.destroy()
            fn=("Courier New",56,"bold"); ch_w=40; H=90
            all_ch=[(c,TEXT if i<2 else C_DIGIT) for i,c in enumerate("0,"+("".join(digits)))]
            W2=len(all_ch)*ch_w+20
            cv=tk.Canvas(self._zdec_f,bg=PANEL,width=W2,height=H,highlightthickness=0)
            cv.pack(); x=10
            for ch,col in all_ch:
                cv.create_text(x+ch_w//2,H//2,text=ch,font=fn,fill=col,anchor="center"); x+=ch_w
            for w in self._zfrac_f.winfo_children(): w.destroy()
            # ── ВИПРАВЛЕНО: чисельник і знаменник відповідають поточній кількості знаків
            numer=int("".join(digits))  # цифри поточної точності
            denom=10**self.zdemo_places
            denom_str="1"+"0"*self.zdemo_places
            draw_frac_canvas(self._zfrac_f,str(numer),denom_str,PANEL,C_DIGIT,C_ZERO,ACCENT).pack(side="left")
            ann=tk.Frame(self._zfrac_f,bg=PANEL); ann.pack(side="left",padx=28)
            s1="цифра" if self.zdemo_places==1 else ("цифри" if self.zdemo_places<5 else "цифр")
            s2="нуль" if self.zdemo_places==1 else ("нулі" if self.zdemo_places<5 else "нулів")
            tk.Label(ann,text=f"← {self.zdemo_places} {s1} після коми",font=("Segoe UI",16,"bold"),bg=PANEL,fg=C_DIGIT).pack(anchor="w")
            tk.Label(ann,text=f"← {self.zdemo_places} {s2} у знаменнику",font=("Segoe UI",16,"bold"),bg=PANEL,fg=C_ZERO).pack(anchor="w")
            pnames={1:"десяті",2:"соті",3:"тисячні",4:"десятитисячні",5:"стотисячні"}
            self._zexp.config(text=f"У числі  {dec_str}  є  {self.zdemo_places} цифр(и) після коми.\nТому у знаменнику «1» та {self.zdemo_places} нул(ів) → {denom_str}.\nЧитаємо: «нуль цілих {numer} {pnames.get(self.zdemo_places,'')}»")

        _zrefresh(True)

    # ══ TRAINER A: decimal → fraction ════════════════════════════════════════
    def show_trainer_a(self):
        self.clear_main(); self.mode="ta"; cf=self.current_frame
        sbar=tk.Frame(cf,bg=PANEL,height=56,highlightbackground=BORDER,highlightthickness=1)
        sbar.pack(fill="x"); sbar.pack_propagate(False)
        self.ta_score_lbl=tk.Label(sbar,text=self._ta_st(),font=F_SCORE,bg=PANEL,fg=GREEN)
        self.ta_score_lbl.pack(side="left",padx=30)
        tk.Label(sbar,text="Запиши десятковий дріб як звичайний  (2 кроки)",font=("Segoe UI",15,"bold"),bg=PANEL,fg=MUTED).pack(side="left",padx=10)
        tk.Label(sbar,text="Цифри після коми = чисельник.  Нулі знаменника = кількість знаків.",font=("Segoe UI",13,"bold"),bg=PANEL,fg=ACCENT).pack(side="right",padx=20)
        center=tk.Frame(cf,bg=BG); center.pack(expand=True)
        banner=tk.Frame(center,bg=CARD_B,padx=18,pady=8,highlightbackground=ACCENT,highlightthickness=2); banner.pack(fill="x",padx=40,pady=(10,4))
        tk.Label(banner,text="📋  Крок 1 → введи ЧИСЕЛЬНИК і натисни «Перевірити»\n     Крок 2 → введи ЗНАМЕННИК і натисни «Перевірити»",font=("Segoe UI",14,"bold"),bg=CARD_B,fg=ACCENT,justify="center").pack()
        tf=tk.Frame(center,bg=PANEL,highlightbackground=BORDER,highlightthickness=1,padx=28,pady=18); tf.pack(pady=(8,4))
        tk.Label(tf,text="Запиши як звичайний дріб:",font=F_SUB,bg=PANEL,fg=TEXT).pack()
        self.ta_task_lbl=tk.Label(tf,text="",font=("Courier New",72,"bold"),bg=PANEL,fg=RED); self.ta_task_lbl.pack(pady=8)
        sr=tk.Frame(center,bg=BG); sr.pack(pady=6); self.ta_steps=[]
        for label,desc in [("Крок 1","Чисельник = ?"),("Крок 2","Знаменник = ?")]:
            box=tk.Frame(sr,bg=BTN_NUM,padx=18,pady=10,highlightbackground=BORDER,highlightthickness=1,width=280)
            box.pack(side="left",padx=10); box.pack_propagate(False)
            tk.Label(box,text=label,font=("Segoe UI",18,"bold"),bg=BTN_NUM,fg=MUTED).pack()
            lbl=tk.Label(box,text=desc,font=("Segoe UI",18),bg=BTN_NUM,fg=MUTED); lbl.pack()
            self.ta_steps.append((box,lbl))
        self.ta_step1=tk.Label(center,text="",font=("Segoe UI",17,"bold"),bg=BG,fg=GREEN); self.ta_step1.pack(pady=2)
        self.ta_step_lbl=tk.Label(center,text="",font=F_SUB,bg=BG,fg=ACCENT); self.ta_step_lbl.pack(pady=4)
        inp_f=tk.Frame(center,bg=BTN_NUM,highlightbackground=ACCENT,highlightthickness=2,padx=14,pady=6); inp_f.pack(pady=4)
        tk.Label(inp_f,text="Відповідь:",font=F_BODYB,bg=BTN_NUM,fg=MUTED).pack(side="left")
        self.ta_inp_lbl=tk.Label(inp_f,text="",font=("Courier New",44,"bold"),bg=BTN_NUM,fg=ACCENT,width=8); self.ta_inp_lbl.pack(side="left",padx=10)
        self.ta_feed=tk.Label(center,text="",font=("Segoe UI",16),bg=BG,fg=ORANGE,wraplength=700,justify="center"); self.ta_feed.pack(pady=4)
        build_numpad(center,self._ta_key).pack(pady=6)
        act=tk.Frame(center,bg=BG); act.pack(pady=8)
        self.ta_check=mkbtn(act,"✔  Перевірити",self._ta_check,bg=GREEN,w=14,h=2); self.ta_check.pack(side="left",padx=10)
        mkbtn(act,"▶  Наступне",self._ta_new,bg=ACCENT,w=12,h=2).pack(side="left",padx=10)
        self._ta_new()

    def _ta_st(self): return f"Правильно: {self.ta_score}  /  Завдань: {self.ta_att}"
    def _ta_new(self):
        places=random.randint(1,4); denom=10**places; numer=random.randint(1,denom-1)
        val=numer/denom; dec=f"{val:.{places}f}".replace(".",",")
        self.ta_dec=dec; self.ta_n=numer; self.ta_d=denom
        self.ta_inp_n=""; self.ta_inp_d=""; self.ta_active="n"; self.ta_n_done=False; self.ta_att+=1
        if self.ta_task_lbl: self.ta_task_lbl.config(text=dec)
        if self.ta_step1: self.ta_step1.config(text="")
        if self.ta_inp_lbl: self.ta_inp_lbl.config(text="",fg=ACCENT)
        if self.ta_feed: self.ta_feed.config(text="")
        if self.ta_check: self.ta_check.config(state="normal",bg=GREEN)
        if self.ta_step_lbl: self.ta_step_lbl.config(text="Крок 1:   Введи ЧИСЕЛЬНИК  (цифри після коми)",fg=ACCENT)
        self._ta_hl(1)
        if self.ta_score_lbl: self.ta_score_lbl.config(text=self._ta_st())

    def _ta_hl(self,step):
        for i,(box,lbl) in enumerate(self.ta_steps):
            act=i+1==step
            box.config(bg=CARD_B if act else BTN_NUM,highlightbackground=ACCENT if act else BORDER,highlightthickness=2 if act else 1)
            lbl.config(bg=CARD_B if act else BTN_NUM,fg=ACCENT if act else MUTED)
            box.winfo_children()[0].config(bg=CARD_B if act else BTN_NUM,fg=ACCENT if act else MUTED)

    def _ta_key(self,ch):
        if ch.isdigit():
            if self.ta_active=="n" and len(self.ta_inp_n)<6: self.ta_inp_n+=ch
            elif self.ta_active=="d" and len(self.ta_inp_d)<8: self.ta_inp_d+=ch
        elif ch=="⌫": self.ta_inp_n=self.ta_inp_n[:-1] if self.ta_active=="n" else self.ta_inp_d[:-1]
        elif ch=="C":
            if self.ta_active=="n": self.ta_inp_n=""
            else: self.ta_inp_d=""
        cur=self.ta_inp_n if self.ta_active=="n" else self.ta_inp_d
        if self.ta_inp_lbl: self.ta_inp_lbl.config(text=cur)

    def _ta_check(self):
        cur=self.ta_inp_n if self.ta_active=="n" else self.ta_inp_d
        if not cur.strip():
            if self.ta_feed: self.ta_feed.config(text="⚠️  Введіть число!",fg=ORANGE); return
        val=int(cur)
        if self.ta_active=="n":
            if val==self.ta_n:
                self.ta_active="d"; self.ta_n_done=True
                if self.ta_step1: self.ta_step1.config(text=f"✅  Крок 1: Чисельник = {val}   (правильно!)",fg=GREEN)
                dec_after=len(self.ta_dec.split(",")[1])
                if self.ta_feed: self.ta_feed.config(text=f"Тепер введи ЗНАМЕННИК.  {dec_after} цифр → знаменник = 1{'0'*dec_after}",fg=GREEN)
                if self.ta_step_lbl: self.ta_step_lbl.config(text=f"Крок 2:   Введи ЗНАМЕННИК  (1 і {dec_after} нулів)",fg=ACCENT2)
                if self.ta_inp_lbl: self.ta_inp_lbl.config(text="",fg=ACCENT2); self.ta_inp_d=""
                self._ta_hl(2)
            else:
                if self.ta_feed: self.ta_feed.config(text=f"❌  Чисельник не {val}.  Цифри після коми = чисельник.",fg=RED)
        else:
            if val==self.ta_d:
                self.ta_score+=1
                if self.ta_check: self.ta_check.config(state="disabled",bg=BTN_NUM)
                if self.ta_feed: self.ta_feed.config(text=f"🎉  Чудово!   {self.ta_dec}  =  {self.ta_n}/{self.ta_d}",fg=GREEN)
            else:
                places=len(self.ta_dec.split(",")[1])
                if self.ta_feed: self.ta_feed.config(text=f"❌  Знаменник не {val}.  {places} цифр → 1{'0'*places}",fg=RED)
        if self.ta_score_lbl: self.ta_score_lbl.config(text=self._ta_st())

    # ══ TRAINER B: fraction → decimal  (ПОВНІСТЮ ПЕРЕРОБЛЕНО) ════════════════
    def show_trainer_b(self):
        self.clear_main(); self.mode="tb"; cf=self.current_frame

        # ── Панель рахунку
        sbar=tk.Frame(cf,bg=PANEL,height=56,highlightbackground=BORDER,highlightthickness=1)
        sbar.pack(fill="x"); sbar.pack_propagate(False)
        self.tb_score_lbl=tk.Label(sbar,text=self._tb_st(),font=F_SCORE,bg=PANEL,fg=GREEN)
        self.tb_score_lbl.pack(side="left",padx=30)
        tk.Label(sbar,text="Запиши дріб як десятковий",font=("Segoe UI",15,"bold"),bg=PANEL,fg=MUTED).pack(side="left",padx=10)
        tk.Label(sbar,text="Нулі знаменника → цифри після коми",font=("Segoe UI",13,"bold"),bg=PANEL,fg=ACCENT2).pack(side="right",padx=24)

        # ── Головний вміст: ліво=завдання, право=нумпад
        main=tk.Frame(cf,bg=BG); main.pack(fill="both",expand=True,padx=20,pady=12)

        left_col=tk.Frame(main,bg=BG); left_col.pack(side="left",fill="both",expand=True)
        right_col=tk.Frame(main,bg=BG,width=280); right_col.pack(side="right",fill="y",padx=(16,0)); right_col.pack_propagate(False)

        # ── Ліва колонка: завдання + введення
        # Блок завдання (дріб великий)
        task_outer=tk.Frame(left_col,bg=PANEL,highlightbackground=BORDER,highlightthickness=1,padx=28,pady=18)
        task_outer.pack(fill="x",pady=(0,10))
        tk.Label(task_outer,text="Запиши як десятковий дріб:",font=F_SUB,bg=PANEL,fg=TEXT).pack(anchor="w")

        # Два рядки: великий дріб зліва + підказка
        task_row=tk.Frame(task_outer,bg=PANEL); task_row.pack(anchor="w",pady=8)

        # Великий дріб-canvas (чисельник над знаменником)
        self.tb_task_f=tk.Frame(task_row,bg=PANEL); self.tb_task_f.pack(side="left",padx=(0,30))
        self.tb_hint=tk.Label(task_row,text="",font=("Segoe UI",16),bg=PANEL,fg=MUTED,justify="left")
        self.tb_hint.pack(side="left",anchor="center")

        # ── Поле введення (наочний вигляд: ціла + кома + цифри)
        inp_outer=tk.Frame(left_col,bg=CARD_B,padx=20,pady=14,highlightbackground=ACCENT2,highlightthickness=2)
        inp_outer.pack(fill="x",pady=(0,8))
        tk.Label(inp_outer,text="Твоя відповідь:",font=("Segoe UI",15,"bold"),bg=CARD_B,fg=ACCENT2).pack(anchor="w",pady=(0,6))

        inp_display=tk.Frame(inp_outer,bg=CARD_B); inp_display.pack(anchor="w")
        # Відображення: [ціла частина][,][цифри] — живе оновлення
        self.tb_whole_lbl=tk.Label(inp_display,text="",font=("Courier New",56,"bold"),bg=CARD_B,fg=TEXT)
        self.tb_whole_lbl.pack(side="left")
        self.tb_comma_lbl=tk.Label(inp_display,text=",",font=("Courier New",56,"bold"),bg=CARD_B,fg=MUTED)
        self.tb_comma_lbl.pack(side="left")
        self.tb_inp_lbl=tk.Label(inp_display,text="",font=("Courier New",56,"bold"),bg=CARD_B,fg=RED,width=6,anchor="w")
        self.tb_inp_lbl.pack(side="left")
        self.tb_cursor_lbl=tk.Label(inp_display,text="▮",font=("Courier New",56,"bold"),bg=CARD_B,fg=ACCENT2)
        self.tb_cursor_lbl.pack(side="left")

        # Підказка про кількість цифр
        self.tb_slots_lbl=tk.Label(inp_outer,text="",font=("Segoe UI",14),bg=CARD_B,fg=MUTED)
        self.tb_slots_lbl.pack(anchor="w",pady=(4,0))

        self.tb_feed=tk.Label(left_col,text="",font=("Segoe UI",16),bg=BG,fg=ORANGE,wraplength=700,justify="center")
        self.tb_feed.pack(pady=4)

        # ── Кнопки дій
        act=tk.Frame(left_col,bg=BG); act.pack(pady=6)
        self.tb_check=mkbtn(act,"✔  Перевірити",self._tb_check,bg=GREEN,w=14,h=2)
        self.tb_check.pack(side="left",padx=10)
        mkbtn(act,"▶  Наступне",self._tb_new,bg=ACCENT2,w=12,h=2).pack(side="left",padx=10)

        # ── Права колонка: нумпад
        tk.Label(right_col,text="Клавіатура",font=("Segoe UI",15,"bold"),bg=BG,fg=MUTED).pack(pady=(8,4))
        build_numpad(right_col,self._tb_key,bg=BG).pack(pady=4)

        self._tb_new()

    def _tb_st(self): return f"Правильно: {self.tb_score}  /  Завдань: {self.tb_att}"

    def _tb_new(self):
        # ── ВИПРАВЛЕНО: включаємо цілі числа ──
        # Вибираємо тип: дріб < 1, дріб > 1 (змішане), або ціле (рідше)
        task_type=random.choice(["pure_frac","mixed","mixed","whole"])
        if task_type=="whole":
            # ціле число, знаменник = 10^k, чисельник = кратне знаменнику
            places=random.randint(1,3); denom=10**places
            whole_part=random.randint(1,9)
            numer=whole_part*denom; whole_val=whole_part
            frac_part=0
        elif task_type=="pure_frac":
            places=random.randint(1,4); denom=10**places
            numer=random.randint(1,denom-1); whole_val=0
            frac_part=numer
        else:  # mixed
            places=random.randint(1,3); denom=10**places
            whole_val=random.randint(1,9)
            frac_part=random.randint(1,denom-1)
            numer=whole_val*denom+frac_part

        val=numer/denom
        dec_str=f"{val:.{places}f}".replace(".",",")
        self.tb_n=numer; self.tb_d=denom; self.tb_whole=whole_val
        self.tb_ans=dec_str.split(",")[1]  # тільки дробова частина
        self.tb_whole_ans=str(whole_val)
        self.tb_inp=""; self.tb_att+=1; self.tb_dec_places=places

        # Великий дріб
        for w in self.tb_task_f.winfo_children(): w.destroy()
        fn_big=("Courier New",52,"bold")
        # Малюємо великий дріб canvas
        ns=str(numer); ds=str(denom)
        bw=max(len(ns),len(ds))*38+24
        cv=tk.Canvas(self.tb_task_f,bg=PANEL,width=bw,height=130,highlightthickness=0)
        cv.pack()
        cv.create_text(bw//2,32,text=ns,font=fn_big,fill=C_DIGIT,anchor="center")
        cv.create_line(4,66,bw-4,66,fill=ACCENT,width=4)
        cv.create_text(bw//2,100,text=ds,font=fn_big,fill=C_ZERO,anchor="center")

        z=places
        s2="нуль" if z==1 else ("нулі" if z<5 else "нулів")
        s3="цифра" if z==1 else ("цифри" if z<5 else "цифр")
        hint_text=f"Знаменник {denom}\n→ {z} {s2}\n→ {z} {s3} після коми"
        if whole_val>0:
            hint_text+=f"\nЦіла частина: {whole_val}"
        if self.tb_hint: self.tb_hint.config(text=hint_text)

        # Оновлюємо відображення
        if self.tb_whole_lbl: self.tb_whole_lbl.config(text=str(whole_val))
        if self.tb_inp_lbl: self.tb_inp_lbl.config(text="",fg=RED)
        if self.tb_cursor_lbl: self.tb_cursor_lbl.config(text="▮")
        if self.tb_slots_lbl:
            slots="_"*places
            self.tb_slots_lbl.config(text=f"Введи {places} цифр(и) після коми:  {whole_val},{slots}")
        if self.tb_feed: self.tb_feed.config(text="")
        if self.tb_check: self.tb_check.config(state="normal",bg=GREEN)
        if self.tb_score_lbl: self.tb_score_lbl.config(text=self._tb_st())

    def _tb_key(self,ch):
        places=self.tb_dec_places
        if ch.isdigit():
            if len(self.tb_inp)<places:
                self.tb_inp+=ch
                if self.tb_inp_lbl: self.tb_inp_lbl.config(text=self.tb_inp)
                # Якщо введено достатньо цифр — автофокус (курсор зникає)
                if len(self.tb_inp)==places:
                    if self.tb_cursor_lbl: self.tb_cursor_lbl.config(text="")
        elif ch=="⌫":
            self.tb_inp=self.tb_inp[:-1]
            if self.tb_inp_lbl: self.tb_inp_lbl.config(text=self.tb_inp)
            if self.tb_cursor_lbl: self.tb_cursor_lbl.config(text="▮")
        elif ch=="C":
            self.tb_inp=""
            if self.tb_inp_lbl: self.tb_inp_lbl.config(text="")
            if self.tb_cursor_lbl: self.tb_cursor_lbl.config(text="▮")

    def _tb_check(self):
        if not self.tb_inp:
            if self.tb_feed: self.tb_feed.config(text="⚠️  Введіть цифри!",fg=ORANGE); return
        places=self.tb_dec_places; padded=self.tb_inp.zfill(places)
        if padded==self.tb_ans:
            self.tb_score+=1
            if self.tb_check: self.tb_check.config(state="disabled",bg=BTN_NUM)
            if self.tb_inp_lbl: self.tb_inp_lbl.config(fg=GREEN)
            if self.tb_cursor_lbl: self.tb_cursor_lbl.config(text="")
            whole=self.tb_whole
            result=f"{whole},{self.tb_ans}"
            if self.tb_feed: self.tb_feed.config(text=f"🎉  Правильно!   {self.tb_n}/{self.tb_d}  =  {result}",fg=GREEN)
        else:
            if self.tb_feed:
                self.tb_feed.config(text=f"❌  Не вірно.  Потрібно {places} цифр після коми.  Правильно: «{self.tb_whole},{self.tb_ans}»",fg=RED)
        if self.tb_score_lbl: self.tb_score_lbl.config(text=self._tb_st())

if __name__=="__main__":
    App().mainloop()
