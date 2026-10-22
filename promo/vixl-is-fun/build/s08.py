from lib import *
PX=[40,449,859]; PY=40; PW=381
SKIN="#f4b183"
def human(ox,oy,k,mood="smile"):
    # origin ox,oy = panel top-left; body anchored bottom of panel art zone
    cx=ox+110; base=oy+535
    ops=[
     {"type":"shape","shape":"rounded-rectangle","name":f"h{k}-body","x":cx-70,"y":base-170,"width":140,"height":200,"radius":50,"fill":"#3b5bff"},
     {"type":"shape","shape":"ellipse","name":f"h{k}-head","x":cx-62,"y":base-330,"width":124,"height":140,"fill":SKIN},
     {"type":"shape","shape":"ellipse","name":f"h{k}-hair","x":cx-68,"y":base-346,"width":136,"height":80,"fill":"#2b1b4e"},
     {"type":"shape","shape":"ellipse","name":f"h{k}-e1","x":cx-30,"y":base-270,"width":16,"height":22 if mood!="shock" else 30,"fill":INK},
     {"type":"shape","shape":"ellipse","name":f"h{k}-e2","x":cx+14,"y":base-270,"width":16,"height":22 if mood!="shock" else 30,"fill":INK},
    ]
    if mood=="smile":
        ops.append({"type":"shape","shape":"arc","name":f"h{k}-m","x":cx-26,"y":base-232,"width":52,"height":36,"start_angle":10,"end_angle":170,"closed":False,"stroke":INK,"stroke_width":6,"line_cap":"round"})
    else:
        ops.append({"type":"shape","shape":"ellipse","name":f"h{k}-m","x":cx-18,"y":base-228,"width":36,"height":44,"fill":INK})
    return ops,[o["name"] for o in ops]
def robot(ox,oy,k,x_off=170):
    cx=ox+x_off; base=oy+535
    ops=[
     {"type":"shape","shape":"rounded-rectangle","name":f"r{k}-body","x":cx-70,"y":base-160,"width":140,"height":190,"radius":22,"fill":"#14b8a6","stroke":INK,"stroke_width":6},
     {"type":"shape","shape":"rounded-rectangle","name":f"r{k}-head","x":cx-78,"y":base-320,"width":156,"height":130,"radius":30,"fill":"#ffc93c","stroke":INK,"stroke_width":6},
     {"type":"shape","shape":"line","name":f"r{k}-ant","x":cx-2,"y":base-380,"width":4,"height":62,"stroke":INK,"stroke_width":6},
     {"type":"shape","shape":"ellipse","name":f"r{k}-ball","x":cx-14,"y":base-402,"width":28,"height":28,"fill":TOMATO,"stroke":INK,"stroke_width":5},
     {"type":"shape","shape":"ellipse","name":f"r{k}-e1","x":cx-46,"y":base-282,"width":34,"height":34,"fill":"#ffffff","stroke":INK,"stroke_width":5},
     {"type":"shape","shape":"ellipse","name":f"r{k}-e2","x":cx+12,"y":base-282,"width":34,"height":34,"fill":"#ffffff","stroke":INK,"stroke_width":5},
     {"type":"shape","shape":"ellipse","name":f"r{k}-p1","x":cx-34,"y":base-270,"width":12,"height":12,"fill":INK},
     {"type":"shape","shape":"ellipse","name":f"r{k}-p2","x":cx+24,"y":base-270,"width":12,"height":12,"fill":INK},
     {"type":"shape","shape":"rounded-rectangle","name":f"r{k}-mouth","x":cx-36,"y":base-228,"width":72,"height":14,"radius":7,"fill":INK},
    ]
    return ops,[o["name"] for o in ops]
def poster(ox,oy,k):
    x=ox+215; y=oy+300
    ops=[
     {"type":"shape","shape":"rounded-rectangle","name":f"po{k}","x":x,"y":y,"width":140,"height":180,"radius":8,"fill":"#ffffff","stroke":INK,"stroke_width":5,"rotation":-6},
     {"type":"shape","shape":"ellipse","name":f"po{k}-a","x":x+22,"y":y+22,"width":64,"height":64,"fill":PINK,"rotation":-6},
     {"type":"shape","shape":"star","name":f"po{k}-b","x":x+56,"y":y+62,"width":56,"height":56,"sides":5,"fill":SUN,"stroke":INK,"stroke_width":4,"rotation":-6},
     {"type":"shape","shape":"rectangle","name":f"po{k}-t","x":x+20,"y":y+138,"width":96,"height":14,"fill":INK,"rotation":-6},
    ]
    return ops,[o["name"] for o in ops]
def build():
    p=new("#fff8e8",[("Bricolage Grotesque",800,"Brico"),("Caveat",700,"Caveat"),("Space Mono",700,"Mono")])
    ap(p,[{"type":"timeline-set","duration":7200,"fps":24,"loop":1}])
    ap(p,[{"type":"comic-layout","name":"cm","columns":3,"gutter":28,"margin":40,"background":"#fff8e8","border":"#1b1b2f","border_width":6,"caption_size":28,
      "panels":[{"name":"p1","caption":"MON 9:00"},{"name":"p2","caption":"MON 9:01"},{"name":"p3","caption":"MON 9:02"}]}])
    # panel tint backgrounds
    for k,(c,x) in enumerate(zip(["#fff0b8","#c9f2e4","#ffd3e2"],PX),1):
        ap(p,[{"type":"shape","shape":"rectangle","name":f"tint{k}","x":x+3,"y":PY+3,"width":PW-6,"height":560,"fill":c}])
    groups={}
    h1,n1=human(PX[0],PY,1); ap(p,h1); groups[1]=n1
    r2,n2=robot(PX[1],PY,2,125); ap(p,r2)
    po,npo=poster(PX[1],PY,2); ap(p,po); groups[2]=n2+npo
    h3,n3=human(PX[2],PY,3,"shock"); ap(p,h3)
    r3,n33=robot(PX[2],PY,3,290); ap(p,r3); groups[3]=n3+n33
    for k in (1,2,3):
        ap(p,[{"type":"group","targets":[f"tint{k}"]+groups[k],"name":f"art{k}"}])
    ap(p,[
     {"type":"speech-bubble","name":"b1","text":"Make me a poster.\nSomething fun!","font":"Brico","size":30,"color":INK,"x":PX[0]+30,"y":PY+24,"max_width":330,"anchor":"h1-head","style":"speech","fill":"#ffffff","stroke":INK},
     {"type":"speech-bubble","name":"b2","text":"23 layers.\nContrast checked.","font":"Brico","size":30,"color":INK,"x":PX[1]+170,"y":PY+40,"max_width":200,"anchor":"r2-head","style":"speech","fill":"#ffffff","stroke":INK},
     {"type":"speech-bubble","name":"b3","text":"Bonus: you're\nin a comic.","font":"Brico","size":26,"color":INK,"x":PX[2]+196,"y":PY+40,"max_width":170,"anchor":"r3-head","style":"speech","fill":"#ffffff","stroke":INK},
     {"type":"speech-bubble","name":"b4","text":"WAIT,\nWHAT?!","font":"Brico","size":36,"color":"#ffffff","x":PX[2]+14,"y":PY+34,"max_width":170,"anchor":"h3-head","style":"shout","fill":TOMATO,"stroke":INK},
    ])
    T=[("cm/p1",300),("art1",300),("b1",900),("cm/p2",2100),("art2",2100),("b2",2700),("cm/p3",3900),("art3",3900),("b3",4500),("b4",5400)]
    ap(p,[{"type":"animate-preset","target":n,"preset":"pop-in","start":t,"duration":450,"easing":"ease-out-back"} for n,t in T])
    ap(p,[{"type":"camera","from":[0,0,1],"to":[409,-110,1.5],"start":6000,"duration":900,"easing":"ease-in-out"}])
    return p
if __name__=="__main__":
    p=build(); print(peek(p,"s08",[1500,3000,4800,5800,7100]))
