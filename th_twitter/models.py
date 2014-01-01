from django.db import models
from django_th.models.services import Services


class Twitter(Services):

    text = models.TextField()
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
