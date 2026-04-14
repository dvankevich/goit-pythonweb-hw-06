#!/bin/bash

echo "--- Очищення бази даних ---"
python clear_data.py

# 1. СТВОРЕННЯ (CREATE)
echo "--- Створення викладачів ---"
python main.py -a create -m Teacher -n "Викладач_1"
python main.py -a create -m Teacher -n "Викладач_2"

echo "--- Створення груп ---"
python main.py -a create -m Group -n "Група_1"
python main.py -a create -m Group -n "Група_2"

echo "--- Створення предметів ---"
python main.py -a create -m Subject -n "Предмет_1" --teacher_id 1
python main.py -a create -m Subject -n "Предмет_2" --teacher_id 1
python main.py -a create -m Subject -n "Предмет_3" --teacher_id 2
python main.py -a create -m Subject -n "Предмет_4" --teacher_id 2

echo "--- Наповнення Групи_1 (студенти 1-5) ---"
for i in {1..5}
do
   python main.py -a create -m Student -n "Студент_$i" --group_id 1
done

echo "--- Наповнення Групи_2 (студенти 6-10) ---"
for i in {6..10}
do
   python main.py -a create -m Student -n "Студент_$i" --group_id 2
done

echo "--- Масове виставлення оцінок ---"
# Виставляємо по дві оцінки першим трьом студентам
for student_id in {1..3}
do
   python main.py -a create -m Grade --grade 10 --student_id $student_id --subject_id 1
   python main.py -a create -m Grade --grade 12 --student_id $student_id --subject_id 2
done

# Додаткова оцінка для перевірки видалення самої оцінки
python main.py -a create -m Grade --grade 7 --student_id 10 --subject_id 4

# 2. ЧИТАННЯ (LIST) - Базова перевірка
echo "--- Початковий список студентів та оцінок ---"
python main.py -a list -m Student
python main.py -a list -m Grade


# 3. ОНОВЛЕННЯ (UPDATE)
echo "--- Тестування оновлення (UPDATE) ---"
# Змінюємо ім'я студента
python main.py -a update -m Student --id 1 -n "Оновлений_Студент_1"

# Переводимо студента в іншу групу
python main.py -a update -m Student --id 5 --group_id 2

# Змінюємо оцінку (припустимо, виправляємо помилку)
python main.py -a update -m Grade --id 1 --grade 11

# Змінюємо викладача для предмета
python main.py -a update -m Subject --id 1 --teacher_id 2


# 4. ВИДАЛЕННЯ (REMOVE)
echo "--- Тестування видалення (REMOVE) ---"
# Видаляємо одну конкретну оцінку (ту, що виставили студенту 10)
# ID цієї оцінки буде 7, оскільки ми перед цим створили 6 оцінок у циклі
python main.py -a remove -m Grade --id 7

# Тестуємо КАСКАДНЕ видалення: Видаляємо Студента 2
# Це має автоматично видалити його оцінки (ID 3 та 4)
python main.py -a remove -m Student --id 2


# 5. ФІНАЛЬНА ПЕРЕВІРКА
echo "--- Фінальна перевірка після змін ---"
echo "Очікуємо побачити змінене ім'я студента 1, відсутність студента 2 та відсутність його оцінок."
python main.py -a list -m Student
python main.py -a list -m Grade
python main.py -a list -m Subject

echo "--- Тестування завершено ---"