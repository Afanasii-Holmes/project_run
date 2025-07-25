from geopy.distance import geodesic
from rest_framework import serializers
from .models import Run, Challenge, Position, CollectibleItem, Subscription
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


class CollectibleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectibleItem
        fields = ['name', 'uid', 'latitude', 'longitude', 'picture', 'value']

    def validate_latitude(self, value):
        if value > 90 or value < -90:
            raise serializers.ValidationError('latitude должен быть в диапазоне от -90.0 до +90.0 градусов')
        return value

    def validate_longitude(self, value):
        if value > 180 or value < -180:
            raise serializers.ValidationError('longitude должен быть в диапазоне от -180.0 до +180.0 градусов')
        return value


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.IntegerField()
    rating = serializers.FloatField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'date_joined', 'type', 'runs_finished', 'rating']

    def get_type(self, obj):
        if obj.is_staff:
            return 'coach'
        else:
            return 'athlete'


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    date_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%f")
    class Meta:
        model = Position
        fields = '__all__'

    def validate(self, data):
        run = data.get('run')
        if run.status != 'in_progress':
            raise serializers.ValidationError('Забег должен быть начат и еще не закончен')

        current_latitude = data.get('latitude')
        current_longitude = data.get('longitude')

        collectible_items = CollectibleItem.objects.all()

        for item in collectible_items:
            distance = geodesic((current_latitude,current_longitude), (item.latitude, item.longitude)).meters
            if distance <= 100:
                item.users.add(run.athlete)

        return data

    def validate_latitude(self, value):
        if value > 90 or value < -90:
            raise serializers.ValidationError('latitude должен быть в диапазоне от -90.0 до +90.0 градусов')
        return value

    def validate_longitude(self, value):
        if value > 180 or value < -180:
            raise serializers.ValidationError('longitude должен быть в диапазоне от -180.0 до +180.0 градусов')
        return value


# class UserDetailSerializer(UserSerializer):
#     items = CollectibleItemSerializer(source='collectibleitems', many=True, read_only=True)
#
#     class Meta:
#         model = User
#         fields = UserSerializer.Meta.fields + ['items']


class AthleteSerializer(UserSerializer):
    items = CollectibleItemSerializer(source='collectibleitems', many=True, read_only=True)
    coach = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['coach', 'items']

    def get_coach(self, obj):
        if Subscription.objects.filter(athlete=obj.id).exists():
            subscription = Subscription.objects.get(athlete=obj.id)
            return subscription.coach.id
        return ''


class CoachSerializer(UserSerializer):
    items = CollectibleItemSerializer(source='collectibleitems', many=True, read_only=True)
    athletes = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['athletes', 'items']

    def get_athletes(self, obj):
        #Возвращает пустой список, если ничего не найдено удовлетворяющее фильтру
        athletes_list = Subscription.objects.filter(coach=obj.id).values_list('athlete__id', flat=True)
        return athletes_list