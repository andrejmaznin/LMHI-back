from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from models.mood_criteria import MoodCriteria
from modules.json_validator import validate_json
from request_schema import mood_criteria


class MoodCriteriaResource(Resource):
    @staticmethod
    @validate_json(mood_criteria)
    def post(payload, token):
        from main_requests import session

        criterias = [MoodCriteria(**criteria) for criteria in payload['mood_criterias']]
        session.add_all(criterias)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise BadRequest('Row already exists')

    @staticmethod
    def get():
        from main_requests import session

        return [i.as_dict() for i in session.query(MoodCriteria).all()]
