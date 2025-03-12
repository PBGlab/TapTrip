from django.shortcuts import render, redirect
from .booking import scrape_booking
from attractions.models import City

# Create your views here.

def booking(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        adults = request.POST.get('adults')
        children = request.POST.get('children')

        # **馬上跳轉到 showhotel.html，不等待爬蟲完成**
        return redirect(f'/showhotel/?city={city}&checkin={checkin}&checkout={checkout}&adults={adults}&children={children}')
    
    return render(request, 'booking.html', {"cities": City.objects.all()})


from django.http import StreamingHttpResponse
import json


def stream_hotels(request):
    city = request.GET.get('city')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    adults = request.GET.get('adults')
    children = request.GET.get('children')

    def event_stream():
        for hotel in scrape_booking(city, checkin, checkout, adults, children):
            json_data = json.dumps(hotel)
            yield f"data: {json_data}\n\n"

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

def showhotel(request):
    return render(request, 'showhotel.html')


#住宿管理頁面
def lodging(request):
    return render(request,'lodging.html')