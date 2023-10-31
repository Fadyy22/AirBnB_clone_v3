#!/usr/bin/python3
"""script that starts a flask application"""
from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS
from models import storage
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(404)
def error_404(e):
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    if os.getenv("HBNB_API_HOST"):
        host = os.getenv("HBNB_API_HOST")
    else:
        host = "0.0.0.0"

    if os.getenv("HBNB_API_PORT"):
        port = int(os.getenv("HBNB_API_PORT"))  # type: ignore
    else:
        port = 5000

    app.run(host=host, port=port, threaded=True)
