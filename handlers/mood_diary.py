from flask import request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from models import MoodDiary, User
from modules.json_validator import validate_json
from request_schema import mood_diary


class MoodDiaryResource(Resource):
    @staticmethod
    @validate_json(mood_diary)
    def post(payload, token):
        from main_requests import session

        mood_diary_note = MoodDiary(**payload['mood_diary_note'])
        mood_diary_note.user_id = session.query(User).filter(User.token == token).one().id

        session.add(mood_diary_note)
        session.commit()

        return {"id": mood_diary_note.id}

    @staticmethod
    def get():
        from main_requests import session

        token = request.headers.get('token')
        user = session.query(User).filter(User.token == token).first()
        if user is not None:
            diary_notes = session.query(MoodDiary).filter(MoodDiary.user_id == user.id)
            return [note.as_dict() for note in diary_notes]

        raise BadRequest()
