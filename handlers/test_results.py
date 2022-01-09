from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from models import Interpretation, TestResult, User
from modules.json_validator import validate_json
from service import db_session

BLOCKS = ['main', 'blue', 'green', 'red', 'yellow']


class TestResultResource(Resource):
    @staticmethod
    @validate_json('test_result/post.json')
    def post(payload, token):
        session = db_session.create_session()

        test_result = TestResult(**payload['test_result'])
        test_result.user_id = session.query(User).filter(User.token == token).one().id

        try:
            session.add(test_result)
            session.commit()
        except IntegrityError:
            raise BadRequest()

        return {"id": test_result.id}

    @staticmethod
    def get():
        session = db_session.create_session()
        test_result_id = request.args.get('id')

        if test_result_id is not None:
            response = {}

            test_result = session.query(TestResult).get(test_result_id)

            for i in BLOCKS:
                response[i] = session.query(Interpretation).get(eval(f'test_result.{i}')).info

            return response

        token = request.headers.get('token')
        if token is None:
            return [result.as_dict() for result in session.query(TestResult).all()]

        user = session.query(User).filter(User.token == token).first()
        if user is not None:
            test_results = session.query(TestResult).filter(TestResult.user_id == user.id)
            return [result.as_dict() for result in test_results]

        raise BadRequest()
