from part2lib import *
import json, re
def x2():
    DUR=7200
    p=base(DUR)
    nf=len(glob.glob(A+"paint/f*.jpg"))
    ap(p,[{"type":"shape","shape":"rectangle","name":"bgfill","x":36,"y":56,"width":728,"height":458,"fill":"#05060f"}])
    t0=300; per=120
    for k in range(nf):
        img(p,A+f"paint/f{k+1:03d}.jpg",f"pf{k}",40,60,720,450); hold(p,f"pf{k}",t0+k*per)
    V=[("variant-watercolor","watercolor"),("variant-oil-paint","oil-paint"),("variant-riso-halftone","riso halftone"),("variant-pencil-sketch","pencil sketch")]
    tv=t0+nf*per+100
    for i,(f,lab) in enumerate(V):
        img(p,A+f"misc/{f}.jpg",f"v{i}",40,60,720,450); hold(p,f"v{i}",tv+i*480)
    ap(p,[{"type":"text","name":"lab","text":"timelapse: 26 paint layers, in painting order","font":"Mono","size":22,"color":"#c9b8ff","x":44,"y":524}])
    text_keys(p,"lab",[(0,"timelapse: 26 paint layers, in painting order")]+[(tv+i*480,f"same document, filter: {lab}") for i,(f,lab) in enumerate(V)])
    panel(p,"panel",790,56,452,458)
    ap(p,[{"type":"text","name":"hdr","text":"05-generative-painting","font":"Mono","size":20,"color":"#7b8cff","x":814,"y":76}])
    code(p,"c1",['{"type":"brush-define",','"name":"reed","base":"brush-pen",','"settings":{"taper":[0.05,0.5],','"roundness":0.6,"angle":70}}'],814,128,500,per=380,size=19,color=SUN)
    code(p,"c2",['{"type":"paint","target":"reeds",','"brush":"reed",','"points":[[212,880],[220,790],…]}'],814,296,2300,per=380,size=19,color="#ffffff")
    ap(p,[{"type":"text","name":"c3","text":"one seeded RNG\ndrives every stroke","font":"Brico","size":34,"color":CREAM,"x":814,"y":432,"line_height":1.02}])
    ap(p,[{"type":"animate-preset","target":"c3","preset":"fade-in","start":3500,"duration":500}])
    stats=["3,723 strokes","26 paint layers","17 brushes + 4 custom"]
    for i,s in enumerate(stats):
        ap(p,[{"type":"text","name":f"st{i}","text":s,"font":"Brico","size":40,"color":[SUN,PINK,"#5ef2e0"][i],"x":[44,372,742][i],"y":596}])
        ap(p,[{"type":"animate-preset","target":f"st{i}","preset":"pop-in","start":1500+i*700,"duration":450,"easing":"ease-out-back"}])
    return p
def x3():
    DUR=7200
    p=base(DUR,"#14112b",[("Press Start 2P",400,"Px")])
    src=open(os.path.join(REPO,"explorations","04-pixel-rpg","build.py")).read()
    body=re.search(r'HERO_BODY = grid\("""\n(.*?)"""\)',src,re.S).group(1)
    legs=re.search(r'"stand": grid\("""\n(.*?)"""\)',src,re.S).group(1)
    rows=[l.strip() for l in (body+"\n"+legs).strip().splitlines() if l.strip()]
    pal={".":"transparent","o":"#1a1c2c","c":"#b13e53","C":"#ef7d57","h":"#5d275d","s":"#ffcd75","S":"#ef7d57","e":"#1a1c2c","t":"#3b5dc9","T":"#29366f","b":"#5d275d","y":"#ffcd75","p":"#566c86","P":"#333c57","k":"#5d275d","K":"#1a1c2c","w":"#f4f4f4"}
    W=len(rows[0]); N=len(rows)
    SC=26
    ap(p,[{"type":"text","name":"hdr","text":"explorations/04-pixel-rpg","font":"Mono","size":22,"color":"#73eff7","x":60,"y":30}])
    ap(p,[{"type":"text","name":"rowsT","text":'"rows": [',"font":"Mono","size":22,"color":"#ffcd75","x":60,"y":90}])
    lines=[f'  "{r}",' for r in rows]
    names=["hdr","rowsT"]
    ap(p,[{"type":"text","name":"rowsC","text":"\n".join(lines),"font":"Mono","size":22,"color":"#f4f4f4","x":60,"y":118,"line_height":1.0}])
    ap(p,[{"type":"text-animate","target":"rowsC","preset":"typewriter","start":300,"duration":2000,"mode":"in"}])
    names+=["rowsC"]
    # sprite built up row by row, in step with the typing
    for k in range(1,N+1):
        r=[(row if i<k else "."*W) for i,row in enumerate(rows)]
        ap(p,[{"type":"pixel-art","name":f"sp{k}","x":640,"y":120,"palette":pal,"rows":r,"shading":False,"outline":False},
              {"type":"resize","target":f"sp{k}","width":W*SC,"height":N*SC}])
        hold(p,f"sp{k}",300+int(2000*(k-1)/N)+60)
        names.append(f"sp{k}")
    ap(p,[{"type":"text","name":"cap","text":"a 16×16 hero is 16 strings and a palette","font":"Px","size":16,"color":"#73eff7","x":"center","y":610}])
    names.append("cap")
    ap(p,[{"type":"group","targets":names,"name":"partA"}])
    hold(p,"partA",0,2400,first_visible=True)
    # part B: the animated overworld
    nf=len(glob.glob(A+"map/f*.png"))
    for k in range(nf):
        img(p,A+f"map/f{k+1:03d}.png",f"mf{k}",160,40,960,576); hold(p,f"mf{k}",2400+int(k*1000/12)+0)
    ap(p,[{"type":"text","name":"capB","text":"frame-save · visible keys · steps() easing: it moves in whole pixels","font":"Mono","size":22,"color":"#ffcd75","x":"center","y":650}])
    hold(p,"capB",2400)
    return p
if __name__=="__main__":
    for n,f,t in (("x2",x2,[400,2000,4500,5400,6000,7000]),("x3",x3,[400,1300,2300,2800,4500,7100])):
        p=f(); print(n,peek(p,n,t))
