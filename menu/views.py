from django.db.models import Model, Count
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from menu.models import MenuModel, DishModel
from menu.serializers import MenuSerializer, DishSerializer, CategorySerializer, MainMenuSerializer
from order.serializers import OrderItemSerializer


class ShowCategoriesView(APIView):
    serializer_class = CategorySerializer
    # permission_classes = [AllowAny]

    def get(self, request: Request):
        try:
            categories = MenuModel.objects.all()
            print(CategorySerializer(categories, many=True).data)
            if not categories:
                return Response({'message': 'There is no dishes available at the moment!'})
            return Response(CategorySerializer(categories, many=True).data)
        except AttributeError as err:
            return Response({'error': str(err)})


class ShowPositionsView(APIView):
    serializer_class = MenuSerializer

    def get(self, request: Request, category):
        try:
            category = MenuModel.objects.filter(category=category).first()
            if not category:
                return Response({'message': 'There is on dishes available in this category('})
            return Response(MenuSerializer(category).data)
        except AttributeError as err:
            return Response({'error': str(err)})


class ShowPopularDishesView(APIView):
    serializer_class = MenuSerializer

    def get(self, request: Request):
        try:
            categories = MenuModel.objects.all()
            return Response(MainMenuSerializer(categories, many=True).data)
        except AttributeError as err:
            return Response({'error': str(err)})
