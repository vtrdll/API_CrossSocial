from rest_framework import serializers

from .models import WOD


class  WodSerializer(serializers.ModelSerializer):

    class Meta:
        model = WOD
        fields = '__all__'
