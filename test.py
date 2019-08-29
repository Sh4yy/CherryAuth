from unittest import TestCase, main
from app import create_db, create_secret
from controllers import *
from uuid import uuid4
from random import choices, randint, choice
from datetime import timedelta
from Utils import JWT
from time import sleep
from string import ascii_letters


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

    def test_login(self):

        uid, password = uuid4().hex, uuid4().hex
        user = register(uid=uid, password=password)
        session = login(uid, password)
        self.assertTrue(session.belongs_to(user))

        self.assertRaises(UserWasNotFound, login, uuid4().hex, password)
        self.assertRaises(IncorrectCredentials, login, uid, password + "1")

    def test_session_query(self):

        uid, password = uuid4().hex, uuid4().hex
        user = register(uid=uid, password=password)
        session = login(uid, password)

        session1 = Session.find_with_refresh_token(session.refresh_token)
        self.assertEqual(session, session1)

        session2 = Session.find_with_session_id(session.session_id)
        self.assertEqual(session, session2)


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

        self.assertTrue(change_password(uid, password, new_password))
        credentials = user.credentials.get()

        self.assertTrue(credentials.does_match(new_password))
        self.assertFalse(credentials.does_match(password))

    def test_change_password_exceptions(self):

        uid, password = uuid4().hex, uuid4().hex
        register(uid, password)

        wrong_password = uuid4().hex
        self.assertRaises(WrongPassword, change_password, uid, wrong_password, uuid4().hex)
        self.assertRaises(UserWasNotFound, change_password, uuid4().hex, wrong_password, uuid4().hex)


class TestAuthTokens(TestCase):

    def test_jwt_token_validation(self):

        uid, password = uuid4().hex, uuid4().hex
        register(uid, password)

        session = login(uid, password)
        jwt_token, payload1 = session.gen_jwt(ttl=timedelta(minutes=5).total_seconds())

        payload2 = verify_jwt_token(jwt_token)

        self.assertEqual(payload1, payload2)

    def test_jwt_token_expiration(self):

        uid, password = uuid4().hex, uuid4().hex
        register(uid, password)

        session = login(uid, password)
        jwt_token, payload1 = session.gen_jwt(ttl=timedelta(seconds=5).total_seconds())

        sleep(6)
        self.assertRaises(JWT.ExpiredSignatureError, verify_jwt_token, jwt_token)

    def test_jwt_cache(self):

        uid, password = uuid4().hex, uuid4().hex
        user = register(uid, password)
        token, payload = login(uid, password).gen_jwt(ttl=3600)

        # perform jwt verification
        self.assertEqual(verify_jwt_token(token)['uid'], user.uid)

        # perform jwt from cache
        for _ in range(1000):
            self.assertEqual(verify_jwt_token(token)['uid'], user.uid)

    def test_jwt_invalid_signature(self):

        uid, password = uuid4().hex, uuid4().hex
        register(uid, password)
        session = login(uid, password)
        jwt_token, payload = session.gen_jwt(ttl=100)
        header, payload, signature = jwt_token.decode().split('.')
        sign_list = list(signature)
        sign_list[randint(0, len(signature) - 1)] = choice(ascii_letters)

        signature = ''.join(sign_list)
        jwt_token_new = f"{header}.{payload}.{signature}".encode()
        self.assertRaises(JWT.InvalidSignatureError, verify_jwt_token, jwt_token_new)

    def test_refresh_token_jwt_request(self):

        uid, password = uuid4().hex, uuid4().hex
        register(uid, password)
        session = login(uid, password)
        jwt_token, payload = session.gen_jwt(ttl=5)
        sleep(6)

        session2 = refresh_token(session.refresh_token)
        jwt_token, _ = session2.gen_jwt(ttl=5)

        payload1 = verify_jwt_token(jwt_token)

        self.assertEqual(payload['uid'], payload1['uid'])

    def test_kill_sessions(self):

        uid, password = uuid4().hex, uuid4().hex
        user = register(uid, password)

        for _ in range(10):
            session = login(uid, password)
            logout(session.refresh_token)

        self.assertEqual(Session.find_with_user(user), [])
        for _ in range(10):
            login(uid, password)

        self.assertTrue(terminate_sessions(uid))
        self.assertEqual(Session.find_with_user(user), [])


class TestLogout(TestCase):

    def test_logout(self):

        uid, password = uuid4().hex, uuid4().hex
        user = register(uid, password)

        session = login(uid, password)
        logout(session.refresh_token)

        self.assertEqual(Session.find_with_user(user), [])


if __name__ == '__main__':
    create_db()
    create_secret()
    main()
