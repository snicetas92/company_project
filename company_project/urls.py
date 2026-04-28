

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Company API",
        default_version='v1',
        description="API for employee and workplace management",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1
    path('api/v1/', include('employees.api_urls')),

    # JWT Auth
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # SWAGGER DOCUMENTATION (Красивый интерфейс)
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # REDOC DOCUMENTATION (Альтернативный вид)
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Web Interface (если нужен)
    path('', include('employees.urls')),
]