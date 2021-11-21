from flask import jsonify
from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from data.service import db_session
from data.models.__all_models import *


class ServiceResource(Resource):
    @staticmethod
    def get(action):
        session = db_session.create_session()
        args = request.args
        if action == "clean_table":
            template = args.get("template")
            value = args.get("value")
            model = args.get("model")
            reverse = args.get("reverse") == "true"

            if model in MODELS_STRINGS:
                model_class = MODELS[MODELS_STRINGS.index(model)]  # getting class by its name
                value_string = eval(f"model_class.{value}")

                if reverse:
                    query = session.query(model_class).filter(value_string.notlike(template)).delete(
                        synchronize_session=False)
                else:
                    query = session.query(model_class).filter(value_string.like(template)).delete(
                        synchronize_session=False)

                deleted = query
                session.commit()

                response = jsonify({'success': 'OK', "deleted": deleted})
                response.status_code = 201
                return response

            raise BadRequest()
