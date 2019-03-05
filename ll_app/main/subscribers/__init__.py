from flask import Blueprint

subs = Blueprint('subs', __name__)

from main.subscribers import routes