#!/usr/bin/python3
"""create a new view for City objects"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.get('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all city objects: GET /api/v1/states"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.get('/cities/<city_id>', strict_slashes=False)
def cityid(city_id):
    """GETting city  object ID"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.delete('/cities/<city_id>', strict_slashes=False)
def del_city(city_id):
    """Deleting"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.post('/states/<state_id>/cities', strict_slashes=False)
def post_city(state_id):
    """Creating a State object using city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    data["state_id"] = state_id
    city = City(**data)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.put('/cities/<city_id>', strict_slashes=False)
def put_city(city_id):
    """PUT city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    data.pop("id", None)
    data.pop("state_id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    for key, value in data.items():
        setattr(city, key, value)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
