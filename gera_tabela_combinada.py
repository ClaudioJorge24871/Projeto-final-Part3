def cria_tabela_combinada(mydb):
    """
    Cria uma tabela que combina dados de comparacoesPlagio e metricas_desempenho,
    incluindo as métricas de desempenho dos dois alunos para o exercício e tipo de avaliação específicos.
    """
    mycursor = mydb.cursor()
    print("Tou aqui")
    try:
        # Comando SQL para criar a tabela combinada
        sql_criar_tabela = """
        CREATE TABLE IF NOT EXISTS tabela_combinada(
            id BIGINT PRIMARY KEY,
            aluno1 VARCHAR(255),
            aluno2 VARCHAR(255),
            curso VARCHAR(255),
            tipo_de_avaliacao VARCHAR(100),
            exercicio INT,
            dificuldade INT,
            indPlagio DECIMAL(5,2),
            aluno1_points DOUBLE,
            aluno1_classification DOUBLE,
            aluno1_evaluation DOUBLE,
            aluno1_efficacy DOUBLE,
            aluno1_efficiency DOUBLE,
            aluno2_points DOUBLE,
            aluno2_classification DOUBLE,
            aluno2_evaluation DOUBLE,
            aluno2_efficacy DOUBLE,
            aluno2_efficiency DOUBLE
        );
        """
        mycursor.execute(sql_criar_tabela)

        # Inserir os dados necessários na tabela combinada
        sql = """
        INSERT INTO tabela_combinada(
            id, aluno1, aluno2, curso, tipo_de_avaliacao, exercicio, dificuldade, indPlagio,
            aluno1_points, aluno1_classification, aluno1_evaluation, aluno1_efficacy, aluno1_efficiency,
            aluno2_points, aluno2_classification, aluno2_evaluation, aluno2_efficacy, aluno2_efficiency
        )
        SELECT 
            cp.id,
            cp.aluno1,
            cp.aluno2,
            cp.curso,
            cp.tipo_de_avaliacao,
            cp.exercicio,
            md1.DIFICULTY AS dificuldade,
            cp.indPlagio,
            md1.POINTS AS aluno1_points,
            md1.CLASSIFICATION AS aluno1_classification,
            md1.EVALUATION AS aluno1_evaluation,
            md1.EFFICACY AS aluno1_efficacy,
            md1.EFFICIENCY AS aluno1_efficiency,
            md2.POINTS AS aluno2_points,
            md2.CLASSIFICATION AS aluno2_classification,
            md2.EVALUATION AS aluno2_evaluation,
            md2.EFFICACY AS aluno2_efficacy,
            md2.EFFICIENCY AS aluno2_efficiency
        FROM comparacoesplagio cp
        LEFT JOIN metricas_desempenho md1 
            ON cp.aluno1 = md1.Aluno 
            AND cp.tipo_de_avaliacao = md1.Tipo_de_avaliacao 
            AND cp.exercicio = md1.Exercicio
        LEFT JOIN metricas_desempenho md2 
            ON cp.aluno2 = md2.Aluno 
            AND cp.tipo_de_avaliacao = md2.Tipo_de_avaliacao 
            AND cp.exercicio = md2.Exercicio
        WHERE md1.DIFICULTY >= 2;
        """
        mycursor.execute(sql)

        mydb.commit()
        print("Dados combinados inseridos com sucesso")

    except Exception as e:
        print(f"Erro ao criar ou inserir dados na tabela: {e}")
        if mydb.is_connected():
            try:
                mydb.rollback()
            except:
                print("Erro durante rollback")
    finally:
        print("Cursor fechado")
        mycursor.close()

# Codigo para inserir os dados vindos da tabela_combinada na tbl elo_mais_plagiador 
"""
INSERT INTO o_elo_mais_plagiador (
    aluno1,
    aluno2,
    indice_de_plagio,
    efficiency_aluno1,
    efficiency_aluno2,
    points_aluno1,
    points_aluno2,
    plagiarism_score_aluno1,
    plagiarism_score_aluno2
)
SELECT 
    aluno1,
    aluno2,
    indPlagio AS indice_de_plagio,
    aluno1_efficiency AS efficiency_aluno1,
    aluno2_efficiency AS efficiency_aluno2,
    aluno1_points AS points_aluno1,
    aluno2_points AS points_aluno2,
    -- Calcular plagiarism_score para aluno1 onde eficiencia é maior do que 5 (threshold)
    CASE 
        WHEN aluno1_efficiency > 5.0 THEN (aluno1_points * indPlagio) / aluno1_efficiency
        ELSE 0
    END AS plagiarism_score_aluno1,
    -- Calcular plagiarism_score para aluno2
    CASE 
        WHEN aluno2_efficiency >5.0 THEN (aluno2_points * indPlagio) / aluno2_efficiency
        ELSE 0
    END AS plagiarism_score_aluno2
FROM 
    tabela_combinada;
"""

# Calcular a média de plagiarism score de cada aluno
""" 
SELECT aluno, 
       AVG(plagiarism_score) AS media_plagiarism_score
FROM (
    SELECT aluno1 AS aluno, plagiarism_score_aluno1 AS plagiarism_score
    FROM o_elo_mais_plagiador
    UNION ALL
    SELECT aluno2 AS aluno, plagiarism_score_aluno2 AS plagiarism_score
    FROM o_elo_mais_plagiador
) AS combined
GROUP BY aluno
ORDER BY media_plagiarism_score DESC;
"""

# Calcular a média de plagio que existe no curso
"""
SELECT AVG(media_plagiarism_score) AS media_geral
FROM (
    SELECT aluno, 
           AVG(plagiarism_score) AS media_plagiarism_score
    FROM (
        SELECT aluno1 AS aluno, plagiarism_score_aluno1 AS plagiarism_score
        FROM o_elo_mais_plagiador
        UNION ALL
        SELECT aluno2 AS aluno, plagiarism_score_aluno2 AS plagiarism_score
        FROM o_elo_mais_plagiador
    ) AS combined
    GROUP BY aluno
) AS medias_individuais;
"""