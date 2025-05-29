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

