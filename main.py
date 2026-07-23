from fastapi import FastAPI
from schema import LivroSchema 
from repository import cadastrar_livro
from repository import buscar_por_id
from repository import listar_livros
from repository import buscar_por_titulo

app = FastAPI()

# Quando alguém acessar http://localhost:8000/, retorna essa mensagem
@app.get("/")
def raiz():
    return {"mensagem": "Bem-vindo à API da Biblioteca!"}

# Quando alguém acessar http://localhost:8000/livros, retorna a lista de livros
@app.get("/livros")
def get_livros():
    livros = listar_livros()
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

@app.get("/livros/{livro_id}")
def get_livro_por_id(livro_id: int):
    livro = buscar_por_id(livro_id)
    if livro:
        return livro
    else: 
        return {"erro": "Livro não encontrado"}

@app.get("/livros/busca/{titulo}")
def get_livro_por_titulo(titulo: str):
    livro = buscar_por_titulo(titulo)
    livros = []
    for registro in livro:
        livros.append({
            "id": registro.livro_id,
            "titulo": registro.titulo,
            "autor": registro.autor,
            "ano_publicacao": registro.ano_publicacao,
            "genero": registro.genero    
        })

    return livros


@app.post("/livros", status_code=201)
def criar_livro(livro: LivroSchema):
    novo_id = cadastrar_livro(livro.titulo, livro.autor, livro.ano_publicacao, livro.genero)
    return {"id": novo_id, "mensagem": "Livro cadastrado com sucesso!"}

    
