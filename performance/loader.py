import os
import sys
import time
import httpx
import threading

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import edge_http

limits = httpx.Limits(max_keepalive_connections=None, max_connections=None, keepalive_expiry=None)


def login(i: int):
    s = edge_http.Client("https://compute.lorenzogiorgi.com/orchestrator/login", str(i), str(i), True, verify=True,
                         http2=True, timeout=None, limits=limits)


thread_list = []
for i in range(0, 3*999):
    x = threading.Thread(target=login, args=(i,))
    x.start()
    time.sleep(0.05)
    thread_list.append(x)
for elem in thread_list:
    elem.join()
    exit(0)

thread_list = []
for i in range(50, 100):
    x = threading.Thread(target=login, args=(i,))
    x.start()
    thread_list.append(x)
for elem in thread_list:
    elem.join()

thread_list = []
for i in range(100, 150):
    x = threading.Thread(target=login, args=(i,))
    x.start()
    thread_list.append(x)
    for elem in thread_list:
        elem.join()

thread_list = []
for i in range(150, 200):
    x = threading.Thread(target=login, args=(i,))
    x.start()
    thread_list.append(x)
for elem in thread_list:
    elem.join()

thread_list = []
for i in range(200, 250):
    x = threading.Thread(target=login, args=(i,))
    x.start()
    thread_list.append(x)
for elem in thread_list:
    elem.join()

thread_list = []
for i in range(250, 300):
    x = threading.Thread(target=login, args=(i,))
    x.start()
    thread_list.append(x)
for elem in thread_list:
    elem.join()

thread_list = []
for i in range(300, 350):
    x = threading.Thread(target=login, args=(i,))
    x.start()
    thread_list.append(x)
for elem in thread_list:
    elem.join()

thread_list = []
for i in range(350, 400):
    x = threading.Thread(target=login, args=(i,))
    x.start()
    thread_list.append(x)
for elem in thread_list:
    elem.join()

thread_list = []
for i in range(400, 450):
    x = threading.Thread(target=login, args=(i,))
    x.start()
    thread_list.append(x)
for elem in thread_list:
    elem.join()
