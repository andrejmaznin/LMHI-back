from flask import jsonify, request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from models.text_data import Interpretation
from service import db_session


class TextDataResource(Resource):
    # url?red=xxxx&green=xxxx&blue=xxxx&yellow=xxxx&main=xxxx
    @staticmethod
    def get():
        session = db_session.create_session()
        ans = {}
        args = request.args
        for i in args.keys():
            code = i + "/" + args[i]
            text = session.query(Interpretation).get(code)
            if text is not None:
                ans[i] = text.info
            else:
                ans[i] = "ERROR"

        return {"result": ans}

    @staticmethod
    def post(num: str = None):
        session = db_session.create_session()
        payload = request.get_json(force=True)

        if num:
            entities = payload["payload"]
            entities = [Interpretation(code=i["code"], info=i["info"]) for i in entities]

            try:
                session.add_all(entities)
                session.commit()
            except IntegrityError:
                raise BadRequest("Row already exists")

            return {'success': 'OK', "rows": len(entities)}

        data = Interpretation(code=payload["code"], info=payload["info"])

        try:
            session.add(data)
        except IntegrityError:
            raise BadRequest("Row already exists")

        return {"row": session.query(Interpretation).get(payload["code"]).as_dict()}
