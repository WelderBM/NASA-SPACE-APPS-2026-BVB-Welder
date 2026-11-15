# 18 — Pendências, consolidadas

> 15/11/2026, 14h40. Varredura de todos os documentos. Três chats estão
> trabalhando no mesmo repositório, e pendência espalhada em quinze documentos
> faz dois chats refazerem o mesmo trabalho. Esta é a lista única.
> **Se resolver algo daqui, risque aqui.**

## 1. Bloqueia a submissão

| o quê | de quem | estado |
| --- | --- | --- |
| Os nove campos em inglês, a declaração de uso de IA e as duas caixas | chat do dado | rascunho em `docs/15`, com colchetes a preencher |
| Nome do projeto no slide e na submissão | **Welder** | decidido não usar "AgroDeal" sem checagem; falta escolher o título |
| Confirmar a hora do prazo com o líder local | **Welder** | conte 22h59 até confirmar |
| Testar todos os links em aba anônima | **Welder** | nada pode pedir login |

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

### 2.2 Limiares sem fonte anotada

- **Caupi** entre 18 °C e 34 °C: fonte não anotada
- **Soja** acima de 40 °C e 7 a 8 mm por dia: fonte não anotada, e o limiar de
  40 °C agora é usado no motor, no aviso de calor
- **Limiar de veranico**: não existe. O motor reporta o número e não classifica
- **Limiar de deriva de vento**: não existe. A decisão de pulverizar está fora do MVP

### 2.3 Fonte fraca

- O ciclo do **milho** veio de jornal (Folha BV). Trocar por Embrapa ou ZARC

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

Não existe `docs/14`. O salto de 13 para 15 é histórico, não é documento perdido.

## Como usar esta lista

Quem resolver um item: risca aqui, no mesmo commit da correção. Quem achar
pendência nova em qualquer documento: traz para cá em vez de deixar no lugar
onde achou.
