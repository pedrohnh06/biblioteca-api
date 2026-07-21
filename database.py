import sqlite3

def criar_conexao():
    conexao = sqlite3.connect("biblioteca.db")
    return conexao

def criar_tabela():
    """
    Cria a tabela 'livros' no banco de dados, caso ela ainda não exista.
    Define as colunas e os tipos de dados necessários.
    """
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    ano_publicacao INTEGER,
    genero TEXT)""")
    
    conexao.commit()
    conexao.close()