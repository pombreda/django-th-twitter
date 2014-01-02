from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django_th.models.services import Services


class Twitter(Services):

    tag = models.CharField(max_length=80, blank=True)
    screen = models.CharField(max_length=80, blank=True)
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'

    def clean(self):
        # check if one of the field is filled
        if self.tag == '' and self.screen == '':
            raise ValidationError(
                _("You have to fill ONE of the both fields (or all together)"))
