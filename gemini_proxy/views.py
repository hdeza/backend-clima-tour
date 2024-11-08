
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
        prompt = f"Imagine you're a local guide in {city} and your mission is to take me on an unforgettable {days}-day experience in this city. The average temperature will be around {temperature}°C, so recommend exciting activities for each day to make the most of it. Tell me everything as if we were chatting in person: I want every activity to sound exciting, and give me practical suggestions on how to enjoy it to the fullest, such as tips on what to bring or interesting details about the place. Describe everything in a smooth, engaging way, without lists or sections. Take me day by day through the adventure as if you were accompanying me! The response must be in English. Please ensure that the total response, including both your input and output, does not exceed 800 tokens."

        # Instanciar el modelo de Gemini 
        model = genai.GenerativeModel('gemini-1.5-flash')

        try:
            # Enviar el prompt a la API de Gemini
            
            #candidateCount especifica la cantidad de respuestas generadas que se mostrarán. Actualmente, este valor solo se puede establecer en 1. 
            # Si no la estableces, el valor predeterminado será 1.

            #stopSequences especifica el conjunto de secuencias de caracteres (hasta 5) que detendrán la generación de resultados. 
            # Si se especifica, la API se detendrá cuando aparezca un stop_sequence por primera vez. La secuencia de detención no se incluirá como parte de la respuesta.

            #maxOutputTokens establece la cantidad máxima de tokens que se deben incluir en un candidato.

            #temperature controla la aleatorización de la salida. Usa valores más altos para obtener respuestas más creativas 
            # y valores más bajos para respuestas más deterministas. Los valores pueden variar de [0.0, 2.0].

            response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(
        # Only one candidate for now.
        candidate_count=1,
        max_output_tokens=800,
        temperature=0.7,
    ), )
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

