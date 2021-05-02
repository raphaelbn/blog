import jwt
from rest_framework import authentication, status
from rest_framework.exceptions import AuthenticationFailed

from blog.settings import SECRET_JWT
from user.models import User


class SystemAuthUser:
    user = None

    def __init__(self, user):
        self.user = user

    @property
    def is_authenticated(self):
        return True


class JWTCustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        access_token = request.META.get('HTTP_AUTHORIZATION', '')
        if not access_token:
            return None

        try:
            payload = jwt.decode(
                access_token, SECRET_JWT, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expirado ou inválido')
        except jwt.InvalidSignatureError:
            raise AuthenticationFailed('Token expirado ou inválido')

        user = User.objects.filter(id=payload['user_id']).first()

        if user is None:
            raise AuthenticationFailed('Token não encontrado')

        return SystemAuthUser(user=user), access_token

    def authenticate_header(self, request):
        return status.HTTP_401_UNAUTHORIZED
