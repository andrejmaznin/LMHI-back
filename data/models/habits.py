import sqlalchemy
from data.service.db_session import SqlAlchemyBase


class Habit(SqlAlchemyBase):
    __tablename__ = 'habits'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    boolean = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    lower = sqlalchemy.Column(sqlalchemy.Integer)
    upper = sqlalchemy.Column(sqlalchemy.Integer)
    value = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
