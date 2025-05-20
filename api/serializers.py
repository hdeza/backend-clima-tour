from rest_framework import serializers
from api.models import Client, Itinerary, Activity

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

'''
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
'''

class ItinerarySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    #city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Itinerary
        fields = '__all__'
        read_only_fields = ['user', 'creation_date']

class ActivitySerializer(serializers.ModelSerializer):
    itinerary = serializers.PrimaryKeyRelatedField(queryset=Itinerary.objects.all())

    class Meta:
        model = Activity
        fields = '__all__'
