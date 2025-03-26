from django.urls import path
from lodging import views
from django.urls import re_path as url

urlpatterns = [
    url(r'^booking/',views.booking,name="booking"), #定房畫面
    url(r'^lodging/',views.lodging,name="lodging"), #管理住宿頁面
    path('stream-hotels/', views.stream_hotels, name='stream_hotels'),  # SSE 路由 傳遞爬蟲結果
    path('showhotel/', views.showhotel, name='showhotel'), #搜尋結果
    path("book_hotel/", views.book_hotel, name="book_hotel"), #預定飯店
    path("delete_lodging/<int:lodging_id>/", views.delete_lodging, name="delete_lodging"), #刪除飯店路由
    path('api/get_lodgings_by_trip/<int:trip_id>/', views.get_lodgings_by_trip, name='get_lodgings_by_trip'),

]