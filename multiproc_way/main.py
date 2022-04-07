from multiprocessing import Event, Process
from time import sleep, time

from loguru import logger
from utils.data_handler import update_data

from utils.dash_main import start


def dash_process():
    logger.info("Starting dash")
    event = Event()
    producer_process = Process(target=start, kwargs={"event": event})
    producer_process.start()
    return producer_process, event


def counter_process():
    logger.info("Starting counter")
    event = Event()
    producer_process = Process(target=update_data, kwargs={"event": event})
    producer_process.start()
    return producer_process, event


def process_handler():
    c_process, counter_event = counter_process()
    checking_time = int(time())
    d_process, producer_event = dash_process()

    while True:
        # every 5 seconds checking scripts and restarting them if needed
        current_time = int(time())
        if current_time > checking_time + 1:
            checking_time = int(time())

            # if repo is updated - reload script gentle
            # if check_git() == "Updated":
            #     make_tests()
            #     if producer_process.is_alive() is True:
            #         producer_event.set()
            #         producer_process.join()
            #     producer_process, producer_event = start_producer_process()

            # checking Consumer
            if d_process.is_alive() is False:
                d_process, producer_event = dash_process()
            if c_process.is_alive() is False:
                c_process, producer_event = counter_process()


if __name__ == "__main__":
    logger.add("./logs/log.log")
    while True:
        try:
            process_handler()
        except KeyboardInterrupt:
            quit()
        except Exception as ex:
            logger.error(ex)
            sleep(15)
