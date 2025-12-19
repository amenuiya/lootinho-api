from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from flask import redirect
from sqlalchemy.exc import IntegrityError
from model import Session, Jogo, Expansao
from schemas import *
from sqlalchemy.orm import joinedload

info = Info(title="Lootinho API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, resources={r"/*": {"origins": "*"}})

boardgame_base = Tag(name="BoardGame", description="Gerenciamento de boardgames")
boardgame_exp = Tag(name="Expansão", description="Gerenciamento de expansões")

@app.get('/')
def home():
    """Redireciona para o swagger"""
    return redirect('/openapi/swagger')


@app.post('/boardgame', tags=[boardgame_base], responses={"200": JogoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_boardgame(form: JogoSchema):
    """Adiciona um novo Jogo à base de dados"""


    jogo = Jogo(
            nome_jogo=form.nome_jogo,
            quantidade_minima=form.quantidade_minima,
            quantidade_maxima=form.quantidade_maxima,
            idade_minima=form.idade_minima,
            editora=form.editora,
            avaliacao=form.avaliacao
    )
    session = Session()

    try:
        session.add(jogo)
        session.commit()
        session.refresh(jogo)

        return {
            "id_jogo": jogo.id_jogo,
            "nome_jogo": jogo.nome_jogo,
            "quantidade_minima": jogo.quantidade_minima,
            "quantidade_maxima": jogo.quantidade_maxima,
            "idade_minima": jogo.idade_minima,
            "editora": jogo.editora,
            "avaliacao": jogo.avaliacao
        }, 200

    except IntegrityError as e:
        session.rollback()
        return {"error": f"Jogo de mesmo nome já salvo na base! {str(e)}"}, 409

    except Exception as e:
        session.rollback()
        return {"error": f"Não foi possível salvar novo jogo! {str(e)}"}, 400

    finally:
        session.close()
    
@app.get('/boardgame', tags=[boardgame_base],
          responses={"200": ListagemJogosSchema, "404": ErrorSchema})
def get_all_boardgame():
    """Retorna todos os jogos cadastrados"""
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
    try:
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
            "avaliacao": jogo.avaliacao
        }, 200

    except IntegrityError as e:
        session.rollback()
        return {"error": f"Erro de integridade: {str(e)}"}, 400
    
    except Exception as e:
        session.rollback()
        return {"error": f"Erro ao encontrar o jogo: {str(e)}"}, 400

@app.put("/boardgame", tags=[boardgame_base], responses={"200": MensagemSchema, "400": ErrorSchema, "404": ErrorSchema})
def atualizar_jogo(body: JogosUpdateSchema):
    """Atualiza um jogo existente"""
    try:
        session = Session()
        jogo = session.query(Jogo).filter(Jogo.id_jogo == body.id_jogo).first()
        
        if not jogo:
            return {"error": "Jogo não encontrado"}, 404
        
        jogo.nome_jogo = body.nome_jogo
        jogo.quantidade_minima = body.quantidade_minima
        jogo.quantidade_maxima = body.quantidade_maxima
        jogo.idade_minima = body.idade_minima
        jogo.editora = body.editora
        jogo.avaliacao = body.avaliacao
        
        
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
    """Deleta um Jogo a partir do ID de jogo informado"""
    jogo_id = query.id_jogo
    try:
        session = Session()
        jogo = session.query(Jogo).filter(Jogo.id_jogo == query.id_jogo).first()

        if jogo.expansoes:
            return {
                "error": "Este jogo possui expansões vinculadas. Remova as expansões antes."
            }, 409

        count = session.query(Jogo).filter(Jogo.id_jogo == jogo_id).delete()
        session.commit()

        if count:
            return {"message": "Jogo removido com sucesso", "id": str(jogo_id)}
    
    except IntegrityError as e:
        session.rollback()
        return {"error": f"Jogo não encontrado na base: {str(e)}"}, 404

##### Expansão #####

@app.post('/expansao', tags=[boardgame_exp], responses={"200": ExpansaoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_expansao(form: ExpansaoSchema):
    """Adiciona uma nova Expansão à base de dados"""

    expansao = Expansao(
            nome_expansao=form.nome_expansao,
            quantidade_minima=form.quantidade_minima,
            quantidade_maxima=form.quantidade_maxima,
            idade_minima=form.idade_minima,
            editora=form.editora,
            avaliacao=form.avaliacao,
            id_jogo=form.id_jogo
    )
    session = Session()
    try:
        session.add(expansao)
        session.commit()
        session.refresh(expansao)

        return {
            "id_expansao": expansao.id_expansao,
            "nome_expansao": expansao.nome_expansao,
            "quantidade_minima": expansao.quantidade_minima,
            "quantidade_maxima": expansao.quantidade_maxima,
            "idade_minima": expansao.idade_minima,
            "editora": expansao.editora,
            "avaliacao": expansao.avaliacao,
            "id_jogo": expansao.id_jogo
        }, 200

    except IntegrityError as e:
        session.rollback()
        return {"error": f"Erro de integridade: {str(e)}"}, 400
    
    except Exception as e:
        session.rollback()
        return {"error": f"Erro ao encontrar a expansão: {str(e)}"}, 400
    finally:
        session.close()

@app.get('/expansao', tags=[boardgame_exp],
          responses={"200": ListagemExpansoesSchema, "404": ErrorSchema})

def get_all_expansao():
    """Retorna todas as expansões cadastradas"""
    session = Session()
    expansoes = session.query(Expansao).options(joinedload(Expansao.jogo)).all()
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
        "avaliacao": expansao.avaliacao
    }, 200

@app.put("/expansao", tags=[boardgame_exp], responses={"200": MensagemSchema, "400": ErrorSchema, "404": ErrorSchema})
def atualizar_expansao(body: ExpansaoUpdateSchema):
    """Atualiza uma expansão existente"""
    try:
        session = Session()
        expansao = session.query(Expansao).filter(Expansao.id_expansao == body.id_expansao).first()
        
        if not expansao:
            return {"error": "Expansão não encontrada"}, 404
        
        expansao.nome_expansao = body.nome_expansao
        expansao.quantidade_minima = body.quantidade_minima
        expansao.quantidade_maxima = body.quantidade_maxima
        expansao.idade_minima = body.idade_minima
        expansao.editora = body.editora
        expansao.avaliacao = body.avaliacao
        expansao.id_jogo = body.id_jogo

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
    """Deleta uma Expansão a partir do ID de expansão informado"""
    expansao_id = query.id_expansao
    try:
        session = Session()

        count = session.query(Expansao).filter(Expansao.id_expansao == expansao_id).delete()
        session.commit()

        if count:
            return {"message": "Expansão removida com sucesso", "id": str(expansao_id)}
    
    except Exception as e:
        session.rollback()
        return {"error": f"Expansão não encontrada na base: {str(e)}"}, 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)