#!/usr/bin/python3
"""
Handler for Amenity objects and operations routes
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects
    """
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves a specific Amenity object by ID
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes a specific Amenity object by ID
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    Creates a new Amenity
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, "Not a JSON")
    if "name" not in amenity_json:
        abort(400, "Missing name")

    new_amenity = Amenity(**amenity_json)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates a specific Amenity object by ID
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, "Not a JSON")

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    for key, value in amenity_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
