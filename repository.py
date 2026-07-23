from database import criar_conexao
from models import Livro

# Lista de colunas válidas para evitar SQL Injection nas funções que precisam inserir
# o nome da coluna diretamente na query (já que placeholders '?' não funcionam para colunas).
COLUNAS_VALIDAS = ['titulo', 'autor', 'ano_publicacao', 'genero']

def cadastrar_livro(titulo, autor, ano_publicacao, genero):
    """
    Insere um novo livro no banco de dados (CREATE).
    Utiliza placeholders (?) para prevenir ataques de SQL Injection.
    """
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO livros (titulo, autor, ano_publicacao, genero) VALUES (?, ?, ?, ?)",
                   (titulo, autor, ano_publicacao, genero))
    
    ultimo_id = cursor.lastrowid
    
    conexao.commit()
    conexao.close()
    
    return ultimo_id

def listar_livros():
    """
    Retorna todos os livros cadastrados no banco de dados (READ).
    Transforma cada registro (tupla) em um objeto Livro através de list comprehension.
    """
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM livros")
    lista = cursor.fetchall()
    conexao.close()

    return [Livro(*registro) for registro in lista]

def buscar_por_titulo(valor_digitado): 
    """
    Busca livros que contenham o termo digitado no título (READ).
    Usa o operador LIKE com % para buscar correspondências parciais.
    """
    conexao = criar_conexao()
    cursor = conexao.cursor()
    termo = f"%{valor_digitado}%"
    cursor.execute("SELECT * FROM livros WHERE titulo LIKE ?", (termo,))
    resultado = cursor.fetchall()
    conexao.close()

    return [Livro(*registro) for registro in resultado]

def buscar_por_autor(valor_digitado):
    """
    Busca livros que contenham o termo digitado no autor (READ).
    """
    conexao = criar_conexao()
    cursor = conexao.cursor()
    termo = f"%{valor_digitado}%"
    cursor.execute("SELECT * FROM livros WHERE autor LIKE ?", (termo,))
    resultado = cursor.fetchall()
    conexao.close()

    return [Livro(*registro) for registro in resultado]

def buscar_por_id(valor_digitado):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM livros WHERE id = ?", (valor_digitado,))
    resultado = cursor.fetchone()
    conexao.close()

    if resultado:
        return Livro(*resultado)
    else:
        return None


def atualizar_livro(coluna, livro_id, novo_valor):
    """
    Atualiza um campo específico de um livro existente (UPDATE).
    Valida a coluna antes de executar a query para garantir segurança.
    """
    if coluna not in COLUNAS_VALIDAS:
        return "Erro: Coluna inválida para atualização."
        
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute(f"UPDATE livros SET {coluna} = ? WHERE id = ?", (novo_valor, livro_id))
    msg = cursor.rowcount
    conexao.commit()
    conexao.close()
    
    if msg > 0:
        return f"Sucesso: Livro atualizado! ({msg} linha afetada)"
    else:
        return "Erro: Nenhum livro encontrado com esse ID."

def remover_livro(livro_id):
    """
    Remove um livro do banco de dados a partir do seu ID (DELETE).
    """
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
    msg = cursor.rowcount
    conexao.commit()
    conexao.close()
    
    if msg > 0:
        return f"Sucesso: Livro removido! ({msg} linha afetada)"
    else:
        return "Erro: Nenhum livro encontrado com esse ID."

def listar_livros_ordenados(coluna, ordem):
    """
    Lista todos os livros ordenados por uma coluna específica (ORDER BY).
    Inclui validação dos parâmetros para evitar SQL Injection.
    """
    if coluna not in COLUNAS_VALIDAS:
        coluna = 'id'  # fallback seguro
        
    ordem = "ASC" if ordem.upper() == "ASC" else "DESC" # garante que seja ASC ou DESC

    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute(f"SELECT * FROM livros ORDER BY {coluna} {ordem}, ano_publicacao ASC")
    tabela_ordenada = cursor.fetchall()
    conexao.close()

    return [Livro(*registro) for registro in tabela_ordenada]

def contar_livros():
    """
    Retorna a quantidade total de livros cadastrados (Função de agregação COUNT).
    """
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM livros")
    quant = cursor.fetchone()
    conexao.close()

    return quant[0]

def livros_por_genero():
    """
    Retorna uma lista agrupada da quantidade de livros por gênero e o total de gêneros distintos.
    (GROUP BY e COUNT DISTINCT)
    """
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT genero, COUNT(*) FROM livros GROUP BY genero")
    totais = cursor.fetchall()
    cursor.execute("SELECT COUNT(DISTINCT genero) FROM livros")
    diferentes = cursor.fetchone()
    conexao.close()

    return totais, diferentes[0]
