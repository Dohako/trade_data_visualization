"""
For my testing purpose
"""

import json
import os

import dotenv
import redis
from loguru import logger


class RedisEnv:
    __slots__ = ("host", "port", "db")

    def __init__(self, path_to_env=".env") -> None:
        if not dotenv.load_dotenv(dotenv_path=path_to_env):
            raise FileNotFoundError(f".env not found in {path_to_env}")
        self.host = os.getenv("REDIS_HOST")
        self.port = os.getenv("REDIS_PORT")
        self.db = os.getenv("REDIS_DB")
        if not all([self.host, self.port, self.db]):
            raise ValueError(
                f"some of values are empty({self.host, self.port, self.db})"
            )


def connect_to_redis(path_to_env=".env"):
    r_env = RedisEnv(path_to_env)
    my_r = redis.Redis(host=r_env.host, port=r_env.port, db=r_env.db)
    return my_r


def update_redis_2():
    my_r = connect_to_redis()
    menu_base = {"test_1": {"test_3": [1, 2, 3], "test_4": 6}, "test2": 3}
    with my_r.pipeline() as pipe:
        for h_id, menu in menu_base.items():
            pipe.set(h_id, json.dumps(menu))
        pipe.execute()


def get_dict_from_redis(key) -> dict:
    my_r = connect_to_redis()
    redis_table = my_r.get(key)
    table = json.loads(redis_table)
    return table


def get_list_from_redis(key) -> list:
    my_r = connect_to_redis()
    values = []
    for i in range(0, my_r.llen(key)):
        try:
            values.append(int(my_r.lindex(key, i)))
        except ValueError as er:
            logger.error(f"on {i} we had {er}")
    return values
