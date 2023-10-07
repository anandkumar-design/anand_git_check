
from rest_framework import serializers
from .models import Students,Marks

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'
