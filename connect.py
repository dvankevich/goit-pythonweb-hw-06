from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Ваші дані для підключення
URI = "postgresql://postgres:567234@localhost:5432/hw04"

engine = create_engine(URI, echo=False) # echo=True включить логування SQL-запитів
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Зручний контекст-менеджер для роботи з сесіями
@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()