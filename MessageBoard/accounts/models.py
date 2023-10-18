from django.db import models
from django.contrib.auth.models import User

# """!!!ПОМЕНЯТЬ В МОДЕЛИ НУЛ и БЛЭНК!!!!!!!!!!!!!!!!!"""
class VerifyUser(models.Model):
    """!!!ПОМЕНЯТЬ В МОДЕЛИ НУЛ и БЛЭНК!!!!!!!!!!!!!!!!!"""
    verify_user = models.OneToOneField(User, related_name='v_user', on_delete=models.CASCADE)
    code = models.CharField(max_length=20, default='')  # код верификации пользователя