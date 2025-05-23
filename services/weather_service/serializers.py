from rest_framework import serializers
from .models import Itinerary, Activity


'''
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
'''

class ItinerarySerializer(serializers.ModelSerializer):
    activities = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Itinerary
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'activities', 'created_at', 'updated_at']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'title', 'description', 'date', 'location', 'weather_condition', 'created_at', 'updated_at']
