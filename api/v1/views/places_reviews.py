#!/usr/bin/python3
"""
Handler for Review objects and operations routes
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def get_reviews_by_place(place_id):
    """
    Retrieves the list of all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    return jsonify([review.to_dict() for review in reviews])


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a specific Review object by ID
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a specific Review object by ID
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, "Not a JSON")
    if "user_id" not in review_json:
        abort(400, "Missing user_id")
    if "text" not in review_json:
        abort(400, "Missing text")

    user_id = review_json["user_id"]
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    review_json["place_id"] = place_id
    new_review = Review(**review_json)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """
    Updates a specific Review object by ID
    """
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, "Not a JSON")

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    for key, value in review_json.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
