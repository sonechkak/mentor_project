from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.landing.models import *
from apps.landing.validators.img_param import content_image_validators, main_image_validators


class ImageFieldMixin:
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.image:
            rep['image'] = instance.image.url
        return rep

    def validate_image(self, value):
        if not value:
            raise ValidationError("Пожалуйста, загрузите изображение.")
        return value


class MainInfSerializer(ImageFieldMixin, serializers.ModelSerializer):
    image = serializers.ImageField(validators=main_image_validators)

    class Meta:
        model = MainInf
        fields = '__all__'


class AboutMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutMe
        fields = '__all__'


class ContentSerializer(ImageFieldMixin, serializers.ModelSerializer):
    image = serializers.ImageField(validators=content_image_validators)

    class Meta:
        model = Content
        fields = '__all__'

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['text']

class ProductSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, required=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'text', 'points']

    def validate_points(self, value):
        if len(value) > 7:
            raise ValidationError("Нельзя добавить больше 7 пунктов.")
        elif len(value) == 0:
            raise ValidationError("Нужно добавить хотя бы один пункт.")
        return value

    def create(self, validated_data):
        points_data = validated_data.pop('points')
        product = Product.objects.create(**validated_data)

        for point_data in points_data:
            Point.objects.create(product=product, **point_data)

        return product

    def update(self, instance, validated_data):
        points_data = validated_data.pop('points')

        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        instance.text = validated_data.get('text', instance.text)
        instance.save()

        instance.points.all().delete()
        for point_data in points_data:
            Point.objects.create(product=instance, **point_data)

        return instance