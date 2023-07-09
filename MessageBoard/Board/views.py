from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *

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