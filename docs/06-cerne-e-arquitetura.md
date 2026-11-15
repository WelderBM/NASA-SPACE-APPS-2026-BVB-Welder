# 6. Cerne e arquitetura

[Voltar ao índice](../README.md)

## Por que separar

Levantamento do Welder em 14/11: é preciso desconectar o cerne, ou backend, da interface de usuário, para que o sistema se adapte a Telegram ou outros meios, e para que ter serviços separados com integração fácil permita escalabilidade. O argumento é que a realidade local de Roraima difere da nacional e da global.

**Afinando o ponto:** o eixo que dá escalabilidade aqui **não é o canal, é o lugar.** Trocar WhatsApp por Telegram é adaptador, trabalho de um dia. O que muda de verdade entre Roraima e o resto é a camada local: aqui a lista de culturas tem mandioca, banana e cacau, no Mato Grosso teria soja e milho; as janelas do ZARC são por município; o perfil de solo é outro. A observação da NASA é a única parte já universal, porque se passa a coordenada e ela responde em qualquer lugar.

## As quatro camadas

| Camada | Varia com | Forma |
| --- | --- | --- |
| **Observação** | coordenada | API da NASA (POWER), igual em todo lugar |
| **Local** | município, estado | arquivo de configuração, não código |
| **Motor** | nada | função pura: entra lugar, observação, o que foi colhido e prioridades; sai comparação |
| **Canal** | WhatsApp, site, Telegram, SMS | adaptador fino, só traduz |

## A decisão que faz a separação existir de verdade

**O motor devolve estrutura, não texto.** Se ele devolver frase pronta, cada canal vira um parser e a separação é fictícia.

Esboço do contrato (a fechar):

```json
{
  "lugar": "Cantá-RR",
  "coordenada": [2.61, -60.60],
  "consultado_em": "2026-11-14",
  "estado_observado": {
    "umidade_solo_perfil": 0.51,
    "umidade_solo_normal": 0.76,
    "chuva_jun_set_mm": 330,
    "chuva_jun_set_normal_mm": 859,
    "maior_veranico_dias": 24,
    "veranico_normal_dias": 9
  },
  "colheu": "milho",
  "familia_colhida": "Poaceae",
  "lotes": 1,
  "prioridades": ["risco", "solo"],
  "opcoes": [
    {
      "nome": "feijão-caupi",
      "tipo": "sucessão",
      "familia": "Fabaceae",
      "nota": 0.78,
      "razoes": [
        {"tipo": "familia", "texto": "família diferente do milho", "dado": null},
        {"tipo": "solo", "texto": "fixa nitrogênio", "dado": null},
        {"tipo": "agua", "texto": "fecha o ciclo em 75 dias", "dado": "330 mm em jun-set de 2026"}
      ],
      "riscos": ["sensível à falta de água na floração"],
      "validar_com_tecnico": ["cultivar para o seu lote"],
      "qualidade_do_dado": "boa"
    }
  ]
}
```

O adaptador de WhatsApp pega isso e preenche o áudio de trinta segundos. O site pega o mesmo e desenha cards e mapa. O doc já dizia que as frases são fixas preenchidas com os números do motor, então é coerente: **o texto vive no adaptador, o número vive no motor.** O vocabulário também: ver a decisão de linguagem em [02-problema-e-produto](02-problema-e-produto.md).

## O freio: monolito modular, não serviços

Serviços separados hoje é over-engineering para uma entrega amanhã às 22h59.

O que queremos é um **monolito modular**: um repositório, fronteiras limpas entre as quatro camadas, motor como função pura, camada local como arquivo de dados. Ganha-se toda a separação e nenhum custo de deploy, mostra-se a arquitetura para a banca, e dá para quebrar em serviços depois sem reescrever o motor. Quebrar agora custa horas que não temos.

## Por que o contrato existe

O contrato nasceu como a fronteira entre o Welder e o Giuliano: sem o formato de
retorno escrito, quem constrói o hub do site e quem constrói o atendimento se
atropelam, porque cada um precisa de um retorno falso para testar contra.

Com o site fora do MVP, essa urgência caiu, e o contrato ficou **pela razão que
importa mais**: é ele que permite ao mesmo motor atender num canal e noutro sem
mudar uma linha, e é por isso que a demo roda o mesmo cerne em Cantá e em Rio
Verde. Quando o hub entrar, entra contra este mesmo contrato.

## O atendimento no WhatsApp é fluxo com ramos

"Hub como site; para a persona do WhatsApp, uma estrutura de decisão como um atendimento via WhatsApp" (Welder, 14/11).

Isso muda o que o cerne precisa expor: atendimento responde em passos pequenos, um por pergunta, e não num payload único. O hub puxa tudo de uma vez.

Passos previstos do atendimento:

1. Onde fica sua terra? (município, ou localização)
2. Quantos lotes você tem? (define se cabe rotação ou só sucessão; ver [05-base-agronomica](05-base-agronomica.md))
3. O que você acabou de colher?
4. Quando colheu?
5. O que mais importa agora? (prioridade)
6. Resposta: as opções comparadas

Na prática o cerne são quatro consultas pequenas mais um cálculo, e ganha uma dimensão nova: o **cenário** (normal, ano de El Niño forte, estado observado atual).

### Restrição de canal que importa para a estrutura

Para o cerne, a única coisa que o canal impõe é **quantas opções cabem num passo**. Se o fluxo assumir poucas escolhas por pergunta, roda em WhatsApp, Telegram, SMS ou no site. Os limites exatos da API se conferem quando se constrói o adaptador, não agora.

## O que mais afeta a decisão, e o que temos

| Família de variável | Variáveis | Temos? |
| --- | --- | --- |
| Clima observado | chuva, temperatura, umidade do solo, radiação, veranico | sim, POWER |
| Calendário | janela do ZARC, data da colheita anterior, o que cabe no tempo que resta | parcial |
| Solo | umidade (NASA), textura, fertilidade, matéria orgânica, declividade | só umidade |
| Biológico | família botânica da anterior, pragas e doenças hospedadas, nematoides, daninhas | **a regra de família resolve a maior parte; ver 05** |
| Nutrientes | o que a anterior extraiu, o que a próxima repõe | só fixação de N |
| Casa | prioridades, mão de obra, consumo próprio, risco aceito, número de lotes | sim, via perguntas |
| Mercado | preço, comprador, semente disponível, crédito | **nada, e não cabe hoje** |

### Sobre a prioridade "renda"

O formulário oferece quatro prioridades: renda, pasto, risco e mão de obra. O cerne consegue servir três. Para **renda** não temos produtividade nem preço por cultura, e levantar isso por município não cabe até domingo. Ou se tira essa prioridade da ferramenta, ou ela aparece como texto qualitativo marcado como não calculado.

Também seguem fora: levantamento de solo do Cantá, que não existe, e dados de mão de obra por cultura, sem fonte boa.

## Limites do cerne

1. **Coluna de família botânica na tabela de culturas** mais a regra de sucessão: não seguir família com a mesma família, e marcar quando a sequência empilha hospedeiro. (A tabela de famílias já está em [05](05-base-agronomica.md); falta virar dado do motor.)
2. **O contrato de retorno fechado**, com a pergunta generalizada no centro.
3. **Ciclo por graus-dia** (GDD do POWER) em vez de dias fixos.
4. **A regra de comparação**: como o motor ordena as opções. Sem ela a saída é tabela, não recomendação. É o buraco mais bloqueante.
