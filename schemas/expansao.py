from pydantic import BaseModel
from typing import List, Optional, Union
from model.expansao import Expansao

class ExpansaoSchema(BaseModel):
    nome_expansao: Optional[str] = "Expansão Exemplo"
    quantidade_minima: Optional[int] = 1
    quantidade_maxima: Optional[int] = 5
    idade_minima: Optional[int] = 5
    editora: Optional[str] = "Editora Exemplo"
    avaliacao: Optional[int] = 1
    id_jogo: int = 1

class ExpansaoViewSchema(BaseModel):
    id_expansao: int = 1
    nome_expansao: Optional[str] = "Expansão Exemplo"
    quantidade_minima: Optional[int] = 1
    quantidade_maxima: Optional[int] = 100
    idade_minima: Optional[int] = 1
    editora: Optional[str] = "Editora Exemplo"
    avaliacao: Optional[int] = 1
    id_jogo: int = 1

class ExpansaoViewComJogoSchema(BaseModel):
    id_expansao: int = 1
    nome_expansao: Optional[str] = "Expansão Exemplo"
    quantidade_minima: Optional[int] = 1
    quantidade_maxima: Optional[int] = 100
    idade_minima: Optional[int] = 1
    editora: Optional[str] = "Editora Exemplo"
    avaliacao: Optional[int] = 1
    id_jogo: int = 1
    nome_jogo: Optional[str] = "Jogo Exemplo"

class ListagemExpansoesSchema(BaseModel):
    """ Representa uma lista de expansões """
    expansoes: List[ExpansaoViewComJogoSchema]

class ExpansaoBuscaIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por ID.
    """
    id_expansao: int = 1

class ExpansaoUpdateSchema(BaseModel):
    id_expansao: int = 1
    nome_expansao: Optional[str] = "Expansão Exemplo"
    quantidade_minima: Optional[int] = 1
    quantidade_maxima: Optional[int] = 100
    idade_minima: Optional[int] = 1
    editora: Optional[str] = "Editora Exemplo"
    avaliacao: Optional[int] = 1
    id_jogo: int = 1
    nome_jogo: str = "Jogo Exemplo"

class ExpansaoDeleteSchema(BaseModel):
    id_expansao: int = 1

def apresenta_todas_expansoes(expansoes: List[Expansao]):
    result = []
    for expansao in expansoes:
        jogo = getattr(expansao, "jogo", None)
        nome_jogo = jogo.nome_jogo if jogo else None
        result.append({
            "id_expansao": expansao.id_expansao,
            "nome_expansao": expansao.nome_expansao,
            "quantidade_minima": expansao.quantidade_minima,
            "quantidade_maxima": expansao.quantidade_maxima,
            "idade_minima": expansao.idade_minima,
            "editora": expansao.editora,
            "avaliacao": expansao.avaliacao,
            "id_jogo": expansao.id_jogo,
            "nome_jogo": nome_jogo
        })
    return {"expansoes": result}