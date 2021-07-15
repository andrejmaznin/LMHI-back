from flask import jsonify, request
from flask_restful import Resource, abort
from data import db_session


class UsersResource(Resource):
    def post(self):
        payload = request.json()
