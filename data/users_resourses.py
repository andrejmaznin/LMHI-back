from flask import jsonify, request
from flask_restful import Resource, abort
import db_session
from users import User
import hashlib


class UsersResource(Resource):
    @staticmethod
    def post():
        payload = request.json()
        session = db_session.create_session()

        if not session.query(User).filter(User.email == payload['email']).all():
            user = User(
                name=payload['name'],
                hashed_password=payload["hashed_password"],
                email=payload['email'],
                info=payload['info']
            )

            session.add(user)
            session.commit()
            response = jsonify({'success': 'OK'})
            response.status_code = 201
            return response

        else:
            response = jsonify({'ERROR': 'USER ALREADY EXISTS'})
            response.status_code = 400
            return response

    @staticmethod
    def patch(user_id):
        payload = request.json()
        session = db_session.create_session()
        current_user = session.query(User).get(user_id)
        if current_user:
            if not session.query(User).filter_by(email=payload["email"]):
                session.query(User).filter_by(id=user_id).update(payload)
                session.commit()

            else:
                response = jsonify({'ERROR': 'EMAIL TAKEN'})
                response.status_code = 400
                return response

        else:
            response = jsonify({'ERROR': 'USER NOT FOUND'})
            response.status_code = 404
            return response
