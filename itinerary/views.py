# itinerary/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .models import Itinerary ,Day
from datetime import datetime,timedelta

from django.views.decorators.csrf import csrf_exempt






def plan_itinerary(request):
    return render(request, "itinerary/plan.html")

@csrf_exempt
@login_required
def create_itinerary(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)  # 查看提交的資料

            days = data.get("days")
            start_date = data.get("start_date")

            # 檢查天數範圍
            if not (1 <= days <= 10):
                return JsonResponse({"error": "天數必須在 1 到 10 天之間"}, status=400)

            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            itinerary = Itinerary.objects.create(user=request.user, start_date=start_date)

            # 創建 Day 物件
            for i in range(days):
                day_date = start_date + timedelta(days=i)
                Day.objects.create(itinerary=itinerary, date=day_date)
            
            print(f"✅ 行程建立成功：ID {itinerary.id}") 
            return JsonResponse({"message": "行程建立成功", "itinerary_id": itinerary.id})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


def get_itinerary(request, itinerary_id=None):
    """取得特定行程或當前使用者最新行程"""
    
    if itinerary_id:
        try:
            itinerary = Itinerary.objects.get(id=itinerary_id)
        except Itinerary.DoesNotExist:
            return JsonResponse({"error": "行程不存在"}, status=404)
    else:
        itinerary = Itinerary.objects.filter(user=request.user).order_by("-created_at").first()
        if not itinerary:
            return JsonResponse({"error": "找不到行程"}, status=404)

    days = []
    for day in itinerary.days.all():
        days.append({
            "id": day.id,
            "day": (day.date - itinerary.start_date).days + 1,
            "date": day.date.strftime("%Y-%m-%d"),
            "attractions": [attraction.name for attraction in day.attractions.all()],
            "accommodations": [accommodation.name for accommodation in day.accommodations.all()]
        })

    return JsonResponse({
        "itinerary_id": itinerary.id,
        "start_date": itinerary.start_date.strftime("%Y-%m-%d"),
        "end_date": (itinerary.start_date + timedelta(days=itinerary.days.count() - 1)).strftime("%Y-%m-%d"),
        "days": days
    })


def cart_view(request):
    """顯示行程購物車頁面"""
    return render(request, "itinerary/cart.html")
