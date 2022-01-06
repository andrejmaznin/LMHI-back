from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from models.mood_criteria import MoodCriteria
from modules.json_validator import validate_json
from service import db_session


class MoodCriteriaResource(Resource):
    @staticmethod
    @validate_json('mood_criteria/post.json')
    def post(payload):
        session = db_session.create_session()

        criterias = [MoodCriteria(**criteria) for criteria in payload['mood_criterias']]
        session.add_all(criterias)

        try:
            session.commit()
        except IntegrityError:
            raise BadRequest('Row already exists')

    @staticmethod
    def get():
        session = db_session.create_session()

        return [i.as_dict() for i in session.query(MoodCriteria).all()]
