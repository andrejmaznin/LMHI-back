from . import db_session
from data.auth_sessions import Session
from data.users import User
from flask import jsonify, request
from flask_restful import Resource


class UsersResource(Resource):
    @staticmethod
    def post():
        payload = request.get_json(force=True)

        session = db_session.create_session()
        if not session.query(User).filter(User.email == payload["email"]).all():
            user = User(
                name=payload['name'],
                hashed_password=payload["hashed_password"],
                email=payload['email'],
                info=payload['info']
            )
            session.add(user)
            user_id = session.query(User).filter_by(
                email=payload["email"]).one().id  # получаем id созданного пользователя, чтобы сообщить его в ответе
            session.commit()
            response = jsonify({'success': 'OK', "id": user_id})
            response.status_code = 201
            return response
        else:
            response = jsonify({'ERROR': 'USER ALREADY EXISTS'})
            response.status_code = 400
            return response

    @staticmethod
    def get():
        session = db_session.create_session()

        users = session.query(User).all()
        users = [{"email": i.email, "hashed_password": i.hashed_password, "name": i.name, "info": i.info} for i in
                 users]
        response = jsonify({"users": users, 'success': 'OK'})
        response.status_code = 201
        return response

    @staticmethod
    def patch():
        payload = request.json
        session = db_session.create_session()

        data = payload["data"]  # все, что нужно изменить
        user_id = payload["id"]
        current_user = session.query(User).get(user_id)

        if current_user:
            if "email" in data.keys():  # email уникальный, поэтому на уже зарегистрированный изменить нельзя
                if session.query(User).filter_by(email=data["email"]):
                    response = jsonify({'ERROR': 'EMAIL TAKEN'})
                    response.status_code = 400
                    return response

            session.query(User).filter_by(id=user_id).update(data)
            session.commit()
        else:
            response = jsonify({'ERROR': 'USER NOT FOUND'})
            response.status_code = 404
            return response


class UserAuthResource(Resource):
    @staticmethod
    def post():
        payload = request.get_json(force=True)

        session = db_session.create_session()
        user = session.query(User).filter_by(email=payload["email"]).all()

        if not user:
            response = jsonify({'ERROR': 'NO USER'})
            response.status_code = 400
            return response

        user = user[0]

        if payload["action"] == "login":
            try:
                session.query(Session).filter_by(user_id=user.id).one()

            except Exception:
                if payload["email"] == user.email and payload["hashed_password"] == user.hashed_password:
                    auth = Session(
                        user_id=user.id)

                    session.add(auth)
                    session.commit()
                    session_id = session.query(Session).filter_by(user_id=user.id).one().id

                    response = jsonify({"session_id": session_id, 'success': 'OK'})
                    response.status_code = 201
                    return response

                response = jsonify({'ERROR': 'WRONG USERNAME OR PASSWORD'})
                response.status_code = 400
                return response

            response = jsonify({'ERROR': 'SESSION ALREADY EXISTS'})
            response.status_code = 400
            return response

        elif payload["action"] == "exit":
            auth_session = session.query(Session).get(payload["id"])
            if auth_session.id:
                if auth_session.user_id == user.id:
                    session.query(Session).filter_by(id=payload["id"]).delete()
                    session.commit()

                    response = jsonify({'success': 'OK'})
                    response.status_code = 201
                    return response

                response = jsonify({'ERROR': 'WRONG USER ID'})
                response.status_code = 400
                return response

            response = jsonify({'ERROR': 'WRONG SESSION ID'})
            response.status_code = 400
            return response

    @staticmethod
    def get():
        session = db_session.create_session()

        sessions = session.query(Session).all()
        sessions = [{"id": i.id, "user_id": i.user_id} for i in
                    sessions]
        response = jsonify({"sessions": sessions, 'success': 'OK'})
        response.status_code = 201
        return response
