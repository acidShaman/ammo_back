from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt import serializers
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.utils.translation import gettext as _


# Create your views here.
class CustomInvalidToken(InvalidToken):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('Token is invalid or expired')


class CustomRefreshTokenView(TokenRefreshView):
    serializer_class = serializers.TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise CustomInvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
