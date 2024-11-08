
import os
import google.generativeai as genai
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status  # Para manejar códigos de estado HTTP.
# Configura la API de Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class ItineraryView(APIView):
    def post(self, request):
        # Recibe la ciudad y temperatura desde la solicitud
        city = request.data.get("city")
        temperature = request.data.get("temperature")
        days = request.data.get("days")

        # Define el prompt con los parámetros proporcionados
        prompt = f"Genera un itinerario breve y claro de {days} días para un viaje a {city} con una temperatura promedio de {temperature}°C. El itinerario debe describir las actividades que se pueden realizar cada día, presentando el título de cada día seguido de una lista de actividades. Cada actividad debe incluir: título, descripción y recomendación adicional. El formato debe ser un solo bloque de texto, fácil de leer, sin ningún tipo de formato de código, Markdown o JSON. El texto debe ser claro, directo y fluido para que el usuario pueda entender fácilmente qué hacer durante cada día del viaje. "

        # Instanciar el modelo de Gemini 
        model = genai.GenerativeModel('gemini-1.5-flash')

        try:
            # Enviar el prompt a la API de Gemini
            #temperature=0.7,  # Control creativity and randomness
            #max_tokens=150,   # Limit output length
            #top_p=0.9,        # Focus on probable tokens
            #presence_penalty=0.5,  # Penalize repeated words
            #frequency_penalty=0.5   # Penalize repeated phrases
            response = model.generate_content(prompt,temperature=0.7, max_tokens= 150, top_p=0.9,presence_penalty=0.5,frequency_penalty=0.5 )
            return Response(response.text, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f"Error generating content: {str(e)}")
            return Response({"error": str(e)}, status=400)


        
# Asi se debe enviar la información al post de la api: 

#{
#  "city": "Bogotá",
#  "temperature": 20,
#  "days": 2
#}

