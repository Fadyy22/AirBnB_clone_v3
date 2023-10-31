#!/usr/bin/python3
"""Create a new view for Place objects """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.get("/cities/<city_id>/places", strict_slashes=False)
def get_places_in_city(city_id):
    """get a list of all places in a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.get("places/<place_id>", strict_slashes=False)
def get_place(place_id):
    """get place"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.delete("/places/<place_id>", strict_slashes=False)
def delete_place(place_id):
    """delete place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.post("/cities/<city_id>/places", strict_slashes=False)
def create_place(city_id):
    """create a new place in a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()

    if not data:
        abort(400, "Not a JSON")

    if "user_id" not in data:
        abort(400, "Missing user_id")

    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)

    if "name" not in data:
        abort(400, "Missing name")

    data["city_id"] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.put("/places/<place_id>", strict_slashes=False)
def update_place(place_id):
    """update existing place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    data.pop("id", None)
    data.pop("user_id", None)
    data.pop("city_id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    for key, value in data.items():
        setattr(place, key, value)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
