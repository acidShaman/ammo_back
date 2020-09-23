from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from menu.models import MenuModel, DishModel
from menu.serializers import MenuSerializer, DishSerializer


class ShowMenuView(APIView):
    serializer_class = MenuSerializer
    permission_classes = [AllowAny]

    def get(self, request: Request):
        try:
            menu = MenuModel.objects.all()
            # print(MenuSerializer(menu).data)
            if not menu:
                return Response({'message': 'There is no dishes available at the moment!'})
            return Response(MenuSerializer(menu).data)
        except AttributeError as err:
            return Response({'error': str(err)})
