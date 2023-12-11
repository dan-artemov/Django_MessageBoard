from django.urls import path
# Импортируем созданное нами представление
from django.contrib.auth.views import LogoutView, LoginView
from accounts.views import register_confirm, Success


urlpatterns = [
   path("logout/", LogoutView.as_view(), name="logout"),
   path("accounts/login/", LoginView.as_view(), name="login"),
   path("accounts/signup/", LoginView.as_view(), name="register"),
   path("register_confirm/<int:pk>/", register_confirm, name="register_confirm"),
   path("success/", Success.as_view(), name="success"),

]
