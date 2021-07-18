from flask import Flask
from data import db_session
from flask_restful import Api
from data.mood_notes_resource import MoodNoteResource
from data.mood_scales_resource import MoodScaleResource


app = Flask(__name__)
api = Api(app)


def main():
    db_session.global_init("lmhi")
    api.add_resource(MoodNoteResource, '/mood_note')
    api.add_resource(MoodScaleResource, '/scale')
    app.run()


if __name__ == '__main__':
    main()
