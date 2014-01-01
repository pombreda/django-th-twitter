# -*- coding: utf-8 -*-

from django import forms
from th_twitter.models import Twitter


class TwitterForm(forms.ModelForm):

    """
        for to handle Twitter service
    """
        
    class Meta:
        model = Twitter
        fields = ('text', )


class TwitterConsummerForm(TwitterForm):
    pass


class TwitterProviderForm(TwitterForm):
    pass
