import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# --- CRUD операції ---

def create(args):
    message = f"Дія: CREATE | Модель: {args.model}"
    
    if args.name:
        message += f" | Ім'я/Назва: {args.name}"
    
    # Зв'язок: Студент -> Група
    if args.model == "Student" and args.group_id:
        message += f" | ID групи: {args.group_id}"
        
    # Зв'язок: Предмет -> Викладач
    if args.model == "Subject" and args.teacher_id:
        message += f" | ID викладача: {args.teacher_id}"
        
    # Зв'язок: Оцінка -> Студент + Предмет
    if args.model == "Grade":
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