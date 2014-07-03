# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django import forms
from th_twitter.models import Twitter


class TwitterForm(forms.ModelForm):

    """
        for to handle Twitter service
    """

    class Meta:
        model = Twitter
        fields = ('tag', 'screen')
        help_texts = {
            'tag': _('Put the tag you want to track from tweeter'),
            'screen': _('Put the name of a user you want to get his tweets'),
        }


class TwitterConsumerForm(TwitterForm):

    class Meta:
        model = Twitter
        fields = ('tag',)
        exclude = ('screen',)
        help_texts = {
            'tag': _('Put the tag you want to add'),
        }


class TwitterProviderForm(TwitterForm):
    pass
