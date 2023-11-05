from django.db import models
from uuid import uuid4
from datetime import datetime, timedelta

# Create your models here.
# ytb user model

class User(models.Model):
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    channel_id = models.CharField(max_length=20)

class Cookie(models.Model):
    email = models.CharField(max_length=20)
    cookie = models.CharField(max_length=20)
    expiry = models.CharField(max_length=20)

    @staticmethod
    def create(email):
        cookie = Cookie(email=email, cookie=str(uuid4()), expiry=str(datetime.now() + timedelta(days=30)))
        cookie.save()
        return cookie.cookie
    
    @staticmethod
    def cookie_check(cookie):
        cookie = Cookie.objects.filter(cookie=cookie)
        if not cookie:
            return False
        if cookie.expiry < str(datetime.now()):
            return False
        return True