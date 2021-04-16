# Python weather API

This repo is management part of Weather station management system - executive part is on https://github.com/110kc3/pi_data_taker 

but it can also be used as standalone system with usage only of publicly available stations.

The application can be found on kchoinski.com page, but feel free to set up it on your own with the usage of this repo.

## Prerequisites for local usage

1. Installing python

https://www.python.org/downloads/

1.1 Add Python to the Windows Path
https://geek-university.com/python/add-python-to-the-windows-path/

1.2 Install pip
python -m pip install --upgrade pip

2. Installing django
https://docs.djangoproject.com/en/3.1/intro/install/

pip install Django

3. Installing used python packages

https://medium.com/analytics-vidhya/how-to-generate-lat-and-long-coordinates-of-city-without-using-apis-25ebabcaf1d5

Nominatim and geopy - for geolocating user specified cities

pip install geopy 
pip install Nominatim

pip install PyMySQL==0.10.1
pip install requests

pip install django-widget-tweaks
pip install django-crispy-forms

4. Run django server locally (The development server)

cd /python_weather_api/dj_ango/pollution_master/

virtualenv env

env\scripts\activate

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py runserver


## License
Copyright 2020, Kamil Choiński, Poland 

Python weather API is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
