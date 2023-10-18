from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import *
from .forms import MessageForm, RegisterUserForm


# Create your views here.
class MessageList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Message
    # Поле, которое будет использоваться для сортировки объектов
    # Объявления будем выводить с сортировкой по дате публикации: от свежей к старой
    ordering = '-data_create'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'messages.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'messages'
    paginate_by = 2


class MessageDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Message
    # Используем другой шаблон — product.html
    template_name = 'Detail.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'detail'


# Представление для создания Объявления.

class MessageCreate(PermissionRequiredMixin, CreateView):
    raise_exception = True
    # Все запросы не аутентифицированных пользователей будут перенаправлены на страницу входа,
    # или будут показаны ошибки HTTP 403 Forbidden, в зависимости от параметра raise_exception.
    # raise_exception = False # True переход на 403 Forbidden
    # Проверка разрешений на добавление поста
    permission_required = ('Board.add_message',)
    # Указываем нашу разработанную форму
    form_class = MessageForm
    # модель товаров
    model = Message
    # и новый шаблон, в котором используется форма.
    template_name = 'message_edit.html'

    # def form_valid(self, form):
    #     message = form.save(commit=False)
    #     # Message.categories = 'at'
    #     return super().form_valid(form)
    def form_valid(self, form):
        message = form.save(commit=False)
        message.message_user = self.request.user
        message.save()
        return super().form_valid(form)


# Представление для редактирования Объявления.
class MessageEdit(PermissionRequiredMixin, UpdateView):
    raise_exception = False
    permission_required = ('Board.change_message',)
    form_class = MessageForm
    model = Message
    template_name = 'Message_edit.html'


# Представление для удаления Объявления.
class MessageDelete(PermissionRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = ('Board.delete_message',)
    model = Message
    template_name = 'message_delete.html'
    success_url = reverse_lazy('message_list')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
