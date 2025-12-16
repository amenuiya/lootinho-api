from sqlalchemy import Column, String, Integer, Date, Float
from model.base import Base

class Jogo(Base):
    __tablename__ = 'jogo'

    id_jogo = Column(Integer, primary_key=True, autoincrement=True)
    nome_jogo = Column(String(255), nullable=True)
    quantidade_minima = Column(Integer, nullable=True)
    quantidade_maxima = Column(Integer, nullable=True)
    idade_minima = Column(Integer, nullable=True)
    editora = Column(String(100), nullable=True)
    avaliacao = Column(Float, nullable=True)
    data_aquisicao = Column(Date, nullable=False)

    def __init__(self, nome_jogo, quantidade_minima, quantidade_maxima, idade_minima, editora, avaliacao, data_aquisicao):
        self.nome_jogo = nome_jogo
        self.quantidade_minima = quantidade_minima
        self.quantidade_maxima = quantidade_maxima
        self.idade_minima = idade_minima
        self.editora = editora
        self.avaliacao = avaliacao
        self.data_aquisicao = data_aquisicao