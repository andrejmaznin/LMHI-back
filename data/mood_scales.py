import sqlalchemy
from .db_session import SqlAlchemyBase


class MoodScale(SqlAlchemyBase):
    __tablename__ = 'mood_scales'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
