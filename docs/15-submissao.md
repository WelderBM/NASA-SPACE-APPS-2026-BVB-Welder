# 15 — Os campos da submissão, rascunho em inglês

> 15/11/2026, 13h30. Rascunho dos campos listados no doc 09, escrito a partir
> do `main` no commit `677c22b`. Os textos de cada campo estão em texto puro,
> sem markdown e sem travessão, prontos para colar. **Tudo o que está entre
> colchetes é pendência para o Welder.**
>
> A lista de campos vem do doc 09. O guia de submissão de 2026 não foi relido
> nesta rodada: o fetch pediu aprovação e ficou sem resposta. Conferir na
> página do projeto se os nomes e os limites de tamanho batem.

## Regras que os textos respeitam

- Só número que está no repositório, com a fonte no próprio texto ou no campo de referências.
- Nada de "nenhuma ferramenta faz isso" sobre o que o ZARC e o RAImundo fazem (doc 12).
- O que não fazemos está escrito: previsão de chuva, preço, mão de obra, cobertura de culturas.
- Sem o nome AgroDeal, que não foi checado.
- O estado da tabela de culturas é o do `main`: 14 culturas, 3 marcadas como dado bom, 4 parcial, 7 falta; 10 das 14 sem ciclo. Se o branch `ecocrop-ciclo-15-11` entrar, atualizar a frase do campo 5.

---

## 1. Project Name

[Decisão do Welder. O título da demo hoje é "Assistente da roça". Sugestão descritiva, sem nome de marca:]

```
Assistente da Roça: what to plant after this harvest
```

## 2. High-Level Project Summary

```
Most crop rotation tools optimize for profit on large farms. A peer reviewed survey (Schöning et al.) found that almost all of them optimize only farm profit, and that all of them ignore plots of a few hundred square meters. In Roraima, Brazil, 87% of the 16,850 farm establishments had no technical assistance in the 2017 IBGE Agricultural Census.

Our tool starts from the harvest the farmer just finished and answers one question: what should I plant next? The farmer picks what to optimize: the soil, low risk, food for the family, or pasture. Changing that choice reorders the answer, which is how the farmer explores rotation strategies instead of receiving one recommendation.

Each answer comes as three separate numbers, never mixed: risk (NASA POWER rainfall and soil moisture for that place and month), fit (crop traits against the farmer's priority) and confidence (how much of the answer we could actually measure). It says plainly what it does not know, including selling price, labor and rain forecasts. It talks by voice in Portuguese, in the words local farmers used in our survey, and it computes in the browser with no server.
```

## 3. Link to Project Demo

[Link público dos 7 slides, feitos no outro chat. Testar em aba anônima.]

## 4. Link to Final Project

```
https://welderbm.github.io/NASA-SPACE-APPS-2026-BVB-Welder/
```

[Se o campo aceitar mais de um link, o repositório: https://github.com/WelderBM/NASA-SPACE-APPS-2026-BVB-Welder]

## 5. Detailed Project Description

```
The problem. The 2026 El Niño hit Roraima hard. At our reference point in Cantá (lat 2.61, lon -60.60), NASA POWER shows 330 mm of rain from June to September 2026 against an 859 mm average, minus 62% and the worst of the 45 year series. The longest dry spell inside the rainy season was 24 days, against a 9 day average. In September, root zone soil moisture was 0.51 against a normal of 0.76, a level that place usually only reaches in January. We do not claim 2027 will repeat this: in the same series, El Niño decay years, which is where 2027 falls, averaged only 2% below normal.

The decision. Six of the eight answers to our farmer survey said that after a harvest they plant something else right away. That is the decision we support: one crop cycle ahead, starting from what was just harvested.

How it works. A deterministic engine takes the farmer's harvest, priority, place and month, and returns structured facts. Three numbers stay separate:
Risk uses NASA data. Rain expected in the crop's growing window is the NASA POWER long-term climatology adjusted by how the last three months compared to normal, divided by the crop's minimum water need. It also reports the longest typical dry spell in the window and whether root zone soil moisture is above or below normal for the month.
Fit uses crop traits only: nitrogen fixation, residue, drought tolerance, cycle length, whether it can wait in the field, whether it is forage. Each priority weighs these differently.
Confidence is the share of the priority's criteria we could actually evaluate for that crop. A low number is shown, not hidden.
Hard rule: never follow a crop with a crop from the same botanical family. The bot says it as "it is not related to cassava, so the pest left in the soil will not take it".

Same code, different place. With the same maize data, planting in April in Cantá gives low water risk (621 mm adjusted against 500 mm needed). Planting in September in Rio Verde, Goiás gives high risk (331 mm). Both places lost about half their April to September rain in 2026, but the dry spell was 2.6 times normal in Cantá and unchanged in Rio Verde. That is why nothing is hard coded per place: data is by coordinate, and each place carries its own crop list and its own wording.

How it talks. Words come from our survey respondents in Roraima: "terra fraca" for weak soil, "estiagem" for dry spell. The bot never says winter or summer, because in the Amazon "winter" means the rainy season and the meaning would flip.

What it does not do. It has no rain forecast; the official ZARC Plantio Certo app has one, and we were built to sit next to it, not replace it. It does not answer price or labor questions and says so. Planting windows from ZARC are not loaded yet. Of the 14 crops in the table, 3 have good data, 4 partial and 7 missing; 10 of the 14 still have no cycle length, and for those the bot answers that it does not know how long they take. Our field research is small: 8 survey answers from 7 people, and no farmer interview in Roraima yet.

Stack. Plain HTML and JavaScript, Web Speech API for listening and speaking in pt-BR, hosted on GitHub Pages. The engine exists in Python and JavaScript, and a conformance test checks 2,748 cases and requires identical answers from both.

Next steps. Load ZARC windows by municipality, water need per crop from Embrapa, SoilGrids for soil, NASA FIRMS for fire, and the same engine on WhatsApp, Telegram and SMS.
```

[O período da climatologia ficou como "long-term" de propósito: o `nasa-power.json` diz 2001 a 2025 para umidade do solo e "conforme a API" para o resto. Não cravar ano sem conferir.]

## 6. NASA Data

```
NASA POWER (Prediction Of Worldwide Energy Resources), Agroclimatology community, monthly, climatology and daily endpoints, MERRA-2 based, accessed 14 and 15 November 2026 for two points: Cantá, Roraima (2.61, -60.60) and Rio Verde, Goiás (-17.79, -50.92).

Used in the decision:
PRECTOTCORR (corrected precipitation): rain expected in the crop window, the year adjustment from the last three months, and dry spell length from daily data.
GWETROOT (root zone soil wetness): soil moisture against the monthly normal, used in "is the soil good?" answers.

Loaded for the same points and shown or planned, not yet used in the ranking: GWETTOP and GWETPROF (surface and profile soil wetness), T2M_MAX and T2M_MIN, RH2M, ALLSKY_SFC_SW_DWN, WS2M, CLOUD_AMT, soil temperature.

Note on units: all three endpoints return PRECTOTCORR in mm per day, and we convert to monthly totals by days in month.
```

[Conferir os nomes exatos de temperatura do solo e de radiação no script que puxou o POWER, que está fora do repositório. Se não der, cortar essa linha.]

## 7. Space Agency Partner & Other Data

```
No data from partner space agencies.

Other data:
FAO ECOCROP database (EcoCrop_DB.csv, copy at github.com/OpenCLIM/ecocrop), read on 15 November 2026. We found its rainfall fields are annual rainfall, not water per crop cycle, so we do not use them for water need.
Embrapa technical publications for crop cycle, critical phase and soil effects (cassava, cowpea, maize and others, listed in the repository).
ZARC agricultural climate risk zoning (Brazilian Ministry of Agriculture), cowpea ordinance for Roraima, 2023/24 season.
IBGE Agricultural Census 2017 for the share of establishments without technical assistance.
Our own survey of farmers in Roraima, 8 answers from 7 people, November 2026. Phone numbers are not published.

References for third party text and code: Web Speech API (browser built-in). Literature: Schöning et al., "Crop rotation and management tools for every farmer?", ScienceDirect. Full source list in docs/08 and in each document of the repository.
```

## 8. Use of Artificial Intelligence

```
We used Claude (Anthropic), an AI assistant, during the hackathon to write and review most of the code (the Python and JavaScript engines, the demo page and the conformance test), to research and check sources, to draft the documentation in the repository and to draft this submission text. A human (Welder Barroso) made the product decisions, checked the sources and reviewed the outputs.

The demo speaks with a synthetic voice. It uses the speech synthesis voices built into the user's browser through the Web Speech API (by default a Google Portuguese voice). This voice is computer generated, not a recording of a person. Speech recognition, when the microphone is used, also runs through the browser's Web Speech API.

No AI model runs inside the demo. Understanding what the user typed or said is keyword matching, and every number and every crop in an answer comes from the deterministic engine over named data. The answer sentences are fixed templates written in advance. Our architecture plans a second AI that would only rewrite the engine's facts into natural speech, with an automatic check that discards any output with a number or crop not present in the engine's answer; it is not implemented.

[Slides: declarar aqui se alguma imagem ou texto dos slides foi gerado por IA, e pôr marca d'água em imagem gerada.]

No NASA logos or NASA design elements are used in AI generated content.
```

## 9. Project Submission Verification

Duas caixas para marcar na página. A do guia de julgamento:

> "I have read and understand the project submission requirements as contained in the NASA Space Apps Project Submission Guide, and I agree to the Participant Terms and Conditions and Privacy Policy."

[A segunda caixa: ler o texto na própria página antes de marcar.]

---

## Antes de enviar

- [ ] Abrir os dois links em aba anônima: nada pode pedir login
- [ ] Confirmar que a frase sobre a tabela de culturas bate com o que está no `main` na hora do envio
- [ ] Se o defeito 4.1 do doc 14 (no branch `ecocrop-ciclo-15-11`) não for corrigido, a demo afirma que a chuva atende a mandioca sem ter dado de água: **ou corrigir, ou não mostrar o "e se" da mandioca no palco**

## Fontes deste documento

- Lista de campos: doc 09
- Caixa de verificação: Judging & Awards Guide, spaceappschallenge.org/resources/judging-awards-guide
- Números: README, docs 04, 10, 11, 12
