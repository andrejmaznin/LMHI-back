import sqlalchemy
from sqlalchemy import orm
from data.service.db_session import SqlAlchemyBase
from datetime import datetime


class Habit(SqlAlchemyBase):
    __tablename__ = 'habits'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation("User")
    habit_name_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("habit_names.id"))
    habit_name = orm.relation("HabitName")
    value = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.now)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
