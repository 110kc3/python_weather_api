from django.db import models


class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'


class Pollution_station(models.Model):
    station_name = models.CharField(max_length=40)
    # station_latitude  = models.FloatField(max_length=40)
    # station_longitude  = models.FloatField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'pollution_stations'
