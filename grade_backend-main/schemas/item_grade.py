from pydantic import BaseModel, Field
from typing import List
from model.item_grade import ItemDeGrade
from model.__init__ import Session
from datetime import datetime, time, date

class ItemDeGradeSchema(BaseModel):
    titulo: str = Field(..., description="Título do item de grade")
    data_exib: str = Field(..., description="Data de exibição no formato dia/mês/ano (dd/mm/yy)")
    inicio_exib: str = Field(..., description="Hora de início da exibição no formato HH:MM")
    duracao: int = Field(..., description="Duração do item de grade em minutos")


class ItemDeGradeBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca baseada no id """
    id_item: int = 4

class ItemDeGradeBuscaTituloSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca baseada no título """
    titulo: str = "BACK TO THE FUTURE"

class ItemDeGradeBuscaDataExibSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca baseada na data de exibição"""
    data_exib: str = Field(..., description="Data de exibição no formato dia/mês/ano (dd/mm/yy)")


class ListagemItensDeGradeSchema(BaseModel):
    """ Define como uma listagem de itens de grade será retornada """
    itens_grade: List[ItemDeGradeSchema]

class ItemDeGradeViewSchema(BaseModel):
    """ Define como um item de grade será retornado """
    id_item: int = 1
    titulo: str = "BACK TO THE FUTURE"
    data_exib: str = "12/12/2012"
    inicio_exib: str = "12:30"
    duracao: int = "120"
    fim_exib: str = "14:30"

class ItemDeGradeDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção """
    message: str
    item_grade: str

def apresenta_itensgrade(itens_grade: List[ItemDeGrade]):
    """ Retorna uma representação dos itens de grade seguindo o schema definido em ItemDeGradeViewSchema """
    result = []
    for item_grade in itens_grade:
        result.append({
            "id_item": item_grade.id_item,
            "titulo": item_grade.titulo,
            "data_exib": item_grade.data_exib.strftime("%d/%m/%Y") if isinstance(item_grade.data_exib, (date, datetime)) else item_grade.data_exib,
            "inicio_exib": ItemDeGrade.minutes_to_time(item_grade.inicio_exib).strftime("%H:%M") if isinstance(item_grade.inicio_exib, int) else item_grade.inicio_exib,
            "duracao": item_grade.duracao,
            "fim_exib": ItemDeGrade.minutes_to_time(item_grade.fim_exib).strftime("%H:%M") if isinstance(item_grade.fim_exib, int) else item_grade.fim_exib
        })
    return {"itens_grade": result}



def apresenta_itemgrade(item_grade: ItemDeGrade):
    """ Retorna uma representação do item de grade seguindo o schema definido em ItemDeGradeViewSchema """
    return {
        "id_item": item_grade.id_item,
        "titulo": item_grade.titulo,
        "data_exib": item_grade.data_exib,
        "inicio_exib": item_grade.inicio_exib,
        "duracao": item_grade.duracao,
        "fim_exib": item_grade.fim_exib,
    }

def itensgrade_dataexib(data_exib: str):
    """ Retorna uma lista de itens de grade com base na data de exibição """
    session = Session()
    try:
        itens_grade = session.query(ItemDeGrade).filter(ItemDeGrade.data_exib == data_exib).all()
    finally:
        session.close()
    return itens_grade

def itensgrade_titulo(titulo: str):
    """ Retorna uma lista de itens de grade com base no título """
    session = Session()
    try:
        itens_grade = session.query(ItemDeGrade).filter(ItemDeGrade.titulo == titulo).all()
    finally:
        session.close()
    return itens_grade

def apresenta_itensgrade_dataexib(data_exib: str):
    """ Retorna uma representação dos itens de grade com base na data de exibição """
    itens_grade = itensgrade_dataexib(data_exib)
    return apresenta_itensgrade(itens_grade)

def apresenta_itensgrade_titulo(titulo: str):
    """ Retorna uma representação dos itens de grade com base no título """
    itens_grade = itensgrade_titulo(titulo)
    return apresenta_itensgrade(itens_grade)
