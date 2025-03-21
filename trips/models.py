from django.db import models
from django.conf import settings
from attractions.models import Attraction

class Trip(models.Model):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('completed', '已完成'),
    ]
    
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.name


class TripDay(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="days")
    date = models.DateField()
    
    attractions = models.ManyToManyField(Attraction, through="TripDayAttraction", blank=True)  # ✅ 正確的 M2M 設定

    def __str__(self):
        return f"{self.trip.name} - {self.date}"


class TripDayAttraction(models.Model):
    trip_day = models.ForeignKey(TripDay, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)    
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "trips_tripdayattraction"  # ✅ 明確指定 Django 應該使用的表名
        ordering = ["order"]

    def __str__(self):
        return f"{self.trip_day.trip.name} - {self.trip_day.date} - {self.order}: {self.attraction.name}"



   
class TripLodging(models.Model):
    """行程與住宿的關聯表，讓 `Trip` 連接 `Lodging`"""
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="lodgings")  # ✅ `Trip` 可以有多個 `Lodging`
    lodging = models.ForeignKey("lodging.Lodging", on_delete=models.CASCADE, related_name="trip_lodgings")  # ✅ 連接 `lodging.Lodging`

    def __str__(self):
        return f"{self.trip.name} - {self.lodging.name} ({self.lodging.check_in} ~ {self.lodging.check_out})"