from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutors, name='tutors'),
    path('<int:tutor_id>', views.tutor_details, name='tutor_details')
]
