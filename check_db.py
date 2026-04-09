from sqlalchemy import create_engine, text

URL = "postgresql://postgres:567234@localhost:5432/hw04"

engine = create_engine(URL)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Підключення успішне! :", result.fetchone()[0])
except Exception as e:
    print("Помилка підключення:")
    print(e)