from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """ Google 登入後，檢查 Email 並自動註冊或關聯 """
        email = sociallogin.account.extra_data.get("email")

        if not email:
            raise ValueError("Google 帳戶未提供 Email")

        try:
            user = User.objects.get(email=email)
            sociallogin.connect(request, user)  # 直接關聯帳號
        except User.DoesNotExist:
            # 確保 username 唯一
            base_username = email.split("@")[0]
            username = base_username
            count = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{count}"
                count += 1

            # 創建新 CustomUser
            user = User.objects.create(
                username=username,
                email=email,
                is_email_verified=True,  # ✅ 設定 Email 已驗證
                is_active=True,  # ✅ 啟用帳號
            )
            sociallogin.connect(request, user)  # 讓 Google 帳號關聯 CustomUser
