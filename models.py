class Livro: 
    """
    Representa um livro na biblioteca.
    Essa classe serve para estruturar os dados que vêm do banco de dados,
    transformando tuplas genéricas em objetos fáceis de manipular.
    """
    def __init__(self, id, titulo, autor, ano_publicacao, genero):
        self.livro_id = id
        self.titulo = titulo    
        self.autor = autor
        self.ano_publicacao = ano_publicacao
        self.genero = genero

    def __str__(self):
        """
        Define como o livro será exibido quando usarmos print(livro).
        """
        return (f"ID: {self.livro_id} | Título: {self.titulo} | Autor: {self.autor} | "
        f"Ano de Publicação: {self.ano_publicacao} | Gênero: {self.genero}")
