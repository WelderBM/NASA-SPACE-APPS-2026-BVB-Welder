# Formulário de submissão do Space Apps, preenchido

> 15/11/2026, 16h40 (Boa Vista), fontes reconferidas às 16h30. Feito a partir da página do projeto salva pelo
> Welder (campos e textos de ajuda) e do main em e10d2a2. Rascunho, não definitivo:
> o chat principal continua mexendo no produto. Substitui os textos do docs/15
> onde os números mudaram (milho 686/386, culturas 4/8/2, 5 sem ciclo, janela do
> ZARC do caupi carregada, renda pedível na demo).
>
> **Prazo pelo formulário: 23h59 no fuso do evento local (Boa Vista)**, não 22h59.
> O que vale é o último clique em "Submit for Judging". "Save Progress" já deixa
> a página pública, mas não envia.

## Project Name

```
AgroDeal: What do I plant next?
```

## Summary (limite 1500; este tem 1127 caracteres, 191 palavras)

```
AgroDeal, What do I plant next?, is a conversation for small farmers in Roraima, in the Brazilian Amazon, who must decide what to plant right after a harvest. In 2026 that decision got harder: NASA POWER shows 330 mm of June to September rain in Cantá, Roraima, against a 1981 to 2026 mean of 859 mm, the lowest since 1981. And 87% of Roraima's 16,850 farm establishments had no technical assistance, according to 2017 IBGE data cited by the state extension agency, IATER.

The farmer says, by voice or text, what was just harvested, then picks what matters: better soil, low risk, food at home, pasture or income. The answer reorders, with the reason. Every option carries three separate numbers: risk, from NASA POWER rain and root-zone soil moisture adjusted to this year; fit, from crop traits weighed by the farmer's goal; and confidence, the share of criteria we could actually measure. What it cannot measure, like income, it says.

Most crop rotation tools optimize profit for large farms. This one lets the small farmer choose what to optimize, and it works beside Brazil's official planting zoning, not instead of it.
```

## Project Demonstration

```
https://drive.google.com/file/d/1mXxqji7_W0kXJdyb5uGGjR-FCtwWLdYl/view?usp=drivesdk
```

## Project

```
https://welderbm.github.io/NASA-SPACE-APPS-2026-BVB-Welder/
```

## Project Details (6023 caracteres)

```
The problem
In 2026 the El Niño hit Roraima, in the Brazilian Amazon. At our reference point in Cantá (lat 2.61, lon -60.60), NASA POWER shows 330 mm of rain from June to September 2026, against a 1981 to 2026 mean of 859 mm: minus 62%, the lowest since 1981. The longest dry spell inside the rainy season was 24 days, against 9. In September, root-zone soil moisture was 0.51, against a normal of 0.76, a level that place usually reaches only in January. We do not claim 2027 will repeat it: in earlier El Niño years, that same rain ranged from 48% below to 17% above the mean.

The people
87% of Roraima's 16,850 farm establishments had no technical assistance (IBGE data for 2017, cited by the state extension agency IATER in 2024). This season, under a state emergency over the El Niño drought, IATER is guiding family farmers to choose crops better adapted to the dry period, but it reaches only as far as an agent can drive. In our survey (8 answers from 7 people in Roraima), 4 of 7 said they plant something else right after a harvest, and drought was the most cited loss. That is the decision we support: one crop cycle ahead, starting from what was just harvested.

What it does
The farmer says, by voice or text, what was just harvested, and picks what matters most: better soil, low risk, food at home, pasture or income. The answer reorders, with the reason. Example, Cantá, July, after cassava: choose low risk and it suggests cowpea, "out of the ground in 70 days". Choose better soil: same crop, new reason, "it leaves the soil stronger". Choose income: it says it cannot measure that. It compares options, never gives orders, and ends with what to check with a technician.

How it works
A deterministic engine takes the harvest, the priority, the place and the month, and returns three numbers that are never mixed into one score.
Risk uses NASA data: rain expected in the crop's growing window (NASA POWER climatology, adjusted by how the last three months compared to normal) against the crop's water need, the typical longest dry spell in the window, and root-zone soil moisture against the monthly normal.
Fit uses crop traits only: nitrogen fixation, residue, drought tolerance, cycle length, whether it can wait in the field, whether it is forage, and the official ZARC planting window. Each priority weighs them differently. With the official cowpea window for Roraima loaded, the low-risk fit of cowpea goes from 53% in April to 87% in July.
Confidence is the share of the priority's criteria we could actually measure for that crop. A crop with too little data cannot take the top spot.
Hard rule: never follow a crop with one from the same botanical family. The bot says it in plain words: "it is not related to cassava, so the pest left in the soil will not take it".

Same code, different place
Same maize, same code. Planting in April in Cantá: 686 mm of adjusted rain against 500 mm needed, low risk. Planting in September in Rio Verde, Goiás: 386 mm, high risk. Nothing is hard coded per place: data comes by coordinate, and each place carries its own crop list, planting windows and wording.

How it talks
Words come from farmers in Roraima: "terra fraca" for weak soil, "estiagem" for dry spell. It never says winter or summer, because in the Amazon "winter" means the rainy season and the meaning would flip. The demo speaks Brazilian Portuguese on purpose, because that is the farmer's language; a line in English at the top tells judges which buttons to tap.

What it does not do
No WhatsApp connection, and that is a decision, not a gap. In our survey, 4 of 8 answers named a written WhatsApp message as how they want to be reached, so WhatsApp is the channel this is built for. The demo renders that same conversation in a page rather than calling the Meta API, which keeps the engine open to inspection and the idea channel independent: the engine returns a structure, and any channel can carry it. The page says this at the top.

No rain forecast: Brazil's official ZARC Plantio Certo app has one, and we were built to sit next to it. No prices, no labor questions, and it says so. Of the 14 crops in the table, 4 have good data, 8 partial and 2 missing, and 5 still have no cycle length; for those, the bot says it does not know how long they take. Our field research is small: 8 survey answers, and one farmer interview, in Goiás, conducted by Giuliano, the other half of this two-person team. Three calls to Roraima farmers are scripted and not yet made.

Honesty is tested
Every answer is checked by an automated test suite: 2,748 cases, and a gap left unsaid fails the build. The engine exists in Python and JavaScript, and a conformance test requires both to answer the same in all 2,748 cases.

Tools
Plain HTML and JavaScript, the engine running in the browser with no server, the Web Speech API for listening and speaking in pt-BR, GitHub Pages for hosting, Python for data collection and tests. Code and data: https://github.com/WelderBM/NASA-SPACE-APPS-2026-BVB-Welder

Next steps
Load the remaining official ZARC planting windows, municipality by municipality. Crop water need from Embrapa or FAO 56, soil texture from SoilGrids. Connect the WhatsApp Business API, then a Telegram adapter, to the same engine, which needs no change to serve either. A field test with Roraima farmers and IATER extension agents.

Use of AI
We used Claude (Anthropic), an AI assistant, to write and review most of the code, research and check sources, draft the documentation, the slides text and this submission. A human, Welder Barroso, made the product decisions, checked the sources and reviewed the outputs. No AI model runs inside the demo: understanding what the user says is keyword matching, every number comes from the deterministic engine over named data, and answer sentences are fixed templates. The demo's voice is the browser's synthetic speech (Web Speech API). The supporting pitch videos were animated with code written by Claude and narrated with Kokoro TTS, an AI voice; both carry a visible AI-generated watermark and say so in their metadata. No NASA logos or design elements are used.
```

## Use of Super Intelligence (só coleta de dados, a banca não vê)

Marcar o que existir na lista: código, texto, vídeo/animação, áudio/voz.
Não marcar imagem gerada (não há) nem "I did not use SI".

## NASA Data

| Link Text | Link Url |
| --- | --- |
| NASA POWER (Prediction Of Worldwide Energy Resources), Agroclimatology | https://power.larc.nasa.gov/ |
| NASA POWER API, monthly point data (PRECTOTCORR, GWETROOT, GWETTOP, GWETPROF) | https://power.larc.nasa.gov/api/temporal/monthly/point |
| NASA POWER API, daily point data (dry spell length) | https://power.larc.nasa.gov/api/temporal/daily/point |
| NASA POWER API, climatology point data | https://power.larc.nasa.gov/api/temporal/climatology/point |

## Space Agency Partner & Other Data

| Link Text | Link Url |
| --- | --- |
| Project code and data (GitHub) | https://github.com/WelderBM/NASA-SPACE-APPS-2026-BVB-Welder |
| FAO ECOCROP database, copy by OpenCLIM (crop cycle) | https://github.com/OpenCLIM/ecocrop |
| ZARC agricultural climate risk zoning, cowpea ordinance for Roraima (MAPA) | https://www.gov.br/agricultura/pt-br/assuntos/riscos-seguro/programa-nacional-de-zoneamento-agricola-de-risco-climatico/portarias/safra-vigente/roraima/PORTN291FEIJOCAUPIRR.pdf |
| IATER Roraima, extension agreement proposal, March 2024 (16,850 establishments, 87% without technical assistance, IBGE 2017 data) | https://prda.sudam.gov.br/pdf/80bff30c20fcfd50e68aaebbd52cdf26.pdf |
| Folha BV, Sep 8 2026: IATER guidance for the El Niño dry period, including choosing crops adapted to it | https://www.folhabv.com.br/?p=667353 |
| Schöning et al. (2023), crop rotation and management tools review | https://doaj.org/article/ac7cad55d97344d0826ef322e929cc11 |
| Embrapa Roraima, production systems for Roraima | https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/68108/1/RoraimaSistemasProducao-19728.pdf |
| Kokoro TTS, AI voice used in the pitch videos | https://github.com/hexgrad/kokoro |
| Space Grotesk font (slides) | https://fonts.google.com/specimen/Space+Grotesk |
| Inter font (slides) | https://fonts.google.com/specimen/Inter |

## Verificação

As duas caixas: Terms and Conditions e Original Work. A segunda diz que todo
recurso externo está listado nos dois campos de dados, por isso fontes e voz
entraram na tabela acima.

## Descrição do time (melhorada)

```
AgroDeal (What do I plant next?) is a voice and text conversation for the Field Shift challenge. It helps small farmers in Roraima, in the Brazilian Amazon, decide what to plant right after a harvest. It uses NASA POWER rain and soil moisture, crop traits from Embrapa and FAO ECOCROP, the official ZARC planting windows, and the goal the farmer picks: better soil, low risk, food at home, pasture or income. It never hides what it cannot measure. Built by a full-stack developer (JavaScript, React, Python), with a live demo in the browser and an engine tested on 2,748 cases.
```
