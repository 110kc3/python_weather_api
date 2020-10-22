#!/bin/bash
#Add script to file /etc/crontab as follow:#* *    * * *   root     #/root/supla-filesensors/var/script_name.sh#, then restart cron process: /etc/init.d/cron restart

#*****************************************************************************************
folder_location="" #set folder for for files with data 
weather_API="4f651df2ff6276adea68dcbe6c969c94" #max 60 calls per minute
pollution_API="aV4cM5PIhRFvnfP4tiN1Cx2TAa8s1sf0"
current_day=$(date +"%d-%m-%y")
current_time=$(date +"%H:%M")

weatherCity="Gliwice"

echo $current_day
echo $current_time


weatherData="http://api.openweathermap.org/data/2.5/weather?q="$weatherCity",pl&units=metric&appid="$weather_API
echo $weatherData
#get weather data
curl -s  $weatherData | json_pp  > weatherData_file.json



#Air pollution - PM1, PM2.5, PM10. 

#####
Gliwice_lat="50.289933901" #50.2945° N
Gliwice_lng="18.6597874761" #18.6714° E
pollutionData="https://airapi.airly.eu/v2/measurements/nearest?lat="$Gliwice_lat"&lng="$Gliwice_lng"&maxDistanceKM=10&apikey="$pollution_API



curl -s  "https://airapi.airly.eu/v2/measurements/nearest?lat="50.289933901&lng="$Gliwice_lng"&maxDistanceKM=10&apikey=aV4cM5PIhRFvnfP4tiN1Cx2TAa8s1sf0" | json_pp


#get list of stations
curl -X GET \
    --header 'Accept: application/json' \
    --header 'apikey: aV4cM5PIhRFvnfP4tiN1Cx2TAa8s1sf0' \
    'https://airapi.airly.eu/v2/installations/nearest?lat=50.062006&lng=19.940984&maxDistanceKM=5&maxResults=3' | json_pp
	
	
curl -X GET \
    --header 'Accept: application/json' \
    --header 'apikey: aV4cM5PIhRFvnfP4tiN1Cx2TAa8s1sf0' \
    'https://airapi.airly.eu/v2/measurements/nearest?lat=50.289933901&lng=18.6597874761&maxDistanceKM=5' | json_pp
	
curl -s  $pollutionData | json_pp > pollutionData_file.json


curl -s https://airapi.airly.eu/v2/measurements/nearest?lat=50.2&lng=18.2&maxDistanceKM=10&apikey=aV4cM5PIhRFvnfP4tiN1Cx2TAa8s1sf0 | json_pp