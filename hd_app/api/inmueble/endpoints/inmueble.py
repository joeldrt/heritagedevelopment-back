import logging

from flask import request
from flask_restplus import Resource, reqparse, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from hd_app.api.inmueble.servicios import crear_inmueble, editar_inmueble, obtener_inmuebles, obtener_inmueble_por_id
from hd_app.api.inmueble.serializadores import inmueble
from hd_app.api.restplus import api

from hd_app.data_auth.models import UserModel
from settings import MINIMUM_USER_API_AUTHORITY, AUTHORITY_ROOT, ROOT_OBJECT

log = logging.getLogger(__name__)
ns = api.namespace('inmuebles', description='Servicios para administrar los inmuebles')


@ns.route('/')
class Inmnueble(Resource):

    @api.marshal_with(inmueble)
    @api.expect(inmueble)
    @jwt_required
    def post(self):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(MINIMUM_USER_API_AUTHORITY):
            abort(401, 'No tiene permisos para realizar esta acción')

        data = request.json

        try:
            inmueble_ret = crear_inmueble(nombre=data.get('nombre'), m2_terreno=data.get('m2_terreno'),
                                          m2_construccion=data.get('m2_construccion'), niveles=data.get('niveles'),
                                          recamaras=data.get('m2_construccion'), banos=data.get('m2_construccion'),
                                          cajones_estacionamiento=data.get('cajones_estacionamiento'),
                                          amenidades=data.get('amenidades'), descripccion=data.get('descripccion'),
                                          precio_venta=data.get('precio_venta'), precio_renta=data.get('precio_renta'),
                                          calle=data.get('calle'), num_exterior=data.get('num_exterior'),
                                          num_interior=data.get('num_interior'), colonia=data.get('colonia'),
                                          municipio=data.get('municipio'), estado=data.get('estado'),
                                          pais=data.get('pais'), tags=data.get('tags'), fotos=data.get('fotos'),
                                          status=data.get('status'))
            return inmueble_ret.to_dict()
        except Exception as exception:
            abort(500, 'Error del servidor al guardar el inmueble')

    @api.marshal_list_with(inmueble)
    @api.doc(security=None)
    def get(self):
        try:
            inmuebles_obj = obtener_inmuebles()
            inmuebles_ret = [
                inmueble.to_dict() for inmueble in inmuebles_obj
            ]
            return inmuebles_ret
        except Exception as ex:
            abort(500, 'Error del servidor al recuperar los inmuebles')


@ns.route('/<string:inmueble_id>')
class InmuebleActions(Resource):

    @api.marshal_with(inmueble)
    @api.doc(security=None)
    def get(self, inmueble_id):
        try:
            inmueble_obj = obtener_inmueble_por_id(inmueble_id=inmueble_id)
            return inmueble_obj.to_dict()
        except Exception as exc:
            abort(500, 'Error del servidor al recuperar el inmueble con el id: {}'.format(inmueble_id))

    @api.marshal_with(inmueble)
    @api.expect(inmueble)
    @jwt_required
    def put(self, inmueble_id):
        login = get_jwt_identity()
        current_user = UserModel.find_by_login(login)

        if not current_user.has_authority(MINIMUM_USER_API_AUTHORITY):
            abort(401, 'No tiene permisos para realizar esta acción')

        inmueble_obj = obtener_inmueble_por_id(inmueble_id=inmueble_id)

        if not inmueble_obj:
            abort(400, 'No existe un inmueble con ese id')

        data = request.json

        try:
            inmueble_obj = editar_inmueble(inmueble_id=data.get('id'), nombre=data.get('nombre'),
                                           m2_terreno=data.get('m2_terreno'), m2_construccion=data.get('m2_construccion'),
                                           niveles=data.get('niveles'), recamaras=data.get('m2_construccion'),
                                           banos=data.get('m2_construccion'),
                                           cajones_estacionamiento=data.get('cajones_estacionamiento'),
                                           amenidades=data.get('amenidades'), descripccion=data.get('descripccion'),
                                           precio_venta=data.get('precio_venta'), precio_renta=data.get('precio_renta'),
                                           calle=data.get('calle'), num_exterior=data.get('num_exterior'),
                                           num_interior=data.get('num_interior'), colonia=data.get('colonia'),
                                           municipio=data.get('municipio'), estado=data.get('estado'),
                                           pais=data.get('pais'), tags=data.get('tags'), fotos=data.get('fotos'),
                                           status=data.get('status'))
            return inmueble_obj.to_dict()
        except Exception as ex:
            abort(500, 'Error del servidor al editar el inmueble')
