# 9. MVP: decisões de 15/11

[Voltar ao índice](../README.md)

Dia da entrega. **O Giuliano não pôde estar presente**, e as decisões abaixo são o que muda quando uma pessoa executa a entrega sozinha. A dupla continua: a persona do site e a entrevista de campo são dele, e estão no [3](03-persona-e-pesquisa.md).

## O que mudou por causa disso

- **O contrato de retorno deixou de ser a prioridade.** Ele existia para duas pessoas trabalharem em paralelo sem se atropelar. Com uma pessoa, o contrato continua valendo como desenho do motor, mas não bloqueia mais ninguém.
- **Sem site.** Só WhatsApp. Decisão do Welder.
- **Plano A, sem o "plus" de API real da Meta.** O motivo é de produto, não de preguiça: deixar em evidência que a ideia entra em qualquer sistema de comunicação. A viabilidade no WhatsApp é explicada, não implementada.

## A hora do prazo

O guia de submissão diz **23h59 no horário local do evento**, e a página do
formulário do projeto, lida em 15/11 às 16h40, diz o mesmo. Um documento anterior
registrava 22h59, que é a hora para a qual o trabalho foi planejado: uma hora de
margem. O que conta é o último clique em "Submit for Judging"; "Save Progress"
deixa a página pública mas não envia.

## Formato do demo: 7 slides, não vídeo

O guia permite vídeo de até 30 segundos **ou** deck de até 7 slides, incluindo o título. Passar do limite tira do julgamento global, então não dá para mandar os dois.

Escolhemos slides. O raciocínio:

1. **Trinta segundos não cabem os nossos números.** Dá para umas 80 palavras. Nosso ativo mais forte é quantitativo (veranico de 24 dias, -62%, solo de setembro no nível de janeiro). Slide segura número.
2. **Variância.** Sozinho, vídeo é a tarefa de maior variância: regravar, nivelar áudio, legendar em inglês, renderizar, subir e conferir acesso público.
3. **Degradação.** Deck meio feito ainda é deck; vídeo meio feito é nada. E sobra tempo para aperfeiçoar.

**Onde o áudio vive:** o produto é voz e slides são mudos, então:

| Campo da submissão | Conteúdo |
| --- | --- |
| Link to Project Demo | os 7 slides, em inglês, hospedados fora (Drive ou YouTube), link público |
| Link to Final Project | a página funcionando, onde o jurado **fala com a coisa** |

Dentro de um slide, um **GIF da conversa acontecendo** com a transcrição visível na tela: mostra o movimento sem edição de vídeo, e se lê sem som. A página do projeto aceita GIF até 10MB.

Se sobrar tempo, gravação de tela com som entra na Detailed Project Description como apoio, **nunca** no campo do demo.

## Campos da página do projeto

Lista de tarefas de escrita, tudo em inglês:

- [ ] Project Name
- [ ] High-Level Project Summary
- [ ] Link to Project Demo (os slides)
- [ ] Link to Final Project (a página)
- [ ] Detailed Project Description
- [ ] NASA Data
- [ ] Space Agency Partner & Other Data
- [ ] Use of Artificial Intelligence
- [ ] Project Submission Verification (marcar as duas caixas)

Regras que pegam: links não podem exigir senha, permissão ou cadastro; a página aceita só imagem JPG, PNG ou GIF até 10MB; para áudio é preciso declarar geração por IA em texto descritivo e metadados; e conteúdo gerado por IA não pode conter nem modificar marca ou elemento de design da NASA.

## Host: GitHub Pages, não artifact

**Artifact não serve para este produto.** O guia do servidor de artifacts é explícito: câmera, microfone, localização e captura de tela são recusados ou ignorados no frame, e `fetch` para outros hosts é bloqueado. Sem microfone não existe atendimento por voz.

**GitHub Pages resolve e é melhor para a submissão:** HTTPS, link público, sem senha nem cadastro, que é exatamente o que as regras exigem, e o microfone funciona.

- Repositório já é público
- `index.html` na raiz do `main`, com `.nojekyll`
- Settings → Pages → Deploy from a branch → `main`, pasta `/ (root)`
- URL: `https://welderbm.github.io/NASA-SPACE-APPS-2026-BVB-Welder/`
- Habilitar o Pages é tarefa manual, na interface do GitHub: a API de Pages não está disponível no ambiente onde o motor foi escrito

## Áudio nos dois sentidos entra no escopo

A proposta inicial cortava "receber e entender áudio do produtor" do escopo. **Decisão do Welder: entra, e ele estava certo.**

Transcrever áudio de mensagem do WhatsApp exigiria servidor, e foi por isso que o áudio quase ficou fora. No navegador não precisa: existe a Web Speech API, `SpeechRecognition` ouve e `speechSynthesis` fala, as duas em pt-BR, sem chave e sem backend. Dá para fazer o atendimento inteiro, estilo central de atendimento de operadora, numa página.

Ressalvas:
- `SpeechRecognition` é Chrome e Edge; Firefox e Safari não cobrem bem
- Precisa permissão de microfone e contexto seguro (HTTPS)
- A voz sintética é geração por IA e **precisa ser declarada** na submissão
- Degradação obrigatória: se o microfone não abrir, o mesmo fluxo segue por botão e texto

Na submissão, a ponte com o WhatsApp é explicada: lá o mesmo fluxo usa mensagem de áudio mais transcrição, e o motor é o mesmo.

## Cerne genérico, validado pelo organizador

O organizador sugeriu um cerne genérico o bastante para não cobrir só Roraima, mantendo o foco. É exatamente a arquitetura de quatro camadas de [06](06-cerne-e-arquitetura.md): a observação da NASA é dirigida por coordenada, então já é universal; só a camada local muda.

**A armadilha é genérico declarado contra genérico provado.** Dizer "serve em qualquer lugar" é barato. O que convence é rodar a mesma pergunta em outro lugar, sem mexer no código, e sair resposta diferente.

Então entrou um segundo lugar: **Rio Verde, Goiás**. Mesmo estado do produtor entrevistado, embora não o município dele.

E a lista de culturas levantada em 14/11 **não estava errada, estava no arquivo errado**: soja, milheto e braquiária são a configuração do Centro-Oeste, não a de Roraima. Nada se perde.

| Configuração local | Culturas |
| --- | --- |
| `roraima` | mandioca, caupi, milho, melancia, banana |
| `centro-oeste` | soja, milho, sorgo, braquiária, milheto |

### O contraste entre os dois lugares é o melhor argumento

Dados do POWER, puxados em 15/11 (ver `dados/nasa-power.json`):

| | Cantá, RR | Rio Verde, GO |
| --- | --- | --- |
| Pico de chuva | maio a julho (287, 289, 255 mm) | novembro a março (189, 204, 214 mm) |
| Mês mais seco | fevereiro (31 mm) | agosto (7 mm) |
| Veranico normal, abril a setembro | **9 dias** | **64 dias** |
| Mínima de julho | 19,8 °C | **5,35 °C** |

**As estações são invertidas.** A estação chuvosa de Cantá é a seca de Rio Verde. Um veranico de 24 dias é catástrofe em Cantá e rotina em Rio Verde. Isso prova que o motor lê o dado em vez de recitar roteiro, e é o critério de Validade.

## Virando a mesa nos dados: o que o agricultor pode perguntar

Decisão do Welder: soltar as amarras e não amadurecer ideia cedo demais. O levantamento de 14/11 filtrou o POWER por suposição antes da hora e ficou com 3 de umas 15 variáveis úteis.

Em vez de perguntar que dado temos, perguntar **o que o agricultor pode perguntar**. Num atendimento por voz, o conjunto de perguntas respondíveis *é* o produto.

| O que ele pergunta | Dado que responde | Temos? |
| --- | --- | --- |
| A terra está boa para plantar? | `GWETTOP`, `GWETROOT`, `GWETPROF` + chuva recente | sim |
| Choveu quanto esse mês? | `PRECTOTCORR` | sim |
| Quantos dias sem chover? | `PRECTOTCORR` diário | sim, por mês e por ano |
| Esse ano está pior que os outros? | série de 1981 a 2026 | sim |
| **Está bom para secar farinha?** | `ALLSKY_SFC_SW_DWN` + `CLOUD_AMT` + `RH2M` | **sim** |
| Está bom para pulverizar? | `WS2M` | sim |
| A terra está quente para germinar? | `TSOIL1` a `TSOIL6` | sim |
| Vai dar doença? | `RH2M` + `T2M` | parcial, falta limiar |
| Quanto falta para colher? | `GDD` | sim, falta a base por cultura |
| O que plantar depois do milho? | família botânica + ciclo + água | sim, é o motor |
| Tem fogo perto de mim? | FIRMS | precisa de chave gratuita |
| **Vai chover semana que vem?** | — | **não, e isso virou recurso** |
| Minha roça está mais fraca que a do vizinho? | NDVI | não cabe hoje |

### O achado local: secar farinha

A mandioca vira farinha, a farinha é a maior saída de Cantá e Iracema, secar depende de sol e de ar seco, e temos radiação, nuvem e umidade relativa. Essa pergunta não sai da literatura de soja nem de dataset americano. **Só existe aqui, e a NASA responde.**

### O que não podemos responder vira recurso

Quando ele perguntar se vai chover, o bot diz que não sabe prever, diz o que sabe (choveu X esse mês, a terra está assim, o normal para a época é Y) e manda para a previsão oficial. Um assistente que admite o limite é mais confiável que um que adivinha, e isso é slide.

## Correção de erro em doc 04

O doc 04 afirmava que "a climatologia devolve mm do mês". **Está errado.** Conferido em 15/11: o endpoint de climatologia também devolve `PRECTOTCORR` em **mm/dia**. Os valores do nosso doc (32, 31, 50, 146, 287 mm) já estavam convertidos, o que mascarou o erro. Confirmação: 1,04 mm/dia × 31 dias = 32 mm, que é o valor de janeiro.

**Regra válida para os três endpoints (climatologia, mensal e diário): `PRECTOTCORR` vem em mm/dia.** Para mm do mês, multiplicar pelos dias.
