import os

import redis
from loguru import logger


class MyRedis:
    """
    class for redis
    created for testing functions with redis through tests
    same as in generator, but less functions
    Made two for independed approach in containers
    """

    __slots__ = ("host", "port", "db", "my_r")

    def __init__(self) -> None:
        self.host = os.getenv("REDIS_HOST")
        self.port = os.getenv("REDIS_PORT")
        self.db = os.getenv("REDIS_DB")
        if not all([self.host, self.port, self.db]):
            raise ValueError(
                f"some of values are empty({self.host, self.port, self.db})"
            )
        self.my_r = None

    def _check_redis(func):
        """
        wrapper for checking if redis object was initialized
        if not - goes for it
        made for testing purposes
        """

        def wrapper(self, *args, **kwargs):
            if self.my_r is None:
                self.connect_to_redis()
            return func(self, *args, **kwargs)

        return wrapper

    def connect_to_redis(self):
        """
        when using functions that were not written in this class - you will need to connect to redis.
        """
        self.my_r = redis.Redis(host=self.host, port=self.port, db=self.db)

    @_check_redis
    def get_list_from_redis(self, key, from_value=0) -> list:
        """
        Get whole list of elements from key

        - key:
            key of value in db
        - from_value:
            value to start retrieving data from db, usualy it have minus. ([-5:])
            That allows not to take whole data, but only pieces
        - return:
            returns list of elements in key
        - raise:
            raises ValueError of redis if there is no such key stored
        """
        values = []
        key_len = self.my_r.llen(key)
        if from_value < 0:
            shift = key_len + from_value
            start_index = shift if shift > 0 else 0
        elif from_value > 0:
            start_index = from_value
        else:
            start_index = 0
        for i in range(start_index, key_len):
            try:
                if key == "time":
                    values.append(float(self.my_r.lindex(key, i)))
                else:
                    values.append(int(self.my_r.lindex(key, i)))
            except ValueError as er:
                logger.error(f"on {i} we had '{er}'")
        return values
