from lib import *
CW,CH=280,290
def pos(i):
    col,row=i%4,i//4
    return 32+col*(CW+32), 80+row*(CH+26)
def card(p,i,label,fill="#ffffff",lab_color=INK,content=None):
    x,y=pos(i)
    names=[]
    ap(p,[{"type":"shape","shape":"rounded-rectangle","name":f"sh{i}","x":x+8,"y":y+8,"width":CW,"height":CH,"radius":22,"fill":INK},
          {"type":"shape","shape":"rounded-rectangle","name":f"cd{i}","x":x,"y":y,"width":CW,"height":CH,"radius":22,"fill":fill,"stroke":INK,"stroke_width":5}])
    names+= [f"sh{i}",f"cd{i}"]
    if content: names+=content(x,y)
    ap(p,[{"type":"text","name":f"lb{i}","text":label,"font":"Mono","size":24,"color":lab_color,"x":x+CW/2-len(label)*7.2,"y":y+CH-42}])
    names.append(f"lb{i}")
    ap(p,[{"type":"group","targets":names,"name":f"card{i}"}])
    return f"card{i}"
def c_qr(x,y):
    ap(p_,[{"type":"qr","name":"qr1","data":"https://github.com/jxburros/Vixl","x":x+42,"y":y+22,"size":196,"color":INK,"background":"#ffffff"}]); return ["qr1"]
def c_bar(x,y):
    ap(p_,[{"type":"barcode","name":"bar1","data":"400638133393","symbology":"ean13","x":x+22,"y":y+55,"width":236,"height":150,"color":INK}]); return ["bar1"]
def c_cut(x,y):
    ap(p_,[{"type":"organic","name":"octo","preset":"octopus","seed":3,"x":x+55,"y":y+28,"width":170,"height":190,"fill":"#ff8fb1"}])
    ap(p_,[{"type":"die-cut","targets":["octo"],"distance":12,"name":"cutline","stroke":"#e11d8c","stroke_width":3}]); return ["octo","cutline"]
def c_tear(x,y):
    ap(p_,[{"type":"shape","shape":"rectangle","name":"paper","x":x+24,"y":y+24,"width":232,"height":200,"fill":"#ffd8a8"},
           {"type":"text","name":"paper-t","text":"torn\nedges","font":"Caveat","size":64,"color":"#b3124a","x":x+70,"y":y+60,"line_height":0.95}])
    ap(p_,[{"type":"tear","target":"paper","seed":4,"strength":"rough","edges":["bottom"],"depth":34,"length":40}]); return ["paper","paper-t"]
def c_lights(x,y):
    ap(p_,[{"type":"string-lights","name":"lights1","from":[x+14,y+34],"to":[x+266,y+34],"sag":38,"bulb":"lantern","size":30,"count":5,"colors":["#ffd77a","#ff8fb1","#5ef2e0"],"seed":2},
           {"type":"string-lights","name":"lights2","from":[x+14,y+130],"to":[x+266,y+130],"sag":30,"bulb":"globe","size":26,"count":7,"colors":["#ffc93c","#ff5a4d","#9b7bff"],"seed":5}])
    ap(p_,[{"type":"top","target":"lights1"},{"type":"top","target":"lights2"}]); return ["lights1","lights2"]
def c_chart(x,y):
    ap(p_,[{"type":"chart","name":"chart1","kind":"bar","x":x+16,"y":y+22,"width":248,"height":210,"categories":["Q1","Q2","Q3","Q4"],"series":[{"name":"fun","values":[3,5,8,13],"color":TOMATO}],"legend":"none","title":None,"value_labels":True,"font_size":16,"label_font":"Mono"}]); return ["chart1"]
def c_diag(x,y):
    ap(p_,[{"type":"diagram-from-text","name":"diag1","text":"idea -> draft\ndraft -> check\ncheck -> ship","direction":"TB","x":x+20,"y":y+18,"width":240,"height":214,"size":18,"font":"Mono","fit":"contain"}]); return ["diag1"]
def c_emoji(x,y):
    ap(p_,[{"type":"text","name":"emo","text":"🎨🚀\n🐙✨","size":84,"x":x+34,"y":y+34,"line_height":1.15}]); return ["emo"]
def build():
    global p_
    p_=new("#ffd84d",[("Bricolage Grotesque",800,"Brico"),("Space Mono",700,"Mono"),("Caveat",700,"Caveat")])
    p=p_
    ap(p,[{"type":"timeline-set","duration":6000,"fps":24,"loop":1},
          {"type":"text","name":"head","text":"the junk drawer","font":"Brico","size":44,"color":INK,"x":32,"y":16}])
    cards=[]
    cards.append(card(p,0,"qr",content=c_qr))
    cards.append(card(p,1,"barcode",content=c_bar))
    cards.append(card(p,2,"die-cut",fill="#d9f7ff",content=c_cut))
    cards.append(card(p,3,"tear",fill="#ffffff",content=c_tear))
    cards.append(card(p,4,"string-lights",fill="#241c4a",lab_color="#ffffff",content=c_lights))
    cards.append(card(p,5,"chart",content=c_chart))
    cards.append(card(p,6,"diagram-from-text",content=c_diag))
    cards.append(card(p,7,"emoji",fill="#ffe3f0",content=c_emoji))
    ap(p,[{"type":"animate-preset","target":c,"preset":"pop-in","start":300+i*300,"duration":500,"easing":"ease-out-back"} for i,c in enumerate(cards)])
    ap(p,[{"type":"motion","recipe":"wiggle","targets":cards,"amount":1.6,"frequency":0.7,"stagger":110,"start":3000,"duration":3000}])
    ap(p,[{"type":"text","name":"sub","text":"niche, on purpose.","font":"Mono","size":28,"color":INK,"x":930,"y":28}])
    return p
if __name__=="__main__":
    p=build(); print(peek(p,"s09",[1000,3800]))
    from vixl.timeline import render_at
    render_at(p,3800).convert("RGB").save(os.path.join(PREV,"s09_full.png"))
