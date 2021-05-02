from rest_framework import serializers, validators

from user.models import User
from blog.utils import get_default_error_messages


class UserSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(min_length=8, error_messages=get_default_error_messages(min_length=8))
    password = serializers.CharField(min_length=6, error_messages=get_default_error_messages(min_length=6))
    email = serializers.EmailField(
        error_messages=get_default_error_messages(),
        validators=[validators.UniqueValidator(queryset=User.objects.all(), message='User already exists')])

    class Meta:
        model = User
        fields = ('displayName', 'email', 'password', 'image')


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(error_messages=get_default_error_messages())
    email = serializers.CharField(error_messages=get_default_error_messages())

    class Meta:
        model = User
        fields = ('email', 'password')
