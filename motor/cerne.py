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
# abaixo disso a nota se apoia na minoria dos criterios, entao a cultura ainda
# aparece na lista mas nao pode ser a indicacao falada sem o aviso junto
CONF_MIN = 0.5
# se a cultura que a gente conhece MAL encaixa muito melhor no que ele pediu do
# que a melhor que a gente conhece bem, calar sobre ela e esconder a resposta.
# foi o caso do pasto: a unica forrageira era a braquiaria, sem ciclo, e o bot
# recomendava feijao-caupi com encaixe 0,28 e confianca 1,0, sem ressalva.
MARGEM_SEM_CICLO = 0.25
MES  = ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto',
        'setembro','outubro','novembro','dezembro']

# Portugues neutro: o que o motor fala quando o lugar nao trouxe vocabulario.
# Serve de rede e, na demo, aparece como limite declarado.
MOLDES_NEUTROS = {
  'indicacao': "Depois {de_colheu}, a melhor opção é {cultura}. {porque}. Quer saber os riscos?",
  'indicacao_com_aviso': "Pelo que você quer, {cultura} seria a melhor, porque {porque}. Mas pode faltar água para ela. Quer ver uma de menor risco?",
  'indicacao_com_aviso_sem_porque': "Pelo que você quer, {cultura} seria a melhor, mas pode faltar água para ela. Quer ver uma de menor risco?",
  'hipotese_boa': "Dá para plantar {cultura}. A chuva do período atende o que ela precisa. Quer comparar com as outras?",
  'hipotese_ruim': "Dá para plantar {cultura}, mas pode faltar água. A chuva do período fica abaixo do que ela precisa. Quer ver outra?",
  'hipotese_parente': "{cultura} é da mesma família {de_colheu}. Plantar em seguida multiplica as pragas de solo. Não recomendo.",
  'hipotese_mesma': "Essa é a mesma cultura que acabou de ser colhida. Repetir multiplica as pragas de solo. Não recomendo.",
  'hipotese_parente_sem_ciclo': "{cultura} é da mesma família {de_colheu}, então não recomendo. Do resto eu não sei: falta a duração do ciclo.",
  'hipotese_sem_ciclo': "{cultura} não é da mesma família {de_colheu}, o que já ajuda, e {mes} costuma ter {chuva}. Falta a duração do ciclo.",
  'sem_dado': "Das culturas da região eu sei a família de {n}, mas não sei a duração de nenhuma. Sem isso eu não indico.",
  'estado_da_terra': "O solo está {estado}. {mes} costuma ter {chuva}.",
  'fechos_terra': "",
  'nao_sei_prever': "Previsão de chuva eu não tenho. {mes} costuma ter {chuva}, com estiagem máxima de {estiagem} dias, e o solo está {estado}.",
  'hipotese_sem_agua': "{cultura} não é da mesma família {de_colheu}. A exigência de água dela não está registrada; a janela acumula {chuva_mm} mm e a estiagem máxima {base} é de {estiagem} dias.",
  'indicacao_pouca_confianca': "Depois {de_colheu}, a melhor opção é {cultura}, mas só {pct}% dos critérios dessa prioridade puderam ser avaliados nela.",
  'lacuna_falada': "A leitura deste ano vai até {ate}; para {mes} há apenas a média de {anos} anos, sem ajuste pelo ano corrente.",
  'melhor_sem_ciclo': "Para esse objetivo a cultura indicada seria {cultura}, porque {porque}. Falta a duração do ciclo dela. Entre as avaliáveis, {alternativa} é a mais próxima.",
  'melhor_sem_ciclo_sem_porque': "Para esse objetivo a cultura indicada seria {cultura}, mas falta a duração do ciclo dela. Entre as avaliáveis, {alternativa} é a mais próxima.",
  'solo_fundo': "Camada superficial {sup}; camada profunda {fundo}. A reserva profunda é a que sustenta no veranico.",
  'aviso_calor': "A máxima de {mes} chega a {pico} °C, acima do limite de {limite} °C dessa cultura.",
  'agua_sem_numero': "A exigência de água dela não está registrada. A janela acumula {chuva_mm} mm e a estiagem máxima {base} é de {estiagem} dias.",
  'porques': {'familia': "é de outra família {de_colheu}, então as pragas de solo têm menos chance de continuar",
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

# concordancia num lugar so. O motor arredonda, a estiagem de junho e julho da
# 1,2 e virava "1 dias" na boca do bot. Nenhum teste olhava gramatica: o
# invariantes.py testava honestidade. Vale para TODOS os moldes de uma vez, em
# vez de consertar molde por molde, que e consertar o caso e nao a classe.
# o par mais longo vem PRIMEIRO: 'dias seguidos' tem que virar 'dia seguido'
# antes de 'dias' virar 'dia', senao sobra "1 dia seguidos". Dicionario preserva
# a ordem de insercao em Python e em JS, e os dois motores dependem disso.
_PLURAL = {'dias seguidos': 'dia seguido', 'meses seguidos': 'mês seguido',
           'dias': 'dia', 'milímetros': 'milímetro', 'graus': 'grau',
           'meses': 'mês', 'anos': 'ano'}
def _conc(t):
    for pl, sg in _PLURAL.items():
        t = t.replace(' 1 ' + pl, ' 1 ' + sg)
    return t

def _fmt(t, **kw):
    return _conc(t.format(**kw))

def render_all(M, chave, fechos=None, **kw):
    """devolve TODAS as variantes da frase. a pagina sorteia sem repetir, e o
    bot deixa de soar gravado. a autoria continua sendo do molde, nunca da IA."""
    corpos = _lista(M.get(chave, ''))
    fs = _lista(M.get(fechos) or ['']) if fechos else ['']
    out = []
    for b in corpos:
        for f in fs:
            try: t = _fmt(b, **kw)
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

def ate_onde_enxergo(place):
    """ate que mes a serie observada de 2026 chega naquele lugar"""
    ch = NASA[place]['ano2026']['chuva_mm']
    idx = [i for i, v in enumerate(ch) if v is not None]
    return max(idx) if idx else None

def lacunas_do_lugar(place, m0):
    """UM lugar so que sabe o que falta e POR QUE. Antes cada consumidor de
    dado tratava o nulo no ponto de uso, com o if que estivesse ali, e por isso
    metade das combinacoes de lugar e mes degradava sem dizer nada."""
    an, out = NASA[place]['ano2026'], []
    ate = ate_onde_enxergo(place)
    if ate is None: return out
    falta_chuva = any(an['chuva_mm'][(m0 - k) % 12] is None for k in (1, 2, 3))
    if falta_chuva:
        out.append({'o_que': 'como o ano está indo', 'ate': MES[ate], 'falar': True,
                    'por_que': f'a leitura deste ano vai até {MES[ate]}',
                    'efeito': 'uso só a média da série, sem ajustar pelo ano corrente'})
    if an['solo_raiz'][m0] is None:
        out.append({'o_que': 'umidade do solo deste mês', 'ate': MES[ate], 'falar': not falta_chuva,
                    'por_que': f'a leitura deste ano vai até {MES[ate]}',
                    'efeito': 'uso só a média da série'})
    return out

def estado_observado(place, m0):
    cl, an = NASA[place]['clim'], NASA[place]['ano2026']
    f, det = fator_do_ano(place, m0)
    e = {'mes': MES[m0], 'anos_de_serie': NASA[place].get('abr_set', {}).get('anos_base'),
         'chuva_normal_do_mes_mm': cl['chuva_mm'][m0],
         'chuva_qualitativa': qualifica_chuva(place, m0),
         'veranico_normal_do_mes_dias': cl['veranico'][m0]}
    if an['solo_raiz'][m0] is not None:
        o, n = an['solo_raiz'][m0], cl['solo_raiz'][m0]
        dif = (o - n)/n if n else 0.0
        e['solo_raiz'] = {'observado': o, 'normal': n, 'diferenca': _r(dif, 3),
            'situacao': 'media' if abs(dif) < 0.03 else ('acima' if dif > 0 else 'abaixo')}
    # o solo tem TRES profundidades no POWER e o motor lia uma. a de cima engana:
    # chuva recente molha a superficie e a reserva de baixo pode estar vazia.
    for chave, campo in (('solo_superficie','solo_sup'), ('solo_profundo','solo_perfil')):
        ob, no = an[campo][m0], cl[campo][m0]
        if ob is None: continue
        d = (ob - no)/no if no else 0.0
        e[chave] = {'observado': ob, 'normal': no, 'diferenca': _r(d, 3),
                    'situacao': 'media' if abs(d) < 0.03 else ('acima' if d > 0 else 'abaixo')}
    sup, fun = e.get('solo_superficie'), e.get('solo_profundo')
    if sup and fun and fun['situacao'] == 'abaixo' and sup['situacao'] != 'abaixo' and (sup['diferenca'] - fun['diferenca']) >= 0.08:
        e['superficie_engana'] = True
    e['tsolo_c'] = cl['tsolo'][m0]
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
    tl = c.get('tmax_sofre_c')
    if tl:
        pico, mp = max((cl['tmax'][m], m) for m, _ in _janela(m0, cmin))
        if pico > tl: r['calor'] = {'limite': tl, 'pico': _r(pico), 'mes': MES[mp]}
    else:
        nao_sei.append('a partir de que temperatura essa cultura sofre')
    r['avaliavel'] = True
    return r, nao_sei

# ------------------------------------------------------------------ encaixe
def cobertura(c):
    """quantos meses a cultura cobre o chao. DERIVADO do ciclo, sem fonte:
    solo descoberto e o que lava. marcado como derivado em prioridades.json."""
    if 'perene' in (c.get('ciclo_nota') or '').lower(): return 1.0
    ci = c.get('ciclo_dias')
    if not ci: return None
    return min(1.0, (ci[0]/30.0)/6.0)

def cabe_na_janela(nome, loc, m0):
    """o mes de plantio esta dentro da janela do ZARC daquele lugar? sem
    janela carregada devolve None, que vira lacuna declarada, nunca zero."""
    j = (loc.get('janelas_zarc') or {}).get(nome) or {}
    ini, fim = j.get('inicio_mes'), j.get('fim_mes')
    if ini is None or fim is None: return None
    dentro = (ini <= m0 <= fim) if ini <= fim else (m0 >= ini or m0 <= fim)
    return 1.0 if dentro else 0.0

def encaixe(c, prioridade, nome=None, loc=None, m0=None):
    p = PRIO[prioridade]
    if not p['servivel']: return None, 0.0, [], p['resposta_honesta']
    ci = c.get('ciclo_dias')
    mapa = {'familia_diferente': 1.0, 'fixa_n': 1.0 if c['fixa_n'] else 0.0,
            'residuo_alto': {'alto':1.0,'medio':0.5,'baixo':0.0}.get(c.get('residuo')),
            'forrageira': 1.0 if c.get('forrageira') else 0.0,
            'tolera_seca': {'alta':1.0,'media':0.6,'baixa':0.2}.get(c.get('tolera_seca')),
            'espera_no_campo': None if c.get('espera_no_campo') is None else float(c['espera_no_campo']),
            'ciclo_curto': (1.0 if ci and ci[0] <= 90 else 0.6 if ci and ci[0] <= 150 else 0.3 if ci else None),
            'agua_baixa': None,
            'cabe_na_janela': (cabe_na_janela(nome, loc, m0) if (nome and loc and m0 is not None) else None),
            'cobertura_meses': cobertura(c)}
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

def render_porque(pqs, prioridade, moldes, colheu_nome, de_colheu='',
                  evitar=None, quantos=1):
    """evitar: chave de porque que nao deve ser usada. Serve para o
    melhor_sem_ciclo, onde a razao da PROPRIA prioridade e tautologica:
    "quem serve e braquiaria, e ela serve de pasto". quantos: quantas razoes
    juntar. O motor tinha quatro razoes prontas da braquiaria e falava zero,
    e falava a unica lacuna duas vezes."""
    d = {}
    for k, pr in pqs: d.setdefault(k, pr)
    if evitar: d.pop(evitar, None)
    ordem = ([prioridade, prioridade+'_seca'] if prioridade == 'risco'
             else [prioridade]) + ['agua', 'familia']
    saida = []
    for k in ordem + [k for k in d if k not in ordem]:
        if k in d and len(saida) < quantos:
            t = _fmt(moldes['porques'].get(k, ''), colheu=colheu_nome,
                     de_colheu=de_colheu, **d[k])
            if t: saida.append((t, k))
    if not saida: return '', None
    if quantos == 1: return saida[0]
    return ', e '.join(t for t, _ in saida), saida[0][1]

def avisos(r, moldes):
    out = []
    v = r.get('veranico')
    if r.get('agua_indireta') and v:
        # sem o numero dela, a chuva da janela e a estiagem na fase critica ainda
        # sao resposta. Antes de 15/11 o bot calava aqui, ou pior: afirmava.
        out.append(_fmt(_lista(moldes.get('agua_sem_numero', ''))[0],
            chuva_mm=r.get('chuva_ajustada_mm') or r.get('chuva_normal_mm'),
            estiagem=_r(v['dias']), base=v['base']))
    elif v and v['dias'] >= 10:
        out.append(f"a estiagem normal {v['base']} é de {_r(v['dias'])} dias")
    if r.get('agua', {}).get('nivel') == 'alto':
        out.append("a chuva do período não cobre o que essa cultura pede")
    cal = r.get('calor')
    if cal:
        out.append(_fmt(_lista(moldes.get('aviso_calor', ''))[0], **cal))
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
           'estado_observado': est, 'lacunas': lacunas_do_lugar(place, m0),
           'opcoes': [], 'sei_pouco': [], 'limites': [],
           'fala': None, 'falas': [], 'aviso_do_ano': None, 'destaque': None}

    if intencao == 'estado-do-solo':
        sr = est.get('solo_raiz')
        res['falas'] = render_all(M, 'estado_da_terra', 'fechos_terra',
            mes=est['mes'], chuva=M['chuva_qualitativa'][est['chuva_qualitativa']],
            estado=M['estado_terra'][sr['situacao']] if sr else 'sem leitura')
        res['fala'] = res['falas'][0]
        if est.get('superficie_engana'):
            sup, fun = est['solo_superficie'], est['solo_profundo']
            res['aviso_do_ano'] = _fmt(_lista(M.get('solo_fundo',''))[0],
                sup=M['estado_terra'][sup['situacao']], fundo=M['estado_terra'][fun['situacao']])
        if not sr: res['limites'].append('sem leitura de umidade do solo para este mês')
        for l in res['lacunas']:
            res['limites'].append(f"{l['o_que']}: {l['por_que']}, então {l['efeito']}")
        if [x for x in res['lacunas'] if x.get('falar')] and not res.get('aviso_do_ano'):
            l = [x for x in res['lacunas'] if x.get('falar')][0]
            res['aviso_do_ano'] = render_all(M, 'lacuna_falada', ate=l['ate'],
                mes=est['mes'], anos=est.get('anos_de_serie') or 45)[0]
        return res
    if intencao == 'vai-chover':
        res['limites'].append('não existe previsão de chuva nestes dados; a série é histórica')
        s = est.get('solo_raiz')
        res['falas'] = render_all(M, 'nao_sei_prever',
            mes=est['mes'], chuva=M['chuva_qualitativa'][est['chuva_qualitativa']],
            estiagem=_r(est['veranico_normal_do_mes_dias']),
            estado=M['estado_terra'][s['situacao']] if s else 'sem leitura')
        res['fala'] = res['falas'][0]
        for l in res['lacunas']:
            res['limites'].append(f"{l['o_que']}: {l['por_que']}, então {l['efeito']}")
        if [x for x in res['lacunas'] if x.get('falar')] and not res.get('aviso_do_ano'):
            l = [x for x in res['lacunas'] if x.get('falar')][0]
            res['aviso_do_ano'] = render_all(M, 'lacuna_falada', ate=l['ate'],
                mes=est['mes'], anos=est.get('anos_de_serie') or 45)[0]
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
        enc, conf, faltou, _ = encaixe(c, p['prioridade'], nome, loc, m0)
        pqs = porques(c, r, fam) if fam else []
        res['opcoes'].append({
            'cultura': c['nome'], 'id': nome, 'familia': c['familia'],
            'ciclo_dias': c.get('ciclo_dias'),
            'mesma_familia_do_que_colheu': bool(fam and c['familia'] == fam),
            'risco': r, 'encaixe': _r(enc,2) if enc is not None else None,
            'confianca': _r(conf,2), '_pqs': pqs,
            'porques': [_fmt(M['porques'].get(k,''), colheu=cn, de_colheu=dcn, **pr) for k, pr in pqs],
            'avisos': avisos(r, M), 'nao_sei': ns,
            # o que o aviso ja falou nao volta no "e tem coisa que eu nao sei":
            # a pagina dizia a mesma ignorancia duas vezes na mesma frase
            'nao_sei_nao_dito': [x for x in ns if not (r.get('agua_indireta') and 'água' in x)],
            'qualidade_do_dado': c['qualidade'],
            # o que a propria linha da cultura manda validar vem do dado, nao daqui:
            # a especie do cara e suposicao e o motor engolia o aviso que o dado trazia
            'validar_com_tecnico': (c.get('validar_com_tecnico') or [])
                                   + ['a janela de plantio oficial do ZARC para o município'],
        })
    sem_janela = [o['cultura'] for o in res['opcoes']
                  if not (loc.get('janelas_zarc') or {}).get(o['id'], {}).get('inicio_mes')]
    if sem_janela:
        res['lacunas'].append({'o_que': 'a janela oficial de plantio',
            'por_que': f"o ZARC não está carregado para {len(sem_janela)} das culturas daqui",
            'efeito': 'não dá para dizer se cabe na janela recomendada', 'falar': False})
    # a confianca vem junto: sem ela nada conseguia barrar uma cultura daqui de
    # virar destaque com encaixe inflado por ignorancia (ver o bloco abaixo)
    res['sei_pouco'] = [{'cultura': o['cultura'], 'id': o['id'], 'familia': o['familia'],
                         'encaixe': o['encaixe'], 'confianca': o['confianca'],
                         '_pqs': o.get('_pqs') or [], 'falta': o['nao_sei']}
                        for o in res['opcoes'] if not o['risco'].get('avaliavel')]
    res['sei_pouco'].sort(key=lambda x: (x['encaixe'] is None, -(x['encaixe'] or 0)))
    res['opcoes'] = [o for o in res['opcoes'] if o['risco'].get('avaliavel')]
    # quem quer arriscar pouco nao recebe no topo uma cultura que o dado da NASA
    # diz que vai faltar agua, nem uma cuja agua a gente nao sabe medir. Antes o
    # risco aparecia ao lado e nao mudava a ordem: na seca do Canta o arroz
    # (agua "sem dado") passava na frente do caupi.
    def agua_ruim(o):
        return 1 if p['prioridade'] == 'risco' and \
            (o['risco'].get('agua') or {}).get('nivel') in ('alto', 'sem dado') else 0
    res['opcoes'].sort(key=lambda o: (o['encaixe'] is None,
        0 if (o['confianca'] or 0) >= CONF_MIN else 1, agua_ruim(o), -(o['encaixe'] or 0)))

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
        elif res['opcoes'][0]['risco'].get('agua', {}).get('nivel') == 'sem dado':
            # NAO dizer que a chuva da quando nao se sabe quanto ela pede
            rk = res['opcoes'][0]['risco']; v = rk.get('veranico') or {}
            res['falas'] = render_all(M, 'hipotese_sem_agua',
                chuva_mm=rk.get('chuva_ajustada_mm') or rk.get('chuva_normal_mm'),
                estiagem=_r(v.get('dias', 0)), base=v.get('base', 'no ciclo'), **kw)
        else:                    res['falas'] = render_all(M, 'hipotese_boa', 'fechos_hipotese', **kw)
    elif not res['opcoes'] and res['sei_pouco']:
        res['falas'] = render_all(M, 'sem_dado', n=len(res['sei_pouco']))
    elif res['opcoes']:
        o = res['opcoes'][0]
        sp = res['sei_pouco'][0] if res['sei_pouco'] else None
        # A MARGEM NAO BASTAVA, porque ela subtraia dois encaixes medidos em
        # quantidades diferentes de evidencia. A braquiaria tirava 1,00 na
        # prioridade 'risco' com UM critério dos quatro medido (tolera_seca), e
        # roubava o destaque de quem tinha 0,60 com tres medidos. Resultado: em
        # 5 dos 6 meses, a resposta de "arriscar pouco" era uma cultura cujo
        # ciclo a gente nao sabe, na prioridade em que o ciclo e o critério
        # principal. A porteira da confianca, que ja valia para as opcoes, agora
        # vale aqui tambem. No 'pasto' a braquiaria tem confianca 1,00, com os
        # tres critérios conhecidos, entao ela continua ganhando: e o caso que a
        # correcao original queria, e ele sobrevive.
        if sp and (sp['confianca'] or 0) >= CONF_MIN \
                and (sp['encaixe'] or 0) - (o['encaixe'] or 0) >= MARGEM_SEM_CICLO:
            res['destaque'] = sp['id']
            # DIZ O QUE SABE ANTES DO QUE NAO SABE. Na conversa de 16h15 o bot
            # recomendou braquiaria para pasto com confianca 1,00, quatro
            # razoes medidas na mao (forrageira, residuo alto, tolera seca,
            # familia diferente) e falou NENHUMA, so a lacuna do ciclo. Evita a
            # razao da propria prioridade, que aqui seria tautologica.
            pq, _ = render_porque(sp.get('_pqs') or [], p['prioridade'], M, cn, dcn,
                                  evitar=p['prioridade'], quantos=2)
            res['falas'] = render_all(M, 'melhor_sem_ciclo' if pq else 'melhor_sem_ciclo_sem_porque',
                cultura=nome_curto(sp['id']), alternativa=nome_curto(o['id']), porque=pq)
            # o aviso da braquiaria NAO entra nos avisos da mandioca: a pagina
            # junta os avisos numa frase so, e o "ela" da frase seguinte, que e
            # da mandioca, era lido como sendo da braquiaria. Dois numeros de uma
            # cultura atribuidos a outra. A fala ja diz o que falta na braquiaria.
        elif (o['confianca'] or 0) < CONF_MIN:
            res['falas'] = render_all(M, 'indicacao_pouca_confianca', colheu=cn, de_colheu=dcn,
                cultura=nome_curto(o['id']), pct=_r((o['confianca'] or 0)*100))
            o['avisos'].insert(0, f"só {_r((o['confianca'] or 0)*100)}% dos critérios dessa prioridade puderam ser avaliados")
        elif o['risco'].get('agua', {}).get('nivel') == 'alto':
            # dizia so a ma noticia: 234 das 816 indicacoes caem aqui e nenhuma
            # dizia POR QUE a cultura e a melhor. Evita a razao 'agua', senao a
            # frase diz "a chuva da o que ela precisa, mas pode faltar agua".
            pqa, _ = render_porque(o['_pqs'], p['prioridade'], M, cn, dcn, evitar='agua')
            res['falas'] = render_all(M,
                'indicacao_com_aviso' if pqa else 'indicacao_com_aviso_sem_porque',
                'fechos_aviso', cultura=nome_curto(o['id']), porque=pqa)
            o['avisos'].insert(0, 'o encaixe é bom mas o lugar não dá a água que ela pede')
        else:
            pq, _ = render_porque(o['_pqs'], p['prioridade'], M, cn, dcn)
            res['falas'] = render_all(M, 'indicacao', 'fechos', colheu=cn, de_colheu=dcn,
                                      cultura=nome_curto(o['id']),
                                      porque=pq[0].upper()+pq[1:] if pq else '')
        # arriscar pouco num mes em que NENHUMA opcao tem agua garantida: a
        # primeira coisa do "o que pode dar errado" e isso
        if intencao != 'e-se' and res['opcoes'] and all(agua_ruim(x) for x in res['opcoes']):
            res['opcoes'][0]['avisos'].insert(0, 'nesse mês todas as opções daqui têm risco alto '
                'de faltar água, ou água que eu não sei medir')
    fal = [l for l in res['lacunas'] if l.get('falar')]
    if fal and not res.get('aviso_do_ano'):
        l = fal[0]
        res['aviso_do_ano'] = render_all(M, 'lacuna_falada', ate=l['ate'],
            mes=est['mes'], anos=est.get('anos_de_serie') or 45)[0]
    fa = est.get('fator_do_ano')
    if fa and intencao in ('proximo-plantio', 'e-se') and res.get('falas'):
        rz = fa['razao']
        if rz <= 0.9 or rz >= 1.1:
            chave = 'aviso_ano_seco' if rz <= 0.9 else 'aviso_ano_chuvoso'
            res['aviso_do_ano'] = render_all(M, chave, pct=_r(rz*100))[0]
    if res.get('falas'): res['fala'] = res['falas'][0]
    if not res.get('destaque') and res['opcoes']: res['destaque'] = res['opcoes'][0]['id']
    for o in res['opcoes']: o.pop('_pqs', None)
    for sp_ in res['sei_pouco']: sp_.pop('_pqs', None)
    for l in res['lacunas']:
        res['limites'].append(f"{l['o_que']}: {l['por_que']}, então {l['efeito']}")
    # a linha fixa do ZARC saiu daqui: era incondicional e por isso FALSA para o
    # caupi, cuja janela esta carregada, e repetia a lacuna condicional de cima.
    # Quem precisa confirmar com tecnico ja vai em validar_com_tecnico da opcao.
    res['limites'].append('de onde vem a semente ou a muda e quanto ela custa não entra aqui; '
                          'esta resposta diz o que plantar, não se dá para comprar')
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
