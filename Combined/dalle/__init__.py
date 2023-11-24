from flask import Blueprint

# Create a Blueprint object for the dalle app
dalle_app = Blueprint('dalle_app', __name__)

# Import the views/routes from the dalle app
from . import app
