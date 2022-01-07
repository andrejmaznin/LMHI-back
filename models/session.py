from datetime import datetime

import sqlalchemy
from sqlalchemy import orm

from service.db_session import SqlAlchemyBase


class Session(SqlAlchemyBase):
    __tablename__ = 'auth_sessions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation("User")
    date = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=datetime.utcnow().timestamp())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
