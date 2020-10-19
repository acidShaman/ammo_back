from MySQLdb._exceptions import IntegrityError
from django.core.exceptions import ValidationError
from django.http import Http404, request
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from order.serializers import OrderSerializer


class OrderCreateView(APIView):
    serializer_class = OrderSerializer

    @staticmethod
    def post(request: Request, *args, **kwargs):
        print(request.data)
        return Response({'message': 'Success'})
