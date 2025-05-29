from django.db import models

class Itinerary(models.Model):
    id = models.AutoField(primary_key=True)
    firebase_uid = models.CharField(max_length=128, db_index=True, null=True)  # UID de Firebase
    city = models.CharField(max_length=128)
    creation_date = models.DateTimeField(auto_now_add=True)
    predicted_temperature = models.FloatField(null=True, blank=True)
    state = models.CharField(max_length=100)

    def __str__(self):
        return f"Itinerario de {self.firebase_uid} en {self.city} - {self.state}"


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='activities')
    hour = models.TimeField()
    description = models.TextField()
    state = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.hour} - {self.description[:20]}..."
