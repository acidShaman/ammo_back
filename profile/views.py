from MySQLdb._exceptions import IntegrityError
from django.core.exceptions import ValidationError
from django.http import Http404, request
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileSerializer, UserSerializer
from profile.models import ProfileModel
from django.contrib.auth.models import User


class ShowProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    @classmethod
    def get(cls, request: Request):
        profile = ProfileModel.objects.get(user_id=request.user.id)
        if not profile:
            return Response({'error': 'User doesn\'t exist!'})
        # print(profile)
        return Response(ProfileSerializer(profile).data)


class UpdateProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    @classmethod
    def patch(cls, request: Request, id):
        try:
            candidate = ProfileModel.objects.get(user_id=id)
            if not candidate:
                return Response({'message': 'User with this id doesn\'t exist'})
            ProfileModel.objects.filter(user_id=id).update(
                phone=request.data.get('phone'), sex=request.data.get('sex'), birthday=request.data.get('birthday')
            )
            User.objects.filter(pk=id).update(
                username=request.data.get('username'), first_name=request.data.get('first_name'), last_name=request.data.get('last_name')
            )
            return Response({'message': f'{request.data["username"]} was updated successfully!'})
        except RuntimeError as err:
            return Response({'error': err})
        except AssertionError as err:
            return Response({'error': err})
        except ValidationError as err:
            return Response({'error': err})


class CreateProfileView(APIView):
    serializer_class = ProfileSerializer

    @classmethod
    def post(cls, request: Request, *args, **kwargs):
        try:
            print(request)
            candidate = User.objects.filter(username=request.data['username'])
            if candidate:
                return Response({'message': 'User with this email already exists, please try another!'})
            user = User(username=request.data['username'], first_name=request.data['first_name'],
                        last_name=request.data['last_name'])
            profile = ProfileModel(user=user, phone=request.data['phone'], birthday=request.data['birthday'],
                                   sex=request.data['sex'])
            profile.user.set_password(request.data['password'])
            user.save()
            profile.save()
            return Response({'message': 'Done', 'user': request.user, 'token': request.token})
        except IntegrityError as error:
            return Response({'error': error})
        except ValidationError as error:
            return Response({'error': error})
        except AttributeError as error:
            return Response({'error': error})
