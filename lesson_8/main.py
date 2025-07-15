import json

import requests
from decouple import config
from geopy import distance
import folium


MAP_KEY = config('MAP_TOKEN')


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def convert_str_in_num(coordinates_const):
    coordinates = []
    for i in coordinates_const:
        coordinates.append(float(i)) # Меняем местами широту и долготу это нужно для правильно работы geopy
    coordinates = tuple(reversed(coordinates))
    return coordinates


def coffe_generator(cs_raw_list):
    coffee_shops = []
    location = input('Где вы находитесь? ')
    coordinates_location = convert_str_in_num(fetch_coordinates(MAP_KEY, location))
    for iteration in cs_raw_list:
        coordinates_coffee_shops = (float(iteration["Latitude_WGS84"]), float(iteration["Longitude_WGS84"]))
        coffee_location = {
            'title': iteration["Name"],
            'distance': distance.distance(coordinates_location, coordinates_coffee_shops).km,
            'latitude': float(iteration["Latitude_WGS84"]),
            'longitude': float(iteration["Longitude_WGS84"])
        }
        coffee_shops.append(coffee_location)
    return coffee_shops, coordinates_location


def get_distance(coffee_shops):
    return coffee_shops['distance']


def main():
    with open('coffee.json', 'r') as coffe_file:
        coffe_address = coffe_file.read()

    coffe_address = json.loads(coffe_address)
    coffe_list, user_location = coffe_generator(coffe_address)
    sorted_shops = sorted(coffe_list, key=get_distance)
    nearest = sorted_shops[:5]

    map = folium.Map(location=(user_location[0], user_location[1]))

    folium.Marker(
        location=[user_location[0], user_location[1]],
        tooltip="Вы находитесь здесь",
        popup="Путь в тысячу ли начинается с первого шага",
        icon=folium.Icon(color="red"),
    ).add_to(map)

    folium.Marker(
        location=[nearest[0]['latitude'], nearest[0]['longitude']],
        tooltip=f"{nearest[0]['title']}",
        popup=f"Заведение: {nearest[0]['title']}, расстояние до него: {nearest[0]['distance']:.2f} км",
        icon=folium.Icon(color="green"),
    ).add_to(map)

    folium.Marker(
        location=[nearest[1]['latitude'], nearest[1]['longitude']],
        tooltip=f"{nearest[1]['title']}",
        popup=f"Заведение: {nearest[1]['title']}, расстояние до него: {nearest[1]['distance']:.2f} км",
        icon=folium.Icon(color="green"),
    ).add_to(map)

    folium.Marker(
        location=[nearest[2]['latitude'], nearest[2]['longitude']],
        tooltip=f"{nearest[2]['title']}",
        popup=f"Заведение: {nearest[2]['title']}, расстояние до него: {nearest[2]['distance']:.2f} км",
        icon=folium.Icon(color="green"),
    ).add_to(map)

    folium.Marker(
        location=[nearest[3]['latitude'], nearest[3]['longitude']],
        tooltip=f"{nearest[3]['title']}",
        popup=f"Заведение: {nearest[3]['title']}, расстояние до него: {nearest[3]['distance']:.2f} км",
        icon=folium.Icon(color="green"),
    ).add_to(map)

    folium.Marker(
        location=[nearest[4]['latitude'], nearest[4]['longitude']],
        tooltip=f"{nearest[4]['title']}",
        popup=f"Заведение: {nearest[4]['title']}, расстояние до него: {nearest[4]['distance']:.2f} км",
        icon=folium.Icon(color="green"),
    ).add_to(map)
    map.save("index.html")


if __name__ == '__main__':
    main()