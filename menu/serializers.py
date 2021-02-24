from menu.models import MenuModel, DishModel
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuModel
        fields = ['id', 'category', 'name', 'isShown', 'image']


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuModel
        fields = ['category', 'name', 'isShown', 'image']

    def create(self, validated_data):
        category = MenuModel(
            category=validated_data['value'],
            name=validated_data['name'],
            isShown=validated_data['isShow'],
            image=validated_data['image']
        )
        category.save()


class EditCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuModel
        fields = ['id', 'category', 'name', 'isShown', 'image']
        extra_kwargs = {
            'category': {
                'required': False
            },
            'name': {
                'required': False
            },
            'isShown': {
                'required': False
            },
            'image': {
                'required': False
            }
        }


class DishSerializer(serializers.ModelSerializer):

    class Meta:
        model = DishModel
        fields = ['id', 'name', 'price', 'about_dish', 'ingredients', 'image']


class NestedPositionsSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = MenuModel
        fields = ['id', 'category', 'name', 'isShown', 'dishes']

    def to_representation(self, instance):
        if len(instance.dishes.all()) >= 1:
            return {
                "id": instance.id,
                "name": instance.name,
                "category": instance.category,
                'isShown': instance.isShown,
                "dishes": DishSerializer(instance.dishes.all(), many=True).data
            }


class MenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = MenuModel
        fields = ['id', 'category', 'name', 'isShown', 'dishes']


class MainMenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = MenuModel
        fields = ['id', 'category', 'name', 'isShown', 'dishes']

    def to_representation(self, instance):
        filter_dishes = instance.dishes.all()[:8]
        return {
            "id": instance.id,
            "name": instance.name,
            "category": instance.category,
            'isShown': instance.isShown,
            "dishes": DishSerializer(filter_dishes, many=True).data
        }




