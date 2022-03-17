from flask import jsonify, request
from werkzeug.exceptions import BadRequest

from modules.json_validator.validator import validate_payload
from request_schema import *  # noqa


def validate_json(file):
    def handler_decorator(handler):
        def inner():
            from main_requests import logger

            logger.debug(file.__name__)
            schema = eval(f'file.{handler.__name__.upper()}')
            if schema is not None:

                payload = request.get_json()

                try:
                    validate_payload(payload=payload, schema=schema)
                except AssertionError:
                    raise BadRequest(str(payload))

                response = jsonify(handler(payload, request.headers.get('token')))
            else:
                response = handler()

            response.status_code = 201
            return response

        return inner

    return handler_decorator
