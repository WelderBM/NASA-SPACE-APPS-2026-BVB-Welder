"""Prototipo do cruzamento. NAO e o motor final: existe para medir
se a nota realmente se move com dado da NASA, ou se e so consulta
de tabela de cultura disfarcada."""
import json, sys

D = 'dados/'
nasa = json.load(open(D+'nasa-power.json'))['lugares']
CULT = json.load(open(D+'culturas.json'))['culturas']
PRIO = json.load(open(D+'prioridades.json'))['prioridades']
LOCAL = {'roraima': json.load(open(D+'local-roraima.json')),
         'centro-oeste': json.load(open(D+'local-centro-oeste.json'))}
DIAS = [31,28,31,30,31,30,31,31,30,31,30,31]
MES = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']

def janela(mes0, dias):
    """meses cobertos pelo ciclo, com fracao do ultimo"""
    out, resto, m = [], dias, mes0
    while resto > 0:
        frac = min(1.0, resto/DIAS[m%12])
        out.append((m%12, frac)); resto -= DIAS[m%12]; m += 1
        if len(out) > 14: break
    return out

def chuva_esperada(place, mes0, dias):
    c = nasa[place]['clim']['chuva_mm']
    return sum(c[m]*f for m,f in janela(mes0, dias))

def veranico_na_fase(place, mes0, fase):
    """maior veranico climatologico nos meses que a fase critica atravessa"""
    v = nasa[place]['clim']['veranico']
    ini, fim = fase
    meses = {(mes0 + d//30) % 12 for d in range(ini, fim+1, 10)}
    return max(v[m] for m in meses), sorted(meses)

# ---- regras de encaixe: caracteristica x observacao -> 0..1 ou None(sem dado)
def encaixe(peso_nome, c, place, mes0):
    ciclo = c.get('ciclo_dias')
    cmin = ciclo[0] if ciclo else None
    if peso_nome == 'familia_diferente':  return 1.0, 'filtro duro ja garantiu'
    if peso_nome == 'fixa_n':             return (1.0 if c['fixa_n'] else 0.0), 'caracteristica'
    if peso_nome == 'residuo_alto':
        return {'alto':1.0,'medio':0.5,'baixo':0.0}.get(c.get('residuo')), 'caracteristica'
    if peso_nome == 'espera_no_campo':
        v = c.get('espera_no_campo');  return (None if v is None else float(v)), 'caracteristica'
    if peso_nome == 'forrageira':         return (1.0 if c.get('forrageira') else 0.0), 'caracteristica'
    if peso_nome == 'tolera_seca':
        return {'alta':1.0,'media':0.6,'baixa':0.2}.get(c.get('tolera_seca')), 'caracteristica'
    if peso_nome == 'ciclo_curto':
        if cmin is None: return None, 'falta ciclo'
        return (1.0 if cmin<=90 else 0.6 if cmin<=150 else 0.3), 'caracteristica'
    if peso_nome == 'agua_baixa':
        ag = c.get('agua_ciclo_mm')
        if not ag or ag[0] is None or cmin is None: return None, 'falta agua_ciclo_mm ou ciclo'
        ch = chuva_esperada(place, mes0, cmin)
        return min(1.0, ch/ag[0]), f'NASA: {ch:.0f}mm esperados / {ag[0]}mm exigidos'
    if peso_nome == 'cabe_na_janela':     return None, 'BLOQUEADO: janela do ZARC nao baixada'
    if peso_nome == 'cobertura_meses':    return None, 'BLOQUEADO: nao existe em culturas.json'
    return None, 'peso desconhecido'

def avalia(local_id, place, colheu, prioridade, mes0):
    loc = LOCAL[local_id]; fam_colhida = CULT[colheu]['familia']
    pesos = PRIO[prioridade]['pesos']; out = []
    for nome in loc['culturas_disponiveis']:
        c = CULT[nome]
        if c['familia'] == fam_colhida: continue                     # filtro 1
        num = den = tot = 0.0; usou_nasa = False; porques = []
        for pn, pw in pesos.items():
            e, why = encaixe(pn, c, place, mes0); tot += pw
            if e is None: continue
            num += pw*e; den += pw
            if why.startswith('NASA'): usou_nasa = True; porques.append(why)
        nota = (num/den) if den else None
        # cruzamento extra, fora dos pesos: veranico x fase critica
        risco = None
        if c.get('fase_critica_dias'):
            vmax, meses = veranico_na_fase(place, mes0, c['fase_critica_dias'])
            risco = f"veranico normal de {vmax:.0f}d na fase critica ({'/'.join(MES[m] for m in meses)})"
            usou_nasa = True
        out.append({'cultura':nome,'familia':c['familia'],'nota':nota,
                    'cobertura': den/tot if tot else 0,'usou_nasa':usou_nasa,
                    'porques':porques,'risco':risco,'qualidade':c['qualidade']})
    out.sort(key=lambda r:(r['nota'] is None, -(r['nota'] or 0)))
    return out

def tabela(titulo, rows):
    print(f"\n{titulo}")
    print(f"  {'cultura':16} {'familia':16} {'nota':>6} {'criterios':>10}  NASA  dado")
    for r in rows:
        n = f"{r['nota']:.2f}" if r['nota'] is not None else "  --"
        print(f"  {r['cultura']:16} {r['familia']:16} {n:>6} {r['cobertura']*100:>9.0f}%  "
              f"{'sim ' if r['usou_nasa'] else 'NAO '} {r['qualidade']}")
        for p in r['porques']: print(f"      + {p}")
        if r['risco']:         print(f"      ! {r['risco']}")

print("="*78); print("CENARIO A  Canta-RR | colheu mandioca | plantio abril")
for pr in ['risco','solo']:
    tabela(f"prioridade = {pr} ({PRIO[pr]['fala']})", avalia('roraima','canta-rr','mandioca',pr,3))
print("\n"+"="*78); print("CENARIO B  Rio Verde-GO | colheu soja | plantio setembro")
for pr in ['risco','solo']:
    tabela(f"prioridade = {pr} ({PRIO[pr]['fala']})", avalia('centro-oeste','rioverde-go','soja',pr,8))
