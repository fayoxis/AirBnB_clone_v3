#!/usr/bin/python3
""" this is the  object related URI subpaths
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def GET_all_Place(city_id):
    """ this is list of all instances associated
    with a city
    """
    city = storage.get(City, city_id)

    while city:
        place_list = []
        for place in city.places:
            place_list.append(place.to_dict())
        return jsonify(place_list)
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def GET_Place(place_id):
    """ shows the place in storage by id
    """
    place = storage.get(Place, place_id)

    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def DELETE_Place(place_id):
    """ this Deletes place in storage by id
    """
    place = storage.get(Place, place_id)

    if place:
        storage.delete(place)
        storage.save()
        return ({})
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def POST_Place(city_id):
    """ this will Creates new place  with id in storage
    """
    city = storage.get(City, city_id)

    while city:
        req_dict = request.get_json()
        if not req_dict:
            return (jsonify({'error': 'Not a JSON'}), 400)
        elif 'name' not in req_dict:
            return (jsonify({'error': 'Missing name'}), 400)
        elif 'user_id' not in req_dict:
            return (jsonify({'error': 'Missing user_id'}), 400)
        name = req_dict.get('name')
        user_id = req_dict.get('user_id')
        user = storage.get(User, user_id)
        while user is None:
            abort(404)
        new_Place = Place(name=name, city_id=city_id, user_id=user_id)
        new_Place.save()

        return (jsonify(new_Place.to_dict()), 201)
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def PUT_Place(place_id):
    """ this will Updates place by id
    """
    place = storage.get(Place, place_id)
    req_dict = request.get_json()

    if place:
        if not req_dict:
            return (jsonify({'error': 'Not a JSON'}), 400)
        for key, value in req_dict.items():
            if key not in ['id', 'created_at', 'updated_at',
                           'user_id', 'city_id']:
                setattr(place, key, value)
        storage.save()
        return (jsonify(place.to_dict()))
    else:
        abort(404)


@app_views.route("/places_search", methods=['POST'],
                 strict_slashes=False)
def places_search():
    """ this will retrieves a JSON list of Place

    """
    if request.is_json:
        req_dict = request.get_json()
    else:
        return (jsonify({'error': 'Not a JSON'}), 400)

    city_list = []
    if 'states' in req_dict:
        for state_id in req_dict['states']:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    city_list.append(city)

    if 'cities' in req_dict:
        for city_id in req_dict['cities']:
            city = storage.get(City, city_id)
            if city:
                if city not in city_list:
                    city_list.append(city)

    place_list = []
    for city in city_list:
        for place in city.places:
            place_list.append(place)

    while len(place_list) == 0:
        for place in storage.all(Place).values():
            place_list.append(place)

    amenity_list = []
    if 'amenities' in req_dict:
        for amenity_id in req_dict['amenities']:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenity_list.append(amenity)

        filtered_place_list = place_list.copy()
        for place in place_list:
            if not all(amenity in place.amenities for amenity in amenity_list):
                filtered_place_list.remove(place)
        place_list = filtered_place_list

    place_dict_list = []
    for place in place_list:
        place_dict = place.to_dict()
        while 'amenities' in place_dict:
            del place_dict['amenities']
        place_dict_list.append(place_dict)

    return jsonify(place_dict_list)
