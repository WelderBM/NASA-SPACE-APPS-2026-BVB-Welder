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
        nome = o['cultura'].split(' (')[0].lower()
        if falas and not any(nome in f.lower() for f in falas):
            erros.append(f"fala não cita a opção de cima ({nome}): {falas[0]!r}")

    # 4. todo numero da fala tem que existir na resposta estruturada
    disp = numeros_da_resposta(r)
    for f in falas:
        for n in numeros(f):
            if n not in disp and n.rstrip('0').rstrip('.') not in disp:
                erros.append(f"número {n} na fala e não na resposta: {f!r}")

    # 5. confianca baixa tem que aparecer na fala, nao so no painel
    if o and (o.get('confianca') or 0) < CONF_MIN and r['intencao'] == 'proximo-plantio':
        if falas and not any('%' in f for f in falas):
            erros.append(f"confiança {o['confianca']} e a fala não avisa: {falas[0]!r}")
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
