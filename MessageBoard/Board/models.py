from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Message(models.Model):
    VARIETY = (
        ('Tanks', 'Танки'),
        ('Healers', 'Хилы'),
        ('DD', 'ДД'),
        ('Traders', 'Торговцы'),
        ('Gildmasters', 'Гилдмастеры'),
        ('Questgivers', 'Квестгиверы'),
        ('Blacksmiths', 'Кузнецы'),
        ('Tanners', 'Кожевники'),
        ('PotionMakers', 'Зельевары'),
        ('SpellMasters', 'Мастера заклинаний'),
    )

    category = models.CharField(max_length=32, choices=VARIETY, default='Tanks', blank=False)

    # Опишем базовые поля модели
    message_header = models.CharField(max_length=255, default='')  # Заголовок объявления
    message_text = models.TextField(default="")  # Текстовое содержимое объявления
    data_create = models.DateTimeField(auto_now_add=True)  # автоматически добавляемая дата и время создания объявления
    # category = models.CharField(max_length=20, choices=VARIETY, default='Tanks', blank=False)
    # picture = models.ImageField(upload_to='images/', null=True, blank=True)
    # Создадим связи с другими моделями
    # связь «один ко многим» с моделью User
    message_user = models.ForeignKey(User, related_name='m_user', on_delete=models.CASCADE)

    def preview(self):
        """Метод preview() возвращает начало объявления (предварительный просмотр) длиной 124 символа
        и добавляет многоточие в конце"""

        return self.message_text[:124] + "..."

    def __str__(self):
        return f'{self.message_header}: {self.preview()}'

    def get_absolute_url(self):
        return reverse('message_detail', args=[str(self.id)])


class Comment(models.Model):
    """
    Модель Comment.
        Позволяет оставлять отклики под каждым Объявлением.
        Модель будет иметь следующие поля:
            связь «один ко многим» с моделью Message;
            связь «один ко многим» со встроенной моделью User
            (отклики может оставить любой зарегистрированный пользователь);
            текст отклика;
            дата и время создания отклика;
            статус рассмотрения отклика: отклик может быть принят или отклонен автором объявления.
    """
    # связь «один ко многим» с моделью Message;
    comment_message = models.ForeignKey(Message, related_name='c_message', on_delete=models.CASCADE)
    # связь «один ко многим» со встроенной моделью User
    user = models.ForeignKey(User, related_name='c_user', on_delete=models.CASCADE)
    # Содержание отклика
    comment = models.TextField(default='')
    # Дата и время создания комментария;
    data_create = models.DateTimeField(auto_now_add=True)
    # Статус рассмотрения отклика (2 - отклик не рассмотрен, 1 - отклик принят, 0 - отклик отклонен).
    # По умолчанию значение поля = 2
    comment_status = models.IntegerField(default=2)  #

    # Методы accept_the_comment() и reject_the_comment() позволяют пользователю принять или отклонить отклик.
    def accept_the_comment(self):
        self.comment_status = 1
        self.save()

    def reject_the_comment(self):
        self.comment_status = 0
        self.save()

    def preview(self):
        """Метод preview() возвращает начало объявления (предварительный просмотр) длиной 124 символа
        и добавляет многоточие в конце"""

        return f'Дата создания: {self.data_create}\nСтатус_отклика: {self.comment_status}\nСодержание:{self.comment}\n'

    def __str__(self):
        return f'Дата создания: {self.data_create}\nСтатус_отклика: {self.comment_status}\nСодержание:{self.comment}\n'
