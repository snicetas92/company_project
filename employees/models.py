from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


# --- 1. Менеджер для CustomUser ---
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


# --- 2. Модель CustomUser ---
class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другой'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)

    gender = models.CharField('Пол', max_length=1, choices=GENDER_CHOICES, blank=True)
    middle_name = models.CharField('Отчество', max_length=150, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def get_full_name(self):
        name = f"{self.last_name} {self.first_name}"
        if self.middle_name:
            name += f" {self.middle_name}"
        return name.strip()

    def __str__(self):
        return self.get_full_name()


# --- 3. Модель Навыка (Skill) ---
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# --- 4. Промежуточная модель для связи Сотрудник-Навык ---
class EmployeeSkill(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('employee', 'skill')


# --- 5. Модель Фотографий сотрудника ---
class EmployeePhoto(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='photos')
    image = models.ImageField(upload_to='employee_photos/')
    order_number = models.PositiveIntegerField(default=0)

    # --- 6. Класс Meta для модели EmployeePhoto ---
    # Этот блок относится ТОЛЬКО к модели EmployeePhoto
    class Meta:
        ordering = ['order_number']

    # --- 7. РЕГИСТРАЦИЯ В АДМИНКЕ (ВНИМАНИЕ: ВЫНЕСЕНА ЗА ПРЕДЕЛЫ КЛАССА META) ---


# Этот код должен быть здесь, на верхнем уровне файла, после всех моделей.
from django.contrib import admin


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):
    list_display = ('employee', 'skill', 'level')