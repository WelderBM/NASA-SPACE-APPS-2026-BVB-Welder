# 16 — De onde vem cada campo, no produto real

> 15/11/2026, 13h50. Pergunta do Welder olhando a demo: "essa configuração será
> adquirida como?" É a única coisa que a demo disfarça, porque ela tem seletores
> e o WhatsApp por voz não tem nenhum.

O motor precisa de quatro coisas: **lugar, data, o que foi colhido e a
prioridade**. Cada uma chega por um caminho diferente, e três delas o produtor
nunca preenche.

| campo | como chega | quantas vezes |
| --- | --- | --- |
| **Lugar** | ele manda a localização pelo WhatsApp, que já tem esse botão | **uma vez na vida** |
| **Data** | o sistema sabe quando a mensagem chegou | nunca é perguntado |
| **O que colheu** | ele fala | toda conversa |
| **Prioridade** | ele fala | toda conversa, e trocar é o `explore` |

## O lugar, que é o único que precisa de gesto

O WhatsApp tem envio de localização nativo, de um toque. É o caminho limpo, e
o produtor não digita coordenada nenhuma. Isso acontece **no primeiro contato e
nunca mais**, porque a roça não muda de lugar.

Se ele não quiser ou não souber mandar, o plano B é o nome do município, que dá
o centroide. A resolução do NASA POWER vem do MERRA-2, numa grade de cerca de
meio grau, então **o centroide do município normalmente cai na mesma célula da
propriedade**. Perde precisão, não perde a resposta. Dizer isso é honesto e é
melhor que fingir precisão de metro.

## A data, que ninguém pergunta

O seletor de mês da demo **não é um campo do produto**. Ele existe para o jurado
poder testar outro mês e ver a resposta mudar. Em produção o mês é hoje, e se o
produtor quiser olhar outro, ele pergunta: "e se eu plantar em setembro?". Isso
é conversa, não formulário.

## Os dois que são conversa

O que ele colheu e o que ele quer são as duas únicas perguntas que o bot faz, e
ele faz uma de cada vez. Desde hoje o bot **pergunta em vez de assumir**: antes
ele lia o seletor e afirmava "da mandioca pra feijão-caupi" sem que ninguém
tivesse falado em mandioca.

## A regra de produto que sai disso

> Cada campo que a ferramenta pede é um produtor que desiste.

O desenho inteiro pede **um toque, uma vez**, e duas frases por conversa. Tudo o
mais o motor deriva. Isso não é economia de interface, é a diferença entre uma
ferramenta que o produtor usa e um cadastro que ele abandona na terceira tela.

E conversa com a lacuna que nos posiciona: o levantamento do Schöning achou que
as ferramentas de rotação ignoram propriedades de poucas centenas de metros
quadrados. Parte do motivo é esse. Ferramenta feita para fazenda grande assume
que existe alguém para preencher cadastro.

## O que o sistema guarda

O número do WhatsApp já é a identidade. Com ele dá para guardar o lugar, a
última colheita e a prioridade que ele costuma escolher, e aí a segunda conversa
começa sabendo de tudo. Nada disso é dado sensível além do que ele mesmo mandou.

## O buraco honesto: o lote

O motor modela **uma área**. Um produtor com três roçados tem três respostas de
"o que eu colhi", e hoje a gente não separa. O contrato já tem o campo `lotes`
previsto (doc 06) e o motor não usa.

Resolver isso é conversa, não cadastro: "esse é o mesmo pedaço de terra da
mandioca, ou é outro?". Fica em próximos passos, declarado.
