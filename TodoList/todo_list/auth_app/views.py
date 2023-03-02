from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from auth_app.middlewares.auth_backend import JWTAuthenticationBackend
from auth_app.serializers import LoginSerializer, RegistrationSerializer
from auth_app.services.auth import get_auth_service


class AuthViewSet(viewsets.GenericViewSet):
    service = get_auth_service()

    @action(detail=False, methods=["post"])
    @transaction.atomic
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)

        access_token, refresh_token = self.service.register(serializer.data)
        return self.get_token_response(access_token, refresh_token)

    @action(detail=False, methods=["post"])
    @transaction.atomic
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)

        access_token, refresh_token = self.service.login(serializer.data)
        return self.get_token_response(access_token, refresh_token, status=200)

    @action(detail=False, methods=["patch"])
    @transaction.atomic
    def refresh(self, request):
        old_refresh_token = request.COOKIES.get("refresh_token", None)
        if old_refresh_token is None:
            raise AuthenticationFailed("Токен обновления не был получен!")

        access_token, refresh_token = self.service.refresh_tokens(old_refresh_token)
        return self.get_token_response(access_token, refresh_token)

    @action(
        detail=False,
        methods=["delete"],
        permission_classes=(IsAuthenticated,),
        authentication_classes=(JWTAuthenticationBackend,),
    )
    def logout(self, request):
        refresh_token = request.COOKIES.get("refresh_token", None)
        if refresh_token is not None:
            self.service.logout(request.user, refresh_token)

        return Response(status=204)

    def get_token_response(self, access_token: str, refresh_token: str, status=201):
        response_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        response = Response(status=status, data=response_data)
        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            max_age=60 * 60 * 24 * 30,
        )

        return response
