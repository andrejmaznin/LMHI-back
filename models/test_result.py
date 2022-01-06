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
    result = sqlalchemy.Column(sqlalchemy.ARRAY(item_type=sqlalchemy.String), nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.now())
