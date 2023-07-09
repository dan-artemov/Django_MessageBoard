from django.urls import path
# Импортируем созданное нами представление
from .views import MessageList

urlpatterns = [
   path('messages/', MessageList.as_view(), name='message_list'),
]
