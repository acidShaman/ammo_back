from MySQLdb._exceptions import IntegrityError
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.validators import EmailValidator, validate_email, RegexValidator
from django.dispatch import receiver
from django.http import Http404, request
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from Ammo_BackEnd import settings
from menu.models import DishModel
from .serializers import ProfileSerializer, AddressSerializer, UserUpdateSerializer, UserCreateSerializer, \
    AddressUpdateSerializer
from profile.models import ProfileModel, AddressModel
from django.contrib.auth.models import User


class ChangePasswordView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        print(request.data)
        try:
            current_user = User.objects.get(username=request.user.username)
            if current_user and current_user.check_password(request.data['old_pwd']):
                current_user.set_password(request.data['new_pwd'])
                current_user.save()
                return Response({'message': 'OK'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': current_user.check_password(request.data['old_pwd'])}, status=status.HTTP_403_FORBIDDEN)
        except TypeError as err:
            return Response({'error': str(err)})
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


class CreateUpdateAddressView(APIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    @classmethod
    def post(cls, request: Request, user_id):
        try:
            candidate = AddressModel.objects.filter(profile__user_id=user_id).first()
            if not candidate:
                serializer = AddressSerializer(request.user, request.data)
                if not serializer.is_valid():
                    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                AddressModel(
                    street=request.data.get('street', ''),
                    number=request.data.get('number', ''),
                    entrance=request.data.get('entrance', ''),
                    housing=request.data.get('housing', ''),
                    door=request.data.get('door', ''),
                    floor=request.data.get('floor', ''),
                    profile=ProfileModel.objects.filter(user_id=user_id).first()
                ).save()
                return Response({'message': f'Address was added to user {user_id}'}, status=status.HTTP_201_CREATED)
            address = AddressModel.objects.filter(profile__user_id=user_id).first()
            serializer = AddressUpdateSerializer(address, request.data)
            if not serializer.is_valid():
                print('Error')
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            serializer.update(address, validated_data=serializer.validated_data)
            return Response({'message': 'OK', 'user': ProfileSerializer(ProfileModel.objects.filter(user_id=request.user.id).first()).data}, status=status.HTTP_200_OK)
        except TypeError as err:
            return Response({'error': str(err)})
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


class ShowProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    @classmethod
    def get(cls, request: Request):
        try:
            profile = ProfileModel.objects.get(user_id=request.user.id)
            print(request.user.is_staff)
            print(profile.user.is_staff)
            if not profile:
                return Response({'error': 'User doesn\'t exist!'})
            return Response(ProfileSerializer(profile).data)
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


class UpdateProfileView(APIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    @classmethod
    def patch(cls, request: Request, id):
        try:
            if request.data.get('phone'):
                phone_candidate = ProfileModel.objects.filter(phone=request.data.get('phone')).first()
                if phone_candidate:
                    return Response({'message': 'Phone exists'}, status=status.HTTP_409_CONFLICT)

            if request.data.get('username'):
                email_candidate = User.objects.filter(username=request.data.get('username')).first()
                if email_candidate:
                    return Response({'message': 'Email exists'}, status=status.HTTP_409_CONFLICT)

            serializer = UserUpdateSerializer(request.user, request.data)
            if not serializer.is_valid():
                return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            # print(serializer.update(request.user, request.data))
            profile = ProfileModel.objects.filter(user_id=id).first()
            ProfileModel.objects.filter(user_id=id).update(
                phone=request.data.get('phone', profile.phone), sex=request.data.get('sex', profile.sex), birthday=request.data.get('birthday', profile.birthday)
            )
            User.objects.filter(pk=id).update(
                username=request.data.get('username', profile.user.username), email=request.data.get('username', profile.user.username),
                first_name=request.data.get('first_name', profile.user.first_name),
                last_name=request.data.get('last_name', profile.user.last_name)
            )
            updated_user = ProfileModel.objects.filter(user_id=id).first()
            return Response({'user': ProfileSerializer(updated_user).data},
                            status=status.HTTP_200_OK)
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


class CreateProfileView(APIView):
    serializer_class = ProfileSerializer

    @classmethod
    def post(cls, request: Request, *args, **kwargs):
        try:
            print(request.data)
            serializer = UserCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            candidate = User.objects.filter(username=request.data['username']).first()
            if ProfileModel.objects.filter(phone=request.data['phone']).first():
                return Response({'message': 'Phone exists'}, status=status.HTTP_409_CONFLICT)
            if candidate:
                return Response({'message': 'Email exists'},
                                status=status.HTTP_409_CONFLICT)
            user = User(username=request.data['username'], email=request.data['username'],
                        first_name=request.data['first_name'],
                        last_name=request.data['last_name'])
            profile = ProfileModel(user=user, phone=request.data['phone'], birthday=request.data.get('birthday'),
                                   sex=request.data.get('sex'))
            profile.user.set_password(request.data['password'])
            user.save()
            profile.save()
            return Response({'message': 'Done'}, status=status.HTTP_201_CREATED)
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


class AppendDeleteFavoritesView(APIView):
    serializer_class = ProfileSerializer

    def delete(self, request: Request, user_id, dish_id, *args, **kwargs):
        try:
            dishes = DishModel.objects.filter(favorited_by__user=user_id).all()
            candidate = ProfileModel.objects.filter(user_id=user_id).first()
            for dish in dishes:
                if dish.id == dish_id:
                    candidate.fav_dishes.remove(dish)
                    return Response({'message': 'OK'}, status=status.HTTP_200_OK)
            candidate = ProfileModel.objects.filter(user_id=user_id).first()
            if not candidate:
                return Response({'message': 'User doesn\'t exist!'},status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Unknown error'}, status=status.HTTP_400_BAD_REQUEST)
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


    def get(self, request: Request, user_id, dish_id, *args, **kwargs):
        try:
            dish = DishModel.objects.filter(pk=dish_id).first()
            candidate = ProfileModel.objects.filter(user_id=user_id).first()
            if not candidate:
                return Response({'message': 'User with this id doesnt exist!'}, status=status.HTTP_400_BAD_REQUEST)
            if not dish:
                return Response({'message': 'Dish with this id doesnt exist!'}, status=status.HTTP_400_BAD_REQUEST)
            candidate.fav_dishes.add(dish)
            return Response({'message': 'OK'}, status=status.HTTP_200_OK)
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




@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('../templates/user_reset_password.html', context)
    email_plaintext_message = f'Вас вітає AmmoSushi Delivery\n' \
                              f'Для відновлення паролю перейдіть по посиланню, що вказане нижче\n' \
                              f'http://localhost:4200/password_reset/{reset_password_token.key}\n'
    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="AmmoSushi Delivery"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
    # msg.attach_alternative(email_html_message, "text/html")
    msg.send()
