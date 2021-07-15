import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class MoodDairy(SqlAlchemyBase):
    __tablename__ = 'mood_diaries'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    scale_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("mood_diary_scales.id"))
    scale = orm.relation('Scale')
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    value = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
