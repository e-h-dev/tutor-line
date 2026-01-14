from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutors, name='tutors'),
    path('<int:tutor_id>', views.tutor_details, name='tutor_details'),
    path('create_tutor/<int:user_id>', views.create_tutor, name='create_tutor'),
    path('review_tutor/<int:tutor_id>', views.review_tutor, name='review_tutor'),
    path('image_load/<int:tutor_id>', views.image_load, name='image_load')
]
