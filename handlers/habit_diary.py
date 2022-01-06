from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from models import HabitNote, User
from modules.json_validator import validate_json
from service import db_session


class HabitDiaryResource(Resource):
    @staticmethod
    @validate_json('habit_diary/post.json')
    def post(payload):
        session = db_session.create_session()

        habit_diary_note = HabitNote(**payload['habit_note'])

        session.add(habit_diary_note)
        try:
            session.commit()
        except IntegrityError:
            raise BadRequest('No user found')

        return {"id": habit_diary_note.id}

    @staticmethod
    def get():
        session = db_session.create_session()

        token = request.headers.get('token')
        user = session.query(User).filter(User.token == token).first()

        diary_notes = session.query(HabitNote).filter(HabitNote.user_id == user.id)

        return [note.as_dict() for note in diary_notes]
