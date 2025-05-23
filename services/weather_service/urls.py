from django.urls import path
#from .views import PrediccionTemperatura
from .views import ItinerariesView, ItineraryDetailsView, ActivityListCreateView, ActivityDetailView

urlpatterns = [
    #path('predict/', PrediccionTemperatura.as_view(), name='predict_temperature'),
    path('itineraries/', ItinerariesView.as_view(), name='itinerary-list'),
    path('itineraries/<int:pk>/', ItineraryDetailsView.as_view(), name='itinerary-detail'),
    path('activities/', ActivityListCreateView.as_view(), name='activity-list'),
    path('activities/<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),
]