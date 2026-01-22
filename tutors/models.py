import random
from django.db import models
from django.contrib.auth.models import User


def rand():
    """
    function to create random number between 1 and 50
    to connect to tutor model color_number, for buisness
    card unique color for each tutor registered.
    """
    return random.randint(1, 255)


class Location(models.Model):
    """
    Model to contain all possible registered
    Locations from which tutors operate from.
    """
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Model to contain the various categories
    of subjects a user can find a tutor from.
    """

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Tutors(models.Model):
    """
    Model to store all tutor information
    """

    class Meta:
        verbose_name_plural = "Tutors"

    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=254)
    location = models.ForeignKey('Location', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    date_added = models.DateField(auto_now=True)
    subject = models.CharField(max_length=254)
    price = models.IntegerField()
    active = models.BooleanField(default=True)
    description = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=14)
    rating = models.FloatField(default=0)
    image = models.ImageField(blank=True, null=True)
    is_male = models.BooleanField()
    color_1 = models.IntegerField(default=rand)
    color_2 = models.IntegerField(default=rand)
    color_3 = models.IntegerField(default=rand)
 
    def __str__(self):
        return self.user.username if self.user else "No user"


class Reviews(models.Model):
    """
    Model to store all tutor reviews
    """

    class Meta:
        verbose_name_plural = "Reveiws"
   
    name = models.CharField(max_length=254)
    tutor = models.ForeignKey('Tutors', related_name='reviews',
                                on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    review = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)

    def __str__(self):
        return self.name

