from lib import *
import math

def chip(label, color, bg=None, x=48, y=640, font="Mono", size=26):
    ops=[]
    ops.append({"type":"text","name":"chip","text":f"style: \"{label}\"","font":font,"size":size,"color":color,"x":x,"y":y})
    return ops

def bauhaus():
    p=new("#f3ead7",[("Archivo Black",400,"Arch"),("Space Mono",700,"Mono")])
    ap(p,[
     {"type":"shape","shape":"ellipse","name":"c","x":640,"y":-60,"width":560,"height":560,"fill":"#e63322"},
     {"type":"shape","shape":"rectangle","name":"bar","x":0,"y":470,"width":1280,"height":60,"fill":"#111111"},
     {"type":"shape","shape":"isosceles-triangle","name":"tri","x":980,"y":330,"width":260,"height":300,"fill":"#1d4ed8"},
     {"type":"shape","shape":"rectangle","name":"sq","x":90,"y":90,"width":160,"height":160,"fill":"#f5c400"},
     {"type":"text","name":"title","text":"VIXL","font":"Arch","size":300,"color":"#111111","x":80,"y":230,"tracking":-8},
     {"type":"text","name":"sub","text":"make something.","font":"Arch","size":44,"color":"#111111","x":96,"y":560},
    ]+chip("bauhaus","#111111",x=700,y=640))
    return p
def vaporwave():
    p=new("#ff77d4",[("Monoton",400,"Mono2"),("Space Mono",700,"Mono")])
    ap(p,[
     {"type":"gradient","name":"sky","start":"#2b0a6b","end":"#ff77d4","direction":"vertical","stops":[{"offset":0,"color":"#1b0a5c"},{"offset":0.55,"color":"#b44bd8"},{"offset":0.62,"color":"#ff77d4"},{"offset":1,"color":"#ffb36b"}]},
     {"type":"shape","shape":"ellipse","name":"sun","x":440,"y":170,"width":400,"height":400,"fill_gradient":{"stops":[{"offset":0,"color":"#ffe36b"},{"offset":1,"color":"#ff4f9a"}],"direction":"vertical"}},
     {"type":"shape","shape":"rectangle","name":"floor","x":0,"y":440,"width":1280,"height":280,"fill":"#1b0a5c"},
    ])
    ops=[]
    for i in range(8):
        y=470+i*i*5+i*8
        ops.append({"type":"shape","shape":"line","name":f"h{i}","x":0,"y":y,"width":1280,"height":2,"stroke":"#5ef2e0","stroke_width":2})
    for i in range(-8,9):
        ops.append({"type":"shape","shape":"path","name":f"v{i}","x":0,"y":440,"path":f"M {640+i*40} 0 L {640+i*200} 280","fill":"none","stroke":"#5ef2e0","stroke_width":2})
    ap(p,ops)
    # stripes across sun
    ap(p,[{"type":"shape","shape":"rectangle","name":f"cut{i}","x":430,"y":340+i*30,"width":420,"height":6+i*3,"fill":"#b44bd8"} for i in range(6)])
    ap(p,[
     {"type":"text","name":"title","text":"VIXL","font":"Mono2","size":210,"color":"#5ef2e0","x":"center","y":40},
     {"type":"text","name":"sub","text":"m a k e   s o m e t h i n g","font":"Mono","size":34,"color":"#ffffff","x":"center","y":600},
    ]+chip("vaporwave","#ffffff",x=40,y=660))
    return p
def neobrutal():
    p=new("#ffd84d",[("Space Grotesk",700,"Grot"),("Space Mono",700,"Mono")])
    ap(p,[
     {"type":"shape","shape":"rounded-rectangle","name":"shadow","x":150,"y":140,"width":980,"height":440,"radius":28,"fill":"#111111"},
     {"type":"shape","shape":"rounded-rectangle","name":"card","x":120,"y":110,"width":980,"height":440,"radius":28,"fill":"#ffffff","stroke":"#111111","stroke_width":8},
     {"type":"shape","shape":"rounded-rectangle","name":"btn-sh","x":724,"y":444,"width":420,"height":90,"radius":20,"fill":"#111111"},
     {"type":"shape","shape":"rounded-rectangle","name":"btn","x":710,"y":430,"width":420,"height":90,"radius":20,"fill":"#ff6ec7","stroke":"#111111","stroke_width":6},
     {"type":"text","name":"btn-t","text":"MAKE IT →","font":"Grot","size":44,"color":"#111111","x":800,"y":446},
     {"type":"text","name":"title","text":"VIXL","font":"Grot","size":250,"color":"#111111","x":160,"y":120,"tracking":-8},
     {"type":"text","name":"sub","text":"make something.","font":"Grot","size":52,"color":"#111111","x":166,"y":400},
     {"type":"shape","shape":"star","name":"star","x":1000,"y":40,"width":190,"height":190,"sides":10,"inner_radius":0.6,"fill":"#5ef2a0","stroke":"#111111","stroke_width":7,"rotation":12},
    ]+chip("neo-brutalist","#111111",x=48,y=640))
    return p
def riso():
    p=new("#f4efe2",[("Bricolage Grotesque",800,"Brico"),("Space Mono",700,"Mono")])
    ap(p,[
     {"type":"shape","shape":"ellipse","name":"pink","x":160,"y":90,"width":620,"height":620,"fill":"#ff48b0"},
     {"type":"shape","shape":"ellipse","name":"blue","x":420,"y":140,"width":620,"height":620,"fill":"#0078bf"},
     {"type":"text","name":"title","text":"VIXL","font":"Brico","size":330,"color":"#f4efe2","x":"center","y":150},
    ])
    ap(p,[
     {"type":"blend","target":"blue","mode":"multiply"},
     {"type":"look","target":"pink","look":"risograph"},
     {"type":"look","target":"blue","look":"risograph"},
     {"type":"text","name":"sub","text":"make something.","font":"Mono","size":34,"color":"#0078bf","x":48,"y":32},
    ]+chip("risograph","#ff48b0",x=900,y=32))
    return p
def deco():
    p=new("#0e1a2b",[("Cinzel",700,"Cinzel"),("Space Mono",700,"Mono")])
    ap(p,[{"type":"shape","shape":"rectangle","name":"ray","x":636,"y":70,"width":8,"height":310,"fill":"#d4af37"}])
    ap(p,[{"type":"radial-repeat","target":"ray","count":25,"cx":640,"cy":470,"sweep":180,"start_angle":-90,"name":"fan"}])
    ap(p,[
     {"type":"shape","shape":"rectangle","name":"mask0","x":0,"y":0,"width":1,"height":1,"fill":"#0e1a2b","opacity":0},
     {"type":"shape","shape":"ellipse","name":"disc","x":560,"y":390,"width":160,"height":160,"fill":"#0e1a2b","stroke":"#d4af37","stroke_width":8},
     {"type":"shape","shape":"rectangle","name":"mask","x":0,"y":470,"width":1280,"height":250,"fill":"#0e1a2b"},
     {"type":"shape","shape":"rectangle","name":"line1","x":240,"y":482,"width":800,"height":4,"fill":"#d4af37"},
     {"type":"text","name":"title","text":"VIXL","font":"Cinzel","size":130,"color":"#d4af37","x":"center","y":500,"tracking":18},
     {"type":"text","name":"sub","text":"M A K E   S O M E T H I N G","font":"Cinzel","size":30,"color":"#f3e6b3","x":"center","y":640},
    ]+chip("art-deco","#d4af37",x=48,y=670,size=22))
    return p
def y2k():
    p=new("#cfe8ff",[("Fredoka",600,"Fred"),("Space Mono",700,"Mono")])
    ap(p,[
     {"type":"gradient","name":"bg","start":"#e9f4ff","end":"#9fc4ff","direction":"angled","angle":120},
     {"type":"shape","shape":"ellipse","name":"orb","x":330,"y":60,"width":640,"height":640,"fill_gradient":{"direction":"radial","center":[0.35,0.3],"stops":[{"offset":0,"color":"#ffffff"},{"offset":0.5,"color":"#9fd0ff"},{"offset":1,"color":"#4d7bff"}]},"stroke":"#ffffff","stroke_width":6},
     {"type":"shape","shape":"ellipse","name":"hi","x":440,"y":110,"width":300,"height":150,"fill":"#ffffff","opacity":0.65},
     {"type":"shape","shape":"sparkle","name":"sp1","x":120,"y":120,"width":120,"height":120,"fill":"#ffffff"},
     {"type":"shape","shape":"sparkle","name":"sp2","x":1050,"y":420,"width":150,"height":150,"fill":"#ffffff"},
     {"type":"shape","shape":"sparkle","name":"sp3","x":1020,"y":90,"width":80,"height":80,"fill":"#ff9de2"},
     {"type":"text","name":"title","text":"vixl","font":"Fred","size":280,"color":"#ffffff","x":"center","y":250,"tracking":-4},
     {"type":"text","name":"sub","text":"make something ✦","font":"Fred","size":46,"color":"#2f4fb8","x":"center","y":520},
    ]+chip("y2k","#2f4fb8",x=48,y=660))
    ap(p,[{"type":"layer-style","target":"title","style":"drop-shadow","color":"#2f4fb8","blur":8,"offset":[0,10],"opacity":0.55}]) if False else None
    return p
def japanese():
    p=new("#f5f1e8",[("Cinzel",700,"Cinzel"),("Space Mono",700,"Mono")])
    ap(p,[
     {"type":"shape","shape":"ellipse","name":"seal","x":1000,"y":120,"width":150,"height":150,"fill":"#c8372d"},
     {"type":"shape","shape":"line","name":"ink","x":200,"y":500,"width":640,"height":2,"stroke":"#222222","stroke_width":2},
     {"type":"text","name":"title","text":"vixl","font":"Mono","size":120,"color":"#222222","x":200,"y":330,"tracking":22},
     {"type":"text","name":"sub","text":"make something.","font":"Mono","size":24,"color":"#8a8478","x":204,"y":530,"tracking":6},
    ]+chip("japanese-minimal","#8a8478",x=48,y=660,size=22))
    return p
def pixel():
    p=new("#14112b",[("Press Start 2P",400,"Px"),("Space Mono",700,"Mono")])
    ap(p,[
     {"type":"text","name":"title","text":"VIXL","font":"Px","size":170,"color":"#ffd84d","x":"center","y":210},
     {"type":"text","name":"sub","text":"PRESS START","font":"Px","size":34,"color":"#ffffff","x":"center","y":520},
     {"type":"text","name":"hi","text":"HI-SCORE 099999","font":"Px","size":22,"color":"#5ef2a0","x":60,"y":50},
     {"type":"pixel-art","name":"ship","x":1020,"y":400,"palette":{"#":"#ff5a4d","o":"#ffd84d",".":"#14112b","w":"#ffffff"},
      "rows":["...##...","..####..",".######.","#wwwwww#","########","#.#..#.#","#......#"],"shading":False,"outline":False},
     {"type":"resize","target":"ship","width":120,"height":105},
    ]+chip("pixel-art","#5ef2a0",x=48,y=660,font="Px",size=18))
    return p
STYLES=[("s04a_bauhaus",bauhaus),("s04b_vapor",vaporwave),("s04c_neobrutal",neobrutal),("s04d_riso",riso),("s04e_deco",deco),("s04f_y2k",y2k),("s04g_japanese",japanese),("s04h_pixel",pixel)]
if __name__=="__main__":
    from PIL import Image
    import sys
    ims=[]
    for n,f in STYLES:
        try:
            p=f(); p.export(os.path.join(PREV,n+".png"),overwrite=True); ims.append(Image.open(os.path.join(PREV,n+".png")).convert("RGB").resize((640,360)))
        except Exception as e:
            print(n,"ERR",str(e)[:600]); ims.append(Image.new("RGB",(640,360),"red"))
    sheet=Image.new("RGB",(1280,360*4))
    for i,im in enumerate(ims): sheet.paste(im,((i%2)*640,(i//2)*360))
    sheet.save(os.path.join(PREV,"s04.png"))

def intro():
    p=new(INK,[("Bricolage Grotesque",800,"Brico"),("Space Mono",700,"Mono")])
    ap(p,[{"type":"timeline-set","duration":2400,"fps":24,"loop":1}])
    ap(p,[
      {"type":"text","name":"a","text":"same words.","font":"Brico","size":170,"color":CREAM,"x":"center","y":130,"tracking":-4},
      {"type":"text","name":"b","text":"28 outfits.","font":"Brico","size":170,"color":SUN,"x":"center","y":330,"tracking":-4},
      {"type":"shape","shape":"star","name":"s1","x":120,"y":520,"width":90,"height":90,"sides":4,"inner_radius":0.3,"fill":PINK},
      {"type":"shape","shape":"star","name":"s2","x":1080,"y":90,"width":70,"height":70,"sides":4,"inner_radius":0.3,"fill":TEAL},
    ])
    ap(p,[
      {"type":"animate-preset","target":"a","preset":"slide-in-up","start":0,"duration":500,"distance":50,"fade":True},
      {"type":"animate-preset","target":"b","preset":"slide-in-up","start":500,"duration":500,"distance":50,"fade":True},
      {"type":"animate-preset","targets":["s1","s2"],"preset":"pop-in","start":300,"duration":400,"stagger":200},
    ])
    return p
