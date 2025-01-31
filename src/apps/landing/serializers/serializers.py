from rest_framework import serializers

from landing.models import *


class MainInfSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainInf
        fields = '__all__'

class AboutMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutMe
        fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'