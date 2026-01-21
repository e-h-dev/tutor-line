from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Message(models.Model):
    """
    Model for all messages information
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    Phone = models.CharField(max_length=254)
    email = models.EmailField()
    message = models.TextField()
    day_sent = models.DateField(auto_now=True)
    time_sent = models.TimeField(auto_now=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.name

