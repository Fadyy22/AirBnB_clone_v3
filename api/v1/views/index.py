#!/usr/bin/python3
"""script that contains route /status"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})
