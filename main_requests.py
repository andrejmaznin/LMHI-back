from flask import Flask
from flask_restful import Api

from data.handlers.habits_names_resourses import HabitNameResource
from data.handlers.habits_resourses import HabitResource
from data.handlers.mood_notes_resourses import MoodNoteResource
from data.handlers.mood_scales_resourses import MoodScaleResource
from data.handlers.service_resourse import ServiceResource
from data.handlers.text_data_resourses import TextDataResource
from data.handlers.users_resourses import UsersResource, UserAuthResource
from data.handlers.beta_habit_resource import BetaHabitResource
from data.handlers.mood_criteria_resource import MoodCriteriaResource
from data.service import db_session

app = Flask(__name__)
api = Api(app)

db_session.global_init()

api.add_resource(UsersResource, '/users')
api.add_resource(UserAuthResource, '/auth')
api.add_resource(TextDataResource, '/result', '/result/<num>')
api.add_resource(HabitResource, '/habits')
api.add_resource(HabitNameResource, '/habit_names')
api.add_resource(ServiceResource, "/service/<action>")
api.add_resource(BetaHabitResource, '/beta_habits')
api.add_resource(MoodCriteriaResource, "/mood_criteria")

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
