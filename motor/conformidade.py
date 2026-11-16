"""Garante que motor/cerne.js responde EXATAMENTE como motor/cerne.py.
Dois motores que divergem em silencio sao pior que um motor so."""
import json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from cerne import atender, LOCAL, CULT

CASOS=[]
for place,lid in [('canta-rr','roraima'),('rioverde-go','centro-oeste')]:
    cs=LOCAL[lid]['culturas_disponiveis']
    for mes in range(12):
        for colheu in cs:
            for pr in ['solo','risco','comida','pasto']:
                CASOS.append({'lugar':{'id':place,'config_local':lid},'momento':{'mes_plantio':mes},
                              'colheu':colheu,'prioridade':pr,'intencao':'proximo-plantio'})
            for hip in cs:
                CASOS.append({'lugar':{'id':place,'config_local':lid},'momento':{'mes_plantio':mes},
                              'colheu':colheu,'prioridade':'risco','intencao':'e-se','hipotese':hip})
        for it in ['vai-chover','estado-do-solo']:
            CASOS.append({'lugar':{'id':place,'config_local':lid},'momento':{'mes_plantio':mes},
                          'prioridade':'risco','intencao':it})

esperado=[atender(c) for c in CASOS]
import tempfile
tmp=os.path.join(tempfile.gettempdir(),'agrodeal-conformidade.json')
with open(tmp,'w',encoding='utf-8') as f:
    json.dump({'casos':CASOS,'esperado':esperado}, f, ensure_ascii=False)
r=subprocess.run(['node','motor/conformidade.js',tmp],capture_output=True,text=True,encoding='utf-8')
print(r.stdout.strip() or r.stderr.strip())
sys.exit(r.returncode)
