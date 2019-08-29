from Utils import redis
import json


class Cache:

    @staticmethod
    def lookup_jwt(jwt_token: str):
        """
        lookup jwt payload
        :param jwt_token: targeted jwt token
        :return: payload as json if found
        """

        payload_str = redis.get(jwt_token)
        if not payload_str:
            return None

        return json.loads(payload_str)

    @classmethod
    def set_jwt(cls, jwt_token: str, payload: dict, ttl: int):
        """
        set a new jwt token and its corresponding payload
        :param jwt_token: targeted jwt_token
        :param payload: payload
        :param ttl: time to live for the cache
        :return: True on success
        """

        payload_str = json.dumps(payload)
        redis.set(jwt_token, payload_str, ex=ttl)
        return True
