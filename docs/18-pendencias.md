# 18 — Pendências, consolidadas

> 15/11/2026, 14h40. Varredura de todos os documentos. Três chats estão
> trabalhando no mesmo repositório, e pendência espalhada em quinze documentos
> faz dois chats refazerem o mesmo trabalho. Esta é a lista única.
> **Se resolver algo daqui, risque aqui.**

## 1. Bloqueia a submissão

| o quê | de quem | estado |
| --- | --- | --- |
| Os nove campos em inglês, a declaração de uso de IA e as duas caixas | chat do dado | rascunho em `docs/15`, com colchetes a preencher |
| ~~Nome do projeto~~ | — | **RESOLVIDO 15/11, 14h50: fica AgroDeal**, decisão do Welder. Ver a ressalva abaixo |
| Confirmar a hora do prazo com o líder local | **Welder** | conte 22h59 até confirmar |
| Testar todos os links em aba anônima | **Welder** | nada pode pedir login |

### O nome: decidido, com uma ressalva que precisa ir para o slide

**Fica AgroDeal**, time e projeto. Zero retrabalho, e o nome já está no site do
Space Apps.

A ressalva é de posicionamento, não de marca. A busca de 15/11 não achou um
produto registrado com esse nome, mas achou que o espaço está cheio de nomes
quase iguais — Agrofy, Agroads, AgriAcordo, Agronegociar, AgriConnection,
Broto — **e todos são marketplaces**. "Deal" promete comércio, e comércio é
exatamente a única prioridade que a gente declara que **não** serve.

**Como neutralizar, e isso é obrigatório no slide 1:**

> **AgroDeal — What do I plant next?**

O subtítulo carrega o sentido que o nome não carrega: a ferramenta parte da
colheita e responde o próximo plantio. E no slide onde dizemos que não
otimizamos lucro, abrir com uma frase que assume a leitura, em vez de deixar o
júri achar contradição:

> *"The name says deal, but this tool does not sell anything. It helps the
> farmer choose what to optimize, and income is the one thing it says it cannot
> answer."*

## 2. Afeta a Validade, e um jurado pode perguntar

### 2.1 A lista de anos de El Niño está incompleta

A nossa série de análogos tem 1982, 1986, 1987, 1991, 1997, 2002, 2009, 2015,
2023 e 2026. Conferindo contra as tabelas públicas de ONI, **faltam pelo menos
1994, 2018 e 2019**. É cerca de um quarto da amostra.

A afirmação de que "a média dos anos de El Niño é de −10%" repousa nessa lista
e **não deve ir para slide**.

**O que sobrevive, e é mais forte:** nos anos de El Niño da nossa série o
desvio de chuva de junho a setembro vai de **−33% a +17%**, e vários vieram
acima da média. Isso derruba "ano de El Niño é ano seco" sem depender de a
lista estar completa, porque acrescentar anos só aumenta a dispersão.

**Recomendação:** usar a faixa, nunca a média. Está corrigido no `nasa-power.json`.

### 2.2 Limiares sem fonte anotada — ~~RESOLVIDO 15/11, 14h45~~

- ~~**Caupi** entre 18 °C e 34 °C~~ → Embrapa Meio-Norte, *Cultivo de
  Feijão-Caupi*, cap. Clima. **E achou um erro:** o ciclo estava em 60 dias sem
  fonte; a Embrapa dá 70 a 75 nas variedades recomendadas. O motor usa o mínimo
  do ciclo para somar a chuva da janela, então 60 fazia a cultura parecer mais
  segura do que é. Corrigido
- ~~**Soja** acima de 40 °C e 7 a 8 mm/dia~~ → Embrapa Soja, *SECA — Soja em
  Carência de Água*. A mesma fonte confirma 450 a 800 mm por ciclo e a faixa de
  20 a 30 °C. O limiar de 40 °C está em uso no aviso de calor
- **Limiar de veranico**: continua sem fonte. O motor reporta o número e não
  classifica, que é o comportamento honesto
- **Limiar de deriva de vento**: continua sem. A decisão de pulverizar está fora
  do MVP

### 2.3 Fonte fraca — ~~RESOLVIDO 15/11, 14h45~~

- ~~O ciclo do **milho** veio de jornal~~ → classificação oficial do MAPA via
  Embrapa Milho e Sorgo: Grupo I abaixo de 110 dias, Grupo II de 110 a 145,
  Grupo III acima de 145, contados da emergência à maturação fisiológica.
  Adotado o Grupo II. A qualidade do dado do milho subiu de *parcial* para *boa*

## 3. Deixa a resposta mais rasa, não trava nada

| o quê | efeito hoje | de quem |
| --- | --- | --- |
| `ciclo_dias` de 7 culturas | elas nunca viram indicação falada | chat do dado, pelo ECOCROP |
| `espera_no_campo` de **batata-doce** e **cará** | "comida em casa" não destaca as duas raízes que esperam na terra | chat do dado |
| `tmax_sofre_c` de 13 culturas | o aviso de calor só acende para a soja | chat do dado, o ECOCROP dá TMAX limpo |
| `agua_ciclo_mm` | **fechado como impossível**: ECOCROP e Embrapa dão chuva anual, não do ciclo | — |
| `cobertura_meses` | peso de solo que não existe na tabela | derivável do ciclo |

## 4. Declarado e aceito como próximo passo

Não são dívidas escondidas, estão ditas no produto e nos documentos.

- **Janela do ZARC**: o motor não lê `janelas_zarc` e `cabe_na_janela` está fixo
  em nulo nos dois motores. Carregar as janelas **não muda resposta nenhuma**
  sem mexer em código, e as janelas estão em texto, não em decêndio comparável
- **SoilGrids**: API REST pausada pelo ISRIC. A camada de solo hoje é a umidade
  da NASA em três profundidades mais a temperatura do solo
- **Lotes**: o motor modela uma área. Quem tem três roçados tem três respostas
- **IA redatora ao vivo**: precisa de chave, não roda em página pública
- **FIRMS, GDD, SMAP, ECOSTRESS, Landsat, API oficial do WhatsApp**

## 5. Pesquisa de campo

- **Zero entrevistas em Roraima.** Temos 8 respostas de formulário de 7 pessoas
  e uma entrevista em Goiás, feita pelo parceiro
- A pergunta que vale é a do medo de investir, e precisa ser feita em Roraima
- Risco de método registrado no `docs/03`: a entrevista de Goiás pode estar
  confirmando uma hipótese que o entrevistador já tinha

## 6. Numeração

**Correção, 14h50 (chat do dado):** o `docs/14` existiu. Era *ECOCROP: o que ele
dá, o que ele não dá*, no branch `ecocrop-ciclo-15-11` (commit `6191dd0`), com o
ciclo de melão, jerimum, batata-doce, arroz e cará já preenchido. O branch foi
apagado do remoto; a cópia existe só no clone local do chat do dado. O
`docs/05` ainda cita "(doc 14)". Decisão do Welder: restaurar no `main` ou
declarar descartado.

## 7. Inconsistências entre documentos, varredura de 14h50 (chat do dado)

Conferido contra o `main` em `2bbd12b`. Só o que não estava acima.

**Número que um jurado pode checar**

| achado | onde | o que fazer |
| --- | --- | --- |
| Dois "normais" de junho a setembro: o slide usa **859 mm** (`media_serie_mm`), a climatologia que o motor usa soma **812 mm**. Com 812, 2026 dá −59%, não −62% | slides `problem-data`, README, doc 15 contra `nasa-power.json` `clim` | dizer no slide de que período é o 859, ou usar um só |
| "Janeiro a outubro de 2026: 858 mm contra 1.428" não tem dado no repositório: a série de 2026 vai até **setembro** (outubro é nulo), e o próprio doc 04 diz na linha 131 que outubro a dezembro não estão na série | README, doc 04 linha 53 e tabela de outubro | tirar, ou gravar a leitura de outubro com data |
| "O pior em 45 anos" com rodapé "1981 a 2026": a base é de 45 anos, e com 2026 a série tem 46 | slides EN e PT | "o pior desde 1981" |
| Pesquisa: 5 de 8 plantam outra coisa em seguida, contagem conferida na planilha (`entregas/README.md`); ainda diz **6 de 8** | doc 11, `local-roraima.json` linha 70 | corrigir para 5 de 8 (4 de 7 pessoas). Doc 15 já corrigido |
| "14 culturas, 4 com dado bom": o arquivo tem **3** marcadas como boa | doc 12, tabela comparativa | 3 boa, 4 parcial, 7 falta |
| **Slide 4 desatualizado pelo `2bbd12b`:** a bolha diz "out of the ground in **60 days**"; a demo agora diz **70 dias** (caupi corrigido para 70 a 75 pela Embrapa). O jurado que repetir a conversa vê outro número | `slides-en/solution.html`, `slides-pt/solution.html`, `texto-de-estudo-do-pitch.md` linha 27; também docs 11 e 12 como exemplo | trocar 60 por 70 nos dois decks e no texto de estudo |
| Linha do milho no doc 05: o título diz "ciclo corrigido para 110–145", a coluna ainda diz **100 a 140** | `docs/05`, linha 102 | trocar a coluna |

**Promessa maior que a fonte**

| achado | onde | o que fazer |
| --- | --- | --- |
| "Fill crop traits from FAO ECOCROP" e "o gargalo não é código, é preencher a tabela": o ECOCROP dá **ciclo** (e nem para a melancia, que vem 0/0). Não dá água do ciclo, não dá tolerância à seca (campo vazio até na mandioca), não dá fixa N nem resíduo | slides `next` EN e PT, `texto-de-estudo-do-pitch.md` | "crop cycles from FAO ECOCROP; water need per crop from Embrapa or FAO 56" |
| `tmax_sofre_c` "o ECOCROP dá TMAX limpo": `TMAX` é a **máxima absoluta** de sobrevivência; a temperatura acima da qual a planta começa a sofrer é mais perto de `TOPMX`, a ótima máxima. É a quarta causa do doc 17 (semântica de campo externo) de novo | seção 3 acima | decidir qual dos dois é `tmax_sofre_c` antes de preencher, e escrever no `campos` do JSON |
| A pendência no fim do `culturas.json` ainda manda preencher **água** pelo ECOCROP | `dados/culturas.json`, `pendencias[0]` | trocar pela conclusão da seção 3: só ciclo |
| `agua_ciclo_mm` "fechado como impossível": é impossível **com ECOCROP e Embrapa**; o Kc do FAO 56 continua sendo caminho | seção 3 acima | "fechado para hoje" |

**Regra do doc 11 quebrada**

- O molde falado de `local-roraima.json` linha 244 diz "**veranico**". O doc 11
  decidiu "estiagem" na fala. O `invariantes.py` não cobre vocabulário, por isso
  passou.

**Documento velho que contradiz o novo**

- README, "O que está aberto" e "Próximos passos sugeridos para amanhã": ainda
  listam a regra de comparação como o buraco mais bloqueante, os slides como não
  escritos e o contrato com o Giuliano. E "site como hub (Giuliano)" contradiz o
  doc 09, "sem site". O mapa não tem o doc 15 nem `entregas/`.
- Doc 09, tabela de culturas por lugar: Roraima com 5 (o arquivo tem 11) e
  Centro-Oeste com **sorgo**, que não existe no `culturas.json`; o arquivo tem
  guandu e caupi.

## Como usar esta lista

Quem resolver um item: risca aqui, no mesmo commit da correção. Quem achar
pendência nova em qualquer documento: traz para cá em vez de deixar no lugar
onde achou.
