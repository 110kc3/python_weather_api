
from django.db import models
from django.db.models import Model
from geopy.geocoders import Nominatim  # city to latitude and longtitude

import datetime
# form validator to city lantitide and longtitude
from django.core.validators import MaxValueValidator, MinValueValidator


from django.utils import timezone
# Create your models here.


class City(models.Model):
    city_name = models.CharField(max_length=40)
    
    city_latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)])
    city_longitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)])

    city_adding_date = models.DateTimeField('date added')

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = "city"
        verbose_name_plural = 'cities'

    def was_added_recently(self):
        return self.city_adding_date >= timezone.now() - datetime.timedelta(days=1)


# class Coordinates(models.Model):
#     question = models.ForeignKey(City, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)