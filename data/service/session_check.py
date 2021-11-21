from data.models.auth_sessions import Session
from datetime import datetime
from data.service import db_session


def check_session(session_id, user_id):
    db_sess = db_session.create_session()
    session = db_sess.query(Session).filter(Session.id == session_id).all()
    if session:
        session = session[0]
        if session.user_id == user_id:
            date = {'date': datetime.now().strftime('%y.%m.%d %H:%M:%S')}
            db_sess.query(Session).filter_by(id=session.id).update(date)
            db_sess.commit()
            return True
        return False
    return False
