from flask import jsonify
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

        criterias = [MoodCriteria(**i) for i in payload['mood_criterias']]
        names = [i.name for i in criterias]

        try:
            session.add_all(criterias)
            session.commit()
        except IntegrityError:
            raise BadRequest('Row already exists')

        response = jsonify(
            {
                'success': 'OK',
                "row": len(
                    list(
                        filter(
                            lambda a: a.name in names, session.query(MoodCriteria).all()
                        )
                    )
                )
            }
        )
        response.status_code = 201
        return response

    def get(self):
        session = db_session.create_session()

        return [i.as_dict() for i in session.query(MoodCriteria).all()]
