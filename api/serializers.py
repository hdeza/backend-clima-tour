from rest_framework import serializers
from .models import Itinerary, Activity

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'itinerary', 'hour', 'description', 'state']
        read_only_fields = ['id']


class ItinerarySerializer(serializers.ModelSerializer):  # Nuevo serializer base
    class Meta:
        model = Itinerary
        fields = ['id', 'firebase_uid', 'city', 'creation_date', 'predicted_temperature', 'state']
        read_only_fields = ['id', 'creation_date', 'firebase_uid']


class ItineraryDetailSerializer(ItinerarySerializer):  # Hereda el base + activities
    activities = ActivitySerializer(many=True, read_only=True)

    class Meta(ItinerarySerializer.Meta):
        fields = ItinerarySerializer.Meta.fields + ['activities']
