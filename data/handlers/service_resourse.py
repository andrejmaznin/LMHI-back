from flask import jsonify
from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from data.models.__all_models import *
from data.service import db_session


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
                    query = session.query(model_class).filter(value_string.notlike(template))
                else:
                    query = session.query(model_class).filter(value_string.like(template))

                if model_class.__tablename__ == "users":
                    user_ids = []
                    for i in query.all():
                        user_ids.append(i.id)
                        
                    sessions = session.query(Session).filter(Session.user_id.in_(user_ids)).delete(
                        synchronize_session=False)

                deleted = query.delete(synchronize_session=False)
                session.commit()

                response = jsonify({'success': 'OK', "deleted": deleted})
                response.status_code = 201
                return response

            raise BadRequest()
