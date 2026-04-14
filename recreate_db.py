from connect import engine
from models import Base


def recreate_database():
    print("Видалення таблиць...")
    Base.metadata.drop_all(bind=engine)

    print("Створення таблиць...")
    Base.metadata.create_all(bind=engine)

    print("Базу даних успішно перестворено!")


if __name__ == "__main__":
    recreate_database()
