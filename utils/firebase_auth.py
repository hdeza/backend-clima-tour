import firebase_admin
from firebase_admin import auth, credentials
from rest_framework import authentication, exceptions

if not firebase_admin._apps:
    cred = credentials.Certificate("config/firebase_key.json")
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
        except Exception:
            raise exceptions.AuthenticationFailed('Token inválido o expirado')

        class FirebaseUser:
            def __init__(self, uid):
                self.uid = uid

            @property
            def is_authenticated(self):
                return True

        return (FirebaseUser(decoded_token['uid']), None)
