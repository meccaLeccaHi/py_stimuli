#!/usr/bin/python

import threading
import time

from inputs import get_gamepad

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.curr_time = time.time()
        self.delay = delay
        self.resp_list = []
        self.resp_time = []
    def run(self):
        print "Starting " + self.name
        print_buttons(self.name, self.curr_time, \
        self.delay, self.resp_list, self.resp_time)
        print "Exiting " + self.name
        return self.resp_list, self.resp_time

# Define a function for the thread
def print_buttons( threadName, curr_time, delay, resp_list, resp_time):
    while time.time()-curr_time < delay:
        if exitFlag:
            threadName.exit()
        events = get_gamepad()
        for event in events:
            if event.state==1:
#                print(event.ev_type, event.code, event.state)
                resp_list.append(event.code)
                resp_time.append(time.time()-curr_time)
    return resp_list, resp_time

# Create new threads
thread1 = myThread(1, "Thread-1", 15)
#thread2 = myThread(2, "Thread-2", 3)

# Start new Threads
thread1.start()
#thread2.start()
for i in range(25):
    time.sleep(1)
    print(str(i))
    
thread1.join()
print thread1.resp_list
print thread1.resp_time

print "Exiting Main Thread"