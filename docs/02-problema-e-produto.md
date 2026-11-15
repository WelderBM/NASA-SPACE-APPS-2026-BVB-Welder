# 2. Problema e produto

[Voltar ao índice](../README.md)

## A pergunta do produto

Versão final, decidida em 14/11:

> **Qual é a melhor plantação para plantar assim que eu colher essa remessa?**

Essa formulação é do Welder e substitui as anteriores. Por que ela é melhor:

- É a pergunta que o produtor realmente faz. Ninguém pergunta "qual rotação recupera meu solo".
- É ancorada num momento real de decisão: depois da colheita.
- **Não embute premissa.** As versões anteriores embutiam "solo seco" ou "antes da seca", que são premissas de 2026. Se 2027 vier normal, a premissa quebra e o produto quebra com ela. Esta sobrevive a ano seco, ano normal, Roraima ou qualquer outro lugar.
- O estado do solo deixa de ser premissa e passa a ser **entrada lida do dado**.
- O El Niño entra indiretamente, pelos dados observados, sem ser citado como objeto.

### Versões anteriores, para histórico

1. "Como ajudar uma família produtora de Roraima a escolher a próxima cultura da rotação antes da seca, com uma informação que chegue até ela?"
2. "...escolher qual rotação protege o solo e aguenta a seca, segundo as prioridades da família..." (sugestão aceita no doc em 14/11)
3. "Qual rotação recupera um solo que começa seco e aguenta um início ruim?" (proposta do Claude, descartada por embutir premissa de 2026)

## Decisão de horizonte: um ciclo à frente

O produto responde **o próximo plantio**, não um plano plurianual. Três restrições independentes apontam para o mesmo formato, e é essa convergência que sustenta a decisão:

| Restrição | O que ela impõe |
| --- | --- |
| **Dado** | Não existe previsão sazonal que possamos usar com honestidade, e o teste dos anos análogos mostrou que nem o El Niño serve de regra simples (ver [04-dados-nasa](04-dados-nasa.md)) |
| **Usuário** | Ele pensa no próximo plantio, não em 2029. "Quem olha com os olhos do futuro próximo quer saber o dia de amanhã" |
| **Terra** | Com um lote, rotação plurianual é quase inviável; o que ele pode mudar é o próximo plantio (ver [05-base-agronomica](05-base-agronomica.md)) |

O benefício de rotação acumula como efeito ao longo do tempo, não como promessa no primeiro uso.

## Decisão de linguagem: tirar o jargão

O produtor não precisa das palavras rotação, sucessão e consórcio, e muitas vezes não as conhece. Na conversa existe apenas:

- "o que plantar agora"
- "o que dá para plantar junto"
- "o que deixar cobrindo a terra"

E as razões viram fala comum:

| No motor | Na conversa |
| --- | --- |
| quebra de ciclo por família botânica | "é de família diferente do que você colheu, isso corta o ciclo da praga que ficou na terra" |
| fixação de nitrogênio | "deixa a terra mais forte para a próxima" |
| ciclo curto, fecha na janela | "fecha antes de a chuva parar" |
| déficit hídrico na fase crítica | "se faltar chuva nesse começo, perde" |

**Ressalva de público:** os termos técnicos ficam no motor e na submissão, porque a banca pode ter agrônomo e o enunciado usa a palavra *rotation*. Esconder o jargão do produtor e manter o rigor embaixo é decisão de design, e vale dizer isso de propósito no pitch. É ponto a favor, não desconhecimento.

Isso é coerente com a arquitetura: o vocabulário vive no adaptador de canal, como os textos. Ver [06-cerne-e-arquitetura](06-cerne-e-arquitetura.md).

## Proposta de valor: reduzir a paralisia

Achado da entrevista com o produtor João, de Goiás, em 14/11: **muitos agricultores ficaram com medo de investir por causa do El Niño.**

Isso reposiciona o valor do produto. O prejuízo do El Niño não é só a safra perdida, é a paralisia: não plantar, não comprar semente, não investir. Uma ferramenta que não prevê nada ainda tem muito valor se reduz essa paralisia, mostrando o que ainda é razoável fazer num ano ruim.

Resolve também uma angústia do projeto: **não precisamos prever para ser úteis.** Precisamos dar base para decidir sem travar.

Ver a entrevista completa e as ressalvas de método em [03-persona-e-pesquisa](03-persona-e-pesquisa.md).

## O núcleo que cabe até domingo

Comparar o que a pessoa acabou de colher com as opções de próximo plantio, usando dados do NASA POWER mais a camada local, e explicar o resultado num áudio de WhatsApp.

- [ ] Tratar como sequência, e não como recomendação de uma cultura solta: partir do que a pessoa acabou de colher e comparar pelo menos 3 opções
- [ ] Para cada opção, mostrar: por que foi sugerida, a evidência, o benefício, o que falta de dado e o risco a revisar com técnico
- [ ] Incluir solo como critério: cobertura, fixação de nitrogênio, resíduo na superfície e exposição à erosão ou ao fogo. Sem dado local, usar um perfil típico de Roraima, marcado como "a validar com a Embrapa"
- [ ] Posicionar como "ZARC atualizado com o clima deste ano": a janela oficial é fixa, o dado da NASA mostra como o ano atual está fugindo dela
- [ ] Usar fogo e seca como critérios da comparação, não como produtos separados
- [ ] Desenhar para o "intermediário digital da família": o filho ou neto que recebe o áudio e mostra para quem decide
- [ ] Mostrar o dado da NASA ao lado do sinal que o produtor já usa para prever a chuva
- [ ] Manter em todas as telas e áudios: apoia a decisão, não substitui o agricultor nem o técnico
- [ ] Tratar El Niño como contexto que justifica a ferramenta, não como centro do produto
- [ ] Usar frases fixas preenchidas com os números do motor; o robô ou o áudio nunca inventa texto
- [ ] Usar o formulário para mostrar que as prioridades são reais (renda, pasto, risco, mão de obra); a família escolhe as prioridades dentro da ferramenta, e o formulário não as alimenta
- [ ] Parar de gerar ideias novas

## Saúde do solo como saída

O enunciado pede fortalecer a saúde do solo, então a comparação precisa mostrar, por opção, o que acontece com o solo. Tudo qualitativo, a validar com a Embrapa Roraima:

- Cobertura: quantos meses do ano o solo fica coberto naquela opção
- Fixação de nitrogênio: leguminosas fixam (caupi, feijão comum, guandu, soja); gramíneas e raízes não
- Resíduo na superfície: gramíneas deixam palha; mandioca deixa pouco
- Exposição à erosão e ao fogo: solo descoberto na seca é o pior caso
- Ocupação da área: a mandioca fica 8 a 12 meses no campo, o que fecha as janelas para outra cultura no período

## Ponto de vista para o pitch

- [ ] Ligar a ferramenta à próxima decisão real: o plantio de 2027 começa em abril
- [ ] Usar a frase de um produtor de soja: ninguém previu que a chuva ia cortar tão cedo ([Portal Amazônia](https://portalamazonia.com/economia/seca-queda-colheita-soja-rr/)). O dado do NASA POWER para o Cantá já mostrava junho 38% abaixo da média
- [ ] Usar um caso real do interior de Roraima, como o Cantá, em vez de um campo genérico
- [ ] Declarar os limites: o que é estimativa de satélite, o que falta validar em campo, incluindo a falta de levantamento de solo do Cantá

## Cortado do núcleo, fica como próximos passos

O robô Buddy, os sensores como centro, o mercúrio do garimpo, a API oficial do WhatsApp, SMAP, ECOSTRESS e Landsat.
