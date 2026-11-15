import numpy as np, soundfile as sf
sr=48000; D=169.0; t=np.arange(int(sr*D))/sr
note=lambda m:440*2**((m-69)/12)
warm=[[48,55,60,64],[45,52,57,60],[41,48,53,57],[43,50,55,59]]   # C Am F G
tense=[[45,52,57,60],[41,48,53,57],[40,47,52,55],[45,52,57,60]]  # Am F Em Am
sections=[(0,17.8,warm),(17.8,74.7,tense),(74.7,169,warm)]
y=np.zeros_like(t); seg=6.0
for a,b,prog in sections:
    k=0; s=a
    while s<b:
        e=min(s+seg,b); ch=prog[k%4]; m=(t>=s-0.6)&(t<e+0.6)
        env=np.clip(np.minimum((t-s+0.6)/1.2,(e+0.6-t)/1.2),0,1)
        for n in ch: f=note(n); y+=m*env*0.05*(np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*2*f*t+.5))
        s=e; k+=1
arpW=[72,76,79,76,69,72,76,72,65,69,72,69,67,71,74,71]
for i,st in enumerate(np.arange(91.0,D-2,0.5)):
    f=note(arpW[i%16]); m=t>=st; tt=t-st; y+=m*0.03*np.exp(-tt*4)*np.sin(2*np.pi*f*tt)
y*=np.clip(t/2,0,1)*np.clip((D-t)/2.5,0,1)
sf.write('music.wav',(y/np.abs(y).max()*0.25).astype(np.float32),sr)
