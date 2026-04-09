from sqlalchemy import create_engine, text
import logging

from connect import URL 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(URL)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        logger.info(f"Підключення успішне! Результат: {result.fetchone()[0]}")
except Exception as e:
    logger.error(f"Помилка підключення: {e}")