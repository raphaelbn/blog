from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from user.models import User
from user.serializers import (ListUserSerializer, LoginSerializer,
                              UserSerializer)
from user.utils import generate_access_token


class UserViewSet(viewsets.ViewSet):
    permission_classes_by_action = {'post': [AllowAny],
                                    'list': [IsAuthenticated],
                                    'get': [IsAuthenticated],
                                    'delete': [IsAuthenticated]}

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)

        user_serializer.save()

        user = User.objects.filter(email=user_serializer.data['email'])
        token = generate_access_token(user[0])
        return Response({'token': token}, status.HTTP_201_CREATED)

    def list(self, request):
        user = User.objects.all()
        list_user_serializer = ListUserSerializer(user, many=True)
        return Response(list_user_serializer.data, status.HTTP_200_OK)

    def get(self, request, pk):
        user = User.objects.filter(id=pk)
        if not user.exists():
            return Response({'message': 'Usuário não existe'}, status.HTTP_404_NOT_FOUND)

        user_serializer = ListUserSerializer(user[0])
        return Response(user_serializer.data, status.HTTP_200_OK)

    def delete(self, request):
        user = User.objects.get(email=request.user.user.email)
        user.delete()

        return Response({}, status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class LoginViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def login(self, request):
        login_serializer = LoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        user = User.objects.filter(email=login_serializer.validated_data['email'], password=login_serializer.validated_data['password'])

        if not user.exists():
            return Response({'message': 'Campos inválidos'}, status.HTTP_400_BAD_REQUEST)

        token = generate_access_token(user[0])
        return Response({'token': token}, status.HTTP_200_OK)
