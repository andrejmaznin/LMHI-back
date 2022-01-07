from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from models import TestResult, User
from modules.json_validator import validate_json
from service import db_session


class TestResultResource(Resource):
    @staticmethod
    @validate_json('test_result/post.json')
    def post(payload):
        session = db_session.create_session()
        test_result = TestResult(**payload['test_result'])

        try:
            session.add(test_result)
            session.commit()
        except IntegrityError:
            raise BadRequest()

        return {"id": test_result.id}

    @staticmethod
    def get():
        session = db_session.create_session()

        token = request.headers.get('token')
        if token is None:
            return [result.as_dict() for result in session.query(TestResult).all()]

        user = session.query(User).filter(User.token == token).first()
        if user is not None:
            test_results = session.query(TestResult).filter(TestResult.user_id == user.id)
            return [result.as_dict() for result in test_results]

        raise BadRequest()
