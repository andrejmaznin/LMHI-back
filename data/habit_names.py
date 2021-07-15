import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class HabitName(SqlAlchemyBase):
    __tablename__ = 'habit_names'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
