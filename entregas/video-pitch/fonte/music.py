import numpy as np, soundfile as sf
sr=48000; D=29.9; t=np.arange(int(sr*D))/sr
def note(f): return 440*2**((f-69)/12)
# chord progression, 4 chords x ~7.5s : C, Am, F, G (warm, hopeful); brighter after 15.7s
chords=[[48,55,60,64],[45,52,57,60],[41,48,53,57],[43,50,55,59]]
seg=D/4; y=np.zeros_like(t)
for i,ch in enumerate(chords):
    a=i*seg; m=(t>=a-0.6)&(t<a+seg+0.6)
    env=np.clip(np.minimum((t-a+0.6)/1.2,(a+seg+0.6-t)/1.2),0,1)
    for n in ch:
        f=note(n); y+= m*env*0.06*(np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*2*f*t+0.5))
# soft plucked arpeggio from 10s (when she asks), every 0.5s
arp=[72,76,79,76, 69,72,76,72, 65,69,72,69, 67,71,74,71]
for k,st in enumerate(np.arange(10.0,D-1.0,0.5)):
    f=note(arp[k%len(arp)]); m=t>=st; tt=t-st
    y+= m*0.035*np.exp(-tt*4)*np.sin(2*np.pi*f*tt)
y*=np.clip(t/1.5,0,1)*np.clip((D-t)/1.5,0,1)
sf.write('music.wav',(y/np.abs(y).max()*0.25).astype(np.float32),sr)
