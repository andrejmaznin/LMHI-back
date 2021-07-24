import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Session(SqlAlchemyBase):
    __tablename__ = 'auth_sessions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation("User")
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)