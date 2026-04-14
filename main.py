import argparse
import logging
from connect import Session
from models import Teacher, Group, Student, Subject, Grade

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

MODELS = {
    "Teacher": Teacher,
    "Group": Group,
    "Student": Student,
    "Subject": Subject,
    "Grade": Grade,
}

# --- CRUD операції ---


def create(args):
    with Session() as session:
        try:
            model_class = MODELS.get(args.model)
            if not model_class:
                logger.error(
                    f"Помилка: Модель {args.model} не знайдена у списку доступних"
                )
                return

            data = {}

            if args.model == "Teacher":
                data = {"fullname": args.name}

            elif args.model == "Group":
                data = {"name": args.name}

            elif args.model == "Student":
                if not args.group_id:
                    logger.error(
                        "Помилка: Для створення студента обов'язково вкажіть --group_id"
                    )
                    return
                data = {"fullname": args.name, "group_id": args.group_id}

            elif args.model == "Subject":
                if not args.teacher_id:
                    logger.error(
                        "Помилка: Для створення предмета обов'язково вкажіть --teacher_id"
                    )
                    return
                data = {"name": args.name, "teacher_id": args.teacher_id}

            elif args.model == "Grade":
                if not all([args.grade, args.student_id, args.subject_id]):
                    logger.error(
                        "Помилка: Для оцінки потрібні --grade, --student_id та --subject_id"
                    )
                    return
                data = {
                    "grade": args.grade,
                    "student_id": args.student_id,
                    "subject_id": args.subject_id,
                }

            if data:
                new_record = model_class(**data)
                session.add(new_record)
                session.commit()

                display_info = getattr(
                    new_record,
                    "fullname",
                    getattr(new_record, "name", f"ID: {new_record.id}"),
                )
                logger.info(
                    f"Успішно створено запис у моделі {args.model}: {display_info}"
                )
            else:
                logger.warning(f"Не вдалося зібрати дані для моделі {args.model}")

        except Exception as e:
            session.rollback()
            logger.error(f"Помилка бази даних: {e}")


def list_records(args):
    with Session() as session:
        try:
            model_class = MODELS.get(args.model)
            if not model_class:
                logger.error(f"Помилка: Модель {args.model} не знайдена")
                return

            records = session.query(model_class).all()
            if not records:
                logger.info(f"Записи у моделі {args.model} відсутні")
                return

            logger.info(f"Список записів моделі {args.model}:")
            logger.info("-" * 30)

            for r in records:
                if args.model == "Grade":
                    logger.info(
                        f"ID: {r.id} | Оцінка: {r.grade} | Студент ID: {r.student_id} | Предмет ID: {r.subject_id}"
                    )
                else:
                    name = getattr(r, "fullname", getattr(r, "name", "Без імені"))
                    extra = ""
                    if args.model == "Student":
                        extra = f" | Група ID: {r.group_id}"
                    elif args.model == "Subject":
                        extra = f" | Викладач ID: {r.teacher_id}"
                    logger.info(f"ID: {r.id} | Назва: {name}{extra}")

        except Exception as e:
            logger.error(f"Помилка при отриманні списку: {e}")


def update(args):
    with Session() as session:
        try:
            model_class = MODELS.get(args.model)
            record = session.get(model_class, args.id)

            if not record:
                logger.error(f"Помилка: Запис з ID {args.id} не знайдено")
                return

            if args.name:
                if hasattr(record, "fullname"):
                    record.fullname = args.name
                else:
                    record.name = args.name

            if args.group_id and hasattr(record, "group_id"):
                record.group_id = args.group_id
            if args.teacher_id and hasattr(record, "teacher_id"):
                record.teacher_id = args.teacher_id
            if args.grade and hasattr(record, "grade"):
                record.grade = args.grade

            session.commit()
            logger.info(f"Запис ID {args.id} у моделі {args.model} успішно оновлено")
        except Exception as e:
            session.rollback()
            logger.error(f"Помилка при оновленні: {e}")


def remove(args):
    with Session() as session:
        try:
            model_class = MODELS.get(args.model)
            record = session.get(model_class, args.id)

            if not record:
                logger.error(f"Помилка: Запис з ID {args.id} не знайдено")
                return

            session.delete(record)
            session.commit()
            logger.info(f"Запис ID {args.id} видалено з моделі {args.model}")
        except Exception as e:
            session.rollback()
            logger.error(f"Помилка при видаленні: {e}")


# --- CLI ---


def main():
    parser = argparse.ArgumentParser(description="CRUD CLI утиліта")

    parser.add_argument(
        "-a", "--action", choices=["create", "list", "update", "remove"], required=True
    )
    parser.add_argument("-m", "--model", choices=MODELS.keys(), required=True)

    parser.add_argument("--id", type=int, help="ID запису")
    parser.add_argument("-n", "--name", help="Ім'я або назва")
    parser.add_argument("--group_id", type=int, help="ID групи")
    parser.add_argument("--teacher_id", type=int, help="ID викладача")
    parser.add_argument("--subject_id", type=int, help="ID предмета")
    parser.add_argument("--student_id", type=int, help="ID студента")
    parser.add_argument("--grade", type=int, help="Значення оцінки")

    args = parser.parse_args()

    if args.action == "create":
        create(args)
    elif args.action == "list":
        list_records(args)
    elif args.action == "update":
        if not args.id:
            logger.error("Помилка: Для оновлення потрібно вказати --id")
            return
        update(args)
    elif args.action == "remove":
        if not args.id:
            logger.error("Помилка: Для видалення потрібно вказати --id")
            return
        remove(args)


if __name__ == "__main__":
    main()
