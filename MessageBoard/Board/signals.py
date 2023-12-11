from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Comment


@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    """Сигнал инициирует отправку сообщения на эл. адрес автору объявления при получении отклика на него
    (т.е. при создании объекта класса Comment и его сохранении)"""
    if created:
        message = f'Новый отклик на объявление {instance.comment_message}. \n' \
                  f'Содержание: {instance.comment}\n' \
                  f'Автор отклика {instance.user} \n' \
                  f'Ссылка на объявление: http://127.0.0.1:8000/messages/{instance.comment_message.id}'

        html_message = (
            f'Новый отклик на объявление <a href="http://127.0.0.1:8000/messages/{instance.comment_message.id}">{instance.comment_message}</a><br>'
            f'Содержание: {instance.comment}<br>'
            f'Автор отклика {instance.user}<br>'
        )

        send_mail(
            subject=f'Уведомление о новом отклике на объявление {instance.comment_message}',
            message=message,
            html_message=html_message,
            from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
            recipient_list=[instance.comment_message.message_user.email],
        )
