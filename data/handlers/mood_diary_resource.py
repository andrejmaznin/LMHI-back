from flask import jsonify, request
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from data.models.mood_diary import MoodDiary
from data.service import db_session


class MoodDiaryResource(Resource):
    def post(self):
        payload = request.get_json()
        session = db_session.create_session()

        try:
            mood_diary_note = MoodDiary(**payload['mood_diary_note'])
        except TypeError:
            raise BadRequest()

        session.add(mood_diary_note)
        session.commit()
        
        response = jsonify({'success': 'OK', "id": mood_diary_note.id})
        response.status_code = 201
        return response
