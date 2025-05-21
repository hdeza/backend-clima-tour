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
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='itineraries')
    city = models.CharField(max_length=128)
    creation_date = models.DateTimeField(auto_now_add=True)
    predicted_temperature = models.FloatField(null=True, blank=True)
    state = models.CharField(max_length=100)

    def __str__(self):
        return f"Itinerario de {self.user.email} en {self.city} - {self.state}"


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='activities')
    hour = models.TimeField()
    description = models.TextField()
    state = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.hour} - {self.description[:20]}..."
