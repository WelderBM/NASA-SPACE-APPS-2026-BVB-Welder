# 14 — ECOCROP: o que ele dá, o que ele não dá, e o que o dado novo expôs

> 15/11/2026, 13h. Preenchimento do ciclo das culturas que voltavam "não sei",
> decidido pelo Welder: só `ciclo_dias` pelo ECOCROP, água nula com motivo.
> O dado ficou no branch `ecocrop-ciclo-15-11`, fora do `main`, pelo motivo
> da seção 4. **Entrou no `main` em 15/11/2026, 15h**, depois que os dois
> defeitos da seção 4 foram corrigidos; a seção 5 conta o que o merge achou.

## 1. O ECOCROP não serve para a água do ciclo. Leia antes de tentar de novo.

O campo de chuva do ECOCROP (`RMIN`, `ROPMN`, `ROPMX`, `RMAX`) é **chuva anual**.
A ficha oficial de cada espécie no portal da FAO rotula a linha como
**"Rainfall (annual)"** (ex.: ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=2175,
o milho). O catálogo da ECHO, que descreve a base, lista os descritores como
"temperature, annual precipitation, soil pH".

O motor precisa de outra coisa: `agua_ciclo_mm`, a água que a cultura exige **no
ciclo**, porque a regra de risco é `chuva da janela ÷ exigência mínima` (doc 10).
Pôr a chuva anual nesse campo é o mesmo erro de unidade do mm/dia que já custou
duas correções no dia 15: a conta roda, o número sai, e está errado por um
fator que ninguém vê.

O tamanho do erro, com números do próprio CSV:

| espécie | ciclo ECOCROP | chuva mínima absoluta (anual) | se lida como "do ciclo" |
| --- | --- | --- | --- |
| *Cucumis melo* (melão) | 50 a 120 dias | 900 mm | o melão "pediria" 900 mm em 50 dias; risco alto em quase todo mês |
| *Oryza sativa* (arroz) | 80 a 180 dias | 1.000 mm | idem |
| *Zea mays* (milho) | 65 a 365 dias | 400 mm (ótimo 600 a 1.200) | o nosso `culturas.json` tem 500 a 800 mm **por ciclo**, de outra fonte: grandezas diferentes |

Uma observação que reforça: o OpenCLIM, que publica a cópia do CSV, aplica
esses limites ao total de chuva do período de crescimento no modelo deles. É
uma escolha de modelagem deles, não o que a FAO rotula. Não copiar.

**Onde está a água do ciclo de verdade:** Embrapa, cultura por cultura, ou o
coeficiente de cultura (Kc) do FAO 56 com a evapotranspiração. As duas são
pesquisa por cultura, sem atalho.

### Outros campos do ECOCROP que não servem aqui

- **Tolerância à seca** (`ABITOL`): vazio para quase todas, **inclusive a
  mandioca**, que tolera seca. Campo vazio não quer dizer "não tolera". Não
  usar como `tolera_seca`.
- **Temperatura** (`TOPMN`, `TOPMX`, `TMAX`): existe, mas o motor não usa
  temperatura hoje (`cerne.py` não lê `tfaixa_boa_c` nem `tmax_sofre_c`).
  Preencher não mudaria resposta nenhuma.
- **Família** (`FAMNAME`): vem em nomenclatura antiga (Gramineae, Leguminosae).
  Não sobrescrever `familia`, que é a regra do "não é parente".

## 2. O que entrou, linha por linha

Fonte de todas: FAO ECOCROP, `EcoCrop_DB.csv`, cópia em
github.com/OpenCLIM/ecocrop, campos `GMIN` e `GMAX`, lido em 15/11/2026.
Cada linha do JSON carrega `ciclo_fonte` com a espécie e o código EcoPort.

| cultura | espécie | EcoPort | ciclo | qualidade |
| --- | --- | --- | --- | --- |
| melão | *Cucumis melo* | 815 | 50 a 120 | parcial |
| jerimum | *Cucurbita moschata* (jerimum caboclo, escolha do Welder) | 820 | 80 a 140 | parcial |
| batata-doce | *Ipomoea batatas* | 1265 | 80 a 170 | parcial |
| arroz | *Oryza sativa* | 1574 | 80 a 180 | parcial |
| cará | *Dioscorea trifida*, **suposição** | 5429 | 280 a 330 | parcial |
| melancia | *Citrullus lanatus* | 708 | **não entrou**: o ECOCROP traz GMIN = GMAX = 0 | falta |
| banana | — | — | **fora de propósito** | falta |

- **Cará:** a *trifida* é a nativa e tradicional entre famílias indígenas e
  ribeirinhas do Amazonas e de Roraima; a *alata* é a introduzida (EcoPort 936,
  220 a 300 dias, registrada como `especie_alternativa`). Não temos fonte de
  qual se planta no interior de Roraima. Está marcada como suposição e com
  `validar_com_tecnico` na própria linha. Observação: o motor ainda não lê
  esse campo da cultura (a lista de `validar_com_tecnico` da resposta é fixa),
  então hoje ele vive só no dado.
- **Banana:** ciclo de perene não é ciclo de rotação. Ela ocupa a área por
  anos. O ECOCROP traz 180 a 365 dias para *Musa acuminata*, e não usamos.
- **Água:** `agua_ciclo_mm` continua `null` nas sete, com `agua_motivo`
  apontando para este documento.
- **Ressalva do ciclo:** a faixa do ECOCROP é global, cobre todas as
  variedades. O motor usa o **mínimo** da faixa, então "sai da terra em X dias"
  fica otimista até trocar por cultivar de Roraima.

## 3. A conformidade, antes e depois

- Antes: 816 casos, só as 4 primeiras culturas de cada lugar, comparando falas
  e cinco campos das opções.
- Ampliado (commit `677c22b`, no `main`): todas as culturas como colheita e
  como hipótese, resposta inteira comparada com chaves ordenadas. **2.748
  casos.** Não precisou amostrar: roda em meio segundo.
- A comparação inteira achou divergência **real**: 540 porques do português
  neutro (Rio Verde) em que o Python dizia "de outra família que a soja" e o JS
  "de outra família da soja". Python alinhado ao JS, que usa o campo `artigo`.
- Com o dado novo: 2.748 casos, idênticos.

## 4. O que o dado novo expôs no motor, e por que ele esperou fora do `main`

O dado está certo. O que ele faz o motor dizer, não.

**4.1. O bot afirma que a chuva dá quando não tem dado de água.** No "e se",
quando a cultura tem ciclo mas `agua_ciclo_mm` é nulo, o nível de água é
"sem dado" e o código cai no ramo `hipotese_boa`: "dá pra plantar, sim. A
chuva desse tempo dá o que ela precisa". **Isso já acontecia antes de hoje com
a mandioca**, a cultura da persona: "e se eu plantar mandioca depois do milho?"
responde que a chuva dá. Com o dado novo passa a acontecer também com melão,
jerimum, batata-doce, cará e arroz. É o sistema afirmando o que não sabe.

**4.2. A cultura que a gente conhece menos volta a ganhar.** Em Cantá, abril,
depois da mandioca, prioridade `risco`: antes o bot ia de caupi (confiança
0,55); com o dado ele vai de **melão, com confiança 0,27**, e diz "é rápida,
sai da terra em 50 dias". O melão ganha porque o único critério medido nele é
o ciclo curto, e 50 dias é o mínimo global. É o bug da braquiária do doc 10:
a ordenação usa só o encaixe e ignora a confiança. Ele estava escondido porque
as culturas sem ciclo eram filtradas antes de entrar no ranking.

As duas correções são código nos dois motores, e a segunda é decisão de
desenho. Ficam com o Welder.

## 5. O merge, e o terceiro defeito

15/11/2026, 15h. As duas correções da seção 4 já estavam no `main` quando este
branch foi lido, feitas por outro caminho e sem saber deste doc:

| defeito da seção 4 | o que o motor diz agora |
| --- | --- |
| 4.1 afirma que a chuva dá sem dado de água | "Quanta água ela pede eu não sei, mas a janela dá 258 milímetros e a estiagem mais longa no ciclo fica em 8 dias." Declara a falta e cruza o que sobra. |
| 4.2 o melão vence com confiança 0,27 | a ordenação passou a usar a confiança como porteira (`CONF_MIN = 0,5`). Em Cantá, abril, depois da mandioca, prioridade `solo`: caupi 0,78; melão **último**, 0,36. |

Com os dois fechados, o motivo de ficar fora morreu e o dado entrou. A
conformidade e os invariantes passam nos 2.748 casos com ele dentro.

**O merge achou um terceiro, da mesma classe.** A linha do cará traz
`validar_com_tecnico: ["qual especie de cara se planta na regiao: Dioscorea
trifida ou Dioscorea alata"]` — escrito no dado justamente para aparecer na
resposta. Os dois motores devolviam esse campo com um texto **fixo no código**:

```python
'validar_com_tecnico': ['a janela de plantio oficial do ZARC para o município'],
```

Um literal se passando por dado derivado. O que a linha mandava validar morria
no motor: o cará saía com `qualidade_do_dado: "parcial"`, confiança 1,00 e
nenhum sinal de que a espécie é suposição nossa. Corrigido nos dois motores —
o pedido da cultura entra na frente do pedido do lugar — e virou o
**invariante 7**: se a linha manda validar, a resposta leva. Antes ninguém
testava isso, e é por isso que ninguém viu.

Fica aberto, e é desenho, não bug: a confiança mede **cobertura** de critério,
não **qualidade** de fonte. Com o ciclo preenchido, melão, jerimum,
batata-doce, cará e arroz passaram todos a 1,00 na prioridade `solo` — do lado
do caupi, cujo ciclo vem da Embrapa com cultivar recomendada, enquanto o deles
é faixa global do ECOCROP. O número certo para essa diferença é
`qualidade_do_dado`, que a resposta já carrega e a fala não diz.

## Fontes

- FAO ECOCROP, `EcoCrop_DB.csv` e `Ecocrop_variable_lookup.csv`, github.com/OpenCLIM/ecocrop, lido em 15/11/2026
- FAO ECOCROP, fichas de espécie com "Rainfall (annual)": ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=2175 (Zea mays) e ?id=970
- ECHOcommunity, descrição do ECOCROP ("annual precipitation"), echocommunity.org
- Espécie do jerimum e status do cará: Welder, 15/11/2026
