from django.urls import path
from .views import ItineraryView, GeminiProxyView

urlpatterns = [
    path("itinerary/", ItineraryView.as_view(), name="itinerary"),
    path('generate/', GeminiProxyView.as_view(), name='gemini-generate'),
]
