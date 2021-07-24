from flask import Flask
from flask_restful import Api

from data import db_session
from data.mood_notes_resourses import MoodNoteResource
from data.mood_scales_resourses import MoodScaleResource
from data.users_resourses import UsersResource

app = Flask(__name__)
api = Api(app)


def main():
    db_session.global_init("lmhi")
    api.add_resource(UsersResource, '/users')
    api.add_resource(MoodNoteResource, '/mood_notes')
    api.add_resource(MoodScaleResource, '/mood_scales')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
