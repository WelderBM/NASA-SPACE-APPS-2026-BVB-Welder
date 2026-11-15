# Persona secundária: versão para o site

[Voltar ao índice](../README.md)

Data de referência: 14/11/2026. Status: rascunho, a validar com o time.

Este arquivo separa as dependências da persona secundária, a mais informatizada: o filho ou neto que acessa um site e mostra as informações para quem decide na família. Ele é paralelo à persona do WhatsApp (README, seção "Persona do WhatsApp") e não substitui essa.

Hipótese de trabalho: a persona secundária é o "intermediário digital da família" (ver README, seção "Ideação"). Se o time decidir outra definição, este arquivo muda com ela.

## O que esta persona consome do cerne

Estes itens vêm do cerne compartilhado. Cada um precisa ser o mesmo dado que o WhatsApp usa.

- Chuva e temperatura do NASA POWER para o município (hoje só o Cantá foi testado).
- Janelas de plantio do ZARC por município e cultura.
- Tabela de culturas: ciclo, água no ciclo, papel na rotação e fonte de cada linha.
- Limiares e regras: caupi entre 18 °C e 34 °C, soja acima de 40 °C, 7 a 8 mm/dia na floração (marcados como "a validar com agrônomo").

## O que é próprio desta persona

- Formulário de prioridades: renda, pasto, risco e mão de obra. A família escolhe as prioridades dentro da ferramenta. O formulário não alimenta o motor.
- Visualização: mapa, comparação de estratégias lado a lado e o dado do NASA POWER ao lado do sinal que o produtor já usa.
- Linguagem: a interface é do intermediário, então pode trazer mais detalhe que o áudio do WhatsApp, sem inventar texto.

## Regra de verificação de textos

Nenhum texto entra no site sem estar nesta tabela com status "verificado". Isso evita a incongruência de contexto que já aconteceu no início do projeto.

| Texto usado no site | Fonte | Data da leitura | Status | Responsável |
| --- | --- | --- | --- | --- |
| Chuva de 2026 no Cantá ~40% abaixo da média | NASA POWER, Cantá (lat 2,61, lon -60,60) | 14/11/2026 | Verificado na API; é dado de modelo, dizer "estimativa" | a definir |
| Agosto de 2026 com 85% abaixo da média no Cantá | NASA POWER | 14/11/2026 | Verificado na API; confirmado em campo pelo SGB e INMET (ver README) | a definir |
| Janela de plantio do caupi em Cantá e Boa Vista (fim de junho a meados de agosto) | Portaria ZARC caupi, safra 2023/2024 | 14/11/2026 | A validar: tabela do PDF veio desalinhada e a portaria pode ter versão mais nova | a definir |
| Soja: 100 a 130 dias, 450 a 800 mm | ZARC soja 2026/27 | 14/11/2026 | A validar: conferir no PDF oficial antes do site | a definir |
| Caupi: 18 °C a 34 °C | fonte ainda não anotada | — | A validar: sem fonte registrada | a definir |
| Soja: acima de 40 °C, 7 a 8 mm/dia na floração | fonte ainda não anotada | — | A validar: sem fonte registrada | a definir |
| 33,63% dos produtores de Roraima são indígenas | IBGE, Censo Agro 2017 | 14/11/2026 | Verificado; o texto antigo "33,5%" está errado | a definir |
| 96% dos produtores usam WhatsApp para decisões de negócio | Canal Rural (pesquisa nacional) | 14/11/2026 | Verificado na fonte; é dado nacional, não de Roraima | a definir |

Para acrescentar um texto: escreva a frase, anote a fonte com o link, a data da leitura e o status. Só depois use no site. Se a fonte mudar, o status volta para "a validar".

## Lacunas

- Número de agricultores familiares por município do interior (SIDRA 6778).
- Janelas de plantio por município fora do Cantá e de Boa Vista.
- Fonte para os limiares de caupi e soja.
- Perfil do intermediário digital em Roraima: quem é, com que aparelho e com que internet.

## Relação com o cerne

Quando o cerne for definido, cada item acima aponta para o campo dele (ex.: `zarc.cantá.caupi`). Nenhum número deve ficar só neste arquivo.
