from rest_framework import serializers
from .models import *

class ProfessorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professors
        fields = ['id', 'name', 'code']

class ModulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modules
        fields = ['id', 'code', 'name', 'taughtYear', 'semester', 'taughtBy']
        depth = 1

class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ['id', 'module', 'Professor', 'rating']
        depth = 1



