import sys, os, shutil, tempfile, subprocess
BUILD=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(BUILD)
sys.path.insert(0,BUILD)
import numpy as np
def remux(video, out, scale=1.0):
    from mkfilm import spec as mk
    from vixl.plugins.film import film
    full=mk(draft=False,audio=True)
    for t in full["audio"]: t["volume"]=round(t["volume"]*scale,3)
    silent={k:v for k,v in full.items() if k!="audio"}
    settings=film.plan(silent,None,True)
    with tempfile.TemporaryDirectory(dir=ROOT) as temp:
        muxed,sound=film._mux_audio(full,ROOT,video,temp,settings,0,settings["frames"],".mp4")
        shutil.copy(muxed,out)
    return out
def levels(path):
    raw=subprocess.run(["ffmpeg","-v","error","-i",path,"-vn","-f","f32le","-ac","1","-ar","48000","-"],capture_output=True).stdout
    a=np.frombuffer(raw,dtype=np.float32)
    return a
if __name__=="__main__":
    v,o,s=sys.argv[1],sys.argv[2],float(sys.argv[3])
    remux(v,o,s)
    a=levels(o)
    print("peak dBFS",round(20*np.log10(np.abs(a).max()+1e-9),1))
    step=48000*2400//1000
    for i in range(0,len(a),step):
        seg=a[i:i+step]; print(i//step, round(20*np.log10(np.sqrt((seg**2).mean())+1e-9),1), end=" | ")
    print()
