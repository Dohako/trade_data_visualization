class TRedis():
    """
    pseudo-redis for testing
    """
    __slots__ = ["global_redis_dict"]
    
    def __init__(self) -> None:
        self.global_redis_dict = {}

    def rpush(self, key, val):
        if key in self.global_redis_dict:
            self.global_redis_dict[key].append(val)
        else:
            self.global_redis_dict.update({key:[val,]})
        return self.llen(key)

    def llen(self, key):
        if key in self.global_redis_dict:
            if not isinstance(self.global_redis_dict[key], list):
                raise AttributeError("no llen attribute for this key")
            return len(self.global_redis_dict[key])
        raise ValueError(f"No such key like {key}")

    def lindex(self, key, index):
        if key in self.global_redis_dict:
            if not isinstance(self.global_redis_dict[key], list):
                raise AttributeError("no lindex attribute for this key")
            return self.global_redis_dict[key][index]