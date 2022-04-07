import os
from random import random
from time import sleep, time

import redis
from loguru import logger


def update_data(update_rate=5, create_new=True):
    """
    Pseudo data changer
    :param: update_rate: int - how often will new data be added to data list
    :param: create_new: bool - should redis be flushed or data need to be saved
    :return: None - idealy this function never stops because it is a simulation
    """
    my_redis = MyRedis()
    start_time = time()
    while True: # here I simulate work of some market places that constantly change price
        if create_new:
            my_redis.clear_rdb()
            create_new = False
            value = 0
        else:
            value = generate_movement() + my_redis.get_last_value(key=name)

        my_redis.update_redis("time",time())
        for i in range(0, 100):
            name = f"ticket_{i}"
            my_redis.update_redis(key=name, val=value)

        sleep(update_rate - (time()-start_time) % update_rate)


class MyRedis:
    """
    class for redis
    created for testing functions with redis through tests
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
        def wrapper(self,*args,**kwargs):
            if self.my_r is None:
                self.connect_to_redis()
            return func(self,*args,**kwargs)
        return wrapper

    def connect_to_redis(self):
        """
        when using functions that were not written in this class - you will need to connect to redis.
        """
        self.my_r = redis.Redis(host=self.host, port=self.port, db=self.db)

    @_check_redis
    def clear_rdb(self):
        self.my_r.flushdb()
        
    @_check_redis
    def update_redis(self, key, val:int|float):
        if isinstance(val, int) or isinstance(val, float):
            return self.my_r.rpush(key, val)
        raise ValueError(f"Only float or int as values for next converting, got {type(val)} instead")

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
