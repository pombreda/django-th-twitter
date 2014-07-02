# -*- coding: utf-8 -*-
# oauth and url stuff
import oauth2 as oauth
import urlparse
import urllib
# add the python API
import twitter

# django classes
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.log import getLogger


# django_th classes
from django_th.services.services import ServicesMgr
from django_th.models import UserService, ServicesActivated, TriggerService

from th_twitter.models import Twitter
"""
    handle process with twitter
    put the following in settings.py

    TH_TWITTER = {
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
        'consumer_secret': 'abcdefghijklmnopqrstuvwxyz',
    }

"""

logger = getLogger('django_th.trigger_happy')


class ServiceTwitter(ServicesMgr):

    def __init__(self):
        self.AUTH_URL = 'https://api.twitter.com/oauth/authorize'
        self.REQ_TOKEN = 'https://api.twitter.com/oauth/request_token'
        self.ACC_TOKEN = 'https://api.twitter.com/oauth/access_token'
        self.consumer_key = settings.TH_TWITTER['consumer_key']
        self.consumer_secret = settings.TH_TWITTER['consumer_secret']

    def process_data(self, token, trigger_id, date_triggered):
        """
            get the data from the service
        """
        data = []

        if token is not None:
            trigger = TriggerService.objects.get(pk=trigger_id)

            token_key, token_secret = token.split('#TH#')

            api = twitter.Api(consumer_key=self.consumer_key,
                              consumer_secret=self.consumer_secret,
                              access_token_key=token_key,
                              access_token_secret=token_secret)

            # get the data of "my" timeline
            if trigger.tag != '':
                statuses = api.GetSearch(term=trigger.tag)
            if trigger.screen != '':
                statuses = api.GetUserTimeline(trigger.screen)

            for s in statuses:
                data.append({'content': s.text})

        return data

    def save_data(self, token, trigger_id, **data):
        """
            let's save the data
        """
        tags = []
        if token and 'link' in data and data['link'] is not None and len(data['link']) > 0:
            # get the evernote data of this trigger
            trigger = Twitter.objects.get(trigger_id=trigger_id)
            token_key, token_secret = token.split('#TH#')
            api = twitter.Api(consumer_key=self.consumer_key,
                              consumer_secret=self.consumer_secret,
                              access_token_key=token_key,
                              access_token_secret=token_secret)
            # todo
            # 1 get content
            # 2 get url if any
            # 3 shortening url
            content = data['url']
            for tag in trigger.tags.split(','):
                tags.append({'#' + tag})

            if 'content' in data and data['content'] is not None and len(data['content']) > 0:
                content += ' ' + data['content'] + ' ' + tags

            status = api.PostUpdate(content)

    def get_twitter_client(self, token=None):
        """
            get the token from twitter
        """
        consumer = oauth.Consumer(self.consumer_key, self.consumer_secret)
        if token:
            client = oauth.Client(consumer, token)
        else:
            client = oauth.Client(consumer)
        return client

    def auth(self, request):
        """
            let's auth the user to the Service
        """

        callbackUrl = 'http://%s%s' % (
            request.get_host(), reverse('twitter_callback'))
        request_token = self.get_request_token(request, callbackUrl)
        print (request_token)
        # Save the request token information for later
        request.session['oauth_token'] = request_token['oauth_token']
        request.session['oauth_token_secret'] = request_token[
            'oauth_token_secret']

        # URL to redirect user to, to authorize your app
        auth_url = self.get_auth_url(request, request_token)

        return auth_url

    def callback(self, request):
        """
            Called from the Service when the user accept to activate it
        """

        try:
            # finally we save the user auth token
            # As we already stored the object ServicesActivated
            # from the UserServiceCreateView now we update the same
            # object to the database so :
            # 1) we get the previous objet
            us = UserService.objects.get(
                user=request.user,
                name=ServicesActivated.objects.get(name='ServiceTwitter'))
            # 2) Readability API require to use 4 parms consumer_key/secret + token_key/secret
            # instead of usually get just the token from an access_token
            # request. So we need to add a string seperator for later use to
            # slpit on this one
            access_token = self.get_access_token(
                request.session['oauth_token'],
                request.session['oauth_token_secret'],
                request.GET.get('oauth_verifier', '')
            )
            us.token = access_token['oauth_token'] + \
                '#TH#' + access_token['oauth_token_secret']

            # 3) and save everything
            us.save()
        except KeyError:
            return '/'

        return 'twitter/callback.html'

    # Oauth Stuff
    def get_auth_url(self, request, request_token):
        return '%s?oauth_token=%s' % (
            self.AUTH_URL,
            urllib.quote(request_token['oauth_token']))

    def get_request_token(self, request, callback_url):
        client = self._get_oauth_client()
        request_url = '%s?oauth_callback=%s' % (
            self.REQ_TOKEN, urllib.quote(callback_url))

        resp, content = client.request(request_url, 'GET')
        request_token = dict(urlparse.parse_qsl(content))
        return request_token

    def get_access_token(
        self, oauth_token, oauth_token_secret, oauth_verifier
    ):
        token = oauth.Token(oauth_token, oauth_token_secret)
        token.set_verifier(oauth_verifier)
        client = self._get_oauth_client(token)

        resp, content = client.request(self.ACC_TOKEN, 'POST')
        access_token = dict(urlparse.parse_qsl(content))
        return access_token

    def _get_oauth_client(self, token=None):
        consumer = oauth.Consumer(self.consumer_key, self.consumer_secret)
        if token:
            client = oauth.Client(consumer, token)
        else:
            client = oauth.Client(consumer)
        return client
