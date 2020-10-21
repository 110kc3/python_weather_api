from django.forms import ModelForm, TextInput
from .models import City


class CityForm(ModelForm):
    class Meta:
        model = City
        # each field from database has to be specified here
        fields = ['city_name', 'city_latitude',
                  'city_longitude', 'city_adding_date']
        widgets = {'city_name': TextInput(
            attrs={'class': 'input', 'placeholder': 'City Name'})}


# class StationForm(ModelForm):
#     class Meta:
#         model = City
#         fields = ['city_latitude', 'city_longitude']
#         widgets = {'city_latitude': NumberInput(attrs={'class': 'input', 'placeholder': 'Station latitude '}, 'city_longitude': NumberInput(attrs={'class': 'input', 'placeholder': 'Station longitude '})}


# class City(models.Model):
#     city_name = models.CharField(max_length=40)

#     city_latitude = models.FloatField(
#         validators=[MinValueValidator(-90), MaxValueValidator(90)])
#     city_longitude = models.FloatField(
#         validators=[MinValueValidator(-90), MaxValueValidator(90)])

#     city_adding_date = models.DateTimeField('date added')

#     def __str__(self):
#         return self.city_name

#     class Meta:
#         verbose_name = "city"
#         verbose_name_plural = 'cities'

#     def was_added_recently(self):
#         return self.city_adding_date >= timezone.now() - datetime.timedelta(days=1)
