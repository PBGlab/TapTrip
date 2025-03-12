from django.shortcuts import render
from attractions.models import City, Attraction
from django.http import JsonResponse
from weather.views import get_weather_data  # ✅ 從 weather 匯入函數

def findattractions(request):
    cities = City.objects.all()  # 取得所有城市
    attractions = []  # 預設為空

    if request.method == "POST":
        city_name = request.POST.get("city")  # 取得選擇的城市名稱
        city = City.objects.filter(name=city_name).first()  # 查找對應的城市
        
        if city:
            attractions = Attraction.objects.filter(city=city)
        
        # ✅ 調用 `weather` App 提供的 `get_weather_data()`
        weather_info = get_weather_data(city_name)

        # **回傳 JSON 給前端,包含 景點 + 天氣**
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
            "weather": weather_info  # ✅ 這裡的天氣數據來自 `weather/views.py`
        })

    return render(request, "attraction3.html", {"cities": cities})  # 初始載入頁面
