import argparse
import logging
from connect import Session
from models import Teacher, Group, Student, Subject, Grade

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# --- CRUD операції ---


def create(args):
    with Session() as session:
        try:
            new_record = None

            if args.model == "Teacher":
                # Teacher використовує fullname
                new_record = Teacher(fullname=args.name)

            elif args.model == "Group":
                # Group використовує name
                new_record = Group(name=args.name)

            elif args.model == "Student":
                # Студент має fullname та group_id
                if not args.group_id:
                    logger.error(
                        "Помилка: Для створення студента обов'язково вкажіть --group_id"
                    )
                    return
                new_record = Student(fullname=args.name, group_id=args.group_id)

            elif args.model == "Subject":
                # Предмет має name та teacher_id
                if not args.teacher_id:
                    logger.error(
                        "Помилка: Для створення предмета обов'язково вкажіть --teacher_id"
                    )
                    return
                new_record = Subject(name=args.name, teacher_id=args.teacher_id)

            elif args.model == "Grade":
                # Оцінка потребує значення, student_id та subject_id
                if not all([args.grade, args.student_id, args.subject_id]):
                    logger.error(
                        "Помилка: Для оцінки потрібні --grade, --student_id та --subject_id"
                    )
                    return
                new_record = Grade(
                    grade=args.grade,
                    student_id=args.student_id,
                    subject_id=args.subject_id,
                )

            if new_record:
                session.add(new_record)
                session.commit()
                display_name = getattr(
                    new_record,
                    "fullname",
                    getattr(new_record, "name", f"ID: {new_record.id}"),
                )
                logger.info(f"Успішно створено: {args.model} -> {display_name}")
            else:
                logger.warning(
                    f"Модель {args.model} не розпізнана або дані некоректні."
                )

        except Exception as e:
            session.rollback()
            logger.error(f"Помилка бази даних: {e}")


def list_records(args):
    logger.info(f"Дія: LIST | Модель: {args.model} | Отримання всіх записів...")


def update(args):
    message = f"Дія: UPDATE | Модель: {args.model} | ID: {args.id}"
    if args.name:
        message += f" | Нове ім'я/назва: {args.name}"
    if args.group_id:
        message += f" | Новий ID групи: {args.group_id}"
    if args.teacher_id:
        message += f" | Новий ID викладача: {args.teacher_id}"
    logger.info(message)


def remove(args):
    logger.info(
        f"Дія: REMOVE | Модель: {args.model} | ID: {args.id} | Видалення запису..."
    )


# --- CLI ---


def main():
    parser = argparse.ArgumentParser(description="CRUD CLI утиліта для бази даних")

    parser.add_argument(
        "-a", "--action", choices=["create", "list", "update", "remove"], required=True
    )
    parser.add_argument(
        "-m",
        "--model",
        choices=["Teacher", "Group", "Student", "Subject", "Grade"],
        required=True,
    )

    # Аргументи для ідентифікації та базових даних
    parser.add_argument("--id", type=int, help="ID запису (для update/remove)")
    parser.add_argument("-n", "--name", help="Ім'я (fullname) або назва (name)")

    # Аргументи для зв'язків (Foreign Keys)
    parser.add_argument("--group_id", type=int, help="ID групи (для Student)")
    parser.add_argument("--teacher_id", type=int, help="ID викладача (для Subject)")
    parser.add_argument("--subject_id", type=int, help="ID предмета (для Grade)")
    parser.add_argument("--student_id", type=int, help="ID студента (для Grade)")

    # Специфічне поле для оцінок
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
