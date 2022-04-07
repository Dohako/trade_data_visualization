import os
import time
from random import random
from time import sleep

import redis
from loguru import logger


def update_data(update_rate=5, create_new=True):
    while True:
        if create_new:
            my_r = connect_to_redis()
            my_r.flushdb()
            create_new = False
            update_redis("time", time.time())
            for i in range(0, 100):
                name = f"ticket_{i}"
                value = 0
                update_redis(name, value)
        else:
            update_redis("time", time.time())
            for i in range(0, 100):
                name = f"ticket_{i}"
                value = generate_movement() + get_last_value(name)
                update_redis(name, value)
        sleep(update_rate)


class RedisEnv:
    __slots__ = ("host", "port", "db")

    def __init__(self) -> None:
        # if not dotenv.load_dotenv(dotenv_path=path_to_env):
        #     raise FileNotFoundError(f".env not found in {path_to_env}")
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


def update_redis(key, val):
    my_r = connect_to_redis()
    my_r.rpush(key, val)


def get_last_value(key) -> int:
    my_r = connect_to_redis()
    key_len = my_r.llen(key)
    if key_len > 0:
        start_index = key_len - 1
        val = int(my_r.lindex(key, start_index))
        return val
    return 0


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement


if __name__ == "__main__":
    update_data(create_new=True)
