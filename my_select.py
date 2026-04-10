import logging
from sqlalchemy import func, desc, select
from connect import Session
from models import Student, Group, Teacher, Subject, Grade

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def select_1(session):
    """1.Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    return session.query(
        Student.fullname, 
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()



if __name__ == '__main__':
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
                separator = "-" * 70
                
                logger.info("\n" + "="*30 + " ЗВІТ ПО БАЗІ ДАНИХ " + "="*30)

                # Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
                logger.info(f"\n1. 5 студентів із найбільшим середнім балом з усіх предметів:")
                logger.info(separator)
                for name, avg in select_1(session):
                    logger.info(f" Студент: {name:<30} | Сер. бал: {avg:>5.2f}")



                logger.info("\n" + "="*80 + "\n")

        except Exception as e:
            logger.error(f"Сталася помилка при виконанні запитів: {e}")