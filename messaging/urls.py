from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.messaging, name='messaging'),
    path('compose_message/<int:tutor_id>', views.compose_message, name='compose_message'),
]
