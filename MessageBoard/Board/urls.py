from django.urls import path
# Импортируем созданное нами представление
from .views import MessageList, MessageDetail, MessageCreate, MessageEdit, MessageDelete

urlpatterns = [
   path('messages/', MessageList.as_view(), name='message_list'),
   path('messages/<int:pk>', MessageDetail.as_view(), name='message_detail'),
   path('messages/create/', MessageCreate.as_view(), name='message_create'),
   path('messages/<int:pk>/edit/', MessageEdit.as_view(), name='message_edit'),
   path('messages/<int:pk>/delete/', MessageDelete.as_view(), name='message_delete'),

]
