from django.shortcuts import render
import joblib
import os
import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Cargar el modelo
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
model_path = os.path.join(BASE_DIR, 'modelo', 'modelo_temperatura_random_forest.pkl')

try:
    model = joblib.load(model_path)
except FileNotFoundError:
    print(f"Error: No se encontró el modelo en {model_path}")
    print("Por favor, asegúrate de que el archivo modelo_temperatura_random_forest.pkl existe en la carpeta 'modelo'")
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