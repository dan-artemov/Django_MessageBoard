from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Message
from django.core.exceptions import ValidationError


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            # 'message_user', # не требуется вывод данного поля, т.к. в соответствующем view автор будет добавлен
            'message_header',
            'message_text',
            'category',
            # 'post_type'
        ]

    def clean_post_header(self):
        name = self.cleaned_data["message_header"]
        if name[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        return name


class RegisterUserForm(UserCreationForm):
    class Meta:
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     for field in self.fields:
        #         self.fields[field].widget.attrs['class'] = 'form-control'

        model = User
        fields = ('email', 'username', 'password1', 'password2')
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-input'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-input'}),
        #
        # }

    def clean_email(self):
        """Reject usernames that differ only in case."""
        email = self.cleaned_data.get("email")
        if (
                email
                and self._meta.model.objects.filter(email__iexact=email).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "email": self.instance.unique_error_message(
                            self._meta.model, ["email"]
                        )
                    }
                )
            )
        else:
            return email


# class ConfirmForm(forms.Form):
#     class Meta:
#         model = User
#         fields = [
#             # 'message_user', # не требуется вывод данного поля, т.к. в соответствующем view автор будет добавлен
#             'message_header',
#             'message_text',
#             'category',
#             # 'post_type'
#         ]
#
#     def clean_post_header(self):
#         name = self.cleaned_data["message_header"]
#         if name[0].islower():
#             raise ValidationError(
#                 "Название должно начинаться с заглавной буквы"
#             )
#         return name