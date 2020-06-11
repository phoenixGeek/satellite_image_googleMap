import requests
import pprint
import sys
import googlemaps
import time
import json
import os.path

API_KEY = "YOUR_API_KEY"
gmaps = googlemaps.Client(key = API_KEY)

zipcode = sys.argv[1]
radius = int(sys.argv[2]) * 1000
save_path = sys.argv[3]

geocode_result = gmaps.geocode(zipcode)
lat = geocode_result[0]["geometry"]["location"]["lat"]
lon = geocode_result[0]["geometry"]["location"]["lng"]
location = str(lat) + ',' + str(lon)

build_types = 'restaurant'


places_result  = gmaps.places_nearby(location = location, radius = radius, open_now = False, type = build_types)


time.sleep(2)


place_result  = gmaps.places_nearby(page_token = places_result['next_page_token'])

time.sleep(2)

stored_results = []


for (place, _place) in zip(places_result['results'], place_result['results']):

    my_place_id = place['place_id']

    my_fields = ['name', 'geometry', 'formatted_phone_number', 'formatted_address']

    places_details  = gmaps.place(place_id= my_place_id , fields= my_fields)

    stored_results.append(places_details['result'])


    _my_place_id = _place['place_id']

    _my_fields = ['name', 'geometry', 'formatted_phone_number', 'formatted_address']

    _places_details  = gmaps.place(place_id= _my_place_id , fields= _my_fields)

    stored_results.append(_places_details['result'])


while "next_page_token" in place_result :

    
    place_result = gmaps.places_nearby(page_token = place_result['next_page_token'])

    time.sleep(2)

    for place in place_result['results']:

        my_place_id = place['place_id']

        my_fields = ['name', 'geometry', 'formatted_phone_number', 'formatted_address']

        places_details  = gmaps.place(place_id= my_place_id , fields= my_fields)

        stored_results.append(places_details['result'])


BASE_URL = "https://maps.googleapis.com/maps/api/staticmap?"
maptype = "satellite"
ZOOM = 20

pprint.pprint(stored_results)

for building in stored_results:

    if building['name'] and building['name'] != '' and  'formatted_phone_number' in building:
        
        lat = building['geometry']['location']['lat']
        lon = building['geometry']['location']['lng']
        
        build_loc = str(lat) + ',' + str(lon)
        
        # lat_dist = building['geometry']['viewport']['northeast']['lat'] - building['geometry']['viewport']['southwest']['lat']
        # lon_dist = building['geometry']['viewport']['northeast']['lng'] - building['geometry']['viewport']['southwest']['lng']

        # lat = building['geometry']['viewport']['northeast']['lat'] - lat_dist / 2
        # lon = building['geometry']['viewport']['northeast']['lng'] - lon_dist / 2
        # build_loc = str(lat) + ',' + str(lon)

        str_build = building['name']
        if "/" in str_build:
            str_build = str_build.replace("/", '-')
        if "\\" in str_build:
            str_build = str_build.replace("\\", '-')
        if "|" in str_build:
            str_build = str_build.replace("|", '-')
    
        build_name = str_build + ".png"
        json_name = str_build + ".json"
        mailAddr = building['formatted_address']
        phone_number = building['formatted_phone_number']            
        data = {'mail address': mailAddr, 'phone number': phone_number}

        
        URL = BASE_URL + "center=" + build_loc + "&zoom=" + str(ZOOM) + "&size=1200x1200" + "&maptype=" + maptype + "&key=" + API_KEY

        response = requests.get(URL)
        pprint.pprint(response)

        if not os.path.isdir(save_path):
            os.mkdir(save_path)

        image_path = os.path.join(save_path, build_name)         

        json_path = os.path.join(save_path, json_name)


        with open(image_path, 'wb') as file:
            file.write(response.content)


        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)