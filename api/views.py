# Importamos los módulos necesarios de Django y otras bibliotecas.
from django.shortcuts import render
#import joblib  # Para cargar el modelo de Machine Learning.
import os      # Para manejar rutas de archivos en el sistema.
from rest_framework.response import Response  # Para crear respuestas HTTP en la API.
from rest_framework.views import APIView  # Para definir vistas basadas en API.
from rest_framework import status  # Para manejar códigos de estado HTTP.
#import pandas as pd  # Para manejar datos en formato tabular.
from rest_framework.permissions import IsAuthenticated

from api.serializers import ItineraryDetailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Itinerary, Activity
from .serializers import ActivitySerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Itinerary, Activity
from .serializers import (
    ItinerarySerializer,
    ItineraryDetailSerializer,
    ActivitySerializer
)

import joblib
import os
import pandas as pd

class ItinerariesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        itineraries = Itinerary.objects.filter(firebase_uid=request.user.uid)
        serializer = ItineraryDetailSerializer(itineraries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItinerarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(firebase_uid=request.user.uid)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItineraryDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, uid):
        try:
            return Itinerary.objects.get(pk=pk, firebase_uid=uid)
        except Itinerary.DoesNotExist:
            return None

    def get(self, request, pk):
        itinerary = self.get_object(pk, request.user.uid)
        if not itinerary:
            return Response({"error": "Itinerary not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItineraryDetailSerializer(itinerary)
        return Response(serializer.data)

    def put(self, request, pk):
        itinerary = self.get_object(pk, request.user.uid)
        if not itinerary:
            return Response({"error": "Itinerary not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItinerarySerializer(itinerary, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(firebase_uid=request.user.uid)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        itinerary = self.get_object(pk, request.user.uid)
        if not itinerary:
            return Response({"error": "Itinerary not found."}, status=status.HTTP_404_NOT_FOUND)
        itinerary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivityListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        activities = Activity.objects.filter(itinerary__firebase_uid=request.user.uid)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    def post(self, request):
        itinerary_id = request.data.get('itinerary')
        try:
            itinerary = Itinerary.objects.get(id=itinerary_id, firebase_uid=request.user.uid)
        except Itinerary.DoesNotExist:
            return Response({"error": "Invalid itinerary or not owned by user."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(itinerary=itinerary)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivityDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, uid):
        try:
            activity = Activity.objects.select_related('itinerary').get(pk=pk)
            if activity.itinerary.firebase_uid != uid:
                return None
            return activity
        except Activity.DoesNotExist:
            return None

    def get(self, request, pk):
        activity = self.get_object(pk, request.user.uid)
        if not activity:
            return Response({"error": "Activity not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)

    def put(self, request, pk):
        activity = self.get_object(pk, request.user.uid)
        if not activity:
            return Response({"error": "Activity not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)

        if "itinerary" in request.data:
            try:
                Itinerary.objects.get(id=request.data["itinerary"], firebase_uid=request.user.uid)
            except Itinerary.DoesNotExist:
                return Response({"error": "Cannot assign activity to itinerary not owned by you."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ActivitySerializer(activity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        activity = self.get_object(pk, request.user.uid)
        if not activity:
            return Response({"error": "Activity not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# Cargar el modelo
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Un solo nivel arriba, la raíz del proyecto
model_path = os.path.join(BASE_DIR, 'model', 'modelo_temperatura_random_forest.pkl')

try:
    model = joblib.load(model_path)
except FileNotFoundError:
    print(f"Error: No se encontró el modelo en {model_path}")
    print("Por favor, asegúrate de que el archivo modelo_temperatura_random_forest.pkl existe en la carpeta 'model'")
    model = None

class PrediccionTemperatura(APIView):
    def post(self, request):
        if model is None:
            return Response(
                {'error': 'El modelo no está disponible. Por favor, contacta al administrador.'}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        data = request.data
        
        try: 
            # Definir los nombres de las características
            feature_names = ['tavg', 'tmin', 'tmax', 'prcp', 'wdir', 'wspd', 'pres', 'latitude', 'longitude']
            
            # Crear un diccionario con los datos
            features_dict = {
                'tavg': data.get('tavg'),
                'tmin': data.get('tmin'),
                'tmax': data.get('tmax'),
                'prcp': data.get('prcp'),
                'wdir': data.get('wdir'),
                'wspd': data.get('wspd'),
                'pres': data.get('pres'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude')
            }
            
            # Verificar que no haya valores nulos o faltantes
            if None in features_dict.values():
                return Response({'error': 'Faltan datos necesarios'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear un DataFrame con los datos y los nombres de las características
            features_df = pd.DataFrame([features_dict])
            
            # Realizar la predicción
            prediccion = model.predict(features_df)[0]
            
            # Devolver la predicción como respuesta en formato JSON
            return Response({'temperatura_predicha': prediccion}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
