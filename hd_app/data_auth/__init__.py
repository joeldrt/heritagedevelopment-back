from flask_sqlalchemy import SQLAlchemy

import settings

db = SQLAlchemy()


def reset_auth_database():
    from hd_app.data_auth.models import UserModel, AuthorityModel, RevokedTokenModel
    db.drop_all()
    db.create_all()

    if not UserModel.find_by_login('admin'):
        init_auth_database_values()


def init_auth_database_values():
    from hd_app.data_auth.models import UserModel, AuthorityModel, RevokedTokenModel

    authority0 = AuthorityModel(authority_name=settings.AUTHORITY_ROOT)
    authority0.save_to_db()
    authority1 = AuthorityModel(authority_name=settings.AUTHORITY_ADMIN)
    authority1.save_to_db()
    authority2 = AuthorityModel(authority_name=settings.AUTHORITY_USER)
    authority2.save_to_db()

    root = UserModel(
        login=settings.ROOT_OBJECT['login'],
        password=UserModel.generate_hash(settings.ROOT_OBJECT['password']),
        firstName=settings.ROOT_OBJECT['firstName'],
        email=settings.ROOT_OBJECT['email'],
        activated=True
    )

    root.authorities.append(authority0)
    root.authorities.append(authority1)
    root.authorities.append(authority2)

    root.save_to_db()

    admin = UserModel(
        login=settings.ADMIN_OBJECT['login'],
        password=UserModel.generate_hash(settings.ADMIN_OBJECT['password']),
        firstName=settings.ADMIN_OBJECT['firstName'],
        lastName=settings.ADMIN_OBJECT['lastName'],
        email=settings.ADMIN_OBJECT['email'],
        activated=True
    )

    admin.authorities.append(authority1)
    admin.authorities.append(authority2)

    admin.save_to_db()
