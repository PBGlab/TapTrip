from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from attractions.models import City,Attraction
import random
from django.middleware.csrf import get_token
# Create your views here.


# 初始畫面
def home2(request):
    TAIWAN_CITIES = City.objects.all()
    
    # 景點預覽用
    random_ids = random.sample(range(1, 753), 6) 
    attractions = Attraction.objects.filter(id__in=random_ids)
    
    errors = request.session.pop('errors', {})
    csrf_token = get_token(request)
    if request.user.is_authenticated:
        return render(request, 'home.html', {
        "cities": TAIWAN_CITIES,
        "attractions": attractions,
        "username": request.user.username  
    })
    return render(request, 'LoginPage.html', {
        "cities": TAIWAN_CITIES,
        "attractions": attractions,
        "errors": errors
    })


# 登入後畫面
def home(request):
    TAIWAN_CITIES = City.objects.all()

    # 景點預覽用
    random_ids = random.sample(range(1, 753), 6) 
    attractions = Attraction.objects.filter(id__in=random_ids)

    return render(request, 'home.html', {
        "cities": TAIWAN_CITIES,
        "attractions": attractions,
        "username": request.user.username  
    })