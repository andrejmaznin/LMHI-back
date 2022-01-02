from flask import jsonify
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest
from flask import Response
from data.models.test_results import TestResult
from data.service import db_session


class TestResultResource(Resource):
    def post(self) -> Response:
        payload = request.get_json()
        session = db_session.create_session()

        try:
            test_result = TestResult(**payload['test_result'])
        except TypeError:
            raise BadRequest()

        if result_id := getattr(
                test_result,
                "id",
                None
        ):
            if unfinished := session.query(TestResult).get(result_id):
                unfinished.result = test_result.result
                unfinished.finished = True
                session.commit()

                response = jsonify({'success': 'OK', "id": result_id})
                response.status_code = 201
                return response

            else:
                raise BadRequest()

        session.add(test_result)
        session.commit()

        response = jsonify({'success': 'OK', "id": test_result.id})
        response.status_code = 201
        return response
