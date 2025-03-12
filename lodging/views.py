from django.shortcuts import render
from .booking import scrape_booking
from attractions.models import City
# Create your views here.

#目前測試要加上這兩行才能爬取Booking 
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def booking(request):
    hotels = []
    TAIWAN_CITIES = City.objects.all()
    if request.method == 'POST':
        city = request.POST.get('city')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        adults = request.POST.get('adults')
        children = request.POST.get('children')
        hotels = scrape_booking(city, checkin, checkout, adults, children)
        return render(request,'showhotel.html',{"hotels": hotels})
    return render(request,'booking.html',{"cities": TAIWAN_CITIES,"hotels": hotels})

#住宿管理頁面
def lodging(request):
    return render(request,'lodging.html')