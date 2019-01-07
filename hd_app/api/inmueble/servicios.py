from typing import List
from datetime import datetime, timedelta
from mongoengine import Q
import json

from hd_app.database.inmueble import Inmueble


def crear_inmueble(nombre: str, m2_terreno: float, m2_construccion: float, niveles: int, recamaras: int, banos: int,
                   medios_banos: int, cajones_estacionamiento: int, amenidades: str, descripccion: str,
                   precio_venta: float, precio_renta: float, calle: str, num_exterior: str, num_interior: str,
                   colonia: str, municipio: str, estado: str, pais: str, tags: [str], fotos: [str]) -> Inmueble:
    inmueble = Inmueble()
    inmueble.nombre = nombre
    inmueble.m2_terreno = m2_terreno
    inmueble.m2_construccion = m2_construccion
    inmueble.niveles = niveles
    inmueble.recamaras = recamaras
    inmueble.banos = banos
    inmueble.medios_banos = medios_banos
    inmueble.cajones_estacionamiento = cajones_estacionamiento
    inmueble.amenidades = amenidades
    inmueble.descripcion = descripccion
    inmueble.precio_venta = precio_venta
    inmueble.precio_renta = precio_renta
    inmueble.calle = calle
    inmueble.num_exterior = num_exterior
    inmueble.num_interior = num_interior
    inmueble.colonia = colonia
    inmueble.municipio = municipio
    inmueble.estado = estado
    inmueble.pais = pais
    inmueble.tags = tags
    inmueble.fotos = fotos

    inmueble.save()

    return inmueble


def editar_inmueble(inmueble_id: str, nombre: str, m2_terreno: float, m2_construccion: float, niveles: int, recamaras: int,
                    banos: int, medios_banos: int, cajones_estacionamiento: int, amenidades: str, descripccion: str,
                    precio_venta: float, precio_renta: float, calle: str, num_exterior: str, num_interior: str,
                    colonia: str, municipio: str, estado: str, pais: str, tags: [str], fotos: [str]) -> Inmueble:
    inmueble = Inmueble.objects().get(id=inmueble_id)
    inmueble.nombre = nombre
    inmueble.m2_terreno = m2_terreno
    inmueble.m2_construccion = m2_construccion
    inmueble.niveles = niveles
    inmueble.recamaras = recamaras
    inmueble.banos = banos
    inmueble.medios_banos = medios_banos
    inmueble.cajones_estacionamiento = cajones_estacionamiento
    inmueble.amenidades = amenidades
    inmueble.descripcion = descripccion
    inmueble.precio_venta = precio_venta
    inmueble.precio_renta = precio_renta
    inmueble.calle = calle
    inmueble.num_exterior = num_exterior
    inmueble.num_interior = num_interior
    inmueble.colonia = colonia
    inmueble.municipio = municipio
    inmueble.estado = estado
    inmueble.pais = pais
    inmueble.tags = tags
    inmueble.fotos = fotos

    inmueble.save()

    return inmueble


def borrar_inmueble(inmueble_id: str) -> bool:
    inmueble = Inmueble.objects().get(id=inmueble_id)
    if not inmueble:
        raise Exception('No se encotró el inmueble con id: {}'.format(inmueble_id))
    inmueble.delete()
    return True


def obtener_inmuebles() -> List[Inmueble]:
    inmuebles = Inmueble.objects().all()
    return inmuebles


def obtener_inmueble_por_id(inmueble_id: str) -> Inmueble:
    inmueble = Inmueble.objects().get(id=inmueble_id)
    return inmueble
