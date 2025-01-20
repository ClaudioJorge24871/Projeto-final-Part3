import json
import hashlib


def gera_tabela(mydb,data_json_path):
    """
    Função para gerar a tabela e preeenchê-la na base de dados
    """

    # Gera o cursor da tabela
    mycursor = mydb.cursor() 
    
    # Cria a tabela comparacoesPlagio (se nao existe) com os atributos (id (PK),aluno1,aluno2,curso,tipo_de_avaliacao,exercicio,indPlagio)
    try:
        sql = "CREATE TABLE IF NOT EXISTS comparacoesPlagio (id BIGINT PRIMARY KEY,aluno1 VARCHAR(255),aluno2 VARCHAR(255),curso VARCHAR(255),tipo_de_avaliacao VARCHAR(100),exercicio INT, indPlagio DECIMAL(5,2))"
        mycursor.execute(sql)
    except Exception as e:
        print("Erro ao criar a tabela")
        raise
    
    # Abrir a pasta results e carregar o json para data
    try:
        with open(data_json_path, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erro ao abrir ou processar o arquivo JSON: {e}")
        return  # Para o programa, pois não faz sentido continuar

    val = []
    # Percorrer cada json dentro do ficheiro 
    for comparacao in data:
        # Obter os atributos (curso,aln1,aln2,tipo,exercicio,indicePlagio)
        aluno1 = comparacao['aln1']
        aluno2 = comparacao['aln2']
        curso = comparacao['curso']
        tipo_de_avaliacao = comparacao['tipo']
        exercicio = int(comparacao['exercicio'])
        indPlagio = round(float(comparacao['indicePlagio']) * 100, 2)
        # Gera um atributo id único
        combinacao = f"{aluno1}{aluno2}{curso}{tipo_de_avaliacao}{exercicio}"
        idUnico = int(hashlib.md5(combinacao.encode()).hexdigest(), 16) % (10 ** 18)
        # Gera os comando para inserir os dados de cada atributo do json para cada atributo correspodente na tabela comparacoesPlagio
        sql = "INSERT INTO comparacoesPlagio (id,aluno1,aluno2,curso,tipo_de_avaliacao,exercicio,indPlagio) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        val.append((idUnico,aluno1,aluno2,curso,tipo_de_avaliacao,exercicio,indPlagio))
    
    mycursor.executemany(sql,val)
    mydb.commit()

    # Print da ultima linha alterada
    print("Foi inserido ",mycursor.rowcount)

    mycursor.close()