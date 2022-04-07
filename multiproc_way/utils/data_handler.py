from random import random
from time import sleep
import json
import os
import time
from loguru import logger


def update_data(event=None, update_rate=5, create_new=True):
    while True:
        if create_new:
            data = {}
            if "time" not in data:
                data.update({"time":[time.time(),]})
            else:
                data["time"].append(time.time())
            for i in range(0,100):
                name = f"ticket_{i}"
                value = 0
                if name not in data:
                    data.update({name:[value]})
                else:
                    data[name].append(value)
            if not os.path.exists("./data"):
                os.mkdir("./data")
            with open(f"./data/data.json", 'w', encoding='utf-8') as f:
                json.dump(data, f)
            create_new = False
    
        else:
            with open(f"./data/data.json", 'r', encoding='utf-8') as f:
                data:dict = json.load(f)
            if "time" not in data:
                data.update({"time":[time.time(),]})
            else:
                data["time"].append(time.time())
            for i in range(0,100):
                name = f"ticket_{i}"
                value = generate_movement()
                if name not in data:
                    data.update({name:[value]})
                else:
                    data[name].append(value + data[name][-1])
            with open(f"./data/data.json", 'w', encoding='utf-8') as f:
                json.dump(data, f)
        if event and event.is_set():
            logger.info("breaking")
            break
        sleep(update_rate)

def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement


if __name__ == "__main__":
    update_data(create_new=True)

