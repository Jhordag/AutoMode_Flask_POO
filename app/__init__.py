from flask import Flask

app = Flask(__name__)

from app import admin
from app import cliente
