import threading
import datetime
from pytz import timezone
from threading import Thread, Event
import time
from trains import Train

class TrainThread(Thread):
    def __init__(self, event):
        self.train = Train()
        Thread.__init__(self)
        self.stopped = event
        self.next_three = self.train.get_next()
    
    def run(self):
        while not self.stopped.wait(30):
            now = datetime.datetime.now(timezone("Europe/Berlin")).strftime("%H:%M")
            if now >= self.next_three[0]:
                self.next_three = self.train.get_next()



if __name__ == '__main__':
    stopFlag = Event()
    thread = TrainThread(stopFlag)
    thread.daemon = True
    thread.start()
    while True:
        time.sleep(1)