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
desvio de chuva de junho a setembro vai de **−48% a +17%** (sem contar 2026), e vários vieram
acima da média. Isso derruba "ano de El Niño é ano seco" sem depender de a
lista estar completa, porque acrescentar anos só aumenta a dispersão.

**Recomendação:** usar a faixa, nunca a média. Está corrigido no `nasa-power.json`.

> **Correção, 15/11, 15h30 (chat do pitch):** esta seção dizia "−33% a +17%".
> A própria lista em `nasa-power.json` (`anos_desenvolvimento`) tem **2015 com
> −48%**, então a faixa é −48% a +17%. O campo `o_que_sobrevive` do
> `nasa-power.json` ainda diz −33% e precisa da mesma troca (dono: chat do
> dado). Vídeo de 3 min, slides e texto de estudo já usam −48%.
>
> **FEITO 15/11, 15h45 (chat do motor):** conferido na própria lista antes de
> aceitar — `anos_desenvolvimento` traz 2015 com −48%, e o −33% era o 1982, não
> o mínimo. Trocado no `nasa-power.json`, no README e no `docs/04`, que é onde
> o número nasceu. Com 2026 na conta a faixa vai a −62%, então **a frase tem
> que dizer se 2026 entra ou não.**

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
| ~~`ciclo_dias` de 7 culturas~~ | **5 FEITAS 15/11, 15h** (PR #1, merge): melão, jerimum, batata-doce, cará e arroz, pelo ECOCROP, com espécie e EcoPort. Faltam **melancia** (o ECOCROP não tem) e **banana** (perene de propósito, fora de `ciclo_dias`). Ver [14](14-ecocrop-ciclo.md) | — |
| A confiança mede **cobertura**, não **qualidade de fonte** | com o ciclo preenchido, as 5 culturas foram a 100% ao lado do caupi, cujo dado é melhor. `qualidade_do_dado` já vai na resposta e a fala não diz | desenho, fica com o Welder |
| ~~`espera_no_campo` de batata-doce e cará~~ | **FEITO 15/11 14h50**, marcado como derivado (raciocínio sobre raiz de reserva), não como fonte. Precisa de validação com técnico | — |
| `tmax_sofre_c` de 13 culturas | o aviso de calor só acende para a soja | chat do dado, o ECOCROP dá TMAX limpo |
| `agua_ciclo_mm` | **fechado como impossível**: ECOCROP e Embrapa dão chuva anual, não do ciclo | — |
| ~~`cobertura_meses`~~ | **FEITO 15/11 14h50**: derivado do ciclo (meses ÷ 6, perene = 1). Marcado como derivado sem fonte, precisa de validação agronômica | — |

## 4. Declarado e aceito como próximo passo

Não são dívidas escondidas, estão ditas no produto e nos documentos.

- ~~**Janela do ZARC**: o motor não lê~~ **MUDOU EM 15/11, 14h50.** O motor lê
  `janelas_zarc` e `cabe_na_janela` funciona: a janela do caupi em Roraima virou
  número (junho a agosto) e **muda a resposta** — o encaixe do caupi vai de 0,53
  em abril para 0,87 em julho, e a confiança sobe de 0,55 para 0,82. Onde não há
  janela o peso fica **nulo e vira lacuna declarada**, nunca zero. Carregar as
  outras janelas agora é só dado, e acende sozinho
- **Recurso para plantar: 0 de 14 campos, e agora a resposta diz isso.**
  15/11, 15h40. O Welder perguntou se tínhamos o dado dos recursos necessários
  para plantar. Não temos nenhum: busca por semente, muda, insumo, custo, adubo,
  calagem, mão de obra, trator, irrigação e crédito não acha campo em arquivo
  algum. Estava só declarado no `decisoes.json` (`comprar-semente` e
  `vale-irrigar` como FORA), que é documento de desenho e o produtor não lê.
  **O furo era de coerência:** o pitch abre com "muitos agricultores tiveram
  medo de investir", e medo de investir é questão de recurso. Agora todo
  `limites` carrega: *"de onde vem a semente ou a muda e quanto ela custa não
  entra aqui; esta resposta diz o que plantar, não se dá para comprar."*
  - **Próximo passo barato, para depois do prazo:** um campo
    `material_de_plantio` — maniva, rama, túbera ou semente comprada. É fato de
    propagação, tem fonte na Embrapa e **não precisa de preço nenhum**, então
    escapa do motivo pelo qual custo ficou fora. E é a distinção que encosta no
    medo de investir: o que ele replanta da própria roça não custa para plantar
    de novo. Entra como **fato que o bot diz**, não como peso novo no ranking,
    porque peso sem fonte foi o erro do `cobertura_meses`.
  - Fica fora de propósito: preço, crédito, PRONAF, mão de obra e maquinário.
    O desafio pede observação da Terra, solo, característica de cultura e
    prioridade do produtor; recurso não está na lista.
- **Uma frase falsa saiu dos limites no mesmo commit:** a linha fixa "a janela
  de plantio oficial do ZARC não está carregada" era **incondicional**, então
  mentia justamente para o caupi, a única cultura cuja janela está carregada —
  e repetia a lacuna condicional que já dizia "não está carregado para 9 das
  culturas daqui". Quem precisa confirmar com técnico já vai no
  `validar_com_tecnico` da opção.
- **SoilGrids**: API REST pausada pelo ISRIC. A camada de solo hoje é a umidade
  da NASA em três profundidades mais a temperatura do solo
- **Lotes**: o motor modela uma área. Quem tem três roçados tem três respostas
- **IA redatora ao vivo**: precisa de chave, não roda em página pública
- **FIRMS, GDD, SMAP, ECOSTRESS, Landsat, API oficial do WhatsApp**

## 5. Pesquisa de campo — roteiro pronto em [docs/19](19-roteiro-das-ligacoes.md)

- **Zero entrevistas em Roraima.** Temos 8 respostas de formulário de 7 pessoas
  e uma entrevista em Goiás, feita pelo parceiro
- A pergunta que vale é a do medo de investir, e precisa ser feita em Roraima
- Risco de método registrado no `docs/03`: a entrevista de Goiás pode estar
  confirmando uma hipótese que o entrevistador já tinha

## 6. Numeração

**Correção, 14h50 (chat do dado):** o `docs/14` existiu. Era *ECOCROP: o que ele
dá, o que ele não dá*, no branch `ecocrop-ciclo-15-11` (commit `6191dd0`), com o
ciclo de melão, jerimum, batata-doce, arroz e cará já preenchido.

**RESOLVIDO 15/11, 15h: está no `main`.** Duas coisas da nota acima estavam
erradas e vale registrar, porque a segunda quase custou o dado: o branch
**não** havia sido apagado do remoto, e havia um **PR aberto** (#1) com ele.
A conclusão "existe só no clone local" veio de não ter olhado o remoto. O
Welder achou o PR na interface do GitHub às 14h53.

A numeração não tem mais buraco: 01 a 19, sem faltas. A citação "(doc 14)" no
`docs/05` volta a valer.

## 7. Inconsistências entre documentos, varredura de 14h50 (chat do dado)

Conferido contra o `main` em `2bbd12b`. Só o que não estava acima.

**Número que um jurado pode checar**

| achado | onde | o que fazer |
| --- | --- | --- |
| Dois "normais" de junho a setembro: o slide usa **859 mm** (`media_serie_mm`), a climatologia que o motor usa soma **812 mm**. Com 812, 2026 dá −59%, não −62% | slides `problem-data`, README, doc 15 contra `nasa-power.json` `clim` | dizer no slide de que período é o 859, ou usar um só |
| "Janeiro a outubro de 2026: 858 mm contra 1.428" não tem dado no repositório: a série de 2026 vai até **setembro** (outubro é nulo), e o próprio doc 04 diz na linha 131 que outubro a dezembro não estão na série | README, doc 04 linha 53 e tabela de outubro | tirar, ou gravar a leitura de outubro com data |
| "O pior em 45 anos" com rodapé "1981 a 2026": a base é de 45 anos, e com 2026 a série tem 46 | slides EN e PT | "o pior desde 1981" |
| ~~Pesquisa: ainda diz 6 de 8~~ | — | **RESOLVIDO 15/11, 15h20.** E era pior: os dois números estavam **trocados entre si** no `local-roraima.json` — "planta outra coisa" com 6 de 8 (é 5) e "seca" com 5 de 8 (é 6). Os dois corrigidos, com a data da conferência na planilha dentro do campo. Doc 11 também |
| ~~"14 culturas, 4 com dado bom": o arquivo tem 3~~ | — | **VERIFICADO 15/11, 15h20: são 4 mesmo**, e a distribuição mudou com o merge. Hoje: **4 boa, 8 parcial, 2 falta**. O doc 12 está certo; quem citar a distribuição, use esses |
| **Slide 4 desatualizado pelo `2bbd12b`:** a bolha diz "out of the ground in **60 days**"; a demo agora diz **70 dias** (caupi corrigido para 70 a 75 pela Embrapa). O jurado que repetir a conversa vê outro número | `slides-en/solution.html`, `slides-pt/solution.html`, `texto-de-estudo-do-pitch.md` linha 27; também docs 11 e 12 como exemplo | trocar 60 por 70 nos dois decks e no texto de estudo |
| ~~Linha do milho no doc 05 se contradizia~~ | — | **RESOLVIDO 15/11, 15h20:** coluna em 110 a 145, fonte trocada para a Embrapa Milho e Sorgo e qualidade para boa. A linha ainda dizia "fraca: fonte é jornal" no mesmo lugar onde o título dizia que o jornal tinha saído |

**Promessa maior que a fonte**

| achado | onde | o que fazer |
| --- | --- | --- |
| "Fill crop traits from FAO ECOCROP" e "o gargalo não é código, é preencher a tabela": o ECOCROP dá **ciclo** (e nem para a melancia, que vem 0/0). Não dá água do ciclo, não dá tolerância à seca (campo vazio até na mandioca), não dá fixa N nem resíduo | slides `next` EN e PT, `texto-de-estudo-do-pitch.md` | "crop cycles from FAO ECOCROP; water need per crop from Embrapa or FAO 56" |
| `tmax_sofre_c` "o ECOCROP dá TMAX limpo": `TMAX` é a **máxima absoluta** de sobrevivência; a temperatura acima da qual a planta começa a sofrer é mais perto de `TOPMX`, a ótima máxima. É a quarta causa do doc 17 (semântica de campo externo) de novo | seção 3 acima | decidir qual dos dois é `tmax_sofre_c` antes de preencher, e escrever no `campos` do JSON |
| ~~A pendência do `culturas.json` manda preencher água pelo ECOCROP~~ | — | **RESOLVIDO no merge do PR #1:** a linha saiu e entraram três, dizendo que o ECOCROP não serve para água, que falta ciclo da melancia, e que o ciclo que entrou é faixa global |
| `agua_ciclo_mm` "fechado como impossível": é impossível **com ECOCROP e Embrapa**; o Kc do FAO 56 continua sendo caminho | seção 3 acima | "fechado para hoje" |

**Regra do doc 11 quebrada — ~~RESOLVIDO 15/11, 15h20~~**

- O molde falado dizia "**veranico**" depois de o doc 11 ter decidido
  "estiagem". Trocado. E a causa ficou fechada: a lista palavra-por-palavra do
  doc 11 virou o **invariante 8**, que reprova jargão em qualquer fala —
  `veranico`, `nitrogênio`, `pousio`, `sucessão`, nome de família botânica, e
  principalmente **`inverno` e `verão`**, que no Norte significam o contrário e
  inverteriam a resposta na boca do bot.
- **Achado de brinde:** esse molde **nunca é alcançado** em nenhum dos 2.748
  casos, então o invariante 8 não o pegaria. Medindo o resto: **18 das 66
  variantes de fala nunca rodam** nos casos de Roraima. Algumas por motivo
  conhecido e declarado (o aviso de calor só existe para a soja, que não se
  planta aqui; o aviso de ano chuvoso não dispara porque 2026 é seco), mas
  texto que nunca rodou é texto que ninguém leu, e foi exatamente aí que o
  "veranico" sobreviveu dois dias. Vale uma varredura depois do prazo.

**Documento velho que contradiz o novo**

- README, "O que está aberto" e "Próximos passos sugeridos para amanhã": ainda
  listam a regra de comparação como o buraco mais bloqueante, os slides como não
  escritos e o contrato com o Giuliano. E "site como hub (Giuliano)" contradiz o
  doc 09, "sem site". O mapa não tem o doc 15 nem `entregas/`.
- Doc 09, tabela de culturas por lugar: Roraima com 5 (o arquivo tem 11) e
  Centro-Oeste com **sorgo**, que não existe no `culturas.json`; o arquivo tem
  guandu e caupi.

### 7.1 O README tinha a sua própria lista de pendências, e ela envelheceu

Varredura de 15/11, 15h. O `README.md` carregava uma seção "O que está aberto,
por ordem de bloqueio" escrita em 14/11 e nunca atualizada. Ela dizia que a
regra de comparação do motor era "o buraco mais bloqueante" (resolvida há
horas), pedia mandar o contrato de retorno ao Giuliano (fora do projeto desde
15/11, e o próprio cabeçalho do README já dizia "Welder, sozinho desde 15/11"),
e trazia **a média de −10% dos anos de El Niño** como número nosso — o número
que a seção 2.1 aqui manda não usar.

A causa não é desatenção, é estrutura: **duas listas da mesma coisa divergem
sempre.** Corrigido pela forma, não pelo caso — o README agora resume e aponta
para cá, e esta lista é a única.

## Como usar esta lista

Quem resolver um item: risca aqui, no mesmo commit da correção. Quem achar
pendência nova em qualquer documento: traz para cá em vez de deixar no lugar
onde achou.

## 8. Privacidade

Telefone, nome e qualquer coisa que identifique quem respondeu o formulário
**não entram neste repositório**, que é público. Ficam na planilha privada do
Drive. Quase aconteceu em 15/11: a primeira versão do `docs/19` tinha os três
números escritos, e a ação foi bloqueada antes do commit.
