# -*- coding: utf-8 -*-
"""O CERNE. Nao sabe o que e WhatsApp, voz, site ou Telegram, e tambem NAO
SABE FALAR RORAIMENSE: o vocabulario e os moldes de frase vivem na camada
local. Trocar de lugar troca a lingua junto com o dado.

Recebe pergunta estruturada, devolve resposta estruturada que ja contem a
frase pronta. Toda frase sai de molde fixo preenchido com numero medido.
Nenhum texto e redigido por IA: a IA so classifica a intencao na porta."""
import json, unicodedata, math

# Python arredonda 0.625 para 0.62 (bancario) e o JavaScript para 0.63
# (meio-pra-cima). Com dois motores isso vira divergencia silenciosa, que e
# pior que um motor so. floor(x+0.5) e exatamente o Math.round do JS, e como os
# dois usam IEEE 754, o resultado bate bit a bit.
def _r(x, n=0):
    if x is None: return None
    if n == 0: return int(math.floor(x + 0.5))
    k = 10 ** n
    return math.floor(x * k + 0.5) / k

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

# Portugues neutro: o que o motor fala quando o lugar nao trouxe vocabulario.
# Serve de rede e, na demo, aparece como limite declarado.
MOLDES_NEUTROS = {
  'indicacao': "Depois {de_colheu}, a melhor opção é {cultura}. {porque}. Quer saber os riscos?",
  'indicacao_com_aviso': "Pelo que você quer, {cultura} seria a melhor, mas pode faltar água para ela. Quer ver uma de menor risco?",
  'hipotese_boa': "{cultura} pode ser plantada. A chuva do período atende o que ela precisa. Quer comparar com as outras?",
  'hipotese_ruim': "{cultura} pode ser plantada, mas pode faltar água. A chuva do período fica abaixo do que ela precisa. Quer ver outra?",
  'hipotese_parente': "{cultura} é da mesma família {de_colheu}. Plantar em seguida multiplica as pragas de solo. Não recomendo.",
  'hipotese_mesma': "Essa é a mesma cultura que acabou de ser colhida. Repetir multiplica as pragas de solo. Não recomendo.",
  'hipotese_parente_sem_ciclo': "{cultura} é da mesma família {de_colheu}, então não recomendo. Do resto eu não sei: falta a duração do ciclo.",
  'hipotese_sem_ciclo': "{cultura} não é da mesma família {de_colheu}, o que já ajuda, e {mes} costuma ter {chuva}. Falta a duração do ciclo.",
  'sem_dado': "Das culturas da região eu sei a família de {n}, mas não sei a duração de nenhuma. Sem isso eu não indico.",
  'estado_da_terra': "O solo está {estado}. {mes} costuma ter {chuva}.",
  'fechos_terra': "",
  'nao_sei_prever': "Previsão de chuva eu não tenho. {mes} costuma ter {chuva}, com estiagem máxima de {estiagem} dias, e o solo está {estado}.",
  'agua_sem_numero': "A exigência de água dela não está registrada. A janela acumula {chuva_mm} mm e a estiagem máxima {base} é de {estiagem} dias.",
  'porques': {'familia': "é de outra família {de_colheu}, então as pragas de solo não se mantêm",
              'agua': "a chuva do período atende o que ela precisa",
              'solo': "melhora o solo para o que vem depois",
              'risco': "é de ciclo curto, {dias} dias",
              'risco_seca': "tolera estiagem melhor que as outras",
              'comida': "pode permanecer no campo, serve de reserva",
              'pasto': "serve de pasto"},
  'estado_terra': {'acima': "mais úmido que o normal", 'abaixo': "mais seco que o normal",
                   'media': "dentro do normal"},
  'aviso_ano_seco': "O ano acumulou {pct}% da chuva normal até aqui; considere menos água disponível.",
  'aviso_ano_chuvoso': "O ano acumulou {pct}% da chuva normal até aqui, acima do costume.",
  'chuva_qualitativa': {'muita': "chuva alta", 'media': "chuva média", 'pouca': "chuva baixa"},
}

def _moldes(loc):
    m = dict(MOLDES_NEUTROS); m.update(loc.get('moldes', {})); return m

def _lista(v): return v if isinstance(v, list) else [v]

def render_all(M, chave, fechos=None, **kw):
    """devolve TODAS as variantes da frase. a pagina sorteia sem repetir, e o
    bot deixa de soar gravado. a autoria continua sendo do molde, nunca da IA."""
    corpos = _lista(M.get(chave, ''))
    fs = _lista(M.get(fechos) or ['']) if fechos else ['']
    out = []
    for b in corpos:
        for f in fs:
            try: t = b.format(**kw)
            except KeyError: continue
            t = (t + ' ' + f).strip() if f else t.strip()
            if t: t = t[0].upper() + t[1:]
            if t and t not in out: out.append(t)
    return out[:8]

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
    return obs/nor, {'observado_mm': _r(obs,1), 'normal_mm': nor,
                     'meses': [MES[m] for m in reversed(ms)]}

def qualifica_chuva(place, m):
    """qualitativo, relativo ao PROPRIO lugar: 146mm e muito em Rio Verde e
    mediano no Canta. Tercis dos 12 meses daquela coordenada."""
    c = sorted(NASA[place]['clim']['chuva_mm']); v = NASA[place]['clim']['chuva_mm'][m]
    return 'pouca' if v <= c[3] else 'muita' if v >= c[8] else 'media'

def estado_observado(place, m0):
    cl, an = NASA[place]['clim'], NASA[place]['ano2026']
    f, det = fator_do_ano(place, m0)
    e = {'mes': MES[m0], 'chuva_normal_do_mes_mm': cl['chuva_mm'][m0],
         'chuva_qualitativa': qualifica_chuva(place, m0),
         'veranico_normal_do_mes_dias': cl['veranico'][m0]}
    if an['solo_raiz'][m0] is not None:
        o, n = an['solo_raiz'][m0], cl['solo_raiz'][m0]
        dif = (o - n)/n if n else 0.0
        e['solo_raiz'] = {'observado': o, 'normal': n, 'diferenca': _r(dif, 3),
            'situacao': 'media' if abs(dif) < 0.03 else ('acima' if dif > 0 else 'abaixo')}
    if f: e['fator_do_ano'] = {'razao': _r(f,2), **det}
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
    r['chuva_normal_mm'] = _r(ch)
    r['chuva_ajustada_mm'] = _r(ch*f) if f else None
    ag = c.get('agua_ciclo_mm')
    if ag and ag[0]:
        razao = (ch*(f or 1))/ag[0]
        r['agua'] = {'exige_mm': ag[0], 'razao': _r(razao,2),
                     'nivel': 'baixo' if razao >= 1.2 else 'médio' if razao >= 0.9 else 'alto'}
    else:
        r['agua'] = {'nivel': 'sem dado'}
        nao_sei.append('quanta água essa cultura precisa')
        r['agua_indireta'] = True   # sem o numero dela, ainda da pra cruzar o resto
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
    mapa = {'familia_diferente': 1.0, 'fixa_n': 1.0 if c['fixa_n'] else 0.0,
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

# ------------------------------------------------------- porques etiquetados
def porques(c, r, fam_colhida):
    """devolve [(chave, params)]. A FRASE vem do molde do lugar, nao daqui:
    e assim que o mesmo motor fala roraimense em Canta e neutro em Rio Verde."""
    out = []
    if c['familia'] != fam_colhida: out.append(('familia', {}))
    if 'razao' in r.get('agua', {}) and r['agua']['nivel'] != 'alto': out.append(('agua', {}))
    if c['fixa_n'] or c.get('residuo') == 'alto': out.append(('solo', {}))
    if c.get('tolera_seca') == 'alta': out.append(('risco_seca', {}))
    elif c.get('ciclo_dias') and c['ciclo_dias'][0] <= 90:
        out.append(('risco', {'dias': c['ciclo_dias'][0]}))
    if c.get('espera_no_campo'): out.append(('comida', {}))
    if c.get('forrageira'): out.append(('pasto', {}))
    return out

def render_porque(pqs, prioridade, moldes, colheu_nome, de_colheu=''):
    d = {}
    for k, pr in pqs: d.setdefault(k, pr)
    ordem = ([prioridade, prioridade+'_seca'] if prioridade == 'risco'
             else [prioridade]) + ['agua', 'familia']
    for k in ordem:
        if k in d:
            return moldes['porques'].get(k, '').format(colheu=colheu_nome, de_colheu=de_colheu, **d[k]), k
    for k, pr in d.items():
        return moldes['porques'].get(k, '').format(colheu=colheu_nome, de_colheu=de_colheu, **pr), k
    return '', None

def avisos(r, moldes):
    out = []
    v = r.get('veranico')
    if r.get('agua_indireta') and v:
        # nao sei o numero dela, mas sei a chuva da janela e a estiagem na fase
        # critica. isso e resposta, e antes eu calava.
        out.append(_lista(moldes.get('agua_sem_numero', ''))[0].format(
            chuva_mm=r.get('chuva_ajustada_mm') or r.get('chuva_normal_mm'),
            estiagem=_r(v['dias']), base=v['base']))
    elif v and v['dias'] >= 10:
        out.append(f"a estiagem normal {v['base']} é de {_r(v['dias'])} dias")
    if r.get('agua', {}).get('nivel') == 'alto':
        out.append("a chuva do período não cobre o que essa cultura pede")
    return out

# ----------------------------------------------------------------- atender
def _norm(s): return unicodedata.normalize('NFKD', s.lower()).encode('ascii','ignore').decode()

def classifica(texto):
    t = _norm(texto)
    for d in DEC.values():
        if d['no_mvp'] and any(_norm(k) in t for k in d['como_ele_fala']): return d['id']
    return None

def atender(p):
    place = p['lugar']['id']; m0 = p['momento']['mes_plantio']
    loc = LOCAL[p['lugar']['config_local']]; M = _moldes(loc)
    intencao = p['intencao']; est = estado_observado(place, m0)
    nome_curto = lambda n: CULT[n]['nome'].split(' (')[0].lower()
    def de(n):
        a = CULT[n].get('artigo', 'a')
        return ('da ' if a == 'a' else 'do ') + nome_curto(n)
    res = {'intencao': intencao, 'lugar': NASA[place]['nome'], 'mes_plantio': MES[m0],
           'registro': 'local' if loc.get('moldes') else 'português neutro',
           'estado_observado': est, 'opcoes': [], 'sei_pouco': [], 'limites': [],
           'fala': None, 'falas': [], 'aviso_do_ano': None}

    if intencao == 'estado-do-solo':
        sr = est.get('solo_raiz')
        res['falas'] = render_all(M, 'estado_da_terra', 'fechos_terra',
            mes=est['mes'], chuva=M['chuva_qualitativa'][est['chuva_qualitativa']],
            estado=M['estado_terra'][sr['situacao']] if sr else 'sem leitura')
        res['fala'] = res['falas'][0]
        if not sr: res['limites'].append('sem leitura de umidade do solo para este mês')
        return res
    if intencao == 'vai-chover':
        res['limites'].append('não existe previsão de chuva nestes dados; a série é histórica')
        s = est.get('solo_raiz')
        res['falas'] = render_all(M, 'nao_sei_prever',
            mes=est['mes'], chuva=M['chuva_qualitativa'][est['chuva_qualitativa']],
            estiagem=_r(est['veranico_normal_do_mes_dias']),
            estado=M['estado_terra'][s['situacao']] if s else 'sem leitura')
        res['fala'] = res['falas'][0]
        return res

    colheu = p.get('colheu'); fam = CULT[colheu]['familia'] if colheu else None
    cn = nome_curto(colheu) if colheu else ''
    dcn = de(colheu) if colheu else ''
    cands = [p['hipotese']] if intencao == 'e-se' and p.get('hipotese') else loc['culturas_disponiveis']
    for nome in cands:
        c = CULT.get(nome)
        if not c: continue
        if fam and c['familia'] == fam and intencao != 'e-se': continue
        r, ns = risco(c, place, m0)
        enc, conf, faltou, _ = encaixe(c, p['prioridade'])
        pqs = porques(c, r, fam) if fam else []
        res['opcoes'].append({
            'cultura': c['nome'], 'id': nome, 'familia': c['familia'],
            'mesma_familia_do_que_colheu': bool(fam and c['familia'] == fam),
            'risco': r, 'encaixe': _r(enc,2) if enc is not None else None,
            'confianca': _r(conf,2), '_pqs': pqs,
            'porques': [M['porques'].get(k,'').format(colheu=cn, de_colheu=dcn, **pr) for k, pr in pqs],
            'avisos': avisos(r, M), 'nao_sei': ns, 'qualidade_do_dado': c['qualidade'],
            'validar_com_tecnico': ['a janela de plantio oficial do ZARC para o município'],
        })
    res['sei_pouco'] = [{'cultura': o['cultura'], 'familia': o['familia'], 'falta': o['nao_sei']}
                        for o in res['opcoes'] if not o['risco'].get('avaliavel')]
    res['opcoes'] = [o for o in res['opcoes'] if o['risco'].get('avaliavel')]
    res['opcoes'].sort(key=lambda o: (o['encaixe'] is None, -(o['encaixe'] or 0)))

    if intencao == 'e-se' and p.get('hipotese'):
        h = p['hipotese']; alvo = nome_curto(h)
        parente = CULT[h]['familia'] == fam
        avaliavel = bool(res['opcoes'])
        kw = dict(cultura=alvo, colheu=cn, de_colheu=dcn)
        if h == colheu:          res['falas'] = render_all(M, 'hipotese_mesma', **kw)
        elif parente and not avaliavel:
                                 res['falas'] = render_all(M, 'hipotese_parente_sem_ciclo', **kw)
        elif parente:            res['falas'] = render_all(M, 'hipotese_parente', **kw)
        elif not avaliavel:      res['falas'] = render_all(M, 'hipotese_sem_ciclo',
            mes=est['mes'], chuva=M['chuva_qualitativa'][est['chuva_qualitativa']], **kw)
        elif res['opcoes'][0]['risco'].get('agua', {}).get('nivel') == 'alto':
                                 res['falas'] = render_all(M, 'hipotese_ruim', 'fechos_hipotese', **kw)
        else:                    res['falas'] = render_all(M, 'hipotese_boa', 'fechos_hipotese', **kw)
    elif not res['opcoes'] and res['sei_pouco']:
        res['falas'] = render_all(M, 'sem_dado', n=len(res['sei_pouco']))
    elif res['opcoes']:
        o = res['opcoes'][0]
        if o['risco'].get('agua', {}).get('nivel') == 'alto':
            res['falas'] = render_all(M, 'indicacao_com_aviso', 'fechos_aviso',
                                      cultura=nome_curto(o['id']))
            o['avisos'].insert(0, 'o encaixe é bom mas o lugar não dá a água que ela pede')
        else:
            pq, _ = render_porque(o['_pqs'], p['prioridade'], M, cn, dcn)
            res['falas'] = render_all(M, 'indicacao', 'fechos', colheu=cn, de_colheu=dcn,
                                      cultura=nome_curto(o['id']),
                                      porque=pq[0].upper()+pq[1:] if pq else '')
    fa = est.get('fator_do_ano')
    if fa and intencao in ('proximo-plantio', 'e-se') and res.get('falas'):
        rz = fa['razao']
        if rz <= 0.9 or rz >= 1.1:
            chave = 'aviso_ano_seco' if rz <= 0.9 else 'aviso_ano_chuvoso'
            res['aviso_do_ano'] = render_all(M, chave, pct=_r(rz*100))[0]
    if res.get('falas'): res['fala'] = res['falas'][0]
    for o in res['opcoes']: o.pop('_pqs', None)
    res['limites'].append('a janela de plantio oficial do ZARC não está carregada; confirme com técnico')
    return res

if __name__ == '__main__':
    casos = [
      ("1. CANTÁ — colheu mandioca, quer arriscar pouco, planta em abril",
       {'lugar':{'id':'canta-rr','config_local':'roraima'},'momento':{'mes_plantio':3},
        'colheu':'mandioca','prioridade':'risco','intencao':'proximo-plantio'}),
      ("2. O MESMO, mas quer que a terra melhore",
       {'lugar':{'id':'canta-rr','config_local':'roraima'},'momento':{'mes_plantio':3},
        'colheu':'mandioca','prioridade':'solo','intencao':'proximo-plantio'}),
      ("3. ELE EXPLORA: 'e se eu plantar milho?'",
       {'lugar':{'id':'canta-rr','config_local':'roraima'},'momento':{'mes_plantio':3},
        'colheu':'mandioca','prioridade':'risco','intencao':'e-se','hipotese':'milho'}),
      ("4. HIPÓTESE DE PARENTE: colheu caupi, 'e se eu plantar caupi de novo?'",
       {'lugar':{'id':'canta-rr','config_local':'roraima'},'momento':{'mes_plantio':3},
        'colheu':'feijao-caupi','prioridade':'risco','intencao':'e-se','hipotese':'feijao-caupi'}),
      ("5. O QUE EU NÃO SEI: 'vai chover semana que vem?'",
       {'lugar':{'id':'canta-rr','config_local':'roraima'},'momento':{'mes_plantio':3},
        'prioridade':'risco','intencao':'vai-chover'}),
      ("6. OUTRO LUGAR, sem vocabulário levantado: Rio Verde, colheu soja, setembro",
       {'lugar':{'id':'rioverde-go','config_local':'centro-oeste'},'momento':{'mes_plantio':8},
        'colheu':'soja','prioridade':'risco','intencao':'proximo-plantio'}),
    ]
    for t, p in casos:
        r = atender(p)
        print("="*74); print(t); print(f"[registro: {r['registro']}]")
        print(f'>> "{r["fala"]}"'); print()
