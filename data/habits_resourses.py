from flask import jsonify, request
from flask_restful import Resource, abort
from . import db_session
from .habits import Habit
from .users import User
from .session_check import check_session
import traceback


class HabitResource(Resource):
    @staticmethod
    def post():  # добавление одной новой записи дневника, требуется session_id, user_id, habit_id, date, value
        payload = request.get_json()
        session = db_session.create_session()
        try:
            if check_session(payload['session_id'],
                             payload['user_id']):  # проверка наличия пользователя с такой сессией
                habit_note = Habit(user_id=payload['user_id'],
                                      habit_id=payload['scale_id'],
                                      date=payload['date'],
                                      value=payload['value']
                                      )
                session.add(habit_note)
                session.commit()
                habit_note_id = session.query(Habit).filter(Habit.date == payload['date'],
                                                               Habit.scale_id == payload['scale_id']).all()[0].id
                response = jsonify({'success': 'OK', "id": habit_note_id})
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
    def get():  # получение всех записей по user_id и habit_id. Требуется session_id, user_id, habit_id
        payload = request.get_json()
        session = db_session.create_session()
        try:
            if check_session(payload['session_id'],
                             payload['user_id']):  # проверка наличия пользователя с такой сессией

                # возвращение списка дневника настроений по пользователю и настроению
                habit_notes = [note.as_dict() for note in
                              session.query(Habit).filter(Habit.user_id == payload['user_id'],
                                                             Habit.scale_id == payload['scale_id']).all()]
                response = jsonify({'success': 'OK', "mood_notes": habit_notes})
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
                session.query(Habit).filter_by(id=payload['id']).update({'value': payload['value']})
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
