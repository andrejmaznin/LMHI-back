from flask import jsonify, request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from data.models.mood_criterias import MoodCriteria
from data.service import db_session


class MoodCriteriaResource(Resource):
    def post(self):
        payload = request.get_json()
        session = db_session.create_session()
        try:
            criterias = [MoodCriteria(**i) for i in payload['mood_criterias']]
            names = [i.name for i in criterias]
            print(criterias, names)
            try:
                session.add_all(criterias)
                session.commit()
            except IntegrityError:
                raise BadRequest('Row already exists')
        except KeyError:
            raise BadRequest('Invalid JSON body')

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
