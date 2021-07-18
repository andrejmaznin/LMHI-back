from flask import jsonify, request
from flask_restful import Resource, abort
from . import db_session
from .mood_notes import MoodNote
from .users import User
import traceback


class MoodNoteResource(Resource):
    @staticmethod
    def post():
        payload = request.json()
        session = db_session.create_session()
        user_id = payload['user_id']
        session_id = payload['session']
        try:
            if session.query(User).filter(User.id == user_id, User.session.like(
                    session_id)).all():  # проверка наличия пользователя с такой сессией
                diary_note = MoodNote(user_id=payload['user_id'],
                                      scale_id=payload['scale_id'],
                                      date=payload['date'],
                                      value=payload['value']
                                      )
                session.add(diary_note)
                session.commit()
                diary_note_id = session.query(MoodNote).filter(MoodNote.date == payload['date'],
                                                               MoodNote.scale_id == payload['scale_id']).all()[0].id
                response = jsonify({'success': 'OK', "id": diary_note_id})
                response.status_code = 201
            else:
                response = jsonify({'ERROR': "NO USER WITH THE SESSION"})
                response.status_code = 400
                return response

        except Exception as error:
            response = jsonify({"ERROR": traceback.format_exc(error)})
            response.status_code = 400
            return response

    @staticmethod
    def get():
        payload = request.json()
        session = db_session.create_session()
        user_id = payload['user_id']
        session_id = payload['session']
        try:
            if session.query(User).filter(User.id == user_id, User.session.like(
                    session_id)).all():  # проверка наличия пользователя с такой сессией
                # возвращение списка дневника настроений по пользователю и настроению
                mood_notes = session.query(MoodNote).filter(MoodNote.user_id == payload['user_id'],
                                                            MoodNote.scale_id == payload['scale_id']).all()
                response = jsonify({'success': 'OK', "mood_notes": mood_notes})
                response.status_code = 201
            else:
                response = jsonify({'ERROR': "NO USER WITH THE SESSION"})
                response.status_code = 400
                return response

        except Exception as error:
            response = jsonify({"ERROR": traceback.format_exc(error)})
            response.status_code = 400
            return response

    @staticmethod
    def patch():
        payload = request.json()
        session = db_session.create_session()
        user_id = payload['user_id']
        session_id = payload['session']
        try:
            if session.query(User).filter(User.id == user_id, User.session.like(
                    session_id)).all():  # проверка наличия пользователя с такой сессией

                session.query(MoodNote).filter_by(user_id=payload['id']).update(value=payload['value'])
                session.commit()
            else:
                response = jsonify({'ERROR': "NO USER WITH THE SESSION"})
                response.status_code = 400
                return response

        except Exception as error:
            response = jsonify({"ERROR": traceback.format_exc(error)})
            response.status_code = 400
            return response
