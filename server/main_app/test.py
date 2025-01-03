import time

from utils.log import logging

counter = 0
while True:
    time.sleep(1)
    # print(counter)
    logging.info(counter)
    counter += 1
