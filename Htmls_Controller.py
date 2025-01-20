import mysql.connector
from pathlib import Path 
from html_templates.Alunos import alunos_tmp
import webbrowser
import tempfile
PROJECT_ROOT = Path(__file__).resolve().parent

def controller_htmls(template,mydb):
    """ 
    Recebe um template (string) por parametro
    Carrega o html do template recebido na web
    """
    if template == "alunos":
        try:
            cursor = mydb.cursor()
            # Buscar os diferentes alunos da tabela de comparacoes
            cursor.execute("SELECT DISTINCT aluno2 FROM comparacoesplagio") 
            alunos = cursor.fetchall() # Fetch do resultado do select para alunos
        except mysql.connector.Error as err:
            print(f"Erro ao conectar ou buscar dados: {err}")
        
        alunos_links = ""
        for aluno in alunos:
            # Acumula o link da lista com o aluno atual
            alunos_links += f'<li><a href="template_Fichas.html">{aluno}</a></li>\n' 

        # Envia a lista de itens para o template em html
        html_content = alunos_tmp(alunos_links) # Guarda em html_content o conteudo html retornado
        
    elif template == "fichas":
        print("AINDA NÃO ESTÁ FEITO")
        
        
    """ Esta parte é geral para todos """    
    try:
        # Cria um arquivo temporário para exibir o HTML
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as temp_file:
            temp_file.write(html_content)
            temp_file_path = temp_file.name

        # Abre o HTML no navegador padrão
        webbrowser.open(f"file://{temp_file_path}")
        
        print("Aqui")
    except Exception as e:
        print("Nao foi possivel abrir o ficheiro")