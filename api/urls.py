from django.urls import path
#from .views import PrediccionTemperatura
from .views import ItinerariesView, ItineraryDetailsView, ActivityListCreateView, ActivityDetailView, PrediccionTemperatura

urlpatterns = [
    #path('predict/', PrediccionTemperatura.as_view(), name='predict_temperature'),
    path('itineraries/', ItinerariesView.as_view()),
    path('itineraries/<int:pk>/', ItineraryDetailsView.as_view()),
    path('activities/', ActivityListCreateView.as_view()),
    path('activities/<int:pk>/', ActivityDetailView.as_view()),
    path('predict/', PrediccionTemperatura.as_view(), name='predict_temperature'),
]