# 11 — Registro: como o bot fala

> Escrito em 15/11/2026, 11h30, depois do Welder apontar que as frases do bot
> estavam cheias de conceito formal. Ele estava certo, e o lugar do erro era o
> pior possível: a frase falada.

## O erro

A decisão de linguagem do doc 02 mandou tirar o jargão. Na implementação ele
voltou sozinho, porque eu escrevi os moldes de frase pensando no dado e não em
quem ouve. O bot dizia:

- "Fixa nitrogênio, que é o que melhora a terra"
- "O ciclo é curto, 60 dias, então fica menos tempo exposto"
- "é de outra família que a Euphorbiaceae"
- "o que mais encaixa é" — termo que eu inventei, que ninguém fala
- "a janela dá 621 milímetros"
- "veja o boletim do INMET"

## A armadilha que ia quebrar a demo

**No Norte, "inverno" é a estação chuvosa e "verão" é a seca.** É o chamado
inverno amazônico: enquanto o resto do Brasil tem o calor do verão, a região
Norte tem chuva intensa e frequente. É o oposto do calendário do Sul e do
Centro-Oeste.

Num bot de voz isso não é detalhe de estilo, é inversão de sentido: se o bot
falar "a chuva do verão" para um produtor de Cantá, ele entende a seca.
**Decisão: o bot nunca diz "inverno" nem "verão".** Diz "o tempo da chuva" e
"o tempo da seca".

## As palavras vieram dos seus respondentes

O formulário teve **8 respostas, 7 pessoas** (duas são da mesma pessoa, mesmo
telefone, 2 minutos de diferença). Municípios: Caracaraí 3, Boa Vista 3,
Rorainópolis 1, Cantá 1. As palavras que eles escreveram, sem opção pronta,
são a melhor fonte de registro que existe para esta persona:

| o que eles escreveram | o que isso resolve |
| --- | --- |
| **"terra fraca"** (2 de 8, como causa de perda) | é a palavra deles para saúde do solo. O desafio pede *strengthen soil health*: em roraimense, é **deixar a terra mais forte** |
| **"estiagem"** | está no vocabulário deles. Melhor que "veranico" na fala |
| **"fica parada até a próxima chuva"** | é pousio, nas palavras deles |
| **"planta outra coisa em seguida"** (5 de 8 respostas, 4 de 7 pessoas) | é sucessão, nas palavras deles. E confirma que a decisão que a gente escolheu é a que eles realmente tomam |
| **"ambiente de lavrado"** | o produtor do Cantá pediu "cultivares adaptadas ao ambiente de lavrado". Lavrado é o ecossistema, e é a palavra local |
| **"se a planta irá sobreviver e produzir"** | é a pergunta real, não "qual a melhor rotação" |
| **"formigas caminhando em processo rápido de coleta de alimento"** | sinal de chuva por conhecimento tradicional. Não é folclore: é a interface que já existe |

Outros números do formulário que valem registro: 7 de 8 decidem **pela
experiência de quem planta**; 4 de 8 querem **mensagem escrita no WhatsApp** e
1 pediu **"um aparelho que fala, lá na propriedade"**; e **3 de 8 só confiariam
em recomendação de satélite se um técnico confirmasse** — que é exatamente por
que o contrato tem o campo `validar_com_tecnico`.

## A troca, palavra por palavra

| era | virou |
| --- | --- |
| fixa nitrogênio | deixa a terra mais forte pro que vem depois |
| o ciclo é curto, 60 dias | é rápida, sai da terra em 60 dias |
| de outra família que a Euphorbiaceae | não é parente da mandioca |
| quebra o ciclo das pragas do solo | a praga que ficou na terra não pega nela |
| o que mais encaixa é | eu iria de |
| a janela dá 621 milímetros | a chuva desse tempo dá o que ela precisa |
| risco de água alto | pode faltar água pra ela |
| veranico de 24 dias | estiagem de 24 dias |
| veja o boletim do INMET | olha a previsão do tempo |
| quer saber o risco? | quer saber o que pode dar errado? |

**"Não é parente"** é o achado melhor da lista: família botânica é literalmente
parentesco, então a palavra do produtor é mais exata que o termo técnico, e não
perde nada.

## A decisão de arquitetura: registro é camada local

Se eu cravar "lavrado" e "terra fraca" no motor, ele deixa de servir Rio Verde,
e aí morre a prova de que o cerne é genérico. Então cada configuração local
carrega seu próprio `vocabulario` e seus próprios `moldes` de frase, e o motor
só preenche. Trocar de lugar troca a língua junto com o dado.

Rio Verde não tem vocabulário levantado, porque não temos respondente de lá.
O motor cai em português neutro e **declara isso na resposta**, no campo
`registro`. É limite honesto, não falha escondida.

Também entrou um campo `artigo` em cada cultura: sem ele o bot falava
"da feijão-caupi" e "do mandioca". A voz lê esse campo em voz alta.

## Regras de fala, fixadas

1. Frase curta, uma ideia, no máximo 35 palavras.
2. Nenhum termo técnico. Se não dá para dizer sem o termo, a frase está errada.
3. Nunca "inverno" nem "verão".
4. Número só quando ele pedir. O qualitativo vem primeiro, e é relativo ao
   próprio lugar: 146 mm é chuva mediana no Cantá e chuva alta em Rio Verde.
5. Termina oferecendo o próximo passo, para o turno continuar vivo.
6. O que o bot não sabe, ele diz, e aponta para onde tem.

## Pendências

- **"tu" ou "você"**: Roraima fala "tu" com verbo na terceira pessoa ("tu quer").
  Os moldes estão com "você", que é mais seguro mas menos de casa. **Decisão do
  Welder**, e é troca de uma linha no JSON.
- Há um catálogo acadêmico de **564 expressões orais dos habitantes do lavrado
  roraimense**, e o **Dicioraima**, dicionário do português de Roraima da UFRR.
  Nenhum dos dois foi lido: são a fonte para expandir o vocabulário depois.
- A Embrapa tem um manual de produção do **Prosa Rural** com dicas de adequação
  de linguagem para rádio. Nosso bot é rádio sob medida; vale ler.

## Fontes

- Inverno amazônico: Revista Oeste, "Inverno amazônico: Região Norte tem clima
  diferente do restante do país", com explicação da meteorologista Andrea Ramos
- Acessibilidade textual em material de extensão rural, base bakhtiniana:
  Revista Diálogo das Letras / periódicos UFMT
- Expressões orais do lavrado roraimense (564 catalogadas): Revista Geográfica
  Acadêmica, v.10 n.1, 2016
- Dicioraima e projeto Retratos Linguísticos de Roraima: Revista Philologus,
  ano 27, n.81, 2021 (UFRR)
- Prosa Rural, manual de produção e edição: Embrapa Infoteca
- Vocabulário dos produtores: formulário próprio, 8 respostas, 14/11/2026
