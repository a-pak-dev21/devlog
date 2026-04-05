from sqlalchemy import create_engine, Engine
from app.settings import settings

def get_engine() -> Engine:
    engine = create_engine(settings.database_url)
    return engine


def get_conn(engine: Engine):
    conn = engine.connect()
    try:
        yield conn
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()
