from flask import Flask
from flask_restful import Api

from handlers import (HabitResource, HabitDiaryResource,
                      MoodCriteriaResource, MoodDiaryResource, ServiceResource,
                      TestResultResource, TextDataResource, UserAuthResource,
                      UsersResource)
from service import db_session

app = Flask(__name__)
api = Api(app)

db_session.global_init()

api.add_resource(UsersResource, '/users')
api.add_resource(UserAuthResource, '/auth')
api.add_resource(TextDataResource, '/result', '/result/<num>')
api.add_resource(ServiceResource, "/service/<action>")
api.add_resource(HabitResource, '/beta_habits')
api.add_resource(MoodCriteriaResource, "/mood_criteria")
api.add_resource(TestResultResource, "/test_result")
api.add_resource(MoodDiaryResource, "/mood_diary")
api.add_resource(HabitDiaryResource, '/habit_diary')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
