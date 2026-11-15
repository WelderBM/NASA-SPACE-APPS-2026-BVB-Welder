# Space Apps 2026: recomendações e fontes

Documento de trabalho do time para o NASA Space Apps 2026 (desafio *Field Shift: Adapting Farms with NASA Data*).

Data de referência: 14/11/2026. Responsável: Welder.

Organizado na ordem do design thinking, do início ao fim do hackathon. Cada fase abre com um clique. Dentro dela, as tarefas e fontes ficam juntas.

## Decisões até agora

- Foco: interior de Roraima, com a persona de quem usa WhatsApp (conversa do time, 14/11).
- Interface: WhatsApp como intermediário, preferencialmente. Site, app e robô ficam como alternativas em aberto (conversa do time, 14/11).
- Base de conhecimento separada do canal: dados, análises e fontes ficam isolados, para que qualquer interface use o mesmo conteúdo (conversa do time, 14/11).
- Em aberto: bot que responde por áudio. A pesquisa mostra uso alto de áudio no Brasil, mas não há dado para Roraima (ver seção "Persona do WhatsApp").
- Em aberto: definição das personas. Aguarda a conversa do time e as respostas do formulário.

## Como o enunciado divide o produto

O desafio pede uma ferramenta de apoio à decisão que use observações da Terra da NASA, juntamente com informações locais sobre o solo, características das culturas e prioridades dos agricultores, para explorar estratégias de rotação que fortaleçam a saúde do solo e adaptem a propriedade às mudanças climáticas.

A palavra "juntamente" divide o trabalho em duas camadas. A observação da Terra vem da NASA: chuva, temperatura e umidade do solo. Solo, culturas e prioridades são a camada local, e não precisam ser dado da NASA; um perfil típico de Roraima pela Embrapa já atende "informações locais sobre o solo".

O enunciado pede observação e adaptação, não previsão. Anos análogos de El Niño são observação: dado passado do mesmo lugar usado para decidir o próximo plantio. A previsão sazonal oficial entra como contexto no pitch, não como dado do motor, e não é dado da NASA: o CPC é da NOAA e o Painel El Niño é do INMET, INPE, CEMADEN, ANA, SGB, SEDEC e CENSIPAM. O GEOS-S2S, da NASA, alimenta o NMME que o CPC sintetiza, então só dá para chamar de previsão da NASA se puxarmos o GEOS-S2S direto.

<details>
<summary><b>1. Imersão: entender o problema</b></summary>

### Contexto para o pitch

O El Niño de 2026 é um dos mais fortes já medidos, e Roraima foi o primeiro estado do Norte a sentir: a Embrapa estima perda de 30% a 50% na safra de 2026.

| Fato | Número | Fonte |
| --- | --- | --- |
| Força do El Niño | Índice RONI de 2,0 °C em agosto a outubro; evento forte a muito forte previsto até janeiro a março de 2027 | [The Watchers, com dados do CPC/NOAA](https://watchers.news/2026/11/10/el-nino-2026-roni-2-0-behind-1997-record-forecast/) |
| Status oficial | El Niño Advisory, com mais de 83% de chance de evento forte a muito forte | [NOAA Coral Reef Watch](https://www.coralreefwatch.noaa.gov/satellite/analyses_guidance/enso_current_conditions.php) |
| Safra de Roraima em 2026 | Perda estimada de 30% a 50% | [Portal Amazônia](https://portalamazonia.com/economia/seca-el-nino-safra-roraima/) |
| Quando a chuva cortou | Já em julho de 2026, no enchimento dos grãos | [Brasil 61](https://brasil61.com/n/el-nino-gestao-da-agua-e-essencial-para-enfrentar-irregularidade-das-chuvas-na-regiao-norte-bras2617300) |
| Soja | Safra pela metade, prejuízo estimado em R$ 2 bilhões, segundo a Aprosoja-RR | [Portal Amazônia](https://portalamazonia.com/economia/seca-el-nino-safra-roraima/) |
| Agricultura familiar | Seca parou a produção de farinha de um produtor em Iracema | [Portal Amazônia](https://portalamazonia.com/economia/seca-roraima-afeta-farinha/) |
| Fogo | Aumento de queimadas esperado entre dezembro de 2026 e abril de 2027 | [Folha BV](https://www.folhabv.com.br/?p=657443) |
| Resposta nacional | Embrapa entregou ao Mapa 163 medidas de gestão de risco climático | [Revista Cultivar](https://revistacultivar.com.br/noticias/embrapa-propoe-163-medidas-para-gestao-de-riscos-climaticos) |

Abrir com a orientação da Embrapa: não planejar só pelo calendário tradicional ([Folha BV](https://www.folhabv.com.br/?p=676921)).

### Persona do WhatsApp: dados do interior de Roraima (pesquisa de 14/11/2026)

Dados gerais e de órgãos públicos. Nenhum deles mede o uso de WhatsApp ou de áudio pelo produtor do interior; isso ainda depende da pesquisa de campo.

- Produtores atendidos: o IATER acompanha 50.192 produtores, sendo 43.192 agricultores familiares e cerca de 7 mil indígenas. A regional de Alto Alegre, Amajari e Boa Vista concentra 23.455 familiares ([Assembleia Legislativa de Roraima, set/2026](https://al.rr.leg.br/2026/09/21/economia-e-desenvolvimento/)).
- Assistência técnica: num documento de convênio de março de 2024, o IATER registra 16.850 estabelecimentos, e 87% deles não recebiam assistência técnica ([IATER, proposta de convênio](https://prda.sudam.gov.br/pdf/80bff30c20fcfd50e68aaebbd52cdf26.pdf)).
- Produção: leite, milho, cacau, café, mandioca e feijão são os principais produtos ([Assembleia Legislativa de Roraima](https://al.rr.leg.br/2026/09/21/economia-e-desenvolvimento/)). Em Cantá e Iracema, a farinha de mandioca tem a maior saída ([Folha BV](https://www.folhabv.com.br/?p=24419)).
- Cacau: o primeiro polo de Roraima começou em Caroebe, com 500 agricultores familiares, e deve se estender a São João da Baliza, Rorainópolis e Caracaraí ([Folha BV](https://www.folhabv.com.br/?p=43195)).
- Celular e internet: em 2015, mais de 98% do acesso à internet em Roraima era feito pelo celular, mas só 6,1% dos moradores rurais usaram internet nos três meses anteriores à pesquisa. É um dado antigo ([Folha BV](https://www.folhabv.com.br/?p=23793); [UERR](https://periodicos.uerr.edu.br/index.php/ambiente/article/download/866/560/2838)).
- Cobertura: oito localidades rurais de Roraima ganharam sinal 4G nos últimos três anos ([Brasil 61](https://brasil61.com/n/expansao-do-4g-no-campo-roraima-soma-mais-oito-localidades-conectadas-mcom260414)). A Anatel aponta qualidade abaixo do mínimo em Alto Alegre, Caracaraí e Pacaraima ([Folha BV](https://www.folhabv.com.br/?p=93188)), e a fibra ainda não chega a alguns municípios do interior ([Folha BV](https://www.folhabv.com.br/?p=94305)).
- Pontos de acesso: há internet pública do programa Gesac em escolas, unidades de saúde e praças de quatro municípios do interior ([Folha BV](https://www.folhabv.com.br/?p=76731)). Houve anúncio de internet nas Casas do Produtor Rural em Rorainópolis, mas a data é antiga ([Folha BV](https://www.folhabv.com.br/?p=25596)).
- WhatsApp: em pesquisa nacional, 96% dos produtores usam o WhatsApp para consultar decisões de negócio ([Canal Rural](https://www.canalrural.com.br/agricultura/quase-100-das-propriedades-rurais-conta-com-internet-mostra-pesquisa/)). Na pesquisa ABMRA 2025, 61% usam o YouTube para orientação técnica ([Forbes Agro](https://forbes.com.br/forbesagro/2025/09/internet-atinge-98-das-propriedades-e-whatsapp-vira-principal-canal-do-agro-diz-nova-pesquisa-abmra/)).
- Áudio no Brasil (não é dado de Roraima): em 2024, 80% dos usuários mensais trocavam áudio, contra 86% que trocavam texto ([Voxbooster, com dados do Panorama Mobile Time/Opinion Box](https://voxbooster.com/pt-BR/blog/voice-message-vs-text-preference-country-statistics-2026/)). Em outra pesquisa, 56% disseram gostar e preferir enviar áudio ([Mobile Time, com dados Exame/MindMiners](https://www.mobiletime.com.br/?p=695702)).
- Precedente: um livro de 2025 sobre extensão rural propõe um método para produzir e enviar áudios de WhatsApp a produtores ([Zenodo](https://zenodo.org/records/14995584)).
- Canal de apoio técnico já existente: o RAImundo, da Embrapa, oferece orientação por WhatsApp a pequenos e médios produtores, inclusive com baixa conectividade ([LexLegal](https://lexlegal.com.br/?p=28389)).

Ainda sem dado:

- Número de estabelecimentos de agricultura familiar por município do interior (tabela 6778 do SIDRA, ou Censo 2017).
- Uso de WhatsApp e de áudio pelo produtor do interior de Roraima.
- Perfil do pecuarista familiar de Roraima.

### Pesquisa com produtores: o que cada resposta decide

O formulário "Como a sua família decide o que plantar?" está pronto, com 13 perguntas. Link de edição: [abrir para editar](https://docs.google.com/forms/d/1g9mkbGMVdfErK_ww15vlBKYNFtulgBS2pxtbsYoKbNo/edit).

O que cada resposta decide: as perguntas sobre produção e perdas definem público e problema; a da área depois da colheita mostra se já existe rotação; internet, quem lê o celular e canal preferido escolhem a interface; a da confiança em satélite diz se o técnico precisa estar no fluxo.

</details>

<details>
<summary><b>2. Análise: organizar os dados</b></summary>

### Dados da NASA

O NASA POWER já foi testado para o Cantá (lat 2,61, lon -60,60) e mostra que de janeiro a outubro de 2026 choveu 858 mm, contra 1.428 mm da média histórica: 40% a menos.

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

A estação chuvosa começou perto do normal e acabou cedo: agosto e setembro somaram 34 mm, contra 268 mm da média. A máxima média de setembro foi 39,6 °C.

- [ ] Usar o NASA POWER como medida de adaptação, comparando a chuva de 2026 com a climatologia, e não como previsão: não exige login, devolve JSON por coordenada e funciona no mundo todo ([site](https://power.larc.nasa.gov/))
- [ ] Mostrar que o teste do POWER (julho com 54% menos chuva) bate com o relato da Embrapa de corte das chuvas em julho; isso é validação
- [ ] Mostrar o dado da NASA ao lado do sinal que o produtor já usa para prever a chuva
- [ ] Usar e declarar pelo menos um dado da NASA

Endereços usados no teste: clima médio em `https://power.larc.nasa.gov/api/temporal/climatology/point` e diário em `https://power.larc.nasa.gov/api/temporal/daily/point`, com `parameters=PRECTOTCORR,T2M_MAX&community=AG&longitude=-60.60&latitude=2.61&format=JSON`. O diário pede também `start` e `end` no formato AAAAMMDD.

### Umidade do solo pelo POWER (confirmado em 14/11/2026)

O POWER entrega umidade do solo pela mesma API, sem login, na comunidade AG: `GWETTOP` (superfície), `GWETROOT` (zona de raiz) e `GWETPROF` (perfil), em fração de 0 a 1. A fonte é o MERRA-2 e a climatologia disponível é de 25 anos, de janeiro de 2001 a dezembro de 2025. Isso resolve a parte de observação de solo que o enunciado pede.

Valores para o Cantá (lat 2,61, lon -60,60):

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

Como ler: o solo mais seco é em fevereiro e março, e o mais úmido em julho. A safra começa em abril, quando a superfície está em 0,54 e subindo. Isso casa com a regra da mandioca: ela é sensível ao déficit de água nos três primeiros meses, e plantada em abril a fase crítica cai justamente nos meses mais úmidos.

A conferir: a climatologia de umidade do solo é de 2001 a 2025, e a de chuva que usamos na tabela acima pode ter outro período-base. Registrar o período de cada consulta antes de comparar os dois.

### Teste dos anos de El Niño (rodado em 14/11/2026)

Testamos se ano de El Niño é ano seco no Cantá, usando a série mensal do POWER de 1981 a 2026 e somando junho a setembro, que é o fim da estação chuvosa e o enchimento dos grãos. Média da série: 859 mm. Atenção, a API mensal devolve mm/dia, não mm do mês; os valores abaixo já foram multiplicados pelos dias de cada mês.

Anos em que o El Niño estava ativo em junho-setembro:

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
| 2026 | 330 | -62% |

O que isso diz: a média desses anos é só 10% abaixo do normal, então "ano de El Niño" sozinho não serve de regra. Mas o déficit aparece nos eventos fortes: 1982, 1997, 2015 e 2023 foram de -21% a -48%, e 2026, com evento muito forte, é o pior da série de 45 anos, com -62%. Os eventos fracos a moderados (1986, 1991, 2002) vieram acima da média. A regra honesta é pela intensidade, não pela presença do fenômeno.

Anos seguintes ao pico, de decaimento, dão média de apenas 2% abaixo do normal. Isso importa para 2027: o CPC prevê El Niño até março-maio de 2027 e neutro a partir de maio-junho-julho, ou seja, a chuva de junho a setembro de 2027 cai num ano de decaimento. Pelos dados, **não há base para dizer que 2027 repete 2026**. Dizer isso no pitch seria errado.

### O que realmente sobra de 2026: o solo

O que atravessa o ano não é a chuva, é a umidade do solo. Comparando 2026 com a climatologia de 2001 a 2025:

| Mês de 2026 | Perfil (normal) | Superfície (normal) |
| --- | --- | --- |
| Julho | 0,74 (0,87) | 0,77 (0,89) |
| Agosto | 0,57 (0,86) | 0,54 (0,87) |
| Setembro | 0,51 (0,76) | 0,32 (0,78) |

Em setembro de 2026 o perfil estava em 0,51, que é o nível que ali normalmente só aparece em janeiro e fevereiro, no fundo da estiagem. A superfície estava em 0,32 contra 0,78 do normal. Em outras palavras: **o solo entrou na estiagem de 2026-2027 já no mínimo do ano, cinco meses mais cedo**. A estiagem vai de outubro a março, e o plantio começa em abril.

Isso reposiciona o produto, e deixa ele mais próximo do enunciado: a pergunta não é se vai faltar chuva em 2027, é qual rotação recupera um solo que começa seco e aguenta um início ruim. É adaptação e saúde do solo, com observação da NASA, que é exatamente o que foi pedido. E casa com a regra da mandioca, sensível ao déficit nos três primeiros meses, justo quando o solo estiver recarregando de uma base baixa.

A conferir neste teste: a lista de anos de El Niño foi escrita de memória e precisa ser checada contra o índice ONI da NOAA; é um único ponto de grade do MERRA-2, que é grosseiro; outubro a dezembro de 2026 ainda não estão na série.

### Medições de campo que confirmam o dado do NASA POWER

Medições de campo que confirmam o dado do NASA POWER (que deu agosto 85% abaixo da média no Cantá):

- Bacia do Rio Branco: em agosto choveu 27,8% do esperado, e de janeiro a agosto só maio ficou acima da média ([boletim do SGB de 04/09/2026](https://sgb.gov.br/sace/boletins/Branco/20260904_14-20260904%20-%20144707.pdf))
- Estação do INMET em Caracaraí: 47,4 mm em agosto, 77,5% abaixo da média ([nota do INMET](https://portal.inmet.gov.br/uploads/notastecnicas/destaque_agosto.pdf))
- Rio Branco em Boa Vista: 124 cm em 04/09/2026, caindo 22 cm em 7 dias (mesmo boletim do SGB)
- Produtores indígenas: 33,63% dos produtores de Roraima, a maior proporção entre os estados ([IBGE](https://agenciadenoticias.ibge.gov.br/en/agencia-news/35880-indigenous-population-has-diversified-agricultural-production-with-a-majority-of-women-producers-and-less-pesticide-use.html))

Uma diferença a registrar: o POWER mostra maio 10% abaixo da média no Cantá, enquanto o SGB aponta maio acima da média na bacia inteira. São áreas e métodos diferentes.

### Base agronômica

O ZARC, do Ministério da Agricultura, já diz por município, solo e cultura em que decêndio o plantio tem risco de 20%, 30% ou 40%. Roraima tem ZARC para arroz, feijão-caupi, mandioca, milho, soja, milho com braquiária e sorgo, entre outras.

- [ ] Baixar no Painel de Indicação de Riscos do ZARC (ou no app Plantio Certo) as janelas do Cantá e de Boa Vista
- [ ] Fechar a tabela de 6 a 8 culturas com ciclo, água, janela de plantio e papel na rotação

| Cultura | Ciclo | Água no ciclo | Papel na rotação | Fonte |
| --- | --- | --- | --- | --- |
| Soja | 100 a 130 dias | 450 a 800 mm | Fixa nitrogênio, base da rotação | [ZARC soja 2026/27](https://www.gov.br/agricultura/pt-br/assuntos/riscos-seguro/programa-nacional-de-zoneamento-agricola-de-risco-climatico/portarias/safra-vigente/roraima/PORTN208SOJARR.ret.pdf) |
| Feijão-caupi | até 75 dias | mínimo de 300 mm | Leguminosa curta, cabe no fim das chuvas | [ZARC caupi](https://www.gov.br/agricultura/pt-br/assuntos/riscos-seguro/programa-nacional-de-zoneamento-agricola-de-risco-climatico/portarias/safra-vigente/roraima/PORTN291FEIJOCAUPIRR.pdf) |
| Milho | 100 a 140 dias | 500 a 800 mm | Safrinha depois da soja | [Folha BV](https://www.folhabv.com.br/?p=450615) |
| Milheto | a levantar | baixa | Cobertura do solo no plantio direto | [Embrapa Roraima](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/694835/1/052008milhetosmiderle.pdf) |
| Braquiária | perene | baixa | Cobertura e pasto após o milho | [Embrapa Roraima](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1029660/1/CIT136N07.pdf) |
| Feijão-guandu | a levantar | baixa | Cobertura e leguminosa | [Embrapa Roraima](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1029660/1/CIT136N07.pdf) |
| Mandioca | 8 a 12 meses; 18 a 24 onde a seca é prolongada | tolerante à seca, crítica nos 3 primeiros meses | Segurança alimentar: a raiz pode esperar no campo | [Embrapa](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1152564/1/Fisiologia-da-mandioca.pdf) |

Limiares para regras no código: caupi vai bem entre 18 °C e 34 °C e perde mais com falta de água na floração; soja sofre acima de 40 °C e consome 7 a 8 mm por dia na floração e no enchimento de grãos.

Mandioca para as regras do código: resiste a períodos de seca, mas é muito sensível ao déficit de água no solo nos três primeiros meses depois do plantio ([Embrapa Cerrados, Circular técnica 51](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1133613/1/Recomendacao-tecnica-do-manejo-de-irrigacao-Circular-tecnica-51.pdf)), e os efeitos negativos seguem altos nos quatro meses seguintes, quando o crescimento vegetativo é mais intenso; em ciclo de 12 meses a fase crítica vai do dia 30 ao dia 150 ([Embrapa Mandioca e Fruticultura, Comunicado técnico 172](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1121941/1/ComunicadoTecnico172-Mauricio-Coelho-AINFO-2.pdf)). No trópico úmido as raízes podem ser colhidas entre 6 e 7 meses, e podem ficar no campo sem colher por muito tempo, o que faz da mandioca um cultivo de segurança contra a fome ([Embrapa, Fisiologia da mandioca](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1152564/1/Fisiologia-da-mandioca.pdf)). A literatura também registra o uso de cultivar precoce para fechar o ciclo antes de a seca se estabelecer.

### A conferir antes de usar

Nenhum destes pontos deve ir para slide ou código sem checagem na fonte original.

- [ ] Janelas do feijão-caupi para Cantá e Boa Vista: a tabela do PDF veio desalinhada; caem aproximadamente entre o fim de junho e meados de agosto
- [ ] A portaria do caupi lida é da safra 2023/2024; ver se há mais nova
- [ ] O número de 40% menos chuva vem de dado de modelo em grade larga (NASA POWER), não de pluviômetro; já conferido com medições de campo, que apontam na mesma direção (ver Contexto para o pitch); mesmo assim, dizer "estimativa"
- [ ] Os meses mais recentes do POWER podem ser revisados depois; registrar a data da consulta (14/11/2026)
- [ ] O chat do Giuliano diz que "o desafio cita a baixa qualidade da pastagem nativa"; o texto do desafio não diz isso, a informação veio de uma matéria
- [ ] "33,5% de produtores indígenas" e "queda de 30% a 50% na safra 2026": a queda de 30% a 50% está confirmada em matérias que citam a nota técnica da Embrapa (ver Contexto para o pitch); o dado dos produtores indígenas está confirmado no IBGE, Censo Agro 2017: 33,63% dos produtores de Roraima, a maior proporção do país
- [ ] Limiares de alerta no código (temperatura, anomalia de chuva): marcar como "a validar com agrônomo"
- [ ] Espécies e cultivares recomendadas: validar com a Embrapa Roraima ou um técnico local
- [ ] Regra sobre código pré-existente: não há texto explícito nos guias; confirmar com o líder local

### Em aberto depois da busca de 14/11

- [ ] Número de estabelecimentos de agricultura familiar em Roraima: não achei em página aberta; consultar a tabela 6778 do SIDRA/IBGE
- [ ] Janelas de plantio por município: as portarias do ZARC não trazem mais essa tabela; só o Painel de Indicação de Riscos e o app Plantio Certo
- [ ] Nota técnica original da Embrapa para o Norte: só achei matérias que a citam
- [ ] Nome AgroDeal: a busca não mostrou produto com esse nome, mas isso não garante que esteja livre; checar domínio e INPI
- [ ] Buscar no Censo Agro do IBGE o número de estabelecimentos de agricultura familiar em Roraima; ainda não encontrado
- [ ] Ler a nota técnica original da Embrapa para a Região Norte e citar ela, não só as matérias

</details>

<details>
<summary><b>3. Ponto de vista: definir o problema</b></summary>

- [ ] Fechar a frase do problema e não mudar mais: "Como ajudar uma família produtora de Roraima a escolher qual rotação protege o solo e aguenta a seca, segundo as prioridades da família, com uma informação que chegue até ela?"
- [ ] Ligar a ferramenta à próxima decisão real: a seca vai até março e o plantio de 2027 começa em abril
- [ ] Usar a frase de um produtor de soja: ninguém previu que a chuva ia cortar tão cedo ([Portal Amazônia](https://portalamazonia.com/economia/seca-queda-colheita-soja-rr/)). O dado do NASA POWER para o Cantá já mostrava junho 38% abaixo da média
- [ ] Usar um caso real do interior de Roraima, como o Cantá, em vez de um campo genérico
- [ ] Declarar os limites: o que é estimativa de satélite, o que falta validar em campo, incluindo a falta de levantamento de solo do Cantá

Fontes de contexto para o problema:

- [Field Shift](https://www.spaceappschallenge.org/2026/challenges/adapting-farms-with-nasa-data/) (desafio e aba Resources)
- [Portal Amazônia: seca afeta produção de farinha](https://portalamazonia.com/economia/seca-roraima-afeta-farinha/)
- [Portal Amazônia: seca reduz safra de Roraima em até 50%](https://portalamazonia.com/economia/seca-el-nino-safra-roraima/)

</details>

<details>
<summary><b>4. Ideação: desenhar a solução</b></summary>

O núcleo que cabe até domingo: comparar a rotação atual com duas alternativas, usando dados do NASA POWER, e explicar o resultado num áudio de WhatsApp.

- [ ] Tratar como rotação, e não como recomendação de uma cultura solta: partir do que a pessoa já planta e comparar pelo menos 3 estratégias, incluindo a atual
- [ ] Para cada estratégia, mostrar: por que foi sugerida, a evidência, o benefício, o que falta de dado e o risco a revisar com técnico
- [ ] Incluir solo como critério: cobertura, fixação de nitrogênio (soja e caupi), resíduo na superfície e exposição à erosão ou ao fogo. Sem dado local, usar um perfil típico de Roraima, marcado como "a validar com a Embrapa"
- [ ] Posicionar como "ZARC atualizado com o clima deste ano": a janela oficial é fixa, o dado da NASA mostra como o ano atual está fugindo dela
- [ ] Usar fogo e seca como critérios da comparação, não como produtos separados
- [ ] Incluir a rotação milho com braquiária, que une lavoura e pasto e resolve a dúvida entre agricultor e pecuarista
- [ ] Desenhar para o "intermediário digital da família": o filho ou neto que recebe o áudio e mostra para quem decide
- [ ] Manter em todas as telas e áudios: apoia a decisão, não substitui o agricultor nem o técnico
- [ ] Tratar El Niño como contexto que justifica a ferramenta, não como centro do produto; manter na abertura do pitch como urgência
- [ ] Decidir hoje entre lavoura e pasto com as respostas do formulário; sem respostas, decidir pelo que a equipe conhece de perto
- [ ] Usar o formulário para mostrar que as prioridades são reais (renda, pasto, risco, mão de obra); a família escolhe as prioridades dentro da ferramenta, e o formulário não as alimenta
- [ ] Parar de gerar ideias novas

Rotações reais de Roraima para as 3 estratégias:

1. Soja, depois milho ou milheto como safrinha
2. Soja, milho e feijão-caupi em sequência
3. Milho consorciado com braquiária, que vira pasto depois da colheita

A safra começa em abril. Um estudo da UFRR na savana concluiu que plantio direto com rotação é alternativa viável para a região ([registro](https://oasisbr.ibict.br/vufind/Record/UFRR-6_4713f65ec21a05349571ac11adae8852)).

Cortar do núcleo e deixar como próximos passos: o robô Buddy, os sensores como centro, o mercúrio do garimpo, a API oficial do WhatsApp, SMAP, ECOSTRESS e Landsat.

### Saúde do solo como saída

O enunciado pede fortalecer a saúde do solo, então a comparação precisa mostrar, por estratégia, o que acontece com o solo. Tudo qualitativo, a validar com a Embrapa Roraima:

- Cobertura: quantos meses do ano o solo fica coberto naquela estratégia
- Fixação de nitrogênio: soja, caupi e guandu fixam; milho e mandioca não
- Resíduo na superfície: milheto e braquiária deixam palha; mandioca deixa pouco
- Exposição à erosão e ao fogo: solo descoberto na seca é o pior caso
- Ocupação da área: a mandioca fica 8 a 12 meses no campo, o que fecha as janelas para outra cultura no período

</details>

<details>
<summary><b>5. Protótipo: construir a ferramenta</b></summary>

- [ ] Usar frases fixas preenchidas com os números do motor; o robô ou o áudio nunca inventa texto
- [ ] Chamar a API por um backend com cache, e não direto do navegador do usuário
- [ ] Parâmetros: PRECTOTCORR (chuva), T2M_MAX e T2M_MIN (temperatura), ALLSKY_SFC_SW_DWN (radiação)
- [ ] Pedir a chave gratuita do FIRMS e somar o histórico de focos de fogo como critério ([FIRMS](https://firms.modaps.eosdis.nasa.gov/))
- [ ] Usar o FAO GAEZ para aptidão de culturas fora dos EUA ([GAEZ](https://gaez.fao.org/))
- [ ] Se sobrar tempo: camada de NDVI ou de chuva IMERG no mapa e controle "e se chover 20% menos?"
- [ ] Deixar SMAP, ECOSTRESS e Landsat para depois; exigem login no Earthdata e arquivos pesados
- [ ] Lembrar que SSURGO, CropScape, PRISM e os demais dados do USDA só cobrem os EUA
- [ ] Limiares de alerta no código: marcar como "a validar com agrônomo"

</details>

<details>
<summary><b>6. Testes: validar com as pessoas</b></summary>

- [ ] Publicar o formulário e disparar com o texto de WhatsApp
- [ ] Mandar para produtores e também para familiares; a pergunta 1 separa os grupos
- [ ] Aplicar por ligação ou áudio com quem não usa formulário, preenchendo vocês mesmos; senão a amostra só terá quem já usa tecnologia
- [ ] Fazer 3 ligações de 10 minutos com quem planta, em paralelo ao formulário
- [ ] Buscar gente nos contatos do Cantá, grupos de produtores, cooperativas, feira do produtor e técnicos de extensão
- [ ] Meta: 10 a 15 respostas e 3 conversas
- [ ] Gravar um áudio de 30 segundos como o sistema mandaria, enviar a 5 pessoas avisando que é exemplo e perguntar só "o que você faria com isso?"
- [ ] Pedir consentimento antes de gravar conversa e não publicar nomes
- [ ] Mostrar a reação de quem recebeu o áudio de teste; é o slide mais forte

</details>

<details>
<summary><b>7. Entrega: submissão e pitch</b></summary>

### Prazo e regras

A submissão fecha domingo, 15/11, às 22h59 de Boa Vista. Fonte das regras: [Project Submission Guide](https://www.spaceappschallenge.org/resources/project-submission-guide/), [Judging & Awards Guide](https://www.spaceappschallenge.org/resources/judging-awards-guide/) e [Participant FAQs](https://www.spaceappschallenge.org/resources/participant-faqs/).

- [ ] Submeter cedo uma versão simples e ir reenviando; só a última versão salva conta
- [ ] Perguntar ao líder local se a banca de Boa Vista tem horário próprio
- [x] Decidido pelo time em 14/11: nada feito antes do hackathon entra no projeto, incluindo o Buddy
- [ ] Demo: vídeo de até 30 segundos ou até 7 slides (contando título e introdução). Passar do limite tira do julgamento global
- [ ] Escrever em inglês a página do projeto e todo material linkado. Vídeo pode ser em português com legenda em inglês; slides só em inglês
- [ ] Testar todos os links em aba anônima; nada pode pedir login ou permissão
- [ ] Listar no campo de referências todo código, texto e imagem de terceiros, incluindo o Buddy
- [ ] Marcar o que foi gerado por IA: marca d'água em imagem e vídeo, aviso em texto para áudio e código. Vale para voz sintética
- [ ] Não usar logo nem identidade da NASA em conteúdo gerado
- [ ] Nenhuma imagem ou voz de menor de 18 anos no demo
- [ ] Conferir que todos do time (máximo 6) estão inscritos no mesmo evento local

Critérios de julgamento, nota de 1 a 5 em cada: Impacto, Criatividade, Validade, Relevância e Apresentação. Entre os dez prêmios globais, o Local Impact Award é o que mais combina com um projeto para agricultores de Roraima.

### Recomendações de pitch e demo

Abrir com o alerta da Embrapa sobre o El Niño 2026/2027 e mostrar, com dado da NASA, que a chuva de 2026 no Cantá já ficou cerca de 40% abaixo da média.

- [ ] Usar um caso real do interior de Roraima, como o Cantá, em vez de um campo genérico
- [ ] Reescrever o pitch de 30 segundos e os 7 slides: a versão do chat do Giuliano fala de erosão e mercúrio, e o foco mudou
- [ ] Mostrar os números da pesquisa separados por grupo ("X produtores e Y familiares")
- [ ] Dar à Apresentação o mesmo peso dos outros critérios; o guia pede isso
- [ ] Citar o Local Impact Award como o prêmio que o projeto mira
- [ ] Deixar robô, sensores e WhatsApp oficial só no último slide, como próximos passos

Roteiro do vídeo sugerido pelo guia: apresentação do time (2 s), desafio e inspiração (3 s), nome e slogan (5 s), como funciona e como usa dados da NASA (10 s), visão de futuro (10 s).

</details>

<details>
<summary><b>Fontes</b></summary>

Páginas abertas e lidas em 14/11/2026.

**Desafio e regras**
- [Field Shift: Adapting Farms with NASA Data](https://www.spaceappschallenge.org/2026/challenges/adapting-farms-with-nasa-data/) (desafio e aba Resources)
- [Participant FAQs](https://www.spaceappschallenge.org/resources/participant-faqs/)
- [Project Submission Guide](https://www.spaceappschallenge.org/resources/project-submission-guide/)
- [Judging & Awards Guide](https://www.spaceappschallenge.org/resources/judging-awards-guide/)

**Dados**
- [NASA POWER](https://power.larc.nasa.gov/)
- [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/)
- [INPE BDQueimadas](https://terrabrasilis.dpi.inpe.br/queimadas/bdqueimadas/)
- [FAO GAEZ](https://gaez.fao.org/)

**Agronomia e contexto de Roraima**
- [ZARC soja Roraima 2026/2027, MAPA](https://www.gov.br/agricultura/pt-br/assuntos/riscos-seguro/programa-nacional-de-zoneamento-agricola-de-risco-climatico/portarias/safra-vigente/roraima/PORTN208SOJARR.ret.pdf)
- [ZARC feijão-caupi Roraima, MAPA](https://www.gov.br/agricultura/pt-br/assuntos/riscos-seguro/programa-nacional-de-zoneamento-agricola-de-risco-climatico/portarias/safra-vigente/roraima/PORTN291FEIJOCAUPIRR.pdf)
- [ZARC milho com braquiária Roraima 2026/2027, MAPA](https://www.gov.br/agricultura/pt-br/assuntos/riscos-seguro/programa-nacional-de-zoneamento-agricola-de-risco-climatico/portarias/safra-vigente/roraima/PO9CAE1.PDF)
- [ZARC milho 1ª safra Roraima, MAPA](https://www.gov.br/agricultura/pt-br/assuntos/riscos-seguro/programa-nacional-de-zoneamento-agricola-de-risco-climatico/portarias/2024-2025/roraima-rr/PO15351.PDF)
- [Embrapa Roraima: plantas de cobertura para plantio direto](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1029660/1/CIT136N07.pdf)
- [Embrapa Roraima: milheto como cobertura](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/694835/1/052008milhetosmiderle.pdf)
- [UFRR: qualidade do solo em plantio direto e rotação na savana](https://oasisbr.ibict.br/vufind/Record/UFRR-6_4713f65ec21a05349571ac11adae8852)
- [Folha BV: Embrapa e o El Niño 2026/2027](https://www.folhabv.com.br/?p=676921)
- [Folha BV: rotação depois da soja](https://www.folhabv.com.br/?p=450615)
- [Folha BV: culturas com ZARC em Roraima](https://www.folhabv.com.br/?p=61194)
- [Embrapa: Fisiologia da mandioca](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1152564/1/Fisiologia-da-mandioca.pdf)
- [Embrapa Cerrados: manejo de irrigação da mandioca, Circular técnica 51](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1133613/1/Recomendacao-tecnica-do-manejo-de-irrigacao-Circular-tecnica-51.pdf)
- [Embrapa Mandioca e Fruticultura: Comunicado técnico 172](https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1121941/1/ComunicadoTecnico172-Mauricio-Coelho-AINFO-2.pdf)

**El Niño e seca de 2026**
- [NOAA Coral Reef Watch: status do ENSO](https://www.coralreefwatch.noaa.gov/satellite/analyses_guidance/enso_current_conditions.php)
- [The Watchers: El Niño 2026, RONI 2,0](https://watchers.news/2026/11/10/el-nino-2026-roni-2-0-behind-1997-record-forecast/)
- [Portal Amazônia: seca reduz safra de Roraima em até 50%](https://portalamazonia.com/economia/seca-el-nino-safra-roraima/)
- [Portal Amazônia: estratégias da Embrapa para o Norte](https://portalamazonia.com/meio-ambiente/embrapa-el-nino-estrategias-norte/)
- [Brasil 61: gestão da água no Norte](https://brasil61.com/n/el-nino-gestao-da-agua-e-essencial-para-enfrentar-irregularidade-das-chuvas-na-regiao-norte-bras2617300)
- [Portal Amazônia: seca ameaça colheita de soja](https://portalamazonia.com/economia/seca-queda-colheita-soja-rr/)
- [Portal Amazônia: seca afeta produção de farinha](https://portalamazonia.com/economia/seca-roraima-afeta-farinha/)
- [Folha BV: queimadas previstas para 2026/2027](https://www.folhabv.com.br/?p=657443)
- [Revista Cultivar: 163 medidas da Embrapa](https://revistacultivar.com.br/noticias/embrapa-propoe-163-medidas-para-gestao-de-riscos-climaticos)
- [SGB: boletim do Rio Branco, 04/09/2026](https://sgb.gov.br/sace/boletins/Branco/20260904_14-20260904%20-%20144707.pdf)
- [INMET: destaques de agosto de 2026](https://portal.inmet.gov.br/uploads/notastecnicas/destaque_agosto.pdf)
- [IBGE: produtores indígenas no Censo Agro 2017](https://agenciadenoticias.ibge.gov.br/en/agencia-news/35880-indigenous-population-has-diversified-agricultural-production-with-a-majority-of-women-producers-and-less-pesticide-use.html)

**Persona e WhatsApp**
- [Assembleia Legislativa de Roraima: agricultura familiar, set/2026](https://al.rr.leg.br/2026/09/21/economia-e-desenvolvimento/)
- [IATER: proposta de convênio, 2024](https://prda.sudam.gov.br/pdf/80bff30c20fcfd50e68aaebbd52cdf26.pdf)
- [Folha BV: farinha em Cantá e Iracema](https://www.folhabv.com.br/?p=24419)
- [Folha BV: polo de cacau em Caroebe](https://www.folhabv.com.br/?p=43195)
- [Folha BV: PNAD 2015, celular e internet](https://www.folhabv.com.br/?p=23793)
- [UERR: acesso à internet em Roraima](https://periodicos.uerr.edu.br/index.php/ambiente/article/download/866/560/2838)
- [Brasil 61: 4G no campo em Roraima](https://brasil61.com/n/expansao-do-4g-no-campo-roraima-soma-mais-oito-localidades-conectadas-mcom260414)
- [Folha BV: qualidade da internet pela Anatel](https://www.folhabv.com.br/?p=93188)
- [Folha BV: fibra no interior](https://www.folhabv.com.br/?p=94305)
- [Folha BV: Gesac em escolas e saúde](https://www.folhabv.com.br/?p=76731)
- [Folha BV: Casas do Produtor Rural](https://www.folhabv.com.br/?p=25596)
- [Canal Rural: WhatsApp e internet no campo](https://www.canalrural.com.br/agricultura/quase-100-das-propriedades-rurais-conta-com-internet-mostra-pesquisa/)
- [Forbes Agro: pesquisa ABMRA 2025](https://forbes.com.br/forbesagro/2025/09/internet-atinge-98-das-propriedades-e-whatsapp-vira-principal-canal-do-agro-diz-nova-pesquisa-abmra/)
- [Voxbooster: preferência por texto ou áudio, com dados do Panorama Mobile Time/Opinion Box](https://voxbooster.com/pt-BR/blog/voice-message-vs-text-preference-country-statistics-2026/)
- [Mobile Time: áudio no WhatsApp, com dados Exame/MindMiners](https://www.mobiletime.com.br/?p=695702)
- [Zenodo: Semeando mensagens, colhendo diálogos (livro, 2025)](https://zenodo.org/records/14995584)
- [LexLegal: RAImundo, da Embrapa](https://lexlegal.com.br/?p=28389)

**Do time**
- [Chat do Giuliano com o Claude](https://claude.ai/share/a7a1ae9d-318f-4836-b737-d47894dda415)
- [Formulário da pesquisa (edição)](https://docs.google.com/forms/d/1g9mkbGMVdfErK_ww15vlBKYNFtulgBS2pxtbsYoKbNo/edit)

</details>
