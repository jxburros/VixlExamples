import os, sys, json
BUILD = os.path.dirname(os.path.abspath(__file__))
HERE = os.path.dirname(BUILD)                      # promo/vixl-is-fun
REPO = os.path.dirname(os.path.dirname(HERE))      # this repository
if os.environ.get("VIXL_REPO"):                    # a Vixl checkout, when vixl is not installed
    sys.path.insert(0, os.path.join(os.environ["VIXL_REPO"], "src"))
sys.path.insert(0, BUILD)
from vixl import Project, VixlError
W, H = 1280, 720
OUT = os.path.join(HERE, "scenes"); os.makedirs(OUT, exist_ok=True)
PREV = os.path.join(HERE, "work", "prev"); os.makedirs(PREV, exist_ok=True)

INK="#1b1b2f"; CREAM="#fff4e0"; TOMATO="#ff5a4d"; SUN="#ffc93c"; TEAL="#14b8a6"; BLUE="#3b5bff"; PINK="#ff8fb1"; LILAC="#9b7bff"

def new(bg, fonts=()):
    p = Project(W, H, background=bg)
    from vixl.typefaces import install_font
    for fam, wt, name in fonts:
        install_font(p, fam, wt, False, name, None)
    return p

def ap(p, ops, **kw):
    r = p.apply(ops, **kw)
    return r

def save(p, name):
    path = os.path.join(OUT, name + ".vixl")
    p.save(path, overwrite=True)
    return path

def frames(p, name, times_ms):
    from PIL import Image
    ims=[]
    for t in times_ms:
        ims.append(p.render(time=t) if False else None)
    return ims

def peek(p, name, times, cols=3, w=640):
    from PIL import Image
    from vixl.timeline import render_at
    ims=[render_at(p, t).convert("RGB") for t in times]
    h = int(w*H/W)
    rows=(len(ims)+cols-1)//cols
    sheet=Image.new("RGB",(cols*w,rows*h),"#888")
    for i,im in enumerate(ims):
        sheet.paste(im.resize((w,h)),((i%cols)*w,(i//cols)*h))
    path=os.path.join(PREV,name+".png"); sheet.save(path); return path

def hop_keys(points, hop=150, up="ease-out-quad", down="ease-in-quad"):
    """points: [(t_ms, x, y)] landings. Returns (xkeys, ykeys): linear x, parabolic-ish y with apex between landings."""
    xk=[]; yk=[]
    for i,(t,x,y) in enumerate(points):
        xk.append({"time":t,"value":x,"easing":"linear"})
        yk.append({"time":t,"value":y,"easing":up})
        if i+1<len(points):
            t2,x2,y2=points[i+1]
            mid=(t+t2)//2
            yk.append({"time":mid,"value":min(y,y2)-hop,"easing":down})
    return xk,yk

def cap(p, name, text, start, end, y, color=INK, size=38, font="Brico", box=None, x="center", box_opacity=0.9, pad=(26,14), fade=300):
    """A caption baked into the shot: editable text (optionally on a rounded plate) that fades in and out."""
    ap(p, [{"type":"text","name":name+"-t","text":text,"font":font,"size":size,"color":color,"x":x,"y":y}])
    names=[name+"-t"]
    if box:
        bx,by,bw,bh=p.bounds(name+"-t")
        ap(p, [{"type":"shape","shape":"rounded-rectangle","name":name+"-b","x":bx-pad[0],"y":by-pad[1],"width":bw+2*pad[0],"height":bh+2*pad[1],"radius":18,"fill":box,"opacity":box_opacity},
               {"type":"reorder","target":name+"-b","below":name+"-t"}])
        names.insert(0,name+"-b")
    ap(p, [{"type":"group","targets":names,"name":name}])
    ap(p, [{"type":"keyframes","target":name,"property":"opacity","keys":[
        {"time":start,"value":0,"easing":"ease-out"},{"time":start+fade,"value":1,"easing":"linear"},
        {"time":end-fade,"value":1,"easing":"ease-in"},{"time":end,"value":0}]}])
