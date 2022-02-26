from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import MyUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'role',
            'email',
            'first_name',
            'last_name',
            'bio',
        )
        model = MyUser


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=(UniqueValidator(queryset=MyUser.objects.all()),)
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=MyUser.objects.all()),)
    )

    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
        )

    def validate_username(self, data):
        if data == 'me':
            raise ValidationError(message='Некорректный username!')
        return data


class GenTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=100)

    class Meta:
        model = MyUser
        fields = (
            'username',
            'confirmation_code',
        )
