# -*- coding: utf-8 -*-
"""O CERNE. Nao sabe o que e WhatsApp, voz, site ou Telegram.
Recebe uma pergunta estruturada, devolve uma resposta estruturada que
JA CONTEM a frase falada. O canal so toca a frase.

Toda frase sai de molde fixo preenchido com numero medido. Nenhum texto
e redigido por IA: a IA so classifica a intencao na entrada."""
import json, unicodedata

D = 'dados/'
_j = lambda f: json.load(open(D+f, encoding='utf-8'))
NASA  = _j('nasa-power.json')['lugares']
CULT  = _j('culturas.json')['culturas']
PRIO  = _j('prioridades.json')['prioridades']
DEC   = {d['id']: d for d in _j('decisoes.json')['decisoes']}
LOCAL = {'roraima': _j('local-roraima.json'),
         'centro-oeste': _j('local-centro-oeste.json')}
DIAS = [31,28,31,30,31,30,31,31,30,31,30,31]
MES  = ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto',
        'setembro','outubro','novembro','dezembro']

# ---------------------------------------------------------------- observacao
def _janela(m0, dias):
    o, r, m = [], dias, m0
    while r > 0 and len(o) < 15:
        o.append((m % 12, min(1.0, r/DIAS[m % 12]))); r -= DIAS[m % 12]; m += 1
    return o

def fator_do_ano(place, m0, n=3):
    c, o = NASA[place]['clim']['chuva_mm'], NASA[place]['ano2026']['chuva_mm']
    ms = [(m0-k) % 12 for k in range(1, n+1)]
    if any(o[m] is None for m in ms): return None, None
    obs, nor = sum(o[m] for m in ms), sum(c[m] for m in ms)
    return obs/nor, {'observado_mm': round(obs,1), 'normal_mm': nor,
                     'meses': [MES[m] for m in reversed(ms)]}

def estado_observado(place, m0):
    cl, an = NASA[place]['clim'], NASA[place]['ano2026']
    f, det = fator_do_ano(place, m0)
    e = {'mes': MES[m0], 'chuva_normal_do_mes_mm': cl['chuva_mm'][m0],
         'veranico_normal_do_mes_dias': cl['veranico'][m0]}
    if an['solo_raiz'][m0] is not None:
        e['solo_raiz'] = {'observado': an['solo_raiz'][m0],
                          'normal': cl['solo_raiz'][m0],
                          'situacao': 'acima do normal' if an['solo_raiz'][m0] > cl['solo_raiz'][m0] else 'abaixo do normal'}
    if f: e['fator_do_ano'] = {'razao': round(f,2), **det}
    return e

# -------------------------------------------------------------------- risco
def risco(c, place, m0):
    r, nao_sei = {}, []
    ciclo = c.get('ciclo_dias'); cmin = ciclo[0] if ciclo else None
    f, _ = fator_do_ano(place, m0); cl = NASA[place]['clim']
    if cmin is None:
        nao_sei.append('quanto tempo essa cultura leva até a colheita')
        return {'avaliavel': False}, nao_sei
    ch = sum(cl['chuva_mm'][m]*fr for m, fr in _janela(m0, cmin))
    r['chuva_normal_mm'] = round(ch)
    r['chuva_ajustada_mm'] = round(ch*f) if f else None
    ag = c.get('agua_ciclo_mm')
    if ag and ag[0]:
        razao = (ch*(f or 1))/ag[0]
        r['agua'] = {'exige_mm': ag[0], 'razao': round(razao,2),
                     'nivel': 'baixo' if razao >= 1.2 else 'médio' if razao >= 0.9 else 'alto'}
    else:
        r['agua'] = {'nivel': 'sem dado'}
        nao_sei.append('quanta água essa cultura precisa no ciclo')
    fc = c.get('fase_critica_dias'); ini, fim = fc if fc else (0, cmin)
    ms = sorted({(m0 + d//30) % 12 for d in range(ini, fim+1, 10)})
    r['veranico'] = {'dias': max(cl['veranico'][m] for m in ms),
                     'meses': [MES[m] for m in ms],
                     'base': 'na fase crítica' if fc else 'no ciclo'}
    if not fc: nao_sei.append('qual é a fase crítica dessa cultura, então usei o ciclo inteiro')
    r['avaliavel'] = True
    return r, nao_sei

# ------------------------------------------------------------------ encaixe
def encaixe(c, prioridade):
    p = PRIO[prioridade]
    if not p['servivel']: return None, 0.0, [], p['resposta_honesta']
    ci = c.get('ciclo_dias')
    mapa = {'familia_diferente': 1.0,
            'fixa_n': 1.0 if c['fixa_n'] else 0.0,
            'residuo_alto': {'alto':1.0,'medio':0.5,'baixo':0.0}.get(c.get('residuo')),
            'forrageira': 1.0 if c.get('forrageira') else 0.0,
            'tolera_seca': {'alta':1.0,'media':0.6,'baixa':0.2}.get(c.get('tolera_seca')),
            'espera_no_campo': None if c.get('espera_no_campo') is None else float(c['espera_no_campo']),
            'ciclo_curto': (1.0 if ci and ci[0] <= 90 else 0.6 if ci and ci[0] <= 150 else 0.3 if ci else None),
            'agua_baixa': None, 'cabe_na_janela': None, 'cobertura_meses': None}
    num = den = tot = 0.0; faltou = []
    for pn, pw in p['pesos'].items():
        tot += pw; e = mapa.get(pn)
        if e is None: faltou.append(pn); continue
        num += pw*e; den += pw
    return (num/den if den else None), (den/tot if tot else 0.0), faltou, None

# ------------------------------------------------------------------ porques
def porques(c, nome, r, prioridade, fam_colhida, nome_colhido=None):
    """devolve (chave, frase). a chave deixa a fala escolher o porque que casa
    com a prioridade dele, em vez de pegar o primeiro da lista."""
    out = []
    if c['familia'] != fam_colhida:
        quem = nome_colhido or fam_colhida
        out.append(('familia', f"é de outra família que a {quem}, então quebra o ciclo das pragas do solo"))
    a = r.get('agua', {})
    if 'razao' in a:
        ch = r['chuva_ajustada_mm'] or r['chuva_normal_mm']
        out.append(('agua', f"a chuva da janela dá {ch} mm e essa cultura pede {a['exige_mm']} mm"))
    if c['fixa_n']:
        out.append(('solo', "fixa nitrogênio, que é o que melhora a terra"))
    elif c.get('residuo') == 'alto':
        out.append(('solo', "deixa muita palha na superfície"))
    if c.get('tolera_seca') == 'alta':
        out.append(('risco', "aguenta seca melhor que as outras"))
    elif c.get('ciclo_dias') and c['ciclo_dias'][0] <= 90:
        out.append(('risco', f"o ciclo é curto, {c['ciclo_dias'][0]} dias, então fica menos tempo exposto"))
    if c.get('espera_no_campo'):
        out.append(('comida', "pode ficar na terra esperando, serve de estoque"))
    if c.get('forrageira'):
        out.append(('pasto', "serve de pasto"))
    return out

def porque_da_prioridade(pqs, prioridade):
    """escolha deterministica: primeiro o porque da prioridade, depois agua,
    depois familia. nunca aleatorio, nunca redigido por IA."""
    d = {}
    for k, t in pqs: d.setdefault(k, t)
    for k in (prioridade, 'agua', 'familia'):
        if k in d: return d[k]
    return next(iter(d.values()), '')

def avisos(r):
    out = []
    v = r.get('veranico')
    if v and v['dias'] >= 10:
        out.append(f"o veranico normal {'na fase crítica' if v['base']=='fase crítica' else 'no ciclo'} é de {v['dias']:.0f} dias")
    if r.get('agua', {}).get('nivel') == 'alto':
        out.append("a chuva da janela não cobre o que essa cultura pede")
    return out

# ----------------------------------------------------------------- atender
def _norm(s):
    return unicodedata.normalize('NFKD', s.lower()).encode('ascii','ignore').decode()

def classifica(texto):
    """o unico lugar onde IA entraria: casar a fala com uma decisao do catalogo.
    aqui e por palavra-chave, para o MVP rodar sem modelo."""
    t = _norm(texto)
    for d in DEC.values():
        if d['no_mvp'] and any(_norm(k) in t for k in d['como_ele_fala']):
            return d['id']
    return None

def atender(p):
    place = p['lugar']['id']; m0 = p['momento']['mes_plantio']
    lid = p['lugar']['config_local']; loc = LOCAL[lid]
    intencao = p['intencao']; est = estado_observado(place, m0)
    res = {'intencao': intencao, 'lugar': NASA[place]['nome'],
           'mes_plantio': MES[m0], 'estado_observado': est,
           'opcoes': [], 'limites': [], 'fala': None}

    if intencao == 'vai-chover':
        res['limites'].append('não existe previsão de chuva nestes dados; a série é histórica')
        s = est.get('solo_raiz')
        res['fala'] = (f"Eu não sei prever chuva, não tenho essa informação. "
                       f"O que eu sei é que {est['mes']} normalmente dá {est['chuva_normal_do_mes_mm']} "
                       f"milímetros" + (f" e a terra está {s['situacao']}." if s else ".") +
                       " Para previsão, veja o boletim do INMET.")
        return res

    colheu = p.get('colheu'); fam = CULT[colheu]['familia'] if colheu else None
    candidatas = ([p['hipotese']] if intencao == 'e-se' and p.get('hipotese')
                  else loc['culturas_disponiveis'])
    for nome in candidatas:
        c = CULT.get(nome)
        if not c: continue
        if fam and c['familia'] == fam and intencao != 'e-se':
            continue
        r, ns = risco(c, place, m0)
        enc, conf, faltou, recusa = encaixe(c, p['prioridade'])
        _pqs = porques(c, nome, r, p['prioridade'], fam,
                       CULT[colheu]['nome'].split(' (')[0].lower()) if fam else []
        res['opcoes'].append({
            'cultura': c['nome'], 'id': nome, 'familia': c['familia'],
            'mesma_familia_do_que_colheu': bool(fam and c['familia'] == fam),
            'risco': r, 'encaixe': round(enc,2) if enc is not None else None,
            'confianca': round(conf,2),
            'porques': [t for _, t in _pqs], '_pqs': _pqs,
            'avisos': avisos(r), 'nao_sei': ns,
            'qualidade_do_dado': c['qualidade'],
            'validar_com_tecnico': ['a janela de plantio oficial do ZARC para o município'],
        })
    # SEPARACAO CRITICA: uma cultura cujo ciclo a gente nao sabe nao pode ser
    # a recomendacao falada. Antes a braquiaria vencia com 27% de confianca:
    # quanto menos dado, melhor o ranking. Isso era bug, e saia na voz.
    res['sei_pouco'] = [{'cultura': o['cultura'], 'familia': o['familia'],
                         'falta': o['nao_sei']} for o in res['opcoes']
                        if not o['risco'].get('avaliavel')]
    res['opcoes'] = [o for o in res['opcoes'] if o['risco'].get('avaliavel')]
    res['opcoes'].sort(key=lambda o: (o['encaixe'] is None, -(o['encaixe'] or 0)))

    if not res['opcoes'] and res.get('sei_pouco'):
        res['fala'] = (f"Das culturas que dão aí, eu sei a família de "
                       f"{len(res['sei_pouco'])}, mas não sei o ciclo de nenhuma. "
                       f"Sem isso eu não arrisco indicar. Quer que eu diga o que sei?")
        return res
    if intencao == 'e-se' and res['opcoes']:
        o = res['opcoes'][0]
        if o['mesma_familia_do_que_colheu']:
            res['fala'] = (f"{o['cultura']} é da mesma família da {colheu}. "
                           f"Plantar seguido deixa a praga do solo se multiplicar. Eu não indicaria.")
        else:
            a = o['risco'].get('agua', {})
            res['fala'] = (f"{o['cultura']} dá para plantar. " +
                           (f"O risco de água é {a['nivel']}: a janela dá "
                            f"{o['risco']['chuva_ajustada_mm'] or o['risco']['chuva_normal_mm']} "
                            f"milímetros e ela pede {a['exige_mm']}. " if 'razao' in a
                            else "Da água eu não sei, falta dado dessa cultura. ") +
                           "Quer comparar com as outras?")
    elif res['opcoes']:
        o = res['opcoes'][0]
        nome_f = o['cultura'].split(' (')[0].lower()
        a = o['risco'].get('agua', {})
        if a.get('nivel') == 'alto':
            # o encaixe pode ser bom e o lugar nao permitir. o aviso vem PRIMEIRO.
            ch = o['risco']['chuva_ajustada_mm'] or o['risco']['chuva_normal_mm']
            res['fala'] = (f"Pelo que você quer, {nome_f} seria a melhor, mas eu te aviso: "
                           f"a chuva da janela dá {ch} milímetros e ela pede {a['exige_mm']}. "
                           f"Quer ver o que arrisca menos?")
            o.setdefault('avisos', []).insert(0, 'o encaixe é bom mas o lugar não dá a água que ela pede')
        else:
            pq = porque_da_prioridade(o['_pqs'], p['prioridade'])
            res['fala'] = (f"Depois da {colheu}, o que mais encaixa é {nome_f}. " +
                           (f"{pq[0].upper()+pq[1:]}. " if pq else "") + "Quer saber o risco?")
    for o in res['opcoes']: o.pop('_pqs', None)
    res['limites'].append('a janela de plantio oficial do ZARC não está carregada; confirme com técnico')
    return res

if __name__ == '__main__':
    import sys
    casos = [
      ("1. CANTÁ, RR — colheu mandioca, quer arriscar pouco, planta em abril",
       {'lugar':{'id':'canta-rr','config_local':'roraima'},'momento':{'mes_plantio':3},
        'colheu':'mandioca','prioridade':'risco','intencao':'proximo-plantio'}),
      ("2. O MESMO produtor, mas agora quer que a TERRA melhore",
       {'lugar':{'id':'canta-rr','config_local':'roraima'},'momento':{'mes_plantio':3},
        'colheu':'mandioca','prioridade':'solo','intencao':'proximo-plantio'}),
      ("3. ELE EXPLORA: 'e se eu plantar milho?'",
       {'lugar':{'id':'canta-rr','config_local':'roraima'},'momento':{'mes_plantio':3},
        'colheu':'mandioca','prioridade':'risco','intencao':'e-se','hipotese':'milho'}),
      ("4. ELE PERGUNTA O QUE EU NÃO SEI: 'vai chover semana que vem?'",
       {'lugar':{'id':'canta-rr','config_local':'roraima'},'momento':{'mes_plantio':3},
        'prioridade':'risco','intencao':'vai-chover'}),
      ("5. OUTRO LUGAR, mesma pergunta do caso 1: Rio Verde, GO, colheu soja, setembro",
       {'lugar':{'id':'rioverde-go','config_local':'centro-oeste'},'momento':{'mes_plantio':8},
        'colheu':'soja','prioridade':'risco','intencao':'proximo-plantio'}),
    ]
    for titulo, p in casos:
        r = atender(p)
        print("="*76); print(titulo); print("="*76)
        print(f'FALA DO BOT: "{r["fala"]}"')
        if r['opcoes']:
            print(f"\n  {'opção':16} {'encaixe':>7} {'conf':>5} {'água':>24}  veranico")
            for o in r['opcoes'][:4]:
                e = f"{o['encaixe']:.2f}" if o['encaixe'] is not None else "  --"
                a = o['risco'].get('agua', {})
                ag = (f"{a['nivel']:6} {a['razao']}x de {a['exige_mm']}mm" if 'razao' in a
                      else a.get('nivel','?'))
                v = o['risco'].get('veranico')
                print(f"  {o['cultura'][:16]:16} {e:>7} {o['confianca']*100:>4.0f}% {ag:>24}  "
                      + (f"{v['dias']:.0f}d {v['base']}" if v else "sem ciclo"))
            o = r['opcoes'][0]
            if o['porques']: print("  porquês:", "; ".join(o['porques']))
            if o['avisos']:  print("  avisos: ", "; ".join(o['avisos']))
            if o['nao_sei']: print("  não sei:", "; ".join(o['nao_sei']))
        print("  limites:", "; ".join(r['limites']), "\n")
