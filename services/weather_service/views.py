# Importamos los módulos necesarios de Django y otras bibliotecas.
from django.shortcuts import render, get_object_or_404
#import joblib  # Para cargar el modelo de Machine Learning.
import os      # Para manejar rutas de archivos en el sistema.
from rest_framework.response import Response  # Para crear respuestas HTTP en la API.
from rest_framework.views import APIView  # Para definir vistas basadas en API.
from rest_framework import status  # Para manejar códigos de estado HTTP.
#import pandas as pd  # Para manejar datos en formato tabular.
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
import requests
from django.conf import settings
from datetime import datetime, timedelta

from .models import Itinerary, Activity
from .serializers import ItinerarySerializer, ActivitySerializer


class ItinerariesView(APIView):
    def get(self, request):
        itineraries = Itinerary.objects.all()
        serializer = ItinerarySerializer(itineraries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItinerarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItineraryDetailsView(APIView):
    def get(self, request, pk):
        itinerary = get_object_or_404(Itinerary, pk=pk)
        serializer = ItinerarySerializer(itinerary)
        return Response(serializer.data)

    def put(self, request, pk):
        itinerary = get_object_or_404(Itinerary, pk=pk)
        serializer = ItinerarySerializer(itinerary, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        itinerary = get_object_or_404(Itinerary, pk=pk)
        itinerary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivityListCreateView(APIView):
    def get(self, request):
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivityDetailView(APIView):
    def get(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)

    def put(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        serializer = ActivitySerializer(activity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




'''

# Cargar el modelo de predicción.
# BASE_DIR obtiene el directorio base del proyecto, que es útil para construir rutas relativas.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# model_path construye la ruta completa al archivo del modelo utilizando la ruta base.
model_path = os.path.join(BASE_DIR, 'model', 'modelo_temperatura_random_forest.pkl')
# Cargamos el modelo desde el archivo .pkl utilizando joblib.
model = joblib.load(model_path) 

# Definimos una clase que maneja las predicciones de temperatura, heredando de APIView.
class PrediccionTemperatura(APIView):
    # Este método se ejecuta cuando se recibe una solicitud POST.
    def post(self, request):
        # Obtenemos los datos enviados en la solicitud.
        data = request.data
        
        try:
            # Creamos una lista con las características necesarias para el modelo de predicción.
            features = {
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
            
            # Verificamos que no haya valores nulos o faltantes en las características.
            if None in features:
                # Si hay datos faltantes, devolvemos un error con código 400 (Bad Request).
                return Response({'error': 'Faltan datos necesarios'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Realizamos la predicción utilizando el modelo cargado.
            # La función predict espera una lista de listas, por lo que envolvemos features en otra lista.
            df_dia = pd.DataFrame([features])
            prediccion = model.predict(df_dia)[0]
            
            # Devolvemos la predicción como respuesta en formato JSON con código 200 (OK).
            return Response({prediccion}, status=status.HTTP_200_OK)
        except Exception as e:
            # En caso de un error inesperado, devolvemos el mensaje de error con código 500 (Internal Server Error).
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
'''

