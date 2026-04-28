from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Workplace(models.Model):
    employee = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Сотрудник",
        related_name="assigned_workplace",
    )

    desk_number = models.CharField("Номер стола", max_length=20, unique=True)
    additional_info = models.TextField("Дополнительная информация", blank=True)

    # --- ВАЛИДАТОР: Проверка соседей ---
    def clean(self):
        """
        Валидатор: Разработчики и Тестировщики не могут сидеть рядом.
        """
        # Проверяем только если сотрудник назначен и у него есть рабочее место
        if self.employee and self.desk_number:

            # --- ИСПРАВЛЕНИЕ: Получаем список навыков как строки ---
            # 1. Получаем QuerySet названий навыков
            skills_qs = self.employee.employeeskill_set.values_list(
                "skill__name", flat=True
            )

            # 2. Превращаем QuerySet в список строк (list) и приводим к нижнему регистру
            # list(skills_qs) -> ['Бэкенд', 'Тестировщик']
            # [s.lower() for s in list(skills_qs)] -> ['бэкенд', 'тестировщик']
            skills_lower = [s.lower() for s in list(skills_qs)]

            # Определяем роли сотрудника
            is_developer = any(
                s in ["разработчик", "developer", "backend", "frontend"]
                for s in skills_lower
            )
            is_tester = any(
                s in ["тестировщик", "qa", "тестирование", "tester"]
                for s in skills_lower
            )

            # Если сотрудник не разработчик и не тестировщик — проверка не нужна
            if not (is_developer or is_tester):
                return

            # Определяем номера соседних столов
            try:
                current_desk_num = int(self.desk_number)
                neighbor_desks_numbers = [current_desk_num - 1, current_desk_num + 1]
                neighbor_desks = [str(num) for num in neighbor_desks_numbers]
            except ValueError:
                raise ValidationError(
                    {
                        "desk_number": "Номер стола должен быть числовым для проверки соседей."
                    }
                )

            # Ищем сотрудников за соседними столами
            neighbors = Workplace.objects.filter(
                desk_number__in=neighbor_desks, employee__isnull=False
            ).exclude(
                pk=self.pk
            )  # Исключаем самого себя

            for neighbor in neighbors:
                neighbor_skills_qs = neighbor.employee.employeeskill_set.values_list(
                    "skill__name", flat=True
                )
                neighbor_skills_lower = [s.lower() for s in list(neighbor_skills_qs)]

                neighbor_is_dev = any(
                    s in ["разработчик", "developer", "backend", "frontend"]
                    for s in neighbor_skills_lower
                )
                neighbor_is_tester = any(
                    s in ["тестировщик", "qa", "тестирование", "tester"]
                    for s in neighbor_skills_lower
                )

                # Если разработчик и сосед — тестировщик (или наоборот) -> Ошибка
                if (is_developer and neighbor_is_tester) or (
                    is_tester and neighbor_is_dev
                ):
                    raise ValidationError(
                        f"Невозможно назначить стол. За соседним столом {neighbor.desk_number} "
                        f"находится сотрудник с несовместимой ролью."
                    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
