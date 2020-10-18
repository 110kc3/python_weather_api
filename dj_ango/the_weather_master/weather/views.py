import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


#additional stuff - httpresponse
from django.http import HttpResponse
from django.template import loader

from django.http import Http404

# def index(request):
#     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4f651df2ff6276adea68dcbe6c969c94'

#     # if request.method == 'POST':
#     #     form = CityForm(request.POST)
#     #     form.save()

#     form = CityForm()

#     cities = City.objects.all()

#     weather_data = []

#     for city in cities:

#         r = requests.get(url.format(city)).json()

#         #{"cod":"404","message":"city not found"}k
#         # if r['cod'] = '404':
#         #     print("detcted 404")

#         city_weather = {
#             'city' : city.name,
#             'temperature' : r['main']['temp'],
#             'humidity' : r['main']['humidity'],
#             'description' : r['weather'][0]['description'],
#             'icon' : r['weather'][0]['icon'],
#         }

#         weather_data.append(city_weather)

#     context = {'weather_data' : weather_data, 'form' : form}
#     return render(request, 'weather/weather.html', context)


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4f651df2ff6276adea68dcbe6c969c94'
    print("The request is: ")
    print(request)
    print("\n")
    if request.method == 'POST':
        print("Inside POST")
        form = CityForm(request.POST)
        if form.is_valid():
            print("FORM IS VALID\n")
            form.save()
        else:
            print("FORM NOT VALID\n")
            return HttpResponse("City not found")

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()
        
        #{"cod":"404","message":"city not found"}k
        # if r['cod'] = '404':
        #     print("detcted 404")

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'humidity' : r['main']['humidity'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)

def detail(request, city_id):
    cities = City.objects.all()
    city_name=cities[city_id].name

    print(cities[city_id].name)
    response = "You're looking at the detail of City: {} with ID: {} \n".format(city_name, city_id)
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
