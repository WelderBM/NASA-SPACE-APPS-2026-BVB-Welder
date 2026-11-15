# 12 — Alinhamento depois do benchmark

> 15/11/2026, 11h45. Um chat paralelo fez o benchmark e derrubou duas das três
> pernas da proposta de valor. Eu verifiquei as três afirmações que passam a
> sustentar tudo, nas fontes primárias, antes de reescrever. **Este documento
> substitui a proposta de valor do doc 02 e a abertura do doc 07.**

## O que morreu, e por quê

### 1. O canal não é diferencial. Morreu.

O **RAImundo**, da Embrapa com MAPA, MDA e a startup AZap.AI, oferece orientação
técnica automatizada para agricultores familiares **diretamente pelo WhatsApp,
com linguagem simples**, e foi desenvolvido para funcionar até em áreas de baixa
conectividade. Cobre manejo, clima, pragas, solo, comercialização e políticas
públicas. A meta declarada é 100 mil agricultores em um ano.

Pior para a minha hipótese: eu já tinha o RAImundo catalogado como "precedente
de canal" desde ontem. Eu devia saber que não dava para chamar o canal de
diferencial, e chamei. Erro meu.

O canal entra como **"chega onde ele já está"**, nunca como o valor.

### 2. Veranico cruzado com fase crítica é o que o ZARC já faz. Morreu.

O **Zarc Plantio Certo** mostra as melhores datas de plantio de **43 culturas**,
por município, tipo de solo e ciclo, com taxas de risco de 20%, 30% e 40%. E o
monitoramento dele traz **cinco tipos de informação para as diferentes fases de
desenvolvimento da cultura: armazenamento de água no solo, precipitação
acumulada, número de dias sem chuvas, temperatura mínima e máxima**. Tem mais de
15 mil usuários ativos e consome a ClimAPI, ou seja, **tem previsão do tempo**.

Ou seja: dias sem chuva por fase da cultura é literalmente uma funcionalidade do
app oficial. Se eu disser no palco que ninguém faz isso, um agrônomo da banca
derruba na hora. E no nosso motor está pior: a fase crítica só está documentada
para a mandioca, o veranico é climatológico, e não temos limiar com fonte.

Consequência dura: **"eu não sei prever chuva" não é virtude, é lacuna nossa
diante do incumbente.** Continua sendo honestidade obrigatória, mas vai no slide
de validade, nunca na abertura.

### 3. Declarar confiança sobrevive, mas como prova, não como pitch.

Não achamos nenhuma ferramenta mostrando quanto da resposta foi medido. Mas a
coisa que o produtor mais quer saber antes de plantar é a chuva, então abrir com
"não sei prever chuva" soa como "não respondo sua pergunta número 1".

## O que é o valor, de verdade

A resposta estava num artigo revisado por pares, e é mais forte do que qualquer
uma das minhas três hipóteses.

O levantamento *Crop rotation and management tools for every farmer?*
(Schöning et al., ScienceDirect) comparou as ferramentas de rotação existentes e
concluiu duas coisas:

1. **"quase todas as ferramentas vão otimizar apenas o lucro da atividade
   agrícola"**, e só umas poucas consideram redução de fertilizante, água
   disponível ou outros objetivos no plano de rotação que entregam;
2. **"todas as ferramentas de rotação ignoraram propriedades com apenas algumas
   centenas de metros quadrados de área de cultivo"**.

E essa lacuna já é tratada como estabelecida por outros: um artigo do IJCAI 2023
cita exatamente esse achado para justificar o próprio trabalho.

Agora olhe o nosso `prioridades.json`. As prioridades que a ferramenta serve são
**a terra, o risco, comida em casa e pasto**. A única que ela **não** serve, e
declara que não serve, é **renda**.

Eu vinha tratando isso como o buraco embaraçoso do projeto. **É a posição.** A
literatura diz que todo mundo otimiza lucro; nós deixamos o produtor escolher o
que otimizar, e lucro é justamente o que não respondemos.

### A proposta de valor, reescrita

> As ferramentas de rotação que existem otimizam lucro, para propriedades
> grandes. Esta deixa o pequeno produtor escolher **o que** otimizar — a terra,
> o risco, a comida de casa, o pasto — responde a partir da **colheita que ele
> acabou de fazer**, e diz na cara o que não sabe. E chega por voz, no canal que
> ele já tem.

Três coisas sustentam isso, e cada uma tem prova nossa:

| afirmação | prova |
| --- | --- |
| Parte da colheita, não da cultura | o Plantio Certo pergunta "qual cultura?" e responde "quando plantar". O nosso pergunta "o que você colheu?" e responde "o que vem agora". É o `explore` do enunciado |
| A prioridade dele reordena a resposta | mesma colheita, mesmo lugar: em `risco` a razão é "é rápida, sai da terra em 60 dias"; em `solo` é "deixa a terra mais forte pro que vem depois" |
| O mesmo código serve outro lugar | mesmo milho, 500 mm exigidos: risco baixo em Cantá (621 mm ajustados), risco alto em Rio Verde (331 mm) |

E a honestidade entra como quarta, no slide de validade: a resposta carrega
**confiança medida** (quanto dos critérios deu para avaliar) e uma lista do que
não sabemos. Ninguém mais mostra isso.

## Onde nos posicionamos

Não competimos com o ZARC nem com o RAImundo. Complementamos, e vale dizer com
precisão:

| | Plantio Certo (ZARC) | RAImundo | este projeto |
| --- | --- | --- | --- |
| pergunta de entrada | qual cultura, quando plantar | qualquer coisa, texto livre | o que colhi, o que vem agora |
| quem escolhe o objetivo | ninguém: o objetivo é risco climático | o usuário, em linguagem livre | o produtor, entre 4 prioridades explícitas |
| otimiza lucro? | não é o foco | não declara | **declara que não sabe** |
| diz o que não sabe | não | não | **sim, com número** |
| previsão de chuva | sim, via ClimAPI | sim | **não** |
| cobertura de culturas | 43 | ampla | 14, 4 com dado bom |

As duas últimas linhas são desvantagens nossas e vão ditas.

## Correções factuais aplicadas

- **O 87%**: a fonte diz que, dos **16.850 estabelecimentos agropecuários** de
  Roraima (IBGE, Censo 2017), 87% não recebiam assistência técnica. Não é "87%
  dos agricultores familiares do estado", e é dado de 2017: o IATER foi criado
  em 2022 e expandiu desde então. Usar a frase com o ano.
- **HydroSCS**: não é ferramenta para produtor, é conjunto de dados de
  forçamento para previsão subsazonal a sazonal. O catálogo no Drive exagerava.
- **Prazo**: o repositório diz 22h59 e o sumário do Drive dizia 23h59. Até o
  líder local confirmar, **conta 22h59**. O Drive foi corrigido.
- **Respondentes**: 8 respostas, 7 pessoas. Já corrigido no doc 03.

## Achado novo que entrou no lugar

O IATER está organizando ação contra os efeitos do **El Niño 2026/2027 agora**,
orientando a agricultura familiar para o período de estiagem, e entre as
orientações está **"escolha de culturas mais adaptadas ao período seco"**.

Isso é literalmente o nosso produto, entregue hoje por extensionista humano. Não
é concorrência: é a prova de que a decisão existe, é oficial, é deste momento, e
alcança só quem o extensionista alcança.

## As seis perguntas do benchmark, respondidas

1. **A demo mostra resposta do motor até as 18h?** Sim, já está em pé. O motor
   roda dentro do navegador (`motor/cerne.js`), com teste de conformidade
   garantindo que responde igual ao Python. **Atualização 12h45:** a resposta
   deixou de ser consultada em tabela e passou a ser calculada. O GitHub Pages
   está no ar.
2. **Trocar a prioridade reordena na demo?** Sim, e é clicável em quatro chips.
   É a prova do `explore`, e é o GIF do slide.
3. **Dá para dizer "complementa o ZARC" com a janela vazia?** Dá para dizer que
   **foi feito para andar ao lado do ZARC**, e não que consome ZARC. Carregar as
   janelas é pesquisa por município, não cabe antes das 18h. Vai para próximos
   passos, declarado.
4. **Qual a frase pronta sobre chuva?** Já escrita, no registro local, e **não
   abre o pitch**: vai no slide de validade.
5. **Usar "AgroDeal"?** **Revertido em 14h50 pelo Welder: sim, fica.** A busca não achou produto registrado, e o time já está inscrito assim. O risco real é outro: o espaço está cheio de marketplaces com nomes parecidos, então o subtítulo "What do I plant next?" é obrigatório no slide 1.
6. **Prazo?** 22h59 até confirmação.

## Fontes verificadas nesta rodada

- Zarc Plantio Certo, monitoramento por fase da cultura e 43 culturas: Portal
  Embrapa, "Nova versão do aplicativo Zarc Plantio Certo…"; Embrapa Rede Zarc,
  "Como usar"; ficha do app na App Store e no Google Play
- RAImundo: Agrolink, "IA com sotaque do campo conecta pequenos produtores";
  Band Agro, 18/07/2025
- Lacuna de pequenas áreas e de objetivo não-lucro: Schöning et al., *Crop
  rotation and management tools for every farmer?*, ScienceDirect; citado em
  IJCAI 2023, "Supporting Sustainable Agroecological Initiatives for Small
  Farmers"
- El Niño 2026/27 e IATER: Diário RR, out/2026
