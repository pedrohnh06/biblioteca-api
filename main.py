from fastapi import FastAPI
from repository import listar_livros

# Cria a instância da aplicação FastAPI
app = FastAPI()

# --- ROTA 1: Boas-vindas ---
# Quando alguém acessar http://localhost:8000/, retorna essa mensagem
@app.get("/")
def raiz():
    return {"mensagem": "Bem-vindo à API da Biblioteca!"}

# --- ROTA 2: Listar todos os livros ---
# Quando alguém acessar http://localhost:8000/livros, retorna a lista de livros
@app.get("/livros")
def get_livros():
    livros = listar_livros()
    
    # Converte cada objeto Livro em um dicionário (JSON precisa de dicionários)
    resultado = []
    for livro in livros:
        resultado.append({
            "id": livro.livro_id,
            "titulo": livro.titulo,
            "autor": livro.autor,
            "ano_publicacao": livro.ano_publicacao,
            "genero": livro.genero
        })
    
    return resultado
