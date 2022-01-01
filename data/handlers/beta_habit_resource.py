from flask import jsonify, request
from flask_restful import Resource
from data.service import db_session
from data.models.habits import Habit

from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError


class BetaHabitResource(Resource):
    def post(self):
        payload = request.get_json()
        session = db_session.create_session()
        try:
            habits = [Habit(**i) for i in payload['habits']]
            habit_names = [i.name for i in habits]
            print(habits, habit_names)
            try:
                session.add_all(habits)
                session.commit()
            except IntegrityError:
                raise BadRequest('Row already exists')
        except KeyError:
            raise BadRequest('invalid JSON body')

        response = jsonify(
            {
                'success': 'OK',
                "row": len(
                    list(
                        filter(
                            lambda a: a.name in habit_names, session.query(Habit).all()
                        )
                    )
                )
            }
        )
        response.status_code = 201
        return response