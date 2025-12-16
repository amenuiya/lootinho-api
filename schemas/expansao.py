from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import List, Optional
from model.expansao import Expansao


class ExpansaoSchema(BaseModel):
    nome_expansao: Optional[str] = None
    quantidade_minima: Optional[int] = None
    quantidade_maxima: Optional[int] = None
    idade_minima: Optional[int] = None
    editora: Optional[str] = None
    avaliacao: Optional[float] = None
    data_aquisicao: str
    id_jogo: Optional[int] = None

    @field_validator("avaliacao", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v


class ExpansaoViewSchema(BaseModel):
    id_expansao: int = Field(..., description="ID da expansão")
    nome_expansao: Optional[str] = Field(None, description="Nome da expansão")
    quantidade_minima: Optional[int] = Field(None, description="Quantidade mínima de jogadores")
    quantidade_maxima: Optional[int] = Field(None, description="Quantidade máxima de jogadores")
    idade_minima: Optional[int] = Field(None, description="Idade mínima recomendada")
    editora: Optional[str] = Field(None, description="Editora da expansão")
    avaliacao: Optional[float] = Field(None, description="Avaliação da expansão")
    data_aquisicao: Optional[str] = Field(None, description="Data de aquisição no formato DD-MM-YYYY")
    id_jogo: int = Field(None, description="ID do jogo base para a expansão")

    model_config = {
        "from_attributes": True
    }

class ListagemExpansoesSchema(BaseModel):
    """ Representa uma lista de expansões """
    expansoes: List[ExpansaoViewSchema]

class ExpansaoBuscaIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por ID.
    """
    id_expansao: int = Field(..., description="ID da expansão a ser buscada")

class ExpansaoUpdateSchema(BaseModel):
    id_expansao: int = Field(..., description="ID da expansão a ser atualizada")
    nome_expansao: Optional[str] = Field(None, description="Nome da expansão")
    quantidade_minima: Optional[int] = Field(None, description="Quantidade mínima de jogadores")
    quantidade_maxima: Optional[int] = Field(None, description="Quantidade máxima de jogadores")
    idade_minima: Optional[int] = Field(None, description="Idade mínima recomendada")
    editora: Optional[str] = Field(None, description="Editora da expansão")
    avaliacao: Optional[float] = Field(None, description="Avaliação da expansão")
    data_aquisicao: Optional[str] = Field(None, description="Data de aquisição no formato DD-MM-YYYY")
    id_jogo: int = Field(None, description="ID do jogo base para a expansão")

class ExpansaoDeleteSchema(BaseModel):
    id_expansao: int = Field(..., description="ID da Expansão a ser deletada")

def apresenta_todas_expansoes(expansoes: List[Expansao]):
    result = []
    for expansao in expansoes:
        result.append({
            "id_expansao": expansao.id_expansao,
            "nome_expansao": expansao.nome_expansao,
            "quantidade_minima": expansao.quantidade_minima,
            "quantidade_maxima": expansao.quantidade_maxima,
            "idade_minima": expansao.idade_minima,
            "editora": expansao.editora,
            "avaliacao": expansao.avaliacao,
            "data_aquisicao": expansao.data_aquisicao,
            "id_jogo": expansao.id_jogo
        })
    return {"expansoes": result}