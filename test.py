from unittest import TestCase, main
from app import create_db, create_secret
from controllers import *
from uuid import uuid4
from random import choices


class TestRegistration(TestCase):

    def test_new_user_registration(self):

        uid = uuid4().hex
        password = uuid4().hex

        user = register(uid=uid, password=password)
        self.assertEqual(user.uid, uid)

    def test_user_query(self):

        uid_list = []
        for _ in range(100):
            uid, password = uuid4().hex, uuid4().hex
            uid_list.append((uid, password))
            register(uid=uid, password=password)

        for (uid, password) in choices(uid_list, k=10):
            user = User.find_with_uid(uid)
            self.assertEqual(user.uid, uid)

    def test_duplicate_user_registration(self):

        uid, password = uuid4().hex, uuid4().hex
        register(uid=uid, password=password)

        self.assertRaises(UserAlreadyExist, register, uid, password)

    def test_user_delete(self):

        uid, password = uuid4().hex, uuid4().hex
        user1 = register(uid=uid, password=password)
        user1.save()

        user2 = User.find_with_uid(uid)
        self.assertEqual(user1, user2)

        user2.delete_instance(recursive=True)
        user3 = User.find_with_uid(uid)
        self.assertIsNone(user3)


class TestPasswordEncryption(TestCase):

    def test_correct_password(self):

        uid, password = uuid4().hex, uuid4().hex
        user = register(uid, password)

        credentials = user.credentials.get()
        self.assertTrue(credentials.belongs_to(user))

        self.assertTrue(credentials.does_match(password))

        random_password = uuid4().hex
        self.assertFalse(credentials.does_match(random_password))

    def test_change_password(self):

        uid, password = uuid4().hex, uuid4().hex
        user = register(uid, password)

        new_password = uuid4().hex
        change_password(uid, password, new_password)

    def test_change_password_exceptions(self):

        uid, password = uuid4().hex, uuid4().hex
        user = register(uid, password)

        wrong_password = uuid4().hex
        self.assertRaises(WrongPassword, change_password, uid, wrong_password, uuid4().hex)
        self.assertRaises(UserWasNotFound, change_password, uuid4().hex, wrong_password, uuid4().hex)


class TestAuthTokens(TestCase):

    def test_jwt_token_validation(self):
        pass

    def test_jwt_token_expiration(self):
        pass

    def test_refresh_token_jwt_request(self):
        pass

    def test_invalid_jwt_token(self):
        pass

    def test_kill_sessions(self):
        pass


class TestLogout(TestCase):

    def test_logout(self):
        pass


if __name__ == '__main__':
    create_db()
    create_secret()
    main()
