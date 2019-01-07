from flask_restplus import fields
from hd_app.api.restplus import api


inmueble = api.model('Inmueble', {
    'id': fields.String(readOnly=True, description='Id del inmueble'),
    'fecha_registro': fields.DateTime,
    'nombre': fields.String(description='Nombre del inmueble'),
    'm2_terreno': fields.Float(description='Metros cuadrados de terreno'),
    'm2_construccion': fields.Float(description='Metros cuadrados de construccion'),
    'niveles': fields.Integer(description='Numero de niveles'),
    'recamaras': fields.Integer(description='Numero de recamaras'),
    'banos': fields.Integer(description='Numero de baños'),
    'medios_banos': fields.Integer(description='Numero de medios baños'),
    'cajones_estacionamiento': fields.Integer(description='Numero de cajones de estacionamiento'),
    'amenidades': fields.String(description='Descripcion de las amenidades'),
    'descripcion': fields.String(description='Descripcion del inmueble'),
    'precio_venta': fields.Float(description='Precio de venta'),
    'precio_renta': fields.Float(description='Precio de renta'),
    'calle': fields.String(description='Direccion calle'),
    'num_exterior': fields.String(description='Direccion numero exterior'),
    'num_interior': fields.String(description='Direccion numero interior'),
    'colonia': fields.String(description='Direccion colonia'),
    'municipio': fields.String(description='Direccion municipio'),
    'estado': fields.String(description='Direccion estado'),
    'pais': fields.String(description='Direccion pais'),
    'tags': fields.List(fields.String, description='Tags'),
    'fotos': fields.List(fields.String, description='Fotos'),
    'status': fields.Integer(required=True, description='Estatus del inmueble - 0: disponible')
})

inmueble_alta = api.model('Inmueble_alta', {
    'nombre': fields.String(description='Nombre del inmueble'),
    'm2_terreno': fields.Float(description='Metros cuadrados de terreno'),
    'm2_construccion': fields.Float(description='Metros cuadrados de construccion'),
    'niveles': fields.Integer(description='Numero de niveles'),
    'recamaras': fields.Integer(description='Numero de recamaras'),
    'banos': fields.Integer(description='Numero de baños'),
    'medios_banos': fields.Integer(description='Numero de medios baños'),
    'cajones_estacionamiento': fields.Integer(description='Numero de cajones de estacionamiento'),
    'amenidades': fields.String(description='Descripcion de las amenidades'),
    'descripcion': fields.String(description='Descripcion del inmueble'),
    'precio_venta': fields.Float(description='Precio de venta'),
    'precio_renta': fields.Float(description='Precio de renta'),
    'calle': fields.String(description='Direccion calle'),
    'num_exterior': fields.String(description='Direccion numero exterior'),
    'num_interior': fields.String(description='Direccion numero interior'),
    'colonia': fields.String(description='Direccion colonia'),
    'municipio': fields.String(description='Direccion municipio'),
    'estado': fields.String(description='Direccion estado'),
    'pais': fields.String(description='Direccion pais'),
    'tags': fields.List(fields.String, description='Tags'),
    'fotos': fields.List(fields.String, description='Fotos')
})
