#!/usr/bin/python3
"""create a new view for City objects"""
from models.city import City
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all city objects: GET /api/v1/states"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def r_city_id(city_id):
    """GETting city  object ID"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """Deleting"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city():
    """Creating a State object using city"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    city = City(**data)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
     city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    for key, value in data.items():
        setattr(city, key, value)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
