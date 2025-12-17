from django.db import models

# Create your models here.

"""
Model to contain all possible registered
Locations from which tutors operate from.
"""


class Location(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


"""
Model to contain the various categories
of subjects a user can find a tutor from.
"""


class Category(models.Model):

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


"""
Model to store all tutor information
"""


class Tutors(models.Model):
    name = models.CharField(max_length=254)
    location = models.ForeignKey('Location', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    date_added = models.DateField(auto_now=True)
    subject = models.CharField(max_length=254, default='Chumash')
    price = models.IntegerField(default=12.5)
    active = models.BooleanField(default=True)
    description = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=14)
    rating = models.IntegerField()
    reviews = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    is_male = models.BooleanField()

    def __str__(self):
        return self.name
