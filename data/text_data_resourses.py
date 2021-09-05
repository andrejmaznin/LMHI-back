from flask import jsonify, request
from flask_restful import Resource

from data import db_session
from data.text_data import Result


class TextDataResource(Resource):
    @staticmethod
    def post():
        payload = request.get_json(force=True)
        ans = []
        session = db_session.create_session()
        for i in payload["results"]:
            text = session.query(Result).get(i)
            if text:
                ans.append(text.info)
            else:
                ans.append("ERROR")

        response = jsonify({'success': 'OK', "results": ans})
        response.status_code = 201
        return response
