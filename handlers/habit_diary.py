from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from models import HabitNote
from modules.json_validator import validate_json
from service import db_session


class HabitDiaryResource(Resource):
    @staticmethod
    @validate_json('habit_diary/post.json')
    def post(payload):
        session = db_session.create_session()

        try:
            habit_diary_note = HabitNote(**payload['habit_note'])
            session.add(habit_diary_note)
            session.commit()
        except IntegrityError:
            raise BadRequest('No user found')

        return {"id": habit_diary_note.id}

    @staticmethod
    def get(user_id: int = None):
        session = db_session.create_session()

        if user_id is not None:
            habit_notes = session.query(HabitNote).filter(HabitNote.user_id == user_id).all()
        else:
            habit_notes = session.query(HabitNote).all()

        return {"habit_notes": [note.as_dict() for note in habit_notes]}
