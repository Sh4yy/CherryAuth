from mongoengine import *
from Models.User import User
from Utils import IDGenerator
from datetime import datetime


class Session(Document):

    session_id = StringField(primary_key=True, unique=True)
    create_date = DateTimeField(default=datetime.utcnow)
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    last_activity = DateTimeField()

    @classmethod
    def init(cls, user):
        session = cls(user=user, session_id=IDGenerator.gen_access_token())
        session.save()
        return session

    @classmethod
    def find_with_user(cls, user):
        """
        query sessions for a user
        :param user: user instance
        :return: list of sessions
        """
        return cls.objects(user=user)

    @classmethod
    def find_with_id(cls, session_id):
        """
        query sessions with id
        :param session_id: target session id
        :return: A single Session
        :raises: DoesNotExist if session was not found
        """
        return cls.objects.get(session_id=session_id)

    def __str__(self):
        return f"<Session(session_id={self.session_id}, user={self.user.gid})>"

    def __repr__(self):
        return self.__str__()