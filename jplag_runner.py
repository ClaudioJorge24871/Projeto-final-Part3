import os
import subprocess

def run_jplag(dataPath,jplag_path):
    """
    Função para rodar o jplag e gera o results.zip
    """
    
    output_path = "output_relatorios"                                           # cria a pasta output se não existir
    os.makedirs(output_path,exist_ok=True)

    pastas_com_java = encontra_pastas_comjava(dataPath)                         # Encontra e guarda numa lista as pastas com java

    for pasta in pastas_com_java:                                               # Executa o jplag para cada pasta com .java's
        executar_jplag(pasta,output_path,jplag_path)


def encontra_pastas_comjava(dataPath):
    """
    Percorre recursivamente a pasta base de Data para 
    encontrar pastas com .java
    """

    pastas_com_java = set()                                                     # Lista para guardar os paths das pastas com java

    for root, dirs, files in os.walk(dataPath):                                 # Percorre as pastas em forma de árvore
        if any(file.endswith('.java') for file in files):                       # Se existir algum ficheiro que acaba em .java na diretoria atual, guarda no set 
            pastas_com_java.add(root)

    return pastas_com_java

def executar_jplag(pasta_exercicios, output_path, jplag_path):
    """
    Função para executar o jplag para 
    cada pasta que possui ficheiros .java
    """

    nome_exercicio = os.path.basename(pasta_exercicios)                         # Para cada pasta, obter o nome final da pasta e o curso
    numero_curso = os.path.join(output_path,obter_curso(pasta_exercicios))                 
    os.makedirs(numero_curso,exist_ok=True)         
    pasta_resultados = os.path.join(numero_curso,nome_exercicio)                # e criar um zip de resultados unico com esse nome

    linguagem = "java"                                                          # define a linguagem dos ficheiros dos exercicios a comparar

    comando = [                                                                 # gera o comando para rodar o jplag no subprocess
        "java","-jar", jplag_path,
        "-l", linguagem,
        pasta_exercicios,
        "-r",pasta_resultados
    ]

    try:
        subprocess.run(comando,check=True)
    except subprocess.CalledProcessError as e:
        print(f"The prompt failed with the return code: {e.returncode}")

def obter_curso(path):
    """
    Função para obter a primeira parte de um caminho. 
    Esta primeira parte deve corresponder ao numero do Curso 
    """

    partes = os.path.normpath(path).split(os.path.sep)                          # divide o caminho em partes
    return partes[-4]


    