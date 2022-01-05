from flask import jsonify
from flask_restful import Resource
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError, NoResultFound
from werkzeug.exceptions import BadRequest

from data.models.auth_sessions import Session
from data.models.users import User
from data.modules.json_validator import validate_json
from data.service import db_session


class UsersResource(Resource):
    @staticmethod
    @validate_json('user/post.json', by_path=True)
    def post(payload):
        session = db_session.create_session()

        try:
            user = User(**payload)
            session.add(user)
            session.commit()

        except IntegrityError:
            raise BadRequest()

        response = jsonify(
            {
                'success': 'OK',
                "id": user.id
            }
        )
        response.status_code = 201
        return response

    @staticmethod
    def get():
        session = db_session.create_session()

        users = [user.as_dict() for user in session.query(User).all()]

        response = jsonify({"users": users, 'success': 'OK'})
        response.status_code = 201
        return response

    @staticmethod
    @validate_json('user/patch.json', by_path=True)
    def patch(payload):
        session = db_session.create_session()

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
    @validate_json('user/auth/post.json', by_path=True)
    def post(payload):
        session = db_session.create_session()
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

                response = jsonify({"session_id": auth.id, 'success': 'OK'})
                response.status_code = 201
                return response
            raise BadRequest()

        elif payload["action"] == "exit":
            auth_session = session.query(Session).get(payload["id"])
            if auth_session.id:
                if auth_session.user_id == user.id:
                    session.query(Session).filter_by(id=payload["id"]).delete()
                    session.commit()

                    response = jsonify({'success': 'OK'})
                    response.status_code = 201
                    return response

            raise BadRequest()
        raise BadRequest()

    @staticmethod
    def get():
        session = db_session.create_session()

        sessions = [{"id": i.id, "user_id": i.user_id} for i in
                    session.query(Session).all()]

        response = jsonify({"sessions": sessions, 'success': 'OK'})
        response.status_code = 201
        return response
