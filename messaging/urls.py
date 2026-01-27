from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.messaging, name='messaging'),
    path('compose_message/<int:tutor_id>', views.compose_message, name='compose_message'),
    path('delete_message/<int:message_id>', views.delete_message, name='delete_message'),
    path('mark_read/<int:message_id>', views.mark_read, name='mark_read'),
]
