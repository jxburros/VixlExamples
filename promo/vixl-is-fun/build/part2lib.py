from lib import *
import glob
PANEL="#12183f"; PANEL_LINE="#2e3a8c"; DARK="#0d1024"
A=os.path.join(HERE,"work","assets")+"/"
def base(dur, bg=DARK, extra_fonts=()):
    p=new(bg,[("Bricolage Grotesque",800,"Brico"),("Space Mono",700,"Mono"),("Caveat",700,"Caveat")]+list(extra_fonts))
    ap(p,[{"type":"timeline-set","duration":dur,"fps":24,"loop":1}])
    return p
def img(p,path,name,x,y,w,h=None):
    p.import_image(path,name=name)
    ops=[{"type":"move","target":name,"x":x,"y":y}]
    ops.append({"type":"resize","target":name,"width":w,**({"height":h} if h else {})})
    ap(p,ops)
def hold(p,name,t_on,t_off=None,first_visible=False):
    keys=[{"time":0,"value":bool(first_visible),"easing":"hold"}]
    if t_on is not None and not(first_visible and t_on==0): keys.append({"time":t_on,"value":True,"easing":"hold"})
    if t_off is not None: keys.append({"time":t_off,"value":False,"easing":"hold"})
    keys=sorted({k["time"]:k for k in keys}.values(),key=lambda k:k["time"])
    ap(p,[{"type":"keyframes","target":name,"property":"visible","keys":keys}])
def panel(p,name,x,y,w,h):
    ap(p,[{"type":"shape","shape":"rounded-rectangle","name":name,"x":x,"y":y,"width":w,"height":h,"radius":20,"fill":PANEL,"stroke":PANEL_LINE,"stroke_width":3}])
def badge(p,text,x=40,y=14,color="#7b8cff",size=20):
    ap(p,[{"type":"text","name":"badge","text":text,"font":"Mono","size":size,"color":color,"x":x,"y":y}])
def code(p,name,lines,x,y,start,per=450,size=20,color="#ffffff",lh=1.35,dur=None):
    """One text layer, typed in. lines is a list of strings"""
    ap(p,[{"type":"text","name":name,"text":"\n".join(lines),"font":"Mono","size":size,"color":color,"x":x,"y":y,"line_height":lh}])
    ap(p,[{"type":"text-animate","target":name,"preset":"typewriter","start":start,"duration":dur or per*len(lines),"mode":"in"}])
def text_keys(p,name,keys):
    ap(p,[{"type":"keyframes","target":name,"property":"text","keys":[{"time":t,"value":v,"easing":"hold"} for t,v in keys]}])
