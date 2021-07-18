import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class MoodNote(SqlAlchemyBase):
    __tablename__ = 'mood_notes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    scale_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("mood_note_scales.id"))
    scale = orm.relation('MoodScale')
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    value = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
