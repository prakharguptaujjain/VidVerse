from django.db import models
from uuid import uuid4
from datetime import datetime, timedelta

# Create your models here.
# ytb user model

class User(models.Model):
    name= models.CharField(max_length=30)
    email = models.CharField(max_length=50,primary_key=True,unique=True)
    password = models.CharField(max_length=128)
    channel_id = models.CharField(max_length=40)
    advertiser_id = models.CharField(max_length=40)

    def __str__(self) -> str:
        return self.email

class Liked_Diliked_Video(models.Model):
    email_id = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
    video_id = models.CharField(max_length=40)
    liked = models.BooleanField(default=False)
    disliked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.video_id
    
class SubscribedChannel(models.Model):
    email_id = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
    channel_id = models.CharField(max_length=40)

    def __str__(self) -> str:
        return self.channel_id
    
class Cookie(models.Model):
    email_id = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
    cookie = models.CharField(max_length=40)
    expiry = models.CharField(max_length=30)

    @staticmethod
    def create(email):
        expiry=str(datetime.now() + timedelta(days=30))
        cookie = Cookie(email_id=email, cookie=str(uuid4()), expiry=expiry)
        cookie.save()
        return cookie.cookie
    
    @staticmethod
    def cookie_check(cookie):
        cookie = Cookie.objects.filter(cookie=cookie)
        if not cookie:
            return False
        if cookie.expiry < str(datetime.now()):
            return False
        return cookie.email_id