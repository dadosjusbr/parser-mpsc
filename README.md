![testes](https://github.com/dadosjusbr/parser-mpsc/actions/workflows/docker-publish.yml/badge.svg)    
[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/dadosjusbr/parser-mpsc)

# Ministério Público de Santa Catarina (MPSC)

Este parser tem como objetivo a recuperação de informações sobre folhas de pagamentos de funcionários a partir do Ministério Público de Santa Catarina. O site com as informações pode ser acessado [aqui](https://servicos-portal.mpsc.mp.br/web/mp-transparente/contracheque).

Ele funciona em conjunto com o [coletor mpsc](https://github.com/dadosjusbr/coletor-mpsc), e faz o parser das planilhas baixadas lá.

Cada planilha é referente a uma destas categorias:

1. Contracheque - Membros Ativos

   |Campo|Descrição|
   |-----|---------|
   |Matricula|Código funcional do membro.|
   |Nome|Nome completo do membro.|
   |Descrição|Nome do cargo efetivo.|
   |Lotação|Lotação do membro.|
   |Remuneração do Cargo|Remuneração do cargo efetivo: Vencimento, GAMPU, V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza.|
   |Outras Verbas Remuneratorias, Legais ou Judiciais|V.P.N.I., adicional por tempo de serviço, quintos, décimos e vantagens decorrentes de sentença judicial ou extensão administrativa.|
   |Função de Confiança ou Cargo em Comissão|Rubricas que representam a retribuição paga pelo exercício de função ou remuneração de cargo em comissão.|
   |Gratificação Natalina|Parcelas da Gratificação Natalina (13º) pagas no mês corrente.|
   |Férias (1/3 Constitucional)|Adicional correspondente a 1/3 (um terço) da remuneração, pago ao membro por ocasião das férias.|
   |Abono de Permanência|Valor equivalente ao da contribuição previdenciária, devido ao funcionário público que esteja em condição de aposentar-se, mas que optou por continuar em atividade (instituído pela Emenda Constitucional nº 41, de 16 de dezembro de 2003.|
   |Outras Remunerações Temporárias|Outras remunerações temporárias.|
   |Verbas Indenizatórias|Auxílio-Alimentação, Auxílio-Transporte, Auxílio-Moradia, Ajuda de Custo e outras desta natureza, exceto diárias, que são divulgadas no Portal da Transparência.|
   |Total de Rendimentos Brutos|Total dos rendimentos brutos pagos no mês.|
   |Contribuição Previdenciária|Contribuição Previdenciária Oficial (Plano de Seguridade Social do Servidor Público e Regime Geral de Previdência Social).|
   |Imposto de Renda|Imposto de Renda Retido na Fonte.|
   |Retenção por Teto Constitucional|Valor deduzido da remuneração básica bruta, quando esta ultrapassa o teto constitucional, nos termos da legislação correspondente.|
   |Total de Descontos|Total dos descontos efetuados no mês.|
   |Rendimento Líquido Total|Rendimento líquido após os descontos referidos nos itens anteriores.|

2. Contracheque - Verbas Indenizatórias
   |Campo|Descrição|
   |-|-|
   |VERBAS INDENIZATÓRIAS|Auxílio-alimentação, auxílio-transporte, auxílio-moradia, ajuda de custo e outras dessa natureza, exceto diárias (que serão divulgadas no Portal da Transparência), discriminada de forma individualizada.|
   |OUTRAS REMUNERAÇÕES TEMPORÁRIAS|Valores pagos a título de adicional de insalubridade ou de periculosidade, adicional noturno, serviço extraordinário, substituição de função, cumulações.|
   |Total|Valor total pago, excluindo-se eventuais descontos.|

Estas planilhas contém as informações de pagamento de todos os meses disponíveis, a fim de gerar os *crawling results* de cada mês.

## Como usar
### Executando com Docker

 - Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 

 - Construção da imagem:

    ```sh
    $ cd coletores/mpsc
    $ sudo docker build -t mpsc .
    ```
 - Execução:
 
    ```sh
    $ sudo docker run -e YEAR=2020 -e MONTH=2 -e GIT_COMMIT=$(git rev-list -1 HEAD) mpsc
    ```
### Execução sem o Docker:

- Para executar o script é necessário rodar o seguinte comando, a partir do diretório `/mpsc`, adicionando às variáveis seus respectivos valores, a depender da consulta desejada. É válido lembrar que faz-se necessario ter o [Python 3.6.9](https://www.python.org/downloads/) instalado.

    ```sh
    MONTH=1 YEAR=2018 python3 src/main.py
    ```
- Para que a execução do script possa ser corretamente executada é necessário que todos os requirements sejam devidamente instalados. Para isso, executar o [PIP](https://pip.pypa.io/en/stable/installing/) passando o arquivo requiments.txt, por meio do seguinte comando:

   ```sh
   pip install -r requirements.txt
   ```