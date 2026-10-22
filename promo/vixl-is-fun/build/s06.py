from lib import *
CX,CY=640,360
def ring(p,name,shape,count,r_in,r_out,w,fill,extra=None,spin_turns=3,**kw):
    h=r_out-r_in
    op={"type":"shape","shape":shape,"name":name+"-seed","x":CX-w/2,"y":CY-r_out,"width":w,"height":h,"fill":fill}
    if extra: op.update(extra)
    ap(p,[op])
    ap(p,[{"type":"radial-repeat","target":name+"-seed","count":count,"cx":CX,"cy":CY,"name":name}])
def build():
    p=new("#1a0f3a",[("Bricolage Grotesque",800,"Brico"),("Space Mono",700,"Mono")])
    ap(p,[{"type":"timeline-set","duration":4800,"fps":24,"loop_mode":"seamless"}])
    ap(p,[{"type":"gradient","name":"bg","start":"#3b1d7a","end":"#0e0724","direction":"radial"}])
    ring(p,"r1","teardrop",24,250,345,48,"#ff8fb1")
    ring(p,"r2","diamond",16,165,265,56,"#ffc93c")
    ring(p,"r3","ellipse",12,85,180,48,"#14b8a6")
    ring(p,"r4","star",8,22,100,50,"#9b7bff",extra={"sides":4,"inner_radius":0.35})
    ap(p,[{"type":"shape","shape":"ellipse","name":"core","x":CX-34,"y":CY-34,"width":68,"height":68,"fill":"#fff4e0","stroke":"#ff5a4d","stroke_width":8}])
    ap(p,[
      {"type":"text","name":"codeL","text":"radial-repeat\n  count: 24\n  mirror: false","font":"Mono","size":26,"color":"#c9b8ff","x":50,"y":300,"line_height":1.4},
      {"type":"text","name":"codeR","text":"spin\n  turns: 6\n  symmetry: 24\n  -> loops forever","font":"Mono","size":26,"color":"#ffd9a0","x":960,"y":290,"line_height":1.4},
    ])
    cap(p,"cap","Symmetry is a one-liner.",300,4600,640,color="#ffffff",size=38,box="#1a0f3a",box_opacity=0.85)
    return p
def motion(p):
    ap(p,[
      {"type":"motion","recipe":"spin","target":"r1","turns":6,"symmetry":24,"duration":4800},
      {"type":"motion","recipe":"spin","target":"r2","turns":-6,"symmetry":16,"duration":4800},
      {"type":"motion","recipe":"spin","target":"r3","turns":12,"symmetry":12,"duration":4800},
      {"type":"motion","recipe":"spin","target":"r4","turns":-8,"symmetry":8,"duration":4800},
      {"type":"motion","recipe":"breathing","targets":["core"],"amount":18,"period":1200,"duration":4800},
    ])
if __name__=="__main__":
    p=build(); motion(p); print(peek(p,"s06",[0,800,1600,2400,3200,4700]))
