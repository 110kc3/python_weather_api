## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [License](#license)

## General info
This repo is management part of Weather station management system - executive part is on https://github.com/110kc3/pi_data_taker 

but it can also be used as standalone system with usage only of publicly available stations on https://airly.org/map/

The application was set-up on kchoinski.com page, hovewer it is disabled now. Feel free to set up it on your own with the usage of this repo.

App uses simple reqistration and login panel, hovewer it needs API key in order to use public stations https://developer.airly.org/en/register

### Main panel view
Stations can be added by specifing the city of weather sensor or exact coordinates.
![image](https://user-images.githubusercontent.com/35073233/158072533-a7071998-bca1-4efb-8e47-c35a6d8f22a1.png)

	
## Technologies
Project is created with:
* Django version: 3.1.3
* bulma version: 0.9.1
* PyMySQL library version: 0.10.1
* requests library version: 2.23.0
* geopy library version: 2.0.0
* nominatim library version: 0.1

## Setup
To run this project, install it locally using pip on virtual environment:

```
$ python -m pip install --upgrade pip
$ pip install virtualenv
$ virtualenv env
$ env\scripts\activate
$ pip install -r requirements.txt
$ python manage.py runserver
```






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
