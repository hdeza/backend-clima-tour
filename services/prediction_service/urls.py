from django.urls import path
from .views import PrediccionTemperatura

urlpatterns = [
    path('predict/', PrediccionTemperatura.as_view(), name='predict_temperature'),
] 