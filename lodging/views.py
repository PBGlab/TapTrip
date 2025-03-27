from django.shortcuts import render, redirect
from .booking import scrape_booking
from attractions.models import City
from .models import Lodging

# Create your views here.

from django.http import JsonResponse
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
from django.conf import settings 

from django.http import JsonResponse

import threading

def booking(request):
    print("🔥 booking view 啟動！")

    if request.method == 'POST':
        city = request.POST.get('city')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        adults = request.POST.get('adults')
        children = request.POST.get('children')

        errors = {}

        try:
            checkin_date = datetime.strptime(checkin, '%Y-%m-%d')
            checkout_date = datetime.strptime(checkout, '%Y-%m-%d')
            if checkin_date >= checkout_date:
                errors['date_error'] = "入住日期必須早於退房日期"
        except ValueError:
            errors['date_error'] = "日期格式錯誤，請選擇有效日期"

        # ✅ 組出 redirect 目的地（無論哪種請求都會用到）
        redirect_url = f'/showhotel/?city={city}&checkin={checkin}&checkout={checkout}&adults={adults}&children={children}'

        # ✅ 如果有錯誤，處理回傳格式
        if errors:
            # 如果是 AJAX 請求，就回傳 JSON
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': errors['date_error']}, status=400)

            # 否則就是 HTML 表單，照舊回原畫面
            return render(request, 'booking.html', {
                "cities": City.objects.all(),
                "checkin": checkin,
                "checkout": checkout,
                "trip_name": request.GET.get('trip', ''),
                "errors": errors
            })

        # ✅ 沒錯誤，根據請求方式回傳
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'redirect_url': redirect_url})

        return redirect(redirect_url)

    # GET 請求（初始進入 booking 頁面）
    checkin = request.GET.get('checkin', '')
    checkout = request.GET.get('checkout', '')
    trip_name = request.GET.get('trip', '')

    return render(request, 'booking.html', {
        "cities": City.objects.all(),
        "checkin": checkin,
        "checkout": checkout,
        "trip_name": trip_name,
        "errors": {}
    })


from django.http import StreamingHttpResponse
import json


def stream_hotels(request):
    print("🧵 stream_hotels() 啟動，執行緒 ID:", threading.get_ident())
    city = request.GET.get('city')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    adults = request.GET.get('adults')
    children = request.GET.get('children')


    def event_stream():
        yield f"data: {json.dumps({'status': 'start', 'message': f'正在查詢 {city} 的飯店資訊'})}\n\n"  # ⬅️ 先丟一筆初始資料給前端
        try:
            for hotel in scrape_booking(city, checkin, checkout, adults, children):
                json_data = json.dumps(hotel, ensure_ascii=False)
                print(f"[stream-hotels] 傳送飯店：{hotel['名稱']}")
                yield f"data: {json_data}\n\n"
            yield "event: done\ndata: 完成載入\n\n"
        except Exception as e:
            print(f"[stream-hotels] 錯誤：{str(e)}")
            yield f"event: error\ndata: 發生錯誤：{str(e)}\n\n"

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


from trips.models import Trip  # 確保你有 import Trip

def showhotel(request):
    city = request.GET.get("city", "")
    checkin = request.GET.get("checkin", "")
    checkout = request.GET.get("checkout", "")
    adults = request.GET.get("adults", "1")
    children = request.GET.get("children", "0")

    # **取得當前使用者的行程**
    user_trips = Trip.objects.filter(user=request.user, status="draft") if request.user.is_authenticated else []

    return render(request, "showhotel.html", {
        "city": city,
        "checkin": checkin,
        "checkout": checkout,
        "adults": adults,
        "children": children,
        "user_trips": user_trips,  # ✅ 把行程傳到前端
    })



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Lodging
from django.contrib.auth.decorators import login_required
from trips.models import Trip, TripLodging

@csrf_exempt
@login_required
def book_hotel(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # **確保 trip 存在**
            trip_instance = Trip.objects.filter(id=data["trip_id"], user=request.user).first()
            if not trip_instance:
                return JsonResponse({"error": "無效的行程 ID 或權限不足"}, status=403)

            # **創建或獲取飯店**
            lodging, created = Lodging.objects.get_or_create(
                user=request.user,
                trip=trip_instance,  
                name=data["name"],
                check_in=data["checkin"],  
                check_out=data["checkout"],
                defaults={
                    "rating": data["rating"],
                    "link": data["link"],
                    "price": data["price"],
                    "address": data["address"],
                    "image": data["image"],
                    "status": "draft"
                }
            )
            
            if created:
                # **建立 `TripLodging` 關聯**
                trip_lodging, created_trip_lodging = TripLodging.objects.get_or_create(
                    trip=trip_instance,
                    lodging=lodging
                )
                return JsonResponse({"message": "住宿已成功預訂!"})
            
            return JsonResponse({"message": "您已預定該飯店"})
            

        except json.JSONDecodeError:
            return JsonResponse({"error": "無效的 JSON 格式"}, status=400)
        except Exception as e:
            import traceback
            traceback.print_exc()  # ✅ 在 Console 顯示錯誤完整資訊
            return JsonResponse({"error": f"伺服器錯誤: {str(e)}"}, status=500)

    return JsonResponse({"error": "只接受 POST 請求"}, status=405)



from django.shortcuts import render, redirect
from trips.models import Trip, TripLodging
from lodging.models import Lodging

@login_required
def lodging(request):
    # 取得當前用戶「草稿」狀態的行程
    draft_trips = Trip.objects.filter(user=request.user, status='draft')

    # **判斷是否有「草稿行程」**
    if not draft_trips.exists():
        
        return render(request, "lodging.html")  # ✅ 沒有草稿行程，跳轉到 lodging.html

    # **準備資料**
    trip_data = []
    for trip in draft_trips:
        trip_lodgings = TripLodging.objects.filter(trip=trip)  # 取得 `TripLodging` (行程與住宿的關聯)
        
        # **從 `TripLodging` 取出完整的 `Lodging` 資料**
        lodgings = [trip_lodging.lodging for trip_lodging in trip_lodgings]

        trip_data.append({
            "trip": trip,
            "lodgings": lodgings if lodgings else None  # 如果有住宿就顯示完整 `Lodging`，否則為 None
        })

    return render(request, "stay-management.html", {"trip_data": trip_data})  # ✅ 有草稿行程，跳轉到 stay-management.html

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from lodging.models import Lodging

@csrf_exempt
def delete_lodging(request, lodging_id):
    if request.method == "DELETE":
        try:
            lodging = Lodging.objects.get(id=lodging_id, user=request.user)
            lodging.delete()
            return JsonResponse({"success": True})
        except Lodging.DoesNotExist:
            return JsonResponse({"success": False, "error": "找不到該住宿或沒有權限"}, status=404)
    
    return JsonResponse({"success": False, "error": "只允許 DELETE 請求"}, status=405)



from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Lodging  # 依你的資料表調整

@login_required
def get_lodgings_by_trip(request, trip_id):
    lodgings = Lodging.objects.filter(trip_id=trip_id).values(
        'id', 'name', 'address', 'price', 'image', 'link', 'check_in', 'check_out'
    )
    return JsonResponse({'lodgings': list(lodgings)})