from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.Serializer):
    username = serializers.RegexField(regex=r"^[\w.@+\-]{1,150}$", required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_username(self, data):
        if User.objects.filter(username=data).exists():
            raise serializers.ValidationError("Username Already Exists.")
        return data

    def validate_password(self, data):
        user_instance = User(username=self.initial_data["username"])

        try:
            validate_password(data, user=user_instance)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.RegexField(regex=r"^[\w.@+\-]{1,150}$", required=True)
    password = serializers.CharField(required=True)
