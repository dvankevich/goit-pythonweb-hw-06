import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

URL = os.getenv("DATABASE_URL")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()), # Перетворюємо рядок "INFO" у константу logging.INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# sqlalchemy logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Створюємо engine
engine = create_engine(URL)
Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info(f"Підключення успішне! Рівень логування: {LOG_LEVEL}")
    except Exception as e:
        logger.error(f"Помилка підключення: {e}")