from django.shortcuts import render, redirect, get_object_or_404
from .models import Trip, TripDay, TripDayAttraction 
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from lodging.models import Lodging
import json

#建立行程
def create_trip(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date")

        # **檢查名稱是否輸入**
        if not name:
            return JsonResponse({"success": False, "error": "行程名稱不能為空！"})

        try:
            # **檢查日期是否有效**
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            
            # **檢查起始日期是否在結束日期之後**
            if start_date > end_date:
                return JsonResponse({"success": False, "error": "開始日期不能晚於結束日期！"})

        except ValueError:
            return JsonResponse({"success": False, "error": "請輸入有效的日期格式！"})

        # **建立 Trip**
        trip = Trip.objects.create(
            user=request.user,
            name=name,
            start_date=start_date,
            end_date=end_date
        )

        # **自動建立 TripDay**
        current_date = start_date
        while current_date <= end_date:
            TripDay.objects.create(trip=trip, date=current_date)
            current_date += timedelta(days=1)

        return JsonResponse({"success": True, "redirect_url": f"/findattractions/?selected_trip={trip.id}"})


    
    message = request.GET.get('message', '')
    return render(request, "create_trip.html", {'message': message})




#刪除行程
@csrf_exempt
def delete_trip(request, trip_id):
    if request.method == "DELETE":
        try:
            trip = Trip.objects.get(id=trip_id, user=request.user)

            # ✅ 先刪除所有關聯的住宿
            related_lodgings = Lodging.objects.filter(trip=trip)
            related_lodgings.delete()

            # ✅ 再刪除行程
            trip.delete()

            return JsonResponse({"success": True, "message": "行程與關聯的住宿已刪除"})
        except Trip.DoesNotExist:
            return JsonResponse({"success": False, "error": "找不到該行程或沒有權限"}, status=404)
    
    return JsonResponse({"success": False, "error": "只允許 DELETE 請求"}, status=405)




#顯示所有行程
def list_trips(request):
    draft_trips = Trip.objects.filter(user=request.user, status='draft')

    if not draft_trips:
        message = "目前還沒有建立任何行程"
        return render(request, "create_trip.html", {"message": message})

    trip_data = []
    for trip in draft_trips:
        trip_days = TripDay.objects.filter(trip=trip).order_by("date")
        total_days = (trip.end_date - trip.start_date).days + 1

        days_data = []
        for day in trip_days:
            attraction_count = TripDayAttraction.objects.filter(trip_day=day).count()  # ✅ 修正這裡的查詢方式
            days_data.append({
                "id": day.id,
                "date": day.date,
                "attraction_count": attraction_count
            })

        # ✅ 修正 lodging 資料
        lodgings = Lodging.objects.filter(trip=trip)  # `Lodging` 直接存 trip
        lodging_data = []
        for lodging in lodgings:
            lodging_data.append({
                "id": lodging.id,
                "name": lodging.name,
                "address": lodging.address,
                "checkin": lodging.check_in,
                "checkout": lodging.check_out,
                "price": lodging.price,
                "link": lodging.link,
                "image": lodging.image
            })

        trip_data.append({
            "trip": trip,
            "total_days": total_days,
            "days": days_data,
            "has_lodging": lodgings.exists(),
            "lodgings": lodging_data
        })

    return render(request, "mytrips.html", {"trip_data": trip_data})


from django.contrib.auth.decorators import login_required

#即時更新編輯行程區塊
@login_required
def api_trips(request):
    user = request.user
    trips = Trip.objects.filter(user=user, status="draft").prefetch_related("days__tripdayattraction_set__attraction")

    trip_data = []
    for trip in trips:
        days = []
        for i, day in enumerate(trip.days.all()):
            attractions = [
                {
                    "trip_day_attraction_id": tda.id,
                    "name": tda.attraction.name,
                    "image_url": tda.attraction.image_url,
                    "link": tda.attraction.link,
                    "hashtag": tda.attraction.hashtag
                }
                for tda in day.tripdayattraction_set.select_related("attraction")
            ]

            days.append({
                "id": day.id,
                "day_number": i + 1,
                "date": str(day.date),
                "attractions": attractions
            })

        trip_data.append({
            "id": trip.id,
            "name": trip.name,
            "days": days
        })

    return JsonResponse({"trips": trip_data})





from attractions.models import Attraction

#新增景點 
def add_to_trip(request):
    if request.method == "POST":
        data = json.loads(request.body)
        trip_day_id = data.get("trip_day_id")
        attraction_id = data.get("attraction")  # 改為 attraction id
        
        try:
            # 取得對應的行程日
            trip_day = TripDay.objects.get(id=trip_day_id)
            # 取得景點 (依照 attraction_id 查詢)
            attraction = Attraction.objects.get(id=attraction_id)
            # 利用 get_or_create 防止重複加入
            tda, created = TripDayAttraction.objects.get_or_create(
                trip_day=trip_day,
                attraction=attraction,
            )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Invalid request"})



#刪除景點 
@csrf_exempt  # 如果你有 CSRF 防護，請根據需求決定是否使用
def delete_attraction(request, attraction_id):
    """
    刪除指定的景點 (TripDayAttraction)
    """
    if request.method == "DELETE":
        try:
            attraction = TripDayAttraction.objects.get(id=attraction_id)
            attraction.delete()
            return JsonResponse({"success": True})
        except TripDayAttraction.DoesNotExist:
            return JsonResponse({"success": False, "error": "景點不存在"}, status=404)
    return JsonResponse({"success": False, "error": "無效的請求"}, status=400)


#完成行程
def complete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    trip.status = "completed"
    trip.save()
    return redirect('view_trip', trip_id=trip.id)


@csrf_exempt  # 或用 @login_required，如果你有登入驗證
def reorder_trip_day(request, day_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_order = data.get("order", [])  # 前端送來的 attraction id list
            print("✅ 收到排序請求：", new_order)

            for index, attraction_id in enumerate(new_order):
                TripDayAttraction.objects.filter(id=attraction_id, trip_day_id=day_id).update(order=index)

            return JsonResponse({"success": True})
        except Exception as e:
            print("❌ 排序失敗：", e)
            return JsonResponse({"success": False, "error": str(e)})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)
