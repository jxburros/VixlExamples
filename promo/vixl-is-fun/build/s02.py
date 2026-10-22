from lib import *
def build():
    p = new("#0a0f2c", [("Bricolage Grotesque",800,"Brico"),("Space Mono",700,"Mono")])
    ap(p, [{"type":"timeline-set","duration":4800,"fps":24,"loop":1}])
    ap(p, [
      {"type":"gradient","name":"sea","start":"#141a4d","end":"#050816","direction":"vertical"},
      {"type":"star-field","name":"stars","count":90,"seed":3,"region":[0,0,1280,300]},
      {"type":"bokeh","name":"bokeh","count":16,"seed":5,"colors":["#7b8cff","#ff8fe1","#5ef2e0"],"region":[560,60,720,640]},
      # code panel
      {"type":"shape","shape":"rounded-rectangle","name":"panel","x":60,"y":150,"width":520,"height":420,"radius":22,"fill":"#12183f","stroke":"#2e3a8c","stroke_width":3},
      {"type":"shape","shape":"ellipse","name":"d1","x":86,"y":172,"width":16,"height":16,"fill":TOMATO},
      {"type":"shape","shape":"ellipse","name":"d2","x":112,"y":172,"width":16,"height":16,"fill":SUN},
      {"type":"shape","shape":"ellipse","name":"d3","x":138,"y":172,"width":16,"height":16,"fill":TEAL},
      {"type":"text","name":"l0","text":"$ vixl_apply","font":"Mono","size":26,"color":"#7b8cff","x":92,"y":226},
      {"type":"text","name":"l1","text":"{\"type\": \"organic\",","font":"Mono","size":30,"color":"#ffffff","x":92,"y":292},
      {"type":"text","name":"l2","text":" \"preset\": \"jellyfish\"}","font":"Mono","size":30,"color":SUN,"x":92,"y":340},
      {"type":"text","name":"l3","text":"{\"type\": \"look\",","font":"Mono","size":30,"color":"#ffffff","x":92,"y":420},
      {"type":"text","name":"l4","text":" \"look\": \"neon\"}","font":"Mono","size":30,"color":PINK,"x":92,"y":468},
      {"type":"organic","name":"jelly","preset":"jellyfish","seed":7,"x":720,"y":70,"width":420,"height":560,"fill":"#a78bfa","stroke":"#e9d5ff"},
    ])
    ap(p, [
      {"type":"duplicate","target":"jelly","name":"jelly-neon"},
    ])
    ap(p, [
      {"type":"look","target":"jelly-neon","look":"neon","color":"#e9a8ff","amount":0.9},
      {"type":"rasterize","target":"jelly"},{"type":"rasterize","target":"jelly-neon"},
      {"type":"opacity","target":"jelly-neon","value":0},
      {"type":"group","targets":["jelly","jelly-neon"],"name":"jf"},
    ])
    ap(p, [
      {"type":"text-animate","target":"l0","preset":"typewriter","start":150,"duration":450,"mode":"in"},
      {"type":"text-animate","target":"l1","preset":"typewriter","start":600,"duration":600,"mode":"in"},
      {"type":"text-animate","target":"l2","preset":"typewriter","start":1200,"duration":700,"mode":"in"},
      {"type":"text-animate","target":"l3","preset":"typewriter","start":2400,"duration":600,"mode":"in"},
      {"type":"text-animate","target":"l4","preset":"typewriter","start":3000,"duration":600,"mode":"in"},
      {"type":"animate-preset","target":"jf","preset":"pop-in","start":1800,"duration":700,"easing":"ease-out-back"},
      {"type":"keyframes","target":"jf","property":"translate-y","sample":{"fn":"sin","period":2400,"amplitude":16,"step_ms":100,"duration":4800,"start":0}},
      {"type":"animate","target":"jelly-neon","property":"opacity","from":0,"to":1,"start":3900,"duration":500},
    ])
    cap(p,"cap","Describe it. Get a jellyfish.",1900,4700,610,color="#ffffff",size=40,box="#2e3a8c")
    return p
if __name__=="__main__":
    p=build(); print(peek(p,"s02",[500,1500,2600,3300,4600]))
