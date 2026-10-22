from lib import *
GROUND=620
# (preset, center x, size w, h, seed, stem height or None)
SPEC=[("sunflower",150,210,210,3,270),("fern",290,120,260,4,None),("tree",440,250,330,2,None),("mushroom",600,120,150,5,None),
      ("cactus",710,120,250,1,None),("rose",850,150,150,6,230),("pine",1000,190,320,2,None),("daisy",1170,140,140,8,200)]
def build():
    p = new("#cfeeff", [("Bricolage Grotesque",800,"Brico"),("Space Mono",700,"Mono")])
    ap(p, [{"type":"timeline-set","duration":4800,"fps":24,"loop":1}])
    ap(p, [
      {"type":"gradient","name":"sky","start":"#7ccbff","end":"#fff1d6","direction":"vertical"},
      {"type":"shape","shape":"sun","name":"sun","x":1010,"y":50,"width":190,"height":190,"fill":SUN},
      {"type":"shape","shape":"cloud","name":"cloud1","x":120,"y":90,"width":240,"height":110,"fill":"#ffffff","opacity":0.9},
      {"type":"shape","shape":"cloud","name":"cloud2","x":600,"y":160,"width":170,"height":80,"fill":"#ffffff","opacity":0.8},
      {"type":"shape","shape":"ellipse","name":"hill-back","x":-200,"y":470,"width":1000,"height":500,"fill":"#7fd6a0"},
      {"type":"shape","shape":"ellipse","name":"hill-back2","x":600,"y":500,"width":1100,"height":500,"fill":"#6cc891"},
      {"type":"shape","shape":"ellipse","name":"hill-front","x":-100,"y":600,"width":1500,"height":380,"fill":"#2f9e6a"},
    ])
    groups=[]
    for pre,cx,w,h,seed,stem in SPEC:
        nm=f"g-{pre}"; ops=[]
        if stem:
            ops.append({"type":"shape","shape":"line","name":f"stem-{pre}","x":cx-4,"y":GROUND-stem,"width":8,"height":stem,"stroke":"#2d7d4f","stroke_width":9,"line_cap":"round"})
            top=GROUND-stem-h//2
        else:
            top=GROUND-h
        ops.append({"type":"organic","name":f"o-{pre}","preset":pre,"seed":seed,"x":cx-w//2,"y":top,"width":w,"height":h})
        ops.append({"type":"text","name":f"lab-{pre}","text":f"\"{pre}\"","font":"Mono","size":17,"color":"#eafff3","x":cx-(len(pre)+2)*5.3,"y":GROUND+42})
        members=[o["name"] for o in ops]
        ap(p, ops)
        ap(p, [{"type":"group","targets":members[:-1],"name":nm}])
        groups.append(nm)
    ap(p, [{"type":"rasterize","target":g} for g in groups])
    ap(p, [{"type":"pivot","targets":groups,"value":"bottom"}])
    labs=[f"lab-{s[0]}" for s in SPEC]
    ap(p, [
      {"type":"animate-preset","targets":groups,"preset":"pop-in","start":300,"duration":600,"stagger":270,"easing":"ease-out-back"},
      {"type":"animate-preset","targets":labs,"preset":"fade-in","start":400,"duration":400,"stagger":270},
      {"type":"motion","recipe":"wiggle","targets":groups,"amount":2.2,"frequency":0.5,"stagger":140,"start":2800,"duration":2000},
      {"type":"animate","target":"cloud1","property":"translate-x","from":0,"to":160,"start":0,"duration":4800,"easing":"linear"},
      {"type":"animate","target":"cloud2","property":"translate-x","from":0,"to":-120,"start":0,"duration":4800,"easing":"linear"},
      {"type":"motion","recipe":"spin","target":"sun","turns":1,"start":0,"duration":4800},
    ])
    cap(p,"cap","34 things that grow. Same seed, same flower.",1200,4700,56,color=INK,size=40,box="#ffffffcc",box_opacity=1)
    return p
if __name__=="__main__":
    p=build(); print(peek(p,"s03",[300,900,1800,2600,3400,5000]))
