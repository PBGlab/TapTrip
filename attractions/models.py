from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Attraction(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey("City", on_delete=models.CASCADE, related_name="attractions")
    link = models.URLField()
    image_url = models.URLField()
    hashtag = models.CharField(max_length=255, blank=True)
    googlemap = models.URLField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.city.name})"
