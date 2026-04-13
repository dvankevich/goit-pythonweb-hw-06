import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# --- CRUD операції


def create(args):
    message = f"Дія: CREATE | Модель: {args.model}"
    if args.name:
        message += f" | Ім'я/Назва: {args.name}"
    if args.group_id:
        message += f" | ID групи: {args.group_id}"
    if args.grade:
        message += f" | Оцінка: {args.grade}"
    if args.student_id:
        message += f" | ID студента: {args.student_id}"
    if args.subject_id:
        message += f" | ID предмета: {args.subject_id}"
    logger.info(message)


def list_records(args):
    logger.info(f"Дія: LIST | Модель: {args.model} | Отримання всіх записів...")


def update(args):
    logger.info(
        f"Дія: UPDATE | Модель: {args.model} | ID: {args.id} | Нове ім'я: {args.name}"
    )


def remove(args):
    logger.info(
        f"Дія: REMOVE | Модель: {args.model} | ID: {args.id} | Видалення запису..."
    )


# --- CLI ---


def main():
    parser = argparse.ArgumentParser(description="CRUD CLI утиліта для бази даних")

    # Основні команди
    parser.add_argument(
        "-a", "--action", choices=["create", "list", "update", "remove"], required=True
    )
    parser.add_argument(
        "-m",
        "--model",
        choices=["Teacher", "Group", "Student", "Subject", "Grade"],
        required=True,
    )

    # аргументи для даних
    parser.add_argument("--id", type=int, help="ID запису")
    parser.add_argument("-n", "--name", help="Ім'я або назва")

    # аргументи для зв'язків та оцінок
    parser.add_argument("--group_id", type=int, help="ID групи для студента")
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
