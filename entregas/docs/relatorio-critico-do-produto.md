# AgroDeal: relatório crítico do produto

> 15/11/2026, 16h05 (Boa Vista). Escrito pelo chat de benchmark, slides e vídeos.
> Base: main em 8959e44 (o motor de d9e6e93), demo servida localmente a partir do
> repositório, Chrome headless em 1280 px e 390 px. Os testes `invariantes.py` e
> `conformidade.py` passam: 2748 casos. Nada aqui foi consertado no código: segue a
> regra de perguntar a classe do defeito antes de mexer no caso.

## Veredito curto

O motor é a parte mais forte do projeto e a mais difícil de copiar. Ele responde a
partir da colheita e reordena pela prioridade do produtor. Diz quanto do que
importa ele conseguiu medir, e o teste quebra quando uma lacuna fica calada. O
mesmo código dá risco baixo para milho no Cantá em abril (686 mm para 500 de
exigência) e risco alto em Rio Verde em setembro (386 mm). Isso é raro em projeto
de hackathon, e é o que a banca precisa ver.

A conversa em volta do motor é a parte fraca. Hoje ela promete mais do que entende.
O defeito mais sério está nela, e não no motor.

## O que conferi e está certo

| Afirmação nos slides e vídeos | Conferido no motor em 15/11, 16h |
| --- | --- |
| Julho, colheu mandioca, arriscar pouco: caupi, "sai da terra em 70 dias" | Sim, encaixe 0,87, confiança 0,82 |
| Mesma situação, a terra melhorar: caupi, "deixa a terra mais forte" | Sim |
| Abril: o encaixe de risco do caupi cai para 0,53 | Sim. Desde d9e6e93, o destaque de abril é arroz (80 dias), não mais braquiária |
| Renda: diz que não mede | Sim: "dela eu só consegui medir 0% do que importa" |
| Pasto: braquiária, ciclo desconhecido, avisa | Sim |
| Chuva em abril: "Prever chuva eu não sei..." | Sim, palavra por palavra |
| Milho 686 mm (Cantá, abril) contra 386 mm (Rio Verde, setembro) | Sim |

A correção de d9e6e93 resolveu um achado meu: em abril, "arriscar pouco" falava de
braquiária, que tem 1 de 4 critérios medidos. Agora a porteira da confiança vale
também para o destaque.

## Defeitos, do mais grave ao menos grave

**1. Digitar ou falar o objetivo não funciona. Só funciona por chip.**
Depois de "colhi mandioca" a demo pergunta "E o que te importa mais agora?". As
respostas "arriscar pouco", "a terra melhorar", "comida em casa", "pasto",
"dinheiro" e "renda", digitadas, voltam todas como "Não peguei". Causa: `trata()`
em `index.html` entende colheita, chuva, solo, riscos e e-se, mas não tem ramo para
prioridade. O objetivo só entra pelos chips ou pelo seletor.
Por que pesa: o slide 4 diz "by voice or text" e "they pick what matters". Por voz,
a escolha do objetivo, que é a proposta de valor inteira, não acontece. Se a banca
testar falando, cai aqui.
Pergunta de classe: o defeito é "a conversa não tem parser para o estado em que ela
mesma está" (prioridade hoje; amanhã qualquer pergunta nova)? Ou é só "faltam
palavras-chave de prioridade"? A primeira resposta pede que cada pergunta da
conversa declare o que aceita como resposta. A segunda resolve só este caso.

**2. "Feijão" sozinho não é reconhecido.**
"colhi feijão" faz a demo repetir "O que você acabou de colher?". Antes ela
respondia sobre mandioca, então piorou menos do que parecia, mas ainda falha.
"colhi caupi" e "colhi feijão-caupi" funcionam. O produtor de Roraima diz feijão.
Pergunta de classe: é um problema de sinônimo (o nome popular não está no dado da
cultura) ou de ambiguidade (feijão comum e caupi são culturas diferentes, e o
produto deveria perguntar qual)? Eu acho que é o segundo: responder caupi para quem
plantou feijão comum seria inventar.

**3. Pessoas de fora do Brasil não conseguem conversar com a demo.**
"I just harvested cassava" volta como "Não peguei". A banca global vai abrir o
link. Os slides estão em inglês e a demo só em português, sem aviso.
Pergunta (não é funcionalidade): basta uma linha em inglês no topo da página
explicando que a demo é em português, para o produtor, e quais chips clicar? Ou
vocês querem que a demo aceite inglês?

**4. O vídeo de 3 minutos diz "Ask about income".**
Pela demo não dá para perguntar de renda: não há chip, e digitado não entende
(defeito 1). O motor responde renda, mas só quem chama direto. A frase do vídeo
está correta sobre o motor e enganosa sobre a demo.
Pergunta: troco a frase do vídeo para "the engine says it can't measure income",
ou a demo ganha o chip de renda? Não mexi até você decidir.

**5. "1 dias".**
Chuva em julho: "a maior estiagem do mês costuma ser de 1 dias". Isso está no
gabarito do motor (`cerne.js`, frase de chuva). O número também parece pequeno
para julho; vale conferir se é a média de estiagem máxima ou um arredondamento.
Classe: plural fixo em todos os gabaritos com "{n} dias". `invariantes.py` testa
honestidade, não gramática. Um teste de concordância pegaria todos de uma vez.

**6. O aviso do ano se repete depois de cada resposta.**
"Só te aviso que o ano veio com..." aparece de novo a cada indicação. Na terceira
vez, o produtor para de ler. Pergunta: o aviso deveria sair uma vez por conversa,
ou uma vez por mudança de mês?

**7. Nome e identidade.**
A página se chama "Assistente da roça — demo", e o cabeçalho também. Os slides e
os vídeos dizem AgroDeal. A banca abre o link do slide 7 e vê outro nome. Também
falta favicon (404).

**8. Celular de 390 px: o botão de enviar fica cortado à direita.**
Quem usa a demo é quem tem celular simples. Aparece na captura de tela de hoje.

**9. A ordem das opções mistura encaixe e confiança sem explicar.**
Às vezes uma cultura com encaixe 1,00 aparece abaixo de uma com encaixe menor,
porque a confiança dela é baixa. A regra é boa, mas a tela não diz por quê. Quem
olha o painel "Diagnóstico" acha que é erro.

## Riscos de apresentação (não são defeitos de código)

- **"No AI calculates or picks the crop."** É verdade e é bom, mas a banca vai
  perguntar "então onde está a IA?". A resposta honesta: a voz é sintética e a
  compreensão é por palavra-chave. É bom ter essa frase ensaiada e não deixar a
  pergunta pegar de surpresa.
- **A voz da demo não foi testada por você num celular real.** O README do
  repositório ainda lista isso. Antes de enviar, teste uma vez no seu Android.
- **Os 859 mm incluem 2026.** Os slides e o vídeo já dizem "1981–2026 mean", e a
  nota de fala tem a resposta: sem 2026, ~871 mm, e a queda continua −62%.
- **A lista de anos de El Niño está incompleta** (faltam 1994, 2018 e 2019). Os
  slides mostram a faixa, nunca uma média. Mantenha assim.
- **docs/15** ainda tinha os números antigos do milho (621/331). Confira se o chat
  do dado já atualizou.

## O que eu faria antes do prazo (22h59)

1. Defeito 1, porque ele contradiz o slide 4. Se não der tempo de consertar,
   troque "by voice or text" por "by voice or text, with tap-to-choose goals". É uma
   frase só, e eu faço.
2. Linha em inglês no topo da demo (defeito 3) e o nome AgroDeal no título (7).
3. Decidir a frase de renda do vídeo (4).
4. Testar os dois links em aba anônima: o PDF e o Pages.

O resto (2, 5, 6, 8, 9) melhora a demo, mas não muda o que a banca julga. São
bons primeiros itens depois do hackathon.
