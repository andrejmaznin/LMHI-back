from datetime import datetime

import sqlalchemy
from sqlalchemy import orm

from service.db_session import SqlAlchemyBase


class HabitNote(SqlAlchemyBase):
    __tablename__ = 'habit_notes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation("User")
    habit_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("habits.id"))
    habit = orm.relation("Habit")
    value = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.now)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
