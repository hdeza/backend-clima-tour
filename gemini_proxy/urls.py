from django.urls import path
from .views import ItineraryView

urlpatterns = [
    path("itinerary/", ItineraryView.as_view(), name="itinerary"),
]
