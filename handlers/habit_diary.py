from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from models import HabitNote, User
from modules.json_validator import validate_json


class HabitDiaryResource(Resource):
    @staticmethod
    @validate_json('habit_diary/post.json')
    def post(payload, token):
        from main_requests import session
        user_id = session.query(User).filter(User.token == token).one().id
        habit_diary_notes = [HabitNote(user_id, **note) for note in payload]

        try:
            session.add_all(habit_diary_notes)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise BadRequest('No user found')

        return [note.id for note in habit_diary_notes]

    @staticmethod
    def get():
        from main_requests import session

        token = request.headers.get('token')
        if not token:
            raise BadRequest('No token provided')

        user = session.query(User).filter(User.token == token).first()
        if user is not None:
            diary_notes = session.query(HabitNote).filter(HabitNote.user_id == user.id)
            return [note.as_dict() for note in diary_notes]

        raise BadRequest('No user for token')
