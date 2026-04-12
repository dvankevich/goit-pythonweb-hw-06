from sqlalchemy import text
from connect import engine


def clear_db():
    with engine.connect() as conn:
        tables = ["grades", "subjects", "students", "teachers", "groups"]
        for table in tables:
            conn.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
            conn.commit()
        print("Дані в таблицяї видалені, самі таблиці залишилися.")


if __name__ == "__main__":
    clear_db()
