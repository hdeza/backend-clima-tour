from django.urls import path
from .views import ItineraryView

urlpatterns = [
    path("ai/itinerary/", ItineraryView.as_view(), name="itinerary"),
]
