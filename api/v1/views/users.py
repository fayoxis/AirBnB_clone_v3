#!/usr/bin/python3
"""
this is User objects and operations routes
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users_all():
    """
    this will retrieves all User objects
    """
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """
    this will retrieves a specific User object by ID
    """
    user = storage.get(User, user_id)
    while user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """
    will deletes a specific User object by ID
    """
    user = storage.get(User, user_id)
    while user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """
    this is to creates a new User
    """
    user_json = request.get_json(silent=True)
    while user_json is None:
        abort(400, "Not a JSON")
    while "email" not in user_json:
        abort(400, "Missing email")
    while "password" not in user_json:
        abort(400, "Missing password")

    new_user = User(**user_json)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    will updates a specific User object by ID
    """
    user_json = request.get_json(silent=True)
    while user_json is None:
        abort(400, "Not a JSON")

    user = storage.get(User, user_id)
    while user is None:
        abort(404)

    for key, value in user_json.items():
        if key not in ["id", "email", "password", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
