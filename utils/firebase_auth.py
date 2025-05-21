import firebase_admin
from firebase_admin import auth, credentials
from rest_framework import authentication, exceptions
from api.models import Client

# Inicializa Firebase solo una vez
if not firebase_admin._apps:
    cred = credentials.Certificate("config/firebase_auth.json")
    firebase_admin.initialize_app(cred)

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        id_token = request.META.get('HTTP_AUTHORIZATION')
        if not id_token:
            return None

        if not id_token.startswith("Bearer "):
            raise exceptions.AuthenticationFailed("Formato de token inválido")

        try:
            token = id_token.split(" ")[1]
            decoded_token = auth.verify_id_token(token)
        except Exception as e:
            print(f"[FIREBASE ERROR] {e}")
            raise exceptions.AuthenticationFailed('Token inválido o expirado')

        uid = decoded_token['uid']
        email = decoded_token.get('email')
        name = decoded_token.get('name', '')

        user, _ = Client.objects.get_or_create(
            firebase_uid=uid,
            defaults={
                'email': email,
                'username': email.split('@')[0],
                'name': name.split()[0] if name else '',
                'lastname': name.split()[1] if name and len(name.split()) > 1 else ''
            }
        )

        return (user, None)
