from django.urls import path
# Импортируем созданное нами представление
from .views import MessageList, MessageDetail, MessageCreate, MessageEdit, MessageDelete, CommentCreate, Profile, \
    download_file, change_status

urlpatterns = [
   path('messages/', MessageList.as_view(), name='message_list'),  # вывод Объявлений на базе ListView
   path('messages/<int:pk>', MessageDetail.as_view(), name='message_detail'),  # содержание Объявления
   path('messages/create/', MessageCreate.as_view(), name='message_create'),  # создание Объявления
   path('messages/<int:pk>/edit/', MessageEdit.as_view(), name='message_edit'),  # редактирование Объявления
   path('messages/<int:pk>/delete/', MessageDelete.as_view(), name='message_delete'),  # удаление Объявления
   path('profile/', Profile.as_view(), name='profile'),  # страница с профилем пользователя на базе ListView
   path('download/<int:file_id>/', download_file, name='download'),  # view для скачивания прикрепленного файла
   path('status/<int:c_id>/<int:m_id>/<slug:command>', change_status, name='change_status'),  # изменения Статуса
   path('comment/create/<int:pk>', CommentCreate.as_view(), name='comment_create'),  # создание Отклика

]
