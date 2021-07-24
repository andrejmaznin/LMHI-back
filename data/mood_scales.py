import sqlalchemy
from .db_session import SqlAlchemyBase


class MoodScale(SqlAlchemyBase):
    __tablename__ = 'mood_scales'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
