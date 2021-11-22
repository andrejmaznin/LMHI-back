import random
import string

from flask import jsonify
from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from data.models.__all_models import *
from data.service import db_session

max_used_int = 0


def value_by_template(template):
    global max_used_int

    if template == "int":
        max_used_int += 1
        return max_used_int + 1

    template = list(template)
    ans = []

    for i in template:
        if i == "_":
            ans.append(random.choice(string.ascii_letters + string.digits))
        elif i == "%":
            ans += random.choices(string.ascii_letters + string.digits, k=random.randint(10, 30))
        else:
            ans.append(i)

    return "".join(ans)


class ServiceResource(Resource):
    @staticmethod
    def get(action):
        session = db_session.create_session()
        args = request.args

        if action == "clean_table":
            template = args.get("template")
            column = args.get("column")
            model = args.get("model")
            reverse = args.get("reverse") == "true"

            if model in MODELS_STRINGS:
                model_class = MODELS[MODELS_STRINGS.index(model)]  # getting class by its name
                value_string = eval(f"model_class.{column}")

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

        elif action == "add":
            try:
                model = args.get("model")
                columns = args.getlist("column")
                templates = args.getlist("template")
                number = int(args.get("number"))

            except ValueError:
                raise BadRequest()

            if model in MODELS_STRINGS and len(columns) == len(templates):
                model_class = MODELS[MODELS_STRINGS.index(model)]
                k = len(columns)
                models = []

                for i in range(number):
                    kwargs = {}
                    for j in range(k):
                        kwargs[columns[j]] = value_by_template(templates[j])

                    models.append(model_class(**kwargs))

                session.add_all(models)
                session.commit()

                response = jsonify({'success': 'OK', "added": number})
                response.status_code = 201
                return response
