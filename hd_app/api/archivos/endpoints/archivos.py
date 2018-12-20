import logging
import os
import base64

from flask import request
from flask_restplus import Resource, abort
from flask_jwt_extended import (jwt_required)
from hd_app.api.archivos.serializadores import envio_archivos
from hd_app.api.inmueble.servicios import obtener_inmueble_por_id
from hd_app.api.restplus import api
from settings import WEB_FOLDER_NAME

log = logging.getLogger(__name__)

ns = api.namespace('archivos', description='Servicios para manejar archivos')


@ns.route('/')
class Archivos(Resource):

    @api.expect(envio_archivos)
    @jwt_required
    def post(self):
        data = request.json

        folder = data.get('folder').replace(" ", "_")
        files = list(data.get('files'))

        inmueble = obtener_inmueble_por_id(inmueble_id=folder)

        if not inmueble:
            abort('400', 'No se encontró el inmueble con id: {}'.format(folder))

        if len(files) <= 0:
            abort('400', 'La petición no contiene archivos a guardar')

        added_files = []

        for current_file in files:
            os.makedirs('hd_app/static/{}'.format(folder), exist_ok=True)

            base64_data = str(current_file['value'])

            filename = current_file['filename'].replace(" ", "_")

            saving_file = open('hd_app/static/{}/{}'.format(folder, filename), 'wb')
            saving_file.write(base64.decodebytes(base64_data.encode()))
            saving_file.close()

            saved_file_name = '{}/{}/{}'.format(WEB_FOLDER_NAME, folder, filename)

            added_files.append(saved_file_name)
            inmueble.fotos.append(saved_file_name)

        inmueble.save()

        return added_files
