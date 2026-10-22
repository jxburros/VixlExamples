from lib import *
import math
S=10
def blob(w,h,eyes=True):
    cx,cy=(w-1)/2,(h-1)/2
    inside=[[((x-cx)/(w/2))**2+((y-cy)/(h/2))**2<=1.0 for x in range(w)] for y in range(h)]
    rows=[]
    for y in range(h):
        r=""
        for x in range(w):
            if not inside[y][x]: r+="."; continue
            edge=any(not(0<=x+dx<w and 0<=y+dy<h and inside[y+dy][x+dx]) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
            if edge: r+="k"; continue
            c="g"
            if y>=h*0.7 or x>=w*0.78: c="d"
            if (x-cx)<-w*0.12 and (y-cy)<-h*0.18 and x<w*0.4 and y<h*0.38: c="h"
            r+=c
        rows.append(r)
    if eyes:
        ey=int(h*0.45); ex1=int(w*0.3); ex2=int(w*0.62)
        for ex in (ex1,ex2):
            for dy in (0,1):
                rows[ey+dy]=rows[ey+dy][:ex]+"e"+rows[ey+dy][ex+1:]
            rows[ey]=rows[ey][:ex+1]+"w"+rows[ey][ex+2:] if False else rows[ey]
    return rows
def cloud(w,h):
    rows=[["." for _ in range(w)] for _ in range(h)]
    for (cx,cy,r) in [(w*0.28,h*0.62,h*0.38),(w*0.5,h*0.4,h*0.42),(w*0.72,h*0.6,h*0.4)]:
        for y in range(h):
            for x in range(w):
                if (x-cx)**2+(y-cy)**2<=r*r and y<h-1: rows[y][x]="w"
    for x in range(1,w-1): rows[h-2][x]="w"
    return ["".join(r) for r in rows]
PAL={"k":"#12302a","g":"#5ef28a","d":"#2fb866","h":"#d9ffe6","e":"#12302a","w":"#ffffff"}
def px(name,rows,pal,x,y,scale=S):
    return [{"type":"pixel-art","name":name,"x":x,"y":y,"palette":{**pal,".":"transparent"},"rows":rows,"shading":False,"outline":False},
            {"type":"resize","target":name,"width":len(rows[0])*scale,"height":len(rows)*scale}]
def build():
    p=new("#7fd3ff",[("Press Start 2P",400,"Px"),("Space Mono",700,"Mono")])
    DUR=4800
    ap(p,[{"type":"timeline-set","duration":DUR,"fps":12,"loop":1}])
    ap(p,[{"type":"solid","name":"sky","color":"#7fd3ff"},
          {"type":"shape","shape":"rectangle","name":"ground","x":0,"y":560,"width":1280,"height":160,"fill":"#8a5a3b"},
          {"type":"shape","shape":"rectangle","name":"grass","x":0,"y":560,"width":1280,"height":30,"fill":"#4cc46a"},
          {"type":"shape","shape":"rectangle","name":"grass2","x":0,"y":590,"width":1280,"height":10,"fill":"#2f9e55"}])
    # dirt specks
    import random; rnd=random.Random(3)
    ap(p,[{"type":"shape","shape":"rectangle","name":f"dirt{i}","x":rnd.randrange(0,1250)//10*10,"y":610+rnd.randrange(0,100)//10*10,"width":20,"height":10,"fill":"#6d452c"} for i in range(26)])
    ap(p,px("cloud1",cloud(16,6),PAL,100,90)+px("cloud2",cloud(12,5),PAL,820,150)+px("cloud3",cloud(14,5),PAL,1180,60))
    # bushes
    bush=blob(10,5,False)
    ap(p,px("bush1",bush,{"k":"#1d5e34","g":"#3bb25b","d":"#2a8c47","h":"#6ee08a"},230,510)+px("bush2",bush,{"k":"#1d5e34","g":"#3bb25b","d":"#2a8c47","h":"#6ee08a"},900,510))
    coin=["..yyyy..",".yyoooy.","yyoyyyoy","yyoyyyoy","yyoyyyoy","yyoyyyoy",".yyoooy.","..yyyy.."]
    cp={"y":"#ffd84d","o":"#e09a1a"}
    coins=[(380,420),(620,360),(860,420),(1100,380)]
    for i,(x,y) in enumerate(coins): ap(p,px(f"coin{i}",coin,cp,x,y,8))
    ap(p,px("slimeA",blob(16,9),PAL,0,560-90,S)+px("slimeB",blob(12,12),PAL,0,560-120,S))
    ap(p,[{"type":"text","name":"score","text":"SCORE 0000","font":"Px","size":30,"color":"#12302a","x":50,"y":40},
          {"type":"text","name":"hint","text":"nearest-neighbour. no blur. ever.","font":"Px","size":20,"color":"#12302a","x":50,"y":96,"opacity":1}])
    # motion
    X0,X1=-200,1420
    def xat(t): return X0+(X1-X0)*t/DUR
    ap(p,[{"type":"keyframes","target":n,"property":"translate-x","keys":[{"time":0,"value":X0,"easing":"linear"},{"time":DUR,"value":X1}]} for n in ("slimeA","slimeB")])
    period=600
    hop=[]; vis_a=[]; vis_b=[]
    t=0
    k=0
    while t<DUR:
        hop+=[{"time":t,"value":0,"easing":"ease-out-quad"},{"time":t+period//2,"value":-150,"easing":"ease-in-quad"}]
        vis_a+=[{"time":t,"value":True,"easing":"hold"},{"time":t+120,"value":False,"easing":"hold"},{"time":t+period-120,"value":True,"easing":"hold"}]
        vis_b+=[{"time":t,"value":False,"easing":"hold"},{"time":t+120,"value":True,"easing":"hold"},{"time":t+period-120,"value":False,"easing":"hold"}]
        t+=period
    hop.append({"time":t,"value":0})
    # dedupe times
    def clean(keys):
        out={}; 
        for kk in keys: out[kk["time"]]=kk
        return [out[tt] for tt in sorted(out)]
    ap(p,[{"type":"keyframes","target":"slimeA","property":"translate-y","keys":clean(hop)},{"type":"keyframes","target":"slimeB","property":"translate-y","keys":clean(hop)},
          {"type":"keyframes","target":"slimeA","property":"visible","keys":clean(vis_a)},{"type":"keyframes","target":"slimeB","property":"visible","keys":clean(vis_b)}])
    # clouds drift
    ap(p,[{"type":"animate","target":"cloud1","property":"translate-x","from":0,"to":200,"start":0,"duration":DUR,"easing":"linear"},
          {"type":"animate","target":"cloud2","property":"translate-x","from":0,"to":-260,"start":0,"duration":DUR,"easing":"linear"},
          {"type":"animate","target":"cloud3","property":"translate-x","from":0,"to":-260,"start":0,"duration":DUR,"easing":"linear"}])
    # coins: bob + collect
    score=[{"time":0,"value":"SCORE 0000","easing":"hold"}]
    for i,(x,y) in enumerate(coins):
        tcol=int((x+80-X0)/(X1-X0)*DUR)
        ap(p,[{"type":"keyframes","target":f"coin{i}","property":"translate-y","sample":{"fn":"sin","period":800,"amplitude":8,"step_ms":100,"duration":tcol,"start":0}},
              {"type":"keyframes","target":f"coin{i}","property":"visible","keys":[{"time":0,"value":True,"easing":"hold"},{"time":tcol,"value":False}]},
              {"type":"keyframes","target":f"coin{i}","property":"scale-x","sample":{"fn":"triangle","period":600,"amplitude":0.5,"offset":0.5,"step_ms":50,"duration":tcol,"start":0}}])
        score.append({"time":tcol,"value":f"SCORE {i+1:04d}","easing":"hold"})
    ap(p,[{"type":"keyframes","target":"score","property":"text","keys":score}])
    ap(p,[{"type":"animate","target":"hint","property":"opacity","from":0,"to":1,"start":300,"duration":10,"easing":"hold"}])
    return p
if __name__=="__main__":
    p=build(); print(peek(p,"s07",[200,900,1700,2600,3400,4800]))
