# Vídeo-pitch de 30 s (história da Rosa)

> 15/11/2026, 14h45 (Boa Vista). Substitui a `entregas/animacao/`, que era um slide animado.

`field-shift-roraima-pitch-30s.mp4`: 29,9 s, 1920×1080, 30 fps, narração em inglês, legenda em inglês gravada na imagem e também em `field-shift-roraima-pitch-30s.en.srt` (para subir junto no YouTube).

## A história

| Tempo | Cena | Narração |
| --- | --- | --- |
| 0 a 7 s | Lavrado seco, buritis, Rosa com o cesto de mandioca. Etiqueta "−62% rain, Jun–Sep 2026, lowest since 1981, NASA POWER" | Cantá, Brazilian Amazon. Rosa just pulled up her cassava… after the weakest rains since 1981. |
| 7 a 10 s | Close, balão de pensamento com "?" | Now, one question. What do I plant next? |
| 10 a 16 s | Ela fala com o celular; satélite chega e mira a terra; cartões "Rain" e "Soil moisture" | She asks. Our assistant reads NASA satellite data for her land. Rain, and soil. |
| 16 a 21 s | Celular com as 4 prioridades; ela toca "Better soil"; resposta "Cowpea"; o chão escurece e brota | She picks what matters. Better soil? Cowpea. It leaves the ground stronger. |
| 21 a 27 s | Tela dividida: trator e cifrão contra a roça pequena com as 4 prioridades; balão "This, I don't know." | Most tools chase profit, for big farms. Ours lets small farmers choose… and says what it doesn't know. |
| 27 a 30 s | Cartão final | What to plant next. For every small farm. |

## De onde vem cada afirmação

- −62% de chuva de junho a setembro de 2026 no Cantá, pior em 45 anos: NASA POWER, `dados/nasa-power.json`, doc 10.
- Mandioca seguida de feijão-caupi com a prioridade "a terra melhorar", motivo "deixa a terra mais forte": saída do `motor/cerne.js` para Cantá, plantio em abril (conferido em 15/11, 14h).
- "Most tools chase profit, for big farms": Schöning et al. (2023), doc 12.
- "Says what it doesn't know": campos `nao_sei` e `limites` do motor; a recusa de prever chuva.
- Rosa é personagem ilustrativa, não uma produtora real.

## Regras do guia de submissão atendidas

- Até 30 s, legenda em inglês.
- Marca d'água visível de IA no canto superior direito: "AI-generated: animation by Claude · voice by Kokoro TTS". O metadado do arquivo também declara animação, voz e música geradas.
- Nenhum logo ou elemento de marca da NASA.
- O campo Project Demo leva **ou** este vídeo **ou** os 7 slides, nunca os dois.

## Como foi feito (pasta `fonte/`)

- Voz: Kokoro TTS (modelo aberto, voz `af_heart`), uma frase por vez, com pausas de respiro entre elas (`tts2.py`, `script.json`, tempos em `timing_af_heart.json`).
- Imagem: cena em SVG animada por JavaScript (`scene.html`), filmada quadro a quadro no Chrome sem tela e codificada com ffmpeg (`render.py`).
- Música: acordes e arpejo sintetizados em código (`music.py`), abaixados quando a voz fala.
