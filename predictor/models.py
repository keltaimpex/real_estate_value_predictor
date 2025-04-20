from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sqft_living = models.FloatField()
    bedrooms = models.IntegerField()
    bathrooms = models.FloatField()
    grade = models.IntegerField()
    floors = models.FloatField()
    sqft_lot = models.FloatField()
    house_age = models.IntegerField()
    sqft_living15 = models.FloatField()
    lat = models.FloatField()
    long = models.FloatField()
    predicted_price_min = models.FloatField()
    predicted_price_max = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp.date()}"