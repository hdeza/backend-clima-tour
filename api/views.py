from django.shortcuts import render
# Create your views here.
import joblib
import os 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# Cargar el modelo
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR,'modelo', 'modelo_temperatura_random_forest.pkl')
model = joblib.load(model_path) 

class PrediccionTemperatura(APIView):
    def post(self, request):
        data = request.data
        
        try: 
            #crea una lista con las caracteristicas necesarias para el modelo
            features = [
                data.get('tavg'),
                data.get('tmin'),
                data.get('tmax'),
                data.get('prcp'),
                data.get('wdir'),
                data.get('wspd'),
                data.get('pres'),
                data.get('latitude'),
                data.get('longitude')
            ]
            
            # verificamos que no haya valores nulos o faltantes
            if None in features:
                return Response({'error': 'Faltan datos necesarios'}, status=status.HTTP_400_BAD_REQUEST)
            
            #realizamos la predicción
            prediccion = model.predict([features])[0]
            
            # Devolvemos la predicción como respuesta en formato JSON
            return Response({'temperatura_predicha': prediccion}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    