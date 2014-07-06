======================================
Django Trigger Happy : Twitter Service
======================================

From Trigger Happy, this connector provides an access to your Twitter account

Requirements :
==============
* django_th 0.9.0
* python-twitter 1.1
* oauth2 1.5.211


Installation:
=============
to get the project, from your virtualenv, do :

.. code:: python

    pip install django-th-twitter
    
then

.. code:: python

    python manage.py syncdb

to startup the database

Parameters :
============
As usual you will setup the database parameters.

Important parts are the settings of the available services :

Settings.py 
-----------

INSTALLED_APPS
~~~~~~~~~~~~~~

add the module th_twitter to INSTALLED_APPS

.. code:: python

    INSTALLED_APPS = (
        'th_twitter',
    )    

TH_SERVICES 
~~~~~~~~~~~

TH_SERVICES is a list of the services we put in django_th/services directory

.. code:: python

    TH_SERVICES = (
        'th_twitter.my_twitter.ServiceTwitter',
    )

TH_TWITTER
~~~~~~~~~~~
TH_TWITTER is the settings you will need to be able to add/read data in/from Twitter.

.. code:: python

    TH_TWITTER = {
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
        'consumer_secret': 'abcdefghijklmnopqrstuvwxyz',
    }

Setting up : Administration
===========================

once the module is installed, go to the admin panel and activate the service
Twitter. 

All you can decide here is to tell if the service requires an external authentication or not.

Once they are activated. User can use them.
