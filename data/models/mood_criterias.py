import sqlalchemy
from data.service.db_session import SqlAlchemyBase


class MoodCriteria(SqlAlchemyBase):
    __tablename__ = 'mood_criterias'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
