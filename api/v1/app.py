#!/usr/bin/python3
"""script that starts a flask application"""

import sys
from api.v1.views import app_views
from flask import Flask
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


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
