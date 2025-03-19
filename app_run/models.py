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