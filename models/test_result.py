from datetime import datetime

import sqlalchemy
from sqlalchemy import orm

from service.db_session import SqlAlchemyBase


class TestResult(SqlAlchemyBase):
    __tablename__ = 'test_results'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    main = sqlalchemy.Column(sqlalchemy.String)
    blue = sqlalchemy.Column(sqlalchemy.String)
    green = sqlalchemy.Column(sqlalchemy.String)
    red = sqlalchemy.Column(sqlalchemy.String)
    yellow = sqlalchemy.Column(sqlalchemy.String)

    date = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=int(datetime.now().timestamp()))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
