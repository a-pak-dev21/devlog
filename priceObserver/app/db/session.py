from sqlalchemy import create_engine, Engine, Connection
from app.settings import settings
from typing import Generator, Annotated
from fastapi import Depends



def get_engine() -> Engine:
    engine = create_engine(settings.database_url)
    return engine


def get_conn(engine: Annotated[Engine, Depends(get_engine)]) -> Generator[Connection, None, None]:
    conn = engine.connect()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
