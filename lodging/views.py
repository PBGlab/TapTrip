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


# import json
# from django.http import StreamingHttpResponse

# import json
# from django.http import StreamingHttpResponse
# from django.shortcuts import render

# def stream_hotels(request):
#     """ 使用 StreamingHttpResponse 來逐筆回傳爬取的飯店資料 """

#     def event_stream():
#         # ✅ 獲取 GET 參數，並確保它們正確被傳遞
#         city = request.GET.get("city")
#         checkin = request.GET.get("checkin")
#         checkout = request.GET.get("checkout")
#         adults = request.GET.get("adults")
#         children = request.GET.get("children")

#         print(f"📌 收到參數: city={city}, checkin={checkin}, checkout={checkout}, adults={adults}, children={children}")

#         if not city or not checkin or not checkout:
#             yield f"data: {json.dumps({'error': '缺少必要參數'})}\n\n"
#             return
        
#         # ✅ 爬取並逐筆發送
#         for hotel in scrape_booking(city, checkin, checkout, adults, children):
#             print(f"✅ 傳送飯店: {hotel['名稱']} - {hotel['價格']}")
#             yield f"data: {json.dumps(hotel)}\n\n"

#     return StreamingHttpResponse(event_stream(), content_type="text/event-stream")
