from flask import Flask
from data import db_session
from flask_restful import reqparse, abort, Api, Resource
from data.users_resourses import UsersResource
from data.mood_notes_resourses import MoodNoteResource
from data.mood_scales_resourses import MoodScaleResource


app = Flask(__name__)
api = Api(app)


def main():
    db_session.global_init()
    api.add_resource(UsersResource, '/users')
    api.add_resource(MoodNoteResource, '/mood_notes')
    api.add_resource(MoodScaleResource, '/mood_scales')
    app.run(host="127.0.0.1", port=8080)


if __name__ == '__main__':
    main()
