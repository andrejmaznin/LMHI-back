import sqlalchemy

from service.db_session import SqlAlchemyBase


class MoodCriteria(SqlAlchemyBase):
    __tablename__ = 'mood_criterias'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
