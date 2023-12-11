import logging
from datetime import timedelta, datetime

from django.template.loader import render_to_string
from django.utils import timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from Board.models import *

logger = logging.getLogger(__name__)


def my_job():
    """
    Задача обеспечивает таргетированную рассылку новых объявлений
    на электронные адреса пользователей, ранее оставивших отклики в той же категории,
    к которой отнесены объявления, созданные авторами за прошедшую неделю
    """
    last_notification_date = timezone.now() - timedelta(days=7)

    # 1. Сформируем множество email пользователей, ранее оставивших хотя-бы один отклик
    emails = set(Comment.objects.all().values_list("user__email", flat=True))
    # 2. Для каждого пользователя по уникальному email формируем алгоритм рассылки
    for email in emails:
        # 3. Формируем множество категорий, соответствующи категориям, указанных в откликах пользователей по пункту 1
        categories = set(Comment.objects.filter(user__email=email).values_list("comment_message__category", flat=True))
        # 4. Выберем все объявления за неделю, у которых категория соответствует множеству из п.2.,
        #    а авторы объявления не равны пользователям из пункта 1.
        new_messages = Message.objects.filter(data_create__gte=last_notification_date,
                                              category__in=categories).exclude(message_user__email=email).order_by(
            'category')

        if len(new_messages) != 0:
            message_list = []
            # 5. Сформируем контекст рассылки для выбранного пользователя и осуществим ее
            for message in new_messages:
                message_header = message.message_header
                data_create = message.data_create
                preview = message.preview()
                pk = message.pk
                category = message.category
                link = f"http://127.0.0.1:8000/messages/{pk}"

                message_list.append({
                    'text': preview,
                    'link': link,
                    'header': message_header,
                    'data_create': data_create,
                    'category': category,
                })
            html_content = render_to_string(
                'daily_messages.html',
                {
                    'message_list': message_list,
                    'email': email,
                })

            subject = "Новые статьи на портале объявлений"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            send_mail(subject, '', from_email, recipient_list, html_message=html_content)


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        # scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="sun", hour="22", minute="32"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
