# Space Apps 2026: Field Shift em Roraima

Documento de trabalho do time para o NASA Space Apps 2026, desafio *Field Shift: Adapting Farms with NASA Data*.

**Responsável:** Welder. **Parceiro:** Giuliano. **Última atualização:** 14/11/2026, 22h.

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
| [Motor](motor/cerne.py) | o cerne rodando: contrato de entrada e saída, as três notas, as frases de molde fixo |
| [Persona secundária (site)](docs/persona-secundaria.md) | a trilha do Giuliano e a regra de verificação de textos |

---

## Onde estamos: decisões fechadas

- **Foco:** interior de Roraima, persona de quem usa WhatsApp.
- **A pergunta do produto:** "qual é a melhor plantação para plantar assim que eu colher essa remessa?" Genérica, sem premissa de 2026, e o El Niño entra pelos dados sem ser citado.
- **Horizonte:** um ciclo à frente. Três restrições independentes convergem: dado, usuário e terra.
- **Interface:** WhatsApp como atendimento guiado (Welder); site como hub (Giuliano). Telegram e SMS no radar, não agora.
- **Arquitetura:** monolito modular com quatro camadas separadas. Motor devolve estrutura, não texto.
- **Linguagem:** nenhum jargão na conversa com o produtor; rigor no motor e na submissão.
- **Base de conhecimento separada do canal**, para que qualquer interface use o mesmo conteúdo.
- **Nada feito antes do hackathon entra no projeto**, incluindo o Buddy.
- **O enunciado pede observação e adaptação, não previsão.** A previsão sazonal entra só como contexto no pitch.
- **Solo não precisa ser dado da NASA**, mas acabou sendo: o POWER entrega umidade do solo sem login.

## O que está aberto, por ordem de bloqueio

1. **A regra de comparação do motor.** Sem ela a saída é tabela, não recomendação. É o buraco mais bloqueante. ([6](docs/06-cerne-e-arquitetura.md))
2. **A abertura do pitch está errada:** dá a entender que 2027 repete 2026, e os dados não sustentam. ([7](docs/07-pitch-e-demo.md))
3. **O contrato de retorno** precisa ser fechado e mandado ao Giuliano, senão os dois não trabalham em paralelo. ([6](docs/06-cerne-e-arquitetura.md))
4. **A maior parte da tabela de culturas está sem dado** de ciclo e água. ([5](docs/05-base-agronomica.md))
5. **Definição formal das personas.** O Welder quer conversar antes de fechar. ([3](docs/03-persona-e-pesquisa.md))
6. **Nenhuma entrevista em Roraima ainda.** A única é de Goiás, n=1. ([3](docs/03-persona-e-pesquisa.md))
7. **A hipótese do áudio não está validada.** ([3](docs/03-persona-e-pesquisa.md))
8. **Pitch de 30 segundos e os 7 slides** não foram escritos. ([7](docs/07-pitch-e-demo.md))

## Próximos passos sugeridos para amanhã, em ordem

1. Fechar o contrato de retorno do motor e mandar ao Giuliano. Destrava os dois lados.
2. Definir a regra de comparação: como o motor ordena as opções.
3. Reescrever a abertura do pitch com o argumento do solo, não com previsão de 2027.
4. Ligar para 3 produtores de Roraima com as três perguntas sobre medo de investir.
5. Preencher ciclo e água das culturas que faltam, priorizando mandioca, caupi, milho, melancia e banana.
6. Escrever o pitch de 30 segundos e os 7 slides, em inglês.
7. Submeter cedo uma versão simples e ir reenviando.

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

- "Ano de El Niño é ano seco" não se sustenta: a média desses anos é só 10% abaixo do normal. O déficit aparece nos eventos fortes.
- 2027 cai num ano de decaimento, e esses anos dão média de -2%. **Não há base para prever repetição de 2026.**
- Chuva mais forte não aconteceu em 2026: o maior dia foi 35,5 mm, abaixo da média de 44,4 mm.

---

## Regra de trabalho

- **Git:** antes de dar push, conferir a versão do momento. Se houver diferença, estudar e atualizar com base no que está lá.
- **Marcos:** cada etapa fechada ganha um branch `marco-revN-data`. Tag não funciona neste ambiente (403 do proxy).
- **Histórico:** o doc do Claude guarda revisões; o git guarda commits. Nada se perde após uma edição.
- **Dados pessoais:** os números de WhatsApp da planilha de respostas ficam fora do repositório.
- **Qualidade de dado:** nada vai para slide ou código sem fonte e sem data de leitura. Cada tabela marca o que está "a validar".
