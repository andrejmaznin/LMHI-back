from flask import Flask
from data import db_session
from flask_restful import reqparse, abort, Api, Resource
from data.users_resourses import UsersResource

app = Flask(__name__)
api = Api(app)


def main():
    #db_session.global_init("lmhi")
    api.add_resource(UsersResource, '/users')
    app.run(host="25.19.108.155", port=8080)


if __name__ == '__main__':
    main()
