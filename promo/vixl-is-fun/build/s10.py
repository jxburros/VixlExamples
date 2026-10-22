from lib import *
def build():
    p=new(CREAM,[("Bricolage Grotesque",800,"Brico"),("Space Mono",700,"Mono")])
    ap(p,[{"type":"timeline-set","duration":6000,"fps":24,"loop":1}])
    ap(p,[
      {"type":"shape","shape":"ellipse","name":"blob-pink","x":-200,"y":380,"width":560,"height":560,"fill":PINK},
      {"type":"shape","shape":"ellipse","name":"blob-teal","x":960,"y":-260,"width":560,"height":560,"fill":TEAL},
      {"type":"shape","shape":"star","name":"burst","x":1070,"y":470,"width":170,"height":170,"sides":8,"inner_radius":0.55,"fill":SUN,"stroke":INK,"stroke_width":6},
      {"type":"text","name":"l1","text":"Go make something","font":"Brico","size":112,"color":INK,"x":"center","y":120,"tracking":-3},
      {"type":"text","name":"l2","text":"weird.","font":"Brico","size":230,"color":TOMATO,"x":"center","y":225,"tracking":-4},
      {"type":"shape","shape":"rounded-rectangle","name":"cmd-bg","x":250,"y":530,"width":780,"height":74,"radius":18,"fill":INK},
      {"type":"text","name":"cmd","text":"uvx --from vixl-engine vixl mcp --workspace .","font":"Mono","size":26,"color":"#fff4e0","x":"center","y":550},
      {"type":"text","name":"url","text":"github.com/jxburros/Vixl","font":"Mono","size":28,"color":INK,"x":"center","y":628},
      {"type":"text","name":"meta","text":"this whole film: 26 editable .vixl files","font":"Mono","size":20,"color":INK,"x":"center","y":676,"opacity":0.7},
    ])
    ap(p,[{"type":"particles","name":"conf","preset":"sparks","count":70,"x":640,"y":740,"spread":[520,10],"velocity":[0,-820],"gravity":900,"turbulence":140,"life":2400,"size":9,"color":SUN,"start":1500,"duration":3000,"seed":3},
          {"type":"particles","name":"conf2","preset":"sparks","count":50,"x":640,"y":740,"spread":[620,10],"velocity":[0,-760],"gravity":900,"turbulence":180,"life":2400,"size":8,"color":BLUE,"start":1500,"duration":3000,"seed":8},
          {"type":"particles","name":"conf3","preset":"sparks","count":50,"x":640,"y":740,"spread":[420,10],"velocity":[0,-880],"gravity":900,"turbulence":120,"life":2400,"size":8,"color":TEAL,"start":1500,"duration":3000,"seed":11}])
    ap(p,[
      {"type":"text-animate","target":"l1","preset":"fade-up","unit":"word","start":300,"duration":500,"stagger":160,"mode":"in"},
      {"type":"text-animate","target":"l2","preset":"pop","unit":"char","start":1200,"duration":500,"stagger":110,"mode":"in"},
      {"type":"text-animate","target":"l2","preset":"wave","unit":"char","start":2200,"duration":900,"stagger":"18%","repeat":True,"mode":"in"} if False else {"type":"animate-preset","target":"burst","preset":"pop-in","start":2400,"duration":500},
      {"type":"animate-preset","targets":["cmd-bg","cmd"],"preset":"slide-in-up","start":2700,"duration":500,"distance":60,"fade":True},
      {"type":"animate-preset","target":"url","preset":"fade-in","start":3300,"duration":600},{"type":"animate-preset","target":"meta","preset":"fade-in","start":4000,"duration":600},
      {"type":"motion","recipe":"spin","target":"burst","start":2400,"duration":3600,"turns":2,"symmetry":8},
      {"type":"motion","recipe":"hover","targets":["l2"],"amount":10,"period":1600,"start":2400,"duration":3200},
    ])
    return p
if __name__=="__main__":
    p=build(); print(peek(p,"s10",[600,1500,2600,3600,5000,5900]))
