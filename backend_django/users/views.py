from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import User,Cookie
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie,csrf_exempt
from django.middleware.csrf import get_token
import json

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_exempt
def signup(request):
    data=json.loads(request.body.decode('utf-8'))
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
    
    # create user
    user = User(email=email, password=password)
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

            if user.password != password:
                return JsonResponse({'status': 400, 'message': 'Incorrect password'})

            cookie = Cookie.create(user)

            return JsonResponse({'status': 200, 'message': 'Login successful', 'cookie': cookie})

        except json.JSONDecodeError as e:
            return JsonResponse({'status': 400, 'message': 'Invalid JSON data.'})
    else:
        return JsonResponse({'status': 405, 'message': 'Invalid request method.'})

        