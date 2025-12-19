from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from model.base import Base

class Expansao(Base):
    __tablename__ = 'expansao'

    id_expansao = Column(Integer, primary_key=True, autoincrement=True)
    nome_expansao = Column(String(255), nullable=True)
    quantidade_minima = Column(Integer, nullable=True)
    quantidade_maxima = Column(Integer, nullable=True)
    idade_minima = Column(Integer, nullable=True)
    editora = Column(String(100), nullable=True)
    avaliacao = Column(Integer, nullable=True)
    id_jogo = Column(Integer, ForeignKey('jogo.id_jogo'), nullable=False)

    jogo = relationship("Jogo", back_populates="expansoes")

    

    def __init__(self, nome_expansao, quantidade_minima, quantidade_maxima, idade_minima, editora, avaliacao, id_jogo):
        self.nome_expansao = nome_expansao
        self.quantidade_minima = quantidade_minima
        self.quantidade_maxima = quantidade_maxima
        self.idade_minima = idade_minima
        self.editora = editora
        self.avaliacao = avaliacao
        self.id_jogo = id_jogo