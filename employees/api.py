

from rest_framework import serializers, viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date

from employees.models import CustomUser, EmployeeSkill, Skill


# --- СЕРИАЛИЗАТОРЫ ---
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']
        read_only_fields = ['id']


class EmployeeSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        source='skill',
        write_only=True,
        required=False  # Позволяет создавать сотрудника без навыков сразу
    )

    class Meta:
        model = EmployeeSkill
        fields = ['id', 'skill', 'skill_id', 'level']
        read_only_fields = ['id']


class CustomUserSerializer(serializers.ModelSerializer):
    skills = EmployeeSkillSerializer(source='employeeskill_set', many=True, required=False)

    # Добавляем вычисляемое поле "Стаж в днях"
    tenure_days = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'password', 'email',
            'first_name', 'last_name', 'gender',
            'hire_date', 'tenure_days', 'skills'
        ]
        extra_kwargs = {'password': {'write_only': True}}  # Пароль нельзя читать через API

    def get_tenure_days(self, obj):
        """Вычисляет стаж в днях."""
        return (date.today() - obj.hire_date).days


# --- ПРАВА ДОСТУПА (PERMISSIONS) ---
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Права для Посетителей и Администраторов.
    Посетители могут только смотреть (GET).
    Админы могут делать всё.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # GET разрешен всем (Посетителям)
        return request.user and request.user.is_staff  # Остальные методы только Админам


class IsAdminOrCurator(permissions.BasePermission):
    """
    Права для Смотрителей и Администраторов.
    Оба могут изменять данные.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


# --- VIEWSETS (ЭНДПОИНТЫ) ---
class CustomUserViewSet(viewsets.ModelViewSet):
    """
    API для работы с сотрудниками.
    Поддерживает: GET (list/filter/retrieve), POST, PUT, PATCH, DELETE.
    """
    queryset = CustomUser.objects.filter(is_active=True)

    # Используем разные сериализаторы для создания и чтения (если нужно)
    # Для простоты используем один.
    serializer_class = CustomUserSerializer

    # --- ПРАВА ДОСТУПА ---
    permission_classes = [IsAdminOrReadOnly]

    # --- ФИЛЬТРАЦИЯ И ПОИСК ---
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    filterset_fields = {
        'hire_date': ['gte', 'lte'],  # Фильтр по дате (больше/меньше даты)
        'employeeskill__skill__name': ['exact'],  # Фильтр по названию навыка (строка!)
        'employeeskill__level': ['gte', 'lte'],  # Фильтр по уровню навыка (число)
        'username': ['exact'],
        'email': ['exact'],
        'first_name': ['exact', 'icontains'],
        'last_name': ['exact', 'icontains'],
        'gender': ['exact'],
    }

    search_fields = ['first_name', 'last_name', 'email']