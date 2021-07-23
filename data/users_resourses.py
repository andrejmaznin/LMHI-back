from data import db_session
from data.users import User
from flask import jsonify, request
from flask_restful import Resource


class UsersResource(Resource):
    @staticmethod
    def post():
        payload = request.json
        session = db_session.create_session()
        if not session.query(User).filter(User.email == payload['email']).all():
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
        users = [i.__dict__ for i in users]
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