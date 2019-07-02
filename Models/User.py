from mongoengine import Document, StringField, DateField
from datetime import datetime


class User(Document):

    # user's global unique id
    gid = StringField(primary_key=True, unique=True)
    reg_date = DateField(default=datetime.utcnow)

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
