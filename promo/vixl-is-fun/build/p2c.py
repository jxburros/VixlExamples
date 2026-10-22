from part2lib import *
def x4():
    DUR=7200
    p=base(DUR,"#0b0c1f")
    # phase A: the poster and the three snippets that make it
    img(p,A+"misc/poster.jpg","poster",50,22,441,676)
    panel(p,"panelA",540,40,700,640)
    ap(p,[{"type":"text","name":"hdrA","text":"01-print-concert-poster","font":"Mono","size":20,"color":"#7b8cff","x":566,"y":60}])
    items=[("sun slices thicken toward the horizon",['{"type":"repeat-blend","target":"slice","count":9,','"dy":8,"dh":3,"end":{"height":30,"fill":"@dusk-500"}}']),
           ("headline bent into an arc",['{"type":"text-layout","target":"title",','"width":790,"height":165,"warp":"arc","amount":0.2}']),
           ("pinned to the print safe area",['{"type":"constrain","target":"title","constraints":','{"center-x":"canvas.center-x",','"top":"guide:safe-top.top+70"}}'])]
    names=["poster","panelA","hdrA"]
    for i,(lab,lines) in enumerate(items):
        y=110+i*190
        ap(p,[{"type":"text","name":f"lab{i}","text":lab,"font":"Brico","size":30,"color":SUN,"x":566,"y":y}])
        code(p,f"cd{i}",lines,566,y+44,400+i*1000,per=300,size=21)
        names+= [f"lab{i}",f"cd{i}"]
        ap(p,[{"type":"animate-preset","target":f"lab{i}","preset":"fade-in","start":300+i*1000,"duration":300}])
    ap(p,[{"type":"group","targets":names,"name":"A"}]); hold(p,"A",0,3600,first_visible=True)
    # phase B: soft proofs
    img(p,A+"misc/compare.jpg","cmp",50,28,1180,619)
    ap(p,[{"type":"text","name":"cmpT","text":"vixl export --proof --icc swop.icc --ink-limit 300","font":"Mono","size":26,"color":"#ffcd75","x":"center","y":660}])
    ap(p,[{"type":"group","targets":["cmp","cmpT"],"name":"B"}]); hold(p,"B",3600,5400)
    # phase C
    img(p,A+"misc/cvd.jpg","cvd",50,28,1180,626)
    ap(p,[{"type":"text","name":"cvdT","text":"vixl export --simulate deuteranopia      (…protanopia, tritanopia)","font":"Mono","size":26,"color":"#73eff7","x":"center","y":664}])
    ap(p,[{"type":"group","targets":["cvd","cvdT"],"name":"C"}]); hold(p,"C",5400)
    return p
def x5():
    DUR=4800
    p=base(DUR,"#0d1024")
    panel(p,"panel",40,70,520,570)
    ap(p,[{"type":"text","name":"hdr","text":"07-trading-cards/data/cards.csv","font":"Mono","size":20,"color":"#7b8cff","x":66,"y":92}])
    rows=["name,element,rarity,atk,def,spd","Cinderwisp,Ember,Common,2,1,4","Tidecaller Maru,Tide,Rare,2,4,3","Mossback Elder,Grove,Common,3,6,1","… 10 more rows (and a 70-character name,","  CJK, emoji and a placeholder row)"]
    code(p,"csv",rows,66,140,300,per=380,size=19,color="#ffffff",lh=1.5)
    ap(p,[{"type":"text","name":"cmd","text":"vixl -p template.vixl\n  render --data cards.csv\n  --comp holo","font":"Mono","size":24,"color":"#ffcd75","x":66,"y":420,"line_height":1.3}])
    ap(p,[{"type":"animate-preset","target":"cmd","preset":"fade-in","start":2200,"duration":400}])
    ap(p,[{"type":"text","name":"cap","text":"one template.\n13 cards.","font":"Brico","size":46,"color":CREAM,"x":66,"y":540,"line_height":0.95}]) if False else None
    cards=["card-standard-0001","card-standard-0003","card-standard-0004","card-holo-0006"]
    W,H=330,462
    for i,c in enumerate(cards):
        x=600+i*0+(i%2)*0
    pos=[(600,70),(790,120),(980,70),(870,260)]
    names=[]
    for i,c in enumerate(cards[:3]):
        img(p,A+f"misc/{c}.jpg",f"cd{i}",[590,770,950][i],[110,150,110][i],300,420); names.append(f"cd{i}")
    img(p,A+"misc/card-holo-0006.jpg","cdh",700,200,330,462); 
    ap(p,[{"type":"animate-preset","target":f"cd{i}","preset":"pop-in","start":900+i*450,"duration":500,"easing":"ease-out-back"} for i in range(3)])
    ap(p,[{"type":"animate-preset","target":"cdh","preset":"pop-in","start":3000,"duration":500,"easing":"ease-out-back"}])
    ap(p,[{"type":"text","name":"lab","text":"13 rows, 13 cards,\nplus a holo foil comp","font":"Brico","size":36,"color":"#ffd77a","x":66,"y":580,"line_height":1.0}])
    ap(p,[{"type":"animate-preset","target":"lab","preset":"fade-in","start":3300,"duration":400}])
    return p
def x6():
    DUR=4800
    p=base(DUR,"#0d1024")
    ap(p,[{"type":"shape","shape":"rounded-rectangle","name":"win","x":60,"y":40,"width":640,"height":640,"radius":14,"fill":"#ffffff"}])
    img(p,A+"misc/info.jpg","info",60,40,640,1724)
    ap(p,[{"type":"clip","target":"info","base":"win"}])
    ap(p,[{"type":"keyframes","target":"info","property":"translate-y","keys":[{"time":300,"value":0,"easing":"ease-in-out"},{"time":4300,"value":-1084}]}])
    panel(p,"panel",740,40,500,640)
    ap(p,[{"type":"text","name":"hdr","text":"08-infographic","font":"Mono","size":20,"color":"#7b8cff","x":766,"y":60}])
    code(p,"c1",['every chart is shapes and paths.','sun rays are one bar, repeated:','{"type":"repeat","target":"ray",','"count":40,"dy":19}'],766,106,400,per=420,size=21,color="#ffffff")
    ap(p,[{"type":"text","name":"t1","text":"the checks caught\nmy own mistake:","font":"Brico","size":38,"color":CREAM,"x":766,"y":340,"line_height":1.0},
          {"type":"text","name":"t2","text":"“98.6%” in the first green\nbar is 3.42:1, under the\n4.5:1 minimum.","font":"Mono","size":22,"color":"#ff8fb1","x":766,"y":440,"line_height":1.3},
          {"type":"text","name":"t3","text":"I left it in.","font":"Caveat","size":58,"color":"#ffd77a","x":766,"y":580}])
    ap(p,[{"type":"animate-preset","target":"t1","preset":"fade-in","start":2200,"duration":400},{"type":"animate-preset","target":"t2","preset":"fade-in","start":2900,"duration":400},{"type":"animate-preset","target":"t3","preset":"pop-in","start":3800,"duration":400,"easing":"ease-out-back"}])
    return p
def x8():
    DUR=7200
    p=base(DUR,"#150f2e")
    img(p,A+"misc/germ-still2.png","g1",40,40,560,315)
    img(p,A+"misc/germ-still1.png","g2",40,380,560,315)
    for n in ("g1","g2"): ap(p,[{"type":"layer-style","target":n,"name":"stroke","settings":{"color":"#ffd84d","width":4}}])
    ap(p,[{"type":"animate-preset","target":"g1","preset":"pop-in","start":200,"duration":450,"easing":"ease-out-back"},{"type":"animate-preset","target":"g2","preset":"pop-in","start":700,"duration":450,"easing":"ease-out-back"}])
    panel(p,"panel",640,40,600,655)
    ap(p,[{"type":"text","name":"hdr","text":"movie/build/characters.py","font":"Mono","size":20,"color":"#7b8cff","x":666,"y":60}])
    ap(p,[{"type":"text","name":"l1","text":"arms pivot at the shoulder","font":"Brico","size":30,"color":SUN,"x":666,"y":104}])
    code(p,"c1",['{"type":"pivot","target":"pip_armL",','"value":[S(11.5), S(1.5)],','"units":"px"}'],666,148,500,per=420,size=21)
    ap(p,[{"type":"text","name":"l2","text":"mouths flap on stepped keys","font":"Brico","size":30,"color":SUN,"x":666,"y":300}])
    code(p,"c2",['d.key(mouth,"visible",0,False)','while t < t1:','  d.key(mouth,"visible",t,on)','  t += 170; on = not on'],666,344,2300,per=420,size=21)
    ap(p,[{"type":"animate-preset","target":"l1","preset":"fade-in","start":400,"duration":300},{"type":"animate-preset","target":"l2","preset":"fade-in","start":2100,"duration":300}])
    ap(p,[{"type":"text","name":"big","text":"8 scenes · 180–410 layers each\nnothing hand-painted or sampled","font":"Brico","size":34,"color":CREAM,"x":666,"y":560,"line_height":1.1}])
    ap(p,[{"type":"animate-preset","target":"big","preset":"fade-in","start":4200,"duration":500}])
    return p
if __name__=="__main__":
    for n,f,t in (("x4",x4,[400,2000,3400,4200,6300,7000]),("x5",x5,[600,1500,2500,3600,4600]),("x6",x6,[400,1500,3000,4700]),("x8",x8,[500,1500,3000,6000])):
        p=f(); print(n,peek(p,n,t))
