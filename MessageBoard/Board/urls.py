from django.urls import path
# Импортируем созданное нами представление
from .views import MessageList, MessageDetail

urlpatterns = [
   path('messages/', MessageList.as_view(), name='message_list'),
   path('messages/<int:pk>', MessageDetail.as_view(), name='message_detail'),
]
