import sqlalchemy
from .db_session import SqlAlchemyBase


class MoodDairyScale(SqlAlchemyBase):
    __tablename__ = 'mood_diary_scales'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
