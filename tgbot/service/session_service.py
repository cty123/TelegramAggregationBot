from tgbot.model.user_session import UserSession
import uuid
import datetime
import logging

from model.session import Session


class SessionService:

    def create_session(self, user_id):
        session_id = str(uuid.uuid4())
        session = Session(user_id=user_id, session_id=session_id, creation_time=datetime.datetime.now())
        session.save()
        return session

    def get_user_session(self, user_id):
        return UserSession.objects(user_id=user_id).first()

    def bind_active_session(self, user_id, session_id):
        UserSession.objects(user_id=user_id).modify(upsert=True, new=True, set__session_id=session_id)
        return None

    def retrieve_session_for_user(self, user_id):
        # Retrieve the active session of the user
        user_session = self.get_user_session(user_id)

        # If the user doesn't have existing session, create a new one for the user and bind it as active
        if user_session is None:
            return self.create_new_session_for_user(user_id)

        # Retrieve the session based on the session id
        session = Session.objects(session_id=user_session.session_id).first()
        logging.info(f"Retrieved session {session.session_id} for user {user_id}")

        return session

    def create_new_session_for_user(self, user_id):
        # Create new session for user
        session = self.create_session(user_id)
        logging.info(f"Created new session for user {user_id}, session_id: {session.session_id}")

        # Set the new session as active session for user
        self.bind_active_session(user_id, session.session_id)
        logging.info(f"Set session {session.session_id} as the active session for user {user_id}")

        return session

    def add_paragraph(self, session_id, text):
        Session.objects(session_id=session_id).update_one(push__paragraphs=text)

    def append_photo(self, session_id, photo_id):
        Session.objects(session_id=session_id).update_one(push__photo=photo_id)

    def append_video(self, session_id, video_id):
        Session.objects(session_id=session_id).update_one(push__video=video_id)
