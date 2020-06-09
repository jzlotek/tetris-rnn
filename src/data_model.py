import queue
import time
import loguru
import datetime
import glob
import json
import numpy as np
import os
import shutil


class Instance:
    def __init__(self, board: np.ndarray, last_move, current_move, next_piece):
        self.board = board.tolist()
        try:
            self.last_move = last_move.tolist()
        except Exception:
            self.last_move = last_move
        self.current_move = current_move.tolist()
        self.next_piece = next_piece

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class DataStore:

    def __init__(self, file_name):
        self.file_name = file_name
        self.queue = queue.Queue()
        self.running = False
        self.saving = False
        self.logger = loguru.logger

    def run(self):
        if not os.path.isdir('tmp'):
            os.makedirs('tmp')
        self.running = True
        while self.running or not self.queue.empty():
            if self.queue.empty():
                time.sleep(5)
                self.logger.info("Write Queue Empty... Sleeping")
                continue
            head = self.queue.get_nowait()
            with open(
                f"tmp/{self.file_name}_" +
                    f"{datetime.datetime.now().strftime('%Y%m%d-%H%M%S%f')}" +
                    ".json.tmp",
                'w'
            ) as tmpfile:
                tmpfile.write(head)

        while self.saving:
            time.sleep(0.1)

    def write(self, data):
        self.queue.put_nowait(str(data))

    def stop(self):
        self.logger.info("Waiting for save queue to finish writing to disk")
        self.saving = True
        self.running = False
        while not self.queue.empty():
            time.sleep(0.1)
        g = glob.glob(f'tmp/{self.file_name}*')
        with open(
            f"{self.file_name}_" +
                f"{datetime.datetime.now().strftime('%m%d%H%M%S')}.json",
            'w'
        ) as file:
            file.write('[')
            for i, f_name in enumerate(g):
                with open(f_name, 'r') as tmp_file:
                    file.write(''.join(tmp_file.readlines()))
                    if i != len(g) - 1:
                        file.write(',\n')
            file.write(']')
        shutil.rmtree('tmp')
        self.saving = False
