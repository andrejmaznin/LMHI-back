import sqlalchemy

from data.service.db_session import SqlAlchemyBase


class Result(SqlAlchemyBase):
    __tablename__ = 'results'

    code = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    info = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
