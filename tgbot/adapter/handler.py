import logging 
from pyrogram.types import InputMediaPhoto

from tgbot.service.session_service import SessionService

START_CMD = "/start"
END_CMD = "/end"

class TGBotHandler:

    def __init__(self) -> None:
        self.session_service = SessionService()

    def handle(self, client, message):

        # Check if the message is a command, currently there are only following commands,
        # * /start - Start a new session to aggregate images and text
        # * /end - End an existing session to aggregate images and text, will return the aggregation result

        message_text = str(message.text)
        user_id = str(message.chat.id)

        logging.info(f"Received message text: {message_text} from user: {user_id}")

        if message_text == START_CMD:
            return self.start_handler(user_id, message)
        
        if message_text == END_CMD:
            return self.end_handler(user_id, message)

        # Get the session id of the user, create a new one if it doesn't exists.
        return self.message_handler(user_id, message)


    def start_handler(self, user_id, message) -> None:
        logging.info(f"Received start command from user: {user_id}, creating new session")
        
        # Create new session
        session_id = self.session_service.create_new_session(user_id)
        message.reply_text(f"Created new session {session_id}")


    def message_handler(self, user_id, message) -> None:
        text = message.text if message.text is not None else message.caption
        photo_id = message.photo.file_id if message.photo is not None else None 

        session = self.session_service.get_or_create_session(user_id)

        if text is not None:
            session.text = text
            session.save()
            message.reply_text(f"Update text [\"{text}]\"")

        if photo_id is not None:
            self.session_service.append_photo_to_session(user_id, photo_id)
            message.reply_text(f"Update photo file id [\"{photo_id}]\"")

    def end_handler(self, user_id, message):
        session = self.session_service.retrieve_session(user_id)
        
        if session is None:
            message.reply_text(f"No existing session exists for user {user_id}, enter /start to start a new session")
            return

        media_files = list(map(lambda p: InputMediaPhoto(p), session.photo))
        if len(media_files) == 0:
            return message.reply_text(session.text)

        first_media = media_files[0]
        first_media.caption = session.text

        return message.reply_media_group(media=media_files)
 