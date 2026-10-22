from lib import *
def build():
    p = new(CREAM, [("Bricolage Grotesque",800,"Brico"),("Space Mono",700,"Mono")])
    ap(p, [{"type":"timeline-set","duration":4800,"fps":24,"loop":1}])
    ap(p, [
      {"type":"shape","shape":"ellipse","name":"blob-pink","x":-220,"y":450,"width":520,"height":520,"fill":PINK},
      {"type":"shape","shape":"ellipse","name":"blob-teal","x":1010,"y":-240,"width":520,"height":520,"fill":TEAL},
      {"type":"shape","shape":"star","name":"burst","x":1065,"y":505,"width":150,"height":150,"sides":8,"inner_radius":0.55,"fill":SUN,"stroke":INK,"stroke_width":6},
      {"type":"text","name":"word","text":"Vixl","font":"Brico","size":330,"color":INK,"x":"center","y":150,"tracking":-6},
      {"type":"text","name":"tag","text":"a layered image engine that is accidentally fun","font":"Mono","size":28,"color":INK,"x":"center","y":456},
      {"type":"shape","shape":"ellipse","name":"ball","x":418,"y":-120,"width":84,"height":84,"fill":TOMATO,"stroke":INK,"stroke_width":6},
    ])
    pts=[(600,418,96),(1200,568,41),(1800,718,151),(2400,863,76),(3000,1098,421)]
    xk,yk=hop_keys(pts,hop=190)
    yk[0:0]=[{"time":0,"value":-120,"easing":"ease-in-quad"}]; xk[0:0]=[{"time":0,"value":418,"easing":"linear"}]
    ap(p, [{"type":"keyframes","target":"ball","property":"x","keys":xk},{"type":"keyframes","target":"ball","property":"y","keys":yk}])
    ap(p, [
      {"type":"text-animate","target":"word","preset":"pop","unit":"char","start":450,"duration":450,"stagger":600,"mode":"in"},
      {"type":"text-animate","target":"tag","preset":"typewriter","start":3000,"duration":1200,"mode":"in"},
      {"type":"animate-preset","target":"burst","preset":"pop-in","start":2700,"duration":500},
      {"type":"motion","recipe":"spin","target":"burst","start":2700,"duration":2100,"turns":1,"symmetry":8},
    ])
    return p
if __name__=="__main__":
    p=build(); print(peek(p,"s01",[0,400,600,900,1050,1300,1500,1950,2400,2800,3400,4100]))
