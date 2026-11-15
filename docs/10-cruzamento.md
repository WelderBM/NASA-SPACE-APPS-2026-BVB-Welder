# 10 — O cruzamento: do dado até a decisão

> Escrito em 15/11/2026, 11h, depois do Welder perguntar se o cruzamento
> estava descrito. **Não estava.** Este documento descreve, mede e dá o
> veredito de viabilidade com número real.

## O que faltava

A arquitetura (doc 06) tinha a fórmula:

```
nota(cultura) = Σ  peso_da_prioridade × encaixe(característica, observação, lugar)
```

O `encaixe` nunca foi definido. Era um nome no lugar de uma regra. Tudo o
resto do cerne existia — observação medida, característica da espécie,
camada local, prioridade como peso — e o meio estava vazio.

## Primeira tentativa: reprovada

`motor/prototipo.py` implementou o `encaixe` do jeito óbvio: cada peso vira
uma regra, soma tudo, normaliza. Rodou. Reprovou por três motivos.

### 1. A NASA quase não entrava na nota

Dos pesos de `prioridades.json`, só um (`agua_baixa`) cruza observação com
característica. Os outros são consulta de tabela de planta:

| peso | o que precisa | usa NASA? |
| --- | --- | --- |
| `fixa_n` | só a característica | não |
| `residuo_alto` | só a característica | não |
| `tolera_seca` | só a característica | não |
| `forrageira` | só a característica | não |
| `espera_no_campo` | só a característica | não |
| `ciclo_curto` | só a característica | não |
| `familia_diferente` | duas características | não (e já é filtro duro) |
| `agua_baixa` | chuva da janela ÷ exigência | **sim** |
| `cabe_na_janela` | janela do ZARC | bloqueado |
| `cobertura_meses` | nem existe na tabela | bloqueado |

Na prioridade **solo**, nenhuma cultura usava dado da NASA. A nota era
tabela de planta com verniz de satélite. O desafio pede uma ferramenta que
*use* observações da Terra: isso não passaria no critério de Validade.

### 2. Quem a gente conhece menos ganhava

A braquiária tirou nota **1,00 usando 27% dos critérios**. Venceu porque o
único critério que deu para medir nela foi tolerar seca. Quanto menos dado,
melhor o ranking. Isso é bug, e é bug que aparece no palco.

### 3. A nota única apagava o sinal do lugar

Milho em Cantá tirou 0,55 e em Rio Verde 0,50 — praticamente igual. Mas a
situação de água nos dois lugares é oposta. A média matou a diferença, que
era justamente a prova de que o cerne é genérico.

## A correção: três números, não um

`motor/prototipo2.py`. Em vez de misturar, separa:

| número | de onde vem | o que responde |
| --- | --- | --- |
| **risco** | NASA + lugar + momento | dá para plantar isso agora, aqui? |
| **encaixe** | característica + prioridade dele | serve para o que ele quer? |
| **confiança** | cobertura do dado | quanto dessa resposta é chute? |

Não se somam. O produtor ouve os três, e a confiança baixa aparece em vez
de ficar escondida dentro de uma nota alta.

### As regras de risco, escritas

**Água.** `chuva_climatológica_da_janela × fator_do_ano ÷ exigência_mínima`.
Razão ≥ 1,2 → baixo. 0,9 a 1,2 → médio. < 0,9 → alto.

**Fator do ano.** Chuva observada nos 3 meses antes do plantio ÷ a
climatologia dos mesmos meses. É assim que o El Niño entra: pelos dados,
sem ser citado. Cantá chegou em abril/2026 com **78%** da chuva normal de
jan–mar. Rio Verde chegou em setembro com **84%** da de jun–ago.

**Veranico.** Maior veranico climatológico nos meses que a **fase crítica**
atravessa; sem fase crítica documentada, o ciclo inteiro. Reporta o número
e não classifica, porque não temos limiar com fonte.

**Solo no plantio.** `GWETROOT` observado contra a climatologia do mês.

### As regras de encaixe

Mapa direto da característica, sem NASA, de propósito: `fixa_n` 1/0;
`residuo` alto 1 / médio 0,5 / baixo 0; `tolera_seca` alta 1 / média 0,6 /
baixa 0,2; `ciclo_curto` ≤90d 1 / ≤150d 0,6 / acima 0,3; `forrageira` e
`espera_no_campo` 1/0. Normaliza pelo peso que deu para medir, e devolve a
fração medida como **confiança**.

## A prova de que o cerne é genérico

Mesmo milho, mesma exigência de 500 mm, mesmo código, coordenada diferente:

| lugar | plantio | normal | ajustado pelo ano | risco de água | veranico |
| --- | --- | --- | --- | --- | --- |
| Cantá, RR | abril | 796 mm | 621 mm | **baixo** (1,24×) | 8 d |
| Rio Verde, GO | setembro | 392 mm | 331 mm | **alto** (0,66×) | 13 d |

Veredito oposto, sem uma linha de código específica de lugar. Era isso que
a nota única tinha apagado.

## O contraste que vale slide

Abril a setembro de 2026, contra 45 anos:

| | chuva 2026 | % do normal | veranico 2026 | veranico normal |
| --- | --- | --- | --- | --- |
| Cantá, RR | 717 mm | 54% | **24 d** | 9,3 d |
| Rio Verde, GO | 105 mm | 53% | 62 d | 64,3 d |

Os dois lugares perderam quase exatamente a mesma fração de chuva. Em Cantá
o veranico foi 2,6× o normal; em Rio Verde não mudou nada. **A mesma
anomalia de chuva significa coisas completamente diferentes.** Em Cantá é
desastre, em Rio Verde é rotina. É por isso que a ferramenta não pode ter
limiar fixo no código, e é por isso que o dado tem que ser por coordenada.

## Viabilidade: o que falta, e o que cada falta custa

| falta | trava o quê | custo de resolver |
| --- | --- | --- |
| ciclo e exigência de água em 7 das 11 culturas de Roraima | elas voltam "sei a família, não sei o ciclo" | baixo: CSV da FAO ECOCROP, 2.568 espécies |
| janela do ZARC quase toda nula | o peso `cabe_na_janela`, 1 dos 4 de risco | médio: Painel do ZARC, município por município |
| `cobertura_meses` não existe na tabela | 1 dos 4 pesos de solo | baixo: derivar do ciclo |
| limiar de veranico sem fonte | classificar o risco de veranico | médio: precisa de literatura |
| limiar de deriva de vento | a decisão de pulverizar | baixo |

**Veredito:** o cruzamento é viável e já roda. Com 4 culturas bem
documentadas ele responde de verdade; com 7 ele responde "não sei", e dizer
não sei é resposta honesta, não falha. O caminho crítico para melhorar não
é código, é preencher a tabela de culturas.

## O que NÃO entra no cruzamento

Preço, comprador, mão de obra, área do produtor. Sem dado, e o bot declara.

## Arquivos

- `motor/prototipo.py` — a primeira tentativa, guardada porque o erro dela
  é o argumento da segunda
- `motor/prototipo2.py` — o cruzamento em três números, que roda
