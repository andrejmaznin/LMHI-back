import os

import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

__factory = None
SqlAlchemyBase = dec.declarative_base()


def global_init():
    global __factory

    if __factory:
        return

    conn_str = "postgresql" + os.environ['DATABASE_URL'].lstrip("postgres")
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()