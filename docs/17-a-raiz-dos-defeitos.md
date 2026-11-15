# 17 — A raiz dos defeitos, e o que foi feito com ela

> 15/11/2026, 14h30. Vinte defeitos em um dia, quase todos da mesma causa. Esta é
> a recapitulação pedida pelo Welder e a correção estrutural que saiu dela: a
> classe foi fechada, não os casos.

## O sintoma

Entre 11h e 14h30 apareceram cerca de vinte defeitos. Parecem variados. Não são.

## A raiz, em uma frase

> O motor tratava cada informação que faltava **no ponto de uso**, com o `if`
> que estivesse ali. Não existia nenhum lugar que soubesse o que estava
> faltando e por quê.

Por isso todo consumidor novo de dado reintroduzia o mesmo defeito. E como o
ramo "senão" costuma ser a afirmação otimista, **a falta de dado virava
afirmação falsa**:

| o que faltava | o que o bot dizia |
| --- | --- |
| a exigência de água da cultura | "a chuva desse tempo dá o que ela precisa" |
| o ciclo da braquiária | recomendava feijão-caupi para pasto, com confiança 1,0 |
| nada: os valores eram iguais | "a terra está mais seca que o normal" |
| a leitura de 2026 depois de setembro | "sem leitura", sem dizer por quê |
| ninguém tinha dito a colheita | "da mandioca pra feijão-caupi" |

## A medida do estrago

Antes da correção: **12 de 24 combinações de lugar e mês degradavam, e nenhuma
dizia o motivo.** Janeiro a março e outubro a dezembro, nos dois lugares,
porque a série observada de 2026 vai até setembro e o motor nunca disse isso.

## As quatro causas, e por que elas são a mesma

1. **O padrão vence o silêncio.** Escrever `se X senão Y` onde a forma honesta
   tem três saídas, e a terceira é "não sei".
2. **Duas implementações da mesma regra.** Python e JavaScript divergindo.
3. **A decisão mora no documento e não no código.** "Sem jargão" voltou
   sozinho; a temperatura ficou um dia na tabela sem leitor.
4. **Semântica de campo externo.** mm/dia contra mm/mês; chuva anual contra
   chuva de ciclo, três vezes.

A 1 e a 3 são a mesma coisa vista de dois lados: **não havia um lugar
responsável pela ausência**, nem um teste que quebrasse quando a decisão era
desrespeitada.

E uma quinta, sobre o método: **consertar o caso e não a classe.** A braquiária
vencendo com 27% de confiança eu tratei como "cultura sem ciclo não pode
ganhar". A causa era "confiança não pesa na ordem". O melão entrou pela mesma
porta assim que ganhou ciclo.

## A correção estrutural

### 1. A lacuna virou cidadã de primeira classe

`lacunas_do_lugar()` é **um lugar só** que sabe o que falta e por quê. Cada
lacuna carrega três campos: `o_que`, `por_que` e `efeito`. Nenhum consumidor de
dado decide sozinho o que fazer com um nulo.

A resposta passa a trazer `lacunas`, os `limites` saem dela, e quando a lacuna
muda o que o produtor deveria esperar, **ele ouve**:

> "Uma coisa antes: a minha leitura deste ano vai até setembro, então pra
> dezembro eu só tenho a média dos 45 anos. Não dá pra te dizer como o ano está
> indo."

### 2. As regras de honestidade viraram teste

`motor/invariantes.py`, seis regras sobre 2.748 casos:

1. não afirmar sobre água sem o número da cultura
2. não dar direção a solo que está dentro da faixa
3. a fala tem que nomear a cultura em `destaque`
4. todo número falado tem que existir na resposta estruturada
5. **degradar em silêncio é falha**: lacuna que muda a expectativa e não é dita
6. confiança baixa tem que aparecer na fala, não só no painel

A 4 e a 5 são as que matam a classe. A 4 eu tinha desenhado no doc 13 para a
futura IA redatora e nunca tinha aplicado em mim.

### 3. A conformidade continua

`motor/conformidade.py`, 2.748 casos exigindo que Python e JavaScript respondam
idêntico. Pegou três arredondamentos divergentes e um molde desalinhado.

## O que isso custa e o que devolve

Custou cerca de uma hora. Devolveu: metade das combinações deixou de mentir por
omissão, e **a próxima vez que alguém escrever um consumidor de dado novo, o
teste quebra antes de chegar no palco.**

## A regra que saiu disso

> Nulo não é um valor. É uma lacuna, e lacuna tem dono, motivo e efeito.
> Se o seu código decide sozinho o que fazer com um nulo, ele está errado.

E a regra de método, que é a que eu mais errei hoje:

> Quando achar um defeito, pergunte qual é a **classe** dele antes de
> consertar o caso. Se a correção não quebra quando a classe reaparece, não foi
> correção, foi remendo.
