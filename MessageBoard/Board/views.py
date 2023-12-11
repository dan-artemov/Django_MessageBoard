from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.encoding import escape_uri_path

from .filters import CommentFilter
from .models import *
from .forms import MessageForm, CommentForm


# Представление для вывода списка Объявлений.
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
    # имя списка, в котором будут лежать все объекты.
    context_object_name = 'messages'
    paginate_by = 5


# Представление для поиска откликов по Объявлениям, а также принятию и отклонению их
class Profile(LoginRequiredMixin, ListView):
    raise_exception = True
    model = Comment
    ordering = '-data_create'
    template_name = 'profile.html'
    context_object_name = 'comments'
    paginate_by = 10

    def get_queryset(self):
        queryset = Comment.objects.filter(comment_message__message_user_id=self.request.user)
        self.filterset = CommentFilter(self.request.GET, queryset, request=self.request.user)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


# class Profile2(LoginRequiredMixin, ListView):
#     raise_exception = True
#     # Указываем модель, объекты которой мы будем выводить
#     model = Message
#     # Поле, которое будет использоваться для сортировки объектов
#     # Объявления будем выводить с сортировкой по дате публикации: от свежей к старой
#     ordering = '-data_create'
#     # Указываем имя шаблона, в котором будут все инструкции о том,
#     # как именно пользователю должны быть показаны наши объекты
#     template_name = 'profile2.html'
#     # Это имя списка, в котором будут лежать все объекты.
#     # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
#     context_object_name = 'messages'
#     paginate_by = 10
#
#     def get_queryset(self):
#         # Получаем обычный запрос
#         queryset = super().get_queryset()
#         # Используем наш класс фильтрации.
#         # self.request.GET содержит объект QueryDict, который мы рассматривали
#         # в этом юните ранее.
#         # Сохраняем нашу фильтрацию в объекте класса,
#         # чтобы потом добавить в контекст и использовать в шаблоне.
#         self.filterset = MessageFilter(self.request.GET, queryset)
#         return self.filterset.qs.filter(message_user_id=self.request.user)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Добавляем в контекст объект фильтрации.
#         context['filterset'] = self.filterset
#         return context

# Представление для изменения статуса отклика и отправки уведомления пользователю.
@login_required
def change_status(request, c_id, m_id, command):
    st = get_object_or_404(Message, pk=m_id)
    if request.user == st.message_user:
        status = st.c_message.get(pk=c_id)
        if command == 'accept':
            status.accept_the_comment
            message = f'Принят отклик на объявление: ({st.message_header}),  http://127.0.0.1:8000/messages/{st.id}'
            html_message = 'Принят отклик на объявление: "{}", ' \
                           'доступ по ссылке http://127.0.0.1:8000/messages/{}'.format(st.message_header, st.id)
        elif command == 'reject':
            status.reject_the_comment
            message = f'Ваш отклик на объявление: ({st.message_header}) отклонен автором объявления'
            html_message = 'Ваш отклик на объявление: ({}) отклонен автором объявления'.format(st.message_header)
        send_mail(
            subject='Уведомление об изменении  состояния отклика на портале',
            message=message,
            html_message=html_message,
            from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
            recipient_list=[status.user.email],
        )
    return HttpResponseRedirect(reverse('profile'))


# Представление для вывода деталей Объявления.
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
    template_name = 'message_create.html'

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


# class RegisterUser(CreateView):
#     form_class = RegisterUserForm
#     template_name = 'registration/register.html'
#     success_url = reverse_lazy('login')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

# Представление для создания Отклика.
class CommentCreate(PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('Board.add_comment',)
    # Указываем нашу разработанную форму
    form_class = CommentForm
    # модель
    model = Comment
    # шаблон, в котором используется форма.
    template_name = 'comment_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form, ):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.comment_message = Message.objects.get(pk=self.kwargs['pk'])
        comment.save()
        return super().form_valid(form)


# Представление для скачивания файла.
def download_file(request, file_id):
    file = get_object_or_404(Message, pk=file_id)
    response = HttpResponse(file.files, content_type='application/force-download')
    response['Content-Disposition'] = "attachment; filename=" + escape_uri_path(file.filename())
    return response
