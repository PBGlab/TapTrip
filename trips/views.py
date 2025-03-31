from django.shortcuts import render, redirect, get_object_or_404
from .models import Trip, TripDay, TripDayAttraction 
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from lodging.models import Lodging
import json


from django.contrib.auth.decorators import login_required

#建立行程
@login_required
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




from django.shortcuts import render
from .models import Trip, TripDay, TripDayAttraction, TripLodging
from attractions.models import Attraction

#行程總表
@login_required(login_url='/login/')
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
            attractions = TripDayAttraction.objects.filter(trip_day=day).select_related("attraction").order_by("order")
            attraction_list = []
            for a in attractions:
                attraction_list.append({
                    "name": a.attraction.name,
                    "city": a.attraction.city.name,
                    "link": a.attraction.link,
                    "image_url": a.attraction.image_url,
                    "googlemap": a.attraction.googlemap,
                    "hashtag": a.attraction.hashtag,
                    "order": a.order,
                })

            days_data.append({
                "id": day.id,
                "date": day.date,
                "attraction_count": len(attraction_list),
                "attractions": attraction_list,
            })

        # ✅ 透過中介表 TripLodging 拿到該行程的所有住宿
        trip_lodgings = TripLodging.objects.filter(trip=trip).select_related("lodging")
        lodging_data = []
        for link in trip_lodgings:
            l = link.lodging
            lodging_data.append({
                "id": l.id,
                "name": l.name,
                "address": l.address,
                "checkin": l.check_in,
                "checkout": l.check_out,
                "price": l.price,
                "link": l.link,
                "image": l.image,
            })

        trip_data.append({
            "trip": trip,
            "total_days": total_days,
            "days": days_data,
            "has_lodging": bool(trip_lodgings),
            "lodgings": lodging_data,
        })

    return render(request, "mytrips.html", {"trip_data": trip_data})


from django.shortcuts import get_object_or_404, render, redirect
from .models import Trip, TripLodging, TripDay, TripDayAttraction
from django.contrib.auth.decorators import login_required

#更改行程狀態 → 完成行程
@login_required
def complete_trip(request, trip_id):
    
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)

    if request.method == 'POST':
        # ✅ 改變行程狀態
        trip.status = 'completed'
        trip.save()

        # ✅ 同步更新 Lodging 狀態
        trip_lodgings = TripLodging.objects.filter(trip=trip).select_related("lodging")
        for tl in trip_lodgings:
            lodging = tl.lodging
            lodging.status = 'completed'
            lodging.save()

        # ✅ 轉向查看「已完成行程」頁面（避免重新送出表單）
        return redirect('view_completed_trips')  # 請確保有設定這個 URL name

    # 若不是 POST → 可考慮導回行程主頁或顯示錯誤
    return redirect('mytrips')

# 查看已完成的行程 
@login_required
def view_completed_trips(request):
    completed_trips = Trip.objects.filter(user=request.user, status='completed')

    trip_data = []
    for trip in completed_trips:
        trip_days = TripDay.objects.filter(trip=trip).order_by("date")
        total_days = (trip.end_date - trip.start_date).days + 1

        days_data = []
        for day in trip_days:
            attractions = TripDayAttraction.objects.filter(trip_day=day).select_related("attraction").order_by("order")
            attraction_list = [{
                "name": a.attraction.name,
                "city": a.attraction.city.name,
                "link": a.attraction.link,
                "image_url": a.attraction.image_url,
                "googlemap": a.attraction.googlemap,
                "hashtag": a.attraction.hashtag,
                "order": a.order,
            } for a in attractions]

            days_data.append({
                "id": day.id,
                "date": day.date,
                "attraction_count": len(attraction_list),
                "attractions": attraction_list,
            })

        # 住宿
        trip_lodgings = TripLodging.objects.filter(trip=trip).select_related("lodging")
        lodging_data = [{
            "id": l.lodging.id,
            "name": l.lodging.name,
            "address": l.lodging.address,
            "checkin": l.lodging.check_in,
            "checkout": l.lodging.check_out,
            "price": l.lodging.price,
            "link": l.lodging.link,
            "image": l.lodging.image,
        } for l in trip_lodgings]

        trip_data.append({
            "trip": trip,
            "total_days": total_days,
            "days": days_data,
            "has_lodging": bool(lodging_data),
            "lodgings": lodging_data,
        })

    return render(request, 'complete_trips.html', {'trip_data': trip_data})


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
                    "hashtag": tda.attraction.hashtag,
                    "latitude": tda.attraction.latitude,
                    "longitude": tda.attraction.longitude
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


from .models import ExportedTrip

#產生分享連結
@login_required
def generate_share_link(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)

    # 如果已經存在，就不要重複產生
    exported, created = ExportedTrip.objects.get_or_create(trip=trip)

    share_url = request.build_absolute_uri(f'/share/{exported.share_token}/')
    return JsonResponse({'share_url': share_url})

from .utils import get_trip_detail_dict
#導向分享連結頁面
def shared_trip_view(request, token):
    exported = get_object_or_404(ExportedTrip, share_token=token)
    trip = exported.trip
    trip_data = get_trip_detail_dict(trip)  # 你之前封裝好的資料整理函式

    return render(request, 'shared_trip.html', {'trip_data': trip_data})
