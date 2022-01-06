import json
from os import path
from flask import jsonify

from flask import request
from werkzeug.exceptions import BadRequest

from modules.json_validator.validator import validate_payload


def validate_json(schema: str = None):
    def handler_decorator(handler):
        def inner():
            if schema is not None:
                target_schema = path.abspath('request_schema/' + schema)
                with open(target_schema, mode='r') as f:
                    target_schema = json.loads(f.read())

                payload = request.get_json()

                try:
                    validate_payload(payload=payload, schema=target_schema)
                except AssertionError:
                    raise BadRequest()

                response = jsonify(handler(payload))
            else:
                response = handler()

            response.status_code = 201
            return response

        return inner

    return handler_decorator