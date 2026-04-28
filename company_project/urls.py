

from django.contrib import admin
from django.urls import path, include  # Импортируем include здесь
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- API v1 ---
    # ИЗМЕНЕНИЕ: Указываем путь к новому файлу api_urls.py
    path('api/v1/', include('employees.api_urls')),

    # --- JWT Auth ---
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # --- Веб-интерфейс ---
    path('', include('employees.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)