from rest_framework import serializers
from . models import *

class FrontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Front
        fields = '__all__'
