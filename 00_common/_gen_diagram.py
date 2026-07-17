#!/usr/bin/env python3
# PseudoLab 데이터 구조 맵 — SVG + PNG 동시 생성 (단일 좌표 소스)
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1500, 900
OUT = os.path.dirname(os.path.abspath(__file__))

# ---- nodes: id -> (x,y,w,h, fill, stroke, [lines]) ----
MASTER=("#dae8fc","#6c8ebf"); SNAP=("#d5e8d4","#82b366")
INCR=("#ffe6cc","#d79b00");   MART=("#e1d5e7","#9673a6")
NODES = {
 "proj": (40,70,300,100, *MASTER, ["dl_projects  (master)","PK: id (= project_id)","title, status, cohort","snapshot · base_date=MAX"]),
 "prof": (40,330,300,170, *MASTER, ["dl_profiles  (master, PII)","PK: id (= user_id)","activity_score, experience_level,","cohorts, runner/builder_count","사전 공변량 · snapshot"]),
 "app":  (440,60,320,110, *SNAP, ["dl_project_applications  (PII)","PK: id | FK: user_id, *_project_id","season(기수), status","첫 참여/승인 후보 · snapshot"]),
 "mem":  (440,250,320,130, *SNAP, ["dl_project_members","PK: id | FK: project_id, user_id","role(runner/builder/member)","! auditor 구분 없음 · status","snapshot"]),
 "task": (440,445,320,110, *SNAP, ["dl_project_tasks","PK: id | FK: project_id, assignee_id","status(done), progress","완주 신호 후보 · snapshot"]),
 "sess": (860,250,320,120, *SNAP, ["dl_project_sessions","PK: id | FK: project_id","week_number, session_date","snapshot"]),
 "att":  (860,445,320,120, *INCR, ["dl_project_attendance","PK: id | FK: session_id, user_id","status(present)","incremental · 중복 없음"]),
 "dmu":  (40,700,320,130, *MART, ["dm_user_daily_activity  (PII)","grain: user x date x metric","metric_value, coverage_status","as_of_date=MAX"]),
 "dmm":  (440,690,380,150, *MART, ["dm_member_weekly_attendance  (정본,PII)","grain: project x user x week","participant_type(regular/auditor) *","member_status, attended, attendance_rate","as_of_date=MAX · 133,919행(중복)"]),
 "dmp":  (900,700,320,130, *MART, ["dm_project_weekly_attendance","grain: project x week","regular_attendance_rate,","auditor_attended_count *","as_of_date=MAX"]),
}
# ---- edges: (src,dst,label,dashed) ----
EDGES = [
 ("proj","app","*_project_id",False),("proj","mem","project_id",False),
 ("proj","task","project_id",False),("proj","sess","project_id",False),
 ("prof","app","user_id",False),("prof","mem","user_id",False),
 ("prof","att","user_id",False),("sess","att","session_id",False),
 ("att","dmm","agg",True),("mem","dmm","",True),
 ("dmm","dmp","rollup",True),("prof","dmu","agg",True),
]

def route(s,d):
    sx,sy,sw,sh=NODES[s][:4]; dx,dy,dw,dh=NODES[d][:4]
    scx,scy=sx+sw/2,sy+sh/2; dcx,dcy=dx+dw/2,dy+dh/2
    if abs(dcx-scx) >= abs(dcy-scy):  # horizontal dominant
        if dcx>=scx: p0=(sx+sw,scy); p3=(dx,dcy)
        else:        p0=(sx,scy);    p3=(dx+dw,dcy)
        mx=(p0[0]+p3[0])/2; pts=[p0,(mx,p0[1]),(mx,p3[1]),p3]
    else:                              # vertical dominant
        if dcy>=scy: p0=(scx,sy+sh); p3=(dcx,dy)
        else:        p0=(scx,sy);    p3=(dcx,dy+dh)
        my=(p0[1]+p3[1])/2; pts=[p0,(p0[0],my),(p3[0],my),p3]
    return pts

def midlabel(pts):  # midpoint of the longest segment → spreads labels to distinct targets
    best=None; bl=-1
    for i in range(len(pts)-1):
        a,b=pts[i],pts[i+1]; L=abs(b[0]-a[0])+abs(b[1]-a[1])
        if L>bl: bl=L; best=((a[0]+b[0])/2,(a[1]+b[1])/2)
    return best

# ===================== SVG =====================
def esc(t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="AppleSDGothicNeo, AppleGothic, sans-serif">']
svg.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
svg.append(f'<text x="40" y="40" font-size="20" font-weight="bold">PseudoLab 데이터 구조 맵 — 회고 실험 분석용 (2026-06-22)</text>')
svg.append('<defs><marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#666"/></marker></defs>')
for s,d,lab,dash in EDGES:
    pts=route(s,d); pline=" ".join(f"{x:.0f},{y:.0f}" for x,y in pts)
    col="#9673a6" if dash else "#666"; da=' stroke-dasharray="6,4"' if dash else ""
    svg.append(f'<polyline points="{pline}" fill="none" stroke="{col}" stroke-width="1.6"{da} marker-end="url(#arr)"/>')
    if lab:
        mx,my=midlabel(pts); svg.append(f'<text x="{mx+4:.0f}" y="{my-4:.0f}" font-size="12" fill="{col}">{esc(lab)}</text>')
for nid,(x,y,w,h,fill,stroke,lines) in NODES.items():
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    for i,ln in enumerate(lines):
        fw="bold" if i==0 else "normal"; fs=13 if i==0 else 11.5
        fc="#B85450" if ln.startswith("!") else "#222"
        svg.append(f'<text x="{x+10}" y="{y+20+i*18}" font-size="{fs}" font-weight="{fw}" fill="{fc}">{esc(ln)}</text>')
# legend
lx,ly=1240,70
svg.append(f'<rect x="{lx}" y="{ly}" width="240" height="230" rx="8" fill="#f5f5f5" stroke="#666" stroke-dasharray="4,3"/>')
svg.append(f'<text x="{lx+12}" y="{ly+24}" font-size="13" font-weight="bold">범례 (Legend)</text>')
leg=[("#dae8fc","마스터 (master)"),("#d5e8d4","snapshot → base_date=MAX"),("#ffe6cc","incremental (중복없음)"),("#e1d5e7","집계 마트 → as_of_date=MAX")]
for i,(c,t) in enumerate(leg):
    yy=ly+44+i*30
    svg.append(f'<rect x="{lx+12}" y="{yy}" width="22" height="16" fill="{c}" stroke="#888"/>')
    svg.append(f'<text x="{lx+42}" y="{yy+13}" font-size="11.5">{esc(t)}</text>')
svg.append(f'<text x="{lx+12}" y="{ly+44+4*30+8}" font-size="11" fill="#B85450">* PII · ! 주의 지점</text>')
# warning note
svg.append(f'<text x="440" y="600" font-size="12.5" fill="#B85450" font-style="italic">⚠ 출석/완주는 dl_project_members(auditor 없음) 말고 dm 마트 + participant_type=regular 로!</text>')
svg.append(f'<text x="440" y="620" font-size="12.5" fill="#B85450" font-style="italic">⚠ snapshot=base_date=MAX, 마트=as_of_date=MAX (미필터 시 30~53배 중복)</text>')
svg.append('</svg>')
open(os.path.join(OUT,"데이터구조_맵.svg"),"w").write("\n".join(svg))

# ===================== PNG (Pillow) =====================
def font(sz,bold=False):
    for p in ["/System/Library/Fonts/AppleSDGothicNeo.ttc","/System/Library/Fonts/Supplemental/AppleGothic.ttf","/Library/Fonts/Arial Unicode.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()
img=Image.new("RGB",(W,H),"white"); dr=ImageDraw.Draw(img)
f_title=font(20); f_hdr=font(14); f_body=font(12); f_lab=font(11); f_leg=font(12)
def btext(xy,t,fnt,fill): dr.text((xy[0]+1,xy[1]),t,font=fnt,fill=fill); dr.text(xy,t,font=fnt,fill=fill)
btext((40,18),"PseudoLab 데이터 구조 맵 — 회고 실험 분석용 (2026-06-22)",f_title,"#111")
def arrow(p_prev,p):  # small triangle at p
    import math
    dx,dy=p[0]-p_prev[0],p[1]-p_prev[1]; L=math.hypot(dx,dy) or 1; ux,uy=dx/L,dy/L
    ax,ay=p[0]-9*ux,p[1]-9*uy; px,py=-uy,ux
    dr.polygon([p,(ax+4*px,ay+4*py),(ax-4*px,ay-4*py)],fill="#666")
for s,d,lab,dash in EDGES:
    pts=route(s,d); col=(150,115,166) if dash else (102,102,102)
    for i in range(len(pts)-1):
        a,b=pts[i],pts[i+1]
        if dash:
            import math
            L=math.hypot(b[0]-a[0],b[1]-a[1]) or 1; n=int(L//10)
            for k in range(0,n,2):
                t0,t1=k/n,min((k+1)/n,1)
                dr.line([(a[0]+(b[0]-a[0])*t0,a[1]+(b[1]-a[1])*t0),(a[0]+(b[0]-a[0])*t1,a[1]+(b[1]-a[1])*t1)],fill=col,width=2)
        else:
            dr.line([a,b],fill=col,width=2)
    arrow(pts[-2],pts[-1])
    if lab:
        mlx,mly=midlabel(pts); dr.text((mlx+4,mly-14),lab,font=f_lab,fill=col)
def hx(c): c=c.lstrip("#"); return tuple(int(c[i:i+2],16) for i in (0,2,4))
for nid,(x,y,w,h,fill,stroke,lines) in NODES.items():
    dr.rounded_rectangle([x,y,x+w,y+h],radius=8,fill=hx(fill),outline=hx(stroke),width=2)
    for i,ln in enumerate(lines):
        fnt=f_hdr if i==0 else f_body
        fc=(184,84,80) if ln.startswith("!") else (34,34,34)
        if i==0: btext((x+10,y+8),ln,fnt,fc)
        else: dr.text((x+10,y+8+i*18),ln,font=fnt,fill=fc)
lx,ly=1240,70
dr.rounded_rectangle([lx,ly,lx+240,ly+230],radius=8,fill=(245,245,245),outline=(102,102,102),width=1)
btext((lx+12,ly+10),"범례 (Legend)",f_hdr,"#111")
for i,(c,t) in enumerate(leg):
    yy=ly+40+i*30; dr.rectangle([lx+12,yy,lx+34,yy+16],fill=hx(c),outline=(136,136,136))
    dr.text((lx+42,yy+1),t,font=f_leg,fill=(34,34,34))
dr.text((lx+12,ly+40+4*30+4),"* PII   ! 주의 지점",font=f_lab,fill=(184,84,80))
dr.text((440,596),"! 출석/완주는 dl_project_members(auditor 없음) 말고 dm 마트 + participant_type=regular 로!",font=f_body,fill=(184,84,80))
dr.text((440,616),"! snapshot=base_date=MAX, 마트=as_of_date=MAX (미필터 시 30~53배 중복)",font=f_body,fill=(184,84,80))
img.save(os.path.join(OUT,"데이터구조_맵.png"))
print("done:", os.path.exists(os.path.join(OUT,"데이터구조_맵.png")), os.path.exists(os.path.join(OUT,"데이터구조_맵.svg")))
print("png size:", img.size)
