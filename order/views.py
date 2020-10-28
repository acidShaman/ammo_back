import json

from MySQLdb._exceptions import IntegrityError
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import Http404, request
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from bot.bot import send_message
from order.models import OrderModel, OrderItemModel
from order.serializers import OrderSerializer
from profile.models import ProfileModel, AddressModel
from profile.serializers import ProfileSerializer


def format_request(data, order_id):
    translation = {'first_name': 'Ім\'я', 'last_name': 'Прізвище', 'phone': 'Номер телефону',
                   'street': 'Вулиця', 'number': 'Номер вулиці', 'entrance': 'Під\'їзд', 'housing': 'Корпус',
                   'door': 'Номер квартири', 'floor': 'Поверх', 'payment_method': 'Спосіб оплати',
                   'training_ch': 'К-ть навчальних паличок', 'normal_ch': 'К-ть нормальних паличок',
                   'promo_code': 'Промо-код', 'commentary': 'Коментар до замовлення',
                   'extra_adds': 'Додатковий імбир та васабі'}
    message = f'Замовлення №{order_id}\n'
    for k, v in data.lists():
        if k in translation.keys():
            message += f'{translation[k]}: {v[0]}\n'
        if k == 'orderItems':
            message += f'Позиції: \n'
            items = json.loads(v[0])
            c = 1
            for item in items:
                if item['quantity'] != 0:
                    message += f'{c}. {item["name"]} -- Кількість:{item["quantity"]}\n'
                    c += 1
    send_message(message)


class OrderCreateView(APIView):
    serializer_class = OrderSerializer

    @staticmethod
    def post(request: Request, *args, **kwargs):
        candidate = ProfileModel.objects.filter(user__first_name=request.data['first_name'],
                                                user__last_name=request.data['last_name'],
                                                phone=request.data['phone']).first()
        if candidate:
            address = AddressModel.objects.filter(profile=candidate).first()
            if not address:
                address = AddressModel(street=request.data.get('street'), number=request.data.get('number'),
                                           entrance=request.data.get('entrance'), housing=request.data.get('housing'),
                                           door=request.data.get('door'), floor=request.data.get('floor'),
                                           profile=candidate)
                address.save()
            order = OrderModel(profile=candidate, address=address)
        else:
            order = OrderModel()

        format_request(request.data, order.id)
        total_price = 0
        for key, value in request.data.lists():
            if key == 'orderItems':
                items = json.loads(value[0])
                for item in items:
                    if item['quantity'] != 0:
                        total_price += (item['quantity'] * item['price'])
                        order_item = OrderItemModel(dish_id=item['id'], quantity=item['quantity'])
                        order_item.save()
                        order.order_items.add(order_item)
        return Response({'message': 'Success'})
