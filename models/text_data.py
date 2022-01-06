import sqlalchemy

from service.db_session import SqlAlchemyBase


class Interpretation(SqlAlchemyBase):
    __tablename__ = 'interpretations'

    code = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    info = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
