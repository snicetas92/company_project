from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Skill, EmployeeSkill

class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (('Дополнительно'), {
            'fields': ('gender', 'middle_name', 'description')
        }),
    )
    inlines = [EmployeeSkillInline]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Skill)