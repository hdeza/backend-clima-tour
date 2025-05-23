from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth
from django.conf import settings

class FirebaseAuthView(APIView):
    def post(self, request):
        try:
            token = request.data.get('token')
            if not token:
                return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar el token con Firebase
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']

            return Response({
                'uid': uid,
                'email': decoded_token.get('email'),
                'name': decoded_token.get('name')
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_401_UNAUTHORIZED) 