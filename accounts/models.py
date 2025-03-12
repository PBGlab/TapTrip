from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.crypto import get_random_string

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)  # ✅ Email 是否驗證
    email_verification_token = models.CharField(max_length=64, blank=True, null=True)  # ✅ Email 驗證 Token

    # ✅ 避免與 Django 內建 `auth_user` 欄位衝突
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True
    )

    def generate_verification_token(self):
        """ 產生隨機驗證 Token """
        self.email_verification_token = get_random_string(32)
        self.save()
