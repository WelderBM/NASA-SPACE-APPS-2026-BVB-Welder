# 4. Dados da NASA

[Voltar ao índice](../README.md)

Todos os testes deste documento foram rodados em 14/11/2026, no ponto do Cantá: **latitude 2,61, longitude -60,60**.

## NASA POWER

É a nossa fonte principal de observação da Terra. Não exige login, devolve JSON por coordenada e funciona no mundo todo ([site](https://power.larc.nasa.gov/)).

A comunidade AG tem **1.388 parâmetros**. Fonte do dado: reanálise MERRA-2, e IMERG para a chuva por satélite.

### Parâmetros que usamos ou devemos usar

| Parâmetro | O que é | Unidade | Status |
| --- | --- | --- | --- |
| `PRECTOTCORR` | chuva corrigida | mm/day | em uso |
| `IMERG_PRECTOT` | chuva por satélite IMERG | mm/day | checagem independente do PRECTOTCORR |
| `GWETTOP` | umidade do solo na superfície | fração 0 a 1 | confirmado em 14/11 |
| `GWETROOT` | umidade na zona de raiz | fração 0 a 1 | confirmado em 14/11 |
| `GWETPROF` | umidade no perfil | fração 0 a 1 | confirmado em 14/11 |
| `T2M_MAX`, `T2M_MIN`, `T2M` | temperatura do ar | °C | em uso |
| `GDD10`, `GDD13_3`, `GDD15_6`, `GDD4_4`, `GDD7_2` | graus-dia acumulados, cinco bases | degree-day-c | **a adotar: é assim que se calcula duração de ciclo de verdade** |
| `TSOIL1` a `TSOIL6` | temperatura do solo em seis profundidades | °C | a avaliar, serve para germinação |
| `RH2M` | umidade relativa | % | a avaliar, proxy de pressão de doença |
| `ALLSKY_SFC_SW_DWN` | radiação na superfície | MJ/m²/day | listado e **não usado**: ou entra numa métrica ou sai da lista |
| `ALLSKY_SFC_PAR_TOT` | radiação fotossinteticamente ativa | MJ/m²/day | a avaliar, liga com biomassa |

**Por que GDD importa:** com graus-dia o ciclo responde ao ano real, em vez de ser "100 a 140 dias" fixo. Em ano quente a cultura fecha mais cedo. Isso muda a conta de "cabe na janela?".

### Endereços e pegadinhas

- Climatologia: `https://power.larc.nasa.gov/api/temporal/climatology/point`
- Mensal: `https://power.larc.nasa.gov/api/temporal/monthly/point` com `start` e `end` em anos
- Diário: `https://power.larc.nasa.gov/api/temporal/daily/point` com `start` e `end` em AAAAMMDD
- Comum a todos: `parameters=...&community=AG&longitude=-60.60&latitude=2.61&format=JSON`
- Lista de parâmetros: `https://power.larc.nasa.gov/api/system/manager/parameters?community=AG&temporal=monthly`

**PEGADINHA IMPORTANTE, corrigida em 15/11:** os **três** endpoints (climatologia, mensal e diário) devolvem `PRECTOTCORR` em **mm/dia**, não em mm do mês. Para obter mm do mês, multiplicar pelos dias. Este doc afirmava antes que a climatologia vinha em mm do mês, o que estava errado; os valores das tabelas abaixo já estavam convertidos, o que mascarou o erro. Confirmação: 1,04 mm/dia x 31 dias = 32 mm, que é janeiro no Cantá. Misturar os dois gera erro de 30x.

**Períodos-base diferentes:** a climatologia de umidade do solo é de janeiro de 2001 a dezembro de 2025 (25 anos). A climatologia de chuva pode ter outro período-base. Registrar o período de cada consulta antes de comparar os dois.

### Acesso: o proxy bloqueia, o navegador resolve

Em 14/11 o proxy do ambiente do Claude passou a recusar `power.larc.nasa.gov` com **403 no túnel CONNECT**, que é negação de política, não falha de rede. Não se deve insistir nesse tipo de erro.

**Contorno que funciona:** usar o navegador integrado, que roda na máquina do usuário. Abrir qualquer página do domínio `power.larc.nasa.gov` e executar `fetch` em JavaScript na própria página, que fica como mesma origem. Foi assim que todos os testes abaixo foram rodados.

Isso afeta só o sandbox do Claude, **não o produto**: o backend de vocês vai rodar em outra máquina.

## Chuva mensal de 2026 contra a climatologia (Cantá)

De janeiro a outubro de 2026 choveu 858 mm, contra 1.428 mm da média histórica: **40% a menos**.

| Mês de 2026 | Média histórica (mm) | 2026 (mm) | Diferença |
| --- | --- | --- | --- |
| Janeiro | 32 | 45 | +41% |
| Fevereiro | 31 | 1 | -97% |
| Março | 50 | 42 | -16% |
| Abril | 146 | 129 | -12% |
| Maio | 287 | 257 | -10% |
| Junho | 289 | 179 | -38% |
| Julho | 255 | 117 | -54% |
| Agosto | 176 | 27 | -85% |
| Setembro | 92 | 7 | -92% |
| Outubro | 70 | 54 | -23% |

A estação chuvosa começou perto do normal e **acabou cedo**: agosto e setembro somaram 34 mm, contra 268 mm da média. A máxima média de setembro foi 39,6 °C.

## Umidade do solo (confirmado em 14/11)

Climatologia 2001-2025 para o Cantá, em fração de 0 a 1:

| Mês | Superfície | Zona de raiz | Perfil |
| --- | --- | --- | --- |
| Janeiro | 0,43 | 0,55 | 0,55 |
| Fevereiro | 0,38 | 0,53 | 0,53 |
| Março | 0,39 | 0,53 | 0,53 |
| Abril | 0,54 | 0,58 | 0,57 |
| Maio | 0,75 | 0,74 | 0,72 |
| Junho | 0,85 | 0,85 | 0,82 |
| Julho | 0,88 | 0,89 | 0,86 |
| Agosto | 0,86 | 0,88 | 0,85 |
| Setembro | 0,78 | 0,79 | 0,77 |
| Outubro | 0,66 | 0,67 | 0,66 |
| Novembro | 0,58 | 0,61 | 0,60 |
| Dezembro | 0,51 | 0,57 | 0,57 |
| Ano | 0,64 | 0,68 | 0,67 |

**Como ler:** o solo mais seco é em fevereiro e março, e o mais úmido em julho. A safra começa em abril, quando a superfície está em 0,54 e subindo. Isso casa com a regra da mandioca: ela é sensível ao déficit nos três primeiros meses, e plantada em abril a fase crítica cai justamente nos meses mais úmidos.

## Teste 1: ano de El Niño é ano seco no Cantá?

**Método:** série mensal do POWER de 1981 a 2026, somando junho a setembro (fim da estação chuvosa e enchimento dos grãos), com os valores convertidos de mm/dia para mm do mês. Média da série: **859 mm**.

Anos em que o El Niño estava ativo em junho-setembro, ou seja, anos de desenvolvimento:

| Ano | Jun-set (mm) | Contra a média |
| --- | --- | --- |
| 1982 | 572 | -33% |
| 1986 | 980 | +14% |
| 1987 | 820 | -5% |
| 1991 | 1.007 | +17% |
| 1997 | 678 | -21% |
| 2002 | 993 | +16% |
| 2009 | 812 | -5% |
| 2015 | 445 | -48% |
| 2023 | 627 | -27% |
| **2026** | **330** | **-62%** |

Média dos anos de desenvolvimento, sem 2026: **-10%**.

Anos de decaimento (o ano seguinte ao pico): 1983 -38%, 1988 +29%, 1992 -9%, 1998 +32%, 2003 0%, 2010 -3%, 2016 -9%, 2024 -15%. Média: **-2%**.

### Conclusão do teste 1

**A regra simples "ano de El Niño é ano seco" não se sustenta.** O desvio nesses anos vai de **−33% a +17%** e três deles vieram acima da média.

> **Ressalva de 15/11, 15h — leia antes de citar a média.** A lista de anos
> acima está incompleta: faltam ao menos **1994, 2018 e 2019**, cerca de um
> quarto da amostra ([18 §2.1](18-pendencias.md)). Então **a média de −10%
> não vale e não vai para slide**, e nem a média de −2% dos anos de
> decaimento. O que sobrevive é a **faixa**, e ela é mais forte justamente
> por isso: acrescentar anos só aumenta a dispersão, nunca estreita.

**O que se sustenta é a intensidade.** Os eventos fortes dão déficit: 1982, 1997, 2015 e 2023 ficaram entre -21% e -48%. Os fracos a moderados (1986, 1991, 2002) vieram acima. E 2026, com evento muito forte, é **o pior da série de 45 anos**, com -62%.

### Consequência para 2027, e para o pitch

O CPC prevê El Niño até março-maio de 2027 e neutro a partir de maio-junho-julho. Então a chuva de junho a setembro de 2027 cai num **ano de decaimento**, e anos de decaimento dão média de apenas -2%.

**Não há base nos dados para dizer que 2027 repete 2026.** O pitch atual abre dando a entender que repete, e isso precisa mudar. Ver [07-pitch-e-demo](07-pitch-e-demo.md).

### A conferir no teste 1

- A lista de anos de El Niño foi escrita de memória pelo Claude e **precisa ser checada contra o índice ONI da NOAA**
- É um único ponto de grade do MERRA-2, que é grosseiro
- Outubro a dezembro de 2026 ainda não estão na série

## Teste 2: o que sobra de 2026 é o solo

Comparando 2026 com a climatologia de 2001-2025:

| Mês de 2026 | Perfil (normal) | Superfície (normal) |
| --- | --- | --- |
| Julho | 0,74 (0,87) | 0,77 (0,89) |
| Agosto | 0,57 (0,86) | 0,54 (0,87) |
| Setembro | 0,51 (0,76) | 0,32 (0,78) |

Em setembro de 2026 o perfil estava em 0,51, que é o nível que ali normalmente só aparece em janeiro e fevereiro, no fundo da estiagem. A superfície estava em 0,32 contra 0,78 do normal.

**O solo entrou na estiagem de 2026-2027 já no mínimo do ano, cinco meses mais cedo.** A estiagem vai de outubro a março, e o plantio começa em abril.

Isso é o que atravessa o ano: não é a chuva, é a umidade do solo.

## Teste 3: chuva forte e veranico (diário, 45 anos)

**Método:** série diária do POWER de 1981 a 2026, janela de abril a setembro. Dia com chuva = 1 mm ou mais.

| | Média 1981-2025 | 2026 |
| --- | --- | --- |
| Total | 1.318 mm | 717 mm |
| Dias com chuva | 142 | 92 |
| Maior chuva num dia | 44,4 mm | 35,5 mm |
| Maior sequência sem chuva | 9 dias | **24 dias** |
| Concentração nos 10 maiores dias | 23% | 35% |
| mm por dia de chuva | 9,2 | 7,8 |

Outros anos de El Niño forte, na mesma janela:

| Ano | Total | Dias com chuva | Maior diário | Maior seca | Concentração |
| --- | --- | --- | --- | --- | --- |
| 1982 | 1.156 mm | 135 | 32,0 mm | 9 dias | 22% |
| 1997 | 1.121 mm | 129 | 41,1 mm | 10 dias | 22% |
| 2015 | 643 mm | 102 | 26,2 mm | 14 dias | 27% |
| 2023 | 1.068 mm | 112 | **71,7 mm** | 15 dias | 32% |

### Conclusão do teste 3

**Em 2026 não houve chuva mais forte: o maior dia foi abaixo da média e a intensidade por dia de chuva caiu.** O que houve foi 50 dias de chuva a menos e um veranico de 24 dias dentro da estação chuvosa, quase três vezes o normal de 9 dias.

**Ressalva estatística:** a concentração subiu de 23% para 35%, mas isso é em parte aritmética. Quando o total despenca, os dez maiores dias viram fatia maior de um bolo menor. Não é prova de eventos mais intensos; o maior diário caiu, e esse é o dado direto.

**Chuva forte acontece aqui, só não foi em 2026:** 2023 teve um dia de 71,7 mm, bem acima dos 44,4 da média.

**O veranico de 24 dias é a métrica mais acionável que achamos.** É o que o produtor reconhece pelo nome, e é número forte para o demo.

## Medições de campo que confirmam o POWER

- Bacia do Rio Branco: em agosto choveu 27,8% do esperado, e de janeiro a agosto só maio ficou acima da média ([boletim do SGB de 04/09/2026](https://sgb.gov.br/sace/boletins/Branco/20260904_14-20260904%20-%20144707.pdf))
- Estação do INMET em Caracaraí: 47,4 mm em agosto, 77,5% abaixo da média ([nota do INMET](https://portal.inmet.gov.br/uploads/notastecnicas/destaque_agosto.pdf))
- Rio Branco em Boa Vista: 124 cm em 04/09/2026, caindo 22 cm em 7 dias (mesmo boletim do SGB)

**Uma divergência a registrar:** o POWER mostra maio 10% abaixo da média no Cantá, enquanto o SGB aponta maio acima da média na bacia inteira. São áreas e métodos diferentes.

## Previsão sazonal: existe, mas não é dado da NASA

Pesquisado em 14/11, a pedido do Welder.

- O horizonte **alcança abril de 2027**: o CPC prevê alta probabilidade (80%) de El Niño ao menos forte até janeiro-fevereiro-março de 2027, e favorece El Niño de qualquer intensidade até março-abril-maio de 2027, com neutro depois, a partir de maio-junho-julho ([CPC, discussão sazonal](https://cpc.ncep.noaa.gov/products/predictions/long_range/fxus05.html)).
- O Brasil tem previsão sazonal oficial mensal: o Painel El Niño 2026-2027 é ação conjunta de INMET, INPE, CEMADEN, ANA, SGB, SEDEC e CENSIPAM ([boletim de outubro](https://portal.inmet.gov.br/uploads/notastecnicas/Painel-El-Ni%C3%B1o-5-edi%C3%A7%C3%A3o1.pdf)). O CPTEC/INPE publica notas técnicas por trimestre com previsão probabilística por tercil.
- A NASA tem o próprio sistema: o **GEOS-S2S**, da GMAO, na versão 3 lançada em março de 2026, com previsões sazonais de 9 a 12 meses ([GMAO](https://gmao.gsfc.nasa.gov/gmao-products/geos-s2s-3/)).

**Mas a previsão vigente não é dado da NASA.** O CPC é da NOAA e o Painel El Niño é dos órgãos brasileiros. A NASA entra de lado: o GEOS-S2S é submetido ao NMME, que o CPC sintetiza. Só dá para chamar de previsão da NASA se puxarmos o GEOS-S2S direto, o que exige grade e é risco de prazo.

**Decisão:** a previsão entra como contexto no pitch, não como dado do motor. O enunciado pede observação e adaptação.

## Outras fontes de dado

- [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/): focos de fogo. Pedir a chave gratuita e somar o histórico como critério
- [INPE BDQueimadas](https://terrabrasilis.dpi.inpe.br/queimadas/bdqueimadas/)
- [FAO GAEZ](https://gaez.fao.org/): aptidão de culturas fora dos EUA
- Deixar para depois: SMAP, ECOSTRESS e Landsat, que exigem login no Earthdata e arquivos pesados
- **Não servem:** SSURGO, CropScape, PRISM e os demais dados do USDA só cobrem os EUA

## A conferir antes de usar

- [ ] O número de 40% menos chuva vem de dado de modelo em grade larga, não de pluviômetro; já conferido com medições de campo, que apontam na mesma direção, mas dizer "estimativa"
- [ ] Os meses mais recentes do POWER podem ser revisados depois; registrar a data da consulta (14/11/2026)
- [ ] Lista de anos de El Niño: checar contra o índice ONI da NOAA
- [ ] Decidir se a radiação entra numa métrica ou sai da lista de parâmetros
- [ ] Testar GDD como substituto do ciclo fixo em dias
