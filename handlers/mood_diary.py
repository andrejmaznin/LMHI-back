from flask import jsonify
from flask_restful import Resource

from models.mood_note import MoodDiary
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

        response = jsonify({'success': 'OK', "id": mood_diary_note.id})
        response.status_code = 201
        return response
