from pydantic import BaseModel
from typing import List, Optional
from model.jogo import Jogo

class JogoSchema(BaseModel):
    """ Define como um novo jogo a ser inserido deve ser representado """

    nome_jogo: str = "Catan"
    quantidade_minima: Optional[int] = 1
    quantidade_maxima: Optional[int] = 5
    idade_minima: Optional[int] = 5
    editora: Optional[str] = "Editora Exemplo"
    avaliacao: Optional[int] = 1


class JogoViewSchema(BaseModel):
    id_jogo: int = 1
    nome_jogo: str = "Catan"
    quantidade_minima: Optional[int] = 1
    quantidade_maxima: Optional[int] = 5
    idade_minima: Optional[int] = 5
    editora: Optional[str] = "Editora Exemplo"
    avaliacao: Optional[int] = 1

class ListagemJogosSchema(BaseModel):
    """ Representa uma lista de jogos """
    jogos: List[JogoViewSchema]

class JogosBuscaIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por ID."""
    id_jogo: int = 1

class JogosUpdateSchema(BaseModel):
    id_jogo: int = 1
    nome_jogo: str = "Catan"
    quantidade_minima: Optional[int] = 1
    quantidade_maxima: Optional[int] = 5
    idade_minima: Optional[int] = 5
    editora: Optional[str] = "Editora Exemplo"
    avaliacao: Optional[int] = 1

class JogosDeleteSchema(BaseModel):
    id_jogo: int = 1

def apresenta_todos_jogos(jogos: List[Jogo]):
    result = []
    for jogo in jogos:
        result.append({
            "id_jogo": jogo.id_jogo,
            "nome_jogo": jogo.nome_jogo,
            "quantidade_minima": jogo.quantidade_minima,
            "quantidade_maxima": jogo.quantidade_maxima,
            "idade_minima": jogo.idade_minima,
            "editora": jogo.editora,
            "avaliacao": jogo.avaliacao
        })
    return {"jogos": result}
