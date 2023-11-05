from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import User,Cookie

def signup(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')

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

def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    # check email in db
    user = User.objects.filter(email=email)
    if not user:
        return JsonResponse({'status': 400, 'message': 'Email does not exist or Incorrect password'})
    
    # check password
    if user.password != password:
        return JsonResponse({'status': 400, 'message': 'Email does not exist or Incorrect password'})
    
    # create cookie
    cookie = Cookie.create(email)
    
    # success & redirect to home page
    return JsonResponse({'status': 200, 'message': 'Login successful', 'cookie': cookie})



        