# 3. Persona e pesquisa de campo

[Voltar ao índice](../README.md)

## As duas personas

Decisão de 14/11: o time se divide por persona e por canal.

| | Persona primária | Persona secundária |
| --- | --- | --- |
| Quem | quem planta e decide, no interior | o "intermediário digital da família": filho ou neto |
| Canal | WhatsApp, como atendimento guiado | site, como hub de exploração |
| Responsável | Welder | Giuliano |
| Documento | este | [persona-secundaria.md](persona-secundaria.md) |

O que une as duas é o cerne: mesmos dados, mesmo motor, mesma resposta estruturada. Ver [06-cerne-e-arquitetura](06-cerne-e-arquitetura.md).

A definição formal das personas ainda está aberta: o Welder quer conversar antes de fechar.

## Dados sobre o produtor do interior de Roraima (pesquisa de 14/11)

Dados gerais e de órgãos públicos. **Nenhum deles mede o uso de WhatsApp ou de áudio pelo produtor do interior**; isso ainda depende de pesquisa de campo.

### Quantos são e quem assiste

- O IATER acompanha 50.192 produtores, sendo 43.192 agricultores familiares e cerca de 7 mil indígenas. A regional de Alto Alegre, Amajari e Boa Vista concentra 23.455 familiares ([Assembleia Legislativa de Roraima, set/2026](https://al.rr.leg.br/2026/09/21/economia-e-desenvolvimento/)).
- Num documento de convênio de março de 2024, o IATER registra 16.850 estabelecimentos, e **87% deles não recebiam assistência técnica** ([IATER, proposta de convênio](https://prda.sudam.gov.br/pdf/80bff30c20fcfd50e68aaebbd52cdf26.pdf)). É o dado mais forte para justificar um canal de informação.
- No Brasil, 82% dos estabelecimentos da agricultura familiar não recebiam assistência especializada, pelo Censo 2017 ([MDA/UFRR](https://www.gov.br/mda/pt-br/acesso-a-informacao/convenios-termos-de-cooperacao-e-termos-de-execucao-descentralizada/termos-de-execucao-descentralizada/2025/ted-ndeg-30879420240068-003731-celebrado-entre-o-mda-e-a-ufrr/pt.pdf)).
- O Projeto de Grãos do IATER atende cerca de 3 mil produtores nos 15 municípios, incluindo 1.377 agricultores familiares não indígenas ([Folha BV](https://www.folhabv.com.br/?p=666375)). Sem data na matéria; confirmar se é atual.
- Produtores indígenas são 33,63% dos produtores de Roraima, a maior proporção entre os estados ([IBGE, Censo Agro 2017](https://agenciadenoticias.ibge.gov.br/en/agencia-news/35880-indigenous-population-has-diversified-agricultural-production-with-a-majority-of-women-producers-and-less-pesticide-use.html)).
- A agricultura familiar é quase 78% dos estabelecimentos rurais de Roraima ([Folha BV, sobre a Embrapa Roraima](https://www.folhabv.com.br/geral/embrapa-roraima-completa-44-anos-impulsionando-producao-agricola-com-pesquisas-e-tecnologias-adaptadas/)).

### Celular, internet e cobertura

- Em 2015, mais de 98% do acesso à internet em Roraima era feito pelo celular, mas **só 6,1% dos moradores rurais** usaram internet nos três meses anteriores à pesquisa. É um dado antigo ([Folha BV](https://www.folhabv.com.br/?p=23793); [UERR](https://periodicos.uerr.edu.br/index.php/ambiente/article/download/866/560/2838)).
- Oito localidades rurais de Roraima ganharam sinal 4G nos últimos três anos ([Brasil 61](https://brasil61.com/n/expansao-do-4g-no-campo-roraima-soma-mais-oito-localidades-conectadas-mcom260414)).
- A Anatel aponta qualidade abaixo do mínimo em Alto Alegre, Caracaraí e Pacaraima ([Folha BV](https://www.folhabv.com.br/?p=93188)), e a fibra ainda não chega a alguns municípios do interior ([Folha BV](https://www.folhabv.com.br/?p=94305)).
- Há internet pública do programa Gesac em escolas, unidades de saúde e praças de quatro municípios do interior ([Folha BV](https://www.folhabv.com.br/?p=76731)). Houve anúncio de internet nas Casas do Produtor Rural em Rorainópolis, mas a data é antiga ([Folha BV](https://www.folhabv.com.br/?p=25596)).

**Implicação de desenho:** mensagem leve, pouco dado por envio, e funcionar com sinal ruim ou offline.

### Canal de informação

- Em pesquisa nacional, 96% dos produtores usam o WhatsApp para consultar decisões de negócio ([Canal Rural](https://www.canalrural.com.br/agricultura/quase-100-das-propriedades-rurais-conta-com-internet-mostra-pesquisa/)).
- Na pesquisa ABMRA 2025, a internet chega a 98% das propriedades e 61% usam o YouTube para orientação técnica ([Forbes Agro](https://forbes.com.br/forbesagro/2025/09/internet-atinge-98-das-propriedades-e-whatsapp-vira-principal-canal-do-agro-diz-nova-pesquisa-abmra/)).
- A Embrapa lançou o RAImundo, assistente por WhatsApp para pequenos e médios produtores, inclusive em áreas com baixa conectividade ([LexLegal](https://lexlegal.com.br/?p=28389)). É referência de canal e precedente.
- O Sistema CNA/Senar tem o JoIA, assistente por WhatsApp com clima, cotações e custos ([CNA](https://cnabrasil.org.br/noticias/joia-sistema-cna-senar-leva-inovacao-para-ajudar-produtor-a-tomar-decisoes)).

### Áudio no WhatsApp: hipótese não confirmada

A intuição do Welder é que essa persona usa mais áudio. Pesquisa feita em 14/11, **sem confirmação para Roraima**:

- O Brasil envia quatro vezes mais mensagens de voz no WhatsApp do que qualquer outro país, segundo a Meta ([Canaltech](https://canaltech.com.br/apps/whatsapp-brasil-envia-4-vezes-mais-audio-do-que-outros-paises-diz-zuckerberg-292037/)).
- Em 2024, 80% dos usuários mensais trocavam áudio, contra 86% que trocavam texto ([Voxbooster, com dados do Panorama Mobile Time/Opinion Box](https://voxbooster.com/pt-BR/blog/voice-message-vs-text-preference-country-statistics-2026/)).
- Em outra pesquisa, 56% disseram gostar e preferir enviar áudio ([Mobile Time, com dados Exame/MindMiners](https://www.mobiletime.com.br/?p=695702)).
- Precedente rural: um livro de 2025 sobre extensão rural propõe um método para produzir e enviar áudios de WhatsApp a produtores ([Zenodo](https://zenodo.org/records/14995584)).

**Contra a hipótese:** na nossa planilha de 6 respondentes, 3 preferem WhatsApp escrito. O formulário não perguntou sobre áudio.

**Como validar:** acrescentar duas perguntas ("você manda áudio no WhatsApp?" e "prefere receber resposta em áudio ou texto?"), pedir para o produtor mostrar como pergunta algo no WhatsApp com o celular na mão, e testar os dois protótipos com 3 a 5 pessoas.

**Cuidado técnico para o bot de áudio:** depende de reconhecer fala com sotaque e ruído de campo, e o WhatsApp precisa carregar bem em conexão fraca.

## Formulário

"Como a sua família decide o que plantar?", 13 perguntas, já publicado. [Link de edição](https://docs.google.com/forms/d/1g9mkbGMVdfErK_ww15vlBKYNFtulgBS2pxtbsYoKbNo/edit).

Planilha de respostas vinculada: 7 linhas, 1 duplicata, 6 respondentes únicos. **Contém números de WhatsApp: dado pessoal, fora do repositório, não publicar.**

Agregados dos 6 únicos:
- 3 "eu planto" e 3 "família"
- Municípios citados: Caracaraí, Cantá, Boa Vista, Rorainópolis
- Seca: 4 de 6 relataram perdas
- Gado: 1 de 6
- Confiança em satélite: sim 4, só com técnico 3 (contagem da planilha com duplicata)
- Canal preferido: WhatsApp escrito, 3
- Quem lê o celular: quem planta 3, família 3, ninguém 1

**Implicação:** a persona pecuarista não é sustentada pela amostra (1 de 6).

### O que cada resposta decide

As perguntas sobre produção e perdas definem público e problema; a da área depois da colheita mostra se já existe rotação; internet, quem lê o celular e canal preferido escolhem a interface; a da confiança em satélite diz se o técnico precisa estar no fluxo.

## Entrevista: João, produtor de Goiás (14/11/2026)

**Proveniência:** entrevistado pelo Giuliano, indicado por um mentor. Um produtor, de Goiás, não de Roraima. n=1. É a nossa primeira entrevista de verdade.

**O que ele disse:**
1. Muitos agricultores ficaram com medo de investir por causa do El Niño.
2. As fortes chuvas trazem muita erosão no solo.
3. Que pode ser irreversível.

**Análise:**

**Ponto 1 é o achado mais valioso até agora.** Não é dado de clima, é comportamento sob incerteza, e é exatamente a decisão que a ferramenta toca. Virou a proposta de valor do produto; ver [02-problema-e-produto](02-problema-e-produto.md).

**Ponto 2 não se confirma para Roraima em 2026.** Testamos no diário do POWER (ver [04-dados-nasa](04-dados-nasa.md)): o maior dia de chuva de 2026 foi 35,5 mm, **abaixo** da média de 44,4 mm, e a intensidade por dia de chuva caiu. O que houve foi 50 dias de chuva a menos e um veranico de 24 dias. A chuva forte que ele descreve provavelmente é experiência geral dele com erosão, não o sinal deste ano. A previsão oficial deste El Niño apontava chuva abaixo da média no centro-norte do país, incluindo boa parte do Centro-Oeste.

**Mas a erosão transfere por outro caminho, e isso vale manter:**
- Chuva forte acontece em Roraima, só não foi em 2026: em 2023, outro ano de El Niño, o maior dia deu 71,7 mm.
- O nosso caminho é inverso ao dele: o solo entrou na estiagem no mínimo do ano e o veranico de 24 dias deixa o solo descoberto e seco dentro da própria estação chuvosa. Solo nu e ressecado é o que lava quando a chuva volta em abril. A erosão chega **depois** da seca, não com chuva em excesso.
- O remédio é o mesmo nos dois casos: cobertura.

**Ponto 3, "pode ser irreversível":** são as palavras dele. Vale como citação de campo, não como afirmação técnica no pitch sem fonte.

**Cuidado de método:** o chat anterior do Giuliano já falava de erosão, e o foco do projeto mudou por isso. Essa entrevista pode estar confirmando uma hipótese que ele já tinha, em vez de trazer evidência nova. Não é motivo para descartar, é motivo para perguntar o mesmo a alguém de Roraima.

## Plano de entrevistas

A pergunta que vale ouro é a do ponto 1, e precisa ser feita em Roraima:

- "Este ano você plantou menos do que pretendia? Comprou menos semente?"
- "O que te fez decidir isso?"
- "O que você precisaria saber para plantar normal no ano que vem?"

Se um produtor de Cantá ou Caracaraí responder parecido com o João, temos o problema do produto confirmado em campo, em dois estados diferentes. Esse é o slide forte.

- [ ] Fazer 3 ligações de 10 minutos com quem planta, em Roraima
- [ ] Aplicar por ligação ou áudio com quem não usa formulário, preenchendo vocês mesmos; senão a amostra só terá quem já usa tecnologia
- [ ] Buscar gente nos contatos do Cantá, grupos de produtores, cooperativas, feira do produtor e técnicos de extensão
- [ ] Meta: 10 a 15 respostas e 3 conversas
- [ ] Gravar um áudio de 30 segundos como o sistema mandaria, enviar a 5 pessoas avisando que é exemplo e perguntar só "o que você faria com isso?"
- [ ] Pedir consentimento antes de gravar conversa e não publicar nomes
- [ ] Mostrar a reação de quem recebeu o áudio de teste; é o slide mais forte
- [ ] Declarar na submissão quantas pessoas responderam, o perfil e a data
- [ ] Mostrar os números da pesquisa separados por grupo ("X produtores e Y familiares")

## Lacunas de dado sobre a persona

- Número de estabelecimentos de agricultura familiar por município do interior: tabela 6778 do SIDRA/IBGE
- Uso de WhatsApp e de áudio pelo produtor do interior de Roraima
- Perfil do pecuarista familiar de Roraima
- Perfil do intermediário digital: quem é, com que aparelho, com que internet
- Estudo da Embrapa sobre perfil de produtores de leite em São Luiz e Rorainópolis, que tem parte sobre o perfil do proprietário: [PDF](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1132606/1/66-PerfilProdutores66-2021-B1.pdf)
