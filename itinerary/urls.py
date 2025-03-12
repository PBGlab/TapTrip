from django.urls import path
from .views import plan_itinerary,create_itinerary,get_itinerary,cart_view

urlpatterns = [

    path("plan/",plan_itinerary,name="plan_itinerary"),
    path('create/', create_itinerary, name='create_itinerary'),  # 設定 create_itinerary 路由
    path("itinerary/", get_itinerary, name="get_current_itinerary"),  # 查詢最新行程
    path("itinerary/<int:itinerary_id>/", get_itinerary, name="get_itinerary"),  # 查詢特定行程
    path("itinerary/cart/", cart_view, name="cart_view"),  # ✅ 確保這行存在
]


