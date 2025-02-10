import os

def store_codes(mydb,dataPath):
    """
        Antes de rodar o jplag, passamos pelas pastas de codigos
        obtemos a ficha, exercicio, aluno e guardamos o conteudo do feicheiro (codigo)
        numa tabela
        Essa tabela é criada aqui e depois os dados são guardados
    """
    mycursor = mydb.cursor()
    try:
        # Criar a tabela 
        sql_Cria_Tabela = """
            CREATE TABLE IF NOT EXISTS codigos_alunos(
                aluno varchar(100),
                curso varchar(100),
                tipo_avaliacao varchar(100),
                exercicio int,
                codigo LONGTEXT
            );
        """
        mycursor.execute(sql_Cria_Tabela)
        
        # Percorrer a pasta da data guardando os valores para serem guardardos na tabela
        for root, dirs, files in os.walk(dataPath):
            if any(file.endswith('java') for file in files):
                curso = os.path.relpath(root, dataPath).split(os.sep)[0] # obtem o curso
                parse_ficheiro_java(files,curso,root,mydb)
        
    except Exception as e:
        print(f"Deu erro: {e}")





def parse_ficheiro_java(files,curso, root,mydb):
    """
    Files é um array com todos os ficheiros .java de uma dada root
    A ideia é dar split em cada indice do array files para obter cada parte do nome do ficheiro
    Os ficheiros têm o seguinte nome: aluno_tipoAvaliacao_exercicio.java
    Damos split no nome por '_' e guardamos cada atributo 
    Em cada iteração, devemos tambem obter o que está dentro do ficheiro (codigo)  
    """
    aluno = ""
    tipo_avaliacao = ""
    exercicio = ""
    codigo = ""
    
    
    # Percorrer cada ficheiro no array files
    for file in files:  
        fileStr = str(file)
        splitted_File = fileStr.split('_')
        aluno = splitted_File[0]                # Aluno a guardar na linha da tabela
        tipo_avaliacao = splitted_File[1]       # Tipo de avaliação a guardar na linha da tabela
        exercicio = int(splitted_File[2][:-5])      # Exercicio a guardar na linha da tabela
        
        file_path = os.path.join(root,file)
        
        # Tentar ler o conteudo do fecheiro para obter o codigo do aluno
        try:
            with open(file_path,"r",encoding="utf-8") as f:
                codigo = f.read() # lê o ficheiro e guarda o conteudo em codigo
                
        except Exception as e:
            print(f"Erro ao ler {file_path}: {e}")
            codigo = "" # Se der erro limpa o ficheiro de codigo (acho que nao é bem necessário mas tasse)
            
        
        insere_dados(aluno,curso,tipo_avaliacao,exercicio,codigo,mydb) # insere os dados na tabela
            
        
def insere_dados(aluno,curso,tipo_avaliacao,exercicio,codigo,mydb):
    
    valores_a_inserir = [aluno,curso,tipo_avaliacao,exercicio,codigo]
    sql_insere_dados = """
        INSERT INTO codigos_alunos(
            aluno,
            curso,
            tipo_avaliacao,
            exercicio,
            codigo
        ) VALUES (
            %s,%s,%s,%s,%s
        )
    """
    
    mycursor = mydb.cursor() 
    mycursor.execute(sql_insere_dados,valores_a_inserir)
    mydb.commit()
    mycursor.close()