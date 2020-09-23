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
            categories = MenuModel.objects.order_by('id').all()
            print(MenuSerializer(categories, many=True).data)
            if not categories:
                return Response({'message': 'There is no dishes available at the moment!'})
            return Response(MenuSerializer(categories, many=True).data)
        except AttributeError as err:
            return Response({'error': str(err)})
