from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from models.habit import Habit
from modules.json_validator import validate_json


class HabitResource(Resource):
    @staticmethod
    @validate_json('habit/post.json')
    def post(payload, token):
        from main_requests import session

        habits = [Habit(**i) for i in payload['habits']]
        session.add_all(habits)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise BadRequest('Row already exists')

    @staticmethod
    def get():
        from main_requests import session

        return [i.as_dict() for i in session.query(Habit).all()]
