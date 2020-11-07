import requests
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from django.http import Http404
import datetime

from .models import City
from .forms import CityForm

from .models import Custom_station
from .forms import CustomStationForm

import json
from geopy.geocoders import Nominatim

# Create your views here.


def index(request):
    pollution_API_key = 'aV4cM5PIhRFvnfP4tiN1Cx2TAa8s1sf0'

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4f651df2ff6276adea68dcbe6c969c94'

    airly_api_url = 'https://airapi.airly.eu/v2/measurements/nearest?lat={}&lng={}&maxDistanceKM=50&apikey=' + pollution_API_key

    print("The request is: ")
    print(request)
    print("\n")

    if request.method == 'POST':

        # copying POST request because original QueryDict cannot be modified
        POST_copy = request.POST.copy()

        # if only city_name is provided, city latitude and longtidude is None
        #
        if request.POST.get('city_latitude') is None and request.POST.get('city_longitude') is None:
            print("City latitude and longitude is None")

            # Getting approximate coordinates for user selected city - seems that this api is sometimes not working (api itself is getting 500 errors)
            try:
                address = request.POST.get('city_name')
                geolocator = Nominatim(user_agent="Your_Name")
                location = geolocator.geocode(address)
                print('printing location address: ', location.address)
                print('printing location latitude and longtitude: ',
                      location.latitude, location.longitude)

                city_latitude = location.latitude
                city_longitude = location.longitude

                # print('Printing city longtitude type: ', type(city_longitude))
                city_latitude = format(city_latitude, '.6f')
                city_longitude = round(city_longitude, 6)
                print('printing location latitude and longtitude after formating: ',
                      city_latitude, city_longitude)

                POST_copy['city_latitude'] = city_latitude
                POST_copy['city_longitude'] = city_longitude

                print(POST_copy['city_name'])
                print(POST_copy['city_latitude'])
            except:
                print('Geolocator API problem...')

        else:
            print("City latitude and longitude is not None")

            city_latitude = request.POST.get('city_latitude')
            city_longitude = request.POST.get('city_longitude')

            print('printing location latitude and longtitude: ',
                  city_latitude, city_longitude)

            try:
                geolocator = Nominatim(user_agent="geoapiExercises")
                coordinates = city_latitude + ", " + city_longitude
                print(coordinates)
                ####################################################################
                location = geolocator.reverse(coordinates, exactly_one=True)
                address = location.raw['address']
                city_geolocation = address.get('city', '')

                POST_copy['city_name'] = city_geolocation
            except:
                print('Geolocator API problem...')

        # checking if specified city exists (is in API)

        check_for_city = requests.get(
            airly_api_url.format(city_latitude, city_longitude))

        # check_for_city.raise_for_status() #for later - each exception handled?

        converted_response = str(check_for_city.status_code)
        print('City check response: ', converted_response)

        if converted_response == "200":

            # Checking if there is data available at selected city

            check_for_city = check_for_city.json()
            with open('response_check.json', 'w') as outfile:
                json.dump(check_for_city, outfile)

            try:
                # there are some sensors like: Zabrze that have only 4 indexes and none of them are temp/humid/pm
                # for now getting rid of them not to cause an error

                print(check_for_city['current']['values'][5]['value'])
                # print(type((check_for_city['current']['values'][0]['value'])))

            except:
                print(
                    "An exception occurred - sesnor does not contain data or data is corrupted")

            else:

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
                    print("Form is valid - saving in DB")

                    # data = form['city_latitude']
                    # print(data)

                    form.save(commit=True)  # commiting our data to database

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

        r = requests.get(airly_api_url.format(
            city.city_latitude, city.city_longitude)).json()

        print('requested url: ', airly_api_url.format(
            city.city_latitude, city.city_longitude))
        with open('recent_response.json', 'w') as outfile:
            json.dump(r, outfile)

        # r['current']['values'][1] have random indexes depending on the station...
        pollution_city = {
            'city_name': city.city_name,
            'city_latitude': city.city_latitude,
            'city_longitude': city.city_longitude,
            'temperature': r['current']['values'][5]['value'],
            'humidity': r['current']['values'][4]['value'],
            'pm2_5': r['current']['values'][1]['value'],
            'pm10': r['current']['values'][2]['value'],

            'description': r['current']['indexes'][0]['description'],
            'color': r['current']['indexes'][0]['color'],
        }

        print(pollution_city)
        weather_data.append(pollution_city)

    # context_pollution = {'pollution_data': pollution_data,
    #                      'station_form': station_form}

    # context = {'weather_data': weather_data, 'form': form,  # data from weather
    #            'pollution_data': pollution_data, 'station_form': station_form}  # data from pollution

    context = {'weather_data': weather_data,
               'form': form}  # data from weather
    return render(request, 'pollution/pollution.html', context)


def custom(request):

    # the request for sensor data is at http://192.168.0.29:8082/data

    url_for_data = 'http://{}:{}/data'
    url_for_response_check = 'http://{}:{}'

    print("The request is: ")
    print(request)
    print("\n")

    if request.method == 'POST':

        # copying POST request because original QueryDict cannot be modified
        POST_copy = request.POST.copy()

        print('The post request is: ', POST_copy)
        print(request.POST.get('station_ip'), request.POST.get('station_port'))

        check_for_response = requests.get(
            url_for_response_check.format(request.POST.get('station_ip'), request.POST.get('station_port')))

        # check_for_city.raise_for_status() #for later - each exception handled?

        converted_response = str(check_for_response.status_code)
        print('City check response: ', converted_response)

        if converted_response == "200":

            pub_date = datetime.datetime.now()
            print(pub_date)
            POST_copy['station_adding_date'] = pub_date

            form = CustomStationForm(POST_copy)

            if form.is_valid():
                print("Form is valid - saving in DB")

                form.save(commit=True)  # commiting our data to database

            else:
                print("form is not valid")
        else:
            print("POST response is not 200 - error:", converted_response)
            # add some kind of communicate for wrong city
            # return HttpResponse("City not found")

    form = CustomStationForm()

    stations = Custom_station.objects.all()

    weather_data_custom = []

    for station in stations:

        r = requests.get(url_for_data.format(
            station.station_ip, station.station_port)).json()

        print('requested url: ', url_for_data.format(
            station.station_ip, station.station_port))
        with open('recent_response_station.json', 'w') as outfile:
            json.dump(r, outfile)

        # r['current']['values'][1] have random indexes depending on the station...
        pollution_custom_station_data = {
            'city_name': r['current']['indexes'][0]['stationcity'],
            'station_ip': station.station_ip,
            'station_port': station.station_port,
            'temperature': r['current']['values'][5]['value'],
            'humidity': r['current']['values'][4]['value'],
            'pm2_5': r['current']['values'][1]['value'],
            'pm10': r['current']['values'][2]['value'],

            'description': r['current']['indexes'][0]['description'],
            'color': r['current']['indexes'][0]['color'],
        }

        print(pollution_custom_station_data)
        weather_data_custom.append(pollution_custom_station_data)

    context = {'weather_data_custom': weather_data_custom,
               'form': form}  # data from weather

    return render(request, 'custom/custom.html', context)
