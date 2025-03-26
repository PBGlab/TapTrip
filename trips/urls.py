from django.urls import path
from .views import create_trip, delete_trip, list_trips, complete_trip,add_to_trip,api_trips,delete_attraction ,reorder_trip_day ,view_completed_trips
from .views import generate_share_link ,shared_trip_view

urlpatterns = [
    # 顯示「建立行程」頁面
    path('create/', create_trip, name='create_trip'),

    # 刪除行程
    path('delete_trip/<int:trip_id>/', delete_trip, name='delete_trip'), 

    # 顯示「我的行程」列表
    path('trips/', list_trips, name='list_trips'),  

    # 添加景點
    path('api/add-to-trip/', add_to_trip, name='add_to_trip'),

    # 刪除景點
    path("api/delete-attraction/<int:attraction_id>/", delete_attraction, name="delete_attraction"),

    #在添加景點列表及時顯示行程清單
    path("api/trips/", api_trips, name="api_trips"), 

    # 完成行程
    path('trip/<int:trip_id>/complete/', complete_trip, name='complete_trip'),

    # 查看已完成的行程 
    path('trips/completed/', view_completed_trips, name='view_completed_trips'),


    # 接收前端送來的景點排序結果，更新 TripDayAttraction 中的順序（order 欄位）
    path("api/trip-day/<int:day_id>/reorder/", reorder_trip_day, name="reorder_trip_day"),

    #產生分享連結
    path('trip/<int:trip_id>/share/', generate_share_link, name='generate_share_link'),
    
    #導向分享連結頁面
    path('share/<str:token>/', shared_trip_view, name='shared_trip_view'),

]