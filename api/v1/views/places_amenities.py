#!/usr/bin/python3
""" a new view for the link between Place objects and Amenity objects"""
from models.place import Place
from models.amenity import Amenity
from os import getenv
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_places_amenities(place_id):
    """retrieve an object into a valid JSON"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        data = [amenity.to_dict() for amenity in place.amenities]
    else:
        data = [storage.get(Amenity, id).to_dict() for id in place.amenity_ids]
    return jsonify(data)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity_place(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_places_amenities(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity not in place.amenities:
            abort(404)
        index = place.amenity_ids.index(amenity_id)
        place.amenity_ids.pop(index)

    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)
