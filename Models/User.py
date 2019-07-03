from mongoengine import *
from datetime import datetime
from Utils import Salting


class Credentials(EmbeddedDocument):

    hashed_pswd = BinaryField()
    salt = BinaryField()

    @classmethod
    def init_and_salt(cls, pswd: str):
        """
        initialize a new Credentials instance
        and salt and hash the password
        :param pswd: pswd
        :return: Credentials instance
        """
        creds = cls()
        creds.salt = Salting.gen_salt()
        creds.hashed_pswd = Salting.hash_pswd(pswd, creds.salt)
        return creds

    def does_math(self, pswd: str):
        """
        check whether a given pswd matches
        :param pswd: given password
        :return: True if matches
        """
        return Salting.validate_pswd(self.hashed_pswd, self.salt, pswd)


class User(Document):

    # user's global unique id
    gid = StringField(primary_key=True)
    reg_date = DateField(default=datetime.utcnow)
    credentials = EmbeddedDocumentField(Credentials)

    @classmethod
    def register(cls, gid, credentials=None):
        """
        register a new user
        :param gid: user's gid
        :param credentials: Credentials instance
        :return: User instance
        """
        user = cls(gid=gid)
        user.credentials = credentials
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


