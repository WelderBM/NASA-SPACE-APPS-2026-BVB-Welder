# -*- coding: utf-8 -*-
"""As regras de honestidade viram TESTE.

A conformidade garante que os dois motores dizem a MESMA coisa. Ela não garante
que a coisa dita seja verdadeira. Quase todo defeito de hoje foi disso: o padrão
vencendo o silêncio, e a decisão ficando no documento em vez de no código.

No doc 13 eu desenhei um verificador para a futura IA redatora: todo número da
saída tem que estar na entrada, toda cultura citada tem que estar nas opções.
Nunca apliquei em mim. É o que este arquivo faz."""
import json, re, sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from cerne import atender, LOCAL, CULT, CONF_MIN

AFIRMA_AGUA = ['dá o que ela precisa', 'atende o que ela precisa', 'dá o que ela pede',
               'cobre o que ela pede', 'dá conta dela', 'a chuva desse tempo dá']
AFIRMA_SOLO = ['mais seca', 'mais seco', 'mais molhada', 'mais úmido']

# O doc 11 trocou palavra por palavra. A lista de la, virada teste:
# 'inverno' e 'verao' nunca, porque no Norte significam o contrario;
# o resto e jargao que o produtor nao usa.
# 'inverno' e 'verao' em qualquer lugar: as duas invertem de sentido entre as
# regioes, entao o bot nao usa nenhuma das duas em canto nenhum. O resto e
# jargao em todo lugar.
JARGAO = ['inverno', 'verão', 'nitrogênio', 'inmet', 'pousio',
          'sucessão', 'euphorbiaceae', 'cucurbitaceae', 'poaceae', 'fabaceae',
          'convolvulaceae', 'dioscoreaceae', 'solanaceae', 'musaceae']
# 'veranico' e decisao do doc 11 e vale SO em Roraima, onde os respondentes
# dizem 'estiagem'. No Centro-Oeste veranico e a palavra local e correta, e o
# molde padrao do cerne.py usa ela de proposito. Eu tinha posto na lista global
# hoje as 15h20 e isso reprovaria texto certo de Rio Verde: armadilha minha,
# achada na varredura dos moldes as 16h.
JARGAO_ROraima = ['veranico']

# 10. gramatica. O motor arredonda e a estiagem de junho, 1,2 dias, virava
# "1 dias". Um teste de concordancia pega a classe toda de uma vez; antes
# nenhum teste olhava a PALAVRA, so o numero e a honestidade.
_SG = 'dia|milímetro|grau|mês|ano'
PLURAL_ERRADO = re.compile(r'\b1\s+(?:[a-zà-ú]+(?:s|es)\b|(?:' + _SG + r')\s+[a-zà-ú]+s\b)', re.I)

def numeros(t):
    return {n.replace(',', '.') for n in re.findall(r'\d+(?:[.,]\d+)?', t or '')}

def numeros_da_resposta(r):
    vistos = set()
    def anda(v):
        if isinstance(v, dict):
            for k, x in v.items():
                if k in ('falas', 'fala', 'aviso_do_ano', 'avisos', 'porques', 'limites',
                         'nao_sei', 'validar_com_tecnico'): continue
                anda(x)
        elif isinstance(v, list):
            for x in v: anda(x)
        elif isinstance(v, (int, float)):
            vistos.add(str(v)); vistos.add(str(int(v)) if v == int(v) else str(v))
            # floor(x+0.5), igual aos dois motores. round() do Python daria 6
            # para 6.5 e o teste acusaria a fala correta de inventar numero.
            vistos.add(str(int(math.floor(v*100 + 0.5))))   # porcentagens
            vistos.add(str(int(math.floor(v + 0.5))))       # como e falado
    anda(r)
    return vistos

def checa(r, caso):
    erros = []
    falas = (r.get('falas') or []) + ([r['aviso_do_ano']] if r.get('aviso_do_ano') else [])
    o = (r.get('opcoes') or [None])[0]

    # 1. nao afirmar sobre agua sem saber quanto a cultura pede
    if o and (o['risco'].get('agua') or {}).get('nivel') == 'sem dado':
        for f in falas:
            for frase in AFIRMA_AGUA:
                if frase in f.lower():
                    erros.append(f"afirma água sem dado: {f!r}")

    # 2. nao dar direcao ao solo quando ele esta dentro da faixa
    sr = (r.get('estado_observado') or {}).get('solo_raiz')
    if sr and sr.get('situacao') == 'media':
        for f in falas:
            for frase in AFIRMA_SOLO:
                if frase in f.lower(): erros.append(f"dá direção a solo na média: {f!r}")

    # 3. a cultura falada tem que ser a primeira opcao, nunca outra
    if o and r['intencao'] == 'proximo-plantio':
        d = r.get('destaque')
        alvo = next((x for x in (r.get('opcoes') or []) + (r.get('sei_pouco') or [])
                     if x.get('id') == d), o)
        nome = alvo['cultura'].split(' (')[0].lower()
        if falas and not any(nome in f.lower() for f in falas):
            erros.append(f"fala não cita a opção de cima ({nome}): {falas[0]!r}")

    # 4. todo numero da fala tem que existir na resposta estruturada
    disp = numeros_da_resposta(r)
    for f in falas:
        for n in numeros(f):
            if n not in disp and n.rstrip('0').rstrip('.') not in disp:
                erros.append(f"número {n} na fala e não na resposta: {f!r}")

    # 5. degradar em silencio e proibido: se falta dado do ano, a resposta diz
    if [l for l in (r.get('lacunas') or []) if l.get('falar')] and not r.get('aviso_do_ano'):
        erros.append(f"degrada em silêncio: lacuna {r['lacunas'][0]['o_que']} e a resposta não declara")

    # 6. confianca baixa tem que aparecer na fala, nao so no painel
    if o and (o.get('confianca') or 0) < CONF_MIN and r['intencao'] == 'proximo-plantio':
        if falas and not any('%' in f for f in falas):
            erros.append(f"confiança {o['confianca']} e a fala não avisa: {falas[0]!r}")

    # 8. o vocabulario do doc 11 tambem e regra, e nao era testado.
    # O molde do solo dizia "veranico" depois de o doc 11 decidir "estiagem",
    # e passou dois dias porque nenhum teste olhava a PALAVRA, so o numero.
    # 'inverno' e 'verao' sao o caso grave: no Norte inverno e a estacao
    # CHUVOSA, entao a palavra inverte a resposta na boca do bot.
    proibidas = list(JARGAO)
    if (caso.get('lugar') or {}).get('config_local') == 'roraima':
        proibidas += JARGAO_ROraima
    for f in falas:
        baixo = f.lower()
        for palavra in proibidas:
            if palavra in baixo:
                erros.append(f"jargao na fala: {palavra!r} em {f[:90]!r}")

    # 10. concordancia: "1 dias" e "1 dia seguidos" nao saem da boca do bot
    for t in falas + [r.get('aviso_do_ano') or ''] + [
             x for o in (r.get('opcoes') or []) for x in (o.get('avisos') or [])]:
        m = PLURAL_ERRADO.search(t or '')
        if m:
            erros.append(f"plural errado: {m.group(0)!r} em {t[:80]!r}")

    # 9. uma cultura que o motor NAO consegue avaliar so pode ser a resposta se
    # a confianca dela passar a porteira. Sem isso, encaixe alto tirado de um
    # critério medido vence encaixe honesto tirado de tres.
    sp = (r.get('sei_pouco') or [])
    if r.get('destaque') and sp and r['destaque'] == sp[0].get('id'):
        if (sp[0].get('confianca') or 0) < CONF_MIN:
            erros.append(f"destaque sem lastro: {r['destaque']} e inavaliavel e tem "
                         f"confianca {sp[0].get('confianca')}")

    # 7. o que a LINHA da cultura manda validar nao pode morrer no motor.
    # O dado do cara trazia "qual especie se planta aqui e suposicao" e a
    # resposta devolvia so a janela do ZARC: o motor engolia o aviso do dado.
    for op in (r.get('opcoes') or []):
        pedido = (CULT.get(op['id'], {}) or {}).get('validar_com_tecnico') or []
        levou = op.get('validar_com_tecnico') or []
        faltou = [x for x in pedido if x not in levou]
        if faltou:
            erros.append(f"o dado manda validar e a resposta não leva: {op['id']} perdeu {faltou[0]!r}")
    return erros

if __name__ == '__main__':
    casos, falhas, total = [], {}, 0
    for place, lid in [('canta-rr','roraima'), ('rioverde-go','centro-oeste')]:
        cs = LOCAL[lid]['culturas_disponiveis']
        for mes in range(12):
            for colheu in cs:
                for pr in ['solo','risco','comida','pasto']:
                    casos.append({'lugar':{'id':place,'config_local':lid},'momento':{'mes_plantio':mes},
                                  'colheu':colheu,'prioridade':pr,'intencao':'proximo-plantio'})
                for hip in cs:
                    casos.append({'lugar':{'id':place,'config_local':lid},'momento':{'mes_plantio':mes},
                                  'colheu':colheu,'prioridade':'risco','intencao':'e-se','hipotese':hip})
            for it in ['vai-chover','estado-do-solo']:
                casos.append({'lugar':{'id':place,'config_local':lid},'momento':{'mes_plantio':mes},
                              'prioridade':'risco','intencao':it})
    for c in casos:
        total += 1
        for e in checa(atender(c), c):
            chave = e.split(':')[0]
            falhas.setdefault(chave, []).append((c, e))
    if not falhas:
        print(f"OK: {total} casos, nenhuma afirmação sem lastro")
    else:
        for k, v in sorted(falhas.items(), key=lambda x: -len(x[1])):
            print(f"\n{len(v)}x  {k}")
            for c, e in v[:2]:
                print(f"   {json.dumps({k2:v2 for k2,v2 in c.items() if k2!='lugar'}, ensure_ascii=False)}")
                print(f"   {e[:190]}")
        print(f"\n{sum(len(v) for v in falhas.values())} violações em {total} casos")
    sys.exit(1 if falhas else 0)
