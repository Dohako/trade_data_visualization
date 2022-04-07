import os

import redis
from loguru import logger


class MyRedis:
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
        def wrapper(self, *args, **kwargs):
            if self.my_r is None:
                self.connect_to_redis()
            return func(self, *args, **kwargs)

        return wrapper

    def connect_to_redis(self):
        self.my_r = redis.Redis(host=self.host, port=self.port, db=self.db)

    @_check_redis
    def get_list_from_redis(self, key, from_value=0) -> list:
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
