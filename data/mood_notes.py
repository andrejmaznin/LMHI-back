import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from datetime import datetime


class MoodNote(SqlAlchemyBase):
    __tablename__ = 'mood_notes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    scale_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("mood_scales.id"))
    scale = orm.relation('MoodScale')
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=False, default=datetime.today)
    value = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
