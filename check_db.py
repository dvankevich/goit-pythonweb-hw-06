from sqlalchemy import create_engine, text
import logging
import os
from dotenv import load_dotenv

from connect import URL 

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()), # Перетворюємо рядок "INFO" у константу logging.INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

engine = create_engine(URL)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        logger.info(f"Підключення успішне! Рівень логування: {LOG_LEVEL}")
except Exception as e:
    logger.error(f"Помилка підключення: {e}")