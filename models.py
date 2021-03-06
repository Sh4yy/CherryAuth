from peewee import *
from datetime import datetime
from Utils.IDGenerator import gen_token
from Utils import Salting, JWT, db
from threading import Thread


class BaseModel(Model):

    class Meta:
        database = db


class User(BaseModel):

    uid = TextField(primary_key=True)
    date_created = DateTimeField(default=datetime.utcnow)

    @classmethod
    def register(cls, uid):
        """
        register a new user
        :param uid: user's global unique id
        :return: User instance
        """

        obj = cls.create(uid=uid)
        obj.save()

        return obj

    @classmethod
    def find_with_uid(cls, uid):
        """
        query user using their uid
        :param uid: targeted uid
        :return: User if found
        """
        return (cls
                .select()
                .where(cls.uid == uid)
                .first())

    def __str__(self):
        return f"<User(uid={self.uid})>"

    def __repr__(self):
        return self.__str__()


class BelongsToUser:

    user = ForeignKeyField(User)

    def belongs_to(self, user: User):
        """
        check whether this instance
        belongs to a user
        :param user: user instance
        :return: True if belongs to user, else false
        """
        return self.user == user

    @classmethod
    def find_with_user(cls, user: User):
        """
        query item using user instance
        :param user: user instance
        :return: list of BelongsToUser if found
        """
        return list(cls.select().where(cls.user == user.uid))


class Session(BaseModel, BelongsToUser):

    session_id = TextField(primary_key=True, default=lambda: gen_token(16))
    refresh_token = TextField(unique=True, default=lambda: gen_token(32))
    date_created = DateTimeField(default=datetime.utcnow)
    last_activity = DateTimeField(default=datetime.utcnow)
    user = ForeignKeyField(User)

    @classmethod
    def init(cls, user):
        """
        create a new Session
        :param user: user's instance
        :return: Session
        """
        obj = cls.create(user=user)
        obj.save()
        return obj

    def gen_jwt(self, ttl: int = 3600):
        """
        generate a new jwt token
        :param ttl: time to live in seconds
        :return: jwt token, payload
        """
        return JWT.gen_jwt(self.session_id, self.user.uid, ttl)

    @classmethod
    def find_with_session_id(cls, session_id: str):
        """
        query session using session id
        :param session_id: target session id
        :return: Session if found
        """
        return (cls
                .select()
                .where(cls.session_id == session_id)
                .first())

    @classmethod
    def find_with_refresh_token(cls, refresh_token: str):
        """
        query session using refresh token
        :param refresh_token: target refresh token
        :return: Session if found
        """
        return (cls
                .select()
                .where(cls.refresh_token == refresh_token)
                .first())

    def update_last_activity(self, background=True):
        """
        update last activity
        :param background: if True will process in background
        :return: True on success
        """

        self.last_activity = datetime.utcnow()
        if background:
            Thread(target=self.save).start()
        else:
            self.save()
        return True

    def __str__(self):
        return f"<Session(session_id={self.session_id}, user={self.user.id})>"

    def __repr__(self):
        return self.__str__()


class Credentials(BaseModel, BelongsToUser):

    user = ForeignKeyField(User, primary_key=True, backref='credentials')
    password = BlobField()  # of course it is hashed
    salt = BlobField()
    date_created = DateTimeField(default=datetime.utcnow)

    @classmethod
    def init(cls, user: User, password: str):
        """
        initialize a new Credentials instance for user
        :param user: target user
        :param password: user's password
        :return: Credentials on success
        :raises IntegrityError: if credentials already exist
        """

        password, salt = cls._create_salt_password(password)
        obj = cls.create(user=user, password=password, salt=salt)
        obj.save()
        return obj

    @staticmethod
    def _create_salt_password(new_password):
        """
        create salt + hashed pass
        :param new_password: new password as str
        :return: password, salt
        """
        salt = Salting.gen_salt()
        password = Salting.hash_pswd(new_password, salt)
        return password, salt

    def change(self, new_password: str):
        """
        change the current password to a new one
        :param new_password: new password
        :return: self
        """
        self.password, self.salt = self._create_salt_password(new_password)
        return self

    def does_match(self, password: str):
        """
        check whether a given password matches
        :param password: given password
        :return: True if matches
        """
        return Salting.validate_pswd(
            hashed_password=self.password.tobytes(),
            salt=self.salt.tobytes(),
            password=password)

    def __str__(self):
        return f"<Credentials(user={self.user.id})>"

    def __repr__(self):
        return self.__str__()

