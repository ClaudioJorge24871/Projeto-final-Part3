def alunos_tmp(alunos_links):
    """
    Recebe os links dos alunos e insere no HTML base.
    Retorna o HTML gerado como uma string.
    """
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Alunos</title>
    </head>
    <body>
        <!--Template que mostra os alunos. Cada aluno é um link-->
        <h1>Todos os alunos</h1>
        <br>
        <!--Introduzir uma search bar-->

        <!--Local onde aparece a lista dos alunos-->
        <ul>
            {alunos_links}
        </ul>
    </body>
    </html>
    """
    return html_template.format(alunos_links=alunos_links)
