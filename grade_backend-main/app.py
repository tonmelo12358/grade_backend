from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request, jsonify
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from flask_cors import CORS

from datetime import datetime
from model import Session, ItemDeGrade
from logger import logger
from schemas import *
import logging

import pytz

# Configura o logger para exibir mensagens de DEBUG e acima
logging.basicConfig(level=logging.DEBUG)

# Define o fuso horário de São Paulo
sp_timezone = pytz.timezone('America/Sao_Paulo')

info = Info(title="Grade API", version="1.0.0")
app = OpenAPI(__name__, info=info)
# Configuração CORS para permitir apenas requisições POST de qualquer origem
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
itemgrade_tag = Tag(name="Item de Grade", description="Adição, visualização e remoção de itens de grade à base à base")
filtros_tag = Tag(name="filtros", description="Adição de filtros a partir de data e título")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/item_grade', tags=[itemgrade_tag],
          responses={"200": ItemDeGradeViewSchema, "409": ErrorSchema, "400": ErrorSchema, "422": ErrorSchema})
def add_itemgrade(form: ItemDeGradeSchema):
    """Adiciona um novo item de grade à base de dados."""
    try:
        session = Session()

        data_exib = datetime.strptime(form.data_exib, "%d/%m/%y").date()
        inicio_exib = datetime.strptime(form.inicio_exib, "%H:%M").time()
        duracao = form.duracao

        # Log para registrar os dados recebidos
        logging.debug(f"Dados recebidos - Título: {form.titulo}, Data de Exibição: {form.data_exib}, "
                      f"Início de Exibição: {form.inicio_exib}, Duração: {form.duracao}")

        # Verificar se a data e a hora são posteriores à data e hora atuais
        now = datetime.now()
        datetime_inicial = datetime.combine(data_exib, inicio_exib)

        # Adicionar logs para as variáveis now e datetime_inicial
        logging.debug(f"Current datetime (now): {now}")
        logging.debug(f"Initial datetime (datetime_inicial): {datetime_inicial}")

        if datetime_inicial <= now:
            error_msg = "Não é possível adicionar itens de grade para datas ou horários anteriores ao atual."
            logger.warning(f"Erro ao adicionar item de grade: {error_msg}")
            return {"message": error_msg}, 400

        item_grade = ItemDeGrade(
            titulo=form.titulo,
            data_exib=data_exib,
            inicio_exib=inicio_exib,
            duracao=duracao
        )

        # Log para registrar o objeto item_grade criado
        logging.debug(f"Item de grade a ser adicionado: {item_grade}")

        # Verificar se há algum item de grade no mesmo dia e horário
        mesmo_dia = session.query(ItemDeGrade).filter(
            ItemDeGrade.data_exib == data_exib,
            ItemDeGrade.inicio_exib < item_grade.fim_exib,
            ItemDeGrade.fim_exib > item_grade.inicio_exib
        ).first()

        if mesmo_dia:
            error_msg = "Já existe um item de grade ocupando o mesmo horário neste dia."
            logger.warning(f"Erro ao adicionar item de grade: {error_msg}")
            return {"message": error_msg}, 409

        session.add(item_grade)
        session.commit()

        return jsonify(item_grade.to_dict()), 200

    except IntegrityError:
        error_msg = "Item de grade com mesmo id já salvo na base."
        logger.warning(f"Erro ao adicionar item de grade: {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = f"Não foi possível salvar novo item de grade. Erro: {str(e)}"
        logger.warning(f"Erro ao adicionar item de grade: {error_msg}")
        return {"message": error_msg}, 400

    finally:
        session.close()



@app.get('/item_grade', tags=[itemgrade_tag],
         responses={"200": ItemDeGradeViewSchema, "404": ErrorSchema})
def get_itemgrade(query: ItemDeGradeBuscaSchema):
    """Faz a busca por um item de grade a partir do id do item

    Retorna uma representação dos itens de grade e o título associado.
    """
    itemgrade_id = query.id_item
    logger.debug(f"Coletando dados sobre correlacao #{itemgrade_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    item_grade = session.query(ItemDeGrade).filter(ItemDeGrade.id_item == itemgrade_id).first()

    if not item_grade:
        # se o item de grade não foi encontrado
        error_msg = "item de grade não encontrado na base :/"
        logger.warning(f"Erro ao buscar itemde grade '{itemgrade_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"itemde grade econtrado: '{item_grade.id_item}'")
        # retorna a representação de correlacao
        return apresenta_itemgrade(item_grade), 200


@app.delete('/item_grade', tags=[itemgrade_tag],
            responses={"200": ItemDeGradeDelSchema, "404": ErrorSchema})
def del_itemgrade(query: ItemDeGradeBuscaSchema):
    """Deleta um item  de grade a partir do id de item de grade informado

    Retorna uma mensagem de confirmação da remoção.
    """
    itemgrade_id = request.args.get('id_item')
    print(itemgrade_id)
    logger.debug(f"Deletando dados sobre item de grade #{itemgrade_id}")

    if not itemgrade_id:
        error_msg = "ID do item de grade não foi fornecido."
        logger.warning(f"Erro ao deletar item de grade: {error_msg}")
        return {"message": error_msg}, 400

    # criando conexão com a base
    session = Session()
    try:
        # fazendo a remoção
        remover_itemgrade = session.query(ItemDeGrade).filter(ItemDeGrade.id_item == itemgrade_id).delete()
        session.commit()

        if remover_itemgrade:
            # retorna a representação da mensagem de confirmação
            logger.debug(f"Deletado item de grade #{itemgrade_id}")
            return {"message": "item de grade removido", "id": itemgrade_id}
        else:
            # se o item de grade não foi encontrado
            error_msg = "item de grade não encontrado na base :/"
            logger.warning(f"Erro ao deletar item de grade #'{itemgrade_id}', {error_msg}")
            return {"message": error_msg}, 404
    except Exception as e:
        error_msg = f"Erro ao processar a solicitação: {str(e)}"
        logger.error(f"Erro ao deletar item de grade: {error_msg}")
        return {"message": error_msg}, 400
    finally:
        session.close()



@app.get('/itens_grade', tags=[itemgrade_tag],
         responses={"200": ListagemItensDeGradeSchema, "500": ErrorSchema})
def get_todos_itensgrade():
    """Retorna todos os itens de grade cadastrados no banco de dados."""
    logger.debug("Coletando todos os itens de grade")

    session = Session()
    try:
        todos_itensgrade = session.query(ItemDeGrade).all()
        if not todos_itensgrade:
            logger.debug("Nenhum item de grade encontrado.")
            return {"itens_grade": []}, 200
        else:
            logger.debug(f"{len(todos_itensgrade)} itens de grade encontrados.")
            itens_grade_dict = []
            for item in todos_itensgrade:
                try:
                    itens_grade_dict.append(item.to_dict())
                except Exception as e:
                    logger.error(f"Erro ao converter item para dict: {e}")
            return {"itens_grade": itens_grade_dict}, 200
    except Exception as e:
        error_msg = f"Erro ao buscar todos os itens de grade: {str(e)}"
        logger.error(error_msg)
        return {"message": error_msg}, 500
    finally:
        session.close()

@app.get('/itens_grade/data_exib', tags=[itemgrade_tag],
         responses={"200": ItemDeGradeViewSchema, "404": ErrorSchema})
def get_itemgrade_dataexib(query: ItemDeGradeBuscaDataExibSchema):
    """Faz a busca por um item de grade a partir de uma data de exibição

    Retorna uma representação dos itens de grade e data de exibicao associada.
    """
    query_params = request.args
    data_str = query_params.get('data_exib')

    try:
        # Converte a string fornecida para um objeto datetime
        data = datetime.strptime(data_str, "%d/%m/%y").date()
        # Converte para string no formato yyyy-mm-dd
        data_formatada = data.strftime("%Y-%m-%d")
    except ValueError as e:
        logger.error(f"Formato de data inválido: {e}")
        return {"message": "Formato de data inválido. Use dd/mm/aa."}, 400

    logger.debug(f"Coletando dados sobre itens de grade com data = {data_formatada}")

    session = Session()
    itensgrade_dataexib = session.query(ItemDeGrade).filter(ItemDeGrade.data_exib == data_formatada).order_by(ItemDeGrade.inicio_exib).all()

    if not itensgrade_dataexib:
        # se não há itens de grade cadastrados
        return {"itens_grade": []}, 200
    else:
        logger.debug(f"{len(itensgrade_dataexib)} itens de grade encontrados")
        return apresenta_itensgrade(itensgrade_dataexib), 200


@app.get('/itens_grade/titulo', tags=[itemgrade_tag],
         responses={"200": ListagemItensDeGradeSchema, "404": ErrorSchema})
def get_itemgrade_titulo(query: ItemDeGradeBuscaTituloSchema):
    """Faz a busca por itens de grade a partir de um título

    Retorna uma representação dos itens de grade e o título associado.
    """
    query = request.args.get('titulo', '')

    logger.debug(f"Coletando dados sobre itens de grade com título contendo = {query}")

    session = Session()
    try:
        itensgrade_titulo = session.query(ItemDeGrade).filter(
            ItemDeGrade.titulo.ilike(f"%{query}%")
        ).all()

        if not itensgrade_titulo:
            logger.debug(f"Nenhum item de grade encontrado com o título contendo: {query}")
            return {"itens_grade": []}, 200
        else:
            logger.debug(f"{len(itensgrade_titulo)} itens de grade encontrados com o título contendo: {query}")
            return apresenta_itensgrade(itensgrade_titulo), 200
    except Exception as e:
        logger.error(f"Erro ao buscar itens de grade: {str(e)}")
        return jsonify({"message": str(e)}), 500
    finally:
        session.close()
