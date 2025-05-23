from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

class Client(models.Model):
    firebase_uid = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name} {self.lastname} ({self.email})"

    @property
    def is_authenticated(self):
        return True

'''
class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
'''


class Itinerary(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Activity(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    weather_condition = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.date}"
