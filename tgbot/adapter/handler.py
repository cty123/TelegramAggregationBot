import logging
from pyrogram.types import InputMediaPhoto, InputMediaVideo

from tgbot.service.session_service import SessionService

PREVIEW_CMD = "/preview"
END_CMD = "/end"


class TGBotHandler:

    def __init__(self) -> None:
        self.session_service = SessionService()

    def handle(self, client, message):
        # Check if the message is a command, currently there are only following commands,
        # * Any message, text or photo - Start a new session for aggregation and accept the incoming content
        # * /preview - Dump the current session without closing the existing session
        # * /end - End an existing session to aggregate images and text, will return the aggregation result

        message_text = str(message.text)
        user_id = str(message.chat.id)

        logging.info(f"Received message text: {message_text} from user: {user_id}")

        # Close the existing session and dump the session content
        if message_text == END_CMD:
            return self.end_handler(user_id, message)

        if message_text == PREVIEW_CMD:
            return self.preview_handler(user_id, message)

        # Get the session id of the user, create a new one if it doesn't exists.
        return self.message_handler(user_id, message)

    def message_handler(self, user_id, message) -> None:
        # Retrieve the current user session first
        session = self.session_service.retrieve_session_for_user(user_id)

        # Extract text, photo and video
        text = message.text if message.text is not None else message.caption
        photo_id = message.photo.file_id if message.photo is not None else None
        video_id = message.video.file_id if message.video is not None else None

        if text is not None:
            self.session_service.add_paragraph(session.session_id, text)
            message.reply_text(f"Added paragraph [\"{text}]\"")

        if photo_id is not None:
            self.session_service.append_photo(session.session_id, photo_id)
            message.reply_text(f"Update photo file id [\"{photo_id}]\"")

        if video_id is not None:
            self.session_service.append_video(session.session_id, video_id)
            message.reply_text(f"Update video file id [\"{video_id}]\"")

    def end_handler(self, user_id, message):
        try:
            self.preview_handler(user_id, message)
        finally:
            self.session_service.create_new_session_for_user(user_id)
            message.reply_text("Current session terminated")
            logging.info(f"Session ended for {user_id}")

    def preview_handler(self, user_id, message):
        session = self.session_service.retrieve_session_for_user(user_id)

        photo_files = list(map(lambda p: InputMediaPhoto(p), session.photo))
        video_files = list(map(lambda p: InputMediaVideo(p), session.video))
        media_files = photo_files + video_files

        text = ""
        for i, p in enumerate(session.paragraphs):
            text += f"{i + 1}. {p.rstrip()}\n"

        if len(media_files) > 10:
            message.reply_text("Session contains more than 10 media files, will only aggregate the first 10.")
            media_files = media_files[:10]

        if len(media_files) == 0:
            if len(text) == 0:
                text = "Empty"

            message.reply_text(text)
        else:
            first_media = media_files[0]
            first_media.caption = text
            message.reply_media_group(media=media_files)
