# Файл: workplaces/tests.py

from django.db import IntegrityError, transaction
from django.test import TestCase
from django.core.exceptions import ValidationError

from workplaces.models import Workplace
from employees.models import CustomUser, Skill, EmployeeSkill


class WorkplaceModelTests(TestCase):
    def setUp(self):
        """Создаем данные для тестов."""
        self.skill_dev, _ = Skill.objects.get_or_create(name='Разработчик')
        self.skill_tester, _ = Skill.objects.get_or_create(name='Тестировщик')

        self.developer = CustomUser.objects.create_user(
            username='dev_user',
            password='devpass',
            email='dev@example.com'
        )
        EmployeeSkill.objects.create(employee=self.developer, skill=self.skill_dev, level=9)

        self.tester = CustomUser.objects.create_user(
            username='test_user',
            password='testpass',
            email='test@example.com'
        )
        EmployeeSkill.objects.create(employee=self.tester, skill=self.skill_tester, level=7)

    # --- ТЕСТ 1: Проверка валидатора (ваш код работает) ---
    def test_validator_blocks_developer_and_tester_neighbors(self):
        """
        Тест: Валидатор должен запрещать разработчику и тестировщику сидеть за соседними столами.
        """
        # Назначаем разработчика за стол 5
        Workplace.objects.create(desk_number='5', employee=self.developer)

        # Создаем новое место для тестировщика за соседним столом 6
        new_workplace = Workplace(desk_number='6', employee=self.tester)

        # Валидатор должен сработать ДО сохранения в БД
        with self.assertRaises(ValidationError):
            new_workplace.full_clean()

            # --- ТЕСТ 2: Проверка целостности БД (уровень базы данных) ---


def test_one_to_one_field_integrity(self):
    """
    Тест: Проверка, что один сотрудник не может иметь два рабочих места.
    Это проверка на уровне БД (уникальность поля OneToOneField).
    """
    # Создаем первое рабочее место
    first_workplace = Workplace(desk_number='5', employee=self.developer)
    first_workplace.save()  # Сохраняем первый объект

    # Создаем второй объект с тем же сотрудником
    second_workplace = Workplace(desk_number='6', employee=self.developer)

    # Ожидание: При попытке сохранить второй объект возникнет ошибка IntegrityError.
    # Мы используем transaction.atomic(), чтобы ошибка не прервала выполнение тестов.
    with self.assertRaises(IntegrityError), transaction.atomic():
        second_workplace.save()