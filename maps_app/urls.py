from django.urls import path
from .views import show_map

urlpatterns = [
    path("", show_map, name="show_map"),  # 讓 `/maps/` 顯示地圖
]
