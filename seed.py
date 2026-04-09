import random
import logging
from faker import Faker
from sqlalchemy.exc import SQLAlchemyError


from connect import Session

from models import Group, Teacher, Student, Subject, Grade

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

fake = Faker('uk_UA')

def seed_database():
    session = Session()
    try:
        # групи
        groups_names = ['SE-1', 'CS-2', 'DA-3']
        groups = [Group(name=name) for name in groups_names]
        session.add_all(groups)
        
        # викладачі
        teachers = [Teacher(fullname=fake.name()) for _ in range(5)]
        session.add_all(teachers)
        
        session.commit()

        # предмети 
        subjects_names = [
            'Архітектура ПЗ', 'Паттерни проєктування', 'DevOps та CI/CD', 
            'Криптографія', 'Моделювання загроз', 
            'Безпека мереж',
            'Машинне навчання', 'Візуалізація даних',
          ]
        # викладач -> предмет
        subjects = [
            Subject(name=name, teacher_id=random.choice(teachers).id)
            for name in subjects_names
        ]
        session.add_all(subjects)
        session.commit()

        # Студенти
        students = [
            Student(fullname=fake.name(), group_id=random.choice(groups).id)
            for _ in range(50)
        ]
        session.add_all(students)
        session.commit()

        # оцінки
        grades = []
        for student in students:
            # Генеруємо від 10 до 20 оцінок для поточного студента
            number_of_grades = random.randint(10, 20)
            for _ in range(number_of_grades):
                grade = Grade(
                    grade=random.randint(1, 5),  # оцінка 
                    # випадкова дата за останній рік
                    date_received=fake.date_time_between(start_date='-1y', end_date='now'),
                    student_id=student.id,
                    subject_id=random.choice(subjects).id
                )
                grades.append(grade)
                
        session.add_all(grades)
        session.commit()

        logger.info("БД наповнено випадковими даними!")

    except SQLAlchemyError as e:
        # скасування змін при помилці
        session.rollback()
        logger.error(f"Помилка при заповненні БД: {e}")
    finally:
        # закриваємо сесію
        session.close()

if __name__ == '__main__':
    seed_database()