from flask import jsonify
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from data.models.text_data import Result
from data.service import db_session


class TextDataResource(Resource):
    # url?red=xxxx&green=xxxx&blue=xxxx&yellow=xxxx&main=xxxx
    @staticmethod
    def get(num: str = None):
        session = db_session.create_session()
        ans = {}
        args = request.args
        for i in args.keys():
            code = i + "/" + args[i]
            text = session.query(Result).get(code)
            if text is not None:
                ans[i] = text.info
            else:
                raise BadRequest()

        response = jsonify({'success': 'OK', "result": ans})
        response.status_code = 201
        return response

    @staticmethod
    def post(num: str = None):
        session = db_session.create_session()
        payload = request.get_json(force=True)

        if num:
            entities = payload["payload"]
            entities = [Result(code=i["code"], info=i["info"]) for i in entities]

            try:
                session.add_all(entities)
                session.commit()
            except IntegrityError:
                raise BadRequest("Row already exists")

            response = jsonify({'success': 'OK', "rows": len(entities)})
            response.status_code = 201
            return response

        data = Result(code=payload["code"], info=payload["info"])

        try:
            session.add(data)
        except IntegrityError:
            raise BadRequest("Row already exists")

        response = jsonify({'success': 'OK', "row": session.query(Result).get(payload["code"]).as_dict()})
        response.status_code = 201
        session.commit()
        return response

