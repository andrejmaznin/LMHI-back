from flask import jsonify, request
from flask_restful import Resource, abort
from . import db_session
from .mood_scales import MoodScale
import traceback


class MoodScaleResource(Resource):
    @staticmethod
    def post():
        payload = request.json()
        session = db_session.create_session()
        try:
            scale = MoodScale(name=payload['name'])
            session.add(scale)
            session.commit()

        except Exception as error:
            response = jsonify({"ERROR": traceback.format_exc(error)})
            response.status_code = 400
            return response

    @staticmethod
    def get():
        payload = request.json()
        session = db_session.create_session()
        try:
            scales = session.query(MoodScale).all()
            response = jsonify({'SUCCES': 'OK', 'scales': scales})
            response.status_code = 201
            return response

        except Exception as error:
            response = jsonify({"ERROR": traceback.format_exc(error)})
            response.status_code = 400
            return response
