from pydantic import BaseModel

class LivroSchema(BaseModel): 
    titulo: str
    autor: str
    ano_publicacao: int
    genero: str