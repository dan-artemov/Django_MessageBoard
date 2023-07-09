from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Модель Category:
    Категории объявлений — темы, которые они отражают, доступные значения:
    Танки, Хилы, ДД, Торговцы, Гилдмастеры, Квестгиверы, Кузнецы, Кожевники, Зельевары, Мастера заклинаний.
    """

    # Поле category сделаем полем для выбора, для это используем параметр "choices" и список кортежей TYPE_CAT
    category = models.CharField(max_length=50, default='Танки', unique=True)

    def __str__(self):
        return f'{self.category}'


class Message(models.Model):
    # Опишем базовые поля модели
    message_header = models.CharField(max_length=255, default='')  # Заголовок объявления
    message_text = models.TextField(default="")  # Текстовое содержимое объявления
    data_create = models.DateTimeField(auto_now_add=True)  # автоматически добавляемая дата и время создания объявления

    # Создадим связи с другими моделями
    # связь «один ко многим» с моделью Category
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)
    # связь «один ко многим» с моделью User
    message_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def preview(self):
        """Метод preview() возвращает начало объявления (предварительный просмотр) длиной 124 символа
        и добавляет многоточие в конце"""

        return self.message_text[:124] + "..."

    def __str__(self):
        return f'{self.message_header}: {self.preview()}'


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
    comment_message = models.ForeignKey(Message, related_name='comments', on_delete=models.CASCADE)
    # связь «один ко многим» со встроенной моделью User
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
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
