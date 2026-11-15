"""Cruzamento reestruturado: tres numeros em vez de um.
A nota unica misturava observacao da NASA com virtude abstrata da planta
e apagava o sinal do lugar. Aqui risco e encaixe ficam separados."""
import json
D='dados/'
nasa=json.load(open(D+'nasa-power.json'))['lugares']
CULT=json.load(open(D+'culturas.json'))['culturas']
PRIO=json.load(open(D+'prioridades.json'))['prioridades']
LOCAL={'roraima':json.load(open(D+'local-roraima.json')),
       'centro-oeste':json.load(open(D+'local-centro-oeste.json'))}
DIAS=[31,28,31,30,31,30,31,31,30,31,30,31]
MES=['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']

def jan_(m0,dias):
    o,r,m=[],dias,m0
    while r>0 and len(o)<15:
        o.append((m%12,min(1.0,r/DIAS[m%12]))); r-=DIAS[m%12]; m+=1
    return o

def fator_do_ano(place,m0,n=3):
    """quanto a chuva dos meses ANTES do plantio ficou do normal"""
    c=nasa[place]['clim']['chuva_mm']; o=nasa[place]['ano2026']['chuva_mm']
    ms=[(m0-k)%12 for k in range(1,n+1)]
    if any(o[m] is None for m in ms): return None,None
    obs=sum(o[m] for m in ms); nor=sum(c[m] for m in ms)
    return obs/nor, (obs,nor,[MES[m] for m in reversed(ms)])

def risco(c,place,m0):
    """o que o LUGAR e o MOMENTO dizem sobre plantar esta especie agora"""
    out={}; ciclo=c.get('ciclo_dias'); cmin=ciclo[0] if ciclo else None
    f,det=fator_do_ano(place,m0)
    clim=nasa[place]['clim']
    if cmin:
        ch=sum(clim['chuva_mm'][m]*fr for m,fr in jan_(m0,cmin))
        out['chuva_normal_mm']=round(ch)
        if f: out['chuva_ajustada_mm']=round(ch*f)
        ag=c.get('agua_ciclo_mm')
        if ag and ag[0]:
            r=(ch*(f or 1))/ag[0]; out['agua']={'razao':round(r,2),
              'nivel':'baixo' if r>=1.2 else 'medio' if r>=0.9 else 'alto',
              'exige_mm':ag[0]}
        else: out['agua']={'nivel':'sem dado','motivo':'falta agua_ciclo_mm'}
        # veranico: na fase critica se houver, senao no ciclo todo
        fc=c.get('fase_critica_dias'); ini,fim=(fc if fc else (0,cmin))
        ms=sorted({(m0+d//30)%12 for d in range(ini,fim+1,10)})
        out['veranico']={'dias_normal':max(clim['veranico'][m] for m in ms),
                         'meses':[MES[m] for m in ms],
                         'base':'fase critica' if fc else 'ciclo inteiro'}
    else: out['agua']={'nivel':'sem dado','motivo':'falta ciclo'}
    sr=nasa[place]['ano2026']['solo_raiz'][m0]
    if sr is not None:
        out['solo_no_plantio']={'obs':sr,'normal':clim['solo_raiz'][m0],
          'situacao':'acima' if sr>clim['solo_raiz'][m0] else 'abaixo'}
    out['fator_do_ano']={'razao':round(f,2),'detalhe':det} if f else None
    return out

def encaixe(c,prioridade):
    """o que a ESPECIE oferece para o que ele quer. sem NASA, de proposito."""
    pesos=PRIO[prioridade]['pesos']; num=den=tot=0.0; faltou=[]
    mapa={'fixa_n':1.0 if c['fixa_n'] else 0.0,
          'residuo_alto':{'alto':1.0,'medio':0.5,'baixo':0.0}.get(c.get('residuo')),
          'forrageira':1.0 if c.get('forrageira') else 0.0,
          'espera_no_campo':None if c.get('espera_no_campo') is None else float(c['espera_no_campo']),
          'tolera_seca':{'alta':1.0,'media':0.6,'baixa':0.2}.get(c.get('tolera_seca')),
          'ciclo_curto':None,'familia_diferente':1.0,'agua_baixa':None,
          'cabe_na_janela':None,'cobertura_meses':None}
    ci=c.get('ciclo_dias')
    if ci: mapa['ciclo_curto']=1.0 if ci[0]<=90 else 0.6 if ci[0]<=150 else 0.3
    for pn,pw in pesos.items():
        tot+=pw; e=mapa.get(pn)
        if e is None: faltou.append(pn); continue
        num+=pw*e; den+=pw
    return (num/den if den else None), (den/tot if tot else 0), faltou

def avalia(lid,place,colheu,prioridade,m0):
    fam=CULT[colheu]['familia']; out=[]
    for nome in LOCAL[lid]['culturas_disponiveis']:
        c=CULT[nome]
        if c['familia']==fam: continue
        enc,cob,faltou=encaixe(c,prioridade)
        out.append({'cultura':nome,'fam':c['familia'],'enc':enc,'conf':cob,
                    'faltou':faltou,'risco':risco(c,place,m0)})
    out.sort(key=lambda r:(r['enc'] is None,-(r['enc'] or 0)))
    return out

def mostra(t,rows):
    print(f"\n{t}")
    print(f"  {'cultura':14} {'encaixe':>7} {'conf':>5}  {'agua':>22}  veranico")
    for r in rows:
        e=f"{r['enc']:.2f}" if r['enc'] is not None else "  --"
        a=r['risco'].get('agua',{})
        if 'razao' in a: ag=f"{a['nivel']:5} ({a['razao']}x de {a['exige_mm']}mm)"
        else: ag=f"{a.get('nivel','?')}"
        v=r['risco'].get('veranico')
        vs=f"{v['dias_normal']:.0f}d em {'/'.join(v['meses'])}" if v else "sem ciclo"
        print(f"  {r['cultura']:14} {e:>7} {r['conf']*100:>4.0f}%  {ag:>22}  {vs}")

print("="*84)
print("CANTA-RR | colheu mandioca | plantio abril")
r=avalia('roraima','canta-rr','mandioca','risco',3)
print(f"  fator do ano: {r[0]['risco']['fator_do_ano']}")
mostra("prioridade = risco",r)
mostra("prioridade = solo",avalia('roraima','canta-rr','mandioca','solo',3))
print("\n"+"="*84)
print("RIO VERDE-GO | colheu soja | plantio setembro")
r=avalia('centro-oeste','rioverde-go','soja','risco',8)
print(f"  fator do ano: {r[0]['risco']['fator_do_ano']}")
mostra("prioridade = risco",r)
print("\n"+"="*84)
print("O MESMO MILHO NOS DOIS LUGARES (a prova de que o cerne e generico)")
for lid,pl,co,m in [('roraima','canta-rr','mandioca',3),('centro-oeste','rioverde-go','soja',8)]:
    rr=risco(CULT['milho'],pl,m)
    print(f"  {pl:14} plantio {MES[m]}: normal {rr['chuva_normal_mm']}mm, "
          f"ajustado {rr.get('chuva_ajustada_mm')}mm, exige 500mm -> risco de agua "
          f"{rr['agua']['nivel'].upper()} ({rr['agua']['razao']}x) | "
          f"veranico {rr['veranico']['dias_normal']:.0f}d")
