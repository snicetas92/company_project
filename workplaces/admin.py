# workplaces/admin.py
from django.contrib import admin
from .models import Workplace

@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    # Имена должны точно совпадать с именами полей в models.py
    list_display = ('desk_number', 'employee', 'additional_info')