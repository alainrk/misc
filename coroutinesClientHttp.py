'''
Thanks to A. Jesse Jiryu Davis "How Do Python Coroutines Work?"

Give this to get easily 2 http server in bash:
while true; do echo -e "HTTP/1.1 200 OK\n\n $(date)" | nc -l -p 1400 -q 1 < file.html; done
while true; do echo -e "HTTP/1.1 200 OK\n\n $(date)" | nc -l -p 1500 -q 1 < file.html; done

'''

from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
import socket
import time

selector = DefaultSelector()
n_tasks = 0

# Pending event i am waiting for
class Future:
    def __init__(self):
        self.callbacks = []

    # Executes all the callback i have pending
    def resolve(self):
        for c in self.callbacks:
            c()

class Task:
    def __init__(self, gen):
        self.gen = gen
        self.step()

    def step(self):
        try:
            f = next(self.gen)
        except StopIteration:
            return
        f.callbacks.append(self.step)

def get(port):
    global n_tasks
    n_tasks += 1

    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(("localhost",port))
    except BlockingIOError:
        pass
    req = 'GET %s HTTP/1.0\n\n' % "/"

    f = Future()
    selector.register(s.fileno(), EVENT_WRITE, data=f) # Register for events WRITE on socket

    # need pause until s is writable
    yield f # Resume here

    selector.unregister(s.fileno())
    # if i didnt wait socket wouldnt have git connected, so writable!
    s.send(req.encode())

    chunks = []

    while True:
        f = Future()
        selector.register(s.fileno(), EVENT_READ, data=f) # Register for events READ on socket
        yield f # Resume here
        # s is readable!
        selector.unregister(s.fileno())
        chunk = s.recv(1000)
        if chunk:
            chunks.append(chunk)
        else:
            body = (b''.join(chunks)).decode()
            print(body)
            n_tasks -= 1
            return

start = time.time()
Task(get(1500))
Task(get(1400))

while n_tasks:
    events = selector.select()
    for event, mask in events:
        fut = event.data
        fut.resolve()

print ("Time took: %f sec" % (time.time() - start))
