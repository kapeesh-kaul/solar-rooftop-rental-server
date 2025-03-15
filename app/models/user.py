from mongoengine import Document, StringField, EmailField

class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True)
    address = StringField(required=True)
