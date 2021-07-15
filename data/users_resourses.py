from flask import jsonify, request
from flask_restful import Resource, abort
import db_session
from users import User
import hashlib


class UsersResource(Resource):
    def post(self):
        payload = request.json()
        session = db_session.create_session()
        if not session.query(User).filter(User.email == payload['email']).all():
            user = User(
                name=payload['name'],
                hashed_password=payload["hashed_password"],
                email=payload['email'],
                info=payload['info'],
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
