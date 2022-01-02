import traceback

from flask import jsonify, request
from flask_restful import Resource

from data.models.mood_notes import MoodNote
from data.service import db_session
from data.service.session_check import check_session


class MoodNoteResource(Resource):
    @staticmethod
    def post():  # добавление одной новой записи дневника, требуется session_id, user_id, scale_id, date, value
        payload = request.get_json()
        session = db_session.create_session()
        try:
            if check_session(payload['session_id'],
                             payload['user_id']):  # проверка наличия пользователя с такой сессией
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
                return response
            else:
                response = jsonify({'ERROR': "NO USER WITH THE SESSION"})
                response.status_code = 400
                return response

        except Exception as error:
            response = jsonify({"ERROR": traceback.format_exc(error)})
            response.status_code = 400
            return response

    @staticmethod
    def get():  # получение всех записей по user_id и scale_id. Требуется session_id, user_id, scale_id
        payload = request.get_json()
        session = db_session.create_session()
        try:
            if check_session(payload['session_id'],
                             payload['user_id']):  # проверка наличия пользователя с такой сессией

                # возвращение списка дневника настроений по пользователю и настроению
                mood_notes = [note.as_dict() for note in
                              session.query(MoodNote).filter(MoodNote.user_id == payload['user_id'],
                                                             MoodNote.scale_id == payload['scale_id']).all()]
                response = jsonify({'success': 'OK', "mood_notes": mood_notes})
                response.status_code = 201
                return response
            else:
                response = jsonify({'ERROR': "NO USER WITH THE SESSION"})
                response.status_code = 400
                return response

        except Exception as error:
            response = jsonify({"ERROR": traceback.format_exc(error)})
            response.status_code = 400
            return response

    @staticmethod
    def patch():  # изменение уже существующей записи по id записи. Требуется id, value.
        payload = request.get_json()
        session = db_session.create_session()
        try:
            if check_session(payload['session_id'],
                             payload['user_id']):  # проверка наличия пользователя с такой сессией
                # возможно только обновление параметра value
                session.query(MoodNote).filter_by(id=payload['id']).update({'value': payload['value']})
                session.commit()
                response = jsonify({'SUCCES': 'OK'})
                response.status_code = 201
                return response
            else:
                response = jsonify({'ERROR': "NO USER WITH THE SESSION"})
                response.status_code = 400
                return response

        except Exception as error:
            response = jsonify({"ERROR": traceback.format_exc(error)})
            response.status_code = 400
            return response
