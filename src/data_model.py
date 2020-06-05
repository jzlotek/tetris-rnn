import queue
import time
import loguru
import threading


class DataStore:

    def __init__(self, file_name):
        self.queue = queue.Queue()
        self.file_p = open(file_name, 'r')
        self.running = False
        self.saving = False
        self.logger = loguru.logger


    def run(self):
        self.running = True
        while self.running:
            while not self.queue.empty():
                self.logger.info("Writing {} elements from queue", len(self.queue))
                l = self.queue.get_nowait()
                self.file_p.write(l)
            self.logger.info("Write Queue Empty... Sleeping")
            time.sleep(5)

        self.logger.info("Waiting for save queue to finish writing to disk")
        while self.saving:
            time.sleep(1)


    def write(self, data):
        self.queue.put_nowait(str(data))


    def stop(self):
        self.saving = True
        self.running = False
        while not self.queue.empty():
            time.sleep(0.1)
        self.file_p.close()
        self.saving = False
