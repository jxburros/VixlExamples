from part2lib import *
import json
def x0():
    p=base(2400+400,INK)
    ap(p,[{"type":"star-field","name":"stars","count":70,"seed":9,"region":[0,0,1280,720]},
      {"type":"text","name":"a","text":"now the real stuff.","font":"Brico","size":112,"color":CREAM,"x":"center","y":190,"tracking":-4},
      {"type":"shape","shape":"line","name":"ul","x":210,"y":340,"width":860,"height":4,"stroke":TOMATO,"stroke_width":10,"line_cap":"round"},
      {"type":"text","name":"b","text":"everything below lives in the VixlExamples repo","font":"Mono","size":30,"color":SUN,"x":"center","y":430},
      {"type":"text","name":"c","text":"(and the code on screen is the real code)","font":"Mono","size":24,"color":PINK,"x":"center","y":488}])
    ap(p,[{"type":"animate-preset","target":"a","preset":"slide-in-up","start":0,"duration":600,"distance":60,"fade":True},
      {"type":"animate-preset","target":"ul","preset":"draw-on","start":700,"duration":600},
      {"type":"animate-preset","target":"b","preset":"fade-in","start":1100,"duration":500},
      {"type":"animate-preset","target":"c","preset":"fade-in","start":1600,"duration":500}])
    return p
def x1():
    DUR=7200
    p=base(DUR)
    marks=json.load(open(A+"rain/marks.json"))
    T=[500+k*440 for k in range(14)]
    ap(p,[{"type":"shape","shape":"rectangle","name":"bgfill","x":50,"y":12,"width":560,"height":696,"fill":"#05060f"}])
    for k in range(14):
        img(p,A+f"rain/s{k:02d}.jpg",f"st{k}",60,22,540,675)
        hold(p,f"st{k}",T[k])
    panel(p,"panel",650,24,590,672)
    ap(p,[{"type":"text","name":"hdr","text":"art/rain-girl-ops.json","font":"Mono","size":22,"color":"#7b8cff","x":682,"y":50},
          {"type":"text","name":"ctr","text":"ops applied: 0004 / 768","font":"Mono","size":34,"color":SUN,"x":682,"y":92}])
    text_keys(p,"ctr",[(0,"ops applied: 0000 / 768")]+[(T[k],f"ops applied: {m:04d} / 768") for k,(_,m) in enumerate(marks)])
    blocks=[(0,["{\"type\":\"gradient\",\"name\":\"sky\",","\"direction\":\"vertical\",\"stops\":[…]}"],"#ffffff"),
            (3,["{\"type\":\"shape\",\"shape\":\"rectangle\",","\"name\":\"bldg0\",\"fill\":\"#626e7d\"}"],"#ffffff"),
            (5,["{\"type\":\"pen\",\"name\":\"shaft\",","\"points\":[[560,300],[556,520],…]}"],"#ffffff"),
            (7,["{\"type\":\"paint\",\"brush\":\"watercolor\",","\"points\":[[-40,56.1],[20,36.2],…]}"],"#ffd77a"),
            (12,["{\"type\":\"look\",\"look\":\"watercolor\",","\"amount\":0.55}"],"#ff8fb1")]
    for i,(stg,lines,col) in enumerate(blocks):
        code(p,f"cb{i}",lines,682,168+i*92,T[stg],per=330,size=22,color=col)
    ap(p,[{"type":"text","name":"tag","text":"768 operations.\n651 are brush strokes.","font":"Brico","size":44,"color":CREAM,"x":682,"y":596,"line_height":1.0}])
    ap(p,[{"type":"animate-preset","target":"tag","preset":"fade-in","start":T[9],"duration":500}])
    badge(p,"explorations › art/",682,664,size=16) if False else None
    return p
if __name__=="__main__":
    for n,f in (("x0",x0),("x1",x1)):
        p=f(); print(n,peek(p,n,[300,1500,3000,4500,6000,7000]))
