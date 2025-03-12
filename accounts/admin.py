from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser  # ✅ 載入自訂使用者模型

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_superuser', 'is_staff', 'is_active', 'is_email_verified', 'date_joined')
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'is_email_verified')  # ✅ 讓你可以篩選 Superuser
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_superuser", "is_staff", "is_email_verified")}),  # ✅ 清楚顯示權限
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)  # 顯示管理員及用戶