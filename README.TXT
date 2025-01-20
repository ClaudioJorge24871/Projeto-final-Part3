Projeto final parte 3

Objetivo: Colocar dados de comparações numa base de dados

Estrutura da Base de dados

                | id (PK) | aluno1 | aluno2 | curso | tipo_de_avaliacao | execicio | indPlagio |
R E G I S T O 1 |         |        |        |       |                   |          |           |
R E G I S T O 2 |         |        |        |       |                   |          |           |


Passos:

. Criar uma base de dados chamada compararPlagioDB e estabelece ligação
. Criar um "main" que chama cada função e passa os parametros necessários
. Criar um "runner" que roda o jplag para gerar o results.zip
. Criar um "parser" que transforma os dados do results.zip em dados json 
. Criar um "tblGenerator", cria a ligação à db e verfica se existe a tabela comparacoesPlagio
    . Se não existir, cria a tabela comparacoesPlagio e atribui os dados
    . Se existe tabela, apaga a existente, cria uma nova e atribui os dados  
. No final, tblGenerator, mostra a tabela comparacoesPlagio


Install mysql: https://dev.mysql.com/downloads/installer/


Estrutura dos testes confidenciais:

Curso1
    |-> java
        | -> Exame0
                | -> Exame0_001
                        | -> AnonymousNx_Exame0_001.java
                        | -> AnonymousNx_Exame0_002.java
                | -> Exame0_002
        | -> Ficha01
        | -> Freq2024

Algoritmo1:

1. Entra na pasta
2. Verifica se existe alguma pasta dentro
        - se sim, entra nessa, vai para 1.
        - se nao, mas houver ficheiros, 
            roda o jplag com o caminho atual
            volta uma pasta
            apaga pasta do caminho atual
        - se nao, nem ficheiros,
            volta uma pasta

Algoritmo2:

1. Percorrer de forma recursiva as pastas até encontrar uma com .java dentro
2. Adicionar o caminho dessas pastas numa lista
3. rodar o jplag para cada um desses caminhos na lista
4. Cada zip de results deve ser unico 

Exemplo de implementação: https://chatgpt.com/share/675eec52-023c-800a-95e5-48f64ded538d