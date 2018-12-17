from flask_restplus import fields
from hd_app.api.restplus import api


login = api.model('Login', {
    'login': fields.String(required=True, description='Nombre de usuario'),
    'password': fields.String(required=True, description='Password del usuario')
})

access_token = api.model('Access Token', {
    'id_token': fields.String(required=True, description='Token del usuario autentificado')
})
