
import os
import google.generativeai as genai
from rest_framework.response import Response
from rest_framework.views import APIView

# Configura la API de Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class ItineraryView(APIView):
    def post(self, request):
        # Recibe la ciudad y temperatura desde la solicitud
        city = request.data.get("city")
        temperature = request.data.get("temperature")
        days = request.data.get("days")

        # Define el prompt con los parámetros proporcionados
        prompt = f"""
Genera un itinerario de {days} días para un viaje a {city} con una temperatura promedio de {temperature}. La respuesta debe ser en formato de texto normal (no en JSON). La estructura de la respuesta debe ser la siguiente:

- Indica el destino del viaje.
- Para cada día, incluye el título del día seguido de las actividades del día.
- Cada actividad debe incluir un título, una breve descripción y una recomendación de lo que debe llevar el viajero (ropa, protección solar, agua, etc.).

El itinerario debe tener la siguiente estructura:

**Día 1 - Encanto Colonial y Ritmos caribeños:**
1. **Recorrido por el Centro Histórico:**  
   Descubre la magia de Cartagena recorriendo sus calles empedradas, admirando sus balcones coloniales, visitando la Plaza de la Aduana, el Palacio de la Inquisición y la Catedral de Cartagena. Disfruta del ambiente vibrante de la ciudad mientras aprendes sobre su rica historia y cultura.  
   *Recomendación:* Usa ropa ligera de algodón, sombrero o gorra y lentes de sol. Bebe mucha agua para mantenerte hidratado. Evita exponerse al sol entre las 12 pm y las 4 pm, las horas de mayor intensidad.

2. **Visita al Castillo San Felipe de Barajas:**  
   Explora la imponente fortaleza del siglo XVI, símbolo de la defensa de la ciudad contra los piratas. Adéntrate en sus túneles, recorre sus murallas y disfruta de las vistas panorámicas desde la cima.  
   *Recomendación:* Recuerda llevar protector solar, gorra y abundante agua. Utiliza calzado cómodo para caminar por las diferentes áreas de la fortaleza.

3. **Almuerzo con vista en el Café Havana:**  
   Disfruta de un delicioso almuerzo caribeño con vista privilegiada de la ciudad y la bahía. Deleita tu paladar con platos tradicionales como el arroz con coco, el pescado frito y las patacones.  
   *Recomendación:* Aprovecha la brisa fresca del mar mientras disfrutas de tu comida.

**Día 2 - Playas y Cultura Afro:**
1. **Día de playa en Playa Blanca:**  
   Relájate en las arenas blancas de Playa Blanca, ubicada en la Isla de Baru, a poca distancia de Cartagena. Disfruta del mar cristalino, toma el sol y disfruta de un delicioso almuerzo de mariscos en un restaurante local.  
   *Recomendación:* Usa protector solar de amplio espectro, lentes de sol, sombrero o gorra y bebe mucha agua. Evita exponerse al sol entre las 12 pm y las 4 pm.

2. **Visita a las Bodegas de Cerveza artesanal:**  
   Prueba las cervezas artesanales de Cartagena en una visita a las bodegas locales. Disfruta de una degustación de las diferentes variedades y aprende sobre el proceso de elaboración de esta bebida tradicional colombiana.  
   *Recomendación:* El ambiente de las bodegas es fresco y agradable.

**Día 3 - Historia y Sabores:**
1. **Visita al Museo Histórico Naval de Cartagena:**  
   Descubre la historia naval de Cartagena en el Museo Histórico Naval. Conoce la historia de las fortificaciones, las batallas navales y la vida de los marinos que han defendido la ciudad.  
   *Recomendación:* El museo ofrece un ambiente fresco y agradable, ideal para recorrer en tranquilidad.

2. **Recorrido en lancha por las Islas del Rosario:**  
   Navega por las aguas cristalinas del Caribe y explora las Islas del Rosario. Disfruta de la belleza natural de la zona, practica esnórquel y disfruta de un delicioso almuerzo en un restaurante de la isla.  
   *Recomendación:* Usa protector solar, lentes de sol, sombrero o gorra y bebe mucha agua.

**Recomendaciones generales:**
- Usa ropa ligera de algodón, sombrero o gorra y lentes de sol para protegerte del sol.
- Bebe mucha agua para mantenerte hidratado, especialmente durante las actividades al aire libre.
- Aprovecha las horas de menor intensidad del sol (antes de las 10 am y después de las 4 pm) para realizar actividades al aire libre.
- Aprovecha las oportunidades para refrescarte en el mar o en piscinas durante el día.
- Utiliza repelente de mosquitos, especialmente durante las horas de la tarde y la noche.
"""


        model = genai.GenerativeModel('gemini-1.5-flash')

        try:
            # Enviar el prompt a la API de Gemini
            response = model.generate_content(prompt)
            return Response(response.text)
        
        except Exception as e:
            return Response({"error": str(e)}, status=400)


        
