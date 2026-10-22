from lib import *
PARTS=['left-upper-leg','left-lower-leg','left-foot','right-upper-leg','right-lower-leg','right-foot','left-upper-arm','left-lower-arm','left-hand','right-upper-arm','right-lower-arm','right-hand','torso','head','hair','left-eye','right-eye','left-brow','right-brow','mouth']
def build():
    p=new("#ffe1ec",[("Bricolage Grotesque",800,"Brico"),("Space Mono",700,"Mono"),("Caveat",700,"Caveat")])
    ap(p,[{"type":"timeline-set","duration":7200,"fps":24,"loop":1}])
    ap(p,[
      {"type":"gradient","name":"bg","start":"#ffd5e5","end":"#ffeccf","direction":"vertical"},
      {"type":"shape","shape":"ellipse","name":"floor","x":260,"y":515,"width":760,"height":62,"fill":"#e9a6bf"},
      {"type":"shape","shape":"star","name":"st1","x":120,"y":110,"width":90,"height":90,"sides":5,"fill":SUN},
      {"type":"shape","shape":"star","name":"st2","x":1090,"y":160,"width":120,"height":120,"sides":5,"fill":LILAC},
      {"type":"shape","shape":"heart","name":"ht","x":1010,"y":470,"width":90,"height":80,"fill":TOMATO},
      {"type":"character","name":"pip","x":490,"y":70,"height":530,"colors":{"skin":"#f4b183","outfit":"#ff5a4d","hair":"#3b1f6b","eyes":"#1b1b2f"}},
    ])
    ap(p,[{"type":"cut-paper","targets":["pip","floor","st1","st2","ht"],"children":True,"grain":0.07,"roughness":0.25,"thickness":5,"fps":12,"jitter":1.2,"seed":4}])
    ap(p,[
      {"type":"animate","target":"pip","property":"translate-x","from":-760,"to":0,"start":0,"duration":2400,"easing":"ease-out"},
      {"type":"character-cycle","target":"pip","cycle":"walk","start":0,"duration":2400,"period":550},
      {"type":"character-cycle","target":"pip","cycle":"wave","start":2400,"duration":1600,"period":700},
      {"type":"speech-bubble","name":"bub","text":"Hi! I'm 20 layers.\nEvery one editable.","font":"Brico","size":34,"color":INK,"x":780,"y":90,"max_width":420,"anchor":"pip/head","style":"speech","fill":"#ffffff","stroke":INK},
    ])
    import math
    cx,cy=595,320
    LAB={"head":("head","Caveat"),"torso":("torso",""),"left-hand":("left-hand",""),"right-foot":("right-foot","")}
    ex=[]; labs=[]
    for part in PARTS:
        nm=f"pip/{part}"
        x,y,w,h=p.bounds(nm)
        mx,my=x+w/2,y+h/2
        dx,dy=mx-cx,my-cy
        if part in ("torso",): dx,dy=0,10
        ox=dx*1.7; oy=dy*(0.38 if dy>0 else 0.12)
        if part in ('hair','left-eye','right-eye','left-brow','right-brow','mouth'): ox,oy=0,-18
        if part=='head': ox,oy=0,-18
        rot={"left":-35,"right":35}.get(part.split("-")[0],0)
        keys=lambda v:[{"time":4200,"value":0,"easing":"ease-out-back"},{"time":5100,"value":v,"easing":"linear"},{"time":5900,"value":v,"easing":"ease-in-out"},{"time":6600,"value":0}]
        ex+=[{"type":"keyframes","target":nm,"property":"translate-x","keys":keys(round(ox))},
             {"type":"keyframes","target":nm,"property":"translate-y","keys":keys(round(oy))}]
        if rot: ex.append({"type":"keyframes","target":nm,"property":"rotation","keys":keys(rot)})
        if part in ("head","torso","left-hand","right-foot"):
            labs.append((part,mx+ox,my+oy))
    ap(p,ex)
    lops=[]
    for part,mx,my in labs:
        side=-1 if "left" in part else 1
        lx={"head":mx+95,"torso":mx-38,"left-hand":mx-150,"right-foot":mx+55}[part]
        ly=my-22 if part!="torso" else my-8
        lops.append({"type":"text","name":f"lab-{part}","text":part,"font":"Caveat","size":40,"color":("#ffffff" if part=="torso" else "#b3124a"),"x":round(lx),"y":round(ly),"opacity":0})
    ap(p,lops)
    for part,_,_ in labs:
        ap(p,[{"type":"keyframes","target":f"lab-{part}","property":"opacity","keys":[{"time":4800,"value":0,"easing":"ease-out"},{"time":5200,"value":1,"easing":"linear"},{"time":5800,"value":1,"easing":"ease-in"},{"time":6200,"value":0}]}])
    ap(p,[{"type":"animate-preset","target":"bub","preset":"pop-in","start":2500,"duration":500,"easing":"ease-out-back"},
          {"type":"animate-preset","target":"bub","preset":"pop-out","start":3900,"duration":300}])
    cap(p,"cap","Everything is a layer. Everything stays editable.",4300,7000,628,color=INK,size=36)
    return p
if __name__=="__main__":
    p=build(); print(peek(p,"s05",[1200,3000,4600,5600,6900]))
    from vixl.timeline import render_at
    render_at(p,0).convert("RGB").save(os.path.join(PREV,"s05_full.png"))
    print([l["name"] for l in p.inspect()["layers"]][:30])
