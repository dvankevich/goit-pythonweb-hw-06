import logging
from sqlalchemy import func, desc
from connect import Session
from models import Student, Teacher, Group, Subject, Grade

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def select_11(session, student_id, teacher_id):
    """
    Середній бал, який певний викладач ставить певному студентові.
    SELECT ROUND(AVG(g.grade), 2)
    FROM grades g
    JOIN subjects sub ON sub.id = g.subject_id
    WHERE g.student_id = :student_id AND sub.teacher_id = :teacher_id;
    """
    return (
        session.query(func.round(func.avg(Grade.grade), 2))
        .select_from(Grade)
        .join(Subject)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .scalar()
    )


def select_12(session, group_id, subject_id):
    """
    Оцінки студентів у певній групі з певного предмета на останньому занятті.
    SELECT s.fullname, g.grade, g.date_received
    FROM grades g
    JOIN students s ON s.id = g.student_id
    WHERE s.group_id = :group_id
      AND g.subject_id = :subject_id
      AND g.date_received = (
          SELECT MAX(date_received)
          FROM grades g2
          JOIN students s2 ON s2.id = g2.student_id
          WHERE s2.group_id = :group_id AND g2.subject_id = :subject_id
      );
    """
    # дата останнього заняття для цієї групи та предмета
    subquery = (
        session.query(func.max(Grade.date_received))
        .select_from(Grade)
        .join(Student)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .scalar_subquery()
    )

    # оцінки за цю дату
    return (
        session.query(Student.fullname, Grade.grade, Grade.date_received)
        .select_from(Grade)
        .join(Student)
        .filter(
            Student.group_id == group_id,
            Grade.subject_id == subject_id,
            Grade.date_received == subquery,
        )
        .all()
    )


if __name__ == "__main__":
    with Session() as session:
        try:
            student = session.query(Student).first()
            teacher = session.query(Teacher).first()
            group = session.query(Group).first()
            subject = session.query(Subject).first()

            if not all([student, teacher, group, subject]):
                logger.warning("База даних порожня! Запустіть seed.py")
            else:
                logger.info("=" * 20 + " ДОДАТКОВІ ЗАПИТИ " + "=" * 20)

                # Середній бал, який певний викладач ставить певному студентові.
                avg_val = select_11(session, student.id, teacher.id)
                logger.info("-" * 70)
                logger.info(
                    f"11. Середній бал від викладача {teacher.fullname} для студента {student.fullname}:"
                )
                logger.info(f"     Результат: {avg_val if avg_val else 'Оцінок немає'}")

                # Оцінки студентів у певній групі з певного предмета на останньому занятті
                logger.info("-" * 70)
                logger.info(
                    f"12. Оцінки групи {group.name} з предмета '{subject.name}' на останньому занятті:"
                )
                res12 = select_12(session, group.id, subject.id)

                if res12:
                    for name, grade, date in res12:
                        fmt_date = date.strftime("%d.%m.%Y")
                        logger.info(
                            f" {name:<30} | Оцінка: {grade:>2} | Дата: {fmt_date}"
                        )
                else:
                    logger.info(" Даних про останнє заняття не знайдено.")

                logger.info("=" * 60 + "\n")

        except Exception as e:
            logger.error(f"Помилка при виконанні запитів: {e}")
