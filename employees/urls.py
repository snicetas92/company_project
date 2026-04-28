# Файл: employees/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Главная страница сайта
    path('', views.home, name='home'),

    # Страница со списком всех сотрудников
    path('employees/', views.employee_list, name='employee_list'),

    # Подробная карточка сотрудника.
    # <int:pk> — это динамическая часть URL, которая передает ID сотрудника в функцию.
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),

    # Страница профиля текущего пользователя.
    # Этот адрес (accounts/profile/) используется Django по умолчанию для перенаправления после входа.
    path('accounts/profile/', views.profile, name='profile'),
]