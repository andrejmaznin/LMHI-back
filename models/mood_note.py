from datetime import datetime

import sqlalchemy
from sqlalchemy import orm

from service.db_session import SqlAlchemyBase


class MoodDiary(SqlAlchemyBase):
    __tablename__ = 'mood_diary'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    result = sqlalchemy.Column(sqlalchemy.ARRAY(item_type=sqlalchemy.Integer), nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.now())
