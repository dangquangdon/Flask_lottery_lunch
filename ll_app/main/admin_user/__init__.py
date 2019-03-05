from flask import Blueprint

adm = Blueprint('adm', __name__)

from main.admin_user import routes
