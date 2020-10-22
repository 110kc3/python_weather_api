import requests
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from django.http import Http404
import datetime

from .models import City
from .forms import CityForm


import json
from geopy.geocoders import Nominatim

# Create your views here.


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4f651df2ff6276adea68dcbe6c969c94'
    print("The request is: ")
    print(request)
    print("\n")

    if request.method == 'POST':

        # if only city_name is provided, city latitude and longtidude is None

        # print(request.POST.get('city_latitude')) #returns None

        # copying POST request because original QueryDict cannot be modified
        POST_copy = request.POST.copy()

        # Getting approximate coordinates for user selected city
        address = request.POST.get('city_name')
        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(address)
        print('printing location address: ', location.address)
        print(('printing location latitude and longtitude: ',
               location.latitude, location.longitude))

        city_latitude = location.latitude
        city_longitude = location.longitude

        # print('Printing city longtitude type: ', type(city_longitude))
        city_latitude = format(city_latitude, '.2f')
        city_longitude = round(city_longitude, 2)
        print('printing location latitude and longtitude after formating: ',
              city_latitude, city_longitude)

        POST_copy['city_latitude'] = city_latitude
        POST_copy['city_longitude'] = city_longitude

        # print(POST_copy['city_name'])
        # print(POST_copy['city_latitude'])

        city_to_check = POST_copy['city_name']

        # checking if specified city exists (is in API)
        check_for_city = requests.get(url.format(city_to_check))

        # check_for_city.raise_for_status() #for later - each exception handled?

        # # check  and print type of num variable
        # print(type(check_for_city.status_code))

        converted_response = str(check_for_city.status_code)
        print('City check response: ', converted_response)

        if converted_response == "200":

            # print('City latitude before form assigning: ',
            #       POST_copy['city_latitude'])

            pub_date = datetime.datetime.now()
            print(pub_date)
            POST_copy['city_adding_date'] = pub_date

            form = CityForm(POST_copy)

            # print('City latitude after form assigning: ',
            #       POST_copy['city_latitude'])

            # print('City latitude after form assigning: ',
            #       form['city_latitude'])

            if form.is_valid():
                print("form is valid")

                # data = form['city_latitude']
                # print(data)

                form.save(commit=True)  # commiting our data to database
                print("POST response is 200 - city exists")
            else:
                print("form is not valid")
        else:
            print("POST response is not 200 - error:", converted_response)
            # add some kind of communicate for wrong city
            # return HttpResponse("City not found")

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        pollution_city = {
            'city_name': city.city_name,
            # 'city_latitude'
            # 'city_longitude'
            'temperature': r['main']['temp'],
            'humidity': r['main']['humidity'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(pollution_city)

    # context_pollution = {'pollution_data': pollution_data,
    #                      'station_form': station_form}

    # context = {'weather_data': weather_data, 'form': form,  # data from weather
    #            'pollution_data': pollution_data, 'station_form': station_form}  # data from pollution

    context = {'weather_data': weather_data,
               'form': form}  # data from weather
    return render(request, 'pollution/pollution.html', context)
