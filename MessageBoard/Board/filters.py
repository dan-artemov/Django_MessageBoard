from django_filters import FilterSet, CharFilter, DateTimeFilter, ChoiceFilter, ModelChoiceFilter
from django.forms import DateTimeInput
from .models import Message, Comment


# Создаем свой набор фильтров для модели Post.

class CommentFilter(FilterSet):
    status = ChoiceFilter(
        field_name='comment_status',
        label='Статус отклика',
        lookup_expr='exact',
        choices=Comment.STATUS,
        empty_label='Не выбрано'
    )
    comment_message = ModelChoiceFilter(
        queryset=Message.objects.all(),
        empty_label="Все объявления",
        label="Объявления",
        )

    header = CharFilter(
        field_name='comment_message__message_header',
        label='Посимвольный поиск',
        lookup_expr='icontains',
    )

    class Meta:
        model = Comment
        fields = {
            'comment_message': [],
        }

    def __init__(self, *args, **kwargs):
        super(CommentFilter, self).__init__(*args, **kwargs)
        self.filters['comment_message'].queryset = Message.objects.filter(message_user_id=kwargs['request'])


# class MessageFilter(FilterSet):
#     category = ChoiceFilter(
#         field_name='category',
#         lookup_expr='exact',
#         choices=Message.VARIETY,
#         label='Категория',
#         empty_label='Не выбрано'
#     )
#
#     header = CharFilter(
#         field_name='message_header',
#         label='Заголовок',
#         lookup_expr='icontains',
#     )
#
#     added_after = DateTimeFilter(
#         field_name='data_create',
#         lookup_expr='gt',
#         widget=DateTimeInput(
#             format='%Y-%m-%dT%H:%M',
#             attrs={'type': 'datetime-local'},
#
#         ),
#         label='Дата создания объявления',
#     )
#
#     status = ChoiceFilter(
#         field_name='c_message__comment_status',
#         label='Статус отклика',
#         lookup_expr='exact',
#         choices=Comment.STATUS,
#         empty_label='Не выбрано'
#     )
#
#     class Meta:
#         # В Meta классе мы должны указать Django модель,
#         # в которой будем фильтровать записи.
#         model = Message
#         # В fields мы описываем по каким полям модели
#         # будет производиться фильтрация.
#         fields = {
#             'category',
#         }
