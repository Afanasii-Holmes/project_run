from rest_framework import serializers
from .models import Run
from django.contrib.auth.models import User


class SmallUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class RunSerializer(serializers.ModelSerializer):
    athlete_data = SmallUserSerializer(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'date_joined', 'type']

    def get_type(self, obj):
        if obj.is_staff:
            return 'coach'
        else:
            return 'athlete'