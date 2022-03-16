from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from models.text_data import Interpretation


class TextDataResource(Resource):
    # url?red=xxxx&green=xxxx&blue=xxxx&yellow=xxxx&main=xxxx
    @staticmethod
    def get():
        from main_requests import session

        ans = {}
        args = request.args
        if args is not None:
            for i in args.keys():
                code = i + "/" + args[i]
                text = session.query(Interpretation).get(code)
                if text is not None:
                    ans[i] = text.info
                else:
                    ans[i] = "ERROR"

            return {"result": ans}
        return [i.as_dict() for i in session.query(Interpretation).all()]

    @staticmethod
    def post(num: str = None):
        from main_requests import session

        payload = request.get_json(force=True)

        if num:
            entities = [Interpretation(code=code, info=info) for code, info in payload.items()]
            session.add_all(entities)

            try:
                session.commit()
            except IntegrityError:
                raise BadRequest("Row already exists")

        else:
            data = Interpretation(**payload)
            session.add(data)

            try:
                session.commit()
            except IntegrityError:
                raise BadRequest("Row already exists")
