# Create your views here.
from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from menu.models import MenuModel, DishModel
from menu.serializers import MenuSerializer, DishSerializer, CategorySerializer, MainMenuSerializer


class ShowCategoriesView(APIView):
    serializer_class = CategorySerializer

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


class CreateNewCategoryView(APIView):
    serializer_class = CategorySerializer

    @classmethod
    def post(cls, request: Request):
        try:
            print(request.data)
            serializer = CategorySerializer(data=request.data)
            isShown = True if request.data['isShown'] and request.data['isShown'] == 'true' else False
            # if request.data['image'] == 'undefined':
            #     request.data['image'] = None
            if not serializer.is_valid():
                return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                category = MenuModel(category=request.data['category'], name=request.data['name'], isShown=isShown, image=request.data.get('image', None))
                category.save()
                return Response(CategorySerializer(category).data, status=200)
        except RuntimeError as err:
            return Response({'error': str(err)})
        except AssertionError as err:
            return Response({'error': str(err)})
        except ValidationError as err:
            return Response({'error': str(err)})
        except IntegrityError as error:
            return Response({'error': str(error)})
        except AttributeError as error:
            return Response({'error': str(error)})
        except KeyError as err:
            return Response({'error': str(err)})
