# Space Apps 2026: Field Shift em Roraima

Documento de trabalho do time para o NASA Space Apps 2026, desafio *Field Shift: Adapting Farms with NASA Data*.

**Responsável:** Welder, sozinho desde 15/11. **Última atualização:** 15/11/2026, 15h.

---

## ⏰ Prazo

**A página do formulário diz 23h59 de Boa Vista, domingo 15/11** (lido na própria
página em 15/11 às 16h40, registrado em `entregas/docs/formulario-submissao.md`).
**Trabalhamos para 22h59**, uma hora de margem, até o líder local confirmar. O que
vale é o último clique em "Submit for Judging": "Save Progress" deixa a página
pública mas não envia.

---

## A proposta, e o que ela não é

Nada aqui vai ficar perfeito até o prazo. Então está escrito o que é **escolha**,
o que é **limite declarado** e o que é **dívida** — e cada linha dá para conferir
abrindo um arquivo ou rodando um teste.

### O que isto é

- **Uma conversa de WhatsApp.** Na nossa pesquisa, 4 de 8 respostas disseram que
  querem ser alcançadas por mensagem escrita no WhatsApp (`dados/local-roraima.json`,
  campo `canal_preferido`). O canal não é palpite.
- Responde **uma** pergunta: o que plantar agora que eu colhi. Um ciclo à frente.
- Cruza observação do NASA POWER (chuva, umidade do solo em três profundidades,
  temperatura do solo, estiagem) com característica da cultura e **a prioridade que
  o produtor escolheu**.
- **Três números que nunca se misturam:** risco, encaixe e confiança.
- **Diz o que não conseguiu medir, na própria resposta.** Dez invariantes sobre
  2.748 casos reprovam se uma resposta afirma sem lastro (`motor/invariantes.py`).
- O mesmo motor em Python e em JavaScript, idênticos nos 2.748 casos
  (`motor/conformidade.py`). A página **calcula no navegador**; não é tabela pronta.
- **Todas as 816 indicações dizem ao menos uma razão medida** antes de dizer o que
  falta. Conferido pelo molde que o motor escolheu, não por palavra-chave: 442 pela
  indicação simples, 242 pela indicação com aviso de água, 132 pela cultura que ele
  não consegue avaliar — e **zero** caíram no molde de reserva que existe para quando
  não há razão nenhuma a dar.
- Família botânica é filtro duro, não peso: nematoide é parasita obrigatório.

### O que isto não é, de propósito

- **Não é integração com o WhatsApp.** A conversa é simulada para a ideia ficar
  visivelmente independente de canal: o motor devolve estrutura, e qualquer canal
  carrega. Viabilidade explicada, não implementada ([9](docs/09-mvp-decisoes-15-11.md)).
- **Não prevê chuva.** O enunciado pede observação e adaptação. O bot responde
  "prever chuva eu não sei, não tenho isso", e o ZARC Plantio Certo, que é oficial,
  já tem previsão: fomos feitos para ficar do lado dele, não no lugar.
- **Não otimiza renda.** É a única prioridade que declaramos não servir, e isso é a
  posição, não o buraco: as ferramentas que existem otimizam lucro para fazenda
  grande ([12](docs/12-alinhamento-pos-benchmark.md)).
- **Não dimensiona a área.** Uma área, uma resposta. Quem tem três roçados tem três
  respostas.
- **Não tem preço, crédito, mão de obra nem maquinário.** A resposta diz isso em voz
  alta, em todo `limites`.
- **Não tem IA rodando dentro da demo.** Compreensão por palavra-chave, aritmética
  determinística sobre dado nomeado, frase de molde fixo. A voz é a do navegador.
- **Não manda no produtor.** Compara, e mostra o que cada escolha faz com a terra
  neste ano.

### O que está incompleto, e declarado

| o que falta | tamanho | o que o bot faz hoje |
| --- | --- | --- |
| `agua_ciclo_mm` | 11 de 14 culturas | diz "quanta água ela pede eu não sei" e cruza o resto |
| `tmax_sofre_c` | 13 de 14 | o cruzamento de calor existe e **nunca dispara** nestes dois lugares |
| janela do ZARC | 1 de 11 em Roraima | onde está carregada **muda a resposta**: caupi de 0,53 em abril para 0,87 em julho |
| ciclo da braquiária | 1 cultura | é a única forrageira, e a única lacuna que trava uma prioridade inteira |
| espécie do cará | 1 cultura | *Dioscorea trifida* é suposição nossa; a linha carrega `validar_com_tecnico` e o painel mostra |
| a confiança mede **cobertura** de critério, não **qualidade** de fonte | desenho | `qualidade_do_dado` carrega a diferença e o painel mostra; a fala não diz |
| pesquisa de campo | n=1, em Goiás | três ligações em Roraima, roteiro pronto e não feitas ([19](docs/19-roteiro-das-ligacoes.md)) |

A lista completa, com dono de cada item, é [18. Pendências](docs/18-pendencias.md).

---

## Mapa dos documentos

| Documento | O que tem dentro |
| --- | --- |
| [1. Desafio, regras e julgamento](docs/01-desafio-regras-julgamento.md) | o enunciado e a leitura dele, prazo, regras de submissão, critérios de julgamento |
| [2. Problema e produto](docs/02-problema-e-produto.md) | a pergunta do produto, horizonte, decisão de linguagem, proposta de valor, o núcleo que cabe |
| [3. Persona e pesquisa de campo](docs/03-persona-e-pesquisa.md) | as duas personas, dados sobre o produtor, formulário, entrevista com o João, plano de entrevistas |
| [4. Dados da NASA](docs/04-dados-nasa.md) | POWER, parâmetros, chuva, umidade do solo, os três testes rodados, previsão sazonal, pegadinhas |
| [5. Base agronômica](docs/05-base-agronomica.md) | rotação contra sucessão, famílias botânicas, a lista real de culturas, ZARC, limiares |
| [6. Cerne e arquitetura](docs/06-cerne-e-arquitetura.md) | as quatro camadas, o contrato de retorno, o fluxo do atendimento, o que falta fechar |
| [7. Pitch e demo](docs/07-pitch-e-demo.md) | a correção urgente do pitch, contexto, os números que valem slide |
| [8. Fontes](docs/08-fontes.md) | tudo que foi lido, agrupado por tema |
| [9. Decisões do MVP, 15/11](docs/09-mvp-decisoes-15-11.md) | solo, WhatsApp sem site, plano A, áudio nos dois sentidos, slides em vez de vídeo |
| [10. O cruzamento](docs/10-cruzamento.md) | **como o dado chega até a decisão**: as regras, o protótipo que reprovou e por quê, o veredito de viabilidade |
| [11. Registro e linguagem](docs/11-registro-e-linguagem.md) | como o bot fala: a armadilha do inverno amazônico, o vocabulário dos respondentes, a troca palavra por palavra |
| [12. Alinhamento depois do benchmark](docs/12-alinhamento-pos-benchmark.md) | **a proposta de valor reescrita**: o que o benchmark derrubou, a lacuna de literatura que nos posiciona, a tabela comparativa |
| [13. A segunda IA, redatora](docs/13-ia-redatora.md) | a IA que escreve mas não calcula, a verificação que impede número inventado, e por que o molde fixo vira rede de segurança |
| [14. ECOCROP: ciclo das culturas](docs/14-ecocrop-ciclo.md) | **por que o ECOCROP não serve para a água do ciclo**, o ciclo que entrou linha por linha, e os três defeitos do motor que o dado novo expôs |
| [15. Campos da submissão](docs/15-submissao.md) | o rascunho dos nove campos em inglês, com o que ainda está entre colchetes |
| [16. De onde vem cada campo](docs/16-como-a-configuracao-chega.md) | como o lugar, a data, a colheita e a prioridade chegam no WhatsApp, sem formulário |
| [17. A raiz dos defeitos](docs/17-a-raiz-dos-defeitos.md) | **a recapitulação**: por que tanto bug, a causa única, e a correção estrutural que fechou a classe |
| [18. Pendências](docs/18-pendencias.md) | **a lista única**, de todos os documentos, com dono e se bloqueia. Resolveu, risca lá |
| [19. Roteiro das ligações](docs/19-roteiro-das-ligacoes.md) | as três perguntas, a quem ligar e o erro de método que elas evitam |
| [Motor](motor/cerne.py) | o cerne rodando: contrato de entrada e saída, as três notas, as frases de molde fixo |
| [Demo](index.html) | a página roda o motor **dentro do navegador** (`motor/cerne.js`), não consulta tabela. Trocar prioridade reordena, trocar o mês muda o veredito, trocar o lugar inverte |
| [Teste de invariantes](motor/invariantes.py) | seis regras de honestidade sobre 2.748 casos: degradar em silêncio ou afirmar sem lastro quebra o teste |
| [Teste de conformidade](motor/conformidade.py) | 2.748 casos exigindo que o motor em Python e o em JavaScript respondam igual. Rode depois de mexer em qualquer um dos dois |
| [Persona secundária (site)](docs/persona-secundaria.md) | **histórico, fora do escopo desde 15/11:** a trilha do site. Sobrevive dele a regra de verificação de textos |

---

## Onde estamos: decisões fechadas

- **Foco:** interior de Roraima, persona de quem usa WhatsApp.
- **A pergunta do produto:** "qual é a melhor plantação para plantar assim que eu colher essa remessa?" Genérica, sem premissa de 2026, e o El Niño entra pelos dados sem ser citado.
- **Horizonte:** um ciclo à frente. Três restrições independentes convergem: dado, usuário e terra.
- **Interface:** WhatsApp como atendimento guiado, **sem site**. Plano A: WhatsApp simulado, sem a API da Meta. Telegram e SMS no radar, não agora. ([9](docs/09-mvp-decisoes-15-11.md))
- **Arquitetura:** monolito modular com quatro camadas separadas. Motor devolve estrutura, não texto.
- **Linguagem:** nenhum jargão na conversa com o produtor; rigor no motor e na submissão.
- **Base de conhecimento separada do canal**, para que qualquer interface use o mesmo conteúdo.
- **Nada feito antes do hackathon entra no projeto**, incluindo o Buddy.
- **O enunciado pede observação e adaptação, não previsão.** A previsão sazonal entra só como contexto no pitch.
- **Solo não precisa ser dado da NASA**, mas acabou sendo: o POWER entrega umidade do solo sem login.

## O que está aberto, por ordem de bloqueio

A lista completa, com dono e estado, é [18. Pendências](docs/18-pendencias.md). **É a única lista.** Esta seção aqui ficou um dia inteira desatualizada enquanto a de lá andava, então agora ela só resume e aponta.

1. **Os nove campos da submissão em inglês**, a declaração de uso de IA e as duas caixas. Rascunho em [15](docs/15-submissao.md), com colchetes a preencher. *Chat do dado.*
2. **Confirmar a hora do prazo** com o líder local. Até confirmar, conta 22h59. **Welder.**
3. **Testar todos os links em aba anônima:** nada pode pedir login. **Welder.**
4. **Os 7 slides existem**, em inglês e em português, com o subtítulo obrigatório na capa, mais um vídeo-pitch de 29,9 s com legenda ([entregas/](entregas/)). Falta: o GIF do slide 4, o link do GitHub Pages no slide 7, **trocar "60 days" por "70 days" nos dois decks** (o caupi foi corrigido e o slide ficou atrás da demo) e exportar em PDF com link público. *Chat dos slides.*
5. **Falar no microfone na demo ao vivo.** Os cinco diagnósticos dão verde; falar nunca foi testado. **Welder.**
6. **Nenhuma entrevista em Roraima ainda.** A única é de Goiás, n=1. As três perguntas estão prontas em [19](docs/19-roteiro-das-ligacoes.md) e os contatos ficam na planilha privada, não aqui. **Welder.**
7. **A hipótese do áudio não está validada.** ([3](docs/03-persona-e-pesquisa.md))
8. **Água por ciclo** falta em oito culturas. O ECOCROP não serve para isso ([14](docs/14-ecocrop-ciclo.md)); a fonte certa é Embrapa por cultura ou o Kc do FAO 56. Não bloqueia: o motor declara a falta em vez de afirmar.
9. **A confiança mede cobertura de critério, não qualidade de fonte.** Com o ciclo do ECOCROP preenchido, cinco culturas foram a 100% ao lado do caupi, cujo dado é melhor. O número certo para essa diferença, `qualidade_do_dado`, a resposta já carrega e a fala não diz. ([14 §5](docs/14-ecocrop-ciclo.md))

**Saiu desta lista em 15/11:** a regra de comparação do motor, que era o item mais bloqueante — virou três notas separadas e 2.748 casos de teste; o contrato de retorno; o nome do projeto; os limiares sem fonte; e o ciclo de cinco culturas.

## Ordem sugerida do que falta hoje

1. Confirmar a hora do prazo. Decide o ritmo de tudo o que vem depois.
2. Submeter cedo uma versão simples e ir reenviando.
3. As três ligações. Quinze minutos tiram o pitch de "uma entrevista em Goiás, n=1".
4. Escrever os 7 slides, em inglês.
5. Falar no microfone na demo, uma vez, antes de apresentar para alguém.
6. Água por ciclo, se sobrar tempo. É o único item da lista que não muda nada se ficar de fora.

---

## Os números que são nossos

Medidos no NASA POWER em 14/11/2026, ponto do Cantá (lat 2,61, lon -60,60). Detalhe e método em [4](docs/04-dados-nasa.md).

| Achado | Número |
| --- | --- |
| Estiagem mais longa na estação chuvosa de 2026 | **24 dias**, contra 9 de média. Vem da série **diária**, que está no [4](docs/04-dados-nasa.md) e não no repositório: não dá para recalcular daqui |
| Dias com chuva, abril a setembro de 2026 | 92, contra 142 de média |
| Chuva de junho a setembro de 2026 | **330 mm contra 812 mm da climatologia: −59%**, o pior desde 1981. Contra os 859 mm da média da série inteira 1981–2026 (campo `media_serie_mm`, guardado no bloco do El Niño; inclui 2026, e sem 2026 a média é ~871 mm) dá −62%; os dois números estão no `nasa-power.json`, então **cite qual** |
| Umidade do solo no perfil, setembro de 2026 | 0,51 contra 0,76 do normal, nível que ali só aparece em janeiro |
| Chuva de janeiro a **setembro** de 2026 | **805 mm contra 1.358 mm: −41%.** Dizia "janeiro a outubro, 858 contra 1.428" até 15/11: outubro a dezembro não estão na série e nenhum dos dois números existia no repositório |

E o que **não** se confirmou, igualmente importante:

- "Ano de El Niño é ano seco" não se sustenta: nos anos de El Niño da nossa série o desvio de chuva de junho a setembro vai de **−48% a +17%** sem contar 2026, e vários vieram acima da média (o mínimo é 2015; com 2026 a faixa vai a −62%). **Usamos a faixa, nunca a média:** a lista de anos está incompleta (faltam ao menos 1994, 2018 e 2019, cerca de um quarto da amostra), e acrescentar anos só aumenta a dispersão — o que torna a faixa mais forte que a média, não mais fraca. ([18 §2.1](docs/18-pendencias.md))
- **Não há base para prever repetição de 2026.** A frase sobre anos de decaimento dar −2% saiu daqui em 15/11: dependia da mesma lista não conferida.
- Chuva mais forte não aconteceu em 2026: o maior dia foi 35,5 mm, abaixo da média de 44,4 mm.

---

## Regra de trabalho

- **Git:** antes de dar push, conferir a versão do momento. Se houver diferença, estudar e atualizar com base no que está lá.
- **Marcos:** cada etapa fechada ganha um branch `marco-revN-data`.
- **Histórico:** o git é o histórico. Nada se perde depois de uma edição, e o commit diz por que a edição foi feita, não só o que mudou.
- **Registro:** os documentos descrevem **o projeto**, não a conversa que o construiu. Sem "vamos fazer", sem autoria de quem sugeriu o que, sem detalhe da ferramenta usada para escrever. O que fica é a decisão, a data, a fonte e o motivo. A declaração de uso de IA é obrigatória e vive num lugar só: o campo *Use of AI* da submissão.
- **Dados pessoais:** os números de WhatsApp da planilha de respostas ficam fora do repositório.
- **Qualidade de dado:** nada vai para slide ou código sem fonte e sem data de leitura. Cada tabela marca o que está "a validar".
