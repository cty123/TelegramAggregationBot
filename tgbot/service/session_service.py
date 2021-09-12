from tgbot.model.user_session import UserSession
import uuid
import datetime
import logging

from model.session import Session

class SessionService:

    def create_new_session(self, user_id):
        # Create new session
        session_id = str(uuid.uuid4())
        session = Session(user_id=user_id, session_id=session_id, creation_time=datetime.datetime.now())
        session.save()

        logging.info(f"Created new session for user {user_id}, session_id: {session_id} - {session}")

        # Set the session as the active session of the user
        UserSession.objects(user_id=user_id).modify(upsert=True, new=True, set__session_id=session_id)

        logging.info(f"Set session {session_id} as the active session for user {user_id}")
        return session_id

    def get_or_create_session(self, user_id):
        # Retrieve the active session of the user
        user_session = self.retrieve_user_session(user_id)

        # Raise error if the user has no active session at all
        if user_session is None:
            return self.create_new_session(user_id)

        # Retrieve the session based on the session id
        session_id = user_session.session_id
        session = Session.objects(session_id=session_id).first()
    
        logging.info(f"Retrieved session {session_id} for user {user_id}")

        return session

    def append_photo_to_session(self, user_id, photo_id):
        user_session = self.get_or_create_session(user_id)

        session_id = user_session.session_id
        Session.objects(session_id=session_id).update_one(push__photo=photo_id)

    def retrieve_user_session(self, user_id):
        user_session = UserSession.objects(user_id=user_id).first()
        return user_session
    
    def retrieve_session(self, user_id):
        user_session = UserSession.objects(user_id=user_id).first()

        if UserSession is None:
            return None
        
        return Session.objects(session_id=user_session.session_id).first()
        