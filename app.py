import os
import io
from flask import Flask, request, redirect, url_for, render_template, jsonify
from flask_caching import Cache
from flask_sslify import SSLify
from flask_cors import CORS

from werkzeug.utils import secure_filename
from requests.auth import HTTPBasicAuth
from google.oauth2 import service_account
from google.cloud import vision
from google.cloud.vision import types

from functools import wraps

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

import requests
import json
import jwt
import random
import string


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])



app = Flask(__name__)
sslify = SSLify(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


def allowed_file(filename):
    return '.' in file and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def mlvision(file, filename):
    images = {}
    vision_client = vision.ImageAnnotatorClient()


    #with io.open(filename, 'rb') as image_file:
        #content = image_file.read()
    content = file.read()

    image = types.Image(content=content)


    # Performs label detection on the image file
    response = vision_client.label_detection(image=image)
    labels = response.label_annotations
    for label in labels:
        images[label.description] = label.score


    return json.dumps(images)




@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/ml', methods=['GET', 'POST'])
def ml_file():
    if request.method == 'POST':
        #get and check file
        f = request.files.get('file')
        if not f:
            return 'No file uploaded.', 400

        #save files
        fname = secure_filename(f.filename)

        #Get dictionary
        uvision = mlvision(f, fname)


        return jsonify(uvision)
    return redirect(request.url)




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get('PORT', 443)))
