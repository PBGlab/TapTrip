from django.db import models
from django.conf import settings  # 使用 AUTH_USER_MODEL

class Lodging(models.Model):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('completed', '已完成'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    trip = models.ForeignKey("trips.Trip", on_delete=models.CASCADE)  
    name = models.CharField(max_length=255)  
    rating = models.CharField(max_length=10, blank=True)  
    link = models.URLField(blank=True,max_length=1000)  
    price = models.CharField(max_length=50, blank=True)  
    address = models.CharField(max_length=255, blank=True)  
    image = models.URLField(blank=True)  
    check_in = models.CharField(max_length=20, blank=True)  
    check_out = models.CharField(max_length=20, blank=True)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')  # ✅ 新增狀態欄位

    def __str__(self):
        return f"{self.name} - {self.address} - {self.price} ({self.check_in} ~ {self.check_out})"
