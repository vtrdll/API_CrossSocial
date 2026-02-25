
from rest_framework import serializers
from .models  import Team

class CreateTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ['name','description', 'box','category', 'membros' ]
        read_only_fields = ["creator"]


class ListTeamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Team
        fields = '__all__'