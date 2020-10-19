import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


from .models import Pollution_station
from .forms import StationForm
import json

# additional stuff - httpresponse
from django.http import HttpResponse
from django.template import loader

from django.http import Http404


# def add_city_validation(request):
#     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4f651df2ff6276adea68dcbe6c969c94'

#     form = CityForm(request.POST)
#     print("City is found\n")
#     form.save()

#     r = request.get(url.format(city)).json()
#     print(r)
#     print( r['cod'])
#     if  r['cod'] is "200":
#         print("City found\n")
#         return True
#     else:
#         print("City not found\n")
#         return False


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4f651df2ff6276adea68dcbe6c969c94'
    print("The request is: ")
    print(request)
    print("\n")

    if request.method == 'POST':
        print(request.POST.get('name'))

        city_to_check = request.POST.get('name')

        # checking if specified city exists
        check_for_city = requests.get(url.format(city_to_check))

        # check_for_city.raise_for_status() #for later - each exception handled?

        # # check  and print type of num variable
        # print(type(check_for_city.status_code))

        converted_response = str(check_for_city.status_code)

        print(converted_response)
        if converted_response == "200":
            form = CityForm(request.POST)
            form.save()
            print("POST response is 200 - city exists")
        else:
            print("POST response is not 200 - error:", converted_response)
            # add some kind of communicate for wrong city
            # return HttpResponse("City not found")

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'humidity': r['main']['humidity'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    # context = {'weather_data': weather_data, 'form': form}


    # TODO: finish adding pollution data
    station_form = StationForm()

    stations = Pollution_station.objects.all()

    pollution_data = []

    # context_pollution = {'pollution_data': pollution_data,
    #                      'station_form': station_form}

    context = {'weather_data': weather_data, 'form': form,  # data from weather
               'pollution_data': pollution_data, 'station_form': station_form}  # data from pollution
    return render(request, 'weather/weather.html', context)


def detail(request, city_id):
    cities = City.objects.all()
    city_name = cities[city_id].name

    print(cities[city_id].name)
    response = "You're looking at the detail of City: {} with ID: {} \n".format(
        city_name, city_id)
    return HttpResponse(response)

# def detail(request, city):
#     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4f651df2ff6276adea68dcbe6c969c94'

#     #question = Question.objects.get(pk=city)
#     print(request)
#     print(city)

#     form = CityForm()

#     # cities = City.objects.all()

#     weather_data_single = []


#     r = requests.get(url.format(city)).json()
#     print(r)

#     #{"cod":"404","message":"city not found"}k
#     # if r['cod'] = '404':
#     #     print("detcted 404")

#     city_weather_single = {
#         'city' : city.name,
#         'temperature' : r['main']['temp'],
#         'humidity' : r['main']['humidity'],
#         'description' : r['weather'][0]['description'],
#         'icon' : r['weather'][0]['icon'],
#     }

#     weather_data_single.append(city_weather_single)

#     context = {'weather_data' : weather_data_single, 'form' : form}
#     # return render(request, 'weather/weather.html', context)

#     response = "You're looking at the detail of City {}.\n".format(city)
#     return HttpResponse(response % context)
