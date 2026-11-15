import soundfile as sf, numpy as np, json, sys
from kokoro_onnx import Kokoro
k=Kokoro('kokoro-v1.0.int8.onnx','voices-v1.0.bin')
# each line = list of [phrase, pause_after_seconds]
L=json.load(open('script.json'))
voice=sys.argv[1]; speed=float(sys.argv[2])
sr=24000; full=[]; t=0.15; timing=[];ph_t=[]
full.append(np.zeros(int(sr*0.15)))
for li,line in enumerate(L):
    start=t
    for ph,pause in line:
        s,sr=k.create(ph,voice=voice,speed=speed,lang='en-us')
        # trim leading/trailing silence
        a=np.abs(s); idx=np.where(a>0.01)[0]
        s=s[max(idx[0]-240,0):idx[-1]+480]
        ph_t.append([ph,round(t,2),round(t+len(s)/sr,2)]); full.append(s); t+=len(s)/sr
        full.append(np.zeros(int(sr*pause))); t+=pause
    timing.append([round(start,2),round(t,2)])
y=np.concatenate(full).astype(np.float32)
sf.write(f'narr_{voice}.wav',y,sr)
json.dump({'lines':timing,'phrases':ph_t},open(f'timing_{voice}.json','w'),indent=0)
print(voice, round(len(y)/sr,2), timing)
