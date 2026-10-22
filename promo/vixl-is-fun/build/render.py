import sys, os, json, shutil, subprocess, tempfile, time
BUILD=os.path.dirname(os.path.abspath(__file__))
if os.environ.get("VIXL_REPO"): sys.path.insert(0,os.path.join(os.environ["VIXL_REPO"],"src"))
sys.path.insert(0,BUILD)
from multiprocessing import Pool
from pathlib import Path
ROOT=os.path.dirname(BUILD)
def part(args):
    spec,a,b,path=args
    from vixl.plugins.film.film import export
    if os.path.exists(path): return path
    export(spec, ROOT, path, frame_range=(a,b))
    return path
def main(out, draft=False, chunk=75, t0=None):
    from mkfilm import spec as mk
    from vixl.plugins.film import film
    full=mk(draft=draft,audio=True)
    silent={k:v for k,v in full.items() if k!="audio"}
    settings=film.plan(silent, None, True)
    n=settings["frames"]
    parts_dir=Path(ROOT)/"work"/("parts_draft" if draft else "parts"); parts_dir.mkdir(parents=True,exist_ok=True)
    jobs=[(silent,a,min(n,a+chunk),str(parts_dir/f"p{a:05d}.mp4")) for a in range(0,n,chunk)]
    t=time.time()
    with Pool(4) as pool:
        for i,p in enumerate(pool.imap(part,jobs)): print("part",i+1,"/",len(jobs),round(time.time()-t),"s",flush=True)
    lst=parts_dir/"list.txt"
    lst.write_text("".join(f"file '{j[3]}'\n" for j in jobs))
    video=parts_dir/"video.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",str(lst),"-c","copy",str(video)],check=True)
    with tempfile.TemporaryDirectory(dir=ROOT) as temp:
        muxed,sound=film._mux_audio(full, ROOT, str(video), temp, settings, 0, n, ".mp4")
        shutil.copy(muxed, out)
    print("done",out,sound)
if __name__=="__main__":
    main(sys.argv[1], draft="--draft" in sys.argv)
