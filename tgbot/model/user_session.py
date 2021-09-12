from enum import unique
from mongoengine import Document
from mongoengine.fields import StringField

class UserSession(Document):
    user_id = StringField(required=True, max_length=32, unique=True)
    session_id = StringField(require=True, max_length=64)

    meta = {
        'indexes': [
            '#user_id',
        ],
    }