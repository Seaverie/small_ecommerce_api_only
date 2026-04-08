from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import EmailTokenObtainPairView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import re_path

schema_view = get_schema_view(
    openapi.Info(
        title="E-commerce API",
        default_version='v1',
        description="Backend API for e-commerce system",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.routers')),

    path('api/token/', EmailTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]

urlpatterns += [
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0)),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0)),
]