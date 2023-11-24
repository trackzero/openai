from flask import Blueprint

# Create a Blueprint object for the vision app
vision_app = Blueprint('vision_app', __name__)

# Import the views/routes from the vision app
from . import app
