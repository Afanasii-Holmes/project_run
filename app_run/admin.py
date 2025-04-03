from django.contrib import admin
from app_run.models import Run, Challenge, AthleteInfo, Position, CollectibleItem, Subscription

admin.site.register(Run)
admin.site.register(Challenge)
admin.site.register(AthleteInfo)
admin.site.register(Position)
admin.site.register(CollectibleItem)
admin.site.register(Subscription)