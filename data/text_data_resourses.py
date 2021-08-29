from flask import jsonify, request
from flask_restful import Resource

from data import db_session
from data.text_data import Result


class TextDataResource(Resource):
    @staticmethod
    def post():
        payload = request.get_json(force=True)

        session = db_session.create_session()
        if not session.query(Result).filter(Result.code == payload["code"]).all():
            text_block = Result(
                code=payload['code'], info=payload["info"]
            )
            session.add(text_block)
            session.commit()
            
            response = jsonify({'success': 'OK'})
            response.status_code = 201
            return response

        else:
            response = jsonify({'ERROR': 'TEXT BLOCK ALREADY EXISTS'})
            response.status_code = 400
            return response

    @staticmethod
    def get():
        payload = request.get_json(force=True)

        session = db_session.create_session()
        text = session.query(Result).get(payload["code"])
        if text:
            response = jsonify({'success': 'OK', "text": text.info})
            response.status_code = 201
            return response

        else:
            response = jsonify({'ERROR': 'INVALID CODE'})
            response.status_code = 400
            return response
