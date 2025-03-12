# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
from attractions.models import Attraction  # 景點來自 attractions 應用

class Itinerary(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()

    def __str__(self):
      return f"行程 ID: {self.id} - {self.user.username}"

class Day(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name="days", on_delete=models.CASCADE)
    date = models.DateField()
    attractions = models.ManyToManyField(Attraction, related_name="days", blank=True)
    accommodations = models.ManyToManyField('Accommodation', related_name="days", blank=True)

    def __str__(self):
        return f"Day {self.date} of itinerary {self.itinerary.id}"
        
class Accommodation(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    booking_url = models.URLField()

    def __str__(self):
        return self.name