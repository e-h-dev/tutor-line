from django.contrib import admin
from . models import Tutors, Location, Category, Reviews

# Register your models here.


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


class TutorAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'name',
        'date_added',
        'location',
        'category',
        'date_added',
        'subject',
        'price',
        'active',
        'description',
        'email',
        'phone',
        'rating',
        'image',
        'is_male'
    )


class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'tutor',
        'rating',
        'review',
        'date',
        'time',
    )


admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tutors, TutorAdmin)
admin.site.register(Reviews, ReviewsAdmin)
