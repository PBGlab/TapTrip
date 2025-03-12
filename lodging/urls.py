from django.urls import path
from lodging import views
from django.urls import re_path as url

urlpatterns = [
    url(r'^booking/',views.booking,name="booking"),
    url(r'^lodging/',views.lodging,name="lodging"),
    path('stream-hotels/', views.stream_hotels, name='stream_hotels'),  # SSE 路由
    path('showhotel/', views.showhotel, name='showhotel'),
]