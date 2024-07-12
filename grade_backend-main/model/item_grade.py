from datetime import datetime, time, date
from sqlalchemy import Column, String, Integer, Date
from model import Base
import logging

class ItemDeGrade(Base):
    __tablename__ = 'item_grade'

    id_item = Column("pk_item", Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(140), nullable=False)
    data_exib = Column(Date, nullable=False)
    inicio_exib = Column(Integer, nullable=False)
    duracao = Column(Integer, nullable=False)
    fim_exib = Column(Integer, nullable=False)

    def __init__(self, titulo: str, data_exib: date, inicio_exib: time, duracao: int):
        self.titulo = titulo
        self.data_exib = data_exib
        self.inicio_exib = self.time_to_minutes(inicio_exib)
        self.duracao = duracao
        self.fim_exib = self.calcular_fim_exib()

    def calcular_fim_exib(self) -> int:
        return self.inicio_exib + self.duracao

    @staticmethod
    def time_to_minutes(t: time) -> int:
        """Converte um objeto time para minutos desde a meia-noite."""
        return t.hour * 60 + t.minute

    @staticmethod
    def minutes_to_time(minutes: int) -> time:
        """Converte minutos desde a meia-noite de volta para um objeto time."""
        hours, minutes = divmod(minutes, 60)
        return time(hour=hours, minute=minutes)

    def to_dict(self):
        try:
            inicio_exib_time = self.minutes_to_time(self.inicio_exib)
            fim_exib_time = self.minutes_to_time(self.fim_exib)
            logging.debug(f"inicio_exib_time: {inicio_exib_time}, fim_exib_time: {fim_exib_time}")
            return {
                'id_item': self.id_item,
                'titulo': self.titulo,
                'data_exib': self.data_exib.strftime("%d/%m/%Y"),
                'inicio_exib': inicio_exib_time.strftime("%H:%M"),
                'duracao': self.duracao,
                'fim_exib': fim_exib_time.strftime("%H:%M")
            }
        except Exception as e:
            logging.error(f"Erro ao converter item {self.id_item} para dict: {e}")
            logging.error(f"Dados do item: id_item={self.id_item}, inicio_exib={self.inicio_exib}, fim_exib={self.fim_exib}")
            raise
