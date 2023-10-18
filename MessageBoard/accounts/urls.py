from django.urls import path
# Импортируем созданное нами представление
from django.contrib.auth.views import LogoutView, LoginView

from Board.views import RegisterUser
from accounts.views import register_confirm


urlpatterns = [
   path("logout/", LogoutView.as_view(), name="logout"),
   path("login/", LoginView.as_view(), name="login1"),
   path("accounts/register/", RegisterUser.as_view(), name="register1"),

   path("accounts/login/", LoginView.as_view(), name="login"),
   path("accounts/signup/", LoginView.as_view(), name="register"),
   path("register_confirm/<int:pk>/", register_confirm, name="register_confirm"),

]
