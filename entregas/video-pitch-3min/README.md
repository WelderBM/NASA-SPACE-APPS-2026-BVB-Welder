# Vídeo-pitch de 3 minutos (AgroDeal)

> 15/11/2026, 15h25 (Boa Vista). Feito a partir do `main` no commit `3347ce9`, depois de ler os docs 15 a 19.

`agrodeal-pitch-3min.mp4`: 2min49s, 1920×1080, 30 fps, narração em inglês com pausas, legenda em inglês gravada na imagem e em `agrodeal-pitch-3min.en.srt`. Marca d'água visível de IA no canto e declaração no metadado do arquivo.

## Roteiro e de onde vem cada número

| Tempo | Bloco | O que diz | Fonte |
| --- | --- | --- | --- |
| 0:00 | Abertura | Rosa (personagem ilustrativa) colhe mandioca no Cantá e pergunta o que plantar agora | — |
| 0:11 | Nome | AgroDeal, com o subtítulo "What do I plant next?" e a frase do doc 18: o nome diz deal, mas a ferramenta não vende nada | doc 18, seção 1 |
| 0:18 | Problema, dado | Junho a setembro de 2026: 330 mm contra 859 mm (média 1981–2025), o mais baixo desde 1981. Veranico de 24 dias contra 9. Umidade do solo na raiz em setembro igual à de janeiro | `dados/nasa-power.json` (`media_serie_mm`, `ano2026.solo_raiz`) |
| 0:40 | El Niño | Nos anos de El Niño da série, a chuva de junho a setembro foi de −48% a +17%; não há regra, então não prevemos | `nasa-power.json`, `jun_set_el_nino.anos_desenvolvimento`. Ver a ressalva abaixo |
| 0:52 | Pessoas | 87% dos 16.850 estabelecimentos sem assistência técnica (IBGE 2017); o IATER orienta escolher culturas adaptadas ao período seco; 4 de 7 famílias plantam de novo logo após colher; medo de investir (entrevista, Goiás) | docs 03, 12, 15 e 18 |
| 1:15 | O que existe | ZARC responde quando plantar a cultura escolhida; quase todas as ferramentas de rotação otimizam só lucro (Schöning et al., 2023) | doc 12 |
| 1:31 | Demo | Mandioca colhida. Terra melhor: caupi, não é parente. Arriscar pouco em julho: caupi, 70 dias. Janela do ZARC (junho a agosto): encaixe de 53% em abril para 87% em julho. Pasto: braquiária, ciclo desconhecido dito. Renda: 0% medido | saída do `motor/cerne.js`, Cantá, rodada em 15/11 às 15h |
| 1:59 | Como funciona | Risco, encaixe e confiança, sem misturar; aritmética sobre dado nomeado, no navegador | docs 06, 13, 17 |
| 2:16 | Mesmo código | Milho, 500 mm: Cantá em abril 686 mm (risco baixo); Rio Verde em setembro 386 mm (risco alto) | saída do motor, 15/11 às 15h (ciclo do milho no Grupo II do MAPA) |
| 2:29 | Limites e próximos passos | Sem previsão de chuva, sem preço, 14 culturas; mais janelas do ZARC, teste de campo em Roraima, WhatsApp | doc 18 |
| 2:39 | Fecho | AgroDeal não diz à Rosa o que fazer; mostra o que cada escolha faz com a terra neste ano | — |

## Ressalva achada ao conferir o El Niño

O `nasa-power.json` (`o_que_sobrevive`) e o doc 18 dizem que a faixa vai "de −33% a +17%". A própria lista do arquivo traz **2015 com −48%** (e 2023 com −27%). A faixa certa, sem contar 2026, é **de −48% a +17%**. O vídeo, os slides e o texto de estudo usam −48%. Registrado no doc 18.

## Como foi feito (pasta `fonte/`)

Mesmo método do vídeo de 30 s: voz Kokoro TTS (`af_heart`), uma frase por vez com pausas (`tts3.py`, `script.json`); cenas em SVG animadas por JavaScript (`parts.svg`, `script.js`, montadas por `build.py` com o cenário e a personagem do vídeo de 30 s); filmagem quadro a quadro no Chrome sem tela (`render3.py`); trilha sintetizada em código (`music3.py`), em tom menor no trecho do problema.

## Regra do guia

O campo Project Demo aceita vídeo de **até 30 s** ou até 7 slides. **Este vídeo de 3 minutos não pode ir no campo de demo.** Ele serve para a apresentação local, se o líder pedir pitch de 3 minutos, ou como apoio com link público na Detailed Project Description.
