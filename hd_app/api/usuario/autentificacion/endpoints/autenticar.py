import logging

from flask import request
from flask_restplus import Resource, reqparse, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from hd_app.api.usuario.serializadores import usuario
from hd_app.api.usuario.autentificacion.serializadores import login, access_token
from hd_app.api.restplus import api

from hd_app.data_auth.models import UserModel

from datetime import timedelta

log = logging.getLogger(__name__)
ns = api.namespace('sesion', description='Servicios para manejar la sesión del usuario')


@ns.route('/autenticar')
class UserLogin(Resource):

    @api.marshal_with(access_token)
    @api.doc(security=None)
    @api.expect(login)
    def post(self):
        data = request.json
        current_user = UserModel.find_by_login(data.get('login'))
        if not current_user:
            abort(401, 'El usuario con login {} no existe'.format(data.get('login')))

        if UserModel.verify_hash(data.get('password'), current_user.password):
            if not current_user.activated:
                abort(401, 'El usuario no está activado')
            expires = timedelta(days=1)
            created_access_token = create_access_token(identity=current_user, expires_delta=expires)

            return {
                'id_token': created_access_token
            }, 201
        else:
            abort(401, 'Credenciales incorrectas')


@ns.route('/cuenta')
class Account(Resource):

    @api.marshal_with(usuario)
    @jwt_required
    def get(self):
        user_login = get_jwt_identity()
        current_user = UserModel.find_by_login(user_login)
        if not current_user:
            abort(401, 'El usuario con login {} no existe'.format(user_login))
        else:
            return current_user.to_json()

    @jwt_required
    def put(self):
        data = request.json
        user_to_edit = UserModel.find_by_login(data.get('login'))
        if not user_to_edit:
            abort(401, 'El usuario con login {} no existe'.format(data.get('login')))
        else:
            user_to_edit.firstName = data.get('firstName')
            user_to_edit.lastName = data.get('lastName')
            try:
                user_to_edit.save_to_db()

                return {'message', 'El usuario {} fue editado correctamente'.format(user_to_edit.login)}
            except:
                abort(500, 'Error del servidor al editar el usuario con login {}'.format(data.get('login')))


change_pss_parser = reqparse.RequestParser(bundle_errors=True)
change_pss_parser.add_argument('old_password', required=True, type=str, location='args')
change_pss_parser.add_argument('new_password', required=True, type=str, location='args')


@ns.route('/password')
class CambiarPassword(Resource):

    @api.expect(change_pss_parser)
    @jwt_required
    def put(self):
        user_login = get_jwt_identity()
        current_user = UserModel.find_by_login(user_login)
        if not current_user:
            abort(401, 'El usuario con login {} no existe'.format(user_login))

        data = change_pss_parser.parse_args()

        if not UserModel.verify_hash(data['old_password'], current_user.password):
            abort(401, 'El password anterior no coincide')

        current_user.password = UserModel.generate_hash(data['new_password'])

        current_user.save_to_db()

        return {'message': 'El password se ha cambiado correctamente'}
