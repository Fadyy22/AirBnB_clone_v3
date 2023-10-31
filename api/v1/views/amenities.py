#!/usr/bin/python3
"""Create a new view for Amenity objects """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.get('/amenities', strict_slashes=False)
def get_amenities():
    """Retrieves the list of all amenity objects: GET /api/v1/states"""
    amenities = storage.all(Amenity)
    if not amenities:
        abort(404)
    return jsonify([obj.to_dict() for obj in amenities.values()])


@app_views.get('/amenities/<amenity_id>', strict_slashes=False)
def amenityid(amenity_id):
    """GETting Amenity  object ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.delete('/amenities/<amenity_id>', strict_slashes=False)
def del_amenity(amenity_id):
    """Deleting"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.post('/amenities', strict_slashes=False)
def post_amenity():
    """Creating amenity object using post"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.put('/amenities/<amenity_id>', strict_slashes=False)
def put_amenity(amenity_id):
    """put amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    for key, value in data.items():
        setattr(amenity, key, value)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
