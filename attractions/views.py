from django.shortcuts import render
from attractions.models import City, Attraction
from django.http import JsonResponse
from trips.models import Trip




#登出狀態頁面
def showattractions(request):
    cities = City.objects.all()  # 取得所有城市
    attractions = []  # 預設為空

    if request.method == "POST":
        city_name = request.POST.get("city")  # 取得選擇的城市名稱
        city = City.objects.filter(name=city_name).first()  # 查找對應的城市
        
        if city:
            attractions = Attraction.objects.filter(city=city)

        return JsonResponse({
            "city": city_name,
            "attractions": [
                {
                    "name": attraction.name,
                    "image_url": attraction.image_url,
                    "link": attraction.link,
                    "hashtag": attraction.hashtag
                }
                for attraction in attractions
            ],
        })

    return render(request, "attraction2.html", {"cities": cities}) 





from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def findattractions(request):
    cities = City.objects.all()

    # 🔍 AJAX 查詢景點
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        city_name = request.POST.get("city")
        city = City.objects.filter(name=city_name).first()

        if city:
            attractions = Attraction.objects.filter(city=city)
        else:
            attractions = []

        return JsonResponse({
            "city": city_name,
            "attractions": [
                {
                    "id": attraction.id,
                    "name": attraction.name,
                    "image_url": attraction.image_url,
                    "link": attraction.link,
                    "hashtag": attraction.hashtag
                }
                for attraction in attractions
            ]
        })

    # 🔁 一般 GET 載入頁面，同時給右側搜尋表單使用的行程/天數資料
    trips = Trip.objects.filter(user=request.user, status="draft").prefetch_related("days")

    trip_data = []
    for trip in trips:
        days = []
        for i, day in enumerate(trip.days.all().order_by("date")):
            days.append({
                "id": day.id,
                "day_number": i + 1,
                "date": str(day.date)
            })

        trip_data.append({
            "id": trip.id,
            "name": trip.name,
            "days": days
        })

    return render(request, "attraction1.html", {
        "cities": cities,
        "trips": trip_data,
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
    })
