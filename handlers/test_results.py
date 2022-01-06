from flask import jsonify
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from models.test_result import TestResult
from modules.json_validator import validate_json
from service import db_session


class TestResultResource(Resource):
    @staticmethod
    @validate_json('test_result/post.json')
    def post(payload):
        session = db_session.create_session()

        test_result = TestResult(**payload['test_result'])

        if result_id := getattr(
                test_result,
                "id",
                None
        ):
            if unfinished := session.query(TestResult).get(result_id):
                unfinished.result = test_result.result
                unfinished.finished = test_result.finished
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
