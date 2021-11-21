from flask import jsonify, request
from flask_restful import Resource
from data.service import db_session
from data.models.mood_scales import MoodScale
import traceback


# TODO: встроить индивидуальные клучи для разработчков для изменения таблицы (27.07.2021)
class MoodScaleResource(Resource):
    @staticmethod
    def post():  # добавление одной новой строки, требуется только имя строки
        payload = request.get_json()
        session = db_session.create_session()
        try:
            scale = MoodScale(name=payload['name'])
            session.add(scale)
            session.commit()
            scale_id = session.query(MoodScale).filter_by(name=payload['name']).one().id
            response = jsonify({'SUCCES': 'OK', 'id': scale_id})
            response.status_code = 201
            return response

        except Exception as error:
            response = jsonify({"ERROR": traceback.format_exc(error)})
            response.status_code = 400
            return response

    @staticmethod
    def get():  # получение всей таблицы с id и name
        session = db_session.create_session()
        try:
            scales = [scale.as_dict() for scale in session.query(MoodScale).all()]
            response = jsonify({'SUCCES': 'OK', 'scales': scales})
            response.status_code = 201
            return response

        except Exception as error:
            response = jsonify({"ERROR": traceback.format_exc(error)})
            response.status_code = 400
            return response
