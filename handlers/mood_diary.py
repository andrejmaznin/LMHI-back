from flask import request
from flask_restful import Resource

from models import MoodDiary, User
from modules.json_validator import validate_json
from service import db_session


class MoodDiaryResource(Resource):
    @staticmethod
    @validate_json('mood_diary/post.json')
    def post(payload):
        session = db_session.create_session()

        mood_diary_note = MoodDiary(**payload['mood_diary_note'])

        session.add(mood_diary_note)
        session.commit()

        return {"id": mood_diary_note.id}

    @staticmethod
    def get():
        session = db_session.create_session()

        token = request.headers.get('token')
        user = session.query(User).filter(User.token == token).first()

        diary_notes = session.query(MoodDiary).filter(MoodDiary.user_id == user.id)

        return [note.as_dict() for note in diary_notes]
