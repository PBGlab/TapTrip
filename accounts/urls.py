from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path('logout/', views.logout_view, name='logout_page'),  # 顯示登出確認頁面
    path('logout-confirm/', views.logout_confirm, name='logout_confirm'),  # 真正執行登出
    path('email_verification_notice/',views.email_verification_notice_view, name='email_verification_notice'), # 提醒前往信箱驗證
    path("verify/<str:token>/", views.verify_email, name="verify_email"), # 顯示驗證確認頁面
    path("api/user-status/", views.user_status, name="user_status"),
    path("updatepassword/", views.updatepassword, name="updatepassword"),
]
