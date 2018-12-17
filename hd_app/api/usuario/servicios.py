from typing import List

from hd_app.data_auth.models import UserModel, AuthorityModel
from settings import ROOT_OBJECT


def crear_usuario(login: str, password: str, first_name: str, last_name: str, email: str,
                  authorities: List[str]) -> UserModel:

    user = UserModel(
        login=login,
        password=UserModel.generate_hash(password),
        firstName=first_name,
        lastName=last_name,
        email=email,
        activated=False
    )

    for authority_str in authorities:
        authority = AuthorityModel.find_by_authority_name(authority_str)
        if authority is not None:
            user.authorities.append(authority)

    user.save_to_db()

    return user


def obtener_usuarios_todos_root() -> List[UserModel]:
    usuarios = UserModel.return_all()
    return usuarios


def obtener_usuarios_todos() -> List[UserModel]:
    usuarios = UserModel.return_all()
    usuarios_return = []
    for usuario in usuarios:
        if usuario.get('login') != ROOT_OBJECT.get('login'):
            usuarios_return.append(usuario)
    return usuarios_return


def editar_usuario(id: int, first_name: str, last_name: str, authorities: List[str]) -> UserModel:
    user = UserModel.find_by_id(id)

    requested_authorities = []

    for authority_str in authorities:
        authority = AuthorityModel.find_by_authority_name(authority_str)
        if authority is not None:
            requested_authorities.append(authority)

    user.firstName = first_name
    user.lastName = last_name

    # se quitan las categorias que el usuario pueda tener y que no vengan en las categorias solicitadas
    for authority in user.authorities:
        if authority not in requested_authorities:
            user.authorities.remove(authority)

    # se agregan las categorias nuevas que no tenga ya el usuario pero que vengan en la solicitud
    for authority in requested_authorities:
        if authority not in user.authorities:
            user.authorities.append(authority)

    user.save_to_db()

    return user


def borrar_usuario(id: int):
    user = UserModel.find_by_id(id)
    if user.login == ROOT_OBJECT.get('login'):
        raise Exception('error - usuario root')
    user.delete_me()
