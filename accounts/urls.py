from django.urls import path , include
from accounts import views



urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path('logout/', views.logout_view, name='logout_page'),  # 顯示登出確認頁面
    path('logout-confirm/', views.logout_confirm, name='logout_confirm'),  # 真正執行登出
    path('email_verification_notice/',views.email_verification_notice_view, name='email_verification_notice'), # 提醒前往信箱驗證
    path("verify/<str:token>/", views.verify_email, name="verify_email"), # 顯示驗證確認頁面
    path("api/user-status/", views.user_status, name="user_status"),
    path("updatepassword/", views.updatepassword, name="updatepassword"),
    path("accounts/", include("allauth.urls")),  # Google OAuth API
    path('forgot-password/', views.forgot_password, name='forgot_password'), #忘記密碼
    path('reset-password/<str:token>/', views.reset_password, name='reset_password') #重設密碼

]
