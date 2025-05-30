import os
import google.generativeai as genai
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
import json

# Configura la API de Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class ItineraryView(APIView):
    def post(self, request):
        city = request.data.get("city")
        temperature = request.data.get("temperature")
        days = request.data.get("days")

        # Prompt optimizado para generar JSON más conciso y dentro del límite de tokens
        prompt = f"""
        Create a {days}-day travel itinerary for {city} with temperature {temperature}°C.
        
        Return ONLY valid JSON with this exact structure:
        {{
            "itinerary": {{
                "city": "{city}",
                "predicted_temperature": {temperature},
                "state": "planificado"
            }},
            "activities": [
                {{
                    "hour": "HH:MM:SS",
                    "description": "Brief activity description (max 80 words)",
                    "state": "pendiente"
                }}
            ]
        }}
        
        Requirements:
        - Generate {days * 3} activities distributed across {days} day(s)
        - Keep descriptions under 80 words each
        - Use realistic hours (08:00:00 to 20:00:00)
        - Activities should match the temperature of {temperature}°C
        - Response must be valid JSON only, no extra text
        - All descriptions in English
        """

        model = genai.GenerativeModel('gemini-1.5-flash')

        try:
            response = model.generate_content(
                prompt, 
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    max_output_tokens=1500,  # Aumentado para dar más espacio
                    temperature=0.3,  # Reducido para más consistencia
                )
            )

            # Limpiar la respuesta de Gemini
            gemini_response_text = response.text.strip()
            
            # Remover markdown si existe
            if gemini_response_text.startswith("```json"):
                gemini_response_text = gemini_response_text[len("```json"):].strip()
            if gemini_response_text.endswith("```"):
                gemini_response_text = gemini_response_text[:-len("```")].strip()
            
            # Remover cualquier texto antes del JSON
            start_idx = gemini_response_text.find('{')
            if start_idx > 0:
                gemini_response_text = gemini_response_text[start_idx:]
            
            # Remover cualquier texto después del JSON
            # Encontrar el último } que cierre el JSON principal
            brace_count = 0
            last_brace_idx = -1
            for i, char in enumerate(gemini_response_text):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        last_brace_idx = i
                        break
            
            if last_brace_idx > 0:
                gemini_response_text = gemini_response_text[:last_brace_idx + 1]

            print(f"Cleaned Gemini response: {gemini_response_text[:500]}...")  # Log para debug

            try:
                # Intentar parsear el JSON
                itinerary_data = json.loads(gemini_response_text)
                
                # Validar estructura del JSON
                if 'itinerary' not in itinerary_data or 'activities' not in itinerary_data:
                    raise ValueError("Invalid JSON structure: missing 'itinerary' or 'activities'")
                
                # Validar que activities sea una lista
                if not isinstance(itinerary_data['activities'], list):
                    raise ValueError("'activities' must be a list")
                
                # Asegurar que predicted_temperature sea float
                if 'predicted_temperature' in itinerary_data['itinerary']:
                    itinerary_data['itinerary']['predicted_temperature'] = float(
                        itinerary_data['itinerary']['predicted_temperature']
                    )

                # Validar cada actividad
                for i, activity in enumerate(itinerary_data['activities']):
                    if not all(key in activity for key in ['hour', 'description', 'state']):
                        # Si falta algún campo, completarlo
                        activity.setdefault('hour', f"{8 + (i * 2):02d}:00:00")
                        activity.setdefault('description', f"Activity {i + 1} in {city}")
                        activity.setdefault('state', 'pendiente')

                print(f"Successfully parsed itinerary with {len(itinerary_data['activities'])} activities")
                return Response(itinerary_data, status=status.HTTP_200_OK)
                
            except json.JSONDecodeError as json_e:
                print(f"JSON decode error: {json_e}")
                print(f"Raw response length: {len(gemini_response_text)}")
                print(f"Raw response: {gemini_response_text}")
                
                # Fallback: crear un itinerario básico
                fallback_itinerary = self.create_fallback_itinerary(city, temperature, days)
                return Response(fallback_itinerary, status=status.HTTP_200_OK)
                
            except ValueError as val_e:
                print(f"Validation error: {val_e}")
                fallback_itinerary = self.create_fallback_itinerary(city, temperature, days)
                return Response(fallback_itinerary, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error generating content: {str(e)}")
            # En caso de error, devolver un itinerario básico
            fallback_itinerary = self.create_fallback_itinerary(city, temperature, days)
            return Response(fallback_itinerary, status=status.HTTP_200_OK)

    def create_fallback_itinerary(self, city, temperature, days):
        """Crea un itinerario básico en caso de fallo de Gemini"""
        activities = []
        
        base_activities = [
            ("09:00:00", f"Explore the historic center of {city}"),
            ("12:00:00", f"Lunch at a local restaurant in {city}"),
            ("15:00:00", f"Visit local attractions and parks in {city}"),
            ("18:00:00", f"Evening stroll and dinner in {city}")
        ]
        
        for day in range(days):
            for hour, desc in base_activities:
                activities.append({
                    "hour": hour,
                    "description": f"Day {day + 1}: {desc}. Temperature: {temperature}°C",
                    "state": "pendiente"
                })
        
        return {
            "itinerary": {
                "city": city,
                "predicted_temperature": float(temperature),
                "state": "planificado"
            },
            "activities": activities[:days * 3]  # Limitar a 3 actividades por día
        }


class GeminiProxyView(APIView):
    def post(self, request):
        try:
            prompt = request.data.get('prompt')
            if not prompt:
                return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)

            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model = genai.GenerativeModel('gemini-pro')

            response = model.generate_content(prompt)

            return Response({
                'response': response.text
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)