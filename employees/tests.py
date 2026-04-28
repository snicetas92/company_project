# Файл: employees/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from workplaces.models import Workplace

CustomUser = get_user_model()


class ProjectTests(TestCase):
    def setUp(self):
        """Создание данных для каждого теста."""
        # ИСПРАВЛЕНИЕ: Добавляем обязательный аргумент 'email'
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='user@example.com',  # <-- ОБЯЗАТЕЛЬНОЕ ПОЛЕ
            first_name='Иван',
            last_name='Иванов',
            hire_date='2020-01-01'
        )

        # ИСПРАВЛЕНИЕ: Добавляем email для суперпользователя
        self.admin = CustomUser.objects.create_superuser(
            username='admin',
            password='adminpassword123',
            email='admin@example.com',  # <-- ОБЯЗАТЕЛЬНОЕ ПОЛЕ
        )

        self.workplace = Workplace.objects.create(
            desk_number='10',
            employee=self.user
        )

        self.client = Client()

    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_employee_detail_anonymous_redirect(self):
        response = self.client.get(reverse('employee_detail', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/login/' in response.url)