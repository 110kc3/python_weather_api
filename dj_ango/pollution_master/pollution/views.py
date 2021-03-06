import requests
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.shortcuts import redirect

from django.http import Http404
import datetime

from .models import City

from .forms import CityForm

from .models import Custom_station
from .forms import CustomStationForm

from .models import User

from django.contrib.auth.models import User

import json
from geopy.geocoders import Nominatim

from django.contrib import messages


from django.contrib.auth.decorators import login_required

from register.models import Profile

# Create your views here.

# test station ip: 192.168.0.29
# test station port: 8082

@login_required
def index(request):

    pollution_API_key = ''

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4f651df2ff6276adea68dcbe6c969c94'

    airly_api_url = 'https://airapi.airly.eu/v2/measurements/nearest?lat={}&lng={}&maxDistanceKM=50&apikey=' + pollution_API_key

    print(request.user.id)
    # city = City.objects.get(id=id)

    api_users = Profile.objects.all()
    api_key = ''
    city_found = False

    for api_user in api_users:
        print('user with id: ', request.user.id,
              ' requesting key form user ', api_user.user_id)
        if request.user.id is api_user.user_id:
            api_key = api_user.api_key

    print('User api_key is: ', api_key)

    # need api key validation uppon registering
    pollution_API_key = api_key

    # print("The request is: ")
    # print(request)
    # print("\n")

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
                city_found = True
            except:
                print('Geolocator API problem...')
                messages.info(
                    request, 'An exception occurred - Geolocator API (external service) problem')
                city_found = False

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
                city_found = True
            except:
                print('Geolocator API problem...')
                messages.info(
                    request, 'An exception occurred - Geolocator API (external service) problem')
                city_found = False

        if city_found == True:
            # checking if specified city exists (is in API)
            check_for_city = requests.get(airly_api_url.format(city_latitude, city_longitude))
        

            # check_for_city.raise_for_status() #for later - each exception handled?

            converted_response = str(check_for_city.status_code)
            print('City check response: ', converted_response)
            
            if converted_response == "200":

                # Checking if there is data available at selected city

                check_for_city = check_for_city.json()
                # with open('response_check.json', 'w') as outfile:
                #     json.dump(check_for_city, outfile)

                try:
                    # there are some sensors like: Zabrze that have only 4 indexes and none of them are temp/humid/pm
                    # for now getting rid of them not to cause an error

                    print(check_for_city['current']['values'][5]['value'])
                    # print(type((check_for_city['current']['values'][0]['value'])))

                except:
                    print(
                        "An exception occurred - sensor does not contain data or data is corrupted")
                    messages.info(
                        request, 'An exception occurred - found sensor does not contain data or data is corrupted')

                else:

                    # print('City latitude before form assigning: ',
                    #       POST_copy['city_latitude'])

                    pub_date = datetime.datetime.now()
                    print(pub_date)
                    POST_copy['city_adding_date'] = pub_date

                    POST_copy['user'] = request.user.id

                    print(request.user.id)
                    print(POST_copy['user'])

                    form = CityForm(POST_copy)

                    # print('City latitude after form assigning: ',
                    #       POST_copy['city_latitude'])

                    # print('City latitude after form assigning: ',
                    #       form['city_latitude'])

                    if form.is_valid():
                        print("Form is valid - saving in DB")
                        messages.info(
                            request, 'Received good response, adding to Database')

                        form.save(commit=True)  # commiting our data to database
                        return redirect('/pollution')

                    else:
                        print("form is not valid")
                        messages.info(request, 'Form is not valid')
            else:
                print("POST response is not 200 - error:", converted_response)
                messages.info(
                    request, 'POST response is not 200 - error')
                # add some kind of communicate for wrong city
                # return HttpResponse("City not found")

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    # print every city with id=request.user.id

    for city in cities:
        print('I am user with id', request.user.id,
              'requesting data from city with id:', city.id, ' with user id of', city.user.id)

        # restrict view of cities not added by specific user
        if request.user.id is city.user.id:

            
            r = requests.get(airly_api_url.format(city.city_latitude, city.city_longitude)).json()
    
            # except:  # if station is not sending data
            #     print('Request failed with station is not sending data')
            #     messages.info(
            #         request, 'Problem with accessing station data - something wrong with station or API key')
                
            #     pollution_city = {
            #         'id': city.id,
            #         'city_name': city.city_name,
            #         'city_latitude': city.city_latitude,
            #         'city_longitude': city.city_longitude,
            #         'temperature': 0,
            #         'humidity': 0,
            #         'pm2_5': 0,
            #         'pm10': 0,

            #         'description': 'Station error',
            #         'color': '#FFFFFF',
            #     }
            #     print(pollution_city)
            #     weather_data.append(pollution_city)

            #     break


            # with open('recent_response.json', 'w') as outfile:
            #     json.dump(r, outfile)

            # r['current']['values'][1] have random indexes depending on the station...
            pollution_city = {
                'id': city.id,
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


@login_required
def deleteCity(request, id):
    # print('Request: ', request, ' with id: ', id)
    city = City.objects.get(id=id)
    city.delete()
    return redirect('/pollution')


@login_required
def deleteStation(request, id):
    # print('Request: ', request, ' with id: ', id)

    station = Custom_station.objects.get(id=id)
    station.delete()
    return redirect('/pollution/custom')


@login_required
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

        try:
            check_for_response = requests.get(url_for_response_check.format(
                request.POST.get('station_ip'), request.POST.get('station_port')))

            # check_for_city.raise_for_status() #for later - each exception handled?

            converted_response = str(check_for_response.status_code)
            print('Station check response: ', converted_response)

            if converted_response == "200":

                pub_date = datetime.datetime.now()
                print(pub_date)
                POST_copy['station_adding_date'] = pub_date
                POST_copy['user'] = request.user.id

                form = CustomStationForm(POST_copy)

                if form.is_valid():
                    print("Form is valid - saving in DB")
                    messages.info(
                        request, 'Received good response, adding to Database')
                    form.save(commit=True)  # commiting our data to database
                    return redirect('/pollution/custom')

                else:
                    print("form is not valid")
                    messages.info(request, 'Form is not valid')
            else:
                print("POST response is not 200 - error:", converted_response)
                messages.info(
                    request, 'POST response is not 200 - error:', converted_response)
                # add some kind of communicate for wrong city
                # return HttpResponse("City not found")
        except:
            print("Problem with connecting to station")
            messages.info(request, 'Problem with connecting to station')
            pass

    form = CustomStationForm()

    stations = Custom_station.objects.all()

    weather_data_custom = []

    for station in stations:

        print('I am user with id', request.user.id,
              'requesting data from station with user id of', station.user.id)

        # # restrict view of cities not added by specific user
        if request.user.id is station.user.id:
            try:
                r = requests.get(url_for_data.format(
                    station.station_ip, station.station_port)).json()
            except:  # if station is not sending data
                print('Request failed')
                messages.info(
                    request, 'Problem with accessing custom station data, please check if it is working or specified ip is correct')

                pollution_custom_station_data = {
                    'id': station.id,
                    'city_name': 'Error',
                    'station_ip': station.station_ip,
                    'station_port': station.station_port,
                    'temperature': 0,
                    'humidity': 0,
                    'pm2_5': 0,
                    'pm10': 0,

                    'description': 'Error getting data',
                    'color': '#ffffff',
                }
                print(pollution_custom_station_data)
                weather_data_custom.append(pollution_custom_station_data)

                break

            print('requested url: ', url_for_data.format(
                station.station_ip, station.station_port))
            # with open('recent_response_station.json', 'w') as outfile:
            #     json.dump(r, outfile)

            pollution_custom_station_data = {
                'id': station.id,
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
