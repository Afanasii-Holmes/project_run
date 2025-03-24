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
    latitude = models.DecimalField(decimal_places=4, max_digits=7)
    longitude = models.DecimalField(decimal_places=4, max_digits=8)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.run} - {self.latitude} - {self.longitude}'
