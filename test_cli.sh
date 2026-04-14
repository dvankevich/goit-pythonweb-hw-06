#!/bin/bash

# Створюємо 2 викладачів
echo "--- Створення викладачів ---"
python main.py -a create -m Teacher -n "Викладач_1"
python main.py -a create -m Teacher -n "Викладач_2"

# Створюємо 2 групи
echo "--- Створення груп ---"
python main.py -a create -m Group -n "Група_1"
python main.py -a create -m Group -n "Група_2"

# Створюємо 4 предмети
echo "--- Створення предметів ---"
python main.py -a create -m Subject -n "Предмет_1" --teacher_id 1
python main.py -a create -m Subject -n "Предмет_2" --teacher_id 1
python main.py -a create -m Subject -n "Предмет_3" --teacher_id 2
python main.py -a create -m Subject -n "Предмет_4" --teacher_id 2

# Створюємо по 5 студентів на кожну групу
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

# Приклад виставлення оцінки 
echo "--- Тестова оцінка ---"
python main.py -a create -m Grade --grade 12 --student_id 1 --subject_id 1

# Виведення списків для перевірки
echo "--- Перевірка списків ---"
python main.py -a list -m Group
python main.py -a list -m Teacher