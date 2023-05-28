from flask import Flask
from flask_cors import CORS, cross_origin
import os, sys

app = Flask(__name__)

app.config['FLASKS3_BUCKET_NAME'] = 'sneakrcred'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin: *'

from api import routes