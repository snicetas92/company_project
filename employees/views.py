# Файл: employees/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser  # Импортируем модель напрямую, так как мы находимся в этом же приложении


# --- 1. Главная страница ---
def home(request):
    """
    Главная страница сайта.
    """
    # Получаем всех активных сотрудников и сортируем их по фамилии
    employees = CustomUser.objects.filter(is_active=True).order_by('last_name')
    return render(request, 'home.html', {'employees': employees})


# --- 2. Список сотрудников ---
def employee_list(request):
    """
    Страница со списком всех сотрудников.
    """
    employees = CustomUser.objects.filter(is_active=True).order_by('last_name')
    return render(request, 'employee_list.html', {'employees': employees})


# --- 3. Подробная карточка сотрудника ---
@login_required(login_url='/login/')  # Защищаем страницу: только для авторизованных!
def employee_detail(request, pk):
    """
    Подробная информация о конкретном сотруднике.
    Параметр pk (primary key) — это ID сотрудника в базе данных.
    """
    # Получаем объект сотрудника по ID или возвращаем ошибку 404, если не найден
    employee = get_object_or_404(CustomUser, pk=pk)

    # Получаем навыки сотрудника
    skills = employee.employeeskill_set.select_related('skill').all()

    # Получаем фотографии сотрудника
    photos = employee.photos.all()

    # Передаем все данные в шаблон
    return render(request, 'employee_detail.html', {
        'employee': employee,
        'skills': skills,
        'photos': photos,
    })


# --- 4. Страница профиля (НОВОЕ ПРЕДСТАВЛЕНИЕ) ---
@login_required(login_url='/login/')  # Защищаем страницу: только для авторизованных!
def profile(request):
    """
    Страница профиля текущего пользователя.
    """
    # Функция просто отрисовывает шаблон profile.html.
    # В шаблоне уже будет доступен объект текущего пользователя через переменную {{ user }}.
    return render(request, 'profile.html')