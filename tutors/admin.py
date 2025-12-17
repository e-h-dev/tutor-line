from django.contrib import admin
from . models import Tutors, Location, Category

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
        'name',
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
        'reviews',
        'image',
        'is_male'
    )


admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tutors, TutorAdmin)
