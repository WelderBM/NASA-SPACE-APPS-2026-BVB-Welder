# Entregas do pitch (chat de benchmark e slides)

> 15/11/2026, 13h50 (Boa Vista). Cópia versionada de tudo o que o chat de
> benchmark e slides gerou. A edição viva continua nos artefatos e no Drive;
> esta pasta é o registro. Regra de sempre: se algo aqui discordar de `docs/`
> ou do motor, o repositório principal manda.

## O que tem aqui

| Pasta | O que é | Original vivo |
| --- | --- | --- |
| `slides-en/` | Os 7 slides em inglês, a versão que vai para o campo Project Demo. Arquivos-fonte do deck (deck.json, deck.css, um HTML por slide, roteiro de fala no `<aside>`) | https://claude.ai/artifact/8vgM1J3M8Jqo4XzjMNhPzV |
| `slides-pt/` | Os mesmos 7 slides em português, só para treino | https://claude.ai/artifact/B5c7gXQRWfndrpbuSnDDt2 |
| `pdf/` | **Os 7 slides exportados em PDF** (EN para o Project Demo, PT só treino), fontes embutidas, sem as notas de fala. Exportados em 15/11, 15h50, depois de rodar o motor de novo (commit d9e6e93) | EN público: https://drive.google.com/file/d/1mKxyajaC_qmSOTCPDL8D4QHTuizu3hN6/view |
| `video-pitch-3min/` | **Vídeo-pitch de 2min49s**, mais denso: problema medido, pessoas, o que existe, demo com a janela do ZARC, como funciona, mesmo código em dois lugares, limites. Só para apresentação local ou apoio, nunca no campo de demo | — |
| `video-pitch/` | **Vídeo-pitch de 29,9 s com história, narração e legenda em inglês.** Roteiro, fontes de cada afirmação e como foi feito no README da pasta | — |
| `animacao/` | (Substituída pelo `video-pitch/`.) Animação de 29,5 s em inglês, com marca d'água de IA (`field-shift-roraima-30s.mp4`) e o script que a gera (`make.py`, Python + PIL + ffmpeg) | — |
| `docs/benchmark-e-proposta-de-valor.md` | Benchmark contra Plantio Certo, RAImundo, JoIA, Plantix, FieldView, Cropwise, Agrolink, Climatempo, vencedores do Space Apps; teste da hipótese | Drive: 1LD9KpiqjeojsQaKOg7nLG9ZgDTJQXoCdTFfOt6ueYhQ |
| `docs/relatorio-critico-do-produto.md` | Relatório crítico do produto em 15/11, 16h: o que conferi no motor, 9 defeitos da demo em ordem de gravidade, cada um com a pergunta de classe, e o que fazer antes das 22h59 | — |
| `docs/texto-de-estudo-do-pitch.md` | Texto longo em português para estudar antes de apresentar, com perguntas difíceis da banca | Drive: 1t7iDUxvjZeTRKCQGOipAoEyJHT-EjVL6WwXTMT7oHwo |

## Onde cada coisa entra na submissão

- **Project Demo:** só os 7 slides em inglês, exportados em PDF com link público. O guia aceita vídeo de até 30 s **ou** até 7 slides, e passar do limite tira do julgamento global.
- **Vídeo-pitch:** pode ir no Project Demo no lugar dos slides (vídeo **ou** slides, nunca os dois). Se o demo for os slides, o vídeo vai como apoio, com link público na Detailed Project Description.

## Ressalvas, para não repetir o que já foi corrigido

- O benchmark é das 12h e foi superado pelo doc 12 em três pontos: o 87% é dos 16.850 estabelecimentos do Censo Agropecuário IBGE 2017; o HydroSCS saiu como precedente; e a pesquisa tem 8 respostas de 7 pessoas.
- A proposta de valor final é a do doc 12 (as ferramentas de rotação otimizam lucro para fazenda grande; esta deixa o pequeno produtor escolher o que otimizar), não a do benchmark.
- Pesquisa, contagem conferida na planilha em 15/11: "planta outra coisa em seguida" em 5 de 8 respostas (4 de 7 pessoas); seca em 6 de 8 respostas (5 de 7 pessoas). 
- Slide 4 traz uma captura real da demo (Cantá, julho, mandioca) no lugar do GIF; slide 7 aponta para welderbm.github.io/NASA-SPACE-APPS-2026-BVB-Welder. Falta o Welder testar os dois links em aba anônima.
- Os 859 mm são a média da série 1981–2026, que inclui 2026. Sem 2026, ~871 mm e a queda continua −62%; a climatologia do motor (812 mm) dá −59%. Slides, vídeo de 3 min e texto de estudo já dizem isso.

- 15/11, 15h25: slides refeitos a partir do `main` em `3347ce9` (nome AgroDeal com subtítulo, caupi 70 dias, milho 686 contra 386 mm, "desde 1981", janela do ZARC, honestidade testada, 4 culturas com dado bom, faixa de El Niño de −48% a +17%).
