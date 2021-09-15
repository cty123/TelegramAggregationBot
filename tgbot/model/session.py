from mongoengine import Document
from mongoengine.fields import BooleanField, DateTimeField, ListField, StringField


class Session(Document):
    user_id = StringField(required=True, max_length=32)
    session_id = StringField(require=True, max_length=64, unique=True)
    creation_time = DateTimeField(required=True)
    photo = ListField(StringField(max_length=512), max_length=10)
    video = ListField(StringField(max_length=512), max_length=10)
    text = StringField(max_length=1024)
    is_open = BooleanField(required=True, default=True)

    meta = {
        'indexes': [
            '#user_id',
            '#session_id'
        ],
    }
