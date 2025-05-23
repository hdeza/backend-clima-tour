from django.urls import path
from .views import FirebaseAuthView

urlpatterns = [
    path('verify/', FirebaseAuthView.as_view(), name='firebase-auth'),
] 