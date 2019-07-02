from mongoengine import *
from datetime import datetime
from Utils import Salting, IDGenerator


class Credentials(EmbeddedDocument):

    hashed_pswd = BinaryField()
    salt = BinaryField()

    def does_math(self, pswd: str):
        """
        check whether a given pswd matches
        :param pswd: given password
        :return: True if matches
        """
        return Salting.validate_pswd(self.hashed_pswd, self.salt, pswd)


class User(Document):

    # user's global unique id
    gid = StringField(primary_key=True, unique=True)
    reg_date = DateField(default=datetime.utcnow)
    credentials = EmbeddedDocumentField(Credentials)

    @classmethod
    def register(cls, gid):
        """
        register a new user
        :param gid: user's gid
        :return: User instance
        """
        user = cls(gid=gid)
        user.save()
        return user

    @classmethod
    def find_with_gid(cls, gid):
        """
        query users with gid
        :param gid: target gid
        :return: A single User
        :raises: DoesNotExist if user was not found
        """
        return cls.objects.get(gid=gid)

    def __str__(self):
        return f"<User(gid={self.gid})>"

    def __repr__(self):
        return self.__str__()


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

