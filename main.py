import mysql.connector
from jplag_runner import run_jplag
from result_parser import parse_results
from pathlib import Path
from tbl_generator import gera_tabela
from gera_tabela_txts import complemento_das_comparacoes
from gera_tabela_combinada import cria_tabela_combinada
from codes_storage import store_codes
from shutil import rmtree

# root do projeto 
PROJECT_ROOT = Path(__file__).resolve().parent

# CONSTANTES DA BASE DE DADOS
HOST = "127.0.0.1"
USER = "claudio"
PASSWORD = "Clauudio90#"
DATABASE = "compararPlagioDB"
TABELA = "comparacoesPlagio"
# CONSTANTES PARA RODAR O JPLAG
DATAPATH = PROJECT_ROOT / "data" 
JPLAGPATH = PROJECT_ROOT / "jplag" / "jplag.jar"
#CONSTANTES PARA FAZER PARSING DOS RESULTADOS
ZIPFILEPATH = PROJECT_ROOT / "output_relatorios"
#CONSTANTES PARA FAZER A TABELA 
DATA_JSON_PATH = PROJECT_ROOT / "results" / "mydata.json"
#Constantes para tabela de TXTs
TXTFOLDERPATH = PROJECT_ROOT / "data" / "TXT" / "TXT"

def main():
    """
    Função main que cria a conecção com a base de dados e chama as funções auxiliares
    """

    # Estabele ligação com a base de dados
    mydb = conectarDB(HOST,USER,PASSWORD,DATABASE)
    print(mydb)
    
    # Store the students codes 
    store_codes(mydb,DATAPATH) 
    
    # Run o jplag
    #run_jplag(DATAPATH,JPLAGPATH)

    # Parsing dos resultados do jplag para ficheiro .json
    #parse_results(ZIPFILEPATH)

    # Apaga a pasta de relatorios zips quando já nao forem necessários
    #rmtree(ZIPFILEPATH)
    
    # Cria a tabela desejada e insere os dados do .json 
    #gera_tabela(mydb,DATA_JSON_PATH)

    # Cria a tabela dos txts
    #complemento_das_comparacoes(mydb,TXTFOLDERPATH)

    # Cria a tabela final com as comparacoes e metricas de desempenho dos alunos comparados
    #cria_tabela_combinada(mydb)

    
def conectarDB(hostname, username, pwd, database):
    """
    Função que tenta conectar à base de dados fornecida e retorna
    Se não existir base de dados, cria uma base de dados com o nome fornecido
    """
    try:
        # Tenta conectar ao MYSQL com a base de dados fornecida
        mydb =  mysql.connector.connect(
            host = hostname,
            user = username,
            password = pwd,
            database = database
        )
    except mysql.connector.errors.ProgrammingError:
        # Se der erro ao conectar por falta de base de dados
        mydb =  mysql.connector.connect(
            host = hostname,
            user = username,
            password = pwd,
        )
        # Faz a conexão normal e cria a base de dados
        mycursor = mydb.cursor()
        mycursor.execute(f"CREATE DATABASE {database}")

    return mydb


if __name__ == '__main__':
    main()