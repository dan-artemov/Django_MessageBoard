from django.db import models
from django.contrib.auth.models import User


class VerifyUser(models.Model):
    """Класс VerifyUser расширяет встроенную модель User посредством OneToOneField
    дополнительным полем code, которое хранит уникальное значение,
    позволяющее пользователю завершить регистрацию на портале"""
    verify_user = models.OneToOneField(User, related_name='v_user', on_delete=models.CASCADE)
    code = models.CharField(max_length=20, default='')  # код верификации пользователя
