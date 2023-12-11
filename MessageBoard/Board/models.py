import os

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Message(models.Model):
    """
    Модель Message.
        Описывает сущность Объявления и содержит следующие поля:
            message_header: заголовок объявления;
            message_text: Текстовое содержимое объявления;
            data_create: Дата создания объявления;
            category: категория объявления, принимает значения, перечисленные в кортеже VARIETY;
            files: файл, прикрепляемый автором к Объявлению;
            photo: изображение, прикрепляемое автором к Объявлению;
            message_user: связь «один ко многим» со встроенной моделью User.
        Модель содержит следующие методы и свойства:
            preview: превью отклика, включающее дату, статус и содержание отклика;
            get_absolute_url: генерирует прямую ссылку на объявление.

    """
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

    # Опишем базовые поля модели
    message_header = models.CharField(max_length=255, default='', verbose_name='Заголовок')  # Заголовок объявления
    message_text = models.TextField(default="", verbose_name='Текст объявления')  # Текстовое содержимое объявления
    data_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')  # Дата создания объявления
    category = models.CharField(max_length=20, choices=VARIETY, default='Tanks', blank=False, verbose_name='Категория')
    files = models.FileField(upload_to='files/%Y/%m/%d', verbose_name='Файл',
                             default=None, null=True, blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото',
                              default=None, null=True, blank=True)
    # Создадим связи с другими моделями
    # связь «один ко многим» с моделью User
    message_user = models.ForeignKey(User, related_name='m_user', on_delete=models.CASCADE)

    def preview(self):
        """Метод preview() возвращает начало объявления (предварительный просмотр) длиной 124 символа
        и добавляет многоточие в конце"""

        return self.message_text[:124] + "..."

    def __str__(self):
        return f'{self.message_header}'

    def get_absolute_url(self):
        return reverse('message_detail', args=[str(self.id)])

    def filename(self):
        return os.path.basename(self.files.name)


class Comment(models.Model):
    """
    Модель Comment.
        Позволяет оставлять отклики под каждым Объявлением.
        Модель имеет следующие поля:
            comment_message: связь «один ко многим» с моделью Message;
            user: связь «один ко многим» со встроенной моделью User;
            comment: содержание отклика;
            data_create: дата и время создания отклика;
            comment_status: принимает три значения, перечисленные в кортеже STATUS.
        Модель содержит следующие методы и свойства:
            accept_the_comment: позволяет принять отклик;
            reject_the_comment: позволяет отклонить отклик;
            preview: превью отклика, включающее дату, статус и содержание отклика;
            get_absolute_url: генерирует прямую ссылку на объявление, для которого создан отклик.
    """
    STATUS = (
        (0, 'отклик отклонен'),
        (1, 'отклик принят'),
        (2, 'отклик не рассмотрен'),
    )
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
    comment_status = models.IntegerField(default=2, choices=STATUS, verbose_name='Статус отклика')  #

    class Meta:
        ordering = ['-data_create']
        indexes = [models.Index(fields=['-data_create'])]

    # Свойства accept_the_comment и reject_the_comment позволяют пользователю принять или отклонить отклик.
    @property
    def accept_the_comment(self):
        self.comment_status = 1
        self.save()

    @property
    def reject_the_comment(self):
        self.comment_status = 0
        self.save()

    def preview(self):
        """Метод preview() возвращает начало объявления (предварительный просмотр) длиной 124 символа
        и добавляет многоточие в конце"""

        return f'Дата создания: {self.data_create}\nСтатус_отклика: {self.comment_status}\nСодержание:{self.comment}\n'

    def __str__(self):
        return f'{self.preview()}'

    def get_absolute_url(self):
        return reverse('message_detail', args=[str(self.comment_message.id)])
