import logging.config

import os
from flask import Flask, Blueprint, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import settings

from hd_app.api.restplus import api
from hd_app.data_auth import db
from hd_app.data_auth.models import RevokedTokenModel
from hd_app.database import global_init as start_mongo

# rutas de los endpoints
from hd_app.api.usuario.autentificacion.endpoints.autenticar import ns as sesion_namespace
from hd_app.api.usuario.endpoints.usuario import ns as usuarios_namespace
from hd_app.api.inmueble.endpoints.inmueble import ns as inmuebles_namespace

app = Flask(__name__, static_url_path='/hd_app/static')
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
CORS(app)

web_folder_name = settings.WEB_FOLDER_NAME


@app.route('/{}/<string:request_folder>/<string:file_name>'.format(web_folder_name))
def dispatch_file(request_folder, file_name):
    return send_from_directory('hd_app/static/{}'.format(request_folder), file_name)


@app.route('/{}/<string:login>/fotos/<string:file_name>'.format(web_folder_name))
def dispatch_profile_picture(login, file_name):
    return send_from_directory('hd_app/static/{}/fotos'.format(login), file_name)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
    flask_app.config['JWT_BLACKLIST_ENABLES'] = settings.JWT_BLACKLIST_ENABLES
    flask_app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = settings.JWT_BLACKLIST_TOKEN_CHECKS


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)

    # se agregan las clases que contienen los endpoints
    api.add_namespace(sesion_namespace)
    api.add_namespace(usuarios_namespace)
    api.add_namespace(inmuebles_namespace)

    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)

    jwt = JWTManager(flask_app)

    start_mongo()

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)

    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        authorities = [authority.authority_name for authority in user.authorities]
        return {'authorities': authorities}

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.login


initialize_app(app)
