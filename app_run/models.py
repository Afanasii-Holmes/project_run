from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICES = [
    ('init', 'Инициализация забега'),
    ('in_progress', 'Забег в процессе'),
    ('finished', 'Забег окончен'),
]


class Run(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    comment = models.TextField()
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='init')
    distance = models.FloatField(default=0)
    run_time_seconds = models.IntegerField(default=0)
    speed = models.FloatField(default=0)

    def __str__(self):
        return f'{self.athlete} - {self.status}'


class AthleteInfo(models.Model):
    weight = models.IntegerField(null=True)
    goals = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.weight}'


class Challenge(models.Model):
    full_name = models.CharField(max_length=100, default='')
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.athlete} - {self.full_name}'


class Position(models.Model):
    latitude = models.DecimalField(decimal_places=6, max_digits=9)
    longitude = models.DecimalField(decimal_places=6, max_digits=10)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    date_time = models.DateTimeField(null=True)
    speed = models.FloatField(default=0)
    distance = models.FloatField(default=0)

    def __str__(self):
        return f'{self.run} - {self.latitude} - {self.longitude}'


class CollectibleItem(models.Model):
    name = models.CharField(max_length=200, default='')
    uid = models.CharField(max_length=200, default='')
    latitude = models.DecimalField(decimal_places=4, max_digits=7)
    longitude = models.DecimalField(decimal_places=4, max_digits=8)
    picture = models.URLField()
    value = models.IntegerField(null=True)
    users = models.ManyToManyField(User, blank=True, related_name='collectibleitems')

    def __str__(self):
        return f"{self.name} - {self.value}"


class Subscription(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='athletes')
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coaches')
    rating = models.IntegerField(null=True)

    class Meta:
        unique_together = ['coach', 'athlete']  # Уникальность подписки между двумя пользователями.

    def __str__(self):
        return f"{self.athlete} подписан на {self.coach}"