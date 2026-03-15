import tkinter as tk
import math, random

# ─── Palette (light, high-contrast) ──────────────────────────────────────────
BG       = "#f0f4f8"
PANEL    = "#ffffff"
CARD     = "#e8edf2"
HDR_BG   = "#1a3a5c"
HDR_FG   = "#ffffff"
ACCENT   = "#1a6faf"   # blue  – first triangle / ABCD
ACCENT2  = "#b5360a"   # rust  – second triangle / KLMN
GOLD     = "#8a5c00"
GREEN    = "#1a7a3c"
RED      = "#c0190e"
TEXT     = "#0d1b2a"
MUTED    = "#4a5568"
WHITE    = "#ffffff"
BTN_BG   = "#d0d8e4"
BTN_HOV  = "#b0bcce"
GREEN_BG = "#c6f0d4"
RED_BG   = "#fad4d2"
LBL_CLR  = "#1a4f8a"   # number labels
DIV      = "#9ab0c8"
TC1      = "#d97000"   # tick / arc colour – triangle 1
TC2      = "#1a7a3c"   # tick / arc colour – triangle 2

# ─── Geometry helpers ─────────────────────────────────────────────────────────

def tri_from_sides(a, b, c):
    if a+b<=c or a+c<=b or b+c<=a: return None
    cosB = max(-1.0, min(1.0, (a*a+c*c-b*b)/(2.0*a*c)))
    Cx = a - c*cosB
    Cy = -c*math.sqrt(max(0.0, 1.0-cosB**2))
    return [(0.0,0.0),(float(a),0.0),(Cx,Cy)]

def tri_from_angles(A, B, C, base=100.0):
    ra,rb,rc = map(math.radians,[A,B,C])
    sinC = math.sin(rc)
    if sinC < 1e-9: return None
    b = base*math.sin(rb)/sinC
    return [(0.0,0.0),(base,0.0),(b*math.cos(ra),-b*math.sin(ra))]

def fit_poly(poly, cx, cy, bw, bh, margin=24):
    xs=[p[0] for p in poly]; ys=[p[1] for p in poly]
    W=max(xs)-min(xs) or 1; H=max(ys)-min(ys) or 1
    s=min((bw-margin*2)/W,(bh-margin*2)/H)
    bx=(max(xs)+min(xs))/2; by=(max(ys)+min(ys))/2
    return [(cx+(x-bx)*s,cy+(y-by)*s) for x,y in poly], s

def max_scale(poly, bw, bh, margin=24):
    """Maximum scale that fits poly in box bw×bh."""
    xs=[p[0] for p in poly]; ys=[p[1] for p in poly]
    W=max(xs)-min(xs) or 1; H=max(ys)-min(ys) or 1
    return min((bw-margin*2)/W,(bh-margin*2)/H)

def place_poly(poly, cx, cy, scale):
    """Centre poly at (cx,cy) with given scale (no auto-scale)."""
    xs=[p[0] for p in poly]; ys=[p[1] for p in poly]
    bx=(max(xs)+min(xs))/2; by=(max(ys)+min(ys))/2
    return [(cx+(x-bx)*scale, cy+(y-by)*scale) for x,y in poly]

def rotate_poly(poly, deg):
    cx=sum(p[0] for p in poly)/len(poly)
    cy=sum(p[1] for p in poly)/len(poly)
    r=math.radians(deg); ca,sa=math.cos(r),math.sin(r)
    return [(cx+(x-cx)*ca-(y-cy)*sa,cy+(x-cx)*sa+(y-cy)*ca) for x,y in poly]

def side_label_pos(p1, p2, off=22):
    """Point offset perpendicularly from segment midpoint (outward from triangle)."""
    mx,my=(p1[0]+p2[0])/2,(p1[1]+p2[1])/2
    # perpendicular direction
    ang=math.atan2(p2[1]-p1[1],p2[0]-p1[0])+math.pi/2
    return mx+off*math.cos(ang), my+off*math.sin(ang)

def angle_label_pos(v, a, b, off=36):
    """Point along angle bisector, far enough from vertex."""
    d1=(a[0]-v[0],a[1]-v[1]); l1=math.hypot(*d1) or 1
    d2=(b[0]-v[0],b[1]-v[1]); l2=math.hypot(*d2) or 1
    u1=(d1[0]/l1,d1[1]/l1); u2=(d2[0]/l2,d2[1]/l2)
    bx=u1[0]+u2[0]; by=u1[1]+u2[1]; bl=math.hypot(bx,by)
    if bl<1e-9: bx,by,bl=-u1[1],u1[0],1.0
    return v[0]+off*bx/bl, v[1]+off*by/bl

def valid_sides():
    while True:
        s=sorted([random.randint(3,14) for _ in range(3)])
        if s[0]+s[1]>s[2]: return s

def valid_angles():
    while True:
        a=random.randint(28,110); b=random.randint(28,110); c=180-a-b
        if 20<c<130: return [a,b,c]

# ─── App ──────────────────────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("§ 24 — Рівність фігур")
        self.configure(bg=BG)
        self.attributes("-fullscreen",True)
        self.bind("<Escape>",    lambda e: self.attributes("-fullscreen",False))
        self.bind("<Key>",       self._on_key)
        self.bind("<Return>",    lambda e: self._check())
        self.bind("<BackSpace>", lambda e: self._numpad("⌫"))
        self.bind("<Delete>",    lambda e: self._numpad("C"))
        self.SW=self.winfo_screenwidth(); self.SH=self.winfo_screenheight()
        self.mode="theory"; self.task=None; self.phase="answer"
        self.inp=""; self.score=self.total=0; self.ans_mode="number"
        self._build_chrome()
        self.show_theory()

    # ── Chrome ────────────────────────────────────────────────────────────────
    def _build_chrome(self):
        hdr=tk.Frame(self,bg=HDR_BG,height=68)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr,text="§ 24",bg=HDR_BG,fg="#7ecbff",
                 font=("Georgia",22,"bold")).pack(side="left",padx=(28,6),pady=12)
        tk.Label(hdr,text="Рівність фігур",bg=HDR_BG,fg=HDR_FG,
                 font=("Georgia",22)).pack(side="left")
        tk.Button(hdr,text="✕",bg=HDR_BG,fg="#aabbcc",bd=0,
                  font=("Segoe UI",18),activebackground=HDR_BG,
                  activeforeground=RED,command=self.destroy).pack(side="right",padx=20)
        nav=tk.Frame(self,bg=PANEL,height=44)
        nav.pack(fill="x"); nav.pack_propagate(False)
        for txt,cmd in [("  Теорія  ",self.show_theory),("  Тренажер  ",self.show_trainer)]:
            tk.Button(nav,text=txt,bg=PANEL,fg=MUTED,bd=0,
                      font=("Segoe UI",13,"bold"),cursor="hand2",
                      activebackground=CARD,activeforeground=ACCENT,
                      command=cmd).pack(side="left",padx=6,pady=6)
        tk.Frame(self,bg=ACCENT,height=3).pack(fill="x")
        self.body=tk.Frame(self,bg=BG)
        self.body.pack(fill="both",expand=True)

    def _clear(self):
        for w in self.body.winfo_children(): w.destroy()

    # ── Theory ────────────────────────────────────────────────────────────────
    def show_theory(self):
        self._clear(); self.mode="theory"
        wrap=self.SW-160
        sf=tk.Frame(self.body,bg=BG); sf.pack(fill="both",expand=True)
        cs=tk.Canvas(sf,bg=BG,highlightthickness=0)
        sb=tk.Scrollbar(sf,orient="vertical",command=cs.yview)
        cs.configure(yscrollcommand=sb.set)
        sb.pack(side="right",fill="y"); cs.pack(side="left",fill="both",expand=True)
        inner=tk.Frame(cs,bg=BG)
        wid=cs.create_window((0,0),window=inner,anchor="nw")
        cs.bind("<Configure>",lambda e: cs.itemconfig(wid,width=e.width))
        inner.bind("<Configure>",lambda e: cs.configure(scrollregion=cs.bbox("all")))
        cs.bind_all("<MouseWheel>",lambda e: cs.yview_scroll(-1*(e.delta//120),"units"))
        f=inner; px=70

        tk.Label(f,text="§ 24. Рівність фігур",bg=BG,fg=HDR_BG,
                 font=("Georgia",32,"bold"),anchor="w").pack(fill="x",padx=px,pady=(28,8))

        def rule(title, body):
            tk.Label(f,text=title,bg=BG,fg=GOLD,font=("Segoe UI",14,"bold"),anchor="w"
                     ).pack(fill="x",padx=px,pady=(16,2))
            tk.Label(f,text=body,bg=BG,fg=TEXT,font=("Segoe UI",14),
                     justify="left",wraplength=wrap,anchor="w"
                     ).pack(fill="x",padx=px,pady=(0,2))

        rule("Означення",
             "Дві фігури називають між собою рівними, якщо при накладанні одна на одну вони збігаються.")
        rule("Рівні відрізки",
             "Відрізки рівні, якщо мають однакову довжину.\n"
             "AB = CD  ⟺  |AB| = |CD|")
        rule("Рівні кути",
             "Кути рівні, якщо мають однакові градусні міри.\n"
             "∠ABC = ∠MNK  ⟺  градусні міри рівні")
        rule("Рівні трикутники",
             "Якщо △ABC = △KLM, то всі відповідні елементи рівні:\n"
             "  Сторони:  AB = KL,   BC = LM,   AC = KM\n"
             "  Кути:      ∠A = ∠K,   ∠B = ∠L,   ∠C = ∠M\n\n"
             "На малюнку рівні сторони позначають однаковою кількістю рисок (|, ||, |||),\n"
             "а рівні кути — однаковою кількістю дуг.")
        rule("Рівні прямокутники",
             "Прямокутники ABCD і KLMN рівні, якщо AB = KL  і  BC = LM.\n"
             "Рівні фігури мають рівні периметри.")

        # Theory illustration (enlarged)
        cv=tk.Canvas(f,bg=WHITE,height=300,bd=1,relief="solid",highlightthickness=0)
        cv.pack(fill="x",padx=px,pady=(20,14))
        self.after(80,lambda: self._draw_theory_fig(cv))

        tk.Button(f,text="Перейти до тренажера  →",bg=ACCENT,fg=WHITE,
                  font=("Segoe UI",14,"bold"),relief="flat",padx=28,pady=10,cursor="hand2",
                  command=self.show_trainer).pack(anchor="w",padx=px,pady=(6,40))

    def _draw_theory_fig(self,cv):
        cv.delete("all"); cv.update_idletasks()
        W=max(int(cv.winfo_width()),self.SW-160); H=300

        # ── 1. Equal segments ──────────────────────────────────────────────
        slen=min(120,int(W*0.13)); x0=int(W*0.05)
        for y,l1,l2 in [(H*0.30,"A","B"),(H*0.65,"C","D")]:
            cv.create_line(x0,y,x0+slen,y,width=5,fill=ACCENT,capstyle="round")
            self._ticks(cv,(x0,y),(x0+slen,y),1,TC1)
            cv.create_text(x0-14,y,text=l1,font=("Georgia",13,"bold"),fill=TEXT)
            cv.create_text(x0+slen+14,y,text=l2,font=("Georgia",13,"bold"),fill=TEXT)
            cv.create_text((2*x0+slen)//2,y-18,text="5 см",font=("Segoe UI",11),fill=MUTED)
        cv.create_text(x0+slen//2,H-18,text="AB = CD",
                       font=("Segoe UI",13,"bold"),fill=LBL_CLR)

        cv.create_line(int(W*0.30),12,int(W*0.30),H-12,fill=DIV,width=1,dash=(5,4))

        # ── 2. Equal angles ────────────────────────────────────────────────
        arm=72
        for xi,lbl in [(int(W*0.415),"O"),(int(W*0.535),"M")]:
            deg=55; r=math.radians(deg)
            cv.create_line(xi,H//2,xi+arm,H//2,width=3,fill=ACCENT,capstyle="round")
            cv.create_line(xi,H//2,
                           xi+int(arm*math.cos(r)),H//2-int(arm*math.sin(r)),
                           width=3,fill=ACCENT,capstyle="round")
            # two arcs = "equal angle" mark
            for rad in [24,16]:
                cv.create_arc(xi-rad,H//2-rad,xi+rad,H//2+rad,
                              start=0,extent=deg,style="arc",outline=TC1,width=2)
            cv.create_text(xi+34,H//2-22,text=f"{deg}°",
                           font=("Segoe UI",11),fill=MUTED)
            cv.create_text(xi-14,H//2+15,text=lbl,
                           font=("Georgia",13,"bold"),fill=TEXT)
        cv.create_text(int(W*0.475),H-18,text="∠O = ∠M",
                       font=("Segoe UI",13,"bold"),fill=LBL_CLR)

        cv.create_line(int(W*0.645),12,int(W*0.645),H-12,fill=DIV,width=1,dash=(5,4))

        # ── 3. Equal triangles (with ticks AND arcs) ────────────────────────
        raw=tri_from_sides(9,7,6)
        hw=int(W*0.145); hh=int(H*0.44)
        raw_rot=rotate_poly(raw,42)
        scale=min(max_scale(raw,hw*2,hh*2), max_scale(raw_rot,hw*2,hh*2))
        p1=place_poly(raw,     int(W*0.762),H//2,scale)
        p2=place_poly(raw_rot, int(W*0.920),H//2,scale)

        for poly,lbls,clr,tc in [
            (p1,["A","B","C"],ACCENT, TC1),
            (p2,["D","E","F"],ACCENT2,TC2)
        ]:
            cv.create_polygon(poly,outline=clr,fill="",width=3)
            ccx=sum(p[0] for p in poly)/3; ccy=sum(p[1] for p in poly)/3
            for i,(px,py) in enumerate(poly):
                dx,dy=px-ccx,py-ccy; d=math.hypot(dx,dy) or 1
                cv.create_text(px+16*dx/d,py+16*dy/d,
                               text=lbls[i],font=("Georgia",12,"bold"),fill=TEXT)
            # side ticks
            for i in range(3):
                self._ticks(cv,poly[i],poly[(i+1)%3],i+1,tc)
            # angle arcs
            for i in range(3):
                oth=[j for j in range(3) if j!=i]
                self._arcs(cv,poly[i],poly[oth[0]],poly[oth[1]],i+1,tc)

        cv.create_text(int(W*0.840),H-18,text="△ABC = △DEF  (сторони і кути рівні)",
                       font=("Segoe UI",12,"bold"),fill=LBL_CLR)

    # ── Trainer ───────────────────────────────────────────────────────────────
    def show_trainer(self):
        self._clear(); self.mode="trainer"
        LW=int(self.SW*0.65)
        left=tk.Frame(self.body,bg=BG,width=LW)
        left.pack(side="left",fill="both"); left.pack_propagate(False)

        top=tk.Frame(left,bg=HDR_BG,height=48)
        top.pack(fill="x"); top.pack_propagate(False)
        tk.Label(top,text="Тренажер",bg=HDR_BG,fg=HDR_FG,
                 font=("Georgia",17,"bold")).pack(side="left",padx=22)
        self.lbl_score=tk.Label(top,text="0 / 0",bg=HDR_BG,fg="#7ecbff",
                                font=("Segoe UI",16,"bold"))
        self.lbl_score.pack(side="right",padx=22)

        self.task_card=tk.Frame(left,bg=WHITE,highlightbackground=ACCENT,highlightthickness=2)
        self.task_card.pack(fill="x",padx=22,pady=(14,0))
        self.task_lbl=tk.Label(self.task_card,text="",bg=WHITE,fg=TEXT,
                               font=("Segoe UI",15,"bold"),justify="center",
                               wraplength=LW-100,pady=12,padx=16)
        self.task_lbl.pack()

        self.cv=tk.Canvas(left,bg=WHITE,height=300,bd=1,relief="solid",highlightthickness=0)
        self.cv.pack(fill="x",padx=22,pady=10)

        self.lbl_fb=tk.Label(left,text="",bg=BG,fg=GREEN,font=("Segoe UI",16,"bold"))
        self.lbl_fb.pack(pady=3)

        self.disp_frame=tk.Frame(left,bg=CARD,highlightbackground=ACCENT,highlightthickness=2)
        self.lbl_disp=tk.Label(self.disp_frame,text="",bg=CARD,fg=TEXT,
                               font=("Courier",42,"bold"),width=10,anchor="e",padx=10)
        self.lbl_disp.pack()

        self.num_frame=tk.Frame(left,bg=BG)
        for row in [["7","8","9"],["4","5","6"],["1","2","3"],["C","0","⌫"]]:
            r=tk.Frame(self.num_frame,bg=BG); r.pack(pady=3)
            for ch in row:
                cbg=RED_BG if ch in("⌫","C") else BTN_BG
                cfg=RED    if ch in("⌫","C") else TEXT
                tk.Button(r,text=ch,bg=cbg,fg=cfg,activebackground=BTN_HOV,
                          font=("Segoe UI",18,"bold"),width=5,height=1,
                          relief="flat",bd=0,
                          command=lambda c=ch: self._numpad(c)).pack(side="left",padx=4)

        self.btn_row=tk.Frame(left,bg=BG); self.btn_row.pack(pady=6)
        self.btn_ok=tk.Button(self.btn_row,text="✓  Перевірити",bg=GREEN,fg=WHITE,
                              font=("Segoe UI",15,"bold"),relief="flat",padx=26,pady=8,
                              command=self._check)
        self.btn_next=tk.Button(self.btn_row,text="▶  Наступне",bg=ACCENT,fg=WHITE,
                                font=("Segoe UI",15,"bold"),relief="flat",padx=26,pady=8,
                                command=self._next)

        self.yn_row=tk.Frame(left,bg=BG)
        tk.Button(self.yn_row,text="  Так  ",bg=GREEN,fg=WHITE,
                  font=("Segoe UI",15,"bold"),relief="flat",padx=28,pady=8,
                  command=lambda: self._check("yes")).pack(side="left",padx=10)
        tk.Button(self.yn_row,text="  Ні  ",bg=RED,fg=WHITE,
                  font=("Segoe UI",15,"bold"),relief="flat",padx=28,pady=8,
                  command=lambda: self._check("no")).pack(side="left",padx=10)

        right=tk.Frame(self.body,bg=PANEL)
        right.pack(side="right",fill="both",expand=True)
        rp=tk.Frame(right,bg=PANEL); rp.pack(fill="both",expand=True,padx=24,pady=24)
        tk.Label(rp,text="Пам'ятай",bg=PANEL,fg=GOLD,
                 font=("Segoe UI",15,"bold")).pack(anchor="w",pady=(0,10))
        for title,body in [
            ("Рівні трикутники",
             "△ABC = △KLM:\nAB=KL,  BC=LM,  AC=KM\n∠A=∠K,  ∠B=∠L,  ∠C=∠M"),
            ("Риски",
             "| — одна риска = рівні сторони\n|| — дві риски = рівні сторони\n||| — три риски = рівні сторони"),
            ("Дуги",
             "Однакова кількість дуг\nбіля кута = рівні кути"),
            ("Сума кутів",
             "∠A + ∠B + ∠C = 180°"),
            ("Рівні прямокутники",
             "AB=KL і BC=LM\n→ ABCD = KLMN"),
            ("Периметр",
             "P = 2·(a + b)"),
        ]:
            card=tk.Frame(rp,bg=CARD,padx=14,pady=10); card.pack(fill="x",pady=4)
            tk.Label(card,text=title,bg=CARD,fg=ACCENT,
                     font=("Segoe UI",12,"bold")).pack(anchor="w")
            tk.Label(card,text=body,bg=CARD,fg=TEXT,
                     font=("Segoe UI",12),justify="left").pack(anchor="w")

        self.after(80,self._next)

    # ── Task generation ───────────────────────────────────────────────────────
    # Задачі:
    #  find_side           — всі сторони ABC відомі; знайди відповідну сторону KLM
    #  find_angle_direct   — 2 кути ABC відомі; знайди відповідний кут KLM
    #  find_angle_compute  — 2 кути ABC відомі → обчисли третій через 180°; він же = кут KLM
    #  check_equal         — так/ні: порівняй сторони
    #  rect_perimeter      — KLMN: обидві сторони відомі; знайди периметр рівного ABCD
    #  rect_side           — KLMN: обидві сторони відомі; ABCD: одна сторона скрита = «?»

    TASK_TYPES = [
        "find_side",
        "find_angle_direct",
        "find_angle_compute",
        "check_equal",
        "rect_perimeter",
        "rect_side",
    ]

    def _next(self):
        if self.mode!="trainer": return
        self.phase="answer"; self.inp=""
        self.lbl_fb.config(text="",bg=BG)
        self.lbl_disp.config(text="",bg=CARD)
        self.btn_next.pack_forget(); self.btn_ok.pack_forget()
        self.yn_row.pack_forget(); self.disp_frame.pack_forget()
        self.num_frame.pack_forget()
        self.cv.delete("all")
        tt=random.choice(self.TASK_TYPES)

        # ── find_side ──────────────────────────────────────────────────────
        # ABC: всі 3 сторони показані.
        # KLM: одна сторона = «?», решта теж показані.
        # Відповідь: та ж сторона ABC.
        if tt=="find_side":
            self.ans_mode="number"
            sides=valid_sides(); uidx=random.randint(0,2)
            kn=["KL","LM","KM"]
            self.task={"type":tt,"sides":sides,"uidx":uidx,"ans":sides[uidx]}
            self.task_lbl.config(
                text=f"△ABC = △KLM.  Всі сторони △ABC позначені на малюнку.\n"
                     f"Знайди {kn[uidx]}  («?»).")
            self.after(10,self._draw_task)

        # ── find_angle_direct ──────────────────────────────────────────────
        # ABC: 2 кути відомі (третій схований).
        # KLM: «?» = один із 2 відомих кутів ABC.
        # Учень просто переносить кут з ABC → KLM.
        elif tt=="find_angle_direct":
            self.ans_mode="number"
            angles=valid_angles()
            hidden_abc=random.randint(0,2)
            shown_abc=[i for i in range(3) if i!=hidden_abc]
            asked_klm=random.choice(shown_abc)
            kn=["∠K","∠L","∠M"]; an=["∠A","∠B","∠C"]
            self.task={"type":tt,"angles":angles,
                       "hidden_abc":hidden_abc,"asked_klm":asked_klm,
                       "ans":angles[asked_klm]}
            self.task_lbl.config(
                text=f"△ABC = △KLM.   "
                     f"{an[shown_abc[0]]}={angles[shown_abc[0]]}°,  "
                     f"{an[shown_abc[1]]}={angles[shown_abc[1]]}°.\n"
                     f"Знайди {kn[asked_klm]}  («?»).")
            self.after(10,self._draw_task)

        # ── find_angle_compute ─────────────────────────────────────────────
        # ABC: 2 кути відомі → треба порахувати третій через 180°.
        # KLM: «?» = цей третій кут.
        elif tt=="find_angle_compute":
            self.ans_mode="number"
            angles=valid_angles()
            unknown=random.randint(0,2)
            shown=[i for i in range(3) if i!=unknown]
            kn=["∠K","∠L","∠M"]; an=["∠A","∠B","∠C"]
            self.task={"type":tt,"angles":angles,"unknown":unknown,"ans":angles[unknown]}
            self.task_lbl.config(
                text=f"△ABC = △KLM.   "
                     f"{an[shown[0]]}={angles[shown[0]]}°,  "
                     f"{an[shown[1]]}={angles[shown[1]]}°.\n"
                     f"Знайди {kn[unknown]}.")
            self.after(10,self._draw_task)

        # ── check_equal ────────────────────────────────────────────────────
        elif tt=="check_equal":
            self.ans_mode="choice"
            sides1=valid_sides(); equal=random.choice([True,False])
            if equal:
                sides2=sides1[:]; ans="yes"
            else:
                sides2=sides1[:]; i=random.randint(0,2); d=random.randint(1,4)
                sides2[i]=max(2,sides2[i]+random.choice([-1,1])*d)
                s=sorted(sides2)
                if s[0]+s[1]<=s[2]: sides2[i]=sides1[i]+d
                ans="no"
            self.task={"type":tt,"sides1":sides1,"sides2":sides2,"ans":ans}
            self.task_lbl.config(text="Чи рівні між собою △ABC і △KLM?\n"
                                      "(порівняй відповідні сторони)")
            self.after(10,self._draw_task)

        # ── rect_perimeter ─────────────────────────────────────────────────
        # KLMN: обидві сторони відомі.
        # ABCD рівний KLMN → знайди периметр ABCD.
        elif tt=="rect_perimeter":
            self.ans_mode="number"
            a=random.randint(4,16); b=random.randint(4,16)
            P=2*(a+b)
            self.task={"type":tt,"a":a,"b":b,"P":P,"ans":P}
            self.task_lbl.config(
                text=f"Прямокутники ABCD і KLMN рівні.\n"
                     f"KL = {a} см,  LM = {b} см.\n"
                     f"Знайди периметр ABCD.")
            self.after(10,self._draw_task)

        # ── rect_side ──────────────────────────────────────────────────────
        # KLMN: обидві сторони відомі.
        # ABCD: одна сторона скрита = «?». Знайди через рівність.
        elif tt=="rect_side":
            self.ans_mode="number"
            a=random.randint(4,16); b=random.randint(4,16)
            while a==b: b=random.randint(4,16)
            # ask_idx: 0=AB(=a) або 1=BC(=b)
            ask_idx=random.choice([0,1])
            ans_val=a if ask_idx==0 else b
            ask_name="AB" if ask_idx==0 else "BC"
            klmn_eq ="KL" if ask_idx==0 else "LM"
            self.task={"type":tt,"a":a,"b":b,"ask_idx":ask_idx,"ans":ans_val}
            self.task_lbl.config(
                text=f"Прямокутники ABCD і KLMN рівні.\n"
                     f"KL = {a} см,  LM = {b} см.\n"
                     f"Знайди {ask_name}  («?»).  Підказка: {ask_name} = {klmn_eq}.")
            self.after(10,self._draw_task)

        if self.ans_mode=="number":
            self.disp_frame.pack(pady=5,ipadx=8,ipady=4)
            self.num_frame.pack(pady=3)
            self.btn_ok.pack(side="left",padx=14)
        else:
            self.yn_row.pack(pady=10)
        self.lbl_score.config(text=f"{self.score} / {self.total}")

    # ── Drawing ───────────────────────────────────────────────────────────────
    def _draw_task(self):
        if not self.task: return
        cv=self.cv; cv.delete("all"); cv.update_idletasks()
        W=max(int(cv.winfo_width()),int(self.SW*0.60)); H=int(cv.winfo_height()) or 300
        t=self.task; tt=t["type"]
        if tt in("find_side","check_equal"):
            self._draw_two_tri_sides(cv,W,H,t)
        elif tt in("find_angle_direct","find_angle_compute"):
            self._draw_two_tri_angles(cv,W,H,t)
        elif tt in("rect_perimeter","rect_side"):
            self._draw_two_rects(cv,W,H,t)

    def _cells(self,W,H):
        m=20; cw=(W-3*m)//2; ch=H-2*m
        return m+cw//2,H//2, m+cw+m+cw//2,H//2, cw,ch

    def _divider(self,cv,W,H):
        cv.create_line(W//2,8,W//2,H-8,fill=DIV,width=1,dash=(5,4))

    # ─────────────────────────────────────────────────────────────────────────
    def _draw_two_tri_sides(self,cv,W,H,t):
        tt=t["type"]
        if tt=="find_side":
            sides1=sides2=t["sides"]; klm_hide=t["uidx"]
        else:
            sides1,sides2=t["sides1"],t["sides2"]; klm_hide=None

        # Build ONE canonical raw polygon for ABC.
        # For check_equal with unequal triangles, build a separate raw for KLM.
        raw1=tri_from_sides(*sides1)
        if raw1 is None: return
        are_same_shape=(sides1==sides2)
        if are_same_shape:
            raw2=raw1          # identical shape — just rotate
        else:
            raw2=tri_from_sides(*sides2)
            if raw2 is None: raw2=raw1

        cx1,cy1,cx2,cy2,cw,ch=self._cells(W,H)
        rot=random.randint(30,150)

        if are_same_shape:
            # Compute one scale valid for BOTH orientations so sizes match exactly
            raw2_rot=rotate_poly(raw1,rot)
            scale=min(max_scale(raw1,cw,ch), max_scale(raw2_rot,cw,ch))
            p1=place_poly(raw1,     cx1,cy1,scale)
            p2=place_poly(raw2_rot, cx2,cy2,scale)
        else:
            p1,_=fit_poly(raw1,cx1,cy1,cw,ch)
            p2,_=fit_poly(rotate_poly(raw2,rot),cx2,cy2,cw,ch)

        self._divider(cv,W,H)
        self._draw_tri_shape(cv,p1,["A","B","C"],ACCENT)
        self._draw_tri_shape(cv,p2,["K","L","M"],ACCENT2)

        # ticks only when equal
        if tt=="find_side":
            for i in range(3):
                vi,vj=[(0,1),(1,2),(0,2)][i]
                self._ticks(cv,p1[vi],p1[vj],i+1,TC1)
                self._ticks(cv,p2[vi],p2[vj],i+1,TC2)

        pairs=[(0,1),(1,2),(0,2)]
        for i,(a,b) in enumerate(pairs):
            ox,oy=side_label_pos(p1[a],p1[b])
            cv.create_text(ox,oy,text=str(sides1[i]),
                           font=("Segoe UI",12,"bold"),fill=LBL_CLR)
        for i,(a,b) in enumerate(pairs):
            ox,oy=side_label_pos(p2[a],p2[b])
            if klm_hide is not None and i==klm_hide:
                cv.create_text(ox,oy,text="?",font=("Segoe UI",15,"bold"),fill=RED)
            else:
                cv.create_text(ox,oy,text=str(sides2[i]),
                               font=("Segoe UI",12,"bold"),fill=LBL_CLR)

    # ─────────────────────────────────────────────────────────────────────────
    def _draw_two_tri_angles(self,cv,W,H,t):
        tt=t["type"]; angles=t["angles"]
        raw=tri_from_angles(*angles)
        if raw is None: return
        cx1,cy1,cx2,cy2,cw,ch=self._cells(W,H)
        rot=random.randint(30,150)
        # Same raw polygon rotated — use one scale for both so sizes match exactly
        raw_rot=rotate_poly(raw,rot)
        scale=min(max_scale(raw,cw,ch), max_scale(raw_rot,cw,ch))
        p1=place_poly(raw,     cx1,cy1,scale)
        p2=place_poly(raw_rot, cx2,cy2,scale)
        self._divider(cv,W,H)
        self._draw_tri_shape(cv,p1,["A","B","C"],ACCENT)
        self._draw_tri_shape(cv,p2,["K","L","M"],ACCENT2)

        # angle arcs on both triangles
        for i in range(3):
            oth=[j for j in range(3) if j!=i]
            self._arcs(cv,p1[i],p1[oth[0]],p1[oth[1]],i+1,TC1)
            self._arcs(cv,p2[i],p2[oth[0]],p2[oth[1]],i+1,TC2)

        if tt=="find_angle_direct":
            hidden_abc=t["hidden_abc"]; asked_klm=t["asked_klm"]
            # ABC: show all except hidden_abc
            for i in range(3):
                if i==hidden_abc: continue
                oth=[j for j in range(3) if j!=i]
                pos=angle_label_pos(p1[i],p1[oth[0]],p1[oth[1]])
                cv.create_text(pos[0],pos[1],text=f"{angles[i]}°",
                               font=("Segoe UI",12,"bold"),fill=LBL_CLR)
            # KLM: show all, asked_klm = «?»
            for i in range(3):
                oth=[j for j in range(3) if j!=i]
                pos=angle_label_pos(p2[i],p2[oth[0]],p2[oth[1]])
                if i==asked_klm:
                    cv.create_text(pos[0],pos[1],text="?",
                                   font=("Segoe UI",15,"bold"),fill=RED)
                else:
                    cv.create_text(pos[0],pos[1],text=f"{angles[i]}°",
                                   font=("Segoe UI",12,"bold"),fill=LBL_CLR)
        else:  # find_angle_compute
            unknown=t["unknown"]
            shown=[i for i in range(3) if i!=unknown]
            # ABC: only show the 2 known angles
            for i in shown:
                oth=[j for j in range(3) if j!=i]
                pos=angle_label_pos(p1[i],p1[oth[0]],p1[oth[1]])
                cv.create_text(pos[0],pos[1],text=f"{angles[i]}°",
                               font=("Segoe UI",12,"bold"),fill=LBL_CLR)
            # KLM: only «?» on the unknown vertex
            oth=[j for j in range(3) if j!=unknown]
            pos=angle_label_pos(p2[unknown],p2[oth[0]],p2[oth[1]])
            cv.create_text(pos[0],pos[1],text="?",
                           font=("Segoe UI",15,"bold"),fill=RED)

    # ─────────────────────────────────────────────────────────────────────────
    def _draw_two_rects(self,cv,W,H,t):
        tt=t["type"]; a,b=t["a"],t["b"]
        scale=min((W//2-60)/max(a,b),(H-80)/max(a,b),16.0)
        rw,rh=a*scale,b*scale
        top_y=int(H//2-rh//2)

        def rect(x0,y0,lbls,clr,sa,sb,qa=False,qb=False):
            cv.create_rectangle(x0,y0,x0+rw,y0+rh,outline=clr,fill="",width=3)
            for lbl,lx,ly in zip(lbls,
                [x0-15, x0+rw+8, x0+rw+8, x0-15],
                [y0-15, y0-15,   y0+rh+8, y0+rh+8]):
                cv.create_text(lx,ly,text=lbl,font=("Georgia",13,"bold"),fill=TEXT)
            # top side = a
            if qa:
                cv.create_text(x0+rw/2,y0-18,text="? см",
                               font=("Segoe UI",13,"bold"),fill=RED)
            elif sa:
                cv.create_text(x0+rw/2,y0-18,text=f"{a} см",
                               font=("Segoe UI",12,"bold"),fill=LBL_CLR)
            # right side = b
            if qb:
                cv.create_text(x0+rw+18,y0+rh/2,text="? см",
                               font=("Segoe UI",13,"bold"),fill=RED)
            elif sb:
                cv.create_text(x0+rw+18,y0+rh/2,text=f"{b} см",
                               font=("Segoe UI",12,"bold"),fill=LBL_CLR)

        x1=W//4-int(rw//2); x2=3*W//4-int(rw//2)

        if tt=="rect_perimeter":
            # Left: KLMN with both sides; Right: ABCD no sides + "P=?"
            rect(x1,top_y,["K","L","M","N"],ACCENT2,sa=True,sb=True)
            self._divider(cv,W,H)
            rect(x2,top_y,["A","B","C","D"],ACCENT, sa=False,sb=False)
            cv.create_text(x2+rw/2,top_y+rh+36,text="P = ?",
                           font=("Segoe UI",15,"bold"),fill=RED)

        else:  # rect_side
            ask_idx=t["ask_idx"]   # 0=ask AB(top=a), 1=ask BC(right=b)
            # Left: KLMN with both sides known
            rect(x1,top_y,["K","L","M","N"],ACCENT2,sa=True,sb=True)
            self._divider(cv,W,H)
            # Right: ABCD — show the known side, hide the asked one
            qa=(ask_idx==0); qb=(ask_idx==1)
            sa=(not qa); sb=(not qb)
            rect(x2,top_y,["A","B","C","D"],ACCENT,sa=sa,sb=sb,qa=qa,qb=qb)

    # ── Shapes ────────────────────────────────────────────────────────────────
    def _draw_tri_shape(self,cv,poly,labels,color):
        cv.create_polygon(poly,outline=color,fill="",width=3)
        cx=sum(p[0] for p in poly)/3; cy=sum(p[1] for p in poly)/3
        for i,(px,py) in enumerate(poly):
            dx,dy=px-cx,py-cy; d=math.hypot(dx,dy) or 1
            cv.create_text(px+17*dx/d,py+17*dy/d,
                           text=labels[i],font=("Georgia",13,"bold"),fill=TEXT)

    def _ticks(self,cv,p1,p2,n,color):
        """
        Draw n tick marks across the segment — perpendicular to it.
        Each tick is a short line crossing the segment at right angles.
        The n marks are spaced along the segment direction.
        """
        dx=p2[0]-p1[0]; dy=p2[1]-p1[1]
        seg_len=math.hypot(dx,dy) or 1
        # unit vector along segment
        ux=dx/seg_len; uy=dy/seg_len
        # unit vector perpendicular to segment (the tick direction)
        px_=-uy; py_=ux
        mark=9   # half-length of each tick
        gap=6    # spacing between ticks along segment
        mx=(p1[0]+p2[0])/2; my=(p1[1]+p2[1])/2
        for i in range(n):
            # offset along segment from midpoint
            along=(i-(n-1)/2)*gap
            cx_=mx+along*ux
            cy_=my+along*uy
            cv.create_line(cx_-mark*px_, cy_-mark*py_,
                           cx_+mark*px_, cy_+mark*py_,
                           fill=color,width=3,capstyle="round")

    def _arcs(self,cv,v,a,b,n,color):
        """n concentric arcs at vertex v, spanning the angle between va and vb."""
        d1=(a[0]-v[0],a[1]-v[1]); l1=math.hypot(*d1) or 1
        d2=(b[0]-v[0],b[1]-v[1]); l2=math.hypot(*d2) or 1
        ang1=math.degrees(math.atan2(-d1[1],d1[0]))
        ang2=math.degrees(math.atan2(-d2[1],d2[0]))
        ext=ang2-ang1
        if ext>180: ext-=360
        elif ext<-180: ext+=360
        r0,gap=16,7
        for i in range(n):
            r=r0+i*gap
            cv.create_arc(v[0]-r,v[1]-r,v[0]+r,v[1]+r,
                          start=ang1,extent=ext,style="arc",outline=color,width=2)

    # ── Input ─────────────────────────────────────────────────────────────────
    def _on_key(self,event):
        if self.mode=="trainer" and self.ans_mode=="number" and event.char.isdigit():
            self._numpad(event.char)

    def _numpad(self,ch):
        if self.mode!="trainer" or self.phase!="answer" or self.ans_mode!="number": return
        if ch=="⌫":   self.inp=self.inp[:-1]
        elif ch=="C": self.inp=""
        elif len(self.inp)<6: self.inp+=ch
        self.lbl_disp.config(text=self.inp)

    def _check(self,choice=None):
        if self.mode!="trainer" or self.phase!="answer": return
        if self.ans_mode=="number":
            if not self.inp: return
            try: got=int(self.inp)
            except ValueError: return
        else:
            if not choice: return
            got=choice
        self.phase="feedback"; self.total+=1
        ok=(got==self.task["ans"])
        if ok:
            self.score+=1
            self.lbl_fb.config(text="✅  Правильно!",fg=GREEN,bg=BG)
            self.lbl_disp.config(bg=GREEN_BG)
            self.after(1100,self._next)
        else:
            ans=self.task["ans"]; tt=self.task["type"]
            suf="°" if "angle" in tt else " см" if tt not in("check_equal",) else ""
            self.lbl_fb.config(text=f"❌  Ні.  Відповідь: {ans}{suf}",fg=RED,bg=BG)
            self.lbl_disp.config(bg=RED_BG)
            self.btn_ok.pack_forget(); self.yn_row.pack_forget()
            self.btn_next.pack(side="left",padx=14)
        self.lbl_score.config(text=f"{self.score} / {self.total}")

if __name__=="__main__":
    App().mainloop()
