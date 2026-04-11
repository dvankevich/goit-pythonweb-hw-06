import logging
from sqlalchemy import func, desc, select
from connect import Session
from models import Student, Group, Teacher, Subject, Grade

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def select_1(session):
    """1.Знайти 5 студентів із найбільшим середнім балом з усіх предметів.

    SELECT s.fullname, ROUND(AVG(g.grade), 2) AS avg_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY avg_grade DESC
    LIMIT 5;
    """
    return (
        session.query(
            Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )


def select_2(session, subject_id):
    """Студент із найвищим середнім балом з певного предмета.
    SELECT s.fullname, ROUND(AVG(g.grade), 2) AS avg_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    WHERE g.subject_id = :subject_id
    GROUP BY s.id
    ORDER BY avg_grade DESC
    LIMIT 1;
    """
    return (
        session.query(
            Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .select_from(Grade)
        .join(Student)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .first()
    )


def select_3(session, subject_id):
    """3. Середній бал у групах з певного предмета.
    SELECT gr.name, ROUND(AVG(g.grade), 2) AS avg_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    JOIN groups gr ON gr.id = s.group_id
    WHERE g.subject_id = :subject_id
    GROUP BY gr.id;
    """
    return (
        session.query(
            Group.name, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )


if __name__ == "__main__":
    with Session() as session:
        try:
            # Отримуємо тестові дані
            student = session.query(Student).first()
            teacher = session.query(Teacher).first()
            group = session.query(Group).first()
            subject = session.query(Subject).first()

            if not all([student, teacher, group, subject]):
                logger.warning("База даних порожня! Спочатку запустіть seed.py")
            else:
                separator = "-" * 60

                logger.info("=" * 30 + " ЗВІТ ПО БАЗІ ДАНИХ " + "=" * 30)

                # Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
                logger.info(separator)
                logger.info(
                    f"1. 5 студентів із найбільшим середнім балом з усіх предметів:"
                )
                for name, avg in select_1(session):
                    logger.info(f" Студент: {name:<30} | Сер. бал: {avg:>5.2f}")

                # 2. студент із найвищим середнім балом з певного предмета
                logger.info(separator)
                logger.info(f"2. Найкращий студент з предмету '{subject.name}':")
                res2 = select_2(session, subject.id)
                if res2:
                    logger.info(f" Студент: {res2[0]:<30} | Сер. бал: {res2[1]:>5.2f}")

                # 3. Середній бал у групах
                logger.info(separator)
                logger.info(f"3. Середній бал у групах з предмету '{subject.name}':")
                for g_name, avg in select_3(session, subject.id):
                    logger.info(f" Група: {g_name:<10} | Сер. бал: {avg:>5.2f}")

                logger.info("\n" + "=" * 80 + "\n")

        except Exception as e:
            logger.error(f"Сталася помилка при виконанні запитів: {e}")
