# Formulário de submissão do Space Apps: texto final

> Versão final de 15/11/2026, 22h (Boa Vista). Substitui o rascunho das 16h40.
> Mudou: o risco de água da NASA reordena no objetivo "arriscar pouco"; o painel
> Compare; a pergunta de renda; as frases sobre praga; MERRA-2; satélite × solo;
> Use of AI com os dois membros, os commits e o logo; referências novas.
>
> **Prazo: 23h59 de Boa Vista.** Vale o último clique em "Submit for Judging".
> "Save Progress" **não** deixa a página pública: o rascunho só aparece para o time.

## Project Name

```
AgroDeal: What do I plant next?
```

## Summary

```
AgroDeal, What do I plant next?, is a conversation for small farmers in Roraima, in the Brazilian Amazon, who must decide what to plant right after a harvest. In 2026 that decision got harder: NASA POWER shows 330 mm of June to September rain in Cantá, Roraima, against a 1981 to 2026 mean of 859 mm, the lowest since 1981. And 87% of Roraima's 16,850 farm establishments had no technical assistance, according to 2017 IBGE data cited by the state extension agency, IATER.

The farmer says, by voice or text, what was just harvested, then picks what matters: better soil, low risk, food at home or pasture. The answer reorders, with the reason, and a side-by-side view compares the top options with planting the same crop again. Every option carries three separate numbers: risk, from NASA POWER rain and root-zone soil moisture adjusted to this year; fit, from crop traits weighed by the farmer's goal; and confidence, the share of criteria we could actually measure. What it cannot measure, like prices or labor, it says.

Most crop rotation tools optimize profit for large farms. This one lets the small farmer choose what to optimize, and it works beside Brazil's official planting zoning, not instead of it.
```

## Project Demonstration

```
https://drive.google.com/file/d/1mXxqji7_W0kXJdyb5uGGjR-FCtwWLdYl/view?usp=drivesdk
```

Antes, suba `entregas\pdf\AgroDeal-pitch-7-slides-EN.pdf` (o novo, com AgroDeal e os dois nomes no slide 1 e links clicáveis no slide 7) como **nova versão** desse mesmo arquivo: no Drive, clique com o botão direito → *Gerenciar versões* (ou *Arquivo → Substituir*) → enviar. O link continua o mesmo.

## Project

```
https://welderbm.github.io/NASA-SPACE-APPS-2026-BVB-Welder/
```

## Project Details

```
The problem
In 2026 the El Niño hit Roraima, in the Brazilian Amazon. At our reference point in Cantá (lat 2.61, lon -60.60), NASA POWER shows 330 mm of rain from June to September 2026, against a 1981 to 2026 mean of 859 mm: minus 62%, the lowest since 1981. The longest dry spell inside the rainy season was 24 days, against 9. In September, root-zone soil moisture was 0.51, against a 2001 to 2025 normal of 0.79, a level that place usually reaches only in January. We do not claim 2027 will repeat it: in earlier El Niño years, that same rain ranged from 48% below to 17% above the mean.

The people
87% of Roraima's 16,850 farm establishments had no technical assistance (IBGE data for 2017, cited by the state extension agency IATER in 2024). This season, under a state emergency over the drought, IATER is guiding family farmers to choose crops better adapted to the dry period, but it reaches only as far as an agent can drive. In our survey (8 answers from 7 people in Roraima), 4 of 7 said they plant something else right after a harvest, and drought was the most cited loss. That is the decision we support: the next crop of the rotation, starting from what was just harvested.

What it does
The farmer says, by voice or text, what was just harvested, and picks what matters most: better soil, low risk, food at home or pasture. The answer reorders, with the reason. Example, Cantá, July, after cassava: choose low risk and it suggests cowpea, "out of the ground in 70 days". Choose better soil: same crop, new reason, "it leaves the soil stronger". Ask about selling or labor: it says it has no price, buyer or labor data, and asks which goal it can measure.
A Compare panel shows the top three options side by side with the existing practice, planting the same crop again: goal fit, share of data measured, NASA water risk, cycle length and what is unknown. For each option it also shows a three-crop rotation sequence: the engine runs again in the month the previous crop leaves the ground, with that month's NASA data and the same goal. The same crop again is never offered, and the panel says why. It compares, never gives orders, and lists what to check with an extension agent.

How it works
A deterministic engine takes the harvest, the priority, the place and the month, and returns three numbers that are never mixed into one score.
Risk uses NASA data: the rain the crop's growing window normally gets (NASA POWER climatology), scaled by how the last three months compared to normal, a persistence heuristic and not a forecast, against the crop's water need; the typical longest dry spell in the window; and root-zone soil moisture against the monthly normal.
Fit uses crop traits only: nitrogen fixation, residue, drought tolerance, cycle length, whether it can wait in the field, whether it is forage, and the official ZARC planting window. Each priority weighs them differently. With the official cowpea window for Roraima loaded, the low-risk fit of cowpea goes from 53% in April to 87% in July.
Confidence is the share of the priority's criteria we could measure for that crop. A crop with too little data cannot take the top spot.
The NASA water risk changes the ranking when the farmer wants to take little risk: options whose water risk is high, or whose water need we cannot check, go below the others. In a dry month when every option is in that situation, the bot says so first when asked "what could go wrong?". Under the other goals the water risk is shown beside each option and spoken on request.
Rule: never follow a crop with one from the same botanical family, because a different family is less likely to carry the same soil pests and diseases. It is a simplification, and the extension agent knows the exceptions.

Satellite, model and ground
NASA POWER values are gridded estimates (about 50 km) from the MERRA-2 reanalysis, which assimilates satellite and ground observations. They are not measurements on the farm. The farmer's own eye on the soil and the extension agent stay the ground truth; the tool gives them the regional picture.

Same code, different place
Same maize, same code. Planting in April in Cantá: 686 mm of adjusted rain against 500 mm needed, low risk. Planting in September in Rio Verde, Goiás: 386 mm, high risk. Nothing is hard coded per place: data comes by coordinate, and each place carries its own crop list, planting windows and wording.

How it talks
Words come from farmers in Roraima: "terra fraca" for weak soil, "estiagem" for dry spell, "macaxeira" for cassava, "feijão de corda" for cowpea. It never says winter or summer, because in the Amazon "winter" means the rainy season. The chat speaks Brazilian Portuguese, the farmer's language; the side panels are in English for judges.

What it does not do
No WhatsApp connection yet: in our survey, 4 of 8 answers named a written WhatsApp message as how they want to be reached, so WhatsApp is the target channel. The demo renders the same conversation in a page, which keeps the engine open to inspection. No rain forecast: Brazil's official ZARC Plantio Certo app has one, and we were built to sit next to it. No prices or labor data, and it says so. Of the 14 crops, 4 have good data, 8 partial and 2 missing, and 5 still have no cycle length; for those, the bot says it does not know. Our field research is small: 8 survey answers and one farmer interview, in Goiás, by Giuliano.

Honesty is tested
3,156 automated cases, across all six goals, check that every answer has a source and that no known gap is left unsaid. The engine exists in Python and JavaScript, and a conformance test requires both to answer the same in all cases.

Tools
Plain HTML and JavaScript, the engine running in the browser with no server; the Web Speech API for listening and speaking in pt-BR; GitHub Pages; Python for the reference engine and the tests. NASA POWER data is stored as JSON in the repository. Code and data (Apache-2.0): https://github.com/WelderBM/NASA-SPACE-APPS-2026-BVB-Welder

Next steps
A water-risk weight for every goal, not only low risk; optimizing whole sequences instead of chaining one-step choices; soil texture from the farmer or SoilGrids; the remaining official ZARC windows; WhatsApp adapter on the same engine; a field test with Roraima farmers and IATER extension agents.

Use of AI
Team AgroDeal, Welder Barroso and Giuliano França, made the product decisions, ran the survey and the interview, checked the sources and reviewed every output. We used Claude (Anthropic), an AI assistant, to write and review most of the code, research and check sources, and draft the documentation, slides text and this submission; most commits in the repository are authored by Claude for that reason. The project logo was generated with an AI image tool and is marked "AI-generated image". No AI model runs inside the demo: understanding the farmer is keyword matching, every number comes from the deterministic engine over named data, and the sentences are fixed templates. The demo's voice is the browser's synthetic speech. No NASA logos or design elements are used.
```

## Imagem do projeto

Troque o logo atual pela versão com marca d'água visível. O logo atual é gerado por IA (tem metadado C2PA do Google com SynthID) e não tem marca: a versão com marca d'água visível "AI-generated image".

## Use of Super Intelligence (só coleta de dados; a banca não vê)

Marcar: código, texto, **imagem**, áudio/voz. Vídeo só se ele continuar citado em algum lugar.

## NASA Data

| Link Text | Link Url |
| --- | --- |
| NASA POWER (Prediction Of Worldwide Energy Resources), Agroclimatology | https://power.larc.nasa.gov/ |
| NASA POWER API, monthly point data (PRECTOTCORR, GWETROOT, GWETTOP, GWETPROF) | https://power.larc.nasa.gov/api/temporal/monthly/point |
| NASA POWER API, daily point data (dry spell length) | https://power.larc.nasa.gov/api/temporal/daily/point |
| NASA POWER API, climatology point data | https://power.larc.nasa.gov/api/temporal/climatology/point |
| MERRA-2 reanalysis (NASA GMAO), the source behind POWER rain and soil moisture | https://gmao.gsfc.nasa.gov/reanalysis/MERRA-2/ |

## Space Agency Partner & Other Data

As linhas antigas continuam. **Acrescentar:**

| Link Text | Link Url |
| --- | --- |
| IBGE Agricultural Census 2017 | https://censoagro2017.ibge.gov.br/ |
| ZARC Plantio Certo app (MAPA and Embrapa), official planting-risk tool we sit next to | https://apps.apple.com/br/app/plantio-certo/id1518252333 |
| RAImundo, Embrapa WhatsApp assistant (precedent for the channel) | https://lexlegal.com.br/?p=28389 |
| Project license: Apache-2.0 | https://github.com/WelderBM/NASA-SPACE-APPS-2026-BVB-Welder/blob/main/LICENSE |

## Descrição do time (página do time; hoje diz "Looking for... teammates!")

```
Team AgroDeal: Welder Barroso and Giuliano França, from Boa Vista, Roraima, Brazil. We built AgroDeal (What do I plant next?) for the Field Shift challenge: a voice and text conversation that helps small farmers in Roraima decide what to plant right after a harvest, using NASA POWER rain and soil moisture, crop traits from Embrapa and FAO ECOCROP, the official ZARC planting windows, and the goal the farmer picks. It never hides what it cannot measure.
```

## Verificação final (aba anônima)

- [ ] Link do Drive abre o PDF **sem login** e o slide 1 mostra "Team AgroDeal: Welder Barroso and Giuliano França"
- [ ] O Pages abre a demo. Tocar *mandioca* e depois *arriscar pouco* mostra o painel **Compare** (aperte Ctrl+F5 se aparecer a versão antiga)
- [ ] Aba Members: Welder e Giuliano
- [ ] As duas caixas de verificação marcadas
- [ ] **Submit for Judging** clicado, e a página mostra o projeto como enviado
