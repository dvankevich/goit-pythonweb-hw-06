import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

URL = "postgresql://postgres:567234@localhost:5432/hw04"

# echo=True щоб увімкнути логування SQLAlchemy
engine = create_engine(URL, echo=False)

Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info(f"Підключення успішне! Результат: {result.fetchone()[0]}")
    except Exception as e:
        logger.error(f"Помилка підключення до бази даних: {e}")