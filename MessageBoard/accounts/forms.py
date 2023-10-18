from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django import forms
from accounts.models import VerifyUser

from accounts.utils import code_generator


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        all_users = Group.objects.get(name="all_users")
        user.groups.add(all_users)
        code = code_generator()
        # user.is_active = False
        a = VerifyUser.objects.create(code=str(code), verify_user_id=user.id)
        print(a)
        confirm_link = reverse('register_confirm', args=[str(user.id)])
        print(confirm_link)
        message = f'Для завершения регистрации на сайте "Доска объявлений" http://127.0.0.1:8000/messages/ \n' \
                  f'и подтверждения адреса электронной почты введите код подтверждения = {code}, ' \
                  f'по следующей ссылке \n http://127.0.0.1:8000/{confirm_link}'


        send_mail(
            subject='Добро пожаловать на портал "Доска объявлений"!',
            message=message,
            html_message='Подтвердите email! Введите код {} перейдя по ссылке http://127.0.0.1:8000/register_confirm/{}'.format(code, user.id),
            from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
            recipient_list=[user.email],
        )
        return user

class VerifyCodeForm(forms.Form):
    code = forms.CharField(max_length=10, label='Код подтверждения')

    # def clean_code(self):
    #     code = self.cleaned_data['code']
    #     # print(f'!!!!!!{code}!!!!!')
    #     if code != '1234':
    #         # print(f'Введенный код {code} не равен 1234  !!!!!')
    #         raise ValidationError('Некорректный код подтверждения')
    #
    #     return code
