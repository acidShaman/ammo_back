from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from profile.models import ProfileModel
from django.contrib.auth.models import User


class ProfileView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProfileModel.objects.all()


class CreateProfileView(APIView):
    serializer_class = ProfileSerializer

    @classmethod
    def post(cls, request: Request, *args, **kwargs):
        print(request.data.keys())
        if request.data.keys() not in ['username', 'first_name', 'last_name', 'phone', 'birthday', 'password']:
            return Response({'message': 'Not enough fields to create new user!'})
        user = User(username=request.data['username'], first_name=request.data['first_name'], last_name=request.data['last_name'])
        profile = ProfileModel(user=user, phone=request.data['phone'], birthday=request.data['birthday'])
        profile.user.set_password(request.data['password'])
        user.save()
        profile.save()
        return Response({'message': 'Done'})
