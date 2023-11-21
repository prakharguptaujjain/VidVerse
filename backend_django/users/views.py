from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import User,Cookie,Liked_Diliked_Video,SubscribedChannel
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie,csrf_exempt
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from uuid import uuid4
from datetime import datetime, timedelta
import json

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_exempt
def signup(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not email or not password or not confirm_password:
        return JsonResponse({'status': 400, 'message': 'All fields are required'})

    if password != confirm_password:
        return JsonResponse({'status': 400, 'message': 'Passwords do not match'})
    
    # check email in db
    user = User.objects.filter(email=email)
    if user:
        return JsonResponse({'status': 400, 'message': 'Email already exists'})
    
    # create user with hashed password
    hashed_password = make_password(password)
    channed_id = str(uuid4())
    advertiser_id = str(uuid4())
    user = User(email=email, password=hashed_password, channel_id=channed_id, advertiser_id=advertiser_id)
    user.save()

    # success & redirect to home page
    return JsonResponse({'status': 201, 'message': 'Signup successful'})

@ensure_csrf_cookie
@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email', None)
            password = data.get('password', None)
            if not email or not password:
                return JsonResponse({'status': 400, 'message': 'Email and password are required.'})

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({'status': 400, 'message': 'Email does not exist or Incorrect password'})

            # Use check_password to validate the entered password
            if not check_password(password, user.password):
                return JsonResponse({'status': 400, 'message': 'Email does not exist or Incorrect password'})

            cookie = Cookie.create(user)

            return JsonResponse({'status': 200, 'message': 'Login successful', 'cookie': cookie})

        except json.JSONDecodeError as e:
            return JsonResponse({'status': 400, 'message': 'Invalid JSON data.'})
    else:
        return JsonResponse({'status': 405, 'message': 'Invalid request method.'})

@csrf_exempt
def user_video_interaction(request):
    data=json.loads(request.body.decode('utf-8'))
    cookie=data.get('cookie')
    
    # check cookie
    cookie = Cookie.objects.filter(cookie=cookie)
    email_id=Cookie.cookie_check(cookie)
    if not email_id:
            return JsonResponse({'status': 303, 'message': 'Cookie does not exist'})
    
    video_id=data.get('video_id',None)
    like_video=data.get('like_video',False)
    unlike_video=data.get('unlike_video',False)
    dislike_video=data.get('dislike_video',False)
    undislike_video=data.get('undislike_video',False)
    comment_video=data.get('comment_video',None)

    if like_video:
        Liked_Diliked_Video.objects.create(email_id, video_id=video_id, liked=True)

    if unlike_video:
        Liked_Diliked_Video.objects.filter(email_id, video_id=video_id).delete()

    if dislike_video:
        Liked_Diliked_Video.objects.create(email_id, video_id=video_id, disliked=True)

    if undislike_video:
        Liked_Diliked_Video.objects.filter(email_id, video_id=video_id).delete()

    if not video_id:
        return JsonResponse({'status': 400, 'message': 'Video id is required'})
    
    return_data = {}
    liked_disliked= Liked_Diliked_Video.objects.filter(email_id, video_id=video_id)
    if liked_disliked:
        return_data['liked'] = liked_disliked.liked
        return_data['disliked'] = liked_disliked.disliked
        return_data['subscribed'] = SubscribedChannel.objects.filter(email_id, channel_id=liked_disliked.channel_id).exists()

    return JsonResponse({'status': 200, 'message': 'Success', 'data': return_data})
    
@csrf_exempt
def user_channel_interaction(request):
    data=json.loads(request.body.decode('utf-8'))
    cookie=data.get('cookie')
    
    # check cookie
    email_id=Cookie.cookie_check(cookie)
    if not email_id:
        return JsonResponse({'status': 303, 'message': 'Cookie does not exist'})
    
    channel_id=data.get('channel_id',None)
    subscribe_channel=data.get('subscribe_channel',False)
    unsubscribe_channel=data.get('unsubscribe_channel',False)

    if subscribe_channel:
        SubscribedChannel.objects.create(email_id, channel_id=channel_id)

    if unsubscribe_channel:
        SubscribedChannel.objects.filter(email_id, channel_id=channel_id).delete()


    if not channel_id:
        return JsonResponse({'status': 400, 'message': 'Channel id is required'})

def creator_dashboard(request):
    data=json.loads(request.body.decode('utf-8'))
    cookie=data.get('cookie')
    
    email_id=Cookie.cookie_check(cookie)
    if not email_id:
        return JsonResponse({'status': 303, 'message': 'Cookie does not exist'})
    
    channel_id=User.objects.filter(cookie=cookie).channel_id

def advertiser_dashboard(request):
    data=json.loads(request.body.decode('utf-8'))
    cookie=data.get('cookie')
    
    email_id=Cookie.cookie_check(cookie)
    if not email_id:
        return JsonResponse({'status': 303, 'message': 'Cookie does not exist'})
    
    advertiser_id=User.objects.filter(cookie=cookie).advertiser_id

def video_info(request):
    data=json.loads(request.body.decode('utf-8'))
    video_id=data.get('video_id',None)
    if not video_id:
        return JsonResponse({'status': 400, 'message': 'Video id is required'})

class Contents:
    @staticmethod
    def new(request):
        data=json.loads(request.body.decode('utf-8'))
        tag=data.get('tag',None)
        searchTerm=data.get('searchTerm',None)
        num=data.get('num',20)

    def trending(request):
        data=json.loads(request.body.decode('utf-8'))
        tag=data.get('tag',None)
        searchTerm=data.get('searchTerm',None)
        num=data.get('num',20)

    def search(request):
        data=json.loads(request.body.decode('utf-8'))
        searchTerm=data.get('searchTerm',None)
        num=data.get('num',20)

    def liked_videos(request):
        data=json.loads(request.body.decode('utf-8'))
        cookie=data.get('cookie',None)
        num=data.get('num',20)

        email_id=Cookie.cookie_check(cookie)
        if not email_id:
            return JsonResponse({'status': 303, 'message': 'Cookie does not exist'})
        

        liked_videos_data = Liked_Diliked_Video.objects.filter(email_id, liked=True)[:num]

        return_data = []
        for i,liked_video in enumerate(liked_videos_data):
            video_title=video_info(liked_video.video_id).get('title')
            return_data.append({
                'vid':i+1,
                'video_id': liked_video.video_id,
                'title': video_title,
            })

        return JsonResponse({'status': 200, 'message': 'Success', 'data': return_data})

    def subscribed(request):
        data=json.loads(request.body.decode('utf-8'))
        cookie=data.get('cookie',None)
        num=data.get('num',20)

        email_id=Cookie.cookie_check(cookie)
        if not email_id:
            return JsonResponse({'status': 303, 'message': 'Cookie does not exist'})
        
        subscribed_channels_data = SubscribedChannel.objects.filter(email_id)[:num]

        return_data = []
        for i,subscribed_channel in enumerate(subscribed_channels_data):
            return_data.append({
                'channel':i+1,
                'channel_id': subscribed_channel.channel_id,
            })
        
        return JsonResponse({'status': 200, 'message': 'Success', 'data': return_data})
