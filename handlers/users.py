from uuid import uuid4

from flask_restful import Resource
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError, NoResultFound
from werkzeug.exceptions import BadRequest

from models.session import Session
from models.user import User
from modules.json_validator import validate_json
from request_schema.user import user_data, auth


class UsersResource(Resource):
    @staticmethod
    @validate_json(user_data)
    def post(payload, token):
        from main_requests import session

        user = User(**payload, token=uuid4())
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise BadRequest('Credentials taken')

        return {"token": user.token}

    @staticmethod
    def get():
        from main_requests import session

        users = [user.as_dict() for user in session.query(User).all()]

        return {"users": users}

    @staticmethod
    @validate_json(user_data)
    def patch(payload, token):
        from main_requests import session

        data = payload["data"]  # все, что нужно изменить

        user = session.query(User).get(payload['id'])

        if user is None:
            raise BadRequest('User not found')

        if data.get('email') is not None:  # email уникальный, поэтому на уже зарегистрированный изменить нельзя
            if session.query(User).filter_by(email=data["email"]):
                raise BadRequest("Email taken")

        session.query(User).filter_by(id=user.id).update(data)
        session.commit()

        return 201


class UserAuthResource(Resource):
    @staticmethod
    @validate_json(auth)
    def post(payload, token):
        from main_requests import session

        try:
            user = session.query(User).filter(
                or_(User.email == payload["login"], User.phone == payload["login"],
                    User.login == payload["login"])).one()

        except NoResultFound:
            raise BadRequest('No user found')

        if payload["action"] == "login":
            if payload["hashed_password"] == user.hashed_password:
                auth = Session(user_id=user.id)
                session.add(auth)
                session.commit()

                user.session = user.session + [auth.id] if user.session else [auth.id]
                session.commit()

                return {"token": user.token}

            raise BadRequest('Wrong password')

        elif payload["action"] == "exit":
            auth_session = session.query(Session).get(payload["id"])
            if auth_session.id:
                if auth_session.user_id == user.id:
                    session.query(Session).filter_by(id=payload["id"]).delete()
                    session.commit()

            raise BadRequest()
        raise BadRequest()

    @staticmethod
    def get():
        from main_requests import session

        sessions = [{"id": i.id, "user_id": i.user_id} for i in
                    session.query(Session).all()]

        return {"sessions": sessions}
