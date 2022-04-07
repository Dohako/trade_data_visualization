import os

import redis
from loguru import logger


class RedisEnv:
    __slots__ = ("host", "port", "db")

    def __init__(self) -> None:
        self.host = os.getenv("REDIS_HOST")
        self.port = os.getenv("REDIS_PORT")
        self.db = os.getenv("REDIS_DB")
        if not all([self.host, self.port, self.db]):
            raise ValueError(
                f"some of values are empty({self.host, self.port, self.db})"
            )


def connect_to_redis():
    r_env = RedisEnv()
    my_r = redis.Redis(host=r_env.host, port=r_env.port, db=r_env.db)
    return my_r


def get_list_from_redis(key, from_value=0) -> list:
    my_r = connect_to_redis()
    values = []
    key_len = my_r.llen(key)
    if from_value < 0:
        shift = key_len + from_value
        start_index = shift if shift > 0 else 0
    else:
        start_index = 0
    for i in range(start_index, key_len):
        try:
            if key == "time":
                values.append(float(my_r.lindex(key, i)))
            else:
                values.append(int(my_r.lindex(key, i)))
        except ValueError as er:
            logger.error(f"on {i} we had '{er}'")
    return values
