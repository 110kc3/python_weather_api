from django.contrib import admin

from .models import City

from .models import Custom_station
# Register your models here.


admin.site.register(City)
admin.site.register(Custom_station)
