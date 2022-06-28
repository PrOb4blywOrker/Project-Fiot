import requests
import json
import geocoder
TOKEN = '5b3ce3597851110001cf62481d5f30742e1447b2b758a901786bdb00'


def matrix(locations: list, profile=0):
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
        'Authorization': TOKEN
    }
    profile_dict = {
        0: 'driving-car',
        1: 'foot-walking'
    }
    data = {"locations": [i[::-1] for i in locations], "metrics": ["distance", "duration"], "units": "m"}
    res = requests.post(f'https://api.openrouteservice.org/v2/matrix/{profile_dict[profile]}',
                        headers=headers,
                        json=data).json()
    return dict(durations=res['durations'][0][1], distances=res['distances'][0][1])
def my_location():
    g = geocoder.ip('me')
    return g


def search_dest_id(city):
	url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

	querystring = {"locale": "uk", "name": city}

	headers = {
		'X-RapidAPI-Key': 'b8132902a3msh80465f8f749e501p1afbb2jsn10b91ca4ab5c',
        'X-RapidAPI-Host': 'booking-com.p.rapidapi.com'
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	dest_id = json.loads(bytes.decode(response.content))[0]['dest_id']
	return dest_id
def search_hotels(dest_id, checkin_date, checkout_date, adults_number, children_number):
	url = "https://booking-com.p.rapidapi.com/v1/hotels/search"
	querystring = {"checkout_date":checkout_date,"units":"metric","dest_id":dest_id,"dest_type":"city","locale":"uk","adults_number":adults_number,"order_by":"popularity","filter_by_currency":"EUR","checkin_date":checkin_date,"room_number":"1","children_number":children_number,"page_number": 0,"categories_filter_ids":"class::2,class::4,free_cancellation::1","include_adjacency":"true"}

	headers = {
		'X-RapidAPI-Key': 'b8132902a3msh80465f8f749e501p1afbb2jsn10b91ca4ab5c',
        'X-RapidAPI-Host': 'booking-com.p.rapidapi.com'
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	d=json.loads(bytes.decode(response.content))['result']

	return d
def search_hotels_without_children(dest_id, checkin_date, checkout_date, adults_number):
	url = "https://booking-com.p.rapidapi.com/v1/hotels/search"
	querystring = {"checkout_date":checkout_date,"units":"metric","dest_id":dest_id,"dest_type":"city","locale":"uk","adults_number":adults_number,"order_by":"popularity","filter_by_currency":"EUR","checkin_date":checkin_date,"room_number":"1","page_number": 0,"categories_filter_ids":"class::2,class::4,free_cancellation::1","include_adjacency":"true"}

	headers = {
		'X-RapidAPI-Key': 'b8132902a3msh80465f8f749e501p1afbb2jsn10b91ca4ab5c',
        'X-RapidAPI-Host': 'booking-com.p.rapidapi.com'
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	d=json.loads(bytes.decode(response.content))['result']

	return d