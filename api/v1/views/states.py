#!/usr/bin/python3
"""
Route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    Retrieves all State objects
    """
    state_list = []
    state_objects = storage.all(State).values()
    for obj in state_objects:
        state_list.append(obj.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    Gets a specific State object by ID
    """
    fetched_object = storage.get(State, state_id)
    if fetched_object is None:
        abort(404)
    return jsonify(fetched_object.to_dict())


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    Create state route
    Returns newly created state object
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, description="Not a JSON")
    if "name" not in state_json:
        abort(400, description="Missing name")

    new_state = State(**state_json)
    new_state.save()
    response = jsonify(new_state.to_dict())
    response.status_code = 201
    return response


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def state_update_by_id(state_id):
    """
    Updates a specific State object by ID
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, description="Not a JSON")
    fetched_object = storage.get(State, state_id)
    if fetched_object is None:
        abort(404)
    for key, value in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_object, key, value)
    fetched_object.save()
    return jsonify(fetched_object.to_dict())


@app_views.route("/states/<state_id>",
                 methods=["DELETE"], strict_slashes=False)
def state_delete_by_id(state_id):
    """
    Deletes a State by ID
    """
    fetched_object = storage.get(State, state_id)
    if fetched_object is None:
        abort(404)
    storage.delete(fetched_object)
    storage.save()
    return jsonify({})
