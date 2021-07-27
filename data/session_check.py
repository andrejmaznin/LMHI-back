from data import db_session
from data.auth_sessions import Session
from data.users import User
from flask import jsonify, request
from flask_restful import Resource
from datetime import datetime


def check_session(session_id, user_id):
    db_sess = db_session.create_session()
    session = db_sess.query(Session).filter(Session.id == session_id).one()
    if session:
        if session.user_id == user_id:
            session.date = datetime.now()
            db_sess.update(session)
            db_sess.commit()
            return True
        return False
    return False
