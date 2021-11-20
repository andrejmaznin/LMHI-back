from flask import jsonify
from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from data import db_session
from data.text_data import Result


class TextDataResource(Resource):
    # url?red=xxxx&green=xxxx&blue=xxxx&yellow=xxxx&main=xxxx
    @staticmethod
    def get():
        session = db_session.create_session()
        ans = {}
        args = request.args
        for i in args.keys():
            code = i + args[i]
            text = session.query(Result).get(code)
            if text is not None:
                ans[i] = text.info
            else:
                raise BadRequest()
        response = jsonify({'success': 'OK', "result": ans})
        response.status_code = 201
        return response

    @staticmethod
    def post():
        payload = request.get_json(force=True)
        session = db_session.create_session()
        data = Result(code=payload["code"], info=payload["info"])
        check = session.query(Result).get(payload["code"])
        if not check:
            session.add(data)
            session.commit()
        session.close()
        response = jsonify({'success': 'OK', "row": session.query(Result).get(payload["code"]).as_dict()})
        response.status_code = 201
        return response

