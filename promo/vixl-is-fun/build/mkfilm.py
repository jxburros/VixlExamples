import sys, json
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from score import build_score, STARTS
POSTERS=["s04a_bauhaus","s04b_vapor","s04c_neobrutal","s04d_riso","s04e_deco","s04f_y2k","s04g_japanese","s04h_pixel"]
NOMINAL=[("s01",4800,0),("s02",4800,320),("s03",4800,320),("s04i",2400,200)]+[(p,600,0) for p in POSTERS]+[("s05",7200,0),("s06",4800,320),("s07",4800,320),("s08",7200,320),("s09",4800,320),("x0",2400,200),("x1",7200,320),("x2",7200,320),("x3",7200,320),("x4",7200,320),("x5",4800,320),("x6",4800,320),("GERM",4800,320),("x8",7200,320),("s10",7200,320)]
CAM={}
for i,p in enumerate(POSTERS):
    CAM[p]={"from":[0.5-0.03*(1 if i%2 else -1),0.5,1.0],"to":[0.5+0.03*(1 if i%2 else -1),0.5,1.09]}
def spec(draft=False,audio=True,upto=None):
    shots=[]
    for i,(name,nom,T) in enumerate(NOMINAL):
        nextT=NOMINAL[i+1][2] if i+1<len(NOMINAL) else 0
        s={"source":("work/assets/misc/germ-clip.mp4" if name=="GERM" else f"scenes/{name}.vixl"),"duration":nom+nextT}
        if T: s["transition"]=T
        if name in CAM: s["camera"]=CAM[name]
        shots.append(s)
    sp={"version":1,"width":1280,"height":720,"fps":25,"shots":shots}
    if draft: sp["quality"]="draft"
    if audio: sp["audio"]=build_score()
    return sp
if __name__=="__main__":
    json.dump({"output":"out/film.mp4","spec":spec()},open("req_full.json","w"))
    json.dump({"spec":spec()},open("req_plan.json","w"))
    # verify the shot grid matches the score
    t=0; 
    for (n,nom,T) in NOMINAL:
        print(n,t); t+=nom
    print("total",t)
