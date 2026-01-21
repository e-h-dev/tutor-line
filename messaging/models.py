from django.db import models
from tutors.models import Tutors

# Create your models here.


class Message(models.Model):
    """
    Model for all messages information
    """

    tutor_name = models.ForeignKey(Tutors, on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    Phone = models.CharField(max_length=254)
    email = models.EmailField()
    message = models.TextField()
    day_sent = models.DateField(auto_now=True)
    time_sent = models.TimeField(auto_now=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.name

