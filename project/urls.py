from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import include
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("livez/", include("health_check.urls")),
    path("silk/", include("silk.urls", namespace="silk")),
    path("~/jana_sergienko/", include("app_jana_sergienko.urls")),
]
