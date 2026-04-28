from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Подключаем URL-адреса приложения employees.
    path("", include("employees.urls")),
    # Подключаем стандартные страницы входа/выхода Django.
    path("accounts/", include("django.contrib.auth.urls")),
]

# Настройка для работы с медиа-файлами (изображениями) в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
