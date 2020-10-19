from django.forms import ModelForm, TextInput
from .models import City
from .models import Pollution_station


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name': TextInput(
            attrs={'class': 'input', 'placeholder': 'City Name'})}


class StationForm(ModelForm):
    class Meta:
        model = Pollution_station
        fields = ['station_name']
        widgets = {'station_name': TextInput(
            attrs={'class': 'input', 'placeholder': 'Station Latitude and Longitude'})}


# class City(models.Model):
#     name = models.CharField(max_length=25)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name_plural = 'cities'


# class Pollution_station(models.Model):
#     station_name = models.CharField(max_length=40)
#     # station_latitude  = models.FloatField(max_length=40)
#     # station_longitude  = models.FloatField(max_length=40)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name_plural = 'pollution_stations'
