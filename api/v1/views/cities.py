#!/usr/bin/python3
"""
Route for handling City objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def cities_by_state(state_id):
    """
    Retrieves all City objects from a specific state
    """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    city_list = [city.to_dict() for city in state_obj.cities]
    return jsonify(city_list)


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """
    Creates a city in a specific state
    """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, description="Not a JSON")

    if "name" not in city_json:
        abort(400, description="Missing name")

    city_json["state_id"] = state_id
    new_city = City(**city_json)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def cities_by_id(city_id):
    """
    Retrieves a specific City object by ID
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    return jsonify(city_obj.to_dict())


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def city_update_by_id(city_id):
    """
    Updates a specific City object by ID
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, description="Not a JSON")

    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    for key, value in city_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city_obj, key, value)
    city_obj.save()
    return jsonify(city_obj.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def city_delete_by_id(city_id):
    """
    Deletes a City by ID
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200
