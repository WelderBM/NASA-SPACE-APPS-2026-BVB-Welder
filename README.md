# Space Apps 2026: Field Shift em Roraima

Documento de trabalho do time para o NASA Space Apps 2026, desafio *Field Shift: Adapting Farms with NASA Data*.

**Responsável:** Welder, sozinho desde 15/11. **Última atualização:** 15/11/2026, 15h.

---

## ⏰ Prazo

**A submissão fecha domingo, 15/11, às 22h59 de Boa Vista.**

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
4. **Os 7 slides, em inglês**, com o subtítulo obrigatório `AgroDeal — What do I plant next?` e a **faixa** do El Niño, nunca a média. *Chat dos slides.*
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
| Veranico na estação chuvosa de 2026 | **24 dias**, contra 9 de média em 45 anos |
| Dias com chuva, abril a setembro de 2026 | 92, contra 142 de média |
| Chuva de junho a setembro de 2026 | 330 mm contra 859 mm: **-62%, o pior da série de 45 anos** |
| Umidade do solo no perfil, setembro de 2026 | 0,51 contra 0,76 do normal, nível que ali só aparece em janeiro |
| Chuva de janeiro a outubro de 2026 | 858 mm contra 1.428 mm: -40% |

E o que **não** se confirmou, igualmente importante:

- "Ano de El Niño é ano seco" não se sustenta: nos anos de El Niño da nossa série o desvio de chuva de junho a setembro vai de **−33% a +17%**, e vários vieram acima da média. **Usamos a faixa, nunca a média:** a lista de anos está incompleta (faltam ao menos 1994, 2018 e 2019, cerca de um quarto da amostra), e acrescentar anos só aumenta a dispersão — o que torna a faixa mais forte que a média, não mais fraca. ([18 §2.1](docs/18-pendencias.md))
- **Não há base para prever repetição de 2026.** A frase sobre anos de decaimento dar −2% saiu daqui em 15/11: dependia da mesma lista não conferida.
- Chuva mais forte não aconteceu em 2026: o maior dia foi 35,5 mm, abaixo da média de 44,4 mm.

---

## Regra de trabalho

- **Git:** antes de dar push, conferir a versão do momento. Se houver diferença, estudar e atualizar com base no que está lá.
- **Marcos:** cada etapa fechada ganha um branch `marco-revN-data`. Tag não funciona neste ambiente (403 do proxy).
- **Histórico:** o doc do Claude guarda revisões; o git guarda commits. Nada se perde após uma edição.
- **Dados pessoais:** os números de WhatsApp da planilha de respostas ficam fora do repositório.
- **Qualidade de dado:** nada vai para slide ou código sem fonte e sem data de leitura. Cada tabela marca o que está "a validar".
