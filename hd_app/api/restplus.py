import logging
import traceback

from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound

import settings

log = logging.getLogger(__name__)

authorizations = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(version='1.0', title='Heritage Development API',
          description='API de la aplicación Heritage Development creado por Digiall.mx',
          authorizations=authorizations,
          security='apiKey')


@api.errorhandler
def default_error_handler(e):
    message = 'Ha ocurrido una excepción sin manejar'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'No se pudo encontrar la base de datos'}, 404

