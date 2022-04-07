import os
import time
from random import random
from time import sleep

import redis
from loguru import logger


def update_data(update_rate=5, create_new=True):
    my_redis = MyRedis()
    my_redis.connect_to_redis()
    my_r = my_redis.my_r
    while True:
        if create_new:
            my_r.flushdb()
            create_new = False
            my_redis.update_redis("time", time.time())
            for i in range(0, 100):
                name = f"ticket_{i}"
                value = 0
                my_redis.update_redis(key=name, val=value)
        else:
            my_redis.update_redis("time", time.time())
            for i in range(0, 100):
                name = f"ticket_{i}"
                value = generate_movement() + my_redis.get_last_value(key=name)
                my_redis.update_redis(key=name, val=value)
        sleep(update_rate)


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
        def wrapper(self,*args,**kwargs):
            if self.my_r is None:
                self.connect_to_redis()
            return func(self,*args,**kwargs)
        return wrapper

    def connect_to_redis(self):
        logger.info("connecting")
        self.my_r = redis.Redis(host=self.host, port=self.port, db=self.db)
        
    @_check_redis
    def update_redis(self, key, val):
        self.my_r.rpush(key, val)

    @_check_redis
    def get_last_value(self, key) -> int:
        key_len = self.my_r.llen(key)
        if key_len > 0:
            start_index = key_len - 1
            val = int(self.my_r.lindex(key, start_index))
            return val
        return 0


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement


if __name__ == "__main__":
    update_data(create_new=True)
    # r = MyRedis()
    # r.update_redis("1",2)
