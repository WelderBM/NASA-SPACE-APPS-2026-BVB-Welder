# Convenções de quem contribui

Este arquivo é instrução, e é o único lugar do repositório onde isso é o caso.
Os documentos em `docs/` descrevem o projeto; aqui se descreve como mexer nele.

## Git

Antes de dar push, confira a versão do momento. Se houver diferença, estude o que
está lá e atualize com base nisso. Nunca force push. Ao diffar o que chegou,
compare contra o **merge-base**, não contra a sua própria ponta: diffar contra a
ponta mostra o seu próprio trabalho como se tivesse sido removido.

Cada etapa fechada ganha um branch `marco-revN-data`. O commit diz **por que** a
mudança foi feita, não só o que mudou.

## Testes, antes de qualquer push

```
python3 motor/conformidade.py   # 2.748 casos: Python e JavaScript respondem igual
python3 motor/invariantes.py    # 2.748 casos: dez regras de honestidade
```

Mexeu num dos dois motores, rode os dois. Os números dos invariantes são
identificadores, não ordem de leitura: `docs/` e commits citam "invariante 7",
"8", "9", "10".

## Dado

Nenhum número entra em documento, slide ou código sem fonte e sem data de
leitura. Cada linha de dado marca a própria qualidade, e o que depende de
validação técnica carrega `validar_com_tecnico`.

Confira unidade duas vezes. O NASA POWER devolve `PRECTOTCORR` em **mm/dia**, não
mm/mês. Chuva anual não é água de ciclo: `agua_ciclo_mm` é a exigência **do
ciclo**, e ECOCROP e Embrapa publicam chuva por ano, então nenhum dos dois serve
para esse campo.

Ao achar um defeito, pergunte qual é a **classe** dele antes de consertar o caso.

## Registro

Documento descreve o projeto. O que fica em cada linha é a decisão, a data, a
fonte e o motivo.

Fora, porque um leitor de fora não usa: "vamos fazer", "acho que", sugestão sem
dono, autoria de quem propôs uma ideia descartada (o motivo do descarte fica),
narração em primeira pessoa e detalhe da ferramenta usada para escrever o texto.
Provenância de **decisão** fica: "decisão do Welder, 15/11" é informação.

O uso de IA é declarado por inteiro no campo *Use of AI* da submissão.

## Vocabulário do produto

O bot nunca diz "inverno" nem "verão": no Norte inverno é a estação chuvosa, e a
palavra inverteria a resposta. Em Roraima é "estiagem", não "veranico" — no
Centro-Oeste veranico é a palavra local e correta. Nada de nome de família
botânica na fala. O `invariantes.py` testa isso.

As frases vivem nos moldes dos arquivos de lugar, nunca no motor. Nos moldes
`agua_sem_numero`, `aviso_calor` e `solo_fundo` só a primeira variante roda:
escreva a melhor primeiro.

## Privacidade

Telefone, nome e qualquer coisa que identifique quem respondeu a pesquisa não
entram neste repositório, que é público — nem como link para material que os
contenha. Ficam na planilha privada do Drive. Os números agregados vão em
`dados/local-roraima.json`, sem identificar ninguém.
