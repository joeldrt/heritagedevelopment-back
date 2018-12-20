import logging

from flask import request
from flask_restplus import Resource, reqparse, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from hd_app.api.restplus import api
from hd_app.data_auth.models import UserModel

log = logging.getLogger(__name__)
ns = api.namespace('authorities', description='Servicio para obtener las autoridades que se pueden asignar')


@ns.route('/')
class Authorities(Resource):

    @jwt_required
    def get(self):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        authorities = [
            authority.authority_name for authority in current_user.authorities
        ]
        return authorities
