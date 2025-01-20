import os


def complemento_das_comparacoes(mydb,txt_folder_path):
    """
        # Percorrer as pastas em data/TXT até aos ficheiros txts
        # Obtem o nome do ficheiro com o tipo Aluno_TipoDeAvaliacao_Exercicio.txt  
        # Corresponde cada parcela do nome do ficheiro aos atributos da BD
        # Cria uma tabela propria com os dados e atributos novos do txt
    """
    mycursor = mydb.cursor()
    try:
        sql = """CREATE TABLE IF NOT EXISTS metricas_desempenho(
            Aluno varchar(255),
            Tipo_de_avaliacao varchar(100),
            Exercicio int,
            CODE varchar(10),
            ID varchar(50),
            FILENAME varchar(255),
            TITLE VARCHAR(255),
            DIFICULTY int,
            SUBMITION_DATE BIGINT,
            POINTS double(4,1),
            CLASSIFICATION double(4,1),
            EVALUATION double(4,1),
            EFFICACY double(4,1),
            EFFICIENCY double(4,1),
            MEMORY int,
            CALCULUS int,
            INSTRUCTION int,
            TIME int
        )"""
        mycursor.execute(sql)
    except Exception as e:
        print("Erro ao criar a tabela")
        raise


    percorre_ficheiros_texto(txt_folder_path,mycursor,mydb)
    print("Acabou")
    
    
def percorre_ficheiros_texto(txt_folder_path,mycursor,mydb):
    for root, dirs, files in os.walk(txt_folder_path):
        for file in files:
            if file.endswith('.TXT'):
                file_path = os.path.join(root,file)
                processa_ficheiro_txt(file_path,mycursor,mydb)


def processa_ficheiro_txt(file_path,cursor,mydb):
    try:
        with open(file_path,'r',encoding='utf-8') as file:
            lines = file.readlines()
            nome_do_ficheiro = os.path.basename(file_path)
            partes = nome_do_ficheiro.split('_')
            aluno = partes[0]
            tipo_de_avaliacao = partes[1]
            exercicio = partes[2].replace(".TXT","")
            valores_a_inserir = [aluno,tipo_de_avaliacao,exercicio]
            atributos_inseridos = []

            for line in lines:
                line.strip() # Remover espaços em branco no inicio e final da linha
                line = line.replace('\n',"")
                if line != "":
                    # Para cada linha obter o atributo correspondente e o seu valor 
                    splitList = line.split(" : ")
                    atributo = splitList[0]
                    valor = splitList[1]

                    if atributo not in atributos_inseridos:
                        valores_a_inserir.append(valor) 
                        atributos_inseridos.append(atributo)

            sql = """INSERT INTO metricas_desempenho(Aluno,Tipo_de_avaliacao,Exercicio,CODE,ID,FILENAME,TITLE,
            DIFICULTY,SUBMITION_DATE,POINTS,CLASSIFICATION,EVALUATION,EFFICACY,EFFICIENCY,MEMORY,CALCULUS,
            INSTRUCTION,TIME)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            cursor.execute(sql,valores_a_inserir)
            mydb.commit()


    except Exception as e:
        print(f"Erro ao processar o ficheiro: {file_path}")