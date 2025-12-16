from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import List, Optional
from model.jogo import Jogo


class JogoSchema(BaseModel):
    """ Define como um novo jogo a ser inserido deve ser representado """
    nome_jogo: str
    quantidade_minima: Optional[int] = None
    quantidade_maxima: Optional[int] = None
    idade_minima: Optional[int] = None
    editora: Optional[str] = None
    avaliacao: Optional[float] = None
    data_aquisicao: str

    @field_validator("avaliacao", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v


class JogoViewSchema(BaseModel):
    id_jogo: int = Field(..., description="ID do jogo")
    nome_jogo: Optional[str] = Field(None, description="Nome do jogo")
    quantidade_minima: Optional[int] = Field(None, description="Quantidade mínima de jogadores")
    quantidade_maxima: Optional[int] = Field(None, description="Quantidade máxima de jogadores")
    idade_minima: Optional[int] = Field(None, description="Idade mínima recomendada")
    editora: Optional[str] = Field(None, description="Editora do jogo")
    avaliacao: Optional[float] = Field(None, description="Avaliação do jogo")
    data_aquisicao: Optional[str] = Field(None, description="Data de aquisição no formato DD-MM-YYYY")

    model_config = {
        "from_attributes": True
    }

class ListagemJogosSchema(BaseModel):
    """ Representa uma lista de jogos """
    jogos: List[JogoViewSchema]

class JogosBuscaIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por ID.
    """
    id_jogo: int = Field(..., description="ID do jogo a ser buscado")

class JogosUpdateSchema(BaseModel):
    id_jogo: int = Field(..., description="ID do jogo a ser atualizado")
    nome_jogo: Optional[str] = Field(None, description="Nome do jogo")
    quantidade_minima: Optional[int] = Field(None, description="Quantidade mínima de jogadores")
    quantidade_maxima: Optional[int] = Field(None, description="Quantidade máxima de jogadores")
    idade_minima: Optional[int] = Field(None, description="Idade mínima recomendada")
    editora: Optional[str] = Field(None, description="Editora do jogo")
    avaliacao: Optional[float] = Field(None, description="Avaliação do jogo")
    data_aquisicao: Optional[str] = Field(None, description="Data de aquisição no formato DD-MM-YYYY")

class JogosDeleteSchema(BaseModel):
    id_jogo: int = Field(..., description="ID do Jogo a ser deletado")

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
            "avaliacao": jogo.avaliacao,
            "data_aquisicao": jogo.data_aquisicao,
        })
    return {"jogos": result}
