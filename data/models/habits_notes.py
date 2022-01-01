import sqlalchemy
from sqlalchemy import orm
from data.service.db_session import SqlAlchemyBase
from datetime import datetime


class HabitNote(SqlAlchemyBase):
    __tablename__ = 'habit_notes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation("User")
    habit_name_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("habits.id"))
    habit_name = orm.relation("Habit")
    value = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.now)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
