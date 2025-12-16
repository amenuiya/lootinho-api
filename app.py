from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from flask import redirect
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from model import Session
from model.jogo import Jogo
from model.expansao import Expansao
from schemas import *

info = Info(title="Lootinho API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, resources={r"/*": {"origins": "*"}})


boardgame_base = Tag(name="BoardGame", description="Gerenciamento de boardgames")
boardgame_exp = Tag(name="Expansão", description="Gerenciamento de boardgames")

@app.get('/')
def home():
    """Redireciona para o swagger
    """
    return redirect('/openapi/swagger')


@app.post('/boardgame', tags=[boardgame_base],
          responses={"201": JogoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_boardgame(form: JogoSchema):
    """Adiciona um novo Jogo à base de dados"""
    try:
        # Converte a data de string (DD-MM-YYYY) para objeto datetime.date
        data_aquisicao = datetime.strptime(form.data_aquisicao, "%d-%m-%Y").date()

        jogo = Jogo(
            nome_jogo=form.nome_jogo,
            quantidade_minima=form.quantidade_minima,
            quantidade_maxima=form.quantidade_maxima,
            idade_minima=form.idade_minima,
            editora=form.editora,
            avaliacao=form.avaliacao,
            data_aquisicao=data_aquisicao  # Agora é um objeto 'date'
        )

        session = Session()
        session.add(jogo)
        session.commit()

        return {"message": "Jogo adicionado com sucesso!"}

    except IntegrityError:
        return {"message": "Jogo de mesmo nome já salvo na base :/"}, 409

    except Exception as e:
        return {"message": f"Não foi possível salvar novo item :/ ({e})"}, 400
    
@app.get('/boardgame', tags=[boardgame_base],
          responses={"200": ListagemJogosSchema, "404": ErrorSchema})
def get_all_boardgame():
    session = Session()
    jogos = session.query(Jogo).all()

    if not jogos: 
        return {"jogos": []}, 200 
    else: 
        return apresenta_todos_jogos(jogos), 200
    
@app.get("/boardgame/<int:id_jogo>",tags =[boardgame_base], responses={"200": JogoViewSchema, "404": ErrorSchema}
)
def buscar_jogo_por_id(path: JogosBuscaIdSchema):
    """Busca um jogo pelo ID"""
    session = Session()

    jogo = (
        session.query(Jogo)
        .filter(Jogo.id_jogo == path.id_jogo)
        .first()
    )

    if not jogo:
        return {"error": "Jogo não encontrado"}, 404

    return {
        "id_jogo": jogo.id_jogo,
        "nome_jogo": jogo.nome_jogo,
        "quantidade_minima": jogo.quantidade_minima,
        "quantidade_maxima": jogo.quantidade_maxima,
        "idade_minima": jogo.idade_minima,
        "editora": jogo.editora,
        "avaliacao": jogo.avaliacao,
        "data_aquisicao": jogo.data_aquisicao.strftime('%d-%m-%Y')
    }, 200

@app.put("/boardgame", tags=[boardgame_base], responses={"200": MensagemSchema, "400": ErrorSchema, "404": ErrorSchema})
def atualizar_jogo(body: JogosUpdateSchema):
    """Atualiza um jogo existente"""
    try:
        session = Session()
        jogo = session.query(Jogo).filter(Jogo.id_jogo == body.id_jogo).first()
        
        if not jogo:
            return {"error": "Jogo não encontrado"}, 404
        
        if body.nome_jogo is not None:
            jogo.nome_jogo = body.nome_jogo
        if body.quantidade_minima is not None:
            jogo.quantidade_minima = body.quantidade_minima
        if body.quantidade_maxima is not None:
            jogo.quantidade_maxima = body.quantidade_maxima
        if body.idade_minima is not None:
            jogo.idade_minima = body.idade_minima
        if body.editora is not None:
            jogo.editora = body.editora
        if body.avaliacao is not None:
            jogo.avaliacao = body.avaliacao
        if body.data_aquisicao is not None:
            jogo.data_aquisicao = datetime.strptime(
                body.data_aquisicao, "%d-%m-%Y"
            ).date()
        
        session.commit()
        return {"message": "Jogo atualizado com sucesso!"}
    
    except IntegrityError as e:
        session.rollback()
        return {"error": f"Erro de integridade: {str(e)}"}, 400
    
    except Exception as e:
        session.rollback()
        return {"error": f"Erro ao atualizar jogo: {str(e)}"}, 400

@app.delete('/boardgame', tags=[boardgame_base],
            responses={"200": JogosDeleteSchema, "404": ErrorSchema})
def del_jogo(query: JogosDeleteSchema):
    """Deleta um Jogo a partir do ID de jogo informado

    Retorna uma mensagem de confirmação da remoção.
    """
    jogo_id = query.id_jogo
    session = Session()

    count = session.query(Jogo).filter(Jogo.id_jogo == jogo_id).delete()
    session.commit()

    if count:
        return {"message": "Jogo removido com sucesso", "id": str(jogo_id)}
    else:
        error_msg = "Jogo não encontrado na base :/"
        return {"message": error_msg}, 404
    
##### Expansão #####

@app.post('/expansao', tags=[boardgame_exp],
          responses={"201": ExpansaoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_expansao(form: ExpansaoSchema):
    """Adiciona uma nova Expansão à base de dados"""
    try:
        # Converte a data de string (DD-MM-YYYY) para objeto datetime.date
        data_aquisicao = datetime.strptime(form.data_aquisicao, "%d-%m-%Y").date()

        expansao = Expansao(
            nome_expansao=form.nome_expansao,
            quantidade_minima=form.quantidade_minima,
            quantidade_maxima=form.quantidade_maxima,
            idade_minima=form.idade_minima,
            editora=form.editora,
            avaliacao=form.avaliacao,
            data_aquisicao=data_aquisicao,
            id_jogo=form.id_jogo
        )

        session = Session()
        session.add(expansao)
        session.commit()

        return {"message": "Expansão adicionada com sucesso!"}

    except IntegrityError:
        return {"message": "Expansão de mesmo nome já salva na base :/"}, 409

    except Exception as e:
        return {"message": f"Não foi possível salvar novo item :/ ({e})"}, 400
    
@app.get('/expansao', tags=[boardgame_exp],
          responses={"200": ListagemExpansoesSchema, "404": ErrorSchema})
def get_all_expansao():
    session = Session()
    expansoes = session.query(Expansao).all()
    if not expansoes: 
        return {"expansoes": []}, 200 
    else: 
        return apresenta_todas_expansoes(expansoes), 200
    
@app.get("/expansao/<int:id_expansao>",tags =[boardgame_exp], responses={"200": ExpansaoViewSchema, "404": ErrorSchema}
)
def buscar_expansao_por_id(path: ExpansaoBuscaIdSchema):
    """Busca uma expansão pelo ID"""
    session = Session()

    expansao = (
        session.query(Expansao)
        .filter(Expansao.id_expansao == path.id_expansao)
        .first()
    )

    if not expansao:
        return {"error": "Expansão não encontrada"}, 404

    return {
        "id_jogo": expansao.id_jogo,
        "id_expansao": expansao.id_expansao,
        "nome_expansao": expansao.nome_expansao,
        "quantidade_minima": expansao.quantidade_minima,
        "quantidade_maxima": expansao.quantidade_maxima,
        "idade_minima": expansao.idade_minima,
        "editora": expansao.editora,
        "avaliacao": expansao.avaliacao,
        "data_aquisicao": expansao.data_aquisicao.strftime('%d-%m-%Y')
    }, 200

@app.put("/expansao", tags=[boardgame_exp], responses={"200": MensagemSchema, "400": ErrorSchema, "404": ErrorSchema})
def atualizar_expansao(body: ExpansaoUpdateSchema):
    """Atualiza uma expansão existente"""
    try:
        session = Session()
        expansao = session.query(Expansao).filter(Expansao.id_expansao == body.id_expansao).first()
        
        if not expansao:
            return {"error": "Expansão não encontrada"}, 404
        
        if body.nome_expansao is not None:
            expansao.nome_expansao = body.nome_expansao
        if body.quantidade_minima is not None:
            expansao.quantidade_minima = body.quantidade_minima
        if body.quantidade_maxima is not None:
            expansao.quantidade_maxima = body.quantidade_maxima
        if body.idade_minima is not None:
            expansao.idade_minima = body.idade_minima
        if body.editora is not None:
            expansao.editora = body.editora
        if body.avaliacao is not None:
            expansao.avaliacao = body.avaliacao
        if body.data_aquisicao is not None:
            expansao.data_aquisicao = datetime.strptime(
                body.data_aquisicao, "%d-%m-%Y"
            ).date()
        
        session.commit()
        return {"message": "Expansão atualizada com sucesso!"}
    
    except IntegrityError as e:
        session.rollback()
        return {"error": f"Erro de integridade: {str(e)}"}, 400
    
    except Exception as e:
        session.rollback()
        return {"error": f"Erro ao atualizar expansão: {str(e)}"}, 400

@app.delete('/expansao', tags=[boardgame_exp],
            responses={"200": ExpansaoDeleteSchema, "404": ErrorSchema})
def del_expansao(query: ExpansaoDeleteSchema):
    """Deleta uma Expansão a partir do ID de expansão informado

    Retorna uma mensagem de confirmação da remoção.
    """
    expansao_id = query.id_expansao
    session = Session()

    count = session.query(Expansao).filter(Expansao.id_expansao == expansao_id).delete()
    session.commit()

    if count:
        return {"message": "Expansão removida com sucesso", "id": str(expansao_id)}
    else:
        error_msg = "Expansão não encontrada na base :/"
        return {"message": error_msg}, 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)