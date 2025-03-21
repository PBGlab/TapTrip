from django.urls import path
from .views import create_trip, delete_trip, list_trips, complete_trip,add_to_trip,api_trips,delete_attraction
urlpatterns = [
    # 顯示「建立行程」頁面
    path('create/', create_trip, name='create_trip'),

    # 刪除行程
    path('delete_trip/<int:trip_id>/', delete_trip, name='delete_trip'), 

    # 顯示「我的行程」列表
    path('trips/', list_trips, name='list_trips'),  

    #添加景點
    path('api/add-to-trip/', add_to_trip, name='add_to_trip'),

    # 刪除景點
    path("api/delete-attraction/<int:attraction_id>/", delete_attraction, name="delete_attraction"),

    #在添加景點列表及時顯示行程清單
    path("api/trips/", api_trips, name="api_trips"), 

    # 完成行程
    path('complete/<int:trip_id>/', complete_trip, name='complete_trip'),
]