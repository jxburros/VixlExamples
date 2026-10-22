"""The film's score: a 100 bpm loop-based cue built from Vixl's synthesized instruments, locked to the shot grid."""
BEAT=600; BAR=2400
CH={"C":(36,[60,64,67]),"Am":(45,[57,60,64]),"F":(41,[53,57,60]),"G":(43,[55,59,62])}
PROG=["C","Am","F","G"]
STARTS={"s01":0,"s02":4800,"s03":9600,"intro":14400,"posters":16800,"pip":21600,"mandala":28800,"pixel":33600,"comic":38400,"drawer":45600,"x0":50400,"rain":52800,"paint":60000,"pixel2":67200,"poster":74400,"cards":81600,"info":86400,"germ":91200,"how":96000,"outro":103200,"end":110400}
def bar_t(b): return b*BAR
tracks={k:[] for k in ("bass","drums","keys","bell","pad","lead","sfx")}
def n(track,t,dur,midi=None,vel=0.8,inst="sine"):
    d={"start":int(t),"duration":max(10,int(dur)),"velocity":round(min(1,vel),2),"instrument":inst}
    if midi is not None: d["midi"]=midi
    tracks[track].append(d)
def chord_for(b): return PROG[b%4]
def pad(b0,b1,vel=0.3,chords=None):
    for b in range(b0,b1):
        c=chords[(b-b0)%len(chords)] if chords else chord_for(b)
        for m in CH[c][1]:
            n("pad",bar_t(b),BAR,m,vel,"sine")
def groove(b0,b1,intensity=1.0,kick4=False,hat=True,bassmode="groove"):
    for b in range(b0,b1):
        t0=bar_t(b); root,tones=CH[chord_for(b)]
        # drums
        kicks=[0,1,2,3] if kick4 else [0,2,2.5]
        for k in kicks: n("drums",t0+k*BEAT,200,None,0.9*intensity,"kick")
        for s in (1,3): n("drums",t0+s*BEAT,180,None,0.7*intensity,"snare")
        if hat:
            for i in range(8): n("drums",t0+i*BEAT/2,80,None,(0.5 if i%2==0 else 0.8)*0.45*intensity,"hihat")
        # bass
        if bassmode=="groove":
            for beat,off,d,v in ((0,0,0.9,0.9),(1,12,0.4,0.6),(2,0,0.9,0.85),(3,7,0.9,0.8)):
                n("bass",t0+beat*BEAT,d*BEAT,root+off,v,"bass")
        else:
            for i in range(8): n("bass",t0+i*BEAT/2,BEAT/2*0.8,root,0.8,"bass")
        # keys arp
        for i,idx in enumerate((0,1,2,1,0,2,1,2)):
            n("keys",t0+i*BEAT/2,BEAT/2*0.9,tones[idx]+12,0.5,"piano")
        n("bell",t0,BAR*0.9,tones[2]+24,0.28,"bell")
def build_score():
    # --- bars 0-1: title. Bell plucks on each landing of the ball (600 ms apart), then a soft arpeggio
    pad(0,2,0.28,["C"])
    for k,m in enumerate((72,76,79,84)):
        n("bell",600*(k+1),500,m,0.8,"bell"); n("sfx",600*(k+1),200,76+k*2,0.45,"pop")
    for i in range(8):
        n("keys",BAR+i*BEAT/2,BEAT/2*0.9,(60,64,67,72,67,64,67,72)[i]+12,0.35+0.04*i,"piano")
    n("sfx",3000,300,84,0.5,"pop")                    # lands on the star
    for i in range(14): n("drums",3600+i*85,70,None,0.2+i*0.04,"hihat")   # tiny build
    n("sfx",4300,600,None,0.5,"whoosh")
    # --- bars 2-5: groove under the jellyfish and the garden
    groove(2,6); pad(2,6,0.22)
    n("sfx",4800+1800,300,79,0.7,"pop"); n("sfx",4800+3900,700,None,0.4,"splash")
    for i,m in enumerate((72,74,76,79,81,84,86,88)): n("bell",9600+300+i*270,300,m,0.7,"bell")
    # --- bar 6: "same words. 28 outfits."  (build)
    for b in (6,):
        t0=bar_t(b)
        for k in range(4): n("drums",t0+k*BEAT,200,None,0.8,"kick")
        for i,t in enumerate((0,200,500,700)): n("sfx",t0+t,160,70+i*3,0.6,"pop")
        for i in range(12): n("drums",t0+BAR-BEAT*1.0+i*50,60,None,0.4+i*0.05,"snare")
        for beat in range(4): n("bass",t0+beat*BEAT,BEAT*0.8,CH["Am"][0] if beat<2 else CH["G"][0],0.8,"bass")
    n("sfx",bar_t(7)-500,500,None,0.5,"whoosh")
    # --- bars 7-8: eight poster cuts, one per beat
    stab=["C","C","Am","Am","F","F","G","G"]
    for i in range(8):
        t=STARTS["posters"]+i*BEAT; c=stab[i]; root,tones=CH[c]
        n("drums",t,200,None,0.95,"kick"); 
        n("drums",t+BEAT/2,60,None,0.4,"hihat")
        if i%2==1: n("drums",t,180,None,0.7,"snare")
        for m in tones: n("keys",t,BEAT*0.55,m+12,0.55,"piano")
        n("bass",t,BEAT*0.5,root,0.9,"bass"); n("bass",t+BEAT/2,BEAT*0.4,root+12,0.7,"bass")
        n("sfx",t,120,72+(i*2),0.35,"click")
    n("sfx",STARTS["pip"]-300,400,None,0.6,"whoosh")
    # --- bars 9-11: Pip. pizzicato walking bass, wood-block offbeats, no kick
    walk={"C":[36,40,43,40],"F":[41,45,48,45],"G":[43,47,50,47]}
    for b,c in zip((9,10,11),("C","F","G")):
        t0=bar_t(b)
        for beat,m in enumerate(walk[c]): n("bass",t0+beat*BEAT,BEAT*0.45,m,0.85,"piano")
        for beat in (1,3): n("drums",t0+beat*BEAT,100,None,0.7,"click")
        for i in range(8): n("drums",t0+i*BEAT/2,60,None,0.2+0.12*(i%2),"hihat")
        root,tones=CH[c]
        for i,idx in enumerate((2,1,2,0)): n("keys",t0+i*BEAT+BEAT/2,BEAT*0.4,tones[idx]+12,0.5,"bell")
        for m in tones: n("pad",t0,BAR,m,0.18,"triangle")
    n("sfx",STARTS["pip"]+4200,500,None,0.6,"splash"); n("sfx",STARTS["pip"]+6600,500,None,0.45,"whoosh")
    for t in (2500,): n("sfx",STARTS["pip"]+t,150,84,0.6,"pop")
    # --- bars 12-13: mandala. dreamy pad + bells with echo, soft kick pulse
    pad(12,14,0.3,["Am","F"])
    for b in (12,13):
        t0=bar_t(b); root,tones=(CH["Am"] if b==12 else CH["F"])
        n("bass",t0,BAR,root,0.7,"sine")
        for k in (0,2): n("drums",t0+k*BEAT,200,None,0.5,"kick")
        for i in range(8):
            m=tones[(0,1,2,1,2,1,0,2)[i]]+24
            n("bell",t0+i*BEAT/2,BEAT,m,0.5,"bell"); n("bell",t0+i*BEAT/2+BEAT/2,BEAT,m,0.2,"bell")
    n("sfx",STARTS["mandala"]-200,700,None,0.4,"whoosh")
    # --- bars 14-15: pixel. chip lead, triangle bass, coins ding
    mel=[72,76,79,76,81,79,76,72, 74,77,81,77,79,77,74,67]
    for i,m in enumerate(mel): n("lead",STARTS["pixel"]+i*BEAT/2*1.0*1.0*1.0*1.0*1.0*1.0*1.0*1.0*1.0+0, BEAT/2*0.85, m, 0.55,"square")
    for b,c in zip((14,15),("C","G")):
        t0=bar_t(b); root=CH[c][0]
        for i in range(8): n("bass",t0+i*BEAT/2,BEAT/2*0.8,root+(12 if i%2 else 0),0.7,"triangle")
        for k in (0,2): n("drums",t0+k*BEAT,150,None,0.7,"kick")
        for s in (1,3): n("drums",t0+s*BEAT,100,None,0.45,"snare")
        for i in range(8): n("drums",t0+i*BEAT/2,50,None,0.3,"hihat")
    for x in (380,620,860,1100):
        tcol=int((x+80+200)/(1420+200)*4800)
        n("bell",STARTS["pixel"]+tcol,260,91,0.8,"bell"); n("bell",STARTS["pixel"]+tcol+90,260,96,0.7,"bell")
    # --- bars 16-18: comic. sparse chords + plucks, stinger on the reveal
    for b,c in zip((16,17,18),("C","Am","F")):
        t0=bar_t(b); root,tones=CH[c]
        for m in tones: n("keys",t0,BAR*0.95,m,0.3,"piano")
        n("bass",t0,BEAT*0.9,root,0.6,"bass"); n("bass",t0+2*BEAT,BEAT*0.9,root,0.5,"bass")
        for beat in (1,3): n("drums",t0+beat*BEAT,80,None,0.4,"click")
        for i in range(8): n("drums",t0+i*BEAT/2,50,None,0.12,"hihat")
    for t in (300,2100,3900): n("sfx",STARTS["comic"]+t,200,74,0.6,"pop")
    for t,m in ((900,67),(2700,72),(4500,76)): n("sfx",STARTS["comic"]+t,180,m,0.5,"click")
    t=STARTS["comic"]+5400
    n("drums",t,300,None,1.0,"kick"); n("drums",t,200,None,0.9,"snare"); n("sfx",t,900,None,0.7,"splash"); n("bass",t,BEAT*2,36,0.9,"bass")
    n("sfx",STARTS["comic"]+6000,700,None,0.6,"whoosh")
    for m in (60,64,67): n("keys",t+BEAT*2,BEAT*2,m+12,0.5,"piano")
    # --- bars 19-20: the junk drawer. groove returns, bell run on card pops
    groove(19,21,kick4=True); pad(19,21,0.2,["F","G"])
    for i,m in enumerate((72,74,76,79,81,84,86,88)): n("sfx",STARTS["drawer"]+300+i*300,200,m+0,0.45,"pop")
    n("sfx",STARTS["drawer"]+4600,400,None,0.5,"whoosh") if False else None
    # --- bars 21-23: finale
    groove(43,45,kick4=True,bassmode="pulse"); pad(43,45,0.25,["Am","F"])
    for i,t in enumerate(range(0,700,110)): n("sfx",STARTS["outro"]+1200+t,150,72+i*2,0.5,"pop")
    n("sfx",STARTS["outro"]+1500,900,None,0.7,"splash")
    n("sfx",STARTS["outro"]+2400,500,None,0.35,"whoosh")
    t=STARTS["outro"]+4800                                   # bar 23: land the chord
    for m in (48,60,64,67,72): n("pad",t,BAR*1.1,m,0.45,"sine")
    for m in (60,64,67,72,76): n("keys",t,BAR*1.1,m,0.5,"piano")
    n("bass",t,BAR*1.1,36,0.9,"bass"); n("drums",t,300,None,1.0,"kick"); n("sfx",t,1400,None,0.6,"splash"); n("bell",t,BAR*1.1,96,0.5,"bell")
    for i,m in enumerate((72,76,79,84,88)): n("bell",t+BEAT+i*220,600,m,0.4,"bell")

    # ===== extension: the real work (bars 21-42) =====
    S=STARTS
    # x0 card: short build
    for k in range(4): n("drums",S["x0"]+k*BEAT,200,None,0.7,"kick")
    for i in range(10): n("drums",S["x0"]+BAR-BEAT+i*60,60,None,0.35+i*0.05,"snare")
    n("sfx",S["x0"],500,None,0.45,"whoosh")
    for i,t in enumerate((0,180,360,540)): n("sfx",S["x0"]+t,150,72+i*2,0.45,"pop")
    # rain girl: slow pad + arps, soft rain of hats, a tick for every stage of the build
    pad(22,25,0.32,["Am","F","C"])
    for b,c in zip((22,23,24),("Am","F","C")):
        t0=bar_t(b); root,tones=CH[c]
        n("bass",t0,BAR,root,0.55,"sine")
        for i in range(4): n("keys",t0+i*BEAT,BEAT*1.4,tones[(0,1,2,1)[i]]+12,0.42,"piano")
        for i in range(8): n("drums",t0+i*BEAT/2,50,None,0.10+0.06*(i%2),"hihat")
        n("bell",t0,BAR*0.9,tones[2]+24,0.25,"bell")
    for k in range(14): n("sfx",S["rain"]+500+k*440,120,84+(k%3)*2,0.22,"click")
    # painting: dreamy, bells with echo, stats pop
    pad(25,28,0.30,["F","G","C"])
    for b,c in zip((25,26,27),("F","G","C")):
        t0=bar_t(b); root,tones=CH[c]
        n("bass",t0,BAR,root,0.6,"sine")
        for k in (0,2): n("drums",t0+k*BEAT,200,None,0.45,"kick")
        for i in range(8):
            m=tones[(0,1,2,1,2,1,0,2)[i]]+24
            n("bell",t0+i*BEAT/2,BEAT,m,0.45,"bell"); n("bell",t0+i*BEAT/2+BEAT/2,BEAT,m,0.18,"bell")
    for i in range(3): n("sfx",S["paint"]+1500+i*700,200,76+i*3,0.5,"pop")
    # pixel: typing ticks for the 16 rows, then the chip tune under the map
    for r in range(16): n("sfx",S["pixel2"]+300+r*125,60,96,0.3,"click")
    t0=bar_t(28); root=CH["C"][0]
    for i in range(8): n("bass",t0+i*BEAT/2,BEAT/2*0.8,root+(12 if i%2 else 0),0.6,"triangle"); n("drums",t0+i*BEAT/2,50,None,0.25,"hihat")
    for k in (0,2): n("drums",t0+k*BEAT,150,None,0.6,"kick")
    for i,m in enumerate((72,76,79,76,72,76,79,84)): n("lead",t0+i*BEAT/2,BEAT/2*0.8,m,0.3,"square")
    for i,m in enumerate(mel+mel[:8]): 
        t=S["pixel2"]+2400+i*BEAT/2
        if t<S["pixel2"]+7200: n("lead",t,BEAT/2*0.85,m,0.5,"square")
    for b,c in zip((29,30),("C","G")):
        t0=bar_t(b)
        if b==29: continue
        root=CH[c][0]
        for i in range(8): n("bass",t0+i*BEAT/2,BEAT/2*0.8,root+(12 if i%2 else 0),0.7,"triangle")
        for k in (0,2): n("drums",t0+k*BEAT,150,None,0.7,"kick")
        for s_ in (1,3): n("drums",t0+s_*BEAT,100,None,0.45,"snare")
        for i in range(8): n("drums",t0+i*BEAT/2,50,None,0.3,"hihat")
    for i in range(8): n("bass",bar_t(29)+i*BEAT/2,BEAT/2*0.8,CH["F"][0]+(12 if i%2 else 0),0.6,"triangle")
    # poster: synthwave groove, whoosh at each change of view
    groove(31,34,kick4=True,bassmode="pulse"); pad(31,34,0.25,["Am","F","G"])
    n("sfx",S["poster"]+3600-200,500,None,0.5,"whoosh"); n("sfx",S["poster"]+5400-200,500,None,0.5,"whoosh")
    # cards: lighter groove, pops as each card lands
    groove(34,36); 
    for i,t in enumerate((900,1350,1800)): n("sfx",S["cards"]+t,200,72+i*4,0.6,"pop")
    n("sfx",S["cards"]+3000,700,None,0.5,"splash")
    # infographic: sparse, a dull knock when the mistake is admitted
    for b,c in zip((36,37),("Am","F")):
        t0=bar_t(b); root,tones=CH[c]
        for m in tones: n("keys",t0,BAR*0.95,m,0.3,"piano")
        n("bass",t0,BEAT*0.9,root,0.55,"bass")
        for beat in (1,3): n("drums",t0+beat*BEAT,80,None,0.35,"click")
        for i in range(8): n("drums",t0+i*BEAT/2,50,None,0.1,"hihat")
    n("sfx",S["info"]+2200,200,50,0.6,"pop"); n("sfx",S["info"]+3800,300,62,0.7,"pop")
    # germ king clip: pizzicato bounce, a stinger on AH-CHOO
    walk2={"C":[36,40,43,40],"G":[43,47,50,47]}
    for b,c in zip((38,39),("C","G")):
        t0=bar_t(b)
        for beat,m in enumerate(walk2[c]): n("bass",t0+beat*BEAT,BEAT*0.45,m,0.85,"piano")
        for beat in (1,3): n("drums",t0+beat*BEAT,100,None,0.7,"click")
        for i in range(8): n("drums",t0+i*BEAT/2,60,None,0.2+0.12*(i%2),"hihat")
        for m in CH[c][1]: n("pad",t0,BAR,m,0.18,"triangle")
    t=S["germ"]+1900
    n("drums",t,300,None,1.0,"kick"); n("drums",t,200,None,0.9,"snare"); n("sfx",t,700,None,0.6,"splash")
    # how-it-was-made: building toward the finale
    pad(40,43,0.28,["F","G","Am"])
    for b,c in zip((40,41,42),("F","G","Am")):
        t0=bar_t(b); root,tones=CH[c]
        for i in range(8): n("keys",t0+i*BEAT/2,BEAT/2*0.9,tones[(0,1,2,1,0,2,1,2)[i]]+12,0.4+0.03*(b-40),"piano")
        n("bass",t0,BAR,root,0.6,"sine")
        for k in range(4 if b>40 else 2): n("drums",t0+(k if b>40 else 2*k)*BEAT,200,None,0.5+0.1*(b-40),"kick")
    for i in range(14): n("drums",bar_t(43)-BEAT+i*40,50,None,0.3+i*0.05,"snare")
    n("sfx",bar_t(43)-500,500,None,0.5,"whoosh")
    vols={"bass":0.55,"drums":0.5,"keys":0.38,"bell":0.32,"pad":0.2,"lead":0.28,"sfx":0.45}
    out=[]
    for name,notes in tracks.items():
        notes.sort(key=lambda d:d["start"])
        out.append({"name":name,"synth":"sine","start":0,"volume":vols[name],"notes":notes})
    return out
if __name__=="__main__":
    t=build_score()
    for tr in t: print(tr["name"],len(tr["notes"]))
