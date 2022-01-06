from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
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

        try:
            session.merge(test_result)
        except IntegrityError:
            raise BadRequest()

        return {"id": test_result.id}
