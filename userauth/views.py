from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from userauth import serializers as userauth_serializers
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, logout, login
from rest_framework.authtoken.models import Token
from rest_framework import status

# Create your views here.


class RegisterAPIView(APIView):
    @staticmethod
    def post(request):
        serializer_instance = userauth_serializers.RegisterSerializer(data=request.data)

        if not serializer_instance.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer_instance.errors
            )

        serialized_data = serializer_instance.validated_data

        user_instance = User.objects.create_user(
            username=serialized_data.get("username"),
            password=serialized_data.get("password"),
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data={"message": f"User successfully created for {user_instance.username}"},
        )


class LoginAPIView(APIView):
    @staticmethod
    def post(request):
        serializer_instance = userauth_serializers.LoginSerializer(data=request.data)

        if not serializer_instance.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer_instance.errors
            )

        serialized_data = serializer_instance.validated_data
        try:
            User.objects.get(username=serialized_data.get("username"))
            user_instance = authenticate(
                username=serialized_data.get("username"),
                password=serialized_data.get("password"),
            )
            if not user_instance is None:
                login(request, user_instance)
                token, created = Token.objects.get_or_create(user=user_instance)
                return Response(status=status.HTTP_200_OK, data={"token": token.key})
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Invalid Credentials."},
            )
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND, data={"message": "User Doesn't Exist"}
            )


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            user_token = Token.objects.get(user=request.user)
            user_token.delete()
            logout(request)
            return Response(
                status=status.HTTP_200_OK,
                data={"message": f"{request.user.username} successfully logged out."},
            )
        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={"errors": str(e)}
            )
