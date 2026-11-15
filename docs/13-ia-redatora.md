# 13 — A segunda IA: redatora, nunca calculista

> 15/11/2026, 12h. Ideia do Welder: uma segunda IA que faça o elo entre o que
> está no banco e o que a IA decifradora entendeu. Este documento adota a ideia,
> coloca o limite que ela precisa, e separa o que vai ao ar hoje do que fica
> para produção.

## O problema que ela resolve

O cerne hoje fala por molde fixo. Isso garante que ele não invente, e é o nosso
argumento mais forte no critério de Validade. O preço é que ele soa gravado:
toda resposta tem a mesma forma, e o teto existe por construção. Dá para
disfarçar com variantes, e a gente disfarçou, mas é teto.

## A arquitetura com três camadas, não duas

| camada | o que faz | pode errar? |
| --- | --- | --- |
| **IA decifradora** | fala do produtor → intenção estruturada | sim, e o erro é barato: pergunta de novo |
| **Motor determinístico** | intenção + dados → fatos estruturados | não: é aritmética sobre dado medido |
| **IA redatora** | fatos estruturados → frase natural | **não pode**, e é aí que mora o perigo |

A primeira já estava na arquitetura desde ontem, como "IA é roteador, não autor".
A terceira é a proposta nova. A regra que as separa:

> **A IA entende e a IA escreve. A IA nunca calcula, nunca escolhe a cultura e
> nunca inventa número.**

## O limite, que é o que torna a ideia aceitável

A redatora recebe **só** a resposta estruturada do motor. Nada de conhecimento
próprio sobre agricultura, nada de buscar na internet, nada do histórico. O
prompt dela é: reescreva estes fatos em uma frase curta, no registro deste
lugar, sem acrescentar fato nenhum.

E depois ela passa por **verificação automática**:

1. todo número que aparecer na saída tem que aparecer na entrada;
2. todo nome de cultura que aparecer na saída tem que estar nas opções que o
   motor devolveu;
3. se a resposta do motor foi uma recusa, a saída não pode virar indicação.

Se qualquer uma falhar, **cai no molde fixo**. É esse o ponto que fecha o
desenho: o sistema de moldes não desaparece, ele vira a rede de segurança. A
redatora é a camada bonita, e a camada honesta continua embaixo dela.

Assim dá para dizer na banca uma frase que quase nenhum projeto com IA
consegue dizer: **se a IA escrever algo que o dado não sustenta, o sistema
descarta e usa a frase conferida.**

## O que vai ao ar hoje, e por quê

Mudou desde que escrevi isto, e para melhor. O **motor determinístico agora roda
dentro do navegador** (`motor/cerne.js`), então a camada do meio não depende de
rede nem de servidor: calcula no aparelho, para qualquer combinação.

A redatora ao vivo é a única que precisaria de chave de API, e chave em
repositório público não existe. Então hoje ela entra **congelada**: as redações
foram escritas antes e vivem nos moldes que o motor preenche.

O desenho que sobra é bom, e vale dizer no slide:

- o cálculo roda **sem internet e sem servidor**, e metade dos respondentes do
  nosso formulário tem internet ruim ou só na cidade;
- **não custa por mensagem**, o que importa quando o alvo são dezenas de
  milhares de produtores sem assistência técnica;
- a resposta é **a mesma toda vez** para o mesmo dado, que é o que um técnico
  precisa para conferir.

Em produção a redatora roda ao vivo quando há sinal, e cai na versão congelada
quando não há. Degradação graciosa: o produtor perde o acabamento da frase,
nunca a resposta.

## Onde ela muda mais a conversa

Não é na frase principal, que já está boa. É no que hoje não existe:

- **acompanhar o fio**: "você já tinha me falado da mandioca, então…"
- **responder pergunta que não está no catálogo**, dizendo com precisão o que
  não sabe, em vez de cair no "não peguei"
- **ajustar o tamanho**: resposta curta de primeira, detalhe só se ele pedir
- **ouvir o jeito dele falar e responder no mesmo jeito**, que é o registro
  deixando de ser tabela e virando comportamento

## Custo honesto

- Latência: a redatora acrescenta de um a três segundos por resposta. Num
  atendimento de voz isso se sente.
- Dinheiro: centavos por conversa, mas vezes dezenas de milhares de produtores.
- Superfície de erro: mesmo com verificação, sobra o tom. A redatora pode soar
  confiante onde o dado é fraco. Mitigação: a confiança medida entra no prompt
  e a instrução de hesitar quando ela for baixa.

## Decisão

Adotada como arquitetura, com a verificação e o fallback obrigatórios.
Implementação ao vivo vai para próximos passos. Hoje entra no slide de
arquitetura como o desenho do sistema, e a demo roda congelada, declarando que
roda congelada.
